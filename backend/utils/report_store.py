from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class StoredReport:
    session_id: str
    report: dict[str, Any]


class ReportStore:
    def __init__(self) -> None:
        self._reports: dict[str, StoredReport] = {}

    def save(self, session_id: str, report: dict[str, Any]) -> None:
        self._reports[session_id] = StoredReport(session_id=session_id, report=report)

    def get(self, session_id: str) -> dict[str, Any] | None:
        stored = self._reports.get(session_id)
        return stored.report if stored else None


report_store = ReportStore()
