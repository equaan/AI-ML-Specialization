from __future__ import annotations

import argparse
import json
import random
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.agents.vision_agent import VisionAgent
from backend.utils.data_paths import canonical_ham10000_dir


DEFAULT_DATA_DIR = canonical_ham10000_dir()
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "evaluation"


def gather_images(dataset_dir: Path) -> list[Path]:
    patterns = ("*.jpg", "*.jpeg", "*.png")
    images: list[Path] = []
    for pattern in patterns:
        images.extend(dataset_dir.rglob(pattern))
    return sorted(images)


def evaluate(dataset_dir: Path, sample_size: int, seed: int) -> dict:
    images = gather_images(dataset_dir)
    if not images:
        raise RuntimeError(f"No images found under {dataset_dir}")

    if sample_size > len(images):
        sample_size = len(images)

    random.seed(seed)
    sample = random.sample(images, sample_size)

    agent = VisionAgent()

    records: list[dict] = []
    image_type_counts: Counter[str] = Counter()
    confidence_values: list[float] = []
    medical_correct = 0

    for image_path in sample:
        result = agent.analyze(image_path)
        predicted_medical = result.image_type != "non_medical"
        is_correct = predicted_medical  # HAM10000 images are medical by dataset definition.
        medical_correct += int(is_correct)

        image_type_counts[result.image_type] += 1
        confidence_values.append(float(result.confidence))

        records.append(
            {
                "image": str(image_path.relative_to(PROJECT_ROOT)),
                "image_type": result.image_type,
                "confidence": float(result.confidence),
                "is_correct": is_correct,
                "analysis_notes": result.analysis_notes,
            }
        )

    total = len(sample)
    accuracy = medical_correct / total if total else 0.0
    avg_conf = sum(confidence_values) / total if total else 0.0

    return {
        "dataset": "HAM10000",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sample_size": total,
        "seed": seed,
        "metric_definition": "medical-image detection accuracy (predicted image_type != non_medical)",
        "accuracy": round(accuracy, 4),
        "average_confidence": round(avg_conf, 4),
        "image_type_counts": dict(image_type_counts),
        "records": records,
    }


def write_reports(metrics: dict, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "vision_ham10000_eval.json"
    md_path = output_dir / "vision_ham10000_eval.md"

    json_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    lines = [
        "# Vision Agent HAM10000 Evaluation",
        "",
        f"- Dataset: {metrics['dataset']}",
        f"- Timestamp (UTC): {metrics['timestamp_utc']}",
        f"- Sample size: {metrics['sample_size']}",
        f"- Metric: {metrics['metric_definition']}",
        f"- Accuracy: {metrics['accuracy']}",
        f"- Average confidence: {metrics['average_confidence']}",
        "",
        "## Image Type Counts",
        "",
    ]

    for key, value in sorted(metrics["image_type_counts"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "Detailed per-image records are stored in:",
            f"- {json_path}",
        ]
    )

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate Vision Agent on HAM10000 images.")
    parser.add_argument("--dataset-dir", type=Path, default=DEFAULT_DATA_DIR, help="Path to HAM10000 images.")
    parser.add_argument("--sample-size", type=int, default=50, help="Number of images to evaluate.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for sampling.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for evaluation outputs.",
    )
    args = parser.parse_args()

    metrics = evaluate(args.dataset_dir, args.sample_size, args.seed)
    json_path, md_path = write_reports(metrics, args.output_dir)

    print(f"Evaluation complete. Accuracy: {metrics['accuracy']}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")


if __name__ == "__main__":
    main()
