from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.utils.data_paths import (
    canonical_cxr_dir,
    canonical_guidelines_dir,
    canonical_ham10000_dir,
    canonical_medmcqa_dir,
    canonical_medqa_dir,
    canonical_mri_dir,
)


def _count_files(path: Path, patterns: tuple[str, ...]) -> int:
    total = 0
    for pattern in patterns:
        total += len(list(path.rglob(pattern)))
    return total


def build_report() -> dict:
    ham_dir = canonical_ham10000_dir()
    cxr_dir = canonical_cxr_dir()
    medqa_dir = canonical_medqa_dir()
    medmcqa_dir = canonical_medmcqa_dir()
    guidelines_dir = canonical_guidelines_dir()
    mri_dir = canonical_mri_dir()

    return {
        "ham10000": {
            "path": str(ham_dir),
            "exists": ham_dir.exists(),
            "image_count": _count_files(ham_dir, ("*.jpg", "*.jpeg", "*.png")),
            "metadata_present": (ham_dir / "HAM10000_metadata.csv").exists(),
        },
        "cxr_kaggle_pneumonia": {
            "path": str(cxr_dir),
            "exists": cxr_dir.exists(),
            "image_count": _count_files(cxr_dir, ("*.jpg", "*.jpeg", "*.png")),
            "train_present": (cxr_dir / "train").exists(),
            "val_present": (cxr_dir / "val").exists(),
            "test_present": (cxr_dir / "test").exists(),
        },
        "mri_utsw_glioma": {
            "path": str(mri_dir),
            "exists": mri_dir.exists(),
            "nii_count": _count_files(mri_dir, ("*.nii.gz", "*.nii")),
            "metadata_present": any(mri_dir.glob("*.tsv")),
        },
        "guidelines": {
            "path": str(guidelines_dir),
            "exists": guidelines_dir.exists(),
            "pdf_count": _count_files(guidelines_dir, ("*.pdf",)),
        },
        "medmcqa": {
            "path": str(medmcqa_dir),
            "exists": medmcqa_dir.exists(),
            "dataset_info_present": (medmcqa_dir / "train" / "dataset_info.json").exists(),
        },
        "medqa": {
            "path": str(medqa_dir),
            "exists": medqa_dir.exists(),
            "hf_export_present": (medqa_dir / "train" / "dataset_info.json").exists(),
            "jsonl_present": any(medqa_dir.glob("*.jsonl")),
        },
    }


def main() -> None:
    report = build_report()
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
