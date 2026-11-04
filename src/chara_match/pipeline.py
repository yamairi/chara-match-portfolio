from __future__ import annotations
import pandas as pd
from .preprocessing import preprocess, validate_input
from .value_clusters import cluster_values
from .product_fit import run_product_model
from .vectors import build_vectors
from .scores import score_all_pairs, unexpected_affinity_by_pair
from .candidates import classify_candidates, customer_shift_long, add_recommendation_reason

def run_pipeline(df, product_cols, character_cols):
    validate_input(df, product_cols, character_cols)
    df4 = preprocess(df)
    df5, diag5 = cluster_values(df4)
    factor_cols = diag5["factor_columns"]

    gaps = []
    model_summary = []
    for p in product_cols:
        fit = run_product_model(df5, p, factor_cols)
        gaps.append(fit["cluster_table"])
        model_summary.append({
            "product_variable": p,
            "selected_model": fit["selected_model"],
            "cv_logloss_basic": fit["cv_logloss_basic"],
            "cv_logloss_extended": fit["cv_logloss_extended"],
            "converged": fit["converged"],
        })
    gap_long = pd.concat(gaps, ignore_index=True)

    vec = build_vectors(df5, product_cols, character_cols)
    pair = score_all_pairs(
        vec["product_vectors"],
        vec["character_vectors"],
        gap_long,
        vec["market_vector"],
        m=30,
    )

    unexpected = unexpected_affinity_by_pair(df5, product_cols, character_cols)
    pair = pair.merge(unexpected, on=["product_variable", "character_variable"], how="left")
    pair, thresholds = classify_candidates(pair)
    pair = add_recommendation_reason(pair)
    shifts = customer_shift_long(vec["product_vectors"], vec["character_vectors"], m=30)

    return {
        "cluster_diagnostics": diag5,
        "model_summary": pd.DataFrame(model_summary),
        "gap_long": gap_long,
        "market_vector": vec["market_vector"],
        "product_vectors": vec["product_vectors"],
        "character_vectors": vec["character_vectors"],
        "pair_scores": pair,
        "thresholds": thresholds,
        "customer_shift_long": shifts,
    }
