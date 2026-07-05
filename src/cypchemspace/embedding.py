"""Embedding helpers for chemical-space visualization."""

from __future__ import annotations

import numpy as np

from cypchemspace._compat import avoid_windows_wmi_platform_probe

avoid_windows_wmi_platform_probe()
import pandas as pd
from sklearn.decomposition import PCA


def compute_embedding(
    features: np.ndarray,
    method: str = "umap",
    random_state: int = 42,
    n_neighbors: int = 8,
    min_dist: float = 0.1,
) -> pd.DataFrame:
    """Compute a two-dimensional embedding from a fingerprint matrix.

    UMAP is used when available and requested. PCA is provided as a deterministic
    fallback for small teaching environments where UMAP is unavailable.
    """

    if features.ndim != 2 or features.shape[0] < 2:
        raise ValueError("features must be a two-dimensional array with at least two rows")

    normalized_method = method.lower()
    if normalized_method == "umap":
        try:
            from umap import UMAP

            safe_neighbors = max(2, min(n_neighbors, features.shape[0] - 1))
            model = UMAP(
                n_components=2,
                n_neighbors=safe_neighbors,
                min_dist=min_dist,
                metric="jaccard",
                random_state=random_state,
            )
            coords = model.fit_transform(features.astype(bool))
        except Exception:
            coords = _pca_embedding(features, random_state=random_state)
            normalized_method = "pca_fallback"
    elif normalized_method == "pca":
        coords = _pca_embedding(features, random_state=random_state)
    else:
        raise ValueError("method must be 'umap' or 'pca'")

    return pd.DataFrame({"umap_x": coords[:, 0], "umap_y": coords[:, 1], "embedding_method": normalized_method})


def _pca_embedding(features: np.ndarray, random_state: int) -> np.ndarray:
    model = PCA(n_components=2, random_state=random_state)
    return model.fit_transform(features.astype(float))
