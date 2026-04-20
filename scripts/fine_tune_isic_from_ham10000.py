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

from backend.training.ham10000_dataset import HAM10000_CLASSES, Ham10000Dataset
from backend.training.ham10000_model import Ham10000BaselineCNN
from backend.training.isic_dataset import load_isic_split


DEFAULT_ISIC_ROOT = PROJECT_ROOT / "data" / "raw" / "skin" / "isic"
DEFAULT_HAM_CHECKPOINT = PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_full_gpu_v1" / "ham10000_baseline.pt"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "models" / "isic_finetune"


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def _evaluate(model: nn.Module, loader: DataLoader, device: torch.device) -> dict:
    model.eval()
    correct = 0
    total = 0
    class_tp = Counter()
    class_total = Counter()
    class_pred = Counter()

    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            logits = model(inputs)
            preds = logits.argmax(dim=1)

            correct += int((preds == labels).sum().item())
            total += int(labels.numel())

            for label, pred in zip(labels.tolist(), preds.tolist()):
                class_total[label] += 1
                class_pred[pred] += 1
                if label == pred:
                    class_tp[label] += 1

    per_class: dict[str, dict[str, float | int]] = {}
    balanced_parts: list[float] = []
    macro_f1_parts: list[float] = []
    for idx, name in enumerate(HAM10000_CLASSES):
        support = class_total[idx]
        pred_count = class_pred[idx]
        tp = class_tp[idx]
        recall = (tp / support) if support else 0.0
        precision = (tp / pred_count) if pred_count else 0.0
        f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

        per_class[name] = {
            "support": support,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
        }
        if support:
            balanced_parts.append(recall)
            macro_f1_parts.append(f1)

    balanced = sum(balanced_parts) / len(balanced_parts) if balanced_parts else 0.0
    macro_f1 = sum(macro_f1_parts) / len(macro_f1_parts) if macro_f1_parts else 0.0
    return {
        "accuracy": round((correct / total) if total else 0.0, 4),
        "balanced_accuracy": round(balanced, 4),
        "macro_f1": round(macro_f1, 4),
        "per_class": per_class,
    }


def fine_tune(
    isic_root: Path,
    ham_checkpoint: Path,
    output_dir: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    seed: int,
    image_size: int,
) -> dict:
    set_seed(seed)
    split = load_isic_split(isic_root)

    train_dataset = Ham10000Dataset(split.train, image_size=image_size)
    val_dataset = Ham10000Dataset(split.validation, image_size=image_size)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Ham10000BaselineCNN(num_classes=len(HAM10000_CLASSES))

    if ham_checkpoint.exists():
        payload = torch.load(ham_checkpoint, map_location="cpu")
        state = payload.get("state_dict", payload)
        model.load_state_dict(state, strict=False)

    model = model.to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    history: list[dict] = []
    best_val_balanced = -1.0
    best_state_dict: dict[str, torch.Tensor] | None = None
    best_epoch = 0

    for epoch in range(1, epochs + 1):
        model.train()
        running_loss = 0.0
        sample_count = 0

        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            logits = model(inputs)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item()) * int(labels.size(0))
            sample_count += int(labels.size(0))

        train_loss = (running_loss / sample_count) if sample_count else 0.0
        val_metrics = _evaluate(model, val_loader, device)
        val_balanced = float(val_metrics["balanced_accuracy"])

        history.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_accuracy": val_metrics["accuracy"],
                "val_balanced_accuracy": val_metrics["balanced_accuracy"],
                "val_macro_f1": val_metrics["macro_f1"],
            }
        )

        if val_balanced > best_val_balanced:
            best_val_balanced = val_balanced
            best_state_dict = copy.deepcopy(model.state_dict())
            best_epoch = epoch

    if best_state_dict is not None:
        model.load_state_dict(best_state_dict)

    final_metrics = _evaluate(model, val_loader, device)

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "isic_finetuned_from_ham10000.pt"
    metrics_path = output_dir / "isic_finetune_metrics.json"

    torch.save(
        {
            "state_dict": model.state_dict(),
            "class_names": HAM10000_CLASSES,
            "image_size": image_size,
            "base_checkpoint": str(ham_checkpoint),
        },
        model_path,
    )

    metrics = {
        "dataset": "ISIC2018_Task3",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "isic_root": str(isic_root),
        "base_checkpoint": str(ham_checkpoint),
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "image_size": image_size,
        "device": str(device),
        "split_sizes": {"train": len(split.train), "validation": len(split.validation)},
        "history": history,
        "best_validation_balanced_accuracy": round(best_val_balanced, 4),
        "best_validation_epoch": best_epoch,
        "validation_metrics": final_metrics,
        "model_path": str(model_path),
    }

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Fine-tune HAM10000 classifier on ISIC Task 3 labels.")
    parser.add_argument("--isic-root", type=Path, default=DEFAULT_ISIC_ROOT, help="ISIC root directory.")
    parser.add_argument("--ham-checkpoint", type=Path, default=DEFAULT_HAM_CHECKPOINT, help="Base HAM10000 checkpoint.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory.")
    parser.add_argument("--epochs", type=int, default=3, help="Fine-tune epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size.")
    parser.add_argument("--learning-rate", type=float, default=5e-4, help="Learning rate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--image-size", type=int, default=128, help="Image size.")
    args = parser.parse_args()

    metrics = fine_tune(
        isic_root=args.isic_root,
        ham_checkpoint=args.ham_checkpoint,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        seed=args.seed,
        image_size=args.image_size,
    )

    print(f"Fine-tuning complete. Validation balanced accuracy: {metrics['validation_metrics']['balanced_accuracy']}")
    print(f"Model saved to: {metrics['model_path']}")
    print(f"Metrics saved to: {args.output_dir / 'isic_finetune_metrics.json'}")


if __name__ == "__main__":
    main()
