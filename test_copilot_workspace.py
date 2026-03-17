"""Verify self-service analytics copilot workspace endpoints locally."""

from pathlib import Path
import sys

from agents.copilot import AnalyticsCopilotAgent
from graph.workflow import run_analysis_sync
from services.run_store import RunStore


def main() -> int:
    sample = Path("data/samples/sales_data.csv")
    result = run_analysis_sync(str(sample), sample.name)
    store = RunStore()
    run = store.save_run(
        file_name=sample.name,
        file_path=str(sample),
        options={"analysis_type": "Deep Analysis"},
        result=result,
    )

    fetched = store.get_run(run["run_id"])
    assert fetched is not None, "saved run not found"

    agent = AnalyticsCopilotAgent()
    answer = agent.answer("What should I investigate first?", fetched)
    assert answer["status"] == "success", answer
    assert answer["answer"], "copilot answer missing"

    print("Copilot workspace verification passed")
    print(run["run_id"])
    print(answer["mode"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
