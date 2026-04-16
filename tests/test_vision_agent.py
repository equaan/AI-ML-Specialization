from pathlib import Path

from PIL import Image

from backend.agents.vision_agent import VisionAgent


def test_vision_agent_returns_non_medical_for_missing_image() -> None:
    agent = VisionAgent(llm=None)
    result = agent.analyze(None)
    assert result.image_type == "non_medical"
    assert result.confidence == 0.0


def test_vision_agent_returns_fallback_for_valid_image(tmp_path: Path) -> None:
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (256, 256), color="white").save(image_path)

    agent = VisionAgent(llm=None)
    result = agent.analyze(str(image_path))

    assert result.image_type in {"unknown", "non_medical"}
    assert isinstance(result.findings, list)


def test_vision_agent_returns_non_medical_for_small_random_image(tmp_path: Path) -> None:
    image_path = tmp_path / "random_photo_like.png"
    Image.effect_noise((96, 96), 100).convert("RGB").save(image_path)

    agent = VisionAgent(llm=None)
    result = agent.analyze(str(image_path))

    assert result.image_type == "non_medical"
    assert "heuristic" in result.analysis_notes.lower()
