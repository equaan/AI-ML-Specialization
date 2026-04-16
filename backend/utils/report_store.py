from __future__ import annotations

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from backend.config import get_settings


class ReportStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        settings = get_settings()
        db_path = Path(settings.chromadb_path).parent / "reports.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self._db_path = db_path
        self._initialize_db()

    def _initialize_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS reports (
                    session_id TEXT PRIMARY KEY,
                    report_json TEXT NOT NULL,
                    lab_report_json TEXT,
                    inputs_json TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._db_path, check_same_thread=False)

    @staticmethod
    def _serialize(payload: dict[str, Any] | None) -> str | None:
        if payload is None:
            return None
        return json.dumps(payload, ensure_ascii=True)

    @staticmethod
    def _deserialize(payload: str | None) -> dict[str, Any] | None:
        if not payload:
            return None
        return json.loads(payload)

    def save(
        self,
        session_id: str,
        report: dict[str, Any],
        lab_report: dict[str, Any] | None = None,
        inputs: dict[str, Any] | None = None,
    ) -> None:
        created_at = datetime.now(timezone.utc).isoformat()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO reports (session_id, report_json, lab_report_json, inputs_json, created_at)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(session_id) DO UPDATE SET
                        report_json=excluded.report_json,
                        lab_report_json=excluded.lab_report_json,
                        inputs_json=excluded.inputs_json,
                        created_at=excluded.created_at
                    """,
                    (
                        session_id,
                        self._serialize(report),
                        self._serialize(lab_report),
                        self._serialize(inputs),
                        created_at,
                    ),
                )
                conn.commit()

    def get(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT report_json FROM reports WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        return self._deserialize(row[0]) if row else None

    def get_full(self, session_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute(
                """
                SELECT session_id, report_json, lab_report_json, inputs_json, created_at
                FROM reports
                WHERE session_id = ?
                """,
                (session_id,),
            ).fetchone()
        if not row:
            return None
        return {
            "session_id": row[0],
            "report": self._deserialize(row[1]),
            "lab_report": self._deserialize(row[2]),
            "inputs": self._deserialize(row[3]),
            "created_at": row[4],
        }

    def list_recent(self, limit: int = 25) -> list[dict[str, Any]]:
        safe_limit = max(1, min(limit, 200))
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT session_id, report_json, lab_report_json, inputs_json, created_at
                FROM reports
                ORDER BY datetime(created_at) DESC
                LIMIT ?
                """,
                (safe_limit,),
            ).fetchall()

        return [
            {
                "session_id": row[0],
                "report": self._deserialize(row[1]),
                "lab_report": self._deserialize(row[2]),
                "inputs": self._deserialize(row[3]),
                "created_at": row[4],
            }
            for row in rows
        ]


report_store = ReportStore()
