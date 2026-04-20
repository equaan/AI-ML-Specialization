from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.agents.mri_triage import MriTriageHelper
from backend.agents.modality_router import ModalityRouter
from backend.config import get_settings
from backend.models.schemas import VisionFindings
from backend.training.cxr_inference import CxrFindingsClassifier
from backend.training.ham10000_inference import Ham10000SkinClassifier
from backend.tools.image_loader import encode_image_to_base64, load_image, looks_like_medical_image


VISION_SYSTEM_PROMPT = (
    "You are a medical imaging analysis assistant. Return only valid JSON with keys: "
    "image_type, findings, anomalies, normal_structures, severity_hint, confidence, analysis_notes."
)

VISION_USER_PROMPT = (
    "Analyze this image. If it is non-medical, return image_type='non_medical' and empty findings."
)


class VisionAgent:
    def __init__(
        self,
        llm: ChatOllama | None = None,
        skin_classifier: Ham10000SkinClassifier | None = None,
        cxr_classifier: CxrFindingsClassifier | None = None,
        modality_router: ModalityRouter | None = None,
        mri_triage: MriTriageHelper | None = None,
    ) -> None:
        self.settings = get_settings()
        self.llm = llm
        self.skin_classifier = skin_classifier or Ham10000SkinClassifier()
        self.cxr_classifier = cxr_classifier or CxrFindingsClassifier()
        self.modality_router = modality_router or ModalityRouter()
        self.mri_triage = mri_triage or MriTriageHelper()

    def analyze(self, image_path: str | Path | None) -> VisionFindings:
        if not image_path:
            return self._non_medical("No image provided.")

        try:
            image = load_image(image_path)
        except Exception as exc:
            return self._non_medical(f"Unreadable image: {exc}")

        if not looks_like_medical_image(image):
            return self._non_medical("Image failed basic medical-image heuristic.")

        routed_modality = self.modality_router.classify(image_path=image_path)
        if routed_modality == "brain_mri":
            return self.mri_triage.analyze(image=image, image_path=image_path)

        cxr_model_result = self._analyze_with_cxr_model(image, routed_modality)
        if cxr_model_result is not None:
            return cxr_model_result

        skin_model_result = self._analyze_with_skin_model(image, routed_modality)
        if skin_model_result is not None:
            return skin_model_result

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

    def _analyze_with_cxr_model(self, image, routed_modality: str) -> VisionFindings | None:
        if routed_modality != "chest_xray":
            return None
        if not self.cxr_classifier.available:
            return None

        prediction = self.cxr_classifier.predict(image)
        if prediction is None:
            return None

        probs = prediction.finding_probabilities
        sorted_items = sorted(probs.items(), key=lambda item: item[1], reverse=True)
        positive = [name for name, score in sorted_items if score >= 0.5]
        top_name, top_score = sorted_items[0]

        if not positive and top_score < 0.35:
            checkpoint_path = self.cxr_classifier.checkpoint_path
            path_note = str(checkpoint_path) if checkpoint_path else "unknown"
            return VisionFindings(
                image_type="chest_xray",
                findings=["CXR classifier did not detect a high-confidence abnormality."],
                anomalies=[f"Top candidate (low confidence): {top_name}:{round(top_score, 3)}"],
                normal_structures=[],
                severity_hint="normal",
                confidence=round(float(top_score), 4),
                analysis_notes=(
                    "Used local CXR findings checkpoint with low-confidence result; "
                    "kept chest-specific output to avoid generic fallback. "
                    f"Checkpoint: {path_note}"
                ),
            )

        findings = [f"CXR classifier suggests: {', '.join(positive)}"] if positive else [
            f"CXR classifier top finding: {top_name}"
        ]
        severity = "urgent" if any(name in {"pneumothorax", "effusion"} for name in positive) else "moderate"
        checkpoint_path = self.cxr_classifier.checkpoint_path
        path_note = str(checkpoint_path) if checkpoint_path else "unknown"

        return VisionFindings(
            image_type="chest_xray",
            findings=findings,
            anomalies=[f"{name}:{round(score, 3)}" for name, score in sorted_items[:4]],
            normal_structures=[],
            severity_hint=severity,
            confidence=round(float(top_score), 4),
            analysis_notes=(
                "Used local CXR findings checkpoint before generic fallback. "
                f"Checkpoint: {path_note}"
            ),
        )

    def _analyze_with_skin_model(self, image, routed_modality: str) -> VisionFindings | None:
        if routed_modality != "skin_lesion":
            return None

        if not self.skin_classifier.available:
            return None

        prediction = self.skin_classifier.predict(image)
        if prediction is None:
            return None

        if prediction.confidence < 0.35:
            return None

        high_risk_labels = {"mel", "akiec", "bcc"}
        severity = "critical" if prediction.label in high_risk_labels else "moderate"
        confidence = round(prediction.confidence, 4)
        checkpoint_path = self.skin_classifier.checkpoint_path
        path_note = str(checkpoint_path) if checkpoint_path else "unknown"

        return VisionFindings(
            image_type="skin_lesion",
            findings=[f"HAM10000 classifier suggests lesion class: {prediction.label}."],
            anomalies=[f"Predicted skin lesion label: {prediction.label}"],
            normal_structures=[],
            severity_hint=severity,
            confidence=confidence,
            analysis_notes=(
                f"Used local HAM10000 checkpoint for inference at confidence {confidence}. "
                f"Checkpoint: {path_note}"
            ),
        )

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
