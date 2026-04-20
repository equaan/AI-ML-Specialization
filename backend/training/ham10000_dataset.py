from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset


HAM10000_CLASSES = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]
CLASS_TO_INDEX = {label: index for index, label in enumerate(HAM10000_CLASSES)}
INDEX_TO_CLASS = {index: label for label, index in CLASS_TO_INDEX.items()}


@dataclass(frozen=True)
class Ham10000Record:
    image_id: str
    image_path: Path
    label: str
    label_index: int
    lesion_id: str


def discover_image_dirs(dataset_dir: Path) -> list[Path]:
    candidates = [
        dataset_dir / "HAM10000_images_part_1",
        dataset_dir / "HAM10000_images_part_2",
    ]
    existing = [candidate for candidate in candidates if candidate.exists()]
    if existing:
        return existing
    return [dataset_dir]


def load_ham10000_records(dataset_dir: Path) -> list[Ham10000Record]:
    metadata_path = dataset_dir / "HAM10000_metadata.csv"
    if not metadata_path.exists():
        raise FileNotFoundError(f"HAM10000 metadata not found at {metadata_path}")

    image_lookup: dict[str, Path] = {}
    for image_dir in discover_image_dirs(dataset_dir):
        for image_path in image_dir.glob("*.jpg"):
            image_lookup[image_path.stem] = image_path

    frame = pd.read_csv(metadata_path)
    records: list[Ham10000Record] = []
    for row in frame.itertuples(index=False):
        image_id = str(row.image_id)
        label = str(row.dx)
        image_path = image_lookup.get(image_id)
        if label not in CLASS_TO_INDEX or image_path is None:
            continue

        records.append(
            Ham10000Record(
                image_id=image_id,
                image_path=image_path,
                label=label,
                label_index=CLASS_TO_INDEX[label],
                lesion_id=str(row.lesion_id),
            )
        )
    return records


def split_records(
    records: list[Ham10000Record],
    val_fraction: float = 0.15,
    test_fraction: float = 0.15,
    seed: int = 42,
) -> tuple[list[Ham10000Record], list[Ham10000Record], list[Ham10000Record]]:
    if not records:
        raise ValueError("No HAM10000 records available for splitting.")

    labels = [record.label for record in records]
    label_counts = pd.Series(labels).value_counts()
    can_stratify_initial = (
        label_counts.min() >= 2
        and int(round(len(records) * (val_fraction + test_fraction))) >= len(label_counts)
    )
    train_records, temp_records = train_test_split(
        records,
        test_size=val_fraction + test_fraction,
        random_state=seed,
        stratify=labels if can_stratify_initial else None,
    )
    temp_labels = [record.label for record in temp_records]
    temp_label_counts = pd.Series(temp_labels).value_counts()
    test_ratio_within_temp = test_fraction / (val_fraction + test_fraction)
    can_stratify_second = (
        not temp_label_counts.empty
        and temp_label_counts.min() >= 2
        and int(round(len(temp_records) * test_ratio_within_temp)) >= len(temp_label_counts)
    )
    val_records, test_records = train_test_split(
        temp_records,
        test_size=test_ratio_within_temp,
        random_state=seed,
        stratify=temp_labels if can_stratify_second else None,
    )
    return list(train_records), list(val_records), list(test_records)


class Ham10000Dataset(Dataset):
    def __init__(self, records: list[Ham10000Record], image_size: int = 128) -> None:
        self.records = records
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, int]:
        record = self.records[index]
        image = Image.open(record.image_path).convert("RGB")
        image = image.resize((self.image_size, self.image_size))
        tensor = torch.from_numpy(np.asarray(image, dtype="float32")).permute(2, 0, 1) / 255.0
        return tensor, record.label_index
