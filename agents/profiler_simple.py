"""Data profiler agent - simplified version for Phase 2."""

from typing import Any, Dict
import pandas as pd
from pathlib import Path

from tools.data_loader import DataLoaderTool
from tools.analyzer import AnalyzerTool
from logger import setup_logger

logger = setup_logger(__name__)


class DataProfilerAgent:
    """
    Simple data profiler agent.
    
    Demonstrates:
    - Loading data from various formats
    - Computing statistical profiles
    - Type detection
    - Correlation analysis
    - Insight generation
    """
    
    def __init__(self):
        """Initialize the profiler agent."""
        self.name = "DataProfiler"
        self.data = None
        logger.info(f"Initialized {self.name}")
    
    def run(self, file_path: str) -> Dict[str, Any]:
        """
        Run the profiler on a data file.
        
        Args:
            file_path: Path to data file (CSV, JSON, XLSX)
        
        Returns:
            Profile information and insights
        """
        logger.info(f"Starting data profile for {file_path}")
        
        try:
            # Step 1: Load data
            logger.info("Step 1: Loading data...")
            self.data = DataLoaderTool.load_file(file_path)
            load_msg = f"✓ Loaded {self.data.shape[0]:,} rows × {self.data.shape[1]} columns"
            
            # Step 2: Profile data
            logger.info("Step 2: Profiling data...")
            profile = AnalyzerTool.profile_dataframe(self.data)
            
            # Step 3: Detect data types
            logger.info("Step 3: Detecting data types...")
            data_types = AnalyzerTool.detect_data_types(self.data)
            
            # Step 4: Calculate correlations
            logger.info("Step 4: Calculating correlations...")
            correlations = AnalyzerTool.calculate_correlations(self.data)
            
            # Step 5: Generate insights
            logger.info("Step 5: Generating insights...")
            insights = AnalyzerTool.generate_insights_from_profile(profile)
            
            # Compile summary
            summary = self._compile_summary(profile, data_types, correlations, insights)
            
            return {
                "status": "success",
                "file_path": file_path,
                "profile": profile,
                "data_types": data_types,
                "correlations": correlations,
                "insights": insights,
                "summary": summary,
                "data_shape": self.data.shape,
            }
        
        except Exception as e:
            logger.error(f"Profile agent error: {str(e)}")
            return {
                "status": "failed",
                "error": str(e),
                "file_path": file_path,
            }
    
    def _compile_summary(self, profile: Dict, types: Dict, corr: Dict, insights: list) -> str:
        """Compile a human-readable summary."""
        summary = "📊 DATA PROFILE SUMMARY\n"
        summary += "=" * 60 + "\n\n"
        
        # Basic info
        shape = profile.get("shape", {})
        summary += f"Dataset Shape: {shape.get('rows', 'N/A'):,} rows × {shape.get('columns', 'N/A')} columns\n"
        summary += f"Columns: {', '.join(profile.get('columns', [])[:5])}"
        if len(profile.get('columns', [])) > 5:
            summary += f" ... and {len(profile['columns']) - 5} more\n\n"
        else:
            summary += "\n\n"
        
        # Data quality
        missing = profile.get("missing_percentage", {})
        high_missing_cols = [col for col, pct in missing.items() if pct > 0]
        summary += f"Data Quality:\n"
        summary += f"  - Columns with missing values: {len(high_missing_cols)}\n"
        summary += f"  - Duplicate rows: {profile.get('duplicate_rows', 0):,}\n"
        
        if high_missing_cols and len(high_missing_cols) <= 5:
            summary += f"  - Missing columns: {', '.join(high_missing_cols)}\n"
        summary += "\n"
        
        # Data types
        summary += f"Data Types:\n"
        summary += f"  - Numeric: {len(types.get('numeric', []))} columns\n"
        summary += f"  - Categorical: {len(types.get('categorical', []))} columns\n"
        summary += f"  - Datetime: {len(types.get('datetime', []))} columns\n"
        summary += f"  - Boolean: {len(types.get('boolean', []))} columns\n\n"
        
        # Correlations
        if corr:
            pairs = []
            for col1, corrs in corr.items():
                for col2, value in corrs.items():
                    if col1 < col2 and abs(value) > 0.5:
                        pairs.append((col1, col2, value))
            
            if pairs:
                summary += f"Strong Correlations (|r| > 0.5): {len(pairs)} found\n"
                for col1, col2, value in sorted(pairs, key=lambda x: abs(x[2]), reverse=True)[:3]:
                    summary += f"  - {col1} ↔ {col2}: {value:.3f}\n"
                summary += "\n"
        
        # Insights
        if insights:
            summary += f"Key Insights:\n"
            for i, insight in enumerate(insights[:5], 1):
                summary += f"  {i}. {insight}\n"
        
        return summary
