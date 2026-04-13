from __future__ import annotations

import base64
from io import BytesIO
from pathlib import Path

from PIL import Image, UnidentifiedImageError


SUPPORTED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}


def validate_image_path(image_path: str | Path) -> Path:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    if path.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
        raise ValueError(f"Unsupported image format: {path.suffix}")
    return path


def load_image(image_path: str | Path) -> Image.Image:
    path = validate_image_path(image_path)
    try:
        image = Image.open(path)
        image.load()
        return image.convert("RGB")
    except UnidentifiedImageError as exc:
        raise ValueError(f"Unreadable image file: {path}") from exc


def resize_image(image: Image.Image, max_size: tuple[int, int] = (1024, 1024)) -> Image.Image:
    resized = image.copy()
    resized.thumbnail(max_size)
    return resized


def encode_image_to_base64(image_path: str | Path, max_size: tuple[int, int] = (1024, 1024)) -> str:
    image = resize_image(load_image(image_path), max_size=max_size)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def looks_like_medical_image(image: Image.Image) -> bool:
    # Conservative heuristic to avoid over-claiming until the vision model is wired in.
    width, height = image.size
    if width < 128 or height < 128:
        return False
    return True
