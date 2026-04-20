from pathlib import Path

from PIL import Image

from backend.training.cxr_dataset import CxrDataset, load_kaggle_cxr_records


def _make_image(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (64, 64), color="white").save(path)


def test_load_kaggle_cxr_records_and_dataset(tmp_path: Path) -> None:
    for split in ("train", "val", "test"):
        _make_image(tmp_path / split / "NORMAL" / f"{split}_normal.jpg")
        _make_image(tmp_path / split / "PNEUMONIA" / f"{split}_pneumonia.jpg")

    train_records = load_kaggle_cxr_records(tmp_path, split="train")
    assert len(train_records) == 2

    label_vectors = [record.finding_targets for record in train_records]
    assert any(vector[-1] == 1.0 for vector in label_vectors)
    assert any(vector[-1] == 0.0 for vector in label_vectors)

    dataset = CxrDataset(train_records, image_size=64)
    image_tensor, finding_targets = dataset[0]
    assert tuple(image_tensor.shape) == (3, 64, 64)
    assert tuple(finding_targets.shape) == (5,)
