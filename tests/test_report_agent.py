from backend.agents.report_agent import ReportAgent
from backend.models.schemas import DISCLAIMER_TEXT, RAGContext, RelevantCondition, VisionFindings


def test_report_agent_returns_disclaimer_and_icd_code() -> None:
    agent = ReportAgent(llm=None)
    report = agent.generate(
      "fever, cough, chest pain",
      VisionFindings(
          image_type="chest_xray",
          findings=["bilateral infiltrates"],
          anomalies=["right lower lobe opacity"],
          normal_structures=[],
          severity_hint="moderate",
          confidence=0.82,
          analysis_notes="",
      ),
      RAGContext(
          relevant_conditions=[
              RelevantCondition(
                  condition="Community-Acquired Pneumonia",
                  likelihood="high",
                  supporting_symptoms=["fever", "cough"],
                  supporting_evidence_indices=[0, 1],
              )
          ],
          missing_information=["Oxygen saturation"],
      ),
    )

    assert report.disclaimer == DISCLAIMER_TEXT
    assert report.differential_diagnosis[0].icd_10_code == "J18.9"


def test_report_agent_escalates_red_flags() -> None:
    agent = ReportAgent(llm=None)
    report = agent.generate(
        "chest pain with oxygen saturation drop and respiratory distress",
        VisionFindings(),
        RAGContext(),
    )

    assert report.red_flags
    assert report.estimated_urgency in {"urgent", "immediate"}


def test_report_agent_maps_icd_for_pulmonary_embolism() -> None:
    agent = ReportAgent(llm=None)
    report = agent.generate(
        "pleuritic chest pain with tachycardia and elevated d-dimer",
        VisionFindings(),
        RAGContext(
            relevant_conditions=[
                RelevantCondition(
                    condition="Pulmonary Embolism",
                    likelihood="high",
                    supporting_symptoms=["pleuritic chest pain", "tachycardia", "d-dimer"],
                    supporting_evidence_indices=[0],
                )
            ]
        ),
    )

    assert report.differential_diagnosis[0].condition == "Pulmonary Embolism"
    assert report.differential_diagnosis[0].icd_10_code == "I26.99"


def test_report_agent_generates_condition_specific_next_steps() -> None:
    agent = ReportAgent(llm=None)
    report = agent.generate(
        "sudden shortness of breath with pleuritic chest pain and tachycardia; d-dimer elevated",
        VisionFindings(),
        RAGContext(
            relevant_conditions=[
                RelevantCondition(
                    condition="Pulmonary Embolism",
                    likelihood="high",
                    supporting_symptoms=["pleuritic chest pain", "tachycardia", "d-dimer"],
                    supporting_evidence_indices=[0],
                ),
                RelevantCondition(
                    condition="Pneumonia with Pleurisy",
                    likelihood="low",
                    supporting_symptoms=["pleuritic", "cough"],
                    supporting_evidence_indices=[1],
                ),
            ]
        ),
    )

    steps_blob = " ".join(report.recommended_next_steps).lower()
    assert "ct pulmonary angiography" in steps_blob
    assert "d-dimer" in steps_blob
    assert "ecg" in steps_blob
