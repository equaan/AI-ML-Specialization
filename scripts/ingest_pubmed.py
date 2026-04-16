from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.rag.embedder import BioBERTEmbedder
from backend.rag.vectorstore import get_chroma_client
from backend.tools.pubmed_tool import PubMedTool


DEFAULT_QUERIES = [
    "community acquired pneumonia diagnosis radiology",
    "covid pneumonitis chest imaging findings",
    "pulmonary edema chest xray differential diagnosis",
]


@dataclass
class PubMedIngestRecord:
    record_id: str
    text: str
    metadata: dict[str, str]


def fetch_pubmed_records(queries: list[str] | None = None, max_results_per_query: int = 5) -> list[PubMedIngestRecord]:
    tool = PubMedTool()
    records: list[PubMedIngestRecord] = []

    for query in queries or DEFAULT_QUERIES:
        articles = tool.search(query, max_results=max_results_per_query)
        for article in articles:
            text = f"{article.title}\n{article.abstract}".strip()
            if not text:
                continue
            records.append(
                PubMedIngestRecord(
                    record_id=f"pubmed-{article.pmid}",
                    text=text,
                    metadata={
                        "source": "pubmed",
                        "pmid": article.pmid,
                        "title": article.title,
                        "url": article.url,
                        "query": query,
                    },
                )
            )

    deduped: dict[str, PubMedIngestRecord] = {}
    for record in records:
        deduped[record.record_id] = record
    return list(deduped.values())


def ingest_pubmed(queries: list[str] | None = None, max_results_per_query: int = 5) -> int:
    records = fetch_pubmed_records(queries=queries, max_results_per_query=max_results_per_query)
    if not records:
        return 0

    embedder = BioBERTEmbedder()
    embeddings = embedder.embed_texts([record.text for record in records])

    client = get_chroma_client()
    collection = client.get_or_create_collection("pubmed_abstracts", metadata={"hnsw:space": "cosine"})
    collection.upsert(
        ids=[record.record_id for record in records],
        documents=[record.text for record in records],
        metadatas=[record.metadata for record in records],
        embeddings=embeddings,
    )
    return len(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest PubMed abstracts into ChromaDB.")
    parser.add_argument(
        "--queries",
        type=str,
        default="",
        help="Comma-separated search queries. Uses defaults if omitted.",
    )
    parser.add_argument(
        "--max-results-per-query",
        type=int,
        default=5,
        help="Number of PubMed hits per query (default: 5)",
    )
    args = parser.parse_args()

    query_list = [q.strip() for q in args.queries.split(",") if q.strip()] if args.queries else None
    total = ingest_pubmed(queries=query_list, max_results_per_query=args.max_results_per_query)
    print(f"Ingested {total} PubMed abstracts into ChromaDB.")
