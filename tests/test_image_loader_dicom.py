from pathlib import Path

import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset

from backend.tools.image_loader import load_image


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
    ds.Rows = 16
    ds.Columns = 16
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0
    ds.PixelData = (b"\x00\x00" * (16 * 16))
    ds.save_as(str(path))


def test_load_image_supports_dicom(tmp_path: Path) -> None:
    dicom_path = tmp_path / "sample.dcm"
    _write_minimal_dcm(dicom_path)

    image = load_image(dicom_path)
    assert image.mode == "RGB"
    assert image.size == (16, 16)
