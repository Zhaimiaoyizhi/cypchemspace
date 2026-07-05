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
    "shared": "#f28e2b",
}

PLOT_LAYERS = (
    ("p450db", "P450DB only", 30, 0.46, 1),
    ("mydb", "mydb only", 40, 0.78, 2),
    ("shared", "shared by mydb and P450DB", 54, 0.92, 3),
)


def plot_embedding(
    table: pd.DataFrame,
    output_path: str | Path,
    x_col: str = "umap_x",
    y_col: str = "umap_y",
    label_col: str = "label",
    title: str = "CYP substrate chemical space",
    x_label: str = "UMAP 1",
    y_label: str = "UMAP 2",
) -> Path:
    """Write a scatter plot with shared compounds drawn on the top layer."""

    for column in (x_col, y_col, label_col):
        if column not in table.columns:
            raise ValueError(f"Missing plotting column: {column}")

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    plot_table = table.copy()
    plot_table["_plot_group"] = assign_plot_groups(plot_table, label_col=label_col)

    fig, ax = plt.subplots(figsize=(7, 5), dpi=160)
    for group_name, legend_label, size, alpha, zorder in PLOT_LAYERS:
        group = plot_table[plot_table["_plot_group"] == group_name]
        if group.empty:
            continue
        ax.scatter(
            group[x_col],
            group[y_col],
            s=size,
            c=LABEL_COLORS[group_name],
            label=f"{legend_label} (n={len(group)})",
            alpha=alpha,
            edgecolors="white",
            linewidths=0.4,
            zorder=zorder,
        )

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(output)
    plt.close(fig)
    return output


def assign_plot_groups(table: pd.DataFrame, label_col: str = "label") -> pd.Series:
    """Assign plotting groups so shared compounds can be highlighted.

    Shared compounds are identified by `std_inchikey` when the same key appears
    under both `mydb` and `p450db`. If that column is absent, rows fall back to
    their source label.
    """

    labels = table[label_col].astype(str).str.lower()
    groups = labels.where(labels.isin(["mydb", "p450db"]), "p450db")

    if "std_inchikey" not in table.columns:
        return groups

    keys = table["std_inchikey"].astype(str).str.strip()
    valid = keys != ""
    label_sets = labels[valid].groupby(keys[valid]).agg(lambda values: set(values))
    shared_keys = {
        key
        for key, label_set in label_sets.items()
        if {"mydb", "p450db"}.issubset(label_set)
    }
    if not shared_keys:
        return groups

    return groups.mask(keys.isin(shared_keys), "shared")
