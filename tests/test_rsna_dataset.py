from pathlib import Path

import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset

from backend.training.rsna_dataset import RsnaDataset, load_rsna_records


def _write_minimal_dcm(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    meta = FileMetaDataset()
    meta.MediaStorageSOPClassUID = pydicom.uid.generate_uid()
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian

    ds = FileDataset(str(path), {}, file_meta=meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.Rows = 8
    ds.Columns = 8
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.PixelData = (b"\x00\x00" * 64)
    ds.save_as(str(path))


def test_load_rsna_records_and_dataset(tmp_path: Path) -> None:
    rsna_dir = tmp_path
    (rsna_dir / "stage_2_train_images").mkdir(parents=True)

    patient_id = "abc"
    _write_minimal_dcm(rsna_dir / "stage_2_train_images" / f"{patient_id}.dcm")

    (rsna_dir / "stage_2_train_labels.csv").write_text(
        "patientId,x,y,width,height,Target\n"
        "abc,,,,,1\n",
        encoding="utf-8",
    )

    records = load_rsna_records(rsna_dir)
    assert len(records) == 1
    assert records[0].target == 1

    dataset = RsnaDataset(records, image_size=32)
    image_tensor, target = dataset[0]
    assert tuple(image_tensor.shape) == (3, 32, 32)
    assert float(target.item()) == 1.0
