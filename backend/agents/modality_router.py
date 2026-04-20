from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from backend.tools.image_loader import load_image


SUPPORTED_MODALITIES = {
    "chest_xray",
    "skin_lesion",
    "brain_mri",
    "report_pdf",
    "generic_document",
}


class ModalityRouter:
    def classify(
        self,
        image_path: str | Path | None = None,
        pdf_path: str | Path | None = None,
    ) -> str:
        if pdf_path:
            return "report_pdf"
        if not image_path:
            return "generic_document"

        path = Path(image_path)
        name = path.as_posix().lower()

        if any(token in name for token in ("chexpert", "cxr", "xray", "x-ray", "chest")):
            return "chest_xray"
        if any(token in name for token in ("ham10000", "isic", "skin", "lesion", "derm")):
            return "skin_lesion"
        if any(token in name for token in ("mri", "brain", "glioma")):
            return "brain_mri"

        try:
            image = load_image(path)
            return self.classify_image(image)
        except Exception:
            return "generic_document"

    def classify_image(self, image: Image.Image) -> str:
        rgb = np.asarray(image.convert("RGB"), dtype=np.float32) / 255.0
        r = rgb[:, :, 0]
        g = rgb[:, :, 1]
        b = rgb[:, :, 2]

        channel_delta = np.mean(np.abs(r - g) + np.abs(g - b) + np.abs(r - b))
        brightness = float(np.mean(rgb))
        dark_fraction = float(np.mean(np.mean(rgb, axis=2) < 0.2))
        warm_fraction = float(np.mean((r > g) & (g > b) & (r > 0.35)))

        width, height = image.size
        aspect_ratio = width / max(height, 1)

        grayscale_like = channel_delta < 0.08
        if grayscale_like and dark_fraction > 0.45 and 0.7 <= aspect_ratio <= 1.35:
            return "brain_mri"

        if grayscale_like and brightness < 0.65:
            return "chest_xray"

        if warm_fraction > 0.28 and channel_delta > 0.1:
            return "skin_lesion"

        return "generic_document"
