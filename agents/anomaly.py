"""Anomaly detection agent for identifying unusual patterns."""

from typing import Any, Dict, List

from tools.analyzer import AnalyzerTool
from tools.data_loader import DataLoaderTool
from logger import setup_logger

logger = setup_logger(__name__)


class AnomalyDetectionAgent:
    """Agent that detects anomalies in data."""
    
    def __init__(self):
        self.name = "AnomalyDetector"
    
    def run(self, data_path: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect anomalies in data.
        
        Args:
            data_path: Path to data file
            profile: Data profile from profiler agent
        
        Returns:
            Detected anomalies and statistics
        """
        logger.info(f"Starting anomaly detection for {data_path}")
        try:
            df = DataLoaderTool.load_file(data_path)
            iqr_results = AnalyzerTool.detect_outliers(df, method="iqr")
            zscore_results = AnalyzerTool.detect_outliers(df, method="zscore")

            combined_rows = sorted(
                set(iqr_results.get("anomaly_rows", [])) | set(zscore_results.get("anomaly_rows", []))
            )
            top_columns = self._rank_anomalous_columns(iqr_results, zscore_results)
            summary = self._build_summary(profile, iqr_results, zscore_results, top_columns)

            return {
                "status": "success",
                "methods": {
                    "iqr": iqr_results,
                    "zscore": zscore_results,
                },
                "top_columns": top_columns,
                "total_anomalous_rows": len(combined_rows),
                "anomaly_rows": combined_rows[:100],
                "summary": summary,
            }
        except Exception as exc:
            logger.error(f"Anomaly detection failed: {exc}")
            return {
                "status": "failed",
                "error": str(exc),
            }

    def _rank_anomalous_columns(
        self,
        iqr_results: Dict[str, Any],
        zscore_results: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Rank columns by anomaly frequency across methods."""
        scores: Dict[str, Dict[str, Any]] = {}
        for method_name, method_results in {
            "iqr": iqr_results,
            "zscore": zscore_results,
        }.items():
            for column, details in method_results.get("columns", {}).items():
                entry = scores.setdefault(column, {"column": column, "score": 0, "methods": []})
                entry["score"] += details.get("count", 0)
                entry["methods"].append(
                    {
                        "method": method_name,
                        "count": details.get("count", 0),
                        "percentage": details.get("percentage", 0.0),
                    }
                )

        ranked = sorted(scores.values(), key=lambda item: item["score"], reverse=True)
        return ranked[:10]

    def _build_summary(
        self,
        profile: Dict[str, Any],
        iqr_results: Dict[str, Any],
        zscore_results: Dict[str, Any],
        top_columns: List[Dict[str, Any]],
    ) -> str:
        """Create a concise human-readable anomaly summary."""
        total_rows = profile.get("shape", {}).get("rows", 0)
        iqr_count = iqr_results.get("total_anomalies", 0)
        zscore_count = zscore_results.get("total_anomalies", 0)

        lines = [
            "ANOMALY DETECTION SUMMARY",
            "=" * 60,
            f"Dataset rows: {total_rows:,}" if total_rows else "Dataset rows: unknown",
            f"IQR anomalies: {iqr_count:,}",
            f"Z-score anomalies: {zscore_count:,}",
        ]

        if top_columns:
            lines.append("")
            lines.append("Most anomalous columns:")
            for item in top_columns[:5]:
                method_summary = ", ".join(
                    f"{method['method']}={method['count']}"
                    for method in item["methods"]
                )
                lines.append(f"- {item['column']}: {item['score']} total flags ({method_summary})")

        return "\n".join(lines)
