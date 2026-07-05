"""CYP substrate chemical-space comparison utilities.

The public functions are loaded lazily so that lightweight commands such as
``python -m cypchemspace.cli --help`` do not pay the RDKit import cost.
"""

from importlib import import_module

__all__ = [
    "canonicalize_smiles",
    "knn_label_enrichment",
    "load_substrate_table",
    "make_morgan_fingerprint_matrix",
    "mol_from_smiles",
]


def __getattr__(name: str):
    if name in {"chem", "cli", "embedding", "enrichment", "io", "visualize"}:
        return import_module(f"cypchemspace.{name}")
    if name in {"canonicalize_smiles", "make_morgan_fingerprint_matrix", "mol_from_smiles"}:
        chem = import_module("cypchemspace.chem")
        return getattr(chem, name)
    if name == "knn_label_enrichment":
        enrichment = import_module("cypchemspace.enrichment")
        return enrichment.knn_label_enrichment
    if name == "load_substrate_table":
        io = import_module("cypchemspace.io")
        return io.load_substrate_table
    raise AttributeError(f"module 'cypchemspace' has no attribute {name!r}")
