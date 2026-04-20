from backend.agents.rag_agent import RAGAgent
from backend.models.schemas import VisionFindings


def test_rag_agent_returns_at_least_three_conditions_for_pneumonia_like_case() -> None:
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

    assert len(result.relevant_conditions) >= 3
    assert result.retrieval_count >= 0


def test_rag_agent_prioritizes_pulmonary_embolism_for_pleuritic_pattern() -> None:
    agent = RAGAgent()
    result = agent.analyze(
        "pleuritic chest pain with tachycardia and elevated d-dimer, sudden shortness of breath",
        VisionFindings(),
    )

    assert result.relevant_conditions
    assert result.relevant_conditions[0].condition == "Pulmonary Embolism"
    assert result.relevant_conditions[0].likelihood == "high"
