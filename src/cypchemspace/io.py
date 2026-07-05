"""Input and output helpers for CYP chemical-space tables."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from cypchemspace._compat import avoid_windows_wmi_platform_probe

avoid_windows_wmi_platform_probe()
import pandas as pd


DEFAULT_REQUIRED_COLUMNS = ("compound_id", "std_smiles", "label")


def load_substrate_table(path: str | Path, required_columns: Iterable[str] = DEFAULT_REQUIRED_COLUMNS) -> pd.DataFrame:
    """Load a substrate table and validate the columns used by the package.

    Parameters
    ----------
    path:
        CSV or TSV file containing one row per compound.
    required_columns:
        Columns that must be present for downstream analysis.
    """

    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input table does not exist: {file_path}")

    sep = "\t" if file_path.suffix.lower() in {".tsv", ".tab"} else ","
    table = pd.read_csv(file_path, sep=sep)
    missing = [column for column in required_columns if column not in table.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    cleaned = table.copy()
    cleaned["compound_id"] = cleaned["compound_id"].astype(str).str.strip()
    cleaned["std_smiles"] = cleaned["std_smiles"].astype(str).str.strip()
    cleaned["label"] = cleaned["label"].astype(str).str.strip().str.lower()
    cleaned = cleaned[(cleaned["compound_id"] != "") & (cleaned["std_smiles"] != "") & (cleaned["label"] != "")]
    if cleaned.empty:
        raise ValueError("No usable substrate rows remained after basic cleaning.")
    return cleaned.reset_index(drop=True)


def write_summary_csv(summary: dict[str, object], path: str | Path) -> None:
    """Write a one-row summary dictionary as CSV."""

    pd.DataFrame([summary]).to_csv(path, index=False)
