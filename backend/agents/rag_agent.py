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
        rules = [
            {
                "condition": "Pulmonary Embolism",
                "likelihood": "high",
                "keywords": [
                    "pleuritic chest pain",
                    "pleuritic",
                    "pleurisy",
                    "sudden shortness of breath",
                    "tachycardia",
                    "hemoptysis",
                    "d-dimer",
                    "hypoxia",
                    "unilateral leg swelling",
                    "pulmonary embolism",
                ],
                "min_matches": 2,
            },
            {
                "condition": "Community-Acquired Pneumonia",
                "likelihood": "high",
                "keywords": ["fever", "cough", "infiltrate", "consolidation", "chest pain"],
                "min_matches": 2,
            },
            {
                "condition": "COVID-19 Pneumonitis",
                "likelihood": "moderate",
                "keywords": ["fever", "cough", "bilateral", "opacity"],
                "min_matches": 2,
            },
            {
                "condition": "Pulmonary Edema",
                "likelihood": "moderate",
                "keywords": ["edema", "cardiomegaly", "breathlessness", "orthopnea"],
                "min_matches": 2,
            },
            {
                "condition": "Asthma Exacerbation",
                "likelihood": "moderate",
                "keywords": ["wheeze", "shortness of breath", "tightness"],
                "min_matches": 2,
            },
            {
                "condition": "Pneumonia with Pleurisy",
                "likelihood": "low",
                "keywords": ["pleuritic", "pleurisy", "pleuritic chest pain", "fever", "cough"],
                "min_matches": 2,
            },
            {
                "condition": "Acute Bronchitis",
                "likelihood": "low",
                "keywords": ["cough", "sputum", "fever"],
                "min_matches": 2,
            },
        ]

        likelihood_priority = {"high": 0, "moderate": 1, "low": 2}

        conditions: list[RelevantCondition] = []
        for rule in rules:
            matched = [keyword for keyword in rule["keywords"] if keyword in symptom_blob]
            if len(matched) >= rule["min_matches"]:
                conditions.append(
                    RelevantCondition(
                        condition=rule["condition"],
                        likelihood=rule["likelihood"],
                        supporting_symptoms=matched,
                        supporting_evidence_indices=list(range(min(len(matched), 3))),
                    )
                )

        conditions.sort(
            key=lambda item: (
                likelihood_priority.get(item.likelihood, 9),
                -len(item.supporting_symptoms),
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
