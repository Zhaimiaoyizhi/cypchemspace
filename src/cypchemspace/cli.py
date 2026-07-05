"""Command-line interface for the cypchemspace course package."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze CYP substrate chemical-space enrichment.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Run fingerprint, embedding, kNN enrichment, and plotting.")
    analyze.add_argument("input_table", help="CSV/TSV table with compound_id, std_smiles, and label columns.")
    analyze.add_argument("--out-dir", default="results/demo_run", help="Directory for output files.")
    analyze.add_argument("--positive-label", default="mydb", help="Label treated as the positive class.")
    analyze.add_argument("--n-bits", type=int, default=2048, help="Morgan fingerprint bit length.")
    analyze.add_argument("--radius", type=int, default=2, help="Morgan fingerprint radius.")
    analyze.add_argument("--k", type=int, default=15, help="Number of nearest neighbors for enrichment.")
    analyze.add_argument("--n-permutations", type=int, default=999, help="Number of label permutations.")
    analyze.add_argument("--random-state", type=int, default=42, help="Random seed.")
    analyze.add_argument("--embedding-method", choices=["umap", "pca"], default="umap", help="2D embedding method.")
    analyze.set_defaults(func=run_analyze)
    return parser


def run_analyze(args: argparse.Namespace) -> int:
    from cypchemspace._compat import avoid_windows_wmi_platform_probe

    avoid_windows_wmi_platform_probe()
    import pandas as pd

    from cypchemspace.chem import make_morgan_fingerprint_matrix
    from cypchemspace.embedding import compute_embedding
    from cypchemspace.enrichment import knn_label_enrichment
    from cypchemspace.io import load_substrate_table, write_summary_csv
    from cypchemspace.visualize import plot_embedding

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    table = load_substrate_table(args.input_table)
    fingerprints, valid_table = make_morgan_fingerprint_matrix(
        table,
        radius=args.radius,
        n_bits=args.n_bits,
    )
    embedding = compute_embedding(
        fingerprints,
        method=args.embedding_method,
        random_state=args.random_state,
    )
    embedded_table = pd.concat([valid_table.reset_index(drop=True), embedding], axis=1)

    summary = knn_label_enrichment(
        fingerprints,
        embedded_table["label"].to_numpy(),
        positive_label=args.positive_label,
        k=args.k,
        n_permutations=args.n_permutations,
        random_state=args.random_state,
    )
    summary.update(
        {
            "input_table": str(Path(args.input_table)),
            "n_valid_molecules": int(len(embedded_table)),
            "fingerprint": f"Morgan radius={args.radius}, n_bits={args.n_bits}",
        }
    )

    embedded_table.to_csv(out_dir / "embedding.csv", index=False)
    write_summary_csv(summary, out_dir / "summary.csv")
    if args.embedding_method == "pca":
        x_label, y_label = "PCA 1", "PCA 2"
    else:
        x_label, y_label = "UMAP 1", "UMAP 2"
    plot_embedding(embedded_table, out_dir / "cypchemspace_umap.png", x_label=x_label, y_label=y_label)

    print(f"Wrote {out_dir / 'embedding.csv'}")
    print(f"Wrote {out_dir / 'summary.csv'}")
    print(f"Wrote {out_dir / 'cypchemspace_umap.png'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
