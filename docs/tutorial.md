# cypchemspace Tutorial

## 1. Install

```bash
conda env create -f environment.yml
conda activate cypchemspace
pip install -e .
```

## 2. Inspect the Demo Data

```python
from cypchemspace import load_substrate_table

table = load_substrate_table("examples/example_data/cyp_substrates_demo.csv")
table.groupby("label").size()
```

The table contains two labels:

- `mydb`: membrane-related CYP substrates from the local project context.
- `p450db`: background CYP substrates from P450DB.

## 3. Run the CLI

```bash
cypchemspace analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-permutations 99
```

Open:

- `results/demo_run/summary.csv`
- `results/demo_run/cypchemspace_umap.png`

## 4. Use the Python API

```python
from cypchemspace import load_substrate_table, make_morgan_fingerprint_matrix, knn_label_enrichment
from cypchemspace.embedding import compute_embedding

table = load_substrate_table("examples/example_data/cyp_substrates_demo.csv")
fingerprints, valid_table = make_morgan_fingerprint_matrix(table)
embedding = compute_embedding(fingerprints, method="umap")
stats = knn_label_enrichment(fingerprints, valid_table["label"], positive_label="mydb", n_permutations=99)
stats
```

## 5. Interpretation

The core statistic is the local fraction of `mydb` neighbors around `mydb` compounds. The permutation test compares that observed fraction against random label shuffles. This supports a statement about local chemical-neighborhood enrichment, not a claim that the two databases form perfectly separated chemical classes.
