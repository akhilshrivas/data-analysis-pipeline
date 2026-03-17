"""Verification for the upgraded LangChain + LangGraph workflow."""

from pathlib import Path
import sys

from graph.workflow import run_analysis_sync


def main() -> int:
    sample_path = Path("data/samples/sales_data.csv")
    result = run_analysis_sync(str(sample_path), sample_path.name)

    assert result["status"] == "completed", result
    assert result["profile"], "profile missing"
    assert result["anomalies"], "anomalies missing"
    assert result["insights"], "insights missing"
    assert result["visualizations"], "visualizations missing"
    assert result["report"], "report missing"
    assert result["report"].get("content"), "report content missing"
    assert Path(result["report"]["report_path"]).exists(), "report file missing"

    print("Upgrade flow verification passed")
    print(result["insights"].get("generation_mode"))
    print(result["report"].get("generation_mode"))
    print(result["report"]["report_path"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
