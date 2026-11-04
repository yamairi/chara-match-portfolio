from __future__ import annotations
import numpy as np
import pandas as pd
from .config import CV_FOLDS, CV_LOGLOSS_IMPROVEMENT, RIDGE_LAMBDA, WEIGHT_COL, VALUE_COLS, N_FACTORS
from .design_matrix import build_basic_design
from .linear_models import RidgeLogisticRegression
from .utils import add_intercept, brier_score, log_loss, weighted_auc, weighted_standardize
from .factor_cluster import extract_rotated_pca_factors

def stratified_folds(y, n_splits=5, seed=1729):
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=int)
    folds = np.empty(len(y), dtype=int)
    for cls in [0, 1]:
        idx = np.flatnonzero(y == cls)
        rng.shuffle(idx)
        folds[idx] = np.arange(len(idx)) % n_splits
    return folds

def _cv(X, y, w, folds, values=None):
    rows = []
    for f in range(folds.max() + 1):
        tr, te = folds != f, folds == f
        train, test = X[tr], X[te]
        if values is not None:
            z, mu, sd = weighted_standardize(values[tr], w[tr])
            fac = extract_rotated_pca_factors(z, w[tr], N_FACTORS)
            test_scores = (((values[te] - mu) / sd) @ fac["projection"] - fac["score_mean"]) / fac["score_std"]
            train = np.column_stack([train, fac["scores"]])
            test = np.column_stack([test, test_scores])
        model = RidgeLogisticRegression(RIDGE_LAMBDA).fit(train, y[tr], w[tr])
        if not model.converged_:
            raise RuntimeError("Cross-validation model did not converge")
        pred = model.predict_proba(test)
        rows.append({
            "fold": int(f), "auc": weighted_auc(y[te], pred, w[te]),
            "logloss": log_loss(y[te], pred, w[te]),
            "brier": brier_score(y[te], pred, w[te]),
            "weight_sum": float(w[te].sum()),
        })
    return pd.DataFrame(rows)

def run_product_model(df, product_col, factor_cols, cluster_col="CLUSTER_ID"):
    w = df[WEIGHT_COL].astype(float).to_numpy()
    y = (pd.to_numeric(df[product_col], errors="coerce").fillna(0).to_numpy() > 0).astype(int)

    basic = build_basic_design(df)
    Xb = add_intercept(basic.to_numpy(dtype=float))
    Xe = add_intercept(np.column_stack([
        basic.to_numpy(dtype=float),
        df[factor_cols].astype(float).to_numpy()
    ]))

    folds = stratified_folds(y, CV_FOLDS)
    mb = _cv(Xb, y, w, folds)
    me = _cv(Xb, y, w, folds, df[VALUE_COLS].to_numpy(dtype=float))
    llb = float(np.average(mb.logloss, weights=mb.weight_sum))
    lle = float(np.average(me.logloss, weights=me.weight_sum))
    use_ext = (llb - lle) > CV_LOGLOSS_IMPROVEMENT

    X = Xe if use_ext else Xb
    model = RidgeLogisticRegression(RIDGE_LAMBDA).fit(X, y, w)
    pred = model.predict_proba(X)

    rows = []
    for cid in sorted(pd.unique(df[cluster_col])):
        mask = df[cluster_col].to_numpy() == cid
        ww = w[mask]
        fit = float(np.average(pred[mask], weights=ww))
        actual = float(np.average(y[mask], weights=ww))
        gap = fit * (1.0 - actual)
        rows.append({
            "product_variable": product_col,
            "cluster_id": int(cid),
            "weighted_fit": fit,
            "weighted_actual_purchase_rate": actual,
            "gap_01": gap,
        })

    return {
        "selected_model": "extended" if use_ext else "basic",
        "cluster_table": pd.DataFrame(rows),
        "cv_basic": mb,
        "cv_extended": me,
        "cv_logloss_basic": llb,
        "cv_logloss_extended": lle,
        "converged": bool(model.converged_),
    }
