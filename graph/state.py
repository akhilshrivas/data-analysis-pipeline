"""Define the state for the analysis workflow."""

from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class AnalysisState:
    """State object passed through the LangGraph workflow."""
    
    # Input
    file_path: str = ""
    file_name: str = ""
    analysis_type: str = "Quick Profile"
    include_anomalies: bool = True
    include_insights: bool = True
    include_visualizations: bool = True
    include_report: bool = True
    
    # Data
    raw_data: Optional[Any] = None
    
    # Workflow Results
    profile: Dict[str, Any] = field(default_factory=dict)
    anomalies: Dict[str, Any] = field(default_factory=dict)
    insights: Dict[str, Any] = field(default_factory=dict)
    visualizations: Dict[str, str] = field(default_factory=dict)
    report: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    status: str = "pending"
    error: Optional[str] = None
    messages: list = field(default_factory=list)
    completed_steps: list = field(default_factory=list)
    
    def add_message(self, message: str):
        """Add a message to the workflow log."""
        self.messages.append(message)

    def mark_step_completed(self, step: str):
        """Track completed steps for UI display."""
        self.completed_steps.append(step)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "file_path": self.file_path,
            "file_name": self.file_name,
            "analysis_type": self.analysis_type,
            "include_anomalies": self.include_anomalies,
            "include_insights": self.include_insights,
            "include_visualizations": self.include_visualizations,
            "include_report": self.include_report,
            "profile": self.profile,
            "anomalies": self.anomalies,
            "insights": self.insights,
            "visualizations": self.visualizations,
            "report": self.report,
            "status": self.status,
            "error": self.error,
            "messages": self.messages,
            "completed_steps": self.completed_steps,
        }
