from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from backend.training.cxr_dataset import CXR_FINDINGS
from backend.training.cxr_model import CxrFindingsCNN
from backend.utils.data_paths import PROJECT_ROOT


DEFAULT_CXR_CHECKPOINT_CANDIDATES = [
    PROJECT_ROOT / "data" / "processed" / "models" / "rsna_gpu_full_v1" / "rsna_pneumonia_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "rsna_gpu_smoke" / "rsna_pneumonia_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "cxr_baseline" / "cxr_findings_baseline.pt",
    PROJECT_ROOT / "data" / "processed" / "models" / "cxr_gpu_smoke" / "cxr_findings_baseline.pt",
]


@dataclass(frozen=True)
class CxrPrediction:
    finding_probabilities: dict[str, float]


class CxrFindingsClassifier:
    def __init__(self, checkpoint_path: Path | None = None) -> None:
        self._checkpoint_path = checkpoint_path or self._first_existing_checkpoint()
        self._model: CxrFindingsCNN | None = None
        self._finding_names = list(CXR_FINDINGS)
        self._image_size = 224
        self._load()

    @property
    def available(self) -> bool:
        return self._model is not None

    @property
    def checkpoint_path(self) -> Path | None:
        return self._checkpoint_path

    def _first_existing_checkpoint(self) -> Path | None:
        for candidate in DEFAULT_CXR_CHECKPOINT_CANDIDATES:
            if candidate.exists():
                return candidate
        return None

    def _load(self) -> None:
        if self._checkpoint_path is None or not self._checkpoint_path.exists():
            return

        payload = torch.load(self._checkpoint_path, map_location="cpu")
        finding_names = payload.get("finding_names")
        if isinstance(finding_names, list) and finding_names:
            self._finding_names = [str(name) for name in finding_names]

        self._image_size = int(payload.get("image_size", 224))
        model = CxrFindingsCNN(num_findings=len(self._finding_names))
        model.load_state_dict(payload["state_dict"])
        model.eval()
        self._model = model

    def predict(self, image: Image.Image) -> CxrPrediction | None:
        if self._model is None:
            return None

        resized = image.convert("RGB").resize((self._image_size, self._image_size))
        tensor = torch.from_numpy(np.asarray(resized, dtype="float32")).permute(2, 0, 1) / 255.0
        tensor = tensor.unsqueeze(0)

        with torch.no_grad():
            logits = self._model(tensor)
            probabilities = torch.sigmoid(logits).squeeze(0).detach().cpu().tolist()

        mapping = {
            finding: float(probabilities[index])
            for index, finding in enumerate(self._finding_names)
        }
        return CxrPrediction(finding_probabilities=mapping)
