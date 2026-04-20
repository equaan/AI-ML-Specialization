from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"


def first_existing_path(*candidates: Path) -> Path:
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


def canonical_ham10000_dir() -> Path:
    return first_existing_path(
        RAW_DATA_DIR / "skin" / "ham10000",
        RAW_DATA_DIR / "ham10000" / "archive",
        RAW_DATA_DIR / "ham10000",
    )


def canonical_medmcqa_dir() -> Path:
    return first_existing_path(
        RAW_DATA_DIR / "text" / "medmcqa",
        RAW_DATA_DIR / "medmcqa" / "hf_medmcqa",
        RAW_DATA_DIR / "medmcqa",
    )


def canonical_medqa_dir() -> Path:
    return first_existing_path(
        RAW_DATA_DIR / "text" / "medqa",
        RAW_DATA_DIR / "medqa" / "data_clean" / "data_clean" / "questions" / "US",
        RAW_DATA_DIR / "medqa",
    )


def canonical_guidelines_dir() -> Path:
    return RAW_DATA_DIR / "guidelines"


def canonical_cxr_dir() -> Path:
    return first_existing_path(
        RAW_DATA_DIR / "cxr" / "kaggle_pneumonia",
        RAW_DATA_DIR / "cxr",
    )


def canonical_mri_dir() -> Path:
    return first_existing_path(
        RAW_DATA_DIR / "mri" / "utsw_glioma",
        RAW_DATA_DIR / "mri",
    )
