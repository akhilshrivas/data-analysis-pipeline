"""Tools for loading data from various sources."""

from typing import Any, Dict, Union, Optional
from pathlib import Path
import pandas as pd

from logger import setup_logger

logger = setup_logger(__name__)


class DataLoaderTool:
    """Load data from CSV, JSON, Excel, SQL, APIs."""
    
    @staticmethod
    def load_csv(file_path: Union[str, Path]) -> pd.DataFrame:
        """Load CSV file."""
        logger.info(f"Loading CSV: {file_path}")
        return pd.read_csv(file_path)
    
    @staticmethod
    def load_json(file_path: Union[str, Path]) -> pd.DataFrame:
        """Load JSON file (array of objects or newline-delimited)."""
        logger.info(f"Loading JSON: {file_path}")
        try:
            # Try standard JSON (array)
            return pd.read_json(file_path)
        except:
            # Try newline-delimited JSON
            return pd.read_json(file_path, lines=True)
    
    @staticmethod
    def load_excel(file_path: Union[str, Path], sheet_name: Optional[str] = 0) -> pd.DataFrame:
        """Load Excel file."""
        logger.info(f"Loading XLSX: {file_path}")
        return pd.read_excel(file_path, sheet_name=sheet_name)
    
    @staticmethod
    def load_file(file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Auto-detect file type and load.
        
        Supports: CSV, JSON, XLSX, XLS
        """
        file_path = Path(file_path)
        ext = file_path.suffix.lower()
        
        if ext == '.csv':
            return DataLoaderTool.load_csv(file_path)
        elif ext == '.json':
            return DataLoaderTool.load_json(file_path)
        elif ext in ['.xlsx', '.xls']:
            return DataLoaderTool.load_excel(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    @staticmethod
    def load_sql(connection_string: str, query: str) -> pd.DataFrame:
        """Load from SQL database."""
        # TODO: Implement in Phase 2 (requires SQLAlchemy)
        pass
    
    @staticmethod
    def load_api(url: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Load from API endpoint."""
        # TODO: Implement in Phase 2
        pass

