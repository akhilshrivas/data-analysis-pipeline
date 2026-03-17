"""Self-service analytics copilot agent."""

from __future__ import annotations

from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.llm_utils import build_chat_model, invoke_with_retry
from logger import setup_logger

logger = setup_logger(__name__)


class AnalyticsCopilotAgent:
    """Answer user questions against a saved analysis workspace."""

    def __init__(self):
        self.name = "AnalyticsCopilot"
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an analytics copilot for a self-service data platform. "
                        "Answer only from the provided run context. Be practical, specific, "
                        "and reference the analysis outputs when possible. If the answer is not "
                        "supported by the context, say that clearly."
                    ),
                ),
                (
                    "human",
                    (
                        "Question: {question}\n"
                        "Run summary: {summary}\n"
                        "Profile: {profile}\n"
                        "Anomalies: {anomalies}\n"
                        "Insights: {insights}\n"
                        "Report: {report}\n"
                        "Answer in concise markdown with a short direct answer and 2-4 supporting bullets."
                    ),
                ),
            ]
        )

    def answer(self, question: str, run_record: Dict[str, Any]) -> Dict[str, Any]:
        """Return a copilot answer for a saved run."""
        result = run_record.get("result", {})
        fallback = self._fallback_answer(question, run_record)

        try:
            chain = self.prompt | build_chat_model(temperature=0.1) | StrOutputParser()
            answer = invoke_with_retry(
                chain,
                {
                    "question": question,
                    "summary": run_record.get("summary", {}),
                    "profile": result.get("profile", {}),
                    "anomalies": result.get("anomalies", {}),
                    "insights": result.get("insights", {}),
                    "report": result.get("report", {}),
                },
            )
            return {"status": "success", "answer": answer, "mode": "langchain_llm"}
        except Exception as exc:
            logger.warning(f"Copilot LLM answer failed, using fallback: {exc}")
            return {"status": "success", "answer": fallback, "mode": "fallback"}

    def _fallback_answer(self, question: str, run_record: Dict[str, Any]) -> str:
        """Create a deterministic answer when the LLM is unavailable."""
        summary = run_record.get("summary", {})
        result = run_record.get("result", {})
        anomalies = result.get("anomalies", {})
        insights = result.get("insights", {})

        return "\n".join(
            [
                f"Direct answer: based on the saved run for `{run_record.get('file_name', 'dataset')}`, here is the most relevant context for: {question}",
                "",
                f"- Dataset size: {summary.get('rows', 0):,} rows x {summary.get('columns', 0)} columns.",
                f"- Flagged anomaly rows: {summary.get('flagged_rows', 0):,}.",
                f"- Executive summary: {summary.get('executive_summary') or insights.get('executive_summary', 'No summary available.')}",
                f"- Most anomalous columns: {', '.join(item['column'] for item in anomalies.get('top_columns', [])[:3]) or 'No anomaly columns recorded.'}",
            ]
        )
