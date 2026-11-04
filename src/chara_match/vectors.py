from __future__ import annotations
import numpy as np
import pandas as pd
from .config import N_CLUSTERS
from .config import SHRINKAGE_M_VALUES, WEIGHT_COL
from .utils import effective_n

def cluster_share_vector(cluster_ids, weights, k=N_CLUSTERS):
    cluster_ids = np.asarray(cluster_ids, dtype=int)
    weights = np.asarray(weights, dtype=float)
    total = weights.sum()
    if total <= 0:
        return np.full(k, np.nan)
    return np.array([
        weights[cluster_ids == cid].sum() / total
        for cid in range(1, k + 1)
    ])

def shrink_vector(raw, market, n_eff, m):
    r = n_eff / (n_eff + m)
    return r * np.asarray(raw) + (1 - r) * np.asarray(market), r

def trust_level(n_eff):
    if n_eff < 30: return "参考値"
    if n_eff < 50: return "低"
    if n_eff < 100: return "中"
    return "高"

def build_vectors(df, product_cols, character_support_cols, cluster_col="CLUSTER_ID"):
    w = df[WEIGHT_COL].astype(float).to_numpy()
    cluster = df[cluster_col].astype(int).to_numpy()
    market = cluster_share_vector(cluster, w, N_CLUSTERS)

    product_rows = []
    for p in product_cols:
        buy = pd.to_numeric(df[p], errors="coerce").fillna(0).to_numpy() > 0
        vec = cluster_share_vector(cluster[buy], w[buy], N_CLUSTERS)
        row = {"entity_variable": p}
        row.update({f"C{k}_share": vec[k-1] for k in range(1, N_CLUSTERS + 1)})
        product_rows.append(row)

    char_rows = []
    for c in character_support_cols:
        support = pd.to_numeric(df[c], errors="coerce").fillna(0).to_numpy() == 1
        ws = w[support]
        raw = cluster_share_vector(cluster[support], ws, N_CLUSTERS)
        neff = effective_n(ws)
        row = {
            "character_variable": c,
            "n_unweighted": int(support.sum()),
            "weight_sum": float(ws.sum()),
            "n_eff": neff,
            "trust_level": trust_level(neff),
        }
        row.update({f"raw_C{k}_share": raw[k-1] for k in range(1, N_CLUSTERS + 1)})
        for m in SHRINKAGE_M_VALUES:
            shr, r = shrink_vector(raw, market, neff, m)
            row[f"reliability_m{m}"] = r
            row.update({f"m{m}_C{k}_share": shr[k-1] for k in range(1, N_CLUSTERS + 1)})
        char_rows.append(row)

    return {
        "market_vector": {f"C{k}_share": market[k-1] for k in range(1, N_CLUSTERS + 1)},
        "product_vectors": pd.DataFrame(product_rows),
        "character_vectors": pd.DataFrame(char_rows),
    }
