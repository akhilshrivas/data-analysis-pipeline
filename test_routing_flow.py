"""Verify LangGraph conditional routing based on selected workflow options."""

from pathlib import Path
import sys

from graph.workflow import run_analysis_sync


def main() -> int:
    sample_path = Path("data/samples/sales_data.csv")
    result = run_analysis_sync(
        str(sample_path),
        sample_path.name,
        options={
            "analysis_type": "Quick Profile",
            "include_anomalies": False,
            "include_insights": False,
            "include_visualizations": False,
            "include_report": True,
        },
    )

    assert result["status"] == "completed", result
    assert not result.get("anomalies"), "anomalies should be skipped"
    assert not result.get("insights"), "insights should be skipped"
    assert not result.get("visualizations"), "visualizations should be skipped"
    assert result.get("report"), "report should still run"
    assert "skip_anomalies" in result.get("completed_steps", []), result.get("completed_steps", [])
    assert "skip_insights" in result.get("completed_steps", []), result.get("completed_steps", [])
    assert "skip_visualizations" in result.get("completed_steps", []), result.get("completed_steps", [])

    print("Routing verification passed")
    print(result["completed_steps"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
