from pathlib import Path

from PIL import Image

from backend.training.chexpert_dataset import CheXpertDataset, load_chexpert_records


def test_load_chexpert_records_and_dataset(tmp_path: Path) -> None:
    images_dir = tmp_path / "train" / "patient1" / "study1"
    images_dir.mkdir(parents=True)
    image_path = images_dir / "view1_frontal.jpg"
    Image.new("RGB", (64, 64), color="white").save(image_path)

    csv_path = tmp_path / "train.csv"
    csv_path.write_text(
        "Path,Atelectasis,Cardiomegaly,Consolidation,Edema,Pleural Effusion,Pneumonia,Pneumothorax\n"
        "CheXpert-v1.0-small/train/patient1/study1/view1_frontal.jpg,1,0,1,0,0,1,0\n",
        encoding="utf-8",
    )

    records = load_chexpert_records(csv_path=csv_path, data_root=tmp_path)
    assert len(records) == 1
    assert records[0].finding_targets[0] == 1.0
    assert records[0].finding_targets[1] == 0.0

    dataset = CheXpertDataset(records, image_size=64)
    image_tensor, targets = dataset[0]
    assert tuple(image_tensor.shape) == (3, 64, 64)
    assert tuple(targets.shape) == (7,)
