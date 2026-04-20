from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset


CXR_FINDINGS = [
    "consolidation",
    "effusion",
    "cardiomegaly",
    "pneumothorax",
    "pneumonia",
]
FINDING_TO_INDEX = {name: index for index, name in enumerate(CXR_FINDINGS)}


@dataclass(frozen=True)
class CxrRecord:
    image_path: Path
    finding_targets: list[float]


def _kaggle_targets_from_folder(folder_name: str) -> list[float]:
    targets = [0.0 for _ in CXR_FINDINGS]
    normalized = folder_name.lower()
    if normalized == "pneumonia":
        targets[FINDING_TO_INDEX["pneumonia"]] = 1.0
        # Kaggle pneumonia data does not include full finding labels; this is a conservative proxy.
        targets[FINDING_TO_INDEX["consolidation"]] = 1.0
    return targets


def load_kaggle_cxr_records(dataset_dir: Path, split: str) -> list[CxrRecord]:
    split_dir = dataset_dir / split
    if not split_dir.exists():
        raise FileNotFoundError(f"CXR split not found: {split_dir}")

    records: list[CxrRecord] = []
    for class_dir in split_dir.iterdir():
        if not class_dir.is_dir():
            continue
        targets = _kaggle_targets_from_folder(class_dir.name)
        for image_path in class_dir.glob("*.jpeg"):
            records.append(CxrRecord(image_path=image_path, finding_targets=targets.copy()))
        for image_path in class_dir.glob("*.jpg"):
            records.append(CxrRecord(image_path=image_path, finding_targets=targets.copy()))
        for image_path in class_dir.glob("*.png"):
            records.append(CxrRecord(image_path=image_path, finding_targets=targets.copy()))

    if not records:
        raise RuntimeError(f"No CXR images found for split: {split}")

    return records


class CxrDataset(Dataset):
    def __init__(self, records: list[CxrRecord], image_size: int = 224) -> None:
        self.records = records
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        record = self.records[index]
        image = Image.open(record.image_path).convert("RGB")
        image = image.resize((self.image_size, self.image_size))
        tensor = torch.from_numpy(np.asarray(image, dtype="float32")).permute(2, 0, 1) / 255.0
        targets = torch.tensor(record.finding_targets, dtype=torch.float32)
        return tensor, targets
