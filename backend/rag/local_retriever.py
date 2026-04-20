from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

from backend.models.schemas import SourceReference
from backend.tools.pdf_parser import PDFParser
from backend.utils.data_paths import canonical_guidelines_dir


PDF_PARSER = PDFParser()
GUIDELINE_ROOT = canonical_guidelines_dir()


def _tokenize(text: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if len(token) > 2}


def _compact(text: str) -> str:
    return " ".join(text.split())


@lru_cache(maxsize=32)
def _load_guideline_corpus() -> list[dict[str, str]]:
    snippets: list[dict[str, str]] = []
    if not GUIDELINE_ROOT.exists():
        return snippets

    for pdf_path in sorted(GUIDELINE_ROOT.glob("*.pdf")):
        try:
            raw_text = PDF_PARSER.extract_text(pdf_path)
        except Exception:
            continue

        title = PDF_PARSER.build_context_summary(raw_text, source_name=pdf_path.name).split(". ", 1)[0]
        paragraphs = [
            _compact(chunk)
            for chunk in re.split(r"\n\s*\n", raw_text)
            if len(_compact(chunk)) >= 80
        ]
        for paragraph in paragraphs[:40]:
            snippets.append(
                {
                    "title": title.replace("Guideline context: ", ""),
                    "snippet": paragraph[:900],
                    "path": str(pdf_path),
                }
            )
    return snippets


def retrieve_local_evidence(
    query_text: str,
    condition_terms: set[str] | None = None,
    limit: int = 5,
) -> tuple[list[str], list[SourceReference]]:
    query_terms = _tokenize(query_text)
    if condition_terms:
        query_terms |= {term.lower() for term in condition_terms}
    if not query_terms:
        return [], []

    scored: list[tuple[int, dict[str, str]]] = []
    for item in _load_guideline_corpus():
        snippet_terms = _tokenize(item["snippet"])
        overlap = len(query_terms & snippet_terms)
        title_overlap = len(query_terms & _tokenize(item["title"]))
        score = overlap + (title_overlap * 3)
        if score > 0:
            scored.append((score, item))

    scored.sort(key=lambda row: row[0], reverse=True)
    top_items = scored[:limit]

    evidence = [f"{item['title']}: {item['snippet']}" for _, item in top_items]
    sources = [
        SourceReference(title=item["title"], pmid=None, url=item["path"])
        for _, item in top_items
    ]
    return evidence, sources
