from pathlib import Path

from PIL import Image

from backend.training.isic_dataset import load_isic_split


def _write_isic_csv(path: Path, rows: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "image,MEL,NV,BCC,AKIEC,BKL,DF,VASC\n" + "\n".join(rows) + "\n",
        encoding="utf-8",
    )


def test_load_isic_split(tmp_path: Path) -> None:
    train_img_dir = tmp_path / "ISIC2018_Task3_Training_Input"
    val_img_dir = tmp_path / "ISIC2018_Task3_Validation_Input"
    train_img_dir.mkdir(parents=True)
    val_img_dir.mkdir(parents=True)

    Image.new("RGB", (16, 16), color="white").save(train_img_dir / "ISIC_1.jpg")
    Image.new("RGB", (16, 16), color="white").save(val_img_dir / "ISIC_2.jpg")

    _write_isic_csv(
        tmp_path / "ISIC2018_Task3_Training_GroundTruth" / "ISIC2018_Task3_Training_GroundTruth.csv",
        ["ISIC_1,1,0,0,0,0,0,0"],
    )
    _write_isic_csv(
        tmp_path / "ISIC2018_Task3_Validation_GroundTruth" / "ISIC2018_Task3_Validation_GroundTruth.csv",
        ["ISIC_2,0,1,0,0,0,0,0"],
    )

    split = load_isic_split(tmp_path)
    assert len(split.train) == 1
    assert len(split.validation) == 1
    assert split.train[0].label == "mel"
    assert split.validation[0].label == "nv"
