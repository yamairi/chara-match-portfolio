from __future__ import annotations
import pandas as pd
from .config import CONTEXT_COLS

def build_basic_design(df: pd.DataFrame):
    """One-hot encode fictional context categories, with no survey-specific recoding."""
    return pd.get_dummies(df[CONTEXT_COLS].astype("category"), drop_first=True, dtype=float).reset_index(drop=True)

def build_context_design(df: pd.DataFrame):
    return build_basic_design(df)
