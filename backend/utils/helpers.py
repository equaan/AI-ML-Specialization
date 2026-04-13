from __future__ import annotations

from pathlib import Path
from uuid import uuid4


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def generate_session_id() -> str:
    return uuid4().hex
