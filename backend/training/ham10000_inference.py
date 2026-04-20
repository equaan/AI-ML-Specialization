from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from backend.training.ham10000_dataset import HAM10000_CLASSES
from backend.training.ham10000_model import Ham10000BaselineCNN
from backend.utils.data_paths import PROJECT_ROOT


DEFAULT_CHECKPOINT_CANDIDATES = [
    PROJECT_ROOT / "data" / "processed" / "models" / "isic_gpu_full_v1" / "isic_finetuned_from_ham10000.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "isic_gpu_smoke" / "isic_finetuned_from_ham10000.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_full_gpu_v1" / "ham10000_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_baseline" / "ham10000_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_smoke_weighted" / "ham10000_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "ham10000_smoke" / "ham10000_baseline.pt",
]


@dataclass(frozen=True)
class SkinPrediction:
    label: str
    confidence: float


class Ham10000SkinClassifier:
    def __init__(self, checkpoint_path: Path | None = None) -> None:
        self._checkpoint_path = checkpoint_path or self._first_existing_checkpoint()
        self._model: Ham10000BaselineCNN | None = None
        self._class_names: list[str] = list(HAM10000_CLASSES)
        self._image_size = 128
        self._load()

    @property
    def available(self) -> bool:
        return self._model is not None

    @property
    def checkpoint_path(self) -> Path | None:
        return self._checkpoint_path

    def _first_existing_checkpoint(self) -> Path | None:
        for candidate in DEFAULT_CHECKPOINT_CANDIDATES:
            if candidate.exists():
                return candidate
        return None

    def _load(self) -> None:
        if self._checkpoint_path is None or not self._checkpoint_path.exists():
            return

        payload = torch.load(self._checkpoint_path, map_location="cpu")
        class_names = payload.get("class_names")
        if isinstance(class_names, list) and class_names:
            self._class_names = [str(name) for name in class_names]

        self._image_size = int(payload.get("image_size", 128))
        model = Ham10000BaselineCNN(num_classes=len(self._class_names))
        model.load_state_dict(payload["state_dict"])
        model.eval()
        self._model = model

    def predict(self, image: Image.Image) -> SkinPrediction | None:
        if self._model is None:
            return None

        resized = image.convert("RGB").resize((self._image_size, self._image_size))
        tensor = torch.from_numpy(np.asarray(resized, dtype="float32")).permute(2, 0, 1) / 255.0
        tensor = tensor.unsqueeze(0)

        with torch.no_grad():
            logits = self._model(tensor)
            probabilities = torch.softmax(logits, dim=1).squeeze(0)
            confidence, class_index = torch.max(probabilities, dim=0)

        class_name = self._class_names[int(class_index.item())]
        return SkinPrediction(label=class_name, confidence=float(confidence.item()))
