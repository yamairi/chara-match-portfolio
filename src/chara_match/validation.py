from __future__ import annotations
import pandas as pd

def spearman_rank_correlation(a, b):
    a = pd.Series(a).rank(method="average")
    b = pd.Series(b).rank(method="average")
    return float(a.corr(b, method="pearson"))

def topk_overlap(a, b, k=10):
    ia = set(pd.Series(a).nlargest(k).index)
    ib = set(pd.Series(b).nlargest(k).index)
    return len(ia & ib)
