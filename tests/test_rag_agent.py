from backend.agents.rag_agent import RAGAgent
from backend.models.schemas import VisionFindings


def test_rag_agent_returns_at_least_one_condition() -> None:
    agent = RAGAgent()
    result = agent.analyze(
        "fever, cough, bilateral chest pain",
        VisionFindings(
            image_type="chest_xray",
            findings=["bilateral infiltrates"],
            anomalies=["right lower lobe opacity"],
            normal_structures=[],
            severity_hint="moderate",
            confidence=0.8,
            analysis_notes="",
        ),
    )

    assert len(result.relevant_conditions) >= 1
    assert result.retrieval_count >= 0
