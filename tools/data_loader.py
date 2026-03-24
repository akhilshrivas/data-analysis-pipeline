"""Tools for loading data from various sources."""

from io import BytesIO, StringIO
from pathlib import Path
import re
from typing import Any, Dict, Optional, Union

import pandas as pd

from logger import setup_logger

logger = setup_logger(__name__)


class DataLoaderTool:
    """Load data from CSV, JSON, Excel, SQL, APIs."""

    @staticmethod
    def _finalize_dataframe(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
        """Normalize parsed dataframes and reject unusable results."""
        if df.empty:
            raise ValueError(f"{source_name} did not contain any tabular rows to analyze.")

        cleaned = df.dropna(axis=0, how="all").dropna(axis=1, how="all")
        if cleaned.empty:
            raise ValueError(f"{source_name} did not contain any usable rows or columns.")

        cleaned.columns = [
            str(column).strip() or f"column_{index + 1}"
            for index, column in enumerate(cleaned.columns)
        ]
        return cleaned.reset_index(drop=True)

    @staticmethod
    def _parse_text_content(text: str, source_name: str) -> pd.DataFrame:
        """Parse tabular text using a small set of common delimiters."""
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n").strip("\ufeff \n\t")
        if not normalized_text:
            raise ValueError(f"{source_name} is empty.")

        non_empty_lines = [line for line in normalized_text.splitlines() if line.strip()]
        if len(non_empty_lines) < 2:
            raise ValueError(
                f"{source_name} needs at least a header row and one data row for analysis."
            )

        parser_attempts: list[tuple[str, dict[str, Any]]] = [
            ("\t", {"sep": "\t"}),
            (",", {"sep": ","}),
            ("|", {"sep": "|"}),
            (";", {"sep": ";"}),
        ]

        best_candidate: pd.DataFrame | None = None
        best_score = 0

        for delimiter, read_kwargs in parser_attempts:
            if sum(line.count(delimiter) for line in non_empty_lines[:10]) == 0:
                continue
            try:
                candidate = pd.read_csv(StringIO(normalized_text), engine="python", **read_kwargs)
                candidate = DataLoaderTool._finalize_dataframe(candidate, source_name)
                score = candidate.shape[1]
                if score > best_score:
                    best_candidate = candidate
                    best_score = score
                if score > 1:
                    return candidate
            except Exception:
                continue

        spaced_lines = [line for line in non_empty_lines if re.search(r"\S\s{2,}\S", line)]
        if len(spaced_lines) >= 2:
            try:
                candidate = pd.read_fwf(StringIO("\n".join(spaced_lines)))
                candidate = DataLoaderTool._finalize_dataframe(candidate, source_name)
                if candidate.shape[1] > 1:
                    return candidate
                if candidate.shape[1] > best_score:
                    best_candidate = candidate
                    best_score = candidate.shape[1]
            except Exception:
                pass

        if best_candidate is not None:
            return best_candidate

        raise ValueError(
            f"{source_name} could not be parsed as a table. Supported text layouts are tab-, comma-, pipe-, semicolon-, or fixed-width columns."
        )

    @staticmethod
    def load_csv(file_path: Union[str, Path]) -> pd.DataFrame:
        """Load CSV file."""
        logger.info(f"Loading CSV: {file_path}")
        return DataLoaderTool._finalize_dataframe(pd.read_csv(file_path), str(file_path))

    @staticmethod
    def load_json(file_path: Union[str, Path]) -> pd.DataFrame:
        """Load JSON file (array of objects or newline-delimited)."""
        logger.info(f"Loading JSON: {file_path}")
        try:
            return DataLoaderTool._finalize_dataframe(pd.read_json(file_path), str(file_path))
        except Exception:
            return DataLoaderTool._finalize_dataframe(
                pd.read_json(file_path, lines=True),
                str(file_path),
            )

    @staticmethod
    def load_text(file_path: Union[str, Path]) -> pd.DataFrame:
        """Load plain-text tabular data."""
        logger.info(f"Loading TXT: {file_path}")
        text = Path(file_path).read_text(encoding="utf-8", errors="replace")
        return DataLoaderTool._parse_text_content(text, str(file_path))

    @staticmethod
    def load_excel(file_path: Union[str, Path], sheet_name: Optional[str] = 0) -> pd.DataFrame:
        """Load Excel file."""
        logger.info(f"Loading XLSX: {file_path}")
        return DataLoaderTool._finalize_dataframe(
            pd.read_excel(file_path, sheet_name=sheet_name),
            str(file_path),
        )

    @staticmethod
    def load_uploaded_file(uploaded_file) -> pd.DataFrame:
        """Load a Streamlit-uploaded file into a dataframe."""
        file_name = uploaded_file.name.lower()
        file_bytes = uploaded_file.getvalue()

        if file_name.endswith(".csv"):
            return DataLoaderTool._finalize_dataframe(
                pd.read_csv(BytesIO(file_bytes)),
                uploaded_file.name,
            )
        if file_name.endswith(".json"):
            try:
                return DataLoaderTool._finalize_dataframe(
                    pd.read_json(BytesIO(file_bytes)),
                    uploaded_file.name,
                )
            except ValueError:
                return DataLoaderTool._finalize_dataframe(
                    pd.read_json(BytesIO(file_bytes), lines=True),
                    uploaded_file.name,
                )
        if file_name.endswith((".xlsx", ".xls")):
            return DataLoaderTool._finalize_dataframe(
                pd.read_excel(BytesIO(file_bytes)),
                uploaded_file.name,
            )
        if file_name.endswith(".txt"):
            text = file_bytes.decode("utf-8", errors="replace")
            return DataLoaderTool._parse_text_content(text, uploaded_file.name)

        raise ValueError(f"Unsupported preview format: {uploaded_file.name}")

    @staticmethod
    def load_file(file_path: Union[str, Path]) -> pd.DataFrame:
        """
        Auto-detect file type and load.

        Supports: CSV, JSON, XLSX, XLS, TXT
        """
        file_path = Path(file_path)
        ext = file_path.suffix.lower()

        if ext == ".csv":
            return DataLoaderTool.load_csv(file_path)
        if ext == ".json":
            return DataLoaderTool.load_json(file_path)
        if ext == ".txt":
            return DataLoaderTool.load_text(file_path)
        if ext in [".xlsx", ".xls"]:
            return DataLoaderTool.load_excel(file_path)
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
