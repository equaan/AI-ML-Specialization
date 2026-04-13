from __future__ import annotations

from typing import Any

from backend.models.schemas import (
    DISCLAIMER_TEXT,
    ClinicalReport,
    DifferentialDiagnosis,
    RAGContext,
    VisionFindings,
)


ICD10_MAP = {
    "Community-Acquired Pneumonia": "J18.9",
    "COVID-19 Pneumonitis": "U07.1",
    "Pulmonary Edema": "J81.1",
    "Asthma Exacerbation": "J45.901",
    "Acute Bronchitis": "J20.9",
    "Undifferentiated clinical presentation": "R69",
}


LIKELIHOOD_TO_SCORE = {
    "high": 0.85,
    "moderate": 0.6,
    "low": 0.35,
}


class ReportAgent:
    def generate(
        self,
        patient_symptoms: str,
        vision_findings: VisionFindings | dict[str, Any] | None,
        rag_context: RAGContext | dict[str, Any] | None,
    ) -> ClinicalReport:
        vision = self._normalize_vision(vision_findings)
        rag = self._normalize_rag(rag_context)
        diagnoses = self._build_differential_diagnosis(rag, vision)
        red_flags = self._derive_red_flags(patient_symptoms, vision)
        urgency = self._estimate_urgency(red_flags)

        return ClinicalReport(
            patient_summary=self._patient_summary(patient_symptoms, vision, rag),
            differential_diagnosis=diagnoses,
            red_flags=red_flags,
            recommended_next_steps=self._recommended_next_steps(diagnoses, red_flags),
            estimated_urgency=urgency,
            additional_history_needed=rag.missing_information,
            disclaimer=DISCLAIMER_TEXT,
        )

    @staticmethod
    def _normalize_vision(vision_findings: VisionFindings | dict[str, Any] | None) -> VisionFindings:
        if isinstance(vision_findings, VisionFindings):
            return vision_findings
        if isinstance(vision_findings, dict):
            return VisionFindings.model_validate(vision_findings)
        return VisionFindings()

    @staticmethod
    def _normalize_rag(rag_context: RAGContext | dict[str, Any] | None) -> RAGContext:
        if isinstance(rag_context, RAGContext):
            return rag_context
        if isinstance(rag_context, dict):
            return RAGContext.model_validate(rag_context)
        return RAGContext()

    def _build_differential_diagnosis(self, rag: RAGContext, vision: VisionFindings) -> list[DifferentialDiagnosis]:
        diagnoses: list[DifferentialDiagnosis] = []
        for rank, condition in enumerate(rag.relevant_conditions, start=1):
            diagnoses.append(
                DifferentialDiagnosis(
                    rank=rank,
                    condition=condition.condition,
                    icd_10_code=ICD10_MAP.get(condition.condition, "R69"),
                    confidence_score=LIKELIHOOD_TO_SCORE.get(condition.likelihood, 0.3),
                    supporting_findings=condition.supporting_symptoms + vision.findings[:2],
                    against_findings=[],
                    clinical_rationale=(
                        f"Condition ranked from symptom-pattern matching and retrieval evidence. "
                        f"Vision severity hint: {vision.severity_hint}."
                    ),
                )
            )
        return diagnoses

    def _patient_summary(self, symptoms: str, vision: VisionFindings, rag: RAGContext) -> str:
        image_summary = ", ".join(vision.findings[:2]) if vision.findings else "no confirmed imaging findings yet"
        condition_summary = rag.relevant_conditions[0].condition if rag.relevant_conditions else "undifferentiated symptoms"
        return (
            f"Patient symptoms: {symptoms or 'not provided'}. "
            f"Imaging summary: {image_summary}. "
            f"Top evidence-backed consideration: {condition_summary}."
        )

    @staticmethod
    def _derive_red_flags(symptoms: str, vision: VisionFindings) -> list[str]:
        combined = f"{symptoms} {' '.join(vision.findings)} {' '.join(vision.anomalies)}".lower()
        red_flags: list[str] = []
        if any(term in combined for term in ("spo2", "oxygen saturation", "respiratory distress", "cyanosis")):
            red_flags.append("Possible respiratory compromise mentioned; urgent review recommended.")
        if any(term in combined for term in ("chest pain", "neurological deficit", "sepsis", "altered mental status")):
            red_flags.append("High-risk symptom detected in input; escalate for clinician assessment.")
        if "critical" in vision.severity_hint.lower():
            red_flags.append("Vision analysis flagged critical severity.")
        return red_flags

    @staticmethod
    def _estimate_urgency(red_flags: list[str]) -> str:
        if len(red_flags) >= 2:
            return "immediate"
        if len(red_flags) == 1:
            return "urgent"
        return "semi_urgent"

    @staticmethod
    def _recommended_next_steps(diagnoses: list[DifferentialDiagnosis], red_flags: list[str]) -> list[str]:
        steps = [
            "Repeat focused clinical examination and vital signs review.",
            "Correlate with CBC, CRP, and other indicated baseline labs.",
            "Review imaging with a qualified clinician or radiologist.",
        ]
        if diagnoses:
            steps.append(f"Prioritize workup for {diagnoses[0].condition}.")
        if red_flags:
            steps.append("Escalate urgently because red-flag criteria were triggered.")
        return steps
