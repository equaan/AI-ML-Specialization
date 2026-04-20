from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datasets import load_dataset, load_from_disk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agents.orchestrator import MediAgentOrchestrator
from backend.utils.data_paths import canonical_medmcqa_dir


DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "evaluation"
DEFAULT_MEDMCQA_DIR = canonical_medmcqa_dir()


@dataclass
class EvalRow:
    question_index: int
    question: str
    predicted_option: int
    expected_option: int
    is_correct: bool
    confidence: float


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _tokens(text: str) -> set[str]:
    return {tok for tok in re.findall(r"[a-z0-9]+", _normalize(text)) if len(tok) > 2}


def _jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _compose_prompt(question: str, options: list[str]) -> str:
    lines = [
        "Answer the medical MCQ using the provided options.",
        f"Question: {question.strip()}",
        "Options:",
        f"A) {options[0]}",
        f"B) {options[1]}",
        f"C) {options[2]}",
        f"D) {options[3]}",
        "Provide your best-supported diagnosis or condition.",
    ]
    return "\n".join(lines)


def _report_text(final_report: dict[str, Any]) -> str:
    parts: list[str] = []
    parts.append(str(final_report.get("patient_summary", "")))
    for diag in final_report.get("differential_diagnosis", []):
        parts.append(str(diag.get("condition", "")))
        parts.append(str(diag.get("clinical_rationale", "")))
        for item in diag.get("supporting_findings", []):
            parts.append(str(item))
    for line in final_report.get("recommended_next_steps", []):
        parts.append(str(line))
    return "\n".join(parts)


def _pick_option(report_blob: str, options: list[str]) -> tuple[int, float]:
    report_norm = _normalize(report_blob)
    report_tokens = _tokens(report_norm)

    scored: list[tuple[int, float]] = []
    for idx, option in enumerate(options):
        option_norm = _normalize(option)
        option_tokens = _tokens(option_norm)

        phrase_hit = 1.0 if option_norm and option_norm in report_norm else 0.0
        token_overlap = _jaccard(report_tokens, option_tokens)
        token_cover = 0.0
        if option_tokens:
            token_cover = len(report_tokens & option_tokens) / len(option_tokens)

        # Weighted score favors exact phrase while still rewarding semantic lexical overlap.
        score = (0.6 * phrase_hit) + (0.25 * token_cover) + (0.15 * token_overlap)
        scored.append((idx, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0]


def _load_medmcqa_split(split: str, dataset_dir: Path):
    try:
        return load_from_disk(str(dataset_dir))[split]
    except Exception:
        return load_dataset("medmcqa", split=split)


def evaluate(sample_size: int, split: str, selection: str, seed: int, dataset_dir: Path) -> dict[str, Any]:
    ds = _load_medmcqa_split(split, dataset_dir)
    total_available = len(ds)
    if total_available == 0:
        raise RuntimeError("MedMCQA split is empty; cannot evaluate.")

    target_size = min(sample_size, total_available)
    if selection == "first_n":
        sampled_indices = list(range(target_size))
    else:
        import random

        random.seed(seed)
        sampled_indices = sorted(random.sample(range(total_available), target_size))

    orchestrator = MediAgentOrchestrator()

    rows: list[EvalRow] = []
    failures = 0

    for idx in sampled_indices:
        record = ds[idx]
        question = str(record.get("question", "")).strip()
        options = [
            str(record.get("opa", "")).strip(),
            str(record.get("opb", "")).strip(),
            str(record.get("opc", "")).strip(),
            str(record.get("opd", "")).strip(),
        ]
        expected = int(record.get("cop", -1))

        if expected not in (0, 1, 2, 3) or any(not opt for opt in options):
            failures += 1
            continue

        prompt = _compose_prompt(question, options)

        try:
            result = orchestrator.run({"patient_symptoms": prompt, "messages": []})
            final_report = result.get("final_report", {})
            report_blob = _report_text(final_report)
            predicted, score = _pick_option(report_blob, options)

            rows.append(
                EvalRow(
                    question_index=idx,
                    question=question,
                    predicted_option=predicted,
                    expected_option=expected,
                    is_correct=(predicted == expected),
                    confidence=round(float(score), 4),
                )
            )
        except Exception:
            failures += 1

    total = len(rows)
    correct = sum(1 for row in rows if row.is_correct)
    accuracy = (correct / total) if total else 0.0

    return {
        "dataset": "medmcqa",
        "split": split,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_size_requested": sample_size,
        "sample_size_scored": total,
        "selection": selection,
        "seed": seed,
        "metric_definition": "Top-1 option accuracy: pick option whose text best matches generated full-pipeline report content (weighted phrase+token overlap)",
        "accuracy": round(accuracy, 4),
        "correct": correct,
        "total": total,
        "failures_or_skipped": failures,
        "records": [
            {
                "question_index": row.question_index,
                "question": row.question,
                "predicted_option": row.predicted_option,
                "expected_option": row.expected_option,
                "is_correct": row.is_correct,
                "confidence": row.confidence,
            }
            for row in rows
        ],
    }


def write_reports(metrics: dict[str, Any], output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "pipeline_medmcqa_accuracy_eval.json"
    md_path = output_dir / "pipeline_medmcqa_accuracy_eval.md"

    json_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = [
        "# Full Pipeline MedMCQA Evaluation (Accuracy)",
        "",
        f"- Dataset: {metrics['dataset']} ({metrics['split']})",
        f"- Timestamp (UTC): {metrics['timestamp_utc']}",
        f"- Requested sample size: {metrics['sample_size_requested']}",
        f"- Scored sample size: {metrics['sample_size_scored']}",
        f"- Selection: {metrics['selection']}",
        f"- Metric: {metrics['metric_definition']}",
        f"- Accuracy: {metrics['accuracy']} ({metrics['correct']}/{metrics['total']})",
        f"- Failures/Skipped: {metrics['failures_or_skipped']}",
        "",
        "Detailed per-question results are stored in:",
        f"- {json_path}",
    ]

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate full MediAgent pipeline on MedMCQA top-1 accuracy.")
    parser.add_argument("--sample-size", type=int, default=50, help="Number of MedMCQA questions to evaluate.")
    parser.add_argument(
        "--split",
        type=str,
        default="train",
        choices=["train", "validation", "test"],
        help="Dataset split to evaluate.",
    )
    parser.add_argument(
        "--selection",
        type=str,
        default="first_n",
        choices=["first_n", "random"],
        help="How to pick evaluation rows from the split.",
    )
    parser.add_argument("--seed", type=int, default=42, help="Random seed when selection=random.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for output reports.",
    )
    parser.add_argument(
        "--dataset-dir",
        type=Path,
        default=DEFAULT_MEDMCQA_DIR,
        help="Local MedMCQA dataset directory; falls back to Hugging Face if missing.",
    )
    args = parser.parse_args()

    metrics = evaluate(
        sample_size=args.sample_size,
        split=args.split,
        selection=args.selection,
        seed=args.seed,
        dataset_dir=args.dataset_dir,
    )
    json_path, md_path = write_reports(metrics, args.output_dir)

    print(f"Evaluation complete. Accuracy: {metrics['accuracy']} ({metrics['correct']}/{metrics['total']})")
    print(f"Failures/Skipped: {metrics['failures_or_skipped']}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()
