# 10-Minute Presentation Outline

## Slide 1: Title

`cypchemspace`: CYP substrate chemical-space comparison as a Python package.

## Slide 2: Biological Question

Do membrane-related CYP substrates from `mydb` show local enrichment in P450DB chemical space?

## Slide 3: Why This Fits the Course Project

Python package, reusable APIs, CLI, tests, notebook, real biological data context, statistical interpretation.

## Slide 4: Data Boundary

Cleaned 2,548-row substrate table is included for the live demo; raw database exports and online-query caches are excluded.

## Slide 5: Package Architecture

Show modules: `io`, `chem`, `embedding`, `enrichment`, `visualize`, `cli`.

## Slide 6: Method

SMILES -> RDKit Mol -> Morgan fingerprint -> UMAP/PCA embedding -> kNN permutation enrichment.

## Slide 7: Live Demo

```bash
cypchemspace analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

## Slide 8: Results

Show the live demo `summary.csv` and `cypchemspace_umap.png`. Explain the PCA plot layers: gray `P450DB` bottom, blue `mydb` middle, orange shared compounds top. Then compare with `results/full_clean_reference/`.

## Slide 9: Interpretation and Limitations

Local enrichment is supported statistically; PCA/UMAP plots are visual summaries; 19 permutations are for recording speed, while the reference result uses 5,000 permutations.

## Slide 10: Future Work

Eight-fingerprint sensitivity, unique-InChIKey collapse, logP module, protein localization curation, workflow automation.
