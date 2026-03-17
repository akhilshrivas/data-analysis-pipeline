"""Define individual nodes for the analysis graph."""

from typing import Any, Dict

from graph.state import AnalysisState
from agents.anomaly import AnomalyDetectionAgent
from agents.insight import InsightGeneratorAgent
from agents.profiler import DataProfilerAgent
from agents.reporter import ReportWriterAgent
from agents.visualizer import VisualizationAgent
from logger import setup_logger

logger = setup_logger(__name__)


def load_data_node(state: AnalysisState) -> AnalysisState:
    """Load data from file."""
    logger.info(f"Node: Loading data from {state.file_path}")
    state.add_message(f"Loading data from {state.file_name}")
    
    try:
        from tools.data_loader import DataLoaderTool
        df = DataLoaderTool.load_file(state.file_path)
        state.add_message(f"OK: Loaded {df.shape[0]:,} rows x {df.shape[1]} columns")
        state.mark_step_completed("load_data")
        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Load data error: {e}")
        return state


def profile_data_node(state: AnalysisState) -> AnalysisState:
    """Profile and explore data using the Data Profiler Agent."""
    logger.info("Node: Profiling data")
    state.add_message("Profiling data with DataProfilerAgent...")
    
    try:
        profiler = DataProfilerAgent()
        result = profiler.run(state.file_path)
        
        if result.get("status") == "success":
            state.profile = result.get("profile", {})
            state.add_message("OK: Data profile completed")
            state.mark_step_completed("profile_data")
            
            # Add insights
            insights = result.get("insights", [])
            for insight in insights[:3]:
                state.add_message(f"  - {insight}")
        else:
            state.error = result.get("error", "Unknown error")
            state.add_message(f"ERROR: Profiling failed: {state.error}")
        
        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Profile node error: {e}")
        return state


def detect_anomalies_node(state: AnalysisState) -> AnalysisState:
    """Detect anomalies in data."""
    logger.info("Node: Detecting anomalies")
    state.add_message("Detecting anomalies with AnomalyDetectionAgent...")

    try:
        detector = AnomalyDetectionAgent()
        result = detector.run(state.file_path, state.profile)

        if result.get("status") == "success":
            state.anomalies = result
            total_rows = result.get("total_anomalous_rows", 0)
            state.add_message(f"OK: Anomaly detection completed with {total_rows:,} flagged rows")
            state.mark_step_completed("detect_anomalies")
            for item in result.get("top_columns", [])[:3]:
                state.add_message(f"  - {item['column']}: {item['score']} anomaly flags")
        else:
            state.error = result.get("error", "Unknown anomaly detection error")
            state.add_message(f"ERROR: Anomaly detection failed: {state.error}")

        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Anomaly node error: {e}")
        return state


def generate_insights_node(state: AnalysisState) -> AnalysisState:
    """Generate insights from data."""
    logger.info("Node: Generating insights")
    state.add_message("Generating insights with InsightGeneratorAgent...")

    try:
        agent = InsightGeneratorAgent()
        result = agent.run(state.file_path, state.profile, state.anomalies)

        if result.get("status") == "success":
            state.insights = result
            state.add_message(f"OK: Insights generated via {result.get('generation_mode', 'unknown')}")
            state.mark_step_completed("generate_insights")
            for finding in result.get("key_findings", [])[:3]:
                state.add_message(f"  - {finding}")
        else:
            state.error = result.get("error", "Unknown insight generation error")
            state.add_message(f"ERROR: Insight generation failed: {state.error}")

        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Insight node error: {e}")
        return state


def create_visualizations_node(state: AnalysisState) -> AnalysisState:
    """Create visualizations."""
    logger.info("Node: Creating visualizations")
    state.add_message("Creating visualization recommendations with VisualizationAgent...")

    try:
        agent = VisualizationAgent()
        result = agent.run(state.file_path, state.profile, state.insights)

        if result.get("status") == "success":
            state.visualizations = result
            state.add_message(
                f"OK: Generated {len(result.get('recommended_charts', []))} chart recommendations"
            )
            state.mark_step_completed("create_visualizations")
        else:
            state.error = result.get("error", "Unknown visualization error")
            state.add_message(f"ERROR: Visualization generation failed: {state.error}")

        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Visualization node error: {e}")
        return state


def generate_report_node(state: AnalysisState) -> AnalysisState:
    """Generate final report."""
    logger.info("Node: Generating report")
    state.add_message("Generating report with ReportWriterAgent...")

    try:
        agent = ReportWriterAgent()
        result = agent.run(
            state.file_path,
            state.profile,
            state.anomalies,
            state.insights,
            state.visualizations,
        )

        if result.get("status") == "success":
            state.report = result
            state.add_message(f"OK: Report generated at {result.get('report_path')}")
            state.mark_step_completed("generate_report")
            state.status = "completed"
        else:
            state.error = result.get("error", "Unknown report generation error")
            state.add_message(f"ERROR: Report generation failed: {state.error}")

        return state
    except Exception as e:
        state.error = str(e)
        state.add_message(f"ERROR: {e}")
        logger.error(f"Report node error: {e}")
        return state


def skip_anomalies_node(state: AnalysisState) -> AnalysisState:
    """Skip anomaly detection when disabled."""
    state.add_message("Skipping anomaly detection based on workflow options")
    state.mark_step_completed("skip_anomalies")
    return state


def skip_insights_node(state: AnalysisState) -> AnalysisState:
    """Skip insight generation when disabled."""
    state.add_message("Skipping insight generation based on workflow options")
    state.mark_step_completed("skip_insights")
    return state


def skip_visualizations_node(state: AnalysisState) -> AnalysisState:
    """Skip visualization generation when disabled."""
    state.add_message("Skipping visualization generation based on workflow options")
    state.mark_step_completed("skip_visualizations")
    return state


def skip_report_node(state: AnalysisState) -> AnalysisState:
    """Skip report generation when disabled."""
    state.add_message("Skipping report generation based on workflow options")
    state.mark_step_completed("skip_report")
    state.status = "completed"
    return state
