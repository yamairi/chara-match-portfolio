from __future__ import annotations
import numpy as np

EPS = 1e-12

def normalize_weights(w):
    w = np.asarray(w, dtype=float)
    m = np.mean(w)
    if not np.isfinite(m) or m <= 0:
        raise ValueError("weights must have positive finite mean")
    return w / m

def weighted_mean(x, w, axis=None):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    if axis is None:
        return float(np.sum(w * x) / np.sum(w))
    if axis == 0:
        return np.sum(x * w[:, None], axis=0) / np.sum(w)
    raise NotImplementedError

def weighted_var(x, w, axis=0):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    mu = weighted_mean(x, w, axis=axis)
    if axis == 0:
        return np.sum(w[:, None] * (x - mu) ** 2, axis=0) / np.sum(w)
    return float(np.sum(w * (x - mu) ** 2) / np.sum(w))

def weighted_std(x, w, axis=0):
    return np.sqrt(np.maximum(weighted_var(x, w, axis=axis), 0.0))

def weighted_standardize(x, w):
    x = np.asarray(x, dtype=float)
    mu = weighted_mean(x, w, axis=0)
    sd = weighted_std(x, w, axis=0)
    if np.any(sd <= 0):
        raise ValueError("zero-SD variable found")
    return (x - mu) / sd, mu, sd

def weighted_cov(x, w):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    mu = weighted_mean(x, w, axis=0)
    xc = x - mu
    return (xc * w[:, None]).T @ xc / np.sum(w)

def weighted_corr(x, w):
    cov = weighted_cov(x, w)
    sd = np.sqrt(np.diag(cov))
    return cov / np.outer(sd, sd)

def effective_n(w):
    w = np.asarray(w, dtype=float)
    den = np.sum(w ** 2)
    if den <= 0:
        return 0.0
    return float(np.sum(w) ** 2 / den)

def cosine_similarity(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    den = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / den) if den > 0 else np.nan

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -40, 40)))

def add_intercept(x):
    x = np.asarray(x, dtype=float)
    return np.column_stack([np.ones(len(x)), x])

def log_loss(y, p, w=None):
    y = np.asarray(y, dtype=float)
    p = np.clip(np.asarray(p, dtype=float), EPS, 1 - EPS)
    v = -(y * np.log(p) + (1 - y) * np.log(1 - p))
    return float(np.average(v, weights=w))

def brier_score(y, p, w=None):
    y = np.asarray(y, dtype=float)
    p = np.asarray(p, dtype=float)
    return float(np.average((y - p) ** 2, weights=w))

def weighted_auc(y, score, w=None):
    y = np.asarray(y, dtype=int)
    score = np.asarray(score, dtype=float)
    w = np.ones(len(y), dtype=float) if w is None else np.asarray(w, dtype=float)
    pos = y == 1
    neg = y == 0
    wp, wn = w[pos].sum(), w[neg].sum()
    if wp <= 0 or wn <= 0:
        return np.nan

    order = np.argsort(score, kind="mergesort")
    s, yy, ww = score[order], y[order], w[order]
    auc_num = 0.0
    cum_neg = 0.0
    i = 0
    while i < len(s):
        j = i + 1
        while j < len(s) and s[j] == s[i]:
            j += 1
        bw = ww[i:j]
        by = yy[i:j]
        block_pos = bw[by == 1].sum()
        block_neg = bw[by == 0].sum()
        auc_num += block_pos * (cum_neg + 0.5 * block_neg)
        cum_neg += block_neg
        i = j
    return float(auc_num / (wp * wn))
