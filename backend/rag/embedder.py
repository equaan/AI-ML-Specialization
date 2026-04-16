from __future__ import annotations

import hashlib
from typing import Any, Iterable


DEFAULT_EMBEDDING_MODEL = "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb"


class BioBERTEmbedder:
    def __init__(self, model_name: str = DEFAULT_EMBEDDING_MODEL) -> None:
        self.model_name = model_name
        self._model: Any | None = None

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        try:
            model = self._get_model()
            embeddings = model.encode(texts, normalize_embeddings=True)
            return [embedding.tolist() for embedding in embeddings]
        except Exception:
            # Fallback keeps local development moving until the full model is available.
            return [self._hash_embedding(text) for text in texts]

    def _get_model(self) -> Any:
        if self._model is None:
            # Import lazily so backend startup does not fail when optional
            # transformer dependencies are temporarily incompatible.
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    @staticmethod
    def _hash_embedding(text: str, dimensions: int = 768) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        values = list(digest) * ((dimensions // len(digest)) + 1)
        trimmed = values[:dimensions]
        return [((value / 255.0) * 2.0) - 1.0 for value in trimmed]


def embed_texts(texts: list[str]) -> list[list[float]]:
    return BioBERTEmbedder().embed_texts(texts)
