from pathlib import Path

from PIL import Image
import pytest

from backend.agents.modality_router import ModalityRouter


def test_modality_router_classifies_pdf() -> None:
    router = ModalityRouter()
    assert router.classify(pdf_path="notes.pdf") == "report_pdf"


def test_modality_router_classifies_by_path_keywords() -> None:
    router = ModalityRouter()
    assert router.classify(image_path="data/raw/skin/ham10000/ISIC_1.jpg") == "skin_lesion"
    assert router.classify(image_path="data/raw/cxr/patient_xray.png") == "chest_xray"
    assert router.classify(image_path="data/raw/mri/brain_scan.png") == "brain_mri"


def test_modality_router_classifies_skin_from_color_pattern(tmp_path: Path) -> None:
    image_path = tmp_path / "unknown.jpg"
    image = Image.new("RGB", (256, 256), color=(210, 140, 120))
    image.save(image_path)

    router = ModalityRouter()
    assert router.classify(image_path=image_path) == "skin_lesion"


def test_modality_router_classifies_mri_from_dark_grayscale(tmp_path: Path) -> None:
    image_path = tmp_path / "unknown.jpg"
    image = Image.new("RGB", (256, 256), color=(20, 20, 20))
    image.save(image_path)

    router = ModalityRouter()
    assert router.classify(image_path=image_path) == "brain_mri"


def test_modality_router_uses_dicom_capable_loader(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    image_path = tmp_path / "upload.dcm"
    image_path.write_bytes(b"dummy")

    def fake_load_image(_path):
        return Image.new("RGB", (256, 256), color=(130, 130, 130))

    monkeypatch.setattr("backend.agents.modality_router.load_image", fake_load_image)

    router = ModalityRouter()
    assert router.classify(image_path=image_path) == "chest_xray"
