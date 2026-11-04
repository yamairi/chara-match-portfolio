import numpy as np
import pandas as pd
import pytest
from chara_match.synthetic import generate_synthetic_data
from chara_match.config import PRODUCT_COLS, CHARACTER_SUPPORT_COLS, VALUE_COLS, N_CLUSTERS, CV_FOLDS
from chara_match.pipeline import run_pipeline
from chara_match.preprocessing import validate_input, preprocess
from chara_match.vectors import shrink_vector
from chara_match.scores import compute_affinity, compute_expansion
from chara_match.utils import cosine_similarity, weighted_auc, effective_n
from chara_match.factor_cluster import extract_rotated_pca_factors

@pytest.fixture(scope="module")
def demo():
    return generate_synthetic_data(256, seed=2718)

@pytest.fixture(scope="module")
def result(demo):
    return run_pipeline(demo, PRODUCT_COLS[:2], CHARACTER_SUPPORT_COLS[:3])

def test_generator_is_reproducible_and_seed_sensitive():
    a = generate_synthetic_data(128, 17)
    pd.testing.assert_frame_equal(a, generate_synthetic_data(128, 17))
    assert not a.equals(generate_synthetic_data(128, 18))

def test_generator_rejects_small_population():
    with pytest.raises(ValueError):
        generate_synthetic_data(10)

def test_schema_and_weights(demo):
    validate_input(demo, PRODUCT_COLS, CHARACTER_SUPPORT_COLS)
    assert demo.SYNTHETIC_ID.is_unique
    assert len(demo.columns) == 4 + len(VALUE_COLS) + len(PRODUCT_COLS) + len(CHARACTER_SUPPORT_COLS)

def test_preprocessing_weighted_moments_and_no_mutation(demo):
    before = demo.copy(deep=True)
    out = preprocess(demo)
    z = out[[f"Z_{c}" for c in VALUE_COLS]].to_numpy()
    w = demo.SAMPLE_WEIGHT.to_numpy()
    assert np.allclose(np.average(z, axis=0, weights=w), 0, atol=1e-10)
    assert np.allclose(np.average(z*z, axis=0, weights=w), 1)
    pd.testing.assert_frame_equal(demo, before)

def test_factor_projection_matches_training_scores(demo):
    out = preprocess(demo)
    x = out[[f"Z_{c}" for c in VALUE_COLS]].to_numpy()
    fac = extract_rotated_pca_factors(x, demo.SAMPLE_WEIGHT.to_numpy())
    transformed = (x @ fac["projection"] - fac["score_mean"]) / fac["score_std"]
    assert np.allclose(transformed, fac["scores"])

def test_shrinkage_limits_and_effective_n():
    raw, market = np.array([.7, .3]), np.array([.4, .6])
    out, reliability = shrink_vector(raw, market, 12, 12)
    assert np.allclose(out, [.55, .45])
    assert reliability == .5
    assert np.allclose(shrink_vector(raw, market, 0, 12)[0], market)
    assert effective_n([2, 2, 2]) == 3
    assert effective_n([1, 4]) < 2

def test_score_formulas_known_answers():
    assert np.allclose(compute_affinity([.6, .4], [.3, .7]), [2, 4/7])
    assert compute_expansion([.2, .1], [2, .5], .5) == pytest.approx(.1)
    assert compute_expansion([.2, .1], [1, 1], .5) == 0
    assert cosine_similarity([1, 0], [0, 1]) == 0
    assert cosine_similarity([.3, .7], [.3, .7]) == pytest.approx(1)

def test_weighted_auc_ties():
    assert weighted_auc([0, 1], [.5, .5], [2, 7]) == .5
    assert weighted_auc([0, 1], [.1, .9], [2, 7]) == 1

def test_pipeline_cartesian_pairs_and_finite_scores(result):
    p = result["pair_scores"]
    assert len(p) == 6
    assert not p.duplicated(["product_variable", "character_variable"]).any()
    assert np.isfinite(p.select_dtypes("number")).all().all()
    assert p.compatibility_m30.between(0, 1 + 1e-10).all()
    assert (p.expansion_m30 >= 0).all()
    assert result["model_summary"].converged.all()

def test_vector_mass_and_shift_conservation(result):
    shares = [f"C{k}_share" for k in range(1, N_CLUSTERS + 1)]
    assert np.allclose(result["product_vectors"][shares].sum(axis=1), 1)
    assert np.allclose(result["character_vectors"][[f"m30_{s}" for s in shares]].sum(axis=1), 1)
    shifts = result["customer_shift_long"]
    assert len(shifts) == 6 * N_CLUSTERS
    assert np.allclose(shifts.groupby(["product_variable", "character_variable"])["shift"].sum(), 0, atol=1e-10)

def test_pipeline_reproducible_and_input_unchanged(demo, result):
    before = demo.copy(deep=True)
    again = run_pipeline(demo, PRODUCT_COLS[:2], CHARACTER_SUPPORT_COLS[:3])
    pd.testing.assert_frame_equal(again["pair_scores"], result["pair_scores"])
    pd.testing.assert_frame_equal(demo, before)

def test_cv_fits_factors_on_training_rows_only(demo, monkeypatch):
    import chara_match.product_fit as mod
    original = mod.extract_rotated_pca_factors
    lengths = []
    def observe(x, w, n):
        lengths.append(len(x))
        return original(x, w, n)
    monkeypatch.setattr(mod, "extract_rotated_pca_factors", observe)
    run_pipeline(demo, PRODUCT_COLS[:1], CHARACTER_SUPPORT_COLS[:1])
    assert len(lengths) == CV_FOLDS
    assert all(0 < n < len(demo) for n in lengths)

@pytest.mark.parametrize("kind", ["missing", "nan", "infinite", "weight_zero", "weight_negative", "constant", "negative_purchase", "single_product_class", "support_code", "empty_support", "missing_context"])
def test_invalid_inputs_fail_clearly(demo, kind):
    x = demo.copy()
    if kind == "missing": x = x.drop(columns=[VALUE_COLS[0]])
    elif kind == "nan": x.loc[0, VALUE_COLS[0]] = np.nan
    elif kind == "infinite": x.loc[0, VALUE_COLS[0]] = np.inf
    elif kind == "weight_zero": x.loc[0, "SAMPLE_WEIGHT"] = 0
    elif kind == "weight_negative": x.loc[0, "SAMPLE_WEIGHT"] = -1
    elif kind == "constant": x[VALUE_COLS[0]] = 1
    elif kind == "negative_purchase": x.loc[0, PRODUCT_COLS[0]] = -1
    elif kind == "single_product_class": x[PRODUCT_COLS[0]] = 0
    elif kind == "support_code": x.loc[0, CHARACTER_SUPPORT_COLS[0]] = 2
    elif kind == "empty_support": x[CHARACTER_SUPPORT_COLS[0]] = 0
    elif kind == "missing_context": x.loc[0, "CONTEXT_GROUP"] = None
    with pytest.raises(ValueError):
        run_pipeline(x, PRODUCT_COLS[:1], CHARACTER_SUPPORT_COLS[:1])
