from pathlib import Path

from PIL import Image

from backend.agents.modality_router import ModalityRouter
from backend.agents.vision_agent import VisionAgent
from backend.training.cxr_inference import CxrPrediction
from backend.training.ham10000_inference import SkinPrediction


class DummySkinClassifier:
    def __init__(self, prediction: SkinPrediction | None = None, available: bool = True) -> None:
        self._prediction = prediction
        self.available = available
        self.checkpoint_path = Path("dummy.pt")

    def predict(self, image):
        return self._prediction


class DummyCxrClassifier:
    def __init__(self, prediction: CxrPrediction | None = None, available: bool = True) -> None:
        self._prediction = prediction
        self.available = available
        self.checkpoint_path = Path("dummy_cxr.pt")

    def predict(self, image):
        return self._prediction


class DummyRouter(ModalityRouter):
    def __init__(self, modality: str) -> None:
        self.modality = modality

    def classify(self, image_path=None, pdf_path=None) -> str:
        return self.modality


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

    assert result.image_type in {"unknown", "non_medical", "skin_lesion"}
    assert isinstance(result.findings, list)


def test_vision_agent_returns_non_medical_for_small_random_image(tmp_path: Path) -> None:
    image_path = tmp_path / "random_photo_like.png"
    Image.effect_noise((96, 96), 100).convert("RGB").save(image_path)

    agent = VisionAgent(llm=None)
    result = agent.analyze(str(image_path))

    assert result.image_type == "non_medical"
    assert "heuristic" in result.analysis_notes.lower()


def test_vision_agent_uses_skin_classifier_when_available(tmp_path: Path) -> None:
    image_path = tmp_path / "skin.png"
    Image.new("RGB", (256, 256), color="white").save(image_path)

    classifier = DummySkinClassifier(prediction=SkinPrediction(label="mel", confidence=0.9), available=True)
    agent = VisionAgent(llm=None, skin_classifier=classifier, modality_router=DummyRouter("skin_lesion"))

    result = agent.analyze(str(image_path))

    assert result.image_type == "skin_lesion"
    assert "mel" in " ".join(result.findings).lower()
    assert result.confidence >= 0.9


def test_vision_agent_skips_skin_classifier_for_non_skin_route(tmp_path: Path) -> None:
    image_path = tmp_path / "cxr.png"
    Image.new("RGB", (256, 256), color="white").save(image_path)

    classifier = DummySkinClassifier(prediction=SkinPrediction(label="mel", confidence=0.95), available=True)
    agent = VisionAgent(llm=None, skin_classifier=classifier, modality_router=DummyRouter("chest_xray"))

    result = agent.analyze(str(image_path))
    assert result.image_type in {"unknown", "non_medical", "chest_xray"}


def test_vision_agent_routes_brain_mri_to_narrow_triage(tmp_path: Path) -> None:
    image_path = tmp_path / "mri.png"
    Image.new("RGB", (256, 256), color=(30, 30, 30)).save(image_path)

    agent = VisionAgent(llm=None, modality_router=DummyRouter("brain_mri"))
    result = agent.analyze(str(image_path))

    assert result.image_type == "brain_mri"
    assert "not a general mri diagnosis" in result.analysis_notes.lower()


def test_vision_agent_uses_cxr_classifier_for_chest_route(tmp_path: Path) -> None:
    image_path = tmp_path / "cxr.png"
    Image.new("RGB", (256, 256), color=(120, 120, 120)).save(image_path)

    cxr_prediction = CxrPrediction(
        finding_probabilities={
            "consolidation": 0.81,
            "effusion": 0.22,
            "cardiomegaly": 0.11,
            "pneumothorax": 0.08,
            "pneumonia": 0.77,
        }
    )
    agent = VisionAgent(
        llm=None,
        cxr_classifier=DummyCxrClassifier(prediction=cxr_prediction, available=True),
        modality_router=DummyRouter("chest_xray"),
    )

    result = agent.analyze(str(image_path))
    assert result.image_type == "chest_xray"
    assert any("consolidation" in finding.lower() for finding in result.findings)
