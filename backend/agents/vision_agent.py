from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.config import get_settings
from backend.models.schemas import VisionFindings
from backend.tools.image_loader import encode_image_to_base64, load_image, looks_like_medical_image


VISION_SYSTEM_PROMPT = (
    "You are a medical imaging analysis assistant. Return only valid JSON with keys: "
    "image_type, findings, anomalies, normal_structures, severity_hint, confidence, analysis_notes."
)

VISION_USER_PROMPT = (
    "Analyze this image. If it is non-medical, return image_type='non_medical' and empty findings."
)


class VisionAgent:
    def __init__(self, llm: ChatOllama | None = None) -> None:
        self.settings = get_settings()
        self.llm = llm

    def analyze(self, image_path: str | Path | None) -> VisionFindings:
        if not image_path:
            return self._non_medical("No image provided.")

        try:
            image = load_image(image_path)
        except Exception as exc:
            return self._non_medical(f"Unreadable image: {exc}")

        if not looks_like_medical_image(image):
            return self._non_medical("Image failed basic medical-image heuristic.")

        if self.llm is None:
            try:
                self.llm = ChatOllama(
                    model=self.settings.vision_model,
                    base_url=self.settings.ollama_base_url,
                    temperature=0.1,
                    format="json",
                )
            except Exception:
                return self._heuristic_medical_response()

        try:
            encoded_image = encode_image_to_base64(image_path)
            response = self.llm.invoke(
                [
                    SystemMessage(content=VISION_SYSTEM_PROMPT),
                    HumanMessage(
                        content=[
                            {"type": "text", "text": VISION_USER_PROMPT},
                            {"type": "image_url", "image_url": f"data:image/png;base64,{encoded_image}"},
                        ]
                    ),
                ]
            )
            return self._parse_response(response.content)
        except Exception:
            return self._heuristic_medical_response()

    def _parse_response(self, content: str | Any) -> VisionFindings:
        if not isinstance(content, str):
            content = str(content)
        data = json.loads(content)
        return VisionFindings.model_validate(data)

    @staticmethod
    def _non_medical(reason: str) -> VisionFindings:
        return VisionFindings(
            image_type="non_medical",
            findings=[],
            anomalies=[],
            normal_structures=[],
            severity_hint="normal",
            confidence=0.0,
            analysis_notes=reason,
        )

    @staticmethod
    def _heuristic_medical_response() -> VisionFindings:
        return VisionFindings(
            image_type="unknown",
            findings=["Medical-looking image detected; full LLaVA analysis pending model availability."],
            anomalies=[],
            normal_structures=[],
            severity_hint="normal",
            confidence=0.25,
            analysis_notes="Fallback response used because the vision model is not reachable yet.",
        )
