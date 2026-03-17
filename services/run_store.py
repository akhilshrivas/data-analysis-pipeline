"""Persistence helpers for saved analysis runs."""

from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from config import settings


class RunStore:
    """Persist analysis runs as JSON files for workspace-style retrieval."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.RUNS_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_run(
        self,
        *,
        file_name: str,
        file_path: str,
        options: Dict[str, Any],
        result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Save a completed analysis run and return its stored record."""
        run_id = uuid4().hex[:12]
        created_at = datetime.now(UTC).isoformat()
        record = {
            "run_id": run_id,
            "created_at": created_at,
            "file_name": file_name,
            "file_path": file_path,
            "options": options,
            "result": result,
            "summary": self._build_summary(result),
        }
        self._write_record(run_id, record)
        return record

    def list_runs(self) -> List[Dict[str, Any]]:
        """Return saved runs newest first."""
        records = []
        for file_path in sorted(self.base_dir.glob("*.json"), reverse=True):
            try:
                with file_path.open("r", encoding="utf-8") as handle:
                    records.append(json.load(handle))
            except Exception:
                continue
        return records

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a saved run by id."""
        path = self.base_dir / f"{run_id}.json"
        if not path.exists():
            return None
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def latest_run(self) -> Optional[Dict[str, Any]]:
        """Return the most recent run if one exists."""
        runs = self.list_runs()
        return runs[0] if runs else None

    def _write_record(self, run_id: str, record: Dict[str, Any]) -> None:
        path = self.base_dir / f"{run_id}.json"
        with path.open("w", encoding="utf-8") as handle:
            json.dump(record, handle, indent=2)

    def _build_summary(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a compact summary for workspace listings."""
        profile = result.get("profile", {})
        anomalies = result.get("anomalies", {})
        insights = result.get("insights", {})
        report = result.get("report", {})
        return {
            "rows": profile.get("shape", {}).get("rows", 0),
            "columns": profile.get("shape", {}).get("columns", 0),
            "flagged_rows": anomalies.get("total_anomalous_rows", 0),
            "executive_summary": insights.get("executive_summary", ""),
            "report_mode": report.get("generation_mode", "n/a"),
        }
