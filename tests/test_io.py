from pathlib import Path

import pytest

from cypchemspace.io import load_substrate_table


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "example_data" / "cyp_substrates_demo.csv"


def test_load_substrate_table_has_required_columns():
    table = load_substrate_table(EXAMPLE)

    assert {"compound_id", "std_smiles", "label"}.issubset(table.columns)
    assert len(table) == 12
    assert set(table["label"]) == {"mydb", "p450db"}


def test_load_substrate_table_rejects_missing_required_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("compound_id,label\nlimonene,mydb\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required columns"):
        load_substrate_table(bad_csv)
