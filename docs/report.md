# Course Project Report: CYP Substrate Chemical Space Comparison

## 1. Background and Biological Question

Cytochrome P450 enzymes metabolize diverse small molecules. The original `CYP_comparison` project asked whether membrane-related CYP substrates collected in a local database occupy locally enriched regions within a broader P450DB substrate chemical space. This course package extracts a compact, reproducible version of that question.

## 2. Data Source and Preprocessing

The demo dataset is a small teaching subset derived from existing project outputs. Each row contains a compound identifier, standardized SMILES string, label, and source membership. Large raw `mydb` and P450DB tables are excluded from the course submission to keep the package portable.

## 3. Package Design and Software Architecture

The package uses a `src-layout` structure. `io.py` validates input tables, `chem.py` wraps RDKit SMILES parsing and Morgan fingerprints, `embedding.py` creates two-dimensional embeddings, `enrichment.py` runs kNN permutation statistics, `visualize.py` writes the core figure, and `cli.py` exposes the workflow as a command-line tool.

## 4. Algorithm or Model

The molecular representation is a Morgan fingerprint. Chemical-space visualization uses UMAP when available, with PCA fallback for constrained teaching environments. The statistical test computes the average fraction of positive-label neighbors around positive-label compounds and estimates an empirical p-value by randomly permuting labels.

## 5. Experiments and Results

The demo workflow writes `embedding.csv`, `summary.csv`, and `cypchemspace_umap.png`. In the full research project, the same conceptual workflow supported the conclusion that local enrichment persists across multiple RDKit fingerprints and after unique-InChIKey sensitivity analysis, although effect sizes decrease after structure-level deduplication.

## 6. Visualization and Interpretation

The scatter plot helps show how `mydb` and P450DB compounds are arranged in a two-dimensional embedding. The figure should be interpreted with the kNN permutation table, because UMAP alone is not a statistical test.

## 7. Testing and Reproducibility

The package includes pytest coverage for input validation, SMILES parsing, canonicalization, fingerprint shape, kNN enrichment, and CLI output generation. Reproducibility files include `requirements.txt`, `environment.yml`, and a demo notebook.

## 8. Limitations

The demo dataset is intentionally small. It cannot replace the full research analysis. The package does not perform online PubChem mapping, LLM rescue, protein localization curation, or all eight-fingerprint sensitivity runs. logP and membrane localization should be treated as interpretation aids rather than direct proof.

## 9. Future Work

Future versions could add all eight RDKit fingerprint methods, unique-InChIKey collapse, logP analysis, red-box cluster protein summaries, and a Snakemake workflow for full-scale reproduction.

## 10. References

- BIO2502 Python/R course project guide.
- RDKit documentation for Morgan fingerprints and molecular descriptors.
- UMAP and k-nearest-neighbor methods for exploratory chemical-space analysis.
