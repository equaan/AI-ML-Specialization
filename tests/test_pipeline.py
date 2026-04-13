from pathlib import Path

from PIL import Image

from backend.agents.orchestrator import MediAgentOrchestrator


def test_pipeline_returns_clinical_report(tmp_path: Path) -> None:
    image_path = tmp_path / "xray.png"
    Image.new("RGB", (256, 256), color="white").save(image_path)

    orchestrator = MediAgentOrchestrator()
    result = orchestrator.run(
        {
            "patient_symptoms": "chest pain and fever",
            "image_path": str(image_path),
            "messages": [],
        }
    )

    final_report = result["final_report"]
    assert final_report["disclaimer"]
    assert len(final_report["differential_diagnosis"]) >= 1
