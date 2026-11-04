from __future__ import annotations
import numpy as np
import pandas as pd
from .config import VALUE_COLS, WEIGHT_COL, CONTEXT_COLS, CV_FOLDS
from .utils import weighted_mean, weighted_std

def validate_input(df, product_cols, character_cols):
    if not product_cols or not character_cols:
        raise ValueError("At least one product and character are required")
    if not df.columns.is_unique or len(set(product_cols)) != len(product_cols) or len(set(character_cols)) != len(character_cols):
        raise ValueError("Duplicate columns are not supported")
    needed = [WEIGHT_COL, *VALUE_COLS, *CONTEXT_COLS, *product_cols, *character_cols]
    missing = [c for c in needed if c not in df]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    if len(df) < 2 * CV_FOLDS:
        raise ValueError("Too few rows for cross-validation")
    numeric = df[[WEIGHT_COL, *VALUE_COLS, *product_cols, *character_cols]].to_numpy(dtype=float)
    if not np.isfinite(numeric).all():
        raise ValueError("Numeric inputs must be finite and non-missing")
    if (df[WEIGHT_COL] <= 0).any():
        raise ValueError("Weights must be positive")
    if df[CONTEXT_COLS].isna().any().any():
        raise ValueError("Context categories must not be missing")
    for c in VALUE_COLS:
        if df[c].nunique() < 2:
            raise ValueError(f"Constant value item: {c}")
    for c in product_cols:
        if (df[c] < 0).any():
            raise ValueError("Product amounts must be nonnegative")
        counts = (df[c] > 0).value_counts()
        if len(counts) != 2 or counts.min() < CV_FOLDS:
            raise ValueError(f"Product needs both classes with enough rows for CV: {c}")
    for c in character_cols:
        if not df[c].isin([0, 1]).all() or df[c].nunique() != 2:
            raise ValueError(f"Support needs binary values and both classes: {c}")

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize continuous artificial items; no source questionnaire coding."""
    out = df.copy()
    w = out[WEIGHT_COL].to_numpy(dtype=float)
    for col in VALUE_COLS:
        x = out[col].to_numpy(dtype=float)
        sd = weighted_std(x, w, axis=None)
        if not np.isfinite(sd) or sd <= 0:
            raise ValueError(f"{col} has zero or invalid weighted SD")
        out[f"Z_{col}"] = (x - weighted_mean(x, w)) / sd
    return out
