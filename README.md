# cypchemspace

`cypchemspace` is a BIO2502 course-project package for comparing membrane-related CYP substrate chemical space against a P450DB background. It turns a larger exploratory CYP comparison repository into a compact, installable, and testable Python package.

## Biological Question

Do membrane-related CYP substrates from the local database (`mydb`) show local enrichment in the broader P450DB substrate chemical space?

The package demonstrates one reproducible analysis path:

1. Load a small compound table with standardized SMILES and source labels.
2. Convert SMILES to RDKit molecules.
3. Compute Morgan molecular fingerprints.
4. Embed the fingerprint space in two dimensions for visualization.
5. Run a k-nearest-neighbor permutation test for local label enrichment.
6. Write a summary table and a core figure.

## Install

Recommended:

```bash
conda env create -f environment.yml
conda activate cypchemspace
pip install -e .
```

Alternative, if RDKit is already available:

```bash
pip install -e .
```

On this Windows Python 3.14 workstation, `pip` and `pandas` may hang while probing platform details through WMI. If that happens, run installation with the bundled startup patch:

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
python -m pip install -e . --no-deps --no-build-isolation
```

## Quick Start

```bash
cypchemspace analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-permutations 99
```

Equivalent module invocation:

```bash
python -m cypchemspace.cli analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-permutations 99
```

Expected outputs:

- `results/demo_run/embedding.csv`
- `results/demo_run/summary.csv`
- `results/demo_run/cypchemspace_umap.png`

## Course Deliverables

- Final report: `docs/final_report.md`
- Proposal: `docs/proposal.md`
- Tutorial: `docs/tutorial.md`
- Slides outline: `docs/slides_outline.md`
- Demo notebook: `examples/demo_cypchemspace.ipynb`
- Video recording guide: `docs/video_recording_guide.md`

## Reusable API

```python
from cypchemspace import load_substrate_table, make_morgan_fingerprint_matrix, knn_label_enrichment

table = load_substrate_table("examples/example_data/cyp_substrates_demo.csv")
fingerprints, valid_table = make_morgan_fingerprint_matrix(table)
stats = knn_label_enrichment(fingerprints, valid_table["label"], positive_label="mydb")
```

## Data Source

The demo CSV is a small teaching subset derived from the larger `CYP_comparison` project outputs. It intentionally excludes the large raw `mydb` and P450DB tables so that the course package is small, portable, and safe to submit. The full research repository contains the broader mapping, rescue, sensitivity, logP, and red-box cluster analyses.

## Result Interpretation

The kNN permutation test asks whether `mydb` compounds have more `mydb` neighbors than expected after random label shuffling. A positive `delta` and a low empirical p-value support local enrichment, but the result should be reported as a fingerprint-neighborhood signal, not proof of absolute class separation.

## Limitations

- The bundled dataset is a teaching subset, not the full analysis set.
- The CLI does not perform remote PubChem lookup.
- UMAP is a visualization method; interpretation should be paired with the kNN permutation statistic.
- Membrane localization is a biological interpretation step and is not directly proven by logP or UMAP alone.

## Tests

```bash
python -m pytest
```

If pytest hangs on the same Windows platform probe, use:

```powershell
$env:PYTHONPATH = "tools\python_startup_patch"
python -m pytest
```

The test suite covers input validation, SMILES parsing, fingerprint matrix shape, kNN enrichment behavior, and CLI output generation.
