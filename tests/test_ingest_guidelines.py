from pathlib import Path

from scripts.ingest_guidelines import build_guideline_chunks, chunk_text


def test_chunk_text_creates_windows() -> None:
    text = " ".join(["word"] * 420)
    chunks = chunk_text(text, chunk_size_words=100, overlap_words=20)
    assert len(chunks) >= 4


def test_build_guideline_chunks_handles_empty_dir(tmp_path: Path) -> None:
    chunks = build_guideline_chunks(tmp_path)
    assert chunks == []
