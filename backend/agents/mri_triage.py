from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from backend.models.schemas import VisionFindings


class MriTriageHelper:
    def analyze(self, image: Image.Image, image_path: str | Path | None = None) -> VisionFindings:
        grayscale = np.asarray(image.convert("L"), dtype=np.float32) / 255.0
        mean_intensity = float(np.mean(grayscale))
        std_intensity = float(np.std(grayscale))

        # Narrow triage only: this does not perform diagnosis.
        concern_score = 0
        if std_intensity > 0.22:
            concern_score += 1
        if mean_intensity < 0.35:
            concern_score += 1

        if concern_score >= 2:
            severity = "urgent"
            confidence = 0.45
            finding = "MRI triage detected atypical intensity pattern; specialist neuroradiology review recommended."
        else:
            severity = "moderate"
            confidence = 0.3
            finding = "MRI triage did not detect a strong high-risk pattern in this baseline screen."

        path_note = str(image_path) if image_path else "unknown"
        return VisionFindings(
            image_type="brain_mri",
            findings=[finding],
            anomalies=[],
            normal_structures=[],
            severity_hint=severity,
            confidence=confidence,
            analysis_notes=(
                "Narrow brain MRI triage only. This output is not a general MRI diagnosis and requires specialist review. "
                f"Source: {path_note}"
            ),
        )
