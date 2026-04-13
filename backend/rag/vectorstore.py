from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import chromadb
from chromadb.api.models.Collection import Collection

from backend.config import get_settings
from backend.utils.logger import get_logger


LOGGER = get_logger(__name__)
DEFAULT_COLLECTIONS = ("medqa_chunks", "pubmed_abstracts", "medical_guidelines")


@dataclass
class ChromaCollections:
    medqa_chunks: Collection
    pubmed_abstracts: Collection
    medical_guidelines: Collection


def get_chroma_client() -> chromadb.PersistentClient:
    settings = get_settings()
    return chromadb.PersistentClient(path=settings.chromadb_path)


def initialize_collections() -> ChromaCollections:
    client = get_chroma_client()
    collections: dict[str, Collection] = {}

    for name in DEFAULT_COLLECTIONS:
        collections[name] = client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
        LOGGER.info("Chroma collection ready: %s", name)

    return ChromaCollections(**collections)


def chromadb_is_healthy() -> bool:
    try:
        client = get_chroma_client()
        client.heartbeat()
        return True
    except Exception as exc:  # pragma: no cover - defensive health check
        LOGGER.warning("Chroma health check failed: %s", exc)
        return False


def query_collection(
    collection_name: str,
    query_embedding: list[float],
    n_results: int = 5,
) -> dict[str, Any]:
    client = get_chroma_client()
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )
    return collection.query(query_embeddings=[query_embedding], n_results=n_results)
