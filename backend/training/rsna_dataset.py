from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pydicom
import torch
from PIL import Image
from torch.utils.data import Dataset


@dataclass(frozen=True)
class RsnaRecord:
    patient_id: str
    image_path: Path
    target: int


def load_rsna_records(rsna_dir: Path) -> list[RsnaRecord]:
    labels_csv = rsna_dir / "stage_2_train_labels.csv"
    images_dir = rsna_dir / "stage_2_train_images"
    if not labels_csv.exists():
        raise FileNotFoundError(f"RSNA labels CSV not found: {labels_csv}")
    if not images_dir.exists():
        raise FileNotFoundError(f"RSNA train images dir not found: {images_dir}")

    target_by_patient: dict[str, int] = {}
    with labels_csv.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            patient_id = str(row.get("patientId", "")).strip()
            if not patient_id:
                continue
            target = int(float(row.get("Target", "0") or 0))
            current = target_by_patient.get(patient_id, 0)
            target_by_patient[patient_id] = max(current, target)

    records: list[RsnaRecord] = []
    for patient_id, target in target_by_patient.items():
        image_path = images_dir / f"{patient_id}.dcm"
        if image_path.exists():
            records.append(RsnaRecord(patient_id=patient_id, image_path=image_path, target=target))

    if not records:
        raise RuntimeError("No RSNA records were loaded.")
    return records


class RsnaDataset(Dataset):
    def __init__(self, records: list[RsnaRecord], image_size: int = 224) -> None:
        self.records = records
        self.image_size = image_size

    def __len__(self) -> int:
        return len(self.records)

    @staticmethod
    def _load_dicom_image(path: Path) -> Image.Image:
        dcm = pydicom.dcmread(str(path))
        arr = dcm.pixel_array.astype("float32")
        arr = arr - arr.min()
        max_val = float(arr.max())
        if max_val > 0:
            arr = arr / max_val
        arr = (arr * 255.0).clip(0, 255).astype("uint8")
        return Image.fromarray(arr, mode="L").convert("RGB")

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        record = self.records[index]
        image = self._load_dicom_image(record.image_path)
        image = image.resize((self.image_size, self.image_size))
        tensor = torch.from_numpy(np.asarray(image, dtype="float32")).permute(2, 0, 1) / 255.0
        target = torch.tensor([float(record.target)], dtype=torch.float32)
        return tensor, target
