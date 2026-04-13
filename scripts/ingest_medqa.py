from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from datasets import load_dataset

from backend.rag.embedder import BioBERTEmbedder
from backend.rag.vectorstore import get_chroma_client


CHUNK_SIZE_WORDS = 180
CHUNK_OVERLAP_WORDS = 30


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


def build_chunks(limit: int | None = None, split: str = "train") -> list[MedQAChunk]:
    dataset = load_dataset("bigbio/med_qa", name="med_qa_en_source", split=split)
    items = dataset.select(range(min(limit, len(dataset)))) if limit else dataset
    chunks: list[MedQAChunk] = []

    for index, record in enumerate(items):
        prompt_parts = [
            str(record.get("question", "")).strip(),
            " ".join(str(option).strip() for option in record.get("options", []) if str(option).strip()),
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


def ingest_medqa(limit: int | None = None, split: str = "train") -> int:
    chunks = build_chunks(limit=limit, split=split)
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
    total = ingest_medqa(limit=100)
    print(f"Ingested {total} MedQA chunks into ChromaDB.")
