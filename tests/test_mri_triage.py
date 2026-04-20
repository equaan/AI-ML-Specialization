from pathlib import Path

from PIL import Image

from backend.agents.mri_triage import MriTriageHelper


def test_mri_triage_returns_guardrailed_brain_mri_response(tmp_path: Path) -> None:
    image_path = tmp_path / "brain_mri.png"
    Image.new("RGB", (256, 256), color=(40, 40, 40)).save(image_path)

    helper = MriTriageHelper()
    result = helper.analyze(Image.open(image_path), image_path=image_path)

    assert result.image_type == "brain_mri"
    assert "not a general mri diagnosis" in result.analysis_notes.lower()
    assert result.severity_hint in {"moderate", "urgent"}
