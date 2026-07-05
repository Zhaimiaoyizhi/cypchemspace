# Live demo result

This directory contains the result generated for the recorded live demo.

Command:

```bash
python -m cypchemspace.cli analyze examples/example_data/clean_rescued_substrates_2548.csv --out-dir results/demo_clean_2548_128bit_pca_perm19 --n-bits 128 --k 15 --n-permutations 19 --embedding-method pca
```

This configuration is intentionally fast enough to rerun during screen
recording:

- input table: 2,548 cleaned substrate records
- fingerprint: Morgan radius 2, 128 bits
- embedding: PCA
- kNN statistic: `k=15`
- permutations: 19

The summary table records `delta = 0.1373273224340521` and `p_value = 0.05`.
Because 19 permutations give coarse p-value resolution, use this as a live
workflow demonstration and compare it with `../full_clean_reference/` for the
project-scale 5,000-permutation result.
