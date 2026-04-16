from __future__ import annotations

import argparse
import json
import random
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datasets import load_dataset

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agents.rag_agent import RAGAgent


DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "evaluation"


class _NoPubMedTool:
    """Offline-safe replacement that keeps evaluation deterministic."""

    def search(self, query: str, max_results: int = 5) -> list[Any]:
        _ = (query, max_results)
        return []


@dataclass
class EvalRow:
    question_index: int
    question: str
    expected_answer: str
    rank: int | None
    reciprocal_rank: float


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _compose_query(question: str, options: list[str]) -> str:
    clean_opts = [str(opt).strip() for opt in options if str(opt).strip()]
    return "\n".join([question.strip(), " ".join(clean_opts)]).strip()


def _resolve_expected_answer(answer: str, options: list[str]) -> str:
    raw = answer.strip()
    if not raw:
        return ""

    upper = raw.upper()
    if len(upper) == 1 and "A" <= upper <= "Z":
        index = ord(upper) - ord("A")
        if 0 <= index < len(options):
            return str(options[index]).strip()

    # Handle formats like "(A)" or "A.".
    letter_match = re.fullmatch(r"\(?\s*([A-Za-z])\s*\)?[\.:]?", raw)
    if letter_match:
        letter = letter_match.group(1).upper()
        index = ord(letter) - ord("A")
        if 0 <= index < len(options):
            return str(options[index]).strip()

    return raw


def _answer_in_text(answer: str, text: str) -> bool:
    answer_norm = _normalize(answer)
    text_norm = _normalize(text)
    if not answer_norm or not text_norm:
        return False

    # Direct phrase match is preferred.
    if answer_norm in text_norm:
        return True

    # Fallback: overlap on informative tokens.
    ans_tokens = [tok for tok in re.findall(r"[a-z0-9]+", answer_norm) if len(tok) > 2]
    if not ans_tokens:
        return False

    hit_count = sum(1 for tok in ans_tokens if tok in text_norm)
    return hit_count >= max(1, int(0.7 * len(ans_tokens)))


def evaluate(sample_size: int, seed: int, split: str, selection: str) -> dict[str, Any]:
    ds = load_dataset("bigbio/med_qa", name="med_qa_en_source", split=split)
    total_available = len(ds)
    if total_available == 0:
        raise RuntimeError("MedQA split is empty; cannot evaluate.")

    target_size = min(sample_size, total_available)
    if selection == "first_n":
        sampled_indices = list(range(target_size))
    else:
        random.seed(seed)
        sampled_indices = sorted(random.sample(range(total_available), target_size))

    agent = RAGAgent(pubmed_tool=_NoPubMedTool())

    rows: list[EvalRow] = []

    for idx in sampled_indices:
        record = ds[idx]
        question = str(record.get("question", "")).strip()
        options = [str(opt).strip() for opt in record.get("options", [])]
        answer_raw = str(record.get("answer", "")).strip()
        expected_answer = _resolve_expected_answer(answer_raw, options)

        query_text = _compose_query(question, options)
        rag_result = agent.analyze(query_text)
        evidence = rag_result.supporting_evidence[:5]

        rank: int | None = None
        reciprocal_rank = 0.0
        for position, snippet in enumerate(evidence, start=1):
            if _answer_in_text(expected_answer, snippet):
                rank = position
                reciprocal_rank = 1.0 / position
                break

        rows.append(
            EvalRow(
                question_index=idx,
                question=question,
                expected_answer=expected_answer,
                rank=rank,
                reciprocal_rank=reciprocal_rank,
            )
        )

    mrr = sum(row.reciprocal_rank for row in rows) / len(rows) if rows else 0.0
    hit_at_5 = sum(1 for row in rows if row.rank is not None)

    return {
        "dataset": "bigbio/med_qa",
        "split": split,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_size": len(rows),
        "seed": seed,
        "selection": selection,
        "metric_definition": "MRR@5 where relevance is detected by ground-truth answer string match in top-5 RAG supporting evidence",
        "mrr_at_5": round(mrr, 4),
        "hit_rate_at_5": round((hit_at_5 / len(rows)) if rows else 0.0, 4),
        "hits_at_5": hit_at_5,
        "total_questions": len(rows),
        "records": [
            {
                "question_index": row.question_index,
                "question": row.question,
                "expected_answer": row.expected_answer,
                "rank": row.rank,
                "reciprocal_rank": round(row.reciprocal_rank, 4),
            }
            for row in rows
        ],
    }


def write_reports(metrics: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "rag_medqa_mrr_eval.json"
    md_path = output_dir / "rag_medqa_mrr_eval.md"

    json_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = [
        "# RAG Agent MedQA Evaluation (MRR@5)",
        "",
        f"- Dataset: {metrics['dataset']} ({metrics['split']})",
        f"- Timestamp (UTC): {metrics['timestamp_utc']}",
        f"- Sample size: {metrics['sample_size']}",
        f"- Selection: {metrics['selection']}",
        f"- Metric: {metrics['metric_definition']}",
        f"- MRR@5: {metrics['mrr_at_5']}",
        f"- Hit@5: {metrics['hit_rate_at_5']} ({metrics['hits_at_5']}/{metrics['total_questions']})",
        "",
        "Detailed per-question results are stored in:",
        f"- {json_path}",
    ]

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate RAG Agent on MedQA with MRR@5.")
    parser.add_argument("--sample-size", type=int, default=100, help="Number of MedQA questions to evaluate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for reproducible sampling.")
    parser.add_argument(
        "--selection",
        type=str,
        default="first_n",
        choices=["first_n", "random"],
        help="How to pick evaluation rows from the split.",
    )
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "validation", "test"],
        help="MedQA split used for evaluation.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to store evaluation output files.",
    )
    args = parser.parse_args()

    metrics = evaluate(sample_size=args.sample_size, seed=args.seed, split=args.split, selection=args.selection)
    json_path, md_path = write_reports(metrics, args.output_dir)

    print(f"Evaluation complete. MRR@5: {metrics['mrr_at_5']}")
    print(f"Hit@5: {metrics['hit_rate_at_5']} ({metrics['hits_at_5']}/{metrics['total_questions']})")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()
