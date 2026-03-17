"""Tools for statistical analysis and data profiling."""

from typing import Any, Dict, List
import pandas as pd
import numpy as np
from logger import setup_logger

logger = setup_logger(__name__)


class AnalyzerTool:
    """Statistical analysis and data profiling."""
    
    @staticmethod
    def profile_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive statistical profile of dataframe.
        
        Returns:
            - shape, dtypes, missing values, basic stats, unique values
        """
        logger.info(f"Profiling dataframe with shape {df.shape}")
        
        profile = {
            "shape": {"rows": df.shape[0], "columns": df.shape[1]},
            "columns": list(df.columns),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicate_rows": int(df.duplicated().sum()),
        }
        
        # Add numeric statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        numeric_stats = {}
        
        for col in numeric_cols:
            numeric_stats[col] = {
                "mean": float(df[col].mean()) if df[col].notna().any() else None,
                "median": float(df[col].median()) if df[col].notna().any() else None,
                "std": float(df[col].std()) if df[col].notna().any() else None,
                "min": float(df[col].min()) if df[col].notna().any() else None,
                "max": float(df[col].max()) if df[col].notna().any() else None,
                "q25": float(df[col].quantile(0.25)) if df[col].notna().any() else None,
                "q75": float(df[col].quantile(0.75)) if df[col].notna().any() else None,
            }
        
        profile["numeric_statistics"] = numeric_stats
        
        # Add categorical statistics
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        categorical_stats = {}
        
        for col in categorical_cols:
            unique_values = df[col].nunique()
            categorical_stats[col] = {
                "unique_count": int(unique_values),
                "top_values": df[col].value_counts().head(5).to_dict() if unique_values > 0 else {},
            }
        
        profile["categorical_statistics"] = categorical_stats
        
        return profile
    
    @staticmethod
    def detect_data_types(df: pd.DataFrame) -> Dict[str, List[str]]:
        """Classify columns by data type."""
        logger.info("Detecting data types")
        
        return {
            "numeric": list(df.select_dtypes(include=[np.number]).columns),
            "categorical": list(df.select_dtypes(include=['object', 'category']).columns),
            "datetime": list(df.select_dtypes(include=['datetime64']).columns),
            "boolean": list(df.select_dtypes(include=['bool']).columns),
        }
    
    @staticmethod
    def calculate_correlations(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Calculate correlations between numeric columns."""
        logger.info("Calculating correlations")
        
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.shape[1] < 2:
            return {}
        
        corr_matrix = numeric_df.corr()
        
        # Convert to nested dict
        return corr_matrix.to_dict()
    
    @staticmethod
    def generate_insights_from_profile(profile: Dict[str, Any]) -> List[str]:
        """Generate human-readable insights from profile."""
        insights = []
        
        # Row/column insights
        shape = profile.get("shape", {})
        if shape:
            insights.append(f"Dataset contains {shape['rows']:,} rows and {shape['columns']} columns")
        
        # Missing values insights
        missing_vals = profile.get("missing_percentage", {})
        high_missing = {col: pct for col, pct in missing_vals.items() if pct > 50}
        if high_missing:
            cols = ", ".join(high_missing.keys())
            insights.append(f"High missing values (>50%) in: {cols}")
        
        # Duplicate insights
        duplicates = profile.get("duplicate_rows", 0)
        if duplicates > 0:
            insights.append(f"Found {duplicates:,} duplicate rows")
        
        # Numeric statistics insights
        numeric_stats = profile.get("numeric_statistics", {})
        for col, stats in numeric_stats.items():
            if stats.get("std") is not None and stats["std"] > 0:
                cv = (stats["std"] / abs(stats["mean"])) if stats["mean"] != 0 else float('inf')
                if cv > 1:
                    insights.append(f"Column '{col}' has high variability (CV={cv:.2f})")
        
        return insights
    
    @staticmethod
    def detect_outliers(df: pd.DataFrame, method: str = "iqr") -> Dict[str, Any]:
        """
        Detect outliers in numeric columns.
        
        Methods: 'iqr', 'zscore'
        """
        logger.info(f"Detecting outliers using {method}")
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {
                "method": method,
                "columns": {},
                "total_anomalies": 0,
                "anomaly_rows": [],
            }

        method = method.lower()
        if method not in {"iqr", "zscore"}:
            raise ValueError(f"Unsupported outlier detection method: {method}")

        anomaly_mask = pd.Series(False, index=df.index)
        column_results: Dict[str, Any] = {}

        for column in numeric_df.columns:
            series = numeric_df[column].dropna()
            if len(series) < 3:
                continue

            if method == "iqr":
                col_mask = AnalyzerTool._iqr_outlier_mask(numeric_df[column])
            else:
                col_mask = AnalyzerTool._zscore_outlier_mask(numeric_df[column])

            outlier_indices = numeric_df.index[col_mask.fillna(False)].tolist()
            anomaly_mask = anomaly_mask | col_mask.fillna(False)

            if outlier_indices:
                column_results[column] = {
                    "count": len(outlier_indices),
                    "percentage": round(len(outlier_indices) / len(df) * 100, 2),
                    "row_indices": outlier_indices[:25],
                }

        anomaly_rows = anomaly_mask[anomaly_mask].index.tolist()
        return {
            "method": method,
            "columns": column_results,
            "total_anomalies": len(anomaly_rows),
            "anomaly_rows": anomaly_rows[:100],
        }

    @staticmethod
    def _iqr_outlier_mask(series: pd.Series) -> pd.Series:
        """Return a boolean mask for IQR-based outliers."""
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if pd.isna(iqr) or iqr == 0:
            return pd.Series(False, index=series.index)

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return (series < lower_bound) | (series > upper_bound)

    @staticmethod
    def _zscore_outlier_mask(series: pd.Series, threshold: float = 3.0) -> pd.Series:
        """Return a boolean mask for z-score-based outliers."""
        mean = series.mean()
        std = series.std()
        if pd.isna(std) or std == 0:
            return pd.Series(False, index=series.index)

        zscores = (series - mean) / std
        return zscores.abs() > threshold

