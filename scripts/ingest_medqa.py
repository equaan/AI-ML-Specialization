from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from datasets import load_dataset, load_from_disk

from backend.rag.embedder import BioBERTEmbedder
from backend.rag.vectorstore import get_chroma_client
from backend.utils.data_paths import canonical_medqa_dir


CHUNK_SIZE_WORDS = 180
CHUNK_OVERLAP_WORDS = 30
DEFAULT_MEDQA_DIR = canonical_medqa_dir()


@dataclass
class MedQAChunk:
    chunk_id: str
    text: str
    metadata: dict[str, str]


def chunk_text(text: str, chunk_size_words: int = CHUNK_SIZE_WORDS, overlap_words: int = CHUNK_OVERLAP_WORDS) -> list[str]:
    words = text.split()
    if not words:
        return []

    chunks: list[str] = []
    start = 0
    step = max(chunk_size_words - overlap_words, 1)
    while start < len(words):
        chunk_words = words[start : start + chunk_size_words]
        chunks.append(" ".join(chunk_words))
        start += step
    return chunks


def _load_local_hf_dataset(dataset_dir: Path, split: str):
    try:
        return load_from_disk(str(dataset_dir))[split]
    except Exception:
        return None


def _iter_us_jsonl_records(dataset_dir: Path, split: str):
    filename_map = {
        "train": "train.jsonl",
        "validation": "test.jsonl",
        "test": "test.jsonl",
    }
    target = dataset_dir / filename_map[split]
    if not target.exists():
        return None

    records: list[dict] = []
    with target.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def load_medqa_records(split: str, dataset_dir: Path | None = None):
    dataset_dir = dataset_dir or DEFAULT_MEDQA_DIR

    local_hf = _load_local_hf_dataset(dataset_dir, split)
    if local_hf is not None:
        return local_hf

    local_jsonl = _iter_us_jsonl_records(dataset_dir, split)
    if local_jsonl is not None:
        return local_jsonl

    return load_dataset("bigbio/med_qa", name="med_qa_en_source", split=split)


def build_chunks(limit: int | None = None, split: str = "train", dataset_dir: Path | None = None) -> list[MedQAChunk]:
    dataset = load_medqa_records(split=split, dataset_dir=dataset_dir)
    if limit:
        target_size = min(limit, len(dataset))
        items = dataset.select(range(target_size)) if hasattr(dataset, "select") else dataset[:target_size]
    else:
        items = dataset
    chunks: list[MedQAChunk] = []

    for index, record in enumerate(items):
        options = record.get("options", [])
        if isinstance(options, list):
            option_text = " ".join(str(option).strip() for option in options if str(option).strip())
        elif isinstance(options, dict):
            option_text = " ".join(str(value).strip() for _, value in sorted(options.items()) if str(value).strip())
        else:
            option_text = ""

        prompt_parts = [
            str(record.get("question", "")).strip(),
            option_text,
            str(record.get("answer", "")).strip(),
        ]
        joined = "\n".join(part for part in prompt_parts if part)
        for chunk_index, chunk in enumerate(chunk_text(joined)):
            chunks.append(
                MedQAChunk(
                    chunk_id=f"medqa-{index}-{chunk_index}",
                    text=chunk,
                    metadata={
                        "source": "bigbio/med_qa",
                        "split": split,
                        "record_index": str(index),
                    },
                )
            )

    return chunks


def ingest_medqa(limit: int | None = None, split: str = "train", dataset_dir: Path | None = None) -> int:
    chunks = build_chunks(limit=limit, split=split, dataset_dir=dataset_dir)
    if not chunks:
        return 0

    embedder = BioBERTEmbedder()
    embeddings = embedder.embed_texts([chunk.text for chunk in chunks])

    client = get_chroma_client()
    collection = client.get_or_create_collection("medqa_chunks", metadata={"hnsw:space": "cosine"})
    collection.upsert(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
        embeddings=embeddings,
    )
    return len(chunks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest MedQA chunks into ChromaDB.")
    parser.add_argument("--limit", type=int, default=100, help="Number of records to process (default: 100)")
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "validation", "test"],
        help="Dataset split to ingest (default: train)",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=DEFAULT_MEDQA_DIR,
        help="Local MedQA dataset directory; falls back to Hugging Face if missing.",
    )
    args = parser.parse_args()

    total = ingest_medqa(limit=args.limit, split=args.split, dataset_dir=args.dataset_dir)
    print(f"Ingested {total} MedQA chunks into ChromaDB.")
