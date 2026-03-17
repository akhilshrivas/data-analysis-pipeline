"""Visualization agent for creating charts and plots."""

from typing import Any, Dict

from tools.visualizer import VisualizerTool
from logger import setup_logger

logger = setup_logger(__name__)


class VisualizationAgent:
    """Agent that creates visualizations from data."""
    
    def __init__(self):
        self.name = "Visualizer"
    
    def run(
        self,
        data_path: str,
        profile: Dict[str, Any],
        insights: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Create visualizations for data.
        
        Args:
            data_path: Path to data file
            profile: Data profile
            insights: Generated insights
        
        Returns:
            Paths to generated visualizations
        """
        logger.info(f"Starting visualization for {data_path}")
        try:
            recommendations = VisualizerTool.recommend_visualizations(profile, insights)
            return {
                "status": "success",
                "recommended_charts": recommendations,
                "dashboard_notes": "Use the recommended charts to build the next interactive dashboard step.",
            }
        except Exception as exc:
            logger.error(f"Visualization generation failed: {exc}")
            return {"status": "failed", "error": str(exc)}
