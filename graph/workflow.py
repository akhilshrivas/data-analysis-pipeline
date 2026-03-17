"""Build and execute the analysis workflow graph."""

from typing import Any, Dict

from langgraph.graph import StateGraph
from graph.state import AnalysisState
from graph.nodes import (
    load_data_node,
    profile_data_node,
    detect_anomalies_node,
    generate_insights_node,
    create_visualizations_node,
    generate_report_node,
    skip_anomalies_node,
    skip_insights_node,
    skip_visualizations_node,
    skip_report_node,
)
from logger import setup_logger

logger = setup_logger(__name__)


def build_analysis_graph():
    """
    Build the LangGraph workflow.
    
    Flow: Load → Profile → Anomalies → Insights → Visualizations → Report
    """
    workflow = StateGraph(AnalysisState)
    
    # Add nodes
    workflow.add_node("load_data", load_data_node)
    workflow.add_node("profile_data", profile_data_node)
    workflow.add_node("detect_anomalies", detect_anomalies_node)
    workflow.add_node("generate_insights", generate_insights_node)
    workflow.add_node("create_visualizations", create_visualizations_node)
    workflow.add_node("generate_report", generate_report_node)
    workflow.add_node("skip_anomalies", skip_anomalies_node)
    workflow.add_node("skip_insights", skip_insights_node)
    workflow.add_node("skip_visualizations", skip_visualizations_node)
    workflow.add_node("skip_report", skip_report_node)
    
    # Add edges (sequential workflow)
    workflow.add_edge("load_data", "profile_data")
    workflow.add_conditional_edges(
        "profile_data",
        route_after_profile,
        {
            "detect_anomalies": "detect_anomalies",
            "generate_insights": "generate_insights",
            "create_visualizations": "create_visualizations",
            "generate_report": "generate_report",
            "skip_anomalies": "skip_anomalies",
            "skip_insights": "skip_insights",
            "skip_visualizations": "skip_visualizations",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "detect_anomalies",
        route_after_anomalies,
        {
            "generate_insights": "generate_insights",
            "create_visualizations": "create_visualizations",
            "generate_report": "generate_report",
            "skip_insights": "skip_insights",
            "skip_visualizations": "skip_visualizations",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "skip_anomalies",
        route_after_anomalies,
        {
            "generate_insights": "generate_insights",
            "create_visualizations": "create_visualizations",
            "generate_report": "generate_report",
            "skip_insights": "skip_insights",
            "skip_visualizations": "skip_visualizations",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "generate_insights",
        route_after_insights,
        {
            "create_visualizations": "create_visualizations",
            "generate_report": "generate_report",
            "skip_visualizations": "skip_visualizations",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "skip_insights",
        route_after_insights,
        {
            "create_visualizations": "create_visualizations",
            "generate_report": "generate_report",
            "skip_visualizations": "skip_visualizations",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "create_visualizations",
        route_after_visualizations,
        {
            "generate_report": "generate_report",
            "skip_report": "skip_report",
        },
    )
    workflow.add_conditional_edges(
        "skip_visualizations",
        route_after_visualizations,
        {
            "generate_report": "generate_report",
            "skip_report": "skip_report",
        },
    )
    
    # Set entry point
    workflow.set_entry_point("load_data")
    
    # Set finish point
    workflow.set_finish_point("generate_report")
    workflow.set_finish_point("skip_report")
    
    return workflow.compile()


def route_after_profile(state: AnalysisState) -> str:
    """Choose the next node after profiling."""
    if state.include_anomalies:
        return "detect_anomalies"
    return "skip_anomalies"


def route_after_anomalies(state: AnalysisState) -> str:
    """Choose the next node after anomaly handling."""
    if state.include_insights:
        return "generate_insights"
    return "skip_insights"


def route_after_insights(state: AnalysisState) -> str:
    """Choose the next node after insight generation."""
    if state.include_visualizations:
        return "create_visualizations"
    return "skip_visualizations"


def route_after_visualizations(state: AnalysisState) -> str:
    """Choose the next node after visualization generation."""
    if state.include_report:
        return "generate_report"
    return "skip_report"


async def run_analysis(
    file_path: str,
    file_name: str,
    options: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Execute the analysis workflow.
    
    Args:
        file_path: Path to the data file
        file_name: Original filename
    
    Returns:
        Analysis results
    """
    logger.info(f"Starting analysis workflow for {file_name}")
    
    # Create initial state
    state = AnalysisState(
        file_path=file_path,
        file_name=file_name,
        status="running",
        analysis_type=(options or {}).get("analysis_type", "Quick Profile"),
        include_anomalies=(options or {}).get("include_anomalies", True),
        include_insights=(options or {}).get("include_insights", True),
        include_visualizations=(options or {}).get("include_visualizations", True),
        include_report=(options or {}).get("include_report", True),
    )
    
    # Build and execute graph
    graph = build_analysis_graph()
    
    try:
        # Run the graph
        result = await graph.ainvoke(state.to_dict())
        result["status"] = "completed"
        logger.info(f"Analysis completed successfully")
        return result
    
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "messages": state.messages,
        }


# Synchronous wrapper for FastAPI
def run_analysis_sync(
    file_path: str,
    file_name: str,
    options: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Synchronous wrapper for analysis."""
    import asyncio
    return asyncio.run(run_analysis(file_path, file_name, options=options))
