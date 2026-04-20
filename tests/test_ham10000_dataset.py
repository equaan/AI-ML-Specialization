from pathlib import Path

import pandas as pd
from PIL import Image

from backend.training.ham10000_dataset import Ham10000Record
from backend.training.ham10000_dataset import (
    Ham10000Dataset,
    load_ham10000_records,
    split_records,
)
from scripts.train_ham10000_baseline import _compute_class_weights


def test_load_ham10000_records_and_split(tmp_path: Path) -> None:
    dataset_dir = tmp_path / "ham10000"
    image_dir_1 = dataset_dir / "HAM10000_images_part_1"
    image_dir_2 = dataset_dir / "HAM10000_images_part_2"
    image_dir_1.mkdir(parents=True)
    image_dir_2.mkdir(parents=True)

    rows = []
    labels = ["nv", "mel", "bcc", "bkl", "akiec", "df", "vasc"] * 2
    for index, label in enumerate(labels, start=1):
        image_id = f"ISIC_{index:07d}"
        target_dir = image_dir_1 if index % 2 == 0 else image_dir_2
        Image.new("RGB", (32, 32), color="white").save(target_dir / f"{image_id}.jpg")
        rows.append({"image_id": image_id, "dx": label, "lesion_id": f"lesion_{index}"})

    pd.DataFrame(rows).to_csv(dataset_dir / "HAM10000_metadata.csv", index=False)

    records = load_ham10000_records(dataset_dir)
    assert len(records) == len(rows)

    train_records, val_records, test_records = split_records(records, seed=7)
    assert len(train_records) + len(val_records) + len(test_records) == len(records)

    sample_dataset = Ham10000Dataset(train_records, image_size=32)
    tensor, label_index = sample_dataset[0]
    assert tuple(tensor.shape) == (3, 32, 32)
    assert isinstance(label_index, int)


def test_compute_class_weights_gives_higher_weight_to_rare_class() -> None:
    records = [
        Ham10000Record("a", Path("a.jpg"), "nv", 5, "l1"),
        Ham10000Record("b", Path("b.jpg"), "nv", 5, "l2"),
        Ham10000Record("c", Path("c.jpg"), "mel", 4, "l3"),
    ]

    weights = _compute_class_weights(records)
    assert weights[4] > weights[5]
