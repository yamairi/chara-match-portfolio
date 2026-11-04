from __future__ import annotations
import numpy as np
import pandas as pd
from .config import N_CLUSTERS
from .config import PRIMARY_SHRINKAGE_M, RIDGE_LAMBDA, WEIGHT_COL
from .design_matrix import build_context_design
from .linear_models import RidgeLogisticRegression
from .utils import add_intercept, cosine_similarity

def _pvec(row):
    return np.array([row[f"C{k}_share"] for k in range(1, N_CLUSTERS + 1)], dtype=float)

def _cvec(row, m):
    return np.array([row[f"m{m}_C{k}_share"] for k in range(1, N_CLUSTERS + 1)], dtype=float)

def compute_affinity(character_vector, market_vector):
    return np.asarray(character_vector, dtype=float) / np.asarray(market_vector, dtype=float)

def compute_expansion(gap_vector, affinity, reliability):
    return float(np.sum(
        np.asarray(gap_vector, dtype=float)
        * np.maximum(np.asarray(affinity, dtype=float) - 1.0, 0.0)
        * float(reliability)
    ))

def score_all_pairs(product_vectors, character_vectors, gap_long, market_vector, m=PRIMARY_SHRINKAGE_M):
    market = np.array([market_vector[f"C{k}_share"] for k in range(1, N_CLUSTERS + 1)], dtype=float)
    gap_wide = (
        gap_long.pivot(index="product_variable", columns="cluster_id", values="gap_01")
        .reindex(columns=range(1, N_CLUSTERS + 1))
    )

    rows = []
    for _, p in product_vectors.iterrows():
        pv = _pvec(p)
        gaps = gap_wide.loc[p["entity_variable"]].to_numpy(dtype=float)
        for _, c in character_vectors.iterrows():
            cv = _cvec(c, m)
            rel = float(c[f"reliability_m{m}"])
            affinity = compute_affinity(cv, market)
            contribution = gaps * np.maximum(affinity - 1.0, 0.0) * rel
            rows.append({
                "product_variable": p["entity_variable"],
                "character_variable": c["character_variable"],
                f"compatibility_m{m}": cosine_similarity(pv, cv),
                f"expansion_m{m}": float(contribution.sum()),
                "top_expansion_cluster_id": int(np.argmax(contribution) + 1),
                "trust_level": c["trust_level"],
                "n_eff": float(c["n_eff"]),
            })
    return pd.DataFrame(rows)

def unexpected_affinity_by_pair(df, product_cols, character_support_cols):
    """Descriptive support residual conditional on fictional context groups.

    Fitted on the analysis sample; not an out-of-sample or causal estimate.
    """
    w = df[WEIGHT_COL].astype(float).to_numpy()
    X = add_intercept(build_context_design(df).to_numpy(dtype=float))

    char_predictions = {}
    char_actual = {}
    for c in character_support_cols:
        y = (pd.to_numeric(df[c], errors="coerce").fillna(0).to_numpy() == 1).astype(int)
        model = RidgeLogisticRegression(RIDGE_LAMBDA).fit(X, y, w)
        char_predictions[c] = model.predict_proba(X)
        char_actual[c] = y

    rows = []
    for p in product_cols:
        buy = pd.to_numeric(df[p], errors="coerce").fillna(0).to_numpy() > 0
        ww = w[buy]
        for c in character_support_cols:
            actual = float(np.average(char_actual[c][buy], weights=ww))
            expected = float(np.average(char_predictions[c][buy], weights=ww))
            rows.append({
                "product_variable": p,
                "character_variable": c,
                "actual_support": actual,
                "context_expected_support": expected,
                "unexpected_affinity": actual - expected,
            })
    return pd.DataFrame(rows)
