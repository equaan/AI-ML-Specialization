from __future__ import annotations

from typing import Any, Optional, TypedDict

from langchain_core.messages import BaseMessage
from langgraph.graph import END, START, StateGraph

from backend.agents.rag_agent import RAGAgent
from backend.agents.report_agent import ReportAgent
from backend.agents.vision_agent import VisionAgent


class MediAgentState(TypedDict, total=False):
    patient_symptoms: str
    image_path: Optional[str]
    pdf_path: Optional[str]
    document_context: Optional[str]
    voice_transcript: Optional[str]
    vision_findings: Optional[dict[str, Any]]
    rag_context: Optional[dict[str, Any]]
    final_report: Optional[dict[str, Any]]
    messages: list[BaseMessage]
    current_agent: str
    error: Optional[str]


class MediAgentOrchestrator:
    def __init__(
        self,
        vision_agent: VisionAgent | None = None,
        rag_agent: RAGAgent | None = None,
        report_agent: ReportAgent | None = None,
    ) -> None:
        self.vision_agent = vision_agent or VisionAgent()
        self.rag_agent = rag_agent or RAGAgent()
        self.report_agent = report_agent or ReportAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(MediAgentState)
        graph.add_node("vision_node", self._vision_node)
        graph.add_node("rag_node", self._rag_node)
        graph.add_node("report_node", self._report_node)
        graph.add_conditional_edges(
            START,
            self._route_from_start,
            {"vision_node": "vision_node", "rag_node": "rag_node"},
        )
        graph.add_edge("vision_node", "rag_node")
        graph.add_edge("rag_node", "report_node")
        graph.add_edge("report_node", END)
        return graph.compile()

    def run(self, initial_state: MediAgentState) -> MediAgentState:
        return self.graph.invoke(initial_state)

    @staticmethod
    def _route_from_start(state: MediAgentState) -> str:
        return "vision_node" if state.get("image_path") else "rag_node"

    def _vision_node(self, state: MediAgentState) -> MediAgentState:
        findings = self.vision_agent.analyze(state.get("image_path"))
        return {
            **state,
            "current_agent": "vision_agent",
            "vision_findings": findings.model_dump(),
        }

    def _rag_node(self, state: MediAgentState) -> MediAgentState:
        symptoms = state.get("voice_transcript") or state.get("patient_symptoms", "")
        rag_context = self.rag_agent.analyze(
            symptoms,
            state.get("vision_findings"),
            document_context=state.get("document_context") or "",
        )
        return {
            **state,
            "current_agent": "rag_agent",
            "rag_context": rag_context.model_dump(),
        }

    def _report_node(self, state: MediAgentState) -> MediAgentState:
        symptoms = state.get("voice_transcript") or state.get("patient_symptoms", "")
        report = self.report_agent.generate(symptoms, state.get("vision_findings"), state.get("rag_context"))
        return {
            **state,
            "current_agent": "report_agent",
            "final_report": report.model_dump(),
        }
