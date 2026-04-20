from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


CHEXPERT_FINDINGS = [
    "Atelectasis",
    "Cardiomegaly",
    "Consolidation",
    "Edema",
    "Pleural Effusion",
    "Pneumonia",
    "Pneumothorax",
]


@dataclass
class CheXpertRecord:
    path: str
    labels: dict[str, float]


def normalize_label(value: str | None) -> float:
    if value is None or value == "":
        return 0.0
    numeric = float(value)
    if numeric < 0:
        return 0.0
    if numeric > 0:
        return 1.0
    return 0.0


def load_chexpert_csv(csv_path: Path, limit: int | None = None) -> list[CheXpertRecord]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CheXpert CSV not found: {csv_path}")

    records: list[CheXpertRecord] = []
    with csv_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            path = str(row.get("Path", "")).strip()
            if not path:
                continue
            labels = {
                finding: normalize_label(row.get(finding))
                for finding in CHEXPERT_FINDINGS
            }
            records.append(CheXpertRecord(path=path, labels=labels))
            if limit is not None and len(records) >= limit:
                break

    return records


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and summarize CheXpert CSV labels.")
    parser.add_argument("--csv", type=Path, required=True, help="Path to CheXpert train.csv or valid.csv")
    parser.add_argument("--limit", type=int, default=1000, help="Optional cap for quick checks")
    args = parser.parse_args()

    records = load_chexpert_csv(args.csv, limit=args.limit)
    if not records:
        print("No CheXpert records loaded.")
        return

    counts = {finding: 0 for finding in CHEXPERT_FINDINGS}
    for record in records:
        for finding in CHEXPERT_FINDINGS:
            if record.labels[finding] > 0:
                counts[finding] += 1

    print(f"Loaded {len(records)} CheXpert rows")
    for finding in CHEXPERT_FINDINGS:
        print(f"{finding}: {counts[finding]}")


if __name__ == "__main__":
    main()
