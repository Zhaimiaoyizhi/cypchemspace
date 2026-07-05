# 10-Minute Presentation Outline

## Slide 1: Title

`cypchemspace`: CYP substrate chemical-space comparison as a Python package.

## Slide 2: Biological Question

Do membrane-related CYP substrates from `mydb` show local enrichment in P450DB chemical space?

## Slide 3: Why This Fits the Course Project

Python package, reusable APIs, CLI, tests, notebook, real biological data context, statistical interpretation.

## Slide 4: Data Boundary

Small teaching subset in the course package; full raw database tables excluded.

## Slide 5: Package Architecture

Show modules: `io`, `chem`, `embedding`, `enrichment`, `visualize`, `cli`.

## Slide 6: Method

SMILES -> RDKit Mol -> Morgan fingerprint -> UMAP/PCA embedding -> kNN permutation enrichment.

## Slide 7: Live Demo

```bash
cypchemspace analyze examples/example_data/cyp_substrates_demo.csv --out-dir results/demo_run --n-permutations 99
```

## Slide 8: Results

Show `summary.csv` and `cypchemspace_umap.png`.

## Slide 9: Interpretation and Limitations

Local enrichment is supported statistically; UMAP is visual; demo data is not the full research dataset.

## Slide 10: Future Work

Eight-fingerprint sensitivity, unique-InChIKey collapse, logP module, protein localization curation, workflow automation.
