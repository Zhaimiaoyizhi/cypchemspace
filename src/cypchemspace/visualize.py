"""Plotting helpers for course-project figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


LABEL_COLORS = {
    "mydb": "#1f77b4",
    "p450db": "#8c8c8c",
}


def plot_embedding(
    table: pd.DataFrame,
    output_path: str | Path,
    x_col: str = "umap_x",
    y_col: str = "umap_y",
    label_col: str = "label",
    title: str = "CYP substrate chemical space",
) -> Path:
    """Write a publication-style scatter plot for the two-class embedding."""

    for column in (x_col, y_col, label_col):
        if column not in table.columns:
            raise ValueError(f"Missing plotting column: {column}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(7, 5), dpi=160)
    for label, group in table.groupby(label_col):
        ax.scatter(
            group[x_col],
            group[y_col],
            s=42 if label == "mydb" else 34,
            c=LABEL_COLORS.get(str(label), "#333333"),
            label=f"{label} (n={len(group)})",
            alpha=0.82 if label == "mydb" else 0.58,
            edgecolors="white",
            linewidths=0.4,
        )

    ax.set_title(title)
    ax.set_xlabel("UMAP 1")
    ax.set_ylabel("UMAP 2")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)
    return output
