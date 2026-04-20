from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from backend.training.ham10000_dataset import CLASS_TO_INDEX, HAM10000_CLASSES, Ham10000Record


@dataclass(frozen=True)
class IsicSplit:
    train: list[Ham10000Record]
    validation: list[Ham10000Record]


def _build_records_from_csv(csv_path: Path, images_dir: Path) -> list[Ham10000Record]:
    if not csv_path.exists():
        raise FileNotFoundError(f"ISIC labels CSV not found: {csv_path}")
    if not images_dir.exists():
        raise FileNotFoundError(f"ISIC images dir not found: {images_dir}")

    frame = pd.read_csv(csv_path)
    records: list[Ham10000Record] = []

    col_to_label = {
        "MEL": "mel",
        "NV": "nv",
        "BCC": "bcc",
        "AKIEC": "akiec",
        "BKL": "bkl",
        "DF": "df",
        "VASC": "vasc",
    }

    for row in frame.itertuples(index=False):
        image_id = str(getattr(row, "image"))
        image_path = images_dir / f"{image_id}.jpg"
        if not image_path.exists():
            continue

        label = None
        for col, mapped_label in col_to_label.items():
            value = float(getattr(row, col, 0.0))
            if value >= 0.5:
                label = mapped_label
                break
        if label is None:
            continue

        records.append(
            Ham10000Record(
                image_id=image_id,
                image_path=image_path,
                label=label,
                label_index=CLASS_TO_INDEX[label],
                lesion_id=f"isic_{image_id}",
            )
        )

    if not records:
        raise RuntimeError("No ISIC records were loaded from provided CSV/images.")
    return records


def load_isic_split(isic_root: Path) -> IsicSplit:
    train_csv = isic_root / "ISIC2018_Task3_Training_GroundTruth" / "ISIC2018_Task3_Training_GroundTruth.csv"
    train_img = isic_root / "ISIC2018_Task3_Training_Input"
    val_csv = isic_root / "ISIC2018_Task3_Validation_GroundTruth" / "ISIC2018_Task3_Validation_GroundTruth.csv"
    val_img = isic_root / "ISIC2018_Task3_Validation_Input"

    train_records = _build_records_from_csv(train_csv, train_img)
    val_records = _build_records_from_csv(val_csv, val_img)
    return IsicSplit(train=train_records, validation=val_records)
