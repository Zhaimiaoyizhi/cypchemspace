# Full clean reference results

This directory stores the full/reference project outputs copied from the
original `CYP_comparison` workflow. They are included so the recorded live demo
can show both a fast reproducible run and the actual project-scale result.

Files:

- `combined_stats_results_perm5000.tsv`: kNN enrichment statistics for the clean
  rescued table using 5,000 label permutations.
- `combined_stats_results_perm5000.meta.json`: metadata for the permutation run.
- `combined_perm_null_perm5000.npz`: saved permutation null distributions.
- `umap_mydb_vs_background_clean_rescued.png`: final UMAP figure for the clean
  rescued analysis.
- `umap_mydb_vs_background_clean_rescued.pdf`: PDF version of the final UMAP
  figure.
- `umap_mydb_vs_background_clean_rescued_plot_data.csv`: plotting table behind
  the final UMAP figure.

The live demo result in `../demo_clean_2548_128bit_pca_perm19/` uses a faster
128-bit fingerprint, PCA embedding, and 19 permutations. The reference result in
this directory uses the project-scale 5,000-permutation statistic for reporting.
