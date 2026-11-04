"""Artificial population generator: accepts no external input or fitted parameters."""
from __future__ import annotations
import numpy as np
import pandas as pd
from .config import VALUE_COLS, PRODUCT_COLS, CHARACTER_SUPPORT_COLS, WEIGHT_COL
from .utils import sigmoid

DEFAULT_SEED = 1729
DEFAULT_ROWS = 640

def generate_synthetic_data(n_rows=DEFAULT_ROWS, seed=DEFAULT_SEED):
    if n_rows < 64:
        raise ValueError("Use at least 64 artificial rows")
    rng = np.random.default_rng(seed)
    group = rng.integers(0, 3, n_rows)
    channel = rng.integers(0, 2, n_rows)
    latent = rng.normal(size=(n_rows, 3))
    latent[:, 0] += (group - 1) * .5
    data = {
        "SYNTHETIC_ID": [f"SYN_{i:05d}" for i in range(1, n_rows + 1)],
        WEIGHT_COL: np.round(rng.uniform(.7, 1.3, n_rows), 6),
        "CONTEXT_GROUP": np.array(["GROUP_A", "GROUP_B", "GROUP_C"])[group],
        "CHANNEL_GROUP": np.array(["CHANNEL_A", "CHANNEL_B"])[channel],
    }
    for j, name in enumerate(VALUE_COLS):
        data[name] = np.round(latent[:, j % 3] + rng.normal(0, .55, n_rows), 6)
    for name in PRODUCT_COLS:
        beta = rng.normal(0, .55, 3)
        probability = sigmoid(-.4 + latent @ beta + .25 * channel)
        buy = rng.random(n_rows) < probability
        data[name] = np.where(buy, rng.integers(1, 6, n_rows), 0)
    for name in CHARACTER_SUPPORT_COLS:
        beta = rng.normal(0, .65, 3)
        probability = sigmoid(-1.2 + latent @ beta + .2 * (group - 1))
        data[name] = (rng.random(n_rows) < probability).astype(int)
    return pd.DataFrame(data)

def data_dictionary():
    records = [
        ("SYNTHETIC_ID", "string", "Sequential artificial identifier"),
        (WEIGHT_COL, "positive float", "Artificial weight; not a population calibration"),
        ("CONTEXT_GROUP", "category", "Fictional context group without demographic meaning"),
        ("CHANNEL_GROUP", "category", "Fictional channel group"),
    ]
    records += [(c, "float", "Artificial continuous preference item") for c in VALUE_COLS]
    records += [(c, "nonnegative integer", "Artificial quantity; positive means purchase") for c in PRODUCT_COLS]
    records += [(c, "binary", "Artificial character support") for c in CHARACTER_SUPPORT_COLS]
    return pd.DataFrame(records, columns=["variable", "type", "description"])
