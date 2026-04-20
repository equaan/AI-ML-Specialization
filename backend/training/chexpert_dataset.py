from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from torch.utils.data import Dataset

from scripts.ingest_chexpert_metadata import CHEXPERT_FINDINGS, normalize_label


@dataclass(frozen=True)
class CheXpertRecord:
    image_path: Path
    finding_targets: list[float]


def load_chexpert_records(csv_path: Path, data_root: Path | None = None, limit: int | None = None) -> list[CheXpertRecord]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CheXpert CSV not found: {csv_path}")

    root = data_root or csv_path.parent
    records: list[CheXpertRecord] = []

    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rel_path = str(row.get("Path", "")).strip()
            if not rel_path:
                continue

            normalized_rel = rel_path.replace("CheXpert-v1.0-small/", "").replace("\\", "/")
            image_path = root / normalized_rel
            if not image_path.exists():
                continue

            targets = [normalize_label(row.get(finding)) for finding in CHEXPERT_FINDINGS]
            records.append(CheXpertRecord(image_path=image_path, finding_targets=targets))

            if limit is not None and len(records) >= limit:
                break

    if not records:
        raise RuntimeError("No usable CheXpert records were loaded.")
    return records


class CheXpertDataset(Dataset):
    def __init__(self, records: list[CheXpertRecord], image_size: int = 224) -> None:
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
