from pathlib import Path

import pytest

from tools.data_loader import DataLoaderTool


def test_load_text_parses_tabular_txt(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("name\tage\tcity\nAsha\t29\tPune\nRavi\t35\tDelhi\n", encoding="utf-8")

    df = DataLoaderTool.load_text(file_path)

    assert list(df.columns) == ["name", "age", "city"]
    assert df.shape == (2, 3)
    assert df.iloc[0]["name"] == "Asha"


def test_load_text_rejects_non_tabular_txt(tmp_path: Path):
    file_path = tmp_path / "notes.txt"
    file_path.write_text("just a sentence\nanother sentence\n", encoding="utf-8")

    with pytest.raises(ValueError, match="could not be parsed as a table"):
        DataLoaderTool.load_text(file_path)
