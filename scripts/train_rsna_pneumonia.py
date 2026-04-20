from __future__ import annotations

import argparse
import copy
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

import torch
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from torch import nn
from torch.utils.data import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.training.cxr_model import CxrFindingsCNN
from backend.training.rsna_dataset import RsnaDataset, RsnaRecord, load_rsna_records


DEFAULT_RSNA_DIR = PROJECT_ROOT / "data" / "raw" / "cxr" / "rsna"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "models" / "rsna_pneumonia"


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def _subsample(records: list[RsnaRecord], max_samples: int, seed: int) -> list[RsnaRecord]:
    if max_samples >= len(records):
        return records
    rng = random.Random(seed)
    shuffled = records.copy()
    rng.shuffle(shuffled)
    return shuffled[:max_samples]


def _evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    model.eval()
    probs_list: list[torch.Tensor] = []
    targets_list: list[torch.Tensor] = []

    with torch.no_grad():
        for inputs, targets in loader:
            inputs = inputs.to(device)
            logits = model(inputs)[:, :1]
            probs = torch.sigmoid(logits).detach().cpu()
            probs_list.append(probs)
            targets_list.append(targets.detach().cpu())

    probs = torch.cat(probs_list, dim=0).squeeze(1)
    targets = torch.cat(targets_list, dim=0).squeeze(1)
    preds = (probs >= 0.5).float()

    tp = float(((preds == 1) & (targets == 1)).sum().item())
    fp = float(((preds == 1) & (targets == 0)).sum().item())
    fn = float(((preds == 0) & (targets == 1)).sum().item())
    tn = float(((preds == 0) & (targets == 0)).sum().item())

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    acc = (tp + tn) / max(tp + tn + fp + fn, 1.0)

    auc = 0.0
    try:
        auc = float(roc_auc_score(targets.numpy(), probs.numpy()))
    except Exception:
        auc = 0.0

    return {
        "accuracy": round(acc, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "auc": round(auc, 4),
    }


def train(
    rsna_dir: Path,
    output_dir: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    seed: int,
    image_size: int,
    max_samples: int | None = None,
) -> dict:
    set_seed(seed)
    records = load_rsna_records(rsna_dir)
    if max_samples:
        records = _subsample(records, max_samples=max_samples, seed=seed)

    labels = [record.target for record in records]
    train_records, val_records = train_test_split(
        records,
        test_size=0.2,
        random_state=seed,
        stratify=labels,
    )

    train_dataset = RsnaDataset(train_records, image_size=image_size)
    val_dataset = RsnaDataset(val_records, image_size=image_size)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = CxrFindingsCNN(num_findings=1).to(device)

    positive_count = sum(record.target for record in train_records)
    negative_count = len(train_records) - positive_count
    pos_weight = torch.tensor([negative_count / max(positive_count, 1)], dtype=torch.float32).to(device)

    criterion = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    history: list[dict] = []
    best_val_f1 = -1.0
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
            logits = model(inputs)[:, :1]
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item()) * int(targets.size(0))
            sample_count += int(targets.size(0))

        train_loss = (running_loss / sample_count) if sample_count else 0.0
        val_metrics = _evaluate(model, val_loader, device)

        history.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_f1": val_metrics["f1"],
                "val_auc": val_metrics["auc"],
            }
        )

        if float(val_metrics["f1"]) > best_val_f1:
            best_val_f1 = float(val_metrics["f1"])
            best_state_dict = copy.deepcopy(model.state_dict())
            best_epoch = epoch

    if best_state_dict is not None:
        model.load_state_dict(best_state_dict)

    final_val = _evaluate(model, val_loader, device)

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "rsna_pneumonia_baseline.pt"
    metrics_path = output_dir / "rsna_pneumonia_baseline_metrics.json"

    torch.save(
        {
            "state_dict": model.state_dict(),
            "task": "rsna_pneumonia_binary",
            "finding_names": ["pneumonia"],
            "image_size": image_size,
        },
        model_path,
    )

    metrics = {
        "dataset": "RSNA Pneumonia Detection",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "rsna_dir": str(rsna_dir),
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "image_size": image_size,
        "device": str(device),
        "split_sizes": {"train": len(train_records), "validation": len(val_records)},
        "history": history,
        "best_validation_f1": round(best_val_f1, 4),
        "best_validation_epoch": best_epoch,
        "validation_metrics": final_val,
        "model_path": str(model_path),
    }

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train RSNA pneumonia baseline model.")
    parser.add_argument("--rsna-dir", type=Path, default=DEFAULT_RSNA_DIR, help="RSNA dataset directory.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    parser.add_argument("--epochs", type=int, default=3, help="Training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Learning rate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--image-size", type=int, default=224, help="Square image size.")
    parser.add_argument("--max-samples", type=int, default=None, help="Optional sample cap for smoke runs.")
    args = parser.parse_args()

    metrics = train(
        rsna_dir=args.rsna_dir,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        seed=args.seed,
        image_size=args.image_size,
        max_samples=args.max_samples,
    )

    print(f"Training complete. Validation F1: {metrics['validation_metrics']['f1']}")
    print(f"Model saved to: {metrics['model_path']}")
    print(f"Metrics saved to: {args.output_dir / 'rsna_pneumonia_baseline_metrics.json'}")


if __name__ == "__main__":
    main()
