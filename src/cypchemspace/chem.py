"""RDKit-based molecular structure and fingerprint helpers."""

from __future__ import annotations

from typing import Iterable, TYPE_CHECKING

import numpy as np
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator

if TYPE_CHECKING:
    import pandas as pd


def mol_from_smiles(smiles: str):
    """Parse a SMILES string into an RDKit molecule, returning None on failure."""

    if not isinstance(smiles, str) or not smiles.strip():
        return None
    try:
        return Chem.MolFromSmiles(smiles)
    except Exception:
        return None


def canonicalize_smiles(smiles: str) -> str | None:
    """Return a canonical RDKit SMILES string, or None if parsing fails."""

    mol = mol_from_smiles(smiles)
    if mol is None:
        return None
    return Chem.MolToSmiles(mol, canonical=True)


def make_morgan_fingerprint_matrix(
    table: "pd.DataFrame",
    smiles_col: str = "std_smiles",
    radius: int = 2,
    n_bits: int = 2048,
) -> tuple[np.ndarray, "pd.DataFrame"]:
    """Generate a Morgan bit fingerprint matrix and return valid rows.

    Invalid SMILES rows are excluded from both the matrix and the returned metadata.
    """

    if smiles_col not in table.columns:
        raise ValueError(f"Missing SMILES column: {smiles_col}")

    generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
    vectors: list[np.ndarray] = []
    valid_indices: list[int] = []

    for index, smiles in table[smiles_col].items():
        mol = mol_from_smiles(smiles)
        if mol is None:
            continue
        fingerprint = generator.GetFingerprint(mol)
        array = np.zeros((n_bits,), dtype=np.uint8)
        Chem.DataStructs.ConvertToNumpyArray(fingerprint, array)
        vectors.append(array)
        valid_indices.append(index)

    if not vectors:
        raise ValueError("No valid molecules could be fingerprinted.")

    valid_table = table.loc[valid_indices].reset_index(drop=True)
    return np.vstack(vectors), valid_table


def canonicalize_many(smiles_values: Iterable[str]) -> list[str | None]:
    """Canonicalize a sequence of SMILES strings."""

    return [canonicalize_smiles(smiles) for smiles in smiles_values]
