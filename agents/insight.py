"""Insight generator agent for deep data analysis."""

from typing import Any, Dict, List

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from agents.llm_utils import build_chat_model, invoke_with_retry
from logger import setup_logger

logger = setup_logger(__name__)


class InsightGeneratorAgent:
    """Agent that generates insights from data analysis."""
    
    def __init__(self):
        self.name = "InsightGenerator"
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are a senior data analyst. Use the structured dataset profile and anomaly "
                        "summary to generate concise, practical business insights. "
                        "Return valid JSON only with keys: executive_summary, key_findings, risks, "
                        "recommended_actions."
                    ),
                ),
                (
                    "human",
                    (
                        "Dataset path: {data_path}\n"
                        "Profile: {profile}\n"
                        "Anomalies: {anomalies}\n"
                        "Create 3-5 findings, 2-4 risks, and 2-4 recommended actions."
                    ),
                ),
            ]
        )
        self.parser = JsonOutputParser()
    
    def run(
        self,
        data_path: str,
        profile: Dict[str, Any],
        anomalies: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate insights from data.
        
        Args:
            data_path: Path to data file
            profile: Data profile
            anomalies: Detected anomalies
        
        Returns:
            Generated insights and analysis
        """
        logger.info(f"Starting insight generation for {data_path}")
        baseline = self._build_baseline_insights(profile, anomalies)

        try:
            chain = self.prompt | build_chat_model() | self.parser
            llm_result = invoke_with_retry(
                chain,
                {
                    "data_path": data_path,
                    "profile": profile,
                    "anomalies": anomalies,
                }
            )

            result = {
                "status": "success",
                "executive_summary": llm_result.get("executive_summary", baseline["executive_summary"]),
                "key_findings": llm_result.get("key_findings", baseline["key_findings"]),
                "risks": llm_result.get("risks", baseline["risks"]),
                "recommended_actions": llm_result.get(
                    "recommended_actions",
                    baseline["recommended_actions"],
                ),
                "generation_mode": "langchain_llm",
            }
            logger.info("Insight generation completed with LangChain LLM chain")
            return result
        except Exception as exc:
            logger.warning(f"LLM insight generation failed, using fallback: {exc}")
            baseline["status"] = "success"
            baseline["generation_mode"] = "fallback"
            return baseline

    def _build_baseline_insights(
        self,
        profile: Dict[str, Any],
        anomalies: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create deterministic insights when the LLM is unavailable."""
        shape = profile.get("shape", {})
        missing = profile.get("missing_percentage", {})
        duplicate_rows = profile.get("duplicate_rows", 0)
        anomaly_rows = anomalies.get("total_anomalous_rows", 0)

        high_missing = [
            f"{column} ({pct:.1f}%)"
            for column, pct in missing.items()
            if pct and pct >= 10
        ][:5]

        findings: List[str] = [
            f"Dataset contains {shape.get('rows', 0):,} rows across {shape.get('columns', 0)} columns.",
            f"Anomaly detection flagged {anomaly_rows:,} rows for deeper review.",
        ]
        if duplicate_rows:
            findings.append(f"Detected {duplicate_rows:,} duplicate rows that may distort aggregates.")
        if high_missing:
            findings.append("Columns with meaningful missingness: " + ", ".join(high_missing))

        risks = []
        if duplicate_rows:
            risks.append("Duplicate rows can overstate totals and bias trend analysis.")
        if high_missing:
            risks.append("Missing data may weaken model quality and downstream reporting.")
        if anomaly_rows:
            risks.append("Flagged outliers may represent either genuine edge cases or data quality issues.")
        if not risks:
            risks.append("No major structural data-quality risks were detected from the current checks.")

        actions = []
        if duplicate_rows:
            actions.append("Deduplicate records before KPI reporting or model training.")
        if high_missing:
            actions.append("Investigate null-heavy columns and define fill/drop rules per field.")
        if anomaly_rows:
            actions.append("Review the flagged rows with domain owners to separate fraud, error, and valid extremes.")
        actions.append("Use this profile as a baseline and rerun after cleaning to compare improvements.")

        return {
            "executive_summary": (
                "The dataset has been profiled and screened for outliers. "
                "The next priority is to validate flagged anomalies and clean quality issues before deeper modeling."
            ),
            "key_findings": findings,
            "risks": risks,
            "recommended_actions": actions,
        }
