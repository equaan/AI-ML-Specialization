from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class ReportStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store_path = Path.cwd() / ".demo" / "runtime" / "reports_store.json"
        self._store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._store_path.exists():
            self._write_store({})

    @staticmethod
    def _serialize(payload: dict[str, Any] | None) -> dict[str, Any] | None:
        if payload is None:
            return None
        return json.loads(json.dumps(payload, ensure_ascii=True))

    def _read_store(self) -> dict[str, dict[str, Any]]:
        if not self._store_path.exists():
            return {}
        try:
            return json.loads(self._store_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _write_store(self, payload: dict[str, dict[str, Any]]) -> None:
        self._store_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    def save(
        self,
        session_id: str,
        report: dict[str, Any],
        lab_report: dict[str, Any] | None = None,
        inputs: dict[str, Any] | None = None,
    ) -> None:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._lock:
            store = self._read_store()
            store[session_id] = {
                "session_id": session_id,
                "report": self._serialize(report),
                "lab_report": self._serialize(lab_report),
                "inputs": self._serialize(inputs),
                "created_at": created_at,
            }
            self._write_store(store)

    def get(self, session_id: str) -> dict[str, Any] | None:
        item = self.get_full(session_id)
        return item["report"] if item else None

    def get_full(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            store = self._read_store()
            return store.get(session_id)

    def list_recent(self, limit: int = 25) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 200))
        with self._lock:
            store = self._read_store()
        items = list(store.values())
        items.sort(key=lambda item: item.get("created_at", ""), reverse=True)
        return items[:safe_limit]


report_store = ReportStore()
