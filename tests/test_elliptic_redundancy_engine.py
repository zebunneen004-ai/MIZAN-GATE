from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from mizan_gate.experiments.elliptic_redundancy import (
    ExperimentProtocolError,
    alert_budget_metrics,
    class_ratio,
    classify_interval,
    estimands_from_metric_map,
    fit_predict_mean_across_seeds,
    load_experiment_plan,
    paired_bootstrap_intervals,
    plan_as_dict,
)

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "configs" / "experiments" / "elliptic_redundancy_v0_1.yaml"
RUNTIME = ROOT / "configs" / "implementation" / "elliptic_redundancy_v0_1_runtime.yaml"


def test_registered_plan_is_exactly_locked() -> None:
    plan = load_experiment_plan(EXPERIMENT, RUNTIME)
    payload = plan_as_dict(plan)
    assert payload["seeds"] == [11, 23, 42, 71, 101]
    assert payload["extension_window"]["train"] == [1, 30]
    assert payload["extension_window"]["evaluate"] == [31, 40]
    assert payload["historical_window"]["train"] == [1, 30]
    assert payload["historical_window"]["evaluate"] == [41, 49]
    assert payload["bootstrap"]["random_seed"] == 20260807
    assert payload["xgboost_runtime"]["n_jobs"] == 1
    assert payload["real_execution_python"] == "3.14.6"
    assert payload["real_execution_versions"]["xgboost"] == "3.3.0"


def test_class_ratio_requires_both_classes() -> None:
    assert class_ratio(pd.Series([0, 0, 0, 1])) == 3.0
    with pytest.raises(ExperimentProtocolError):
        class_ratio(pd.Series([0, 0]))


def test_estimands_follow_registered_formula() -> None:
    values = estimands_from_metric_map(
        {
            "local": 0.40,
            "local_plus_topology": 0.44,
            "full_supplied": 0.50,
            "full_plus_topology": 0.51,
        }
    )
    assert values["delta_local"] == pytest.approx(0.04)
    assert values["delta_full"] == pytest.approx(0.01)
    assert values["redundancy_contrast"] == pytest.approx(0.03)
    assert values["full_minus_local"] == pytest.approx(0.10)


def test_alert_budget_uses_score_then_txid_tie_break() -> None:
    metrics = alert_budget_metrics(
        txid=np.array([30, 10, 20, 40]),
        target=np.array([1, 0, 1, 0]),
        scores=np.array([0.8, 0.9, 0.9, 0.1]),
        budget=0.5,
    )
    assert metrics["alerts"] == 2
    # txId 10 and 20 tie at 0.9; both are selected before txId 30 at 0.8.
    assert metrics["true_positives"] == 1
    assert metrics["precision"] == pytest.approx(0.5)
    assert metrics["recall"] == pytest.approx(0.5)


class _FakeModel:
    def __init__(self, seed: int):
        self.seed = seed

    def fit(self, x: pd.DataFrame, y: pd.Series) -> _FakeModel:
        assert len(x) == len(y)
        return self

    def predict_proba(self, x: pd.DataFrame) -> np.ndarray:
        score = np.clip(0.1 + x.iloc[:, 0].to_numpy() * 0.1 + self.seed * 0.001, 0, 1)
        return np.column_stack([1 - score, score])


def _fake_factory(parameters: dict, seed: int, n_jobs: int, target: pd.Series) -> _FakeModel:
    assert parameters == {"unused": True}
    assert n_jobs == 1
    assert set(target.unique()) == {0, 1}
    return _FakeModel(seed)


def test_seed_probabilities_are_averaged_before_metrics() -> None:
    train = pd.DataFrame({"x": [0.0, 1.0, 2.0, 3.0], "label": [0, 0, 1, 1]})
    evaluation = pd.DataFrame({"x": [0.0, 1.0, 2.0, 3.0], "label": [0, 1, 0, 1]})
    means, seed_metrics = fit_predict_mean_across_seeds(
        train,
        {"synthetic": evaluation},
        ["x"],
        feature_set="synthetic",
        parameters={"unused": True},
        seeds=[1, 3],
        n_jobs=1,
        model_factory=_fake_factory,
    )
    expected = np.array([0.102, 0.202, 0.302, 0.402])
    assert np.allclose(means["synthetic"], expected)
    assert len(seed_metrics) == 2


def _synthetic_prediction_frame() -> pd.DataFrame:
    rows = []
    for time_step in range(31, 36):
        for within in range(20):
            label = int(within % 5 == 0)
            txid = time_step * 1000 + within
            base = 0.15 + 0.65 * label + 0.002 * within
            scores = {
                "local": base,
                "local_plus_topology": base + (0.03 if label else -0.01),
                "full_supplied": base + (0.05 if label else -0.02),
                "full_plus_topology": base + (0.055 if label else -0.022),
            }
            for feature_set, score in scores.items():
                rows.append(
                    {
                        "txId": txid,
                        "time_step": time_step,
                        "label": label,
                        "feature_set": feature_set,
                        "mean_score": float(np.clip(score, 0, 1)),
                    }
                )
    return pd.DataFrame(rows)


def test_paired_bootstrap_is_deterministic() -> None:
    predictions = _synthetic_prediction_frame()
    first = paired_bootstrap_intervals(
        predictions,
        repetitions=50,
        random_seed=123,
        method="time_step_block",
        alpha=0.05,
        practical_margin=0.01,
    )
    second = paired_bootstrap_intervals(
        predictions,
        repetitions=50,
        random_seed=123,
        method="time_step_block",
        alpha=0.05,
        practical_margin=0.01,
    )
    pd.testing.assert_frame_equal(first, second)
    assert set(first["contrast"]) == {
        "delta_local",
        "delta_full",
        "redundancy_contrast",
        "full_minus_local",
    }


def test_interval_classification_matches_preregistered_rules() -> None:
    assert classify_interval(0.011, 0.020, 0.01) == "helpful"
    assert classify_interval(-0.030, -0.011, 0.01) == "harmful"
    assert classify_interval(-0.005, 0.008, 0.01) == "practically_neutral"
    assert classify_interval(-0.02, 0.02, 0.01) == "uncertain"
