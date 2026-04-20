from __future__ import annotations

from collections import OrderedDict
from typing import Any

from backend.models.schemas import RAGContext, RelevantCondition, SourceReference, VisionFindings
from backend.rag.embedder import BioBERTEmbedder
from backend.rag.local_retriever import retrieve_local_evidence
from backend.rag.medical_knowledge import CONDITION_PROFILES, ConditionProfile
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

    def analyze(
        self,
        patient_symptoms: str,
        vision_findings: VisionFindings | dict[str, Any] | None = None,
        document_context: str = "",
    ) -> RAGContext:
        vision = self._normalize_vision_findings(vision_findings)
        query_text = self._build_query(patient_symptoms, vision, document_context)
        ranked_conditions = self._infer_conditions(patient_symptoms, vision, document_context)
        local_evidence, local_sources = self._retrieve_local_context(
            query_text,
            ranked_conditions,
            document_context,
        )
        chroma_hits = self._retrieve_chroma_context(query_text)
        pubmed_articles = self._retrieve_pubmed_context(query_text)
        evidence = self._merge_evidence(local_evidence, chroma_hits, pubmed_articles, document_context)
        sources = self._build_sources(local_sources, chroma_hits, pubmed_articles)

        return RAGContext(
            relevant_conditions=ranked_conditions,
            supporting_evidence=evidence[:6],
            sources=sources[:6],
            retrieval_count=len(evidence[:6]),
            key_clinical_patterns=self._extract_patterns(patient_symptoms, vision, document_context, ranked_conditions),
            missing_information=self._missing_information(patient_symptoms),
        )

    def _normalize_vision_findings(self, vision_findings: VisionFindings | dict[str, Any] | None) -> VisionFindings:
        if isinstance(vision_findings, VisionFindings):
            return vision_findings
        if isinstance(vision_findings, dict):
            return VisionFindings.model_validate(vision_findings)
        return VisionFindings()

    def _build_query(self, patient_symptoms: str, vision: VisionFindings, document_context: str) -> str:
        parts = [
            patient_symptoms.strip(),
            " ".join(vision.findings),
            " ".join(vision.anomalies),
            document_context.strip(),
        ]
        return " ".join(part for part in parts if part)

    def _retrieve_local_context(
        self,
        query_text: str,
        conditions: list[RelevantCondition],
        document_context: str,
    ) -> tuple[list[str], list[SourceReference]]:
        condition_terms = {condition.condition for condition in conditions[:3]}
        if document_context:
            condition_terms |= {document_context[:40]}
        return retrieve_local_evidence(query_text, condition_terms=condition_terms, limit=4)

    def _retrieve_chroma_context(self, query_text: str) -> list[str]:
        if not query_text.strip():
            return []
        try:
            query_embedding = self.embedder.embed_texts([query_text])[0]
            result = query_collection("medqa_chunks", query_embedding, n_results=4)
            documents = result.get("documents", [[]])
            return [doc for doc in documents[0] if doc]
        except Exception:
            return []

    def _retrieve_pubmed_context(self, query_text: str) -> list[PubMedArticle]:
        try:
            return self.pubmed_tool.search(query_text, max_results=3)
        except Exception:
            return []

    def _infer_conditions(
        self,
        symptoms: str,
        vision: VisionFindings,
        document_context: str,
    ) -> list[RelevantCondition]:
        combined_text = self._build_query(symptoms, vision, document_context).lower()
        scored: list[tuple[int, list[str], ConditionProfile]] = []

        for profile in CONDITION_PROFILES:
            matched_terms: list[str] = []
            score = 0

            for hallmark in profile.hallmark_terms:
                if hallmark in combined_text:
                    matched_terms.append(hallmark)
                    score += 3

            for term, weight in profile.supporting_terms.items():
                if term in combined_text:
                    if term not in matched_terms:
                        matched_terms.append(term)
                    score += weight

            if any(term in document_context.lower() for term in profile.document_terms):
                score += 4
                matched_terms.append("document-guided evidence")

            if vision.image_type == "skin_lesion" and profile.condition in {"Cellulitis", "Melanoma"}:
                score += 2
            if "non_medical" == vision.image_type and profile.condition in {"Cellulitis", "Melanoma"}:
                score -= 1

            if score > 0:
                scored.append((score, matched_terms[:6], profile))

        scored.sort(key=lambda item: item[0], reverse=True)

        conditions: list[RelevantCondition] = []
        for score, matched, profile in scored[:5]:
            conditions.append(
                RelevantCondition(
                    condition=profile.condition,
                    likelihood=self._likelihood_from_score(score),
                    supporting_symptoms=matched or [profile.summary],
                    supporting_evidence_indices=list(range(min(len(matched), 3))),
                )
            )

        if not conditions:
            conditions.append(
                RelevantCondition(
                    condition="Undifferentiated clinical presentation",
                    likelihood="low",
                    supporting_symptoms=["Insufficient structured evidence; broader evaluation is still required."],
                    supporting_evidence_indices=[],
                )
            )

        return conditions

    @staticmethod
    def _likelihood_from_score(score: int) -> str:
        if score >= 10:
            return "high"
        if score >= 6:
            return "moderate"
        return "low"

    def _merge_evidence(
        self,
        local_hits: list[str],
        chroma_hits: list[str],
        pubmed_articles: list[PubMedArticle],
        document_context: str,
    ) -> list[str]:
        merged = OrderedDict[str, None]()

        if document_context:
            merged[document_context.strip()] = None
        for hit in local_hits:
            merged[hit.strip()] = None
        for hit in chroma_hits:
            merged[hit.strip()] = None
        for article in pubmed_articles:
            snippet = f"{article.title}: {article.abstract}".strip(": ")
            merged[snippet] = None
        return [item for item in merged.keys() if item]

    def _build_sources(
        self,
        local_sources: list[SourceReference],
        chroma_hits: list[str],
        pubmed_articles: list[PubMedArticle],
    ) -> list[SourceReference]:
        sources: list[SourceReference] = list(local_sources)
        for index, _ in enumerate(chroma_hits):
            sources.append(SourceReference(title=f"ChromaDB chunk {index + 1}", pmid=None, url=None))
        for article in pubmed_articles:
            sources.append(SourceReference(title=article.title, pmid=article.pmid, url=article.url))
        return sources

    def _extract_patterns(
        self,
        symptoms: str,
        vision: VisionFindings,
        document_context: str,
        conditions: list[RelevantCondition],
    ) -> list[str]:
        patterns: list[str] = []
        lower = symptoms.lower()
        if "fever" in lower:
            patterns.append("Febrile/inflammatory pattern detected in history.")
        if any(term in lower for term in ("chest pain", "shortness of breath", "dyspnea")):
            patterns.append("Cardiorespiratory symptom cluster is present.")
        if document_context:
            patterns.append("Uploaded document context influenced retrieval ranking.")
        if vision.findings:
            patterns.append("Imaging findings are available to refine the differential.")
        if conditions:
            patterns.append(f"Top ranked consideration: {conditions[0].condition}.")
        return patterns or ["Limited structured pattern evidence available."]

    @staticmethod
    def _missing_information(symptoms: str) -> list[str]:
        lower = symptoms.lower()
        missing: list[str] = []
        if "day" not in lower and "week" not in lower and "hour" not in lower:
            missing.append("Duration of symptoms")
        if "spo2" not in lower and "oxygen" not in lower and "saturation" not in lower:
            missing.append("Oxygen saturation")
        if "age" not in lower and "child" not in lower and "adult" not in lower:
            missing.append("Patient age")
        return missing
