from __future__ import annotations
import numpy as np
import pandas as pd
from .config import N_CLUSTERS

def classify_candidates(pair_scores, compatibility_col="compatibility_m30", expansion_col="expansion_m30"):
    out = pair_scores.copy()
    comp_median = float(out[compatibility_col].quantile(0.50))
    comp_q3 = float(out[compatibility_col].quantile(0.75))
    exp_q3 = float(out[expansion_col].quantile(0.75))

    high_c = out[compatibility_col] >= comp_q3
    high_e = out[expansion_col] >= exp_q3

    out["candidate_type"] = np.select(
        [high_c & high_e, high_c & ~high_e, ~high_c & high_e],
        ["本命候補", "既存顧客強化", "新市場開拓"],
        default="優先度低め",
    )
    out["compatibility_band"] = np.select(
        [
            out[compatibility_col] >= comp_q3,
            out[compatibility_col] >= comp_median
        ],
        ["high", "medium"],
        default="low",
    )
    return out, {
        "compatibility_median": comp_median,
        "compatibility_top_quartile": comp_q3,
        "expansion_top_quartile": exp_q3,
    }

def customer_shift_long(product_vectors, character_vectors, m=30):
    rows = []
    for _, p in product_vectors.iterrows():
        pv = np.array([p[f"C{k}_share"] for k in range(1, N_CLUSTERS + 1)])
        for _, c in character_vectors.iterrows():
            cv = np.array([c[f"m{m}_C{k}_share"] for k in range(1, N_CLUSTERS + 1)])
            for k, val in enumerate(cv - pv, start=1):
                rows.append({
                    "product_variable": p["entity_variable"],
                    "character_variable": c["character_variable"],
                    "cluster_id": k,
                    "shift": float(val),
                })
    return pd.DataFrame(rows)

def add_recommendation_reason(df):
    out = df.copy()
    def reason(r):
        if r["candidate_type"] == "本命候補":
            return "現在顧客との相性が高く、新市場への拡張余地も大きい候補"
        if r["candidate_type"] == "既存顧客強化":
            return "現在の購買層との親和性が高く、既存顧客向け施策に向く候補"
        if r["candidate_type"] == "新市場開拓":
            return f"クラスタ{int(r['top_expansion_cluster_id'])}方向への拡張余地が大きい候補"
        return "他候補と比較しながら優先度を慎重に検討する候補"
    out["recommendation_reason"] = out.apply(reason, axis=1)
    return out
