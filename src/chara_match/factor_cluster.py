from __future__ import annotations
import numpy as np
from .config import N_FACTORS
from .utils import weighted_corr, weighted_standardize

def varimax(loadings, gamma=1.0, max_iter=100, tol=1e-7):
    phi = np.asarray(loadings, dtype=float)
    p, k = phi.shape
    R = np.eye(k)
    old = 0.0
    for _ in range(max_iter):
        lam = phi @ R
        target = lam ** 3 - (gamma / p) * lam @ np.diag(np.diag(lam.T @ lam))
        u, s, vh = np.linalg.svd(phi.T @ target)
        R = u @ vh
        cur = s.sum()
        if old and cur / old < 1 + tol:
            break
        old = cur
    return phi @ R, R

def _align_rotated_factors(loadings, scores):
    """Orient each component by its largest loading; no semantic anchor table."""
    signs = np.sign(loadings[np.argmax(np.abs(loadings), axis=0), np.arange(loadings.shape[1])])
    signs[signs == 0] = 1
    return loadings * signs, scores * signs

def extract_rotated_pca_factors(Xz, w, n_factors=N_FACTORS):
    Xz = np.asarray(Xz, dtype=float)
    corr = weighted_corr(Xz, w)
    eigvals, eigvecs = np.linalg.eigh(corr)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]

    V = eigvecs[:, :n_factors]
    vals = eigvals[:n_factors]
    loadings = V * np.sqrt(np.maximum(vals, 0.0))[None, :]
    scores = Xz @ V

    rot_loadings, R = varimax(loadings)
    rot_scores = scores @ R
    signs = np.sign(rot_loadings[np.argmax(np.abs(rot_loadings), axis=0), np.arange(n_factors)])
    signs[signs == 0] = 1
    rot_loadings, rot_scores = _align_rotated_factors(rot_loadings, rot_scores)
    rot_scores_z, score_mean, score_std = weighted_standardize(rot_scores, w)

    return {
        "scores": rot_scores_z,
        "projection": (V @ R) * signs,
        "score_mean": score_mean,
        "score_std": score_std,
        "loadings": rot_loadings,
        "eigenvalues": eigvals,
    }

class WeightedKMeans:
    def __init__(self, n_clusters, n_init=30, max_iter=300, tol=1e-7, seed_base=1729):
        self.n_clusters = int(n_clusters)
        self.n_init = int(n_init)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.seed_base = int(seed_base)
        self.cluster_centers_ = None
        self.labels_ = None
        self.inertia_ = None
        self.best_seed_ = None
        self.n_iter_ = None

    @staticmethod
    def _dist2(X, centers):
        return ((X[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)

    def _init_pp(self, X, w, rng):
        n = len(X)
        centers = []
        first = rng.choice(n, p=w / w.sum())
        centers.append(X[first].copy())
        for _ in range(1, self.n_clusters):
            d2 = self._dist2(X, np.asarray(centers)).min(axis=1)
            p = w * d2
            idx = rng.choice(n, p=(p / p.sum()) if p.sum() > 0 else (w / w.sum()))
            centers.append(X[idx].copy())
        return np.asarray(centers)

    def _one(self, X, w, seed):
        rng = np.random.default_rng(seed)
        centers = self._init_pp(X, w, rng)
        for it in range(1, self.max_iter + 1):
            d2 = self._dist2(X, centers)
            labels = d2.argmin(axis=1)
            new = centers.copy()
            for k in range(self.n_clusters):
                mask = labels == k
                if mask.any():
                    new[k] = np.average(X[mask], axis=0, weights=w[mask])
                else:
                    idx = int(np.argmax(w * d2.min(axis=1)))
                    new[k] = X[idx]
            movement = np.max(np.linalg.norm(new - centers, axis=1))
            centers = new
            if movement < self.tol:
                break
        d2 = self._dist2(X, centers)
        labels = d2.argmin(axis=1)
        inertia = float(np.sum(w * d2[np.arange(len(X)), labels]))
        return centers, labels, inertia, it

    def fit(self, X, sample_weight):
        X = np.asarray(X, dtype=float)
        w = np.asarray(sample_weight, dtype=float)
        best = None
        for i in range(self.n_init):
            seed = self.seed_base + i
            out = self._one(X, w, seed)
            if best is None or out[2] < best[2]:
                best = (*out, seed)
        self.cluster_centers_, self.labels_, self.inertia_, self.n_iter_, self.best_seed_ = best
        return self

    def transform(self, X):
        return np.sqrt(self._dist2(np.asarray(X, dtype=float), self.cluster_centers_))

    def assignment_margin(self, X):
        d = np.sort(self.transform(X), axis=1)
        return d[:, 1] - d[:, 0]
