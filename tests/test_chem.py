from pathlib import Path

from cypchemspace.chem import canonicalize_smiles, make_morgan_fingerprint_matrix, mol_from_smiles
from cypchemspace.io import load_substrate_table


EXAMPLE = Path(__file__).resolve().parents[1] / "examples" / "example_data" / "cyp_substrates_demo.csv"


def test_mol_from_smiles_returns_none_for_invalid_smiles():
    assert mol_from_smiles("not-a-smiles") is None


def test_canonicalize_smiles_normalizes_equivalent_smiles():
    assert canonicalize_smiles("CC(C)=C") == canonicalize_smiles("C=C(C)C")


def test_morgan_fingerprint_matrix_shape_matches_input_rows():
    table = load_substrate_table(EXAMPLE)

    matrix, valid_table = make_morgan_fingerprint_matrix(table, n_bits=128)

    assert matrix.shape == (12, 128)
    assert len(valid_table) == 12
