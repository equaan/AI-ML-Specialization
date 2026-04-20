from __future__ import annotations

import argparse
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

from backend.training.ham10000_dataset import (
    CLASS_TO_INDEX,
    HAM10000_CLASSES,
    Ham10000Record,
    Ham10000Dataset,
    load_ham10000_records,
    split_records,
)
from backend.utils.data_paths import canonical_ham10000_dir


DEFAULT_DATASET_DIR = canonical_ham10000_dir()
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_baseline"


class Ham10000BaselineCNN(nn.Module):
    def __init__(self, num_classes: int = len(HAM10000_CLASSES)) -> None:
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.AdaptiveAvgPool2d((4, 4)),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 4 * 4, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, num_classes),
        )

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(inputs))


def set_seed(seed: int) -> None:
    random.seed(seed)
    torch.manual_seed(seed)


def _subsample_records(records: list[Ham10000Record], max_samples: int, seed: int) -> list[Ham10000Record]:
    if max_samples >= len(records):
        return records

    rng = random.Random(seed)
    grouped: dict[str, list[Ham10000Record]] = {}
    for record in records:
        grouped.setdefault(record.label, []).append(record)

    sampled: list[Ham10000Record] = []
    for label_records in grouped.values():
        rng.shuffle(label_records)
        sampled.append(label_records[0])

    remaining_pool = [record for record in records if record not in sampled]
    rng.shuffle(remaining_pool)
    slots_left = max_samples - len(sampled)
    sampled.extend(remaining_pool[: max(0, slots_left)])
    rng.shuffle(sampled)
    return sampled[:max_samples]


def _accuracy(model: nn.Module, loader: DataLoader, device: torch.device) -> float:
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            logits = model(inputs)
            preds = logits.argmax(dim=1)
            correct += int((preds == labels).sum().item())
            total += int(labels.numel())
    return (correct / total) if total else 0.0


def train(
    dataset_dir: Path,
    output_dir: Path,
    epochs: int,
    batch_size: int,
    learning_rate: float,
    seed: int,
    image_size: int,
    max_samples: int | None = None,
) -> dict:
    set_seed(seed)
    records = load_ham10000_records(dataset_dir)
    if max_samples:
        records = _subsample_records(records, max_samples=max_samples, seed=seed)
    if not records:
        raise RuntimeError("No HAM10000 records available for training.")

    train_records, val_records, test_records = split_records(records, seed=seed)
    train_dataset = Ham10000Dataset(train_records, image_size=image_size)
    val_dataset = Ham10000Dataset(val_records, image_size=image_size)
    test_dataset = Ham10000Dataset(test_records, image_size=image_size)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = Ham10000BaselineCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    history: list[dict] = []
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
        val_accuracy = _accuracy(model, val_loader, device)
        history.append(
            {
                "epoch": epoch,
                "train_loss": round(train_loss, 4),
                "val_accuracy": round(val_accuracy, 4),
            }
        )

    test_accuracy = _accuracy(model, test_loader, device)

    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "ham10000_baseline.pt"
    metrics_path = output_dir / "ham10000_baseline_metrics.json"

    torch.save(
        {
            "state_dict": model.state_dict(),
            "class_names": HAM10000_CLASSES,
            "image_size": image_size,
        },
        model_path,
    )

    metrics = {
        "dataset": "HAM10000",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_dir": str(dataset_dir),
        "class_to_index": CLASS_TO_INDEX,
        "split_sizes": {
            "train": len(train_records),
            "validation": len(val_records),
            "test": len(test_records),
        },
        "label_distribution": dict(sorted(Counter(record.label for record in records).items())),
        "epochs": epochs,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "image_size": image_size,
        "device": str(device),
        "history": history,
        "test_accuracy": round(test_accuracy, 4),
        "model_path": str(model_path),
    }
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a baseline HAM10000 skin lesion classifier.")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATASET_DIR, help="Path to HAM10000 dataset.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Output directory for model and metrics.")
    parser.add_argument("--epochs", type=int, default=3, help="Number of training epochs.")
    parser.add_argument("--batch-size", type=int, default=32, help="Training batch size.")
    parser.add_argument("--learning-rate", type=float, default=1e-3, help="Optimizer learning rate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed.")
    parser.add_argument("--image-size", type=int, default=128, help="Square image size for training.")
    parser.add_argument("--max-samples", type=int, default=None, help="Optional cap for quick smoke runs.")
    args = parser.parse_args()

    metrics = train(
        dataset_dir=args.dataset_dir,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.learning_rate,
        seed=args.seed,
        image_size=args.image_size,
        max_samples=args.max_samples,
    )

    print(f"Training complete. Test accuracy: {metrics['test_accuracy']}")
    print(f"Model saved to: {metrics['model_path']}")
    print(f"Metrics saved to: {args.output_dir / 'ham10000_baseline_metrics.json'}")


if __name__ == "__main__":
    main()
