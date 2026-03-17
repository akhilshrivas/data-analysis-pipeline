"""Report writer agent for generating comprehensive analysis reports."""

from pathlib import Path
from typing import Any, Dict

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.llm_utils import build_chat_model, invoke_with_retry
from config import settings
from logger import setup_logger

logger = setup_logger(__name__)


class ReportWriterAgent:
    """Agent that generates reports from analysis results."""
    
    def __init__(self):
        self.name = "ReportWriter"
        self.output_dir = Path(settings.OUTPUTS_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are writing a markdown data analysis report for a developer learning "
                        "LangChain and LangGraph. Be concise, structured, and explain the important findings."
                    ),
                ),
                (
                    "human",
                    (
                        "Dataset path: {data_path}\n"
                        "Profile: {profile}\n"
                        "Anomalies: {anomalies}\n"
                        "Insights: {insights}\n"
                        "Visualizations: {visualizations}\n"
                        "Write a markdown report with sections: Overview, Data Quality, Anomalies, "
                        "Insights, Visual Plan, Recommended Next Steps."
                    ),
                ),
            ]
        )
    
    def run(
        self,
        data_path: str,
        profile: Dict[str, Any],
        anomalies: Dict[str, Any],
        insights: Dict[str, Any],
        visualizations: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report.
        
        Args:
            data_path: Path to data file
            profile: Data profile
            anomalies: Detected anomalies
            insights: Generated insights
            visualizations: Created visualizations
        
        Returns:
            Path to generated report
        """
        logger.info(f"Starting report generation for {data_path}")
        report_markdown = self._build_fallback_report(
            data_path=data_path,
            profile=profile,
            anomalies=anomalies,
            insights=insights,
            visualizations=visualizations,
        )

        generation_mode = "fallback"
        try:
            chain = self.prompt | build_chat_model(temperature=0.1) | StrOutputParser()
            report_markdown = invoke_with_retry(
                chain,
                {
                    "data_path": data_path,
                    "profile": profile,
                    "anomalies": anomalies,
                    "insights": insights,
                    "visualizations": visualizations,
                }
            )
            generation_mode = "langchain_llm"
        except Exception as exc:
            logger.warning(f"LLM report generation failed, using fallback: {exc}")

        output_path = self.output_dir / f"{Path(data_path).stem}_report.md"
        output_path.write_text(report_markdown, encoding="utf-8")

        return {
            "status": "success",
            "report_path": str(output_path),
            "content": report_markdown,
            "generation_mode": generation_mode,
        }

    def _build_fallback_report(
        self,
        data_path: str,
        profile: Dict[str, Any],
        anomalies: Dict[str, Any],
        insights: Dict[str, Any],
        visualizations: Dict[str, Any],
    ) -> str:
        """Create a deterministic markdown report when the LLM is unavailable."""
        shape = profile.get("shape", {})
        missing = profile.get("missing_percentage", {})
        top_missing = sorted(missing.items(), key=lambda item: item[1], reverse=True)[:5]
        findings = insights.get("key_findings", [])
        risks = insights.get("risks", [])
        actions = insights.get("recommended_actions", [])
        chart_recommendations = visualizations.get("recommended_charts", [])

        lines = [
            "# Data Analysis Report",
            "",
            "## Overview",
            f"- Source file: `{data_path}`",
            f"- Rows: {shape.get('rows', 0):,}",
            f"- Columns: {shape.get('columns', 0)}",
            "",
            "## Data Quality",
            f"- Duplicate rows: {profile.get('duplicate_rows', 0):,}",
        ]
        for column, pct in top_missing:
            lines.append(f"- Missing values: {column} = {pct:.2f}%")

        lines.extend(
            [
                "",
                "## Anomalies",
                f"- Total flagged rows: {anomalies.get('total_anomalous_rows', 0):,}",
            ]
        )
        for item in anomalies.get("top_columns", [])[:5]:
            lines.append(f"- {item['column']}: {item['score']} anomaly flags")

        lines.extend(["", "## Insights"])
        for finding in findings:
            lines.append(f"- {finding}")

        lines.extend(["", "## Risks"])
        for risk in risks:
            lines.append(f"- {risk}")

        lines.extend(["", "## Visual Plan"])
        for chart in chart_recommendations:
            lines.append(
                f"- {chart['chart_type']}: {chart['reason']} ({', '.join(chart.get('columns', []))})"
            )

        lines.extend(["", "## Recommended Next Steps"])
        for action in actions:
            lines.append(f"- {action}")

        return "\n".join(lines)
