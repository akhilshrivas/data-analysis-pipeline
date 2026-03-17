"""Phase 3 verification for the anomaly detection workflow."""

from pathlib import Path
import sys

from agents.anomaly import AnomalyDetectionAgent
from agents.profiler import DataProfilerAgent
from graph.workflow import run_analysis_sync


def main() -> int:
    sample_file = Path("data/samples/sales_data.csv")
    if not sample_file.exists():
        print(f"Missing sample file: {sample_file}")
        return 1

    profiler = DataProfilerAgent()
    profile_result = profiler.run(str(sample_file))
    if profile_result.get("status") != "success":
        print(f"Profiler failed: {profile_result}")
        return 1

    anomaly_agent = AnomalyDetectionAgent()
    anomaly_result = anomaly_agent.run(str(sample_file), profile_result["profile"])
    if anomaly_result.get("status") != "success":
        print(f"Anomaly agent failed: {anomaly_result}")
        return 1

    workflow_result = run_analysis_sync(str(sample_file), sample_file.name)
    if workflow_result.get("status") != "completed":
        print(f"Workflow failed: {workflow_result}")
        return 1

    print("Phase 3 verification passed")
    print(f"Flagged rows: {anomaly_result.get('total_anomalous_rows', 0)}")
    print(f"Top anomaly columns: {[item['column'] for item in anomaly_result.get('top_columns', [])[:3]]}")
    print(f"Workflow messages: {len(workflow_result.get('messages', []))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
