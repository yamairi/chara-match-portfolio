from __future__ import annotations
import numpy as np
from .utils import normalize_weights, sigmoid

class RidgeLogisticRegression:
    """Weighted L2 logistic regression with unpenalized intercept."""
    def __init__(self, lam=1.0, max_iter=80, tol=1e-8):
        self.lam = float(lam)
        self.max_iter = int(max_iter)
        self.tol = float(tol)
        self.coef_ = None
        self.converged_ = False
        self.n_iter_ = 0

    def fit(self, X, y, sample_weight=None):
        self.converged_ = False
        self.n_iter_ = 0
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)
        w = np.ones(len(y)) if sample_weight is None else normalize_weights(sample_weight)

        p = X.shape[1]
        beta = np.zeros(p)
        penalty = np.eye(p) * self.lam
        penalty[0, 0] = 0.0

        for it in range(1, self.max_iter + 1):
            prob = sigmoid(X @ beta)
            v = np.clip(prob * (1 - prob), 1e-8, None)
            grad = X.T @ (w * (y - prob)) - penalty @ beta
            H = X.T @ ((w * v)[:, None] * X) + penalty
            try:
                step = np.linalg.solve(H, grad)
            except np.linalg.LinAlgError:
                step = np.linalg.pinv(H) @ grad
            new_beta = beta + step
            if np.max(np.abs(new_beta - beta)) < self.tol:
                beta = new_beta
                self.converged_ = True
                self.n_iter_ = it
                break
            beta = new_beta
        else:
            self.n_iter_ = self.max_iter

        self.coef_ = beta
        return self

    def predict_proba(self, X):
        return sigmoid(np.asarray(X, dtype=float) @ self.coef_)
