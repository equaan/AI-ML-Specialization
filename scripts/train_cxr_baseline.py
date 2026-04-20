from __future__ import annotations

import argparse
import copy
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.training.cxr_dataset import CXR_FINDINGS, CxrDataset, CxrRecord, load_kaggle_cxr_records
from backend.training.cxr_model import CxrFindingsCNN
from backend.utils.data_paths import canonical_cxr_dir


DEFAULT_DATASET_DIR = canonical_cxr_dir()
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "models" / "cxr_baseline"


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def _subsample_records(records: list[CxrRecord], max_samples: int, seed: int) -> list[CxrRecord]:
    if max_samples >= len(records):
        return records
    rng = random.Random(seed)
    copied = records.copy()
    rng.shuffle(copied)
    return copied[:max_samples]


def _compute_pos_weight(records: list[CxrRecord]) -> torch.Tensor:
    positives = [0.0 for _ in CXR_FINDINGS]
    for record in records:
        for index, value in enumerate(record.finding_targets):
            positives[index] += float(value)

    total = float(len(records))
    weights: list[float] = []
    for positive in positives:
        negative = max(total - positive, 1.0)
        denom = positive if positive > 0 else 1.0
        weights.append(negative / denom)

    return torch.tensor(weights, dtype=torch.float32)


def _evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    model.eval()
    all_probs: list[torch.Tensor] = []
    all_targets: list[torch.Tensor] = []

    with torch.no_grad():
        for inputs, targets in loader:
            inputs = inputs.to(device)
            logits = model(inputs)
            probs = torch.sigmoid(logits).detach().cpu()
            all_probs.append(probs)
            all_targets.append(targets.detach().cpu())

    if not all_probs:
        return {
            "macro_f1": 0.0,
            "per_finding": {name: {"precision": 0.0, "recall": 0.0, "f1": 0.0} for name in CXR_FINDINGS},
        }

    probs = torch.cat(all_probs, dim=0)
    targets = torch.cat(all_targets, dim=0)
    preds = (probs >= 0.5).float()

    per_finding: dict[str, dict[str, float]] = {}
    f1_values: list[float] = []
    for index, finding in enumerate(CXR_FINDINGS):
        pred_col = preds[:, index]
        target_col = targets[:, index]

        tp = float(((pred_col == 1) & (target_col == 1)).sum().item())
        fp = float(((pred_col == 1) & (target_col == 0)).sum().item())
        fn = float(((pred_col == 0) & (target_col == 1)).sum().item())

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        per_finding[finding] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }
        f1_values.append(f1)

    macro_f1 = sum(f1_values) / len(f1_values) if f1_values else 0.0
    return {
        "macro_f1": round(macro_f1, 4),
        "per_finding": per_finding,
    }


def train(
    dataset_dir: Path,
    output_dir: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    seed: int,
    image_size: int,
    max_train_samples: int | None = None,
) -> dict:
    set_seed(seed)

    train_records = load_kaggle_cxr_records(dataset_dir, split="train")
    val_records = load_kaggle_cxr_records(dataset_dir, split="val")
    test_records = load_kaggle_cxr_records(dataset_dir, split="test")

    if max_train_samples:
        train_records = _subsample_records(train_records, max_samples=max_train_samples, seed=seed)

    train_dataset = CxrDataset(train_records, image_size=image_size)
    val_dataset = CxrDataset(val_records, image_size=image_size)
    test_dataset = CxrDataset(test_records, image_size=image_size)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CxrFindingsCNN().to(device)
    pos_weight = _compute_pos_weight(train_records).to(device)
    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    history: list[dict] = []
    best_val_macro_f1 = -1.0
    best_state_dict: dict[str, torch.Tensor] | None = None
    best_epoch = 0

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        sample_count = 0

        for inputs, targets in train_loader:
            inputs = inputs.to(device)
            targets = targets.to(device)

            optimizer.zero_grad()
            logits = model(inputs)
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item()) * int(targets.size(0))
            sample_count += int(targets.size(0))

        train_loss = (running_loss / sample_count) if sample_count else 0.0
        val_metrics = _evaluate(model, val_loader, device)
        val_macro_f1 = float(val_metrics["macro_f1"])

        history.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_macro_f1": round(val_macro_f1, 4),
            }
        )

        if val_macro_f1 > best_val_macro_f1:
            best_val_macro_f1 = val_macro_f1
            best_state_dict = copy.deepcopy(model.state_dict())
            best_epoch = epoch

    if best_state_dict is not None:
        model.load_state_dict(best_state_dict)

    test_metrics = _evaluate(model, test_loader, device)

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "cxr_findings_baseline.pt"
    metrics_path = output_dir / "cxr_findings_baseline_metrics.json"

    torch.save(
        {
            "state_dict": model.state_dict(),
            "finding_names": CXR_FINDINGS,
            "image_size": image_size,
            "dataset_type": "kaggle_pneumonia_proxy_labels",
            "notes": "Only pneumonia and consolidation are supervised from Kaggle labels.",
        },
        model_path,
    )

    finding_positive_counts = Counter()
    for record in train_records:
        for index, value in enumerate(record.finding_targets):
            if value > 0:
                finding_positive_counts[CXR_FINDINGS[index]] += 1

    metrics = {
        "dataset": "kaggle_pneumonia",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_dir": str(dataset_dir),
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "image_size": image_size,
        "device": str(device),
        "split_sizes": {
            "train": len(train_records),
            "validation": len(val_records),
            "test": len(test_records),
        },
        "supervised_findings": {
            finding: int(finding_positive_counts.get(finding, 0))
            for finding in CXR_FINDINGS
        },
        "history": history,
        "best_validation_macro_f1": round(best_val_macro_f1, 4),
        "best_validation_epoch": best_epoch,
        "test_macro_f1": test_metrics["macro_f1"],
        "test_per_finding": test_metrics["per_finding"],
        "model_path": str(model_path),
        "labeling_note": "Kaggle baseline provides direct supervision for pneumonia; consolidation is proxied.",
    }

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train chest X-ray findings baseline model.")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR, help="Path to CXR dataset.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Learning rate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--image-size", type=int, default=224, help="Square image size.")
    parser.add_argument("--max-train-samples", type=int, default=None, help="Optional train cap for smoke run.")
    args = parser.parse_args()

    metrics = train(
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        seed=args.seed,
        image_size=args.image_size,
        max_train_samples=args.max_train_samples,
    )

    print(f"Training complete. Test macro-F1: {metrics['test_macro_f1']}")
    print(f"Model saved to: {metrics['model_path']}")
    print(f"Metrics saved to: {args.output_dir / 'cxr_findings_baseline_metrics.json'}")


if __name__ == "__main__":
    main()
