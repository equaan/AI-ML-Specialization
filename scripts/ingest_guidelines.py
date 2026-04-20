from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.embedder import BioBERTEmbedder
from backend.rag.vectorstore import get_chroma_client
from backend.tools.pdf_parser import PDFParser
from backend.utils.data_paths import canonical_guidelines_dir


DEFAULT_GUIDELINES_DIR = canonical_guidelines_dir()
CHUNK_SIZE_WORDS = 180
CHUNK_OVERLAP_WORDS = 30


@dataclass
class GuidelineChunk:
    chunk_id: str
    text: str
    metadata: dict[str, str]


def chunk_text(text: str, chunk_size_words: int = CHUNK_SIZE_WORDS, overlap_words: int = CHUNK_OVERLAP_WORDS) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    step = max(chunk_size_words - overlap_words, 1)
    start = 0
    while start < len(words):
        window = words[start : start + chunk_size_words]
        chunks.append(" ".join(window))
        start += step
    return chunks


def _compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _infer_guideline_org(filename: str) -> str:
    lower = filename.lower()
    if "nice" in lower:
        return "NICE"
    if "who" in lower:
        return "WHO"
    return "other"


def build_guideline_chunks(guidelines_dir: Path, max_files: int | None = None) -> list[GuidelineChunk]:
    parser = PDFParser()
    pdf_paths = sorted(guidelines_dir.rglob("*.pdf"))
    if max_files is not None:
        pdf_paths = pdf_paths[:max_files]

    chunks: list[GuidelineChunk] = []
    for pdf_path in pdf_paths:
        try:
            raw_text = parser.extract_text(pdf_path)
        except Exception:
            continue

        compact_text = _compact(raw_text)
        if len(compact_text) < 120:
            continue

        title = parser._extract_document_title(compact_text, source_name=pdf_path.name)
        org = _infer_guideline_org(pdf_path.name)
        for chunk_index, chunk in enumerate(chunk_text(compact_text)):
            chunk_hash = hashlib.md5(f"{pdf_path}:{chunk_index}".encode("utf-8")).hexdigest()
            chunks.append(
                GuidelineChunk(
                    chunk_id=f"guideline-{chunk_hash}",
                    text=chunk,
                    metadata={
                        "source": "medical_guideline",
                        "org": org,
                        "title": title,
                        "path": str(pdf_path),
                        "filename": pdf_path.name,
                    },
                )
            )

    return chunks


def ingest_guidelines(guidelines_dir: Path, max_files: int | None = None) -> int:
    chunks = build_guideline_chunks(guidelines_dir=guidelines_dir, max_files=max_files)
    if not chunks:
        return 0

    embedder = BioBERTEmbedder()
    embeddings = embedder.embed_texts([chunk.text for chunk in chunks])

    client = get_chroma_client()
    collection = client.get_or_create_collection("medical_guidelines", metadata={"hnsw:space": "cosine"})
    collection.upsert(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
        embeddings=embeddings,
    )
    return len(chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest guideline PDFs into ChromaDB medical_guidelines collection.")
    parser.add_argument("--guidelines-dir", type=Path, default=DEFAULT_GUIDELINES_DIR, help="Directory containing guideline PDFs.")
    parser.add_argument("--max-files", type=int, default=None, help="Optional cap on PDFs for smoke ingest.")
    args = parser.parse_args()

    total = ingest_guidelines(guidelines_dir=args.guidelines_dir, max_files=args.max_files)
    print(f"Ingested {total} guideline chunks into ChromaDB.")


if __name__ == "__main__":
    main()
