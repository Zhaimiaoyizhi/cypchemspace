"""k-nearest-neighbor label enrichment statistics."""

from __future__ import annotations

import numpy as np
from sklearn.neighbors import NearestNeighbors


def knn_label_enrichment(
    features: np.ndarray,
    labels,
    positive_label: str = "mydb",
    k: int = 15,
    n_permutations: int = 999,
    random_state: int = 42,
) -> dict[str, float | int | str]:
    """Estimate whether positive-label compounds cluster with each other locally.

    The observed statistic is the fraction of positive-label neighbors among the
    k nearest neighbors of positive-label compounds. The p-value is an empirical
    upper-tail permutation p-value.
    """

    matrix = np.asarray(features)
    label_array = np.asarray(labels, dtype=str)
    if matrix.ndim != 2:
        raise ValueError("features must be a two-dimensional array")
    if len(label_array) != matrix.shape[0]:
        raise ValueError("labels length must match number of feature rows")
    if matrix.shape[0] <= 2:
        raise ValueError("at least three rows are required for kNN enrichment")
    if positive_label not in set(label_array):
        raise ValueError(f"positive_label not present: {positive_label}")

    safe_k = max(1, min(k, matrix.shape[0] - 1))
    observed = _positive_neighbor_fraction(matrix, label_array, positive_label, safe_k)
    rng = np.random.default_rng(random_state)
    null_values = np.empty(n_permutations, dtype=float)
    for index in range(n_permutations):
        permuted = rng.permutation(label_array)
        null_values[index] = _positive_neighbor_fraction(matrix, permuted, positive_label, safe_k)

    p_value = (float(np.sum(null_values >= observed)) + 1.0) / (float(n_permutations) + 1.0)
    return {
        "positive_label": positive_label,
        "k": safe_k,
        "n_rows": int(matrix.shape[0]),
        "n_positive": int(np.sum(label_array == positive_label)),
        "n_permutations": int(n_permutations),
        "observed_positive_neighbor_fraction": float(observed),
        "mean_null_positive_neighbor_fraction": float(np.mean(null_values)),
        "delta": float(observed - np.mean(null_values)),
        "p_value": float(p_value),
    }


def _positive_neighbor_fraction(features: np.ndarray, labels: np.ndarray, positive_label: str, k: int) -> float:
    positive_mask = labels == positive_label
    if not np.any(positive_mask):
        return 0.0

    neighbors = NearestNeighbors(n_neighbors=k + 1, metric="jaccard")
    neighbors.fit(features.astype(bool))
    indices = neighbors.kneighbors(return_distance=False)[:, 1:]
    positive_neighbor_counts = np.mean(labels[indices[positive_mask]] == positive_label, axis=1)
    return float(np.mean(positive_neighbor_counts))
