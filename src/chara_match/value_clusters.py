from __future__ import annotations
import numpy as np
import pandas as pd
from .config import (
    FACTOR_CODES, FACTOR_LABELS, KMEANS_MAX_ITER, KMEANS_N_INIT,
    KMEANS_SEED_BASE, KMEANS_TOL, N_CLUSTERS, N_FACTORS,
    WEIGHT_COL, STANDARDIZED_VALUE_COLS,
)
from .factor_cluster import WeightedKMeans, extract_rotated_pca_factors

def cluster_values(df: pd.DataFrame):
    missing = [c for c in [WEIGHT_COL, *STANDARDIZED_VALUE_COLS] if c not in df.columns]
    if missing:
        raise KeyError(f"Missing standardized columns: {missing[:10]}")

    X = df[STANDARDIZED_VALUE_COLS].astype(float).to_numpy()
    w = df[WEIGHT_COL].astype(float).to_numpy()

    fac = extract_rotated_pca_factors(X, w, n_factors=N_FACTORS)
    F = fac["scores"]

    out = df.copy()
    factor_cols = []
    for j, (code, label) in enumerate(zip(FACTOR_CODES, FACTOR_LABELS), start=1):
        col = f"FACTOR_{j:02d}"
        out[col] = F[:, j - 1]
        factor_cols.append(col)

    km = WeightedKMeans(
        N_CLUSTERS,
        n_init=KMEANS_N_INIT,
        max_iter=KMEANS_MAX_ITER,
        tol=KMEANS_TOL,
        seed_base=KMEANS_SEED_BASE,
    ).fit(F, w)

    if len(np.unique(km.labels_)) != N_CLUSTERS:
        raise ValueError("Data cannot form the requested number of nonempty clusters")
    out["CLUSTER_ID"] = km.labels_ + 1
    dist = km.transform(F)
    out["CLUSTER_DISTANCE"] = dist[np.arange(len(out)), km.labels_]
    out["CLUSTER_MARGIN"] = km.assignment_margin(F)

    diag = {
        "factor_columns": factor_cols,
        "factor_labels": FACTOR_LABELS,
        "eigenvalues": fac["eigenvalues"].tolist(),
        "rotated_loadings": fac["loadings"].tolist(),
        "weighted_inertia": km.inertia_,
        "best_seed": km.best_seed_,
        "iterations": km.n_iter_,
        "note": (
            "K-means numeric IDs can permute across reruns/equivalent solutions; "
            "semantic labels should be assigned by inspecting cluster profiles."
        ),
    }
    return out, diag
