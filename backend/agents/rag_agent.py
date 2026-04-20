from __future__ import annotations

from collections import OrderedDict
from typing import Any

from backend.models.schemas import RAGContext, RelevantCondition, SourceReference, VisionFindings
from backend.rag.embedder import BioBERTEmbedder
from backend.rag.vectorstore import query_collection
from backend.tools.pubmed_tool import PubMedArticle, PubMedTool


class RAGAgent:
    def __init__(
        self,
        embedder: BioBERTEmbedder | None = None,
        pubmed_tool: PubMedTool | None = None,
    ) -> None:
        self.embedder = embedder or BioBERTEmbedder()
        self.pubmed_tool = pubmed_tool or PubMedTool()

    def analyze(self, patient_symptoms: str, vision_findings: VisionFindings | dict[str, Any] | None = None) -> RAGContext:
        vision = self._normalize_vision_findings(vision_findings)
        query_text = self._build_query(patient_symptoms, vision)
        chroma_hits = self._retrieve_chroma_context(query_text)
        pubmed_articles = self._retrieve_pubmed_context(query_text)
        conditions = self._infer_conditions(patient_symptoms, vision)
        evidence = self._merge_evidence(chroma_hits, pubmed_articles)
        sources = self._build_sources(chroma_hits, pubmed_articles)

        return RAGContext(
            relevant_conditions=conditions,
            supporting_evidence=evidence[:5],
            sources=sources[:5],
            retrieval_count=len(evidence[:5]),
            key_clinical_patterns=self._extract_patterns(patient_symptoms, vision),
            missing_information=self._missing_information(patient_symptoms),
        )

    def _normalize_vision_findings(self, vision_findings: VisionFindings | dict[str, Any] | None) -> VisionFindings:
        if isinstance(vision_findings, VisionFindings):
            return vision_findings
        if isinstance(vision_findings, dict):
            return VisionFindings.model_validate(vision_findings)
        return VisionFindings()

    def _build_query(self, patient_symptoms: str, vision: VisionFindings) -> str:
        parts = [patient_symptoms.strip(), " ".join(vision.findings), " ".join(vision.anomalies)]
        return " ".join(part for part in parts if part)

    def _retrieve_chroma_context(self, query_text: str) -> list[str]:
        if not query_text.strip():
            return []
        query_embedding = self.embedder.embed_texts([query_text])[0]
        try:
            result = query_collection("medqa_chunks", query_embedding, n_results=5)
            documents = result.get("documents", [[]])
            return [doc for doc in documents[0] if doc]
        except Exception:
            return []

    def _retrieve_pubmed_context(self, query_text: str) -> list[PubMedArticle]:
        try:
            return self.pubmed_tool.search(query_text, max_results=5)
        except Exception:
            return []

    def _infer_conditions(self, symptoms: str, vision: VisionFindings) -> list[RelevantCondition]:
        symptom_blob = f"{symptoms} {' '.join(vision.findings)} {' '.join(vision.anomalies)}".lower()
        profiles = [
            {
                "condition": "Pulmonary Embolism",
                "terms": {
                    "pleuritic chest pain": 3,
                    "pleuritic": 3,
                    "pleurisy": 3,
                    "d-dimer": 3,
                    "hemoptysis": 3,
                    "unilateral leg swelling": 3,
                    "sudden shortness of breath": 2,
                    "tachycardia": 2,
                    "hypoxia": 2,
                    "oxygen saturation drop": 2,
                    "chest pain": 1,
                    "shortness of breath": 1,
                },
                "minimum_score": 4,
            },
            {
                "condition": "Community-Acquired Pneumonia",
                "terms": {
                    "fever": 2,
                    "cough": 2,
                    "productive cough": 2,
                    "infiltrate": 3,
                    "consolidation": 3,
                    "opacity": 1,
                    "chest pain": 1,
                },
                "minimum_score": 4,
            },
            {
                "condition": "Pneumonia with Pleurisy",
                "terms": {
                    "pleuritic chest pain": 3,
                    "pleuritic": 2,
                    "pleurisy": 2,
                    "fever": 1,
                    "cough": 1,
                },
                "minimum_score": 3,
            },
            {
                "condition": "COVID-19 Pneumonitis",
                "terms": {
                    "fever": 1,
                    "cough": 1,
                    "bilateral": 2,
                    "ground glass": 3,
                    "opacity": 1,
                    "loss of smell": 2,
                },
                "minimum_score": 3,
            },
            {
                "condition": "Pulmonary Edema",
                "terms": {
                    "orthopnea": 3,
                    "paroxysmal nocturnal dyspnea": 3,
                    "cardiomegaly": 2,
                    "edema": 2,
                    "breathlessness": 1,
                },
                "minimum_score": 3,
            },
            {
                "condition": "Asthma Exacerbation",
                "terms": {
                    "wheeze": 3,
                    "shortness of breath": 2,
                    "tightness": 2,
                    "night cough": 2,
                },
                "minimum_score": 3,
            },
            {
                "condition": "Acute Bronchitis",
                "terms": {
                    "cough": 2,
                    "sputum": 2,
                    "fever": 1,
                    "sore throat": 1,
                },
                "minimum_score": 3,
            },
        ]

        scored: list[tuple[int, list[str], str]] = []
        for profile in profiles:
            matched = [term for term in profile["terms"] if term in symptom_blob]
            score = sum(profile["terms"][term] for term in matched)
            if score >= profile["minimum_score"]:
                scored.append((score, matched, profile["condition"]))

        scored.sort(key=lambda item: item[0], reverse=True)

        def likelihood_from_score(score: int) -> str:
            if score >= 6:
                return "high"
            if score >= 4:
                return "moderate"
            return "low"

        conditions: list[RelevantCondition] = []
        for score, matched, condition_name in scored[:5]:
            conditions.append(
                RelevantCondition(
                    condition=condition_name,
                    likelihood=likelihood_from_score(score),
                    supporting_symptoms=matched,
                    supporting_evidence_indices=list(range(min(len(matched), 3))),
                )
            )

        if not conditions:
            conditions.append(
                RelevantCondition(
                    condition="Undifferentiated clinical presentation",
                    likelihood="low",
                    supporting_symptoms=["Insufficient structured evidence; stronger retrieval needed."],
                    supporting_evidence_indices=[],
                )
            )
        return conditions[:5]

    def _merge_evidence(self, chroma_hits: list[str], pubmed_articles: list[PubMedArticle]) -> list[str]:
        merged = OrderedDict[str, None]()
        for hit in chroma_hits:
            merged[hit.strip()] = None
        for article in pubmed_articles:
            snippet = f"{article.title}: {article.abstract}".strip(": ")
            merged[snippet] = None
        return list(merged.keys())

    def _build_sources(self, chroma_hits: list[str], pubmed_articles: list[PubMedArticle]) -> list[SourceReference]:
        sources: list[SourceReference] = []
        for index, _ in enumerate(chroma_hits):
            sources.append(SourceReference(title=f"ChromaDB chunk {index + 1}", pmid=None, url=None))
        for article in pubmed_articles:
            sources.append(SourceReference(title=article.title, pmid=article.pmid, url=article.url))
        return sources

    def _extract_patterns(self, symptoms: str, vision: VisionFindings) -> list[str]:
        patterns: list[str] = []
        if "fever" in symptoms.lower():
            patterns.append("Systemic inflammatory or infectious pattern present.")
        if vision.findings:
            patterns.append("Imaging findings are available to refine differential diagnosis.")
        if not patterns:
            patterns.append("Limited structured pattern evidence available.")
        return patterns

    @staticmethod
    def _missing_information(symptoms: str) -> list[str]:
        lower = symptoms.lower()
        missing: list[str] = []
        if "duration" not in lower:
            missing.append("Duration of symptoms")
        if "spo2" not in lower and "oxygen" not in lower:
            missing.append("Oxygen saturation")
        if "age" not in lower:
            missing.append("Patient age")
        return missing
