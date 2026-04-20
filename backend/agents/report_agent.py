from __future__ import annotations

import json
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from backend.config import get_settings
from backend.models.schemas import (
    DISCLAIMER_TEXT,
    ClinicalReport,
    DifferentialDiagnosis,
    RAGContext,
    RelevantCondition,
    VisionFindings,
)


ICD10_MAP = {
    "Sepsis": "A41.9",
    "Pulmonary Embolism": "I26.99",
    "Community-Acquired Pneumonia": "J18.9",
    "Pneumonia with Pleurisy": "J18.9",
    "COVID-19 Pneumonitis": "U07.1",
    "COVID-19": "U07.1",
    "Pulmonary Edema": "J81.1",
    "Acute Heart Failure": "I50.9",
    "Asthma Exacerbation": "J45.901",
    "Acute Bronchitis": "J20.9",
    "Acute Coronary Syndrome": "I24.9",
    "Stable Angina": "I20.9",
    "Viral Upper Respiratory Infection": "J06.9",
    "Influenza-like Illness": "J11.1",
    "Bacterial Pharyngitis": "J02.8",
    "Cellulitis": "L03.90",
    "Melanoma": "C43.9",
    "Undifferentiated clinical presentation": "R69",
}


LIKELIHOOD_TO_SCORE = {
    "high": 0.85,
    "moderate": 0.6,
    "low": 0.35,
}


class ReportAgent:
    def __init__(self, llm: ChatOllama | None = None) -> None:
        self.settings = get_settings()
        self.llm = llm

    def generate(
        self,
        patient_symptoms: str,
        vision_findings: VisionFindings | dict[str, Any] | None,
        rag_context: RAGContext | dict[str, Any] | None,
    ) -> ClinicalReport:
        vision = self._normalize_vision(vision_findings)
        rag = self._normalize_rag(rag_context)
        llm_report = self._generate_with_llm(patient_symptoms, vision, rag)
        if llm_report is not None:
            reconciled = self._apply_rag_consistency_overrides(llm_report, rag, vision)
            reconciled.recommended_next_steps = self._recommended_next_steps(
                reconciled.differential_diagnosis,
                reconciled.red_flags,
                patient_symptoms,
            )
            reconciled.estimated_urgency = self._apply_urgency_guardrails(
                reconciled.estimated_urgency,
                patient_symptoms,
                reconciled.red_flags,
                reconciled.differential_diagnosis,
            )
            return reconciled
        fallback = self._generate_fallback_report(patient_symptoms, vision, rag)
        fallback.estimated_urgency = self._apply_urgency_guardrails(
            fallback.estimated_urgency,
            patient_symptoms,
            fallback.red_flags,
            fallback.differential_diagnosis,
        )
        return fallback

    def _apply_rag_consistency_overrides(
        self,
        report: ClinicalReport,
        rag: RAGContext,
        vision: VisionFindings,
    ) -> ClinicalReport:
        existing_by_name = {item.condition.lower(): item for item in report.differential_diagnosis}
        additions: list[DifferentialDiagnosis] = []

        for condition in rag.relevant_conditions:
            if condition.likelihood != "high":
                continue
            key = condition.condition.lower()
            if key in existing_by_name:
                existing = existing_by_name[key]
                if existing.icd_10_code == "R69":
                    existing.icd_10_code = ICD10_MAP.get(condition.condition, existing.icd_10_code)
                continue

            additions.append(
                DifferentialDiagnosis(
                    rank=0,
                    condition=condition.condition,
                    icd_10_code=ICD10_MAP.get(condition.condition, "R69"),
                    confidence_score=LIKELIHOOD_TO_SCORE.get(condition.likelihood, 0.3),
                    supporting_findings=condition.supporting_symptoms + vision.findings[:2],
                    against_findings=self._build_against_findings(condition),
                    clinical_rationale=(
                        "Added from high-likelihood RAG evidence to preserve clinically "
                        "salient differential coverage."
                    ),
                )
            )

        merged = additions + report.differential_diagnosis
        for index, diagnosis in enumerate(merged, start=1):
            diagnosis.rank = index
            diagnosis.icd_10_code = ICD10_MAP.get(diagnosis.condition, diagnosis.icd_10_code)

        report.differential_diagnosis = merged[:5]
        return report

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

    def _generate_with_llm(
        self,
        patient_symptoms: str,
        vision: VisionFindings,
        rag: RAGContext,
    ) -> ClinicalReport | None:
        if self.llm is None:
            try:
                self.llm = ChatOllama(
                    model=self.settings.ollama_model,
                    base_url=self.settings.ollama_base_url,
                    temperature=0.1,
                    format="json",
                )
            except Exception:
                return None

        prompt = (
            "Generate a structured clinical report as valid JSON with keys "
            "patient_summary, differential_diagnosis, red_flags, recommended_next_steps, "
            "estimated_urgency, additional_history_needed, disclaimer.\n\n"
            f"Symptoms: {patient_symptoms}\n"
            f"Vision findings: {vision.model_dump_json()}\n"
            f"RAG context: {rag.model_dump_json()}\n"
            f'Disclaimer must be exactly: "{DISCLAIMER_TEXT}"'
        )

        try:
            response = self.llm.invoke(
                [
                    SystemMessage(content="You are a clinical decision support report generator. Return only JSON."),
                    HumanMessage(content=prompt),
                ]
            )
            data = json.loads(response.content)
            return ClinicalReport.model_validate(data)
        except Exception:
            return None

    def _generate_fallback_report(
        self,
        patient_symptoms: str,
        vision: VisionFindings,
        rag: RAGContext,
    ) -> ClinicalReport:
        diagnoses = self._build_differential_diagnosis(rag, vision)
        red_flags = self._derive_red_flags(patient_symptoms, vision)
        urgency = self._estimate_urgency(red_flags)

        return ClinicalReport(
            patient_summary=self._patient_summary(patient_symptoms, vision, rag),
            differential_diagnosis=diagnoses,
            red_flags=red_flags,
            recommended_next_steps=self._recommended_next_steps(diagnoses, red_flags, patient_symptoms),
            estimated_urgency=urgency,
            additional_history_needed=rag.missing_information,
            disclaimer=DISCLAIMER_TEXT,
        )

    def _build_differential_diagnosis(self, rag: RAGContext, vision: VisionFindings) -> list[DifferentialDiagnosis]:
        diagnoses: list[DifferentialDiagnosis] = []
        for rank, condition in enumerate(rag.relevant_conditions, start=1):
            against_findings = self._build_against_findings(condition)
            diagnoses.append(
                DifferentialDiagnosis(
                    rank=rank,
                    condition=condition.condition,
                    icd_10_code=ICD10_MAP.get(condition.condition, "R69"),
                    confidence_score=LIKELIHOOD_TO_SCORE.get(condition.likelihood, 0.3),
                    supporting_findings=condition.supporting_symptoms + vision.findings[:2],
                    against_findings=against_findings,
                    clinical_rationale=(
                        f"Condition ranked from symptom-pattern matching and retrieval evidence. "
                        f"Vision severity hint: {vision.severity_hint}."
                    ),
                )
            )
        return diagnoses

    @staticmethod
    def _build_against_findings(condition: RelevantCondition) -> list[str]:
        if condition.likelihood == "high":
            return ["No strong contradictory evidence identified in the currently provided inputs."]
        if condition.likelihood == "moderate":
            return ["Pattern fit is partial; confirm with focused exam, vitals, and targeted testing."]
        return ["Limited high-specificity supporting evidence; treat as lower-priority until further data arrives."]

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
        if any(
            term in combined
            for term in ("chest pain", "neurological deficit", "sepsis", "altered mental status", "less responsive")
        ):
            red_flags.append("High-risk symptom detected in input; escalate for clinician assessment.")
        if "critical" in vision.severity_hint.lower():
            red_flags.append("Vision analysis flagged critical severity.")
        return red_flags or [
            "No immediate high-risk red flags identified from current inputs; continue monitoring and fill missing data."
        ]

    @staticmethod
    def _estimate_urgency(red_flags: list[str]) -> str:
        actionable_flags = [
            flag
            for flag in red_flags
            if not flag.startswith("No immediate high-risk red flags identified")
        ]
        if len(actionable_flags) >= 2:
            return "immediate"
        if len(actionable_flags) == 1:
            return "urgent"
        if len(red_flags) >= 2:
            return "immediate"
        if len(red_flags) == 1:
            return "semi_urgent"
        return "semi_urgent"

    @staticmethod
    def _recommended_next_steps(
        diagnoses: list[DifferentialDiagnosis],
        red_flags: list[str],
        patient_symptoms: str,
    ) -> list[str]:
        symptom_blob = patient_symptoms.lower()
        steps: list[str] = ["Repeat focused clinical examination and full vital signs review."]

        top_conditions = [item.condition for item in diagnoses[:3]]
        condition_steps = {
            "Sepsis": [
                "Initiate urgent sepsis screening with full vitals, lactate, CBC, and blood cultures.",
                "Escalate immediately for clinician review and organ-dysfunction assessment.",
            ],
            "Pulmonary Embolism": [
                "Order D-dimer and urgent CT pulmonary angiography if PE probability is intermediate/high.",
                "Assess hemodynamic stability and initiate emergency referral pathway.",
                "Perform lower-limb venous Doppler if DVT is suspected.",
            ],
            "Community-Acquired Pneumonia": [
                "Order CBC, CRP, and chest imaging correlation for pneumonia severity assessment.",
                "Obtain sputum and blood cultures before antibiotics when clinically feasible.",
            ],
            "Pneumonia with Pleurisy": [
                "Check pleuritic pain severity and evaluate for pleural effusion with chest imaging.",
                "Consider inflammatory markers and focused respiratory examination follow-up.",
            ],
            "Acute Bronchitis": [
                "Provide symptomatic respiratory care plan and monitor for worsening dyspnea/fever.",
                "Reassess if symptoms persist beyond expected course or red flags develop.",
            ],
            "Viral Upper Respiratory Infection": [
                "Use supportive care, hydration, and follow-up if symptoms worsen or breathing becomes difficult.",
            ],
            "Influenza-like Illness": [
                "Consider influenza or respiratory viral testing based on severity and local protocol.",
            ],
            "Asthma Exacerbation": [
                "Check peak expiratory flow and bronchodilator response.",
                "Escalate to urgent care if persistent wheeze or oxygen desaturation is present.",
            ],
            "Pulmonary Edema": [
                "Evaluate for cardiac cause with ECG, BNP, and bedside imaging as available.",
                "Monitor oxygenation continuously and assess need for urgent cardiology review.",
            ],
            "Acute Heart Failure": [
                "Evaluate for cardiac decompensation with ECG, BNP, and chest imaging as available.",
                "Monitor oxygenation and fluid status closely.",
            ],
            "Acute Coronary Syndrome": [
                "Obtain ECG and serial troponin testing urgently.",
                "Escalate for emergency clinician assessment of possible acute coronary syndrome.",
            ],
            "Stable Angina": [
                "Risk-stratify chest pain and arrange prompt cardiac evaluation with ECG.",
            ],
            "Bacterial Pharyngitis": [
                "Perform focused throat examination and consider testing if bacterial features predominate.",
            ],
            "Cellulitis": [
                "Examine the involved skin area and assess for systemic spread or rapidly progressive infection.",
            ],
            "Melanoma": [
                "Arrange focused dermatology review if the lesion has malignant features or recent change.",
            ],
        }

        for condition in top_conditions:
            steps.extend(condition_steps.get(condition, []))

        if any(term in symptom_blob for term in ("chest pain", "tachycardia", "d-dimer")):
            steps.append("Perform ECG and serial troponin testing to exclude concurrent acute coronary syndrome.")
        if any(term in symptom_blob for term in ("hypoxia", "spo2", "oxygen", "respiratory distress")):
            steps.append("Start continuous pulse oximetry and titrate oxygen support per clinical protocol.")
        if any(term in symptom_blob for term in ("less responsive", "altered mental status", "confusion")):
            steps.append("Escalate immediately because mental-status change can indicate severe illness.")

        if red_flags:
            steps.append("Escalate urgently because red-flag criteria were triggered.")

        if not top_conditions:
            steps.append("Correlate with CBC, CRP, and baseline labs to refine differential diagnosis.")

        deduped_steps: list[str] = []
        seen: set[str] = set()
        for step in steps:
            if step not in seen:
                seen.add(step)
                deduped_steps.append(step)

        return deduped_steps[:8]

    @staticmethod
    def _apply_urgency_guardrails(
        current_urgency: str,
        patient_symptoms: str,
        red_flags: list[str],
        diagnoses: list[DifferentialDiagnosis],
    ) -> str:
        order = {
            "routine": 0,
            "non_urgent": 0,
            "semi_urgent": 1,
            "urgent": 2,
            "immediate": 3,
        }
        reverse = {v: k for k, v in order.items()}

        symptom_blob = patient_symptoms.lower()
        red_flag_blob = " ".join(red_flags).lower()
        top_conditions = [item.condition.lower() for item in diagnoses[:3]]

        level = order.get((current_urgency or "semi_urgent").lower(), 1)

        dka_markers = [
            "type 1 diabetes",
            "ketones",
            "anion gap",
            "bicarbonate",
            "fruity breath",
            "confusion",
            "altered mental",
            "ph 7.",
            "deep labored breathing",
        ]
        if sum(1 for marker in dka_markers if marker in symptom_blob) >= 3:
            level = max(level, order["immediate"])

        skin_evolution_markers = [
            "pigmented lesion",
            "asymmetry",
            "irregular",
            "variegated",
            "diameter over 6",
            "rapid evolution",
            "grew from",
        ]
        if ("melanoma" in " ".join(top_conditions)) and sum(
            1 for marker in skin_evolution_markers if marker in symptom_blob
        ) >= 2:
            level = max(level, order["urgent"])

        low_acuity_markers = [
            "annual preventive check",
            "hba1c",
            "ldl",
            "triglycerides",
        ]
        severe_exclusions = [
            "shortness of breath",
            "spo2",
            "hemoptysis",
            "confusion",
            "altered mental",
            "d-dimer",
            "troponin",
            "sepsis",
            "ketones",
            "anion gap",
        ]
        explicit_low_risk_context = (
            "annual preventive check" in symptom_blob
            and "no chest pain" in symptom_blob
            and ("no dyspnea" in symptom_blob or "or dyspnea" in symptom_blob)
        )
        if explicit_low_risk_context and not any(marker in symptom_blob for marker in severe_exclusions):
            level = min(level, order["semi_urgent"])
        elif (
            sum(1 for marker in low_acuity_markers if marker in symptom_blob) >= 3
            and not any(marker in symptom_blob for marker in severe_exclusions)
            and not any(term in red_flag_blob for term in ["high-risk", "immediate", "critical"])
        ):
            level = min(level, order["semi_urgent"])

        return reverse[level]
