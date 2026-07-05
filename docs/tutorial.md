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

table = load_substrate_table("examples/example_data/clean_rescued_substrates_2548.csv")
table.groupby("label").size()
```

The table contains two labels:

- `mydb`: membrane-related CYP substrates from the local project context.
- `p450db`: background CYP substrates from P450DB.

## 3. Run the CLI

```bash
cypchemspace analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

Open:

- `results/demo_clean_2548_128bit_pca_perm19/summary.csv`
- `results/demo_clean_2548_128bit_pca_perm19/cypchemspace_umap.png`

The output can be compared with `results/full_clean_reference/`, which stores
the full/reference project result produced with 5,000 permutations.

## 4. Use the Python API

```python
from cypchemspace import load_substrate_table, make_morgan_fingerprint_matrix, knn_label_enrichment
from cypchemspace.embedding import compute_embedding

table = load_substrate_table("examples/example_data/clean_rescued_substrates_2548.csv")
fingerprints, valid_table = make_morgan_fingerprint_matrix(table, n_bits=128)
embedding = compute_embedding(fingerprints, method="pca")
stats = knn_label_enrichment(fingerprints, valid_table["label"], positive_label="mydb", k=15, n_permutations=19)
stats
```

## 5. Interpretation

The core statistic is the local fraction of `mydb` neighbors around `mydb` compounds. The permutation test compares that observed fraction against random label shuffles. This supports a statement about local chemical-neighborhood enrichment, not a claim that the two databases form perfectly separated chemical classes.
