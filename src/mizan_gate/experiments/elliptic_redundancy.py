"""MIZAN-GATE 0.1A Elliptic relational-redundancy experiment engine.

This module implements the preregistered experiment without interpreting its result.
Real Elliptic execution is intentionally separated from synthetic/unit testing.
"""

from __future__ import annotations

import hashlib
import json
import math
import platform
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import metadata as importlib_metadata
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import sklearn
import xgboost
import yaml
from sklearn.metrics import average_precision_score, roc_auc_score
from xgboost import XGBClassifier

from mizan_gate.data.elliptic import EllipticStudy1Data, load_elliptic_study1
from mizan_gate.features.registry import FeatureManifest, load_feature_manifest


class ExperimentProtocolError(ValueError):
    """Raised when implementation inputs violate the registered experiment protocol."""


PRIMARY_FEATURE_SETS = (
    "local",
    "local_plus_topology",
    "full_supplied",
    "full_plus_topology",
)
SECONDARY_FEATURE_SETS = (
    "aggregate",
    "topology_completed",
    "aggregate_plus_topology",
)
ALL_REGISTERED_FEATURE_SETS = PRIMARY_FEATURE_SETS + SECONDARY_FEATURE_SETS


@dataclass(frozen=True)
class TemporalWindow:
    name: str
    role: str
    train_start: int
    train_end: int
    evaluation_start: int
    evaluation_end: int


@dataclass(frozen=True)
class ExperimentPlan:
    experiment_id: str
    implementation_id: str
    seeds: tuple[int, ...]
    model_parameters: dict[str, Any]
    xgboost_runtime: dict[str, Any]
    development_windows: tuple[TemporalWindow, ...]
    extension_window: TemporalWindow
    historical_window: TemporalWindow
    alert_budgets: tuple[float, ...]
    practical_margin: float
    bootstrap_observation_repetitions: int
    bootstrap_time_step_repetitions: int
    bootstrap_seed: int
    bootstrap_alpha: float
    bootstrap_maximum_attempt_multiplier: int
    feature_manifest_sha256: str
    real_execution_python: str
    real_execution_versions: dict[str, str]


ModelFactory = Callable[[dict[str, Any], int, int, pd.Series], Any]


def _load_yaml(path: str | Path) -> dict[str, Any]:
    resolved = Path(path).expanduser().resolve()
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise ExperimentProtocolError(f"YAML root must be a mapping: {resolved}")
    return payload


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _pair_to_bounds(value: Sequence[int], label: str) -> tuple[int, int]:
    if len(value) != 2:
        raise ExperimentProtocolError(f"{label} must contain exactly two time-step bounds.")
    start, end = int(value[0]), int(value[1])
    if start > end:
        raise ExperimentProtocolError(f"{label} start exceeds end: {(start, end)}")
    return start, end


def load_experiment_plan(
    experiment_config_path: str | Path,
    runtime_config_path: str | Path,
) -> ExperimentPlan:
    """Load and strictly validate the frozen design plus prospective runtime lock."""

    experiment = _load_yaml(experiment_config_path)
    runtime = _load_yaml(runtime_config_path)

    experiment_id = str(experiment["experiment_id"])
    if runtime.get("experiment_id") != experiment_id:
        raise ExperimentProtocolError("Runtime configuration references a different experiment ID.")
    if experiment["primary_model"]["family"] != "xgboost":
        raise ExperimentProtocolError("MIZAN-GATE 0.1A primary model must remain XGBoost.")
    if experiment["primary_model"]["strategy"] != "fixed_parameters_across_feature_sets":
        raise ExperimentProtocolError("Primary model strategy no longer matches the frozen design.")

    seeds = tuple(
        int(value)
        for value in experiment["primary_model"]["seed_protocol"]["matched_seeds"]
    )
    if seeds != (11, 23, 42, 71, 101):
        raise ExperimentProtocolError(f"Matched seed protocol changed unexpectedly: {seeds}")
    aggregation = experiment["primary_model"]["seed_protocol"]["primary_aggregation"]
    if aggregation != "mean_predicted_probability_across_seeds_before_metric_calculation":
        raise ExperimentProtocolError("Seed aggregation no longer matches the preregistration.")

    registered_pairs = tuple(
        tuple(str(item) for item in pair) for pair in experiment["feature_sets"]["primary_pairs"]
    )
    if registered_pairs != (
        ("local", "local_plus_topology"),
        ("full_supplied", "full_plus_topology"),
    ):
        raise ExperimentProtocolError(f"Primary feature-set pairs changed: {registered_pairs}")
    registered_secondary = tuple(
        str(value) for value in experiment["feature_sets"]["secondary_sets"]
    )
    if registered_secondary != SECONDARY_FEATURE_SETS:
        raise ExperimentProtocolError(f"Secondary feature sets changed: {registered_secondary}")

    development_windows: list[TemporalWindow] = []
    for index, fold in enumerate(experiment["splits"]["development"]["expanding_folds"], start=1):
        train_start, train_end = _pair_to_bounds(fold["train"], f"development fold {index} train")
        eval_start, eval_end = _pair_to_bounds(
            fold["validation"], f"development fold {index} validation"
        )
        if train_end >= eval_start:
            raise ExperimentProtocolError(f"Development fold {index} violates temporal ordering.")
        development_windows.append(
            TemporalWindow(
                name=f"development_fold_{index}",
                role="development_descriptive",
                train_start=train_start,
                train_end=train_end,
                evaluation_start=eval_start,
                evaluation_end=eval_end,
            )
        )

    extension_start, extension_end = _pair_to_bounds(
        experiment["splits"]["extension_window"]["time_steps"], "extension window"
    )
    historical_start, historical_end = _pair_to_bounds(
        experiment["splits"]["historical_known_holdout"]["time_steps"],
        "historical window",
    )
    extension_window = TemporalWindow(
        name="extension_31_40",
        role="locked_temporal_extension",
        train_start=1,
        train_end=30,
        evaluation_start=extension_start,
        evaluation_end=extension_end,
    )
    historical_window = TemporalWindow(
        name="historical_41_49",
        role="historical_known_secondary_extension",
        train_start=1,
        train_end=30,
        evaluation_start=historical_start,
        evaluation_end=historical_end,
    )
    if (extension_start, extension_end) != (31, 40):
        raise ExperimentProtocolError("Extension window must remain time steps 31-40.")
    if (historical_start, historical_end) != (41, 49):
        raise ExperimentProtocolError("Historical window must remain time steps 41-49.")

    budgets = tuple(float(value) for value in experiment["metrics"]["alert_budgets"])
    if budgets != (0.01, 0.05, 0.1, 0.2):
        raise ExperimentProtocolError(f"Alert budgets changed unexpectedly: {budgets}")

    runtime_xgb = dict(runtime["xgboost"])
    expected_runtime = {
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "tree_method": "hist",
        "n_jobs": 1,
    }
    if runtime_xgb != expected_runtime:
        raise ExperimentProtocolError(
            f"XGBoost runtime lock mismatch: expected {expected_runtime}, observed {runtime_xgb}"
        )

    bootstrap = experiment["bootstrap"]
    runtime_bootstrap = runtime["bootstrap"]
    if runtime_bootstrap["interval_method"] != "percentile":
        raise ExperimentProtocolError(
            "Only the prospectively locked percentile bootstrap is allowed."
        )

    return ExperimentPlan(
        experiment_id=experiment_id,
        implementation_id=str(runtime["implementation_id"]),
        seeds=seeds,
        model_parameters=dict(experiment["primary_model"]["parameters"]),
        xgboost_runtime=runtime_xgb,
        development_windows=tuple(development_windows),
        extension_window=extension_window,
        historical_window=historical_window,
        alert_budgets=budgets,
        practical_margin=float(experiment["practical_margin_pr_auc"]),
        bootstrap_observation_repetitions=int(bootstrap["observation_level_repetitions"]),
        bootstrap_time_step_repetitions=int(bootstrap["time_step_block_repetitions"]),
        bootstrap_seed=int(runtime_bootstrap["random_seed"]),
        bootstrap_alpha=float(runtime_bootstrap["alpha"]),
        bootstrap_maximum_attempt_multiplier=int(runtime_bootstrap["maximum_attempt_multiplier"]),
        feature_manifest_sha256=str(experiment["feature_manifest_sha256"]),
        real_execution_python=str(runtime["real_execution_python"]),
        real_execution_versions={
            str(key): str(value) for key, value in runtime["real_execution_versions"].items()
        },
    )


def plan_as_dict(plan: ExperimentPlan) -> dict[str, Any]:
    def window_payload(window: TemporalWindow) -> dict[str, Any]:
        return {
            "name": window.name,
            "role": window.role,
            "train": [window.train_start, window.train_end],
            "evaluate": [window.evaluation_start, window.evaluation_end],
        }

    return {
        "experiment_id": plan.experiment_id,
        "implementation_id": plan.implementation_id,
        "seeds": list(plan.seeds),
        "primary_feature_sets": list(PRIMARY_FEATURE_SETS),
        "secondary_feature_sets": list(SECONDARY_FEATURE_SETS),
        "model_parameters": plan.model_parameters,
        "xgboost_runtime": plan.xgboost_runtime,
        "development_windows": [window_payload(value) for value in plan.development_windows],
        "extension_window": window_payload(plan.extension_window),
        "historical_window": window_payload(plan.historical_window),
        "alert_budgets": list(plan.alert_budgets),
        "practical_margin": plan.practical_margin,
        "bootstrap": {
            "observation_repetitions": plan.bootstrap_observation_repetitions,
            "time_step_repetitions": plan.bootstrap_time_step_repetitions,
            "random_seed": plan.bootstrap_seed,
            "alpha": plan.bootstrap_alpha,
        },
        "feature_manifest_sha256": plan.feature_manifest_sha256,
        "real_execution_python": plan.real_execution_python,
        "real_execution_versions": plan.real_execution_versions,
    }


def class_ratio(target: pd.Series | np.ndarray) -> float:
    values = np.asarray(target)
    positives = int(np.count_nonzero(values == 1))
    negatives = int(np.count_nonzero(values == 0))
    if positives == 0 or negatives == 0:
        raise ExperimentProtocolError("Training target must contain both labeled classes.")
    return negatives / positives


def make_xgboost_model(
    parameters: dict[str, Any],
    seed: int,
    n_jobs: int,
    target: pd.Series,
) -> XGBClassifier:
    return XGBClassifier(
        **parameters,
        objective="binary:logistic",
        eval_metric="logloss",
        tree_method="hist",
        random_state=seed,
        n_jobs=n_jobs,
        scale_pos_weight=class_ratio(target),
        missing=np.nan,
    )


def _slice_time(frame: pd.DataFrame, start: int, end: int) -> pd.DataFrame:
    result = frame.loc[frame["time_step"].between(start, end)].copy()
    if result.empty:
        raise ExperimentProtocolError(f"Empty temporal slice {start}-{end}.")
    if result["label"].nunique() < 2:
        raise ExperimentProtocolError(f"Temporal slice {start}-{end} contains only one class.")
    return result


def _validate_feature_columns(
    frame: pd.DataFrame, columns: Sequence[str], feature_set: str
) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ExperimentProtocolError(
            f"Feature set {feature_set} has columns absent from the analysis frame: {missing}"
        )
    values = frame.loc[:, list(columns)].to_numpy(dtype=np.float64, copy=False)
    if not np.isfinite(values).all():
        raise ExperimentProtocolError(f"Feature set {feature_set} contains non-finite predictors.")


def fit_predict_mean_across_seeds(
    train: pd.DataFrame,
    evaluations: Mapping[str, pd.DataFrame],
    features: Sequence[str],
    *,
    feature_set: str,
    parameters: dict[str, Any],
    seeds: Sequence[int],
    n_jobs: int,
    model_factory: ModelFactory = make_xgboost_model,
) -> tuple[dict[str, np.ndarray], pd.DataFrame]:
    """Fit matched technical seeds and average probabilities observation-wise."""

    _validate_feature_columns(train, features, feature_set)
    for frame in evaluations.values():
        _validate_feature_columns(frame, features, feature_set)

    train_x = train.loc[:, list(features)]
    target = train["label"]
    prediction_sums = {
        name: np.zeros(len(frame), dtype=np.float64) for name, frame in evaluations.items()
    }
    seed_metric_rows: list[dict[str, Any]] = []

    for seed in seeds:
        model = model_factory(parameters, int(seed), int(n_jobs), target)
        model.fit(train_x, target)
        for window_name, evaluation in evaluations.items():
            scores = np.asarray(
                model.predict_proba(evaluation.loc[:, list(features)])[:, 1], dtype=np.float64
            )
            if scores.shape != (len(evaluation),):
                raise ExperimentProtocolError("Model returned an unexpected prediction shape.")
            if not np.isfinite(scores).all() or ((scores < 0) | (scores > 1)).any():
                raise ExperimentProtocolError("Model returned invalid probabilities.")
            prediction_sums[window_name] += scores
            seed_metric_rows.append(
                {
                    "window": window_name,
                    "feature_set": feature_set,
                    "seed": int(seed),
                    "pr_auc": float(average_precision_score(evaluation["label"], scores)),
                    "roc_auc": float(roc_auc_score(evaluation["label"], scores)),
                }
            )

    divisor = float(len(seeds))
    means = {name: values / divisor for name, values in prediction_sums.items()}
    return means, pd.DataFrame(seed_metric_rows)


def discrimination_metrics(
    target: pd.Series | np.ndarray, scores: np.ndarray
) -> dict[str, float | int]:
    y = np.asarray(target)
    probabilities = np.asarray(scores, dtype=np.float64)
    return {
        "rows": len(y),
        "licit": int(np.count_nonzero(y == 0)),
        "illicit": int(np.count_nonzero(y == 1)),
        "prevalence": float(np.mean(y)),
        "pr_auc": float(average_precision_score(y, probabilities)),
        "roc_auc": float(roc_auc_score(y, probabilities)),
    }


def alert_budget_metrics(
    txid: pd.Series | np.ndarray,
    target: pd.Series | np.ndarray,
    scores: np.ndarray,
    budget: float,
) -> dict[str, float | int]:
    if not 0 < budget <= 1:
        raise ExperimentProtocolError("Alert budget must be in (0, 1].")
    ranked = pd.DataFrame(
        {
            "txId": np.asarray(txid),
            "label": np.asarray(target, dtype=np.int8),
            "score": np.asarray(scores, dtype=np.float64),
        }
    ).sort_values(["score", "txId"], ascending=[False, True], kind="mergesort")
    alerts = max(1, math.ceil(len(ranked) * budget))
    selected = ranked.iloc[:alerts]
    positives = int(ranked["label"].sum())
    true_positives = int(selected["label"].sum())
    precision = true_positives / alerts
    recall = true_positives / positives if positives else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "budget": float(budget),
        "alerts": int(alerts),
        "true_positives": true_positives,
        "false_positives": int(alerts - true_positives),
        "false_negatives": int(positives - true_positives),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
    }


def estimands_from_metric_map(metric_map: Mapping[str, float]) -> dict[str, float]:
    required = set(PRIMARY_FEATURE_SETS)
    missing = sorted(required - set(metric_map))
    if missing:
        raise ExperimentProtocolError(f"Missing primary feature-set metrics: {missing}")
    local = float(metric_map["local"])
    local_topology = float(metric_map["local_plus_topology"])
    full = float(metric_map["full_supplied"])
    full_topology = float(metric_map["full_plus_topology"])
    delta_local = local_topology - local
    delta_full = full_topology - full
    return {
        "m_local": local,
        "m_local_plus_topology": local_topology,
        "m_full_supplied": full,
        "m_full_plus_topology": full_topology,
        "delta_local": delta_local,
        "delta_full": delta_full,
        "redundancy_contrast": delta_local - delta_full,
        "full_minus_local": full - local,
    }


def _primary_prediction_wide(predictions: pd.DataFrame) -> pd.DataFrame:
    primary = predictions.loc[predictions["feature_set"].isin(PRIMARY_FEATURE_SETS)].copy()
    identity = ["txId", "time_step", "label"]
    for feature_set in PRIMARY_FEATURE_SETS:
        subset = primary.loc[primary["feature_set"].eq(feature_set), identity + ["mean_score"]]
        if subset.duplicated(identity).any():
            raise ExperimentProtocolError(f"Duplicate predictions for feature set {feature_set}.")
    wide = primary.pivot(index=identity, columns="feature_set", values="mean_score").reset_index()
    missing = sorted(set(PRIMARY_FEATURE_SETS) - set(wide.columns))
    if missing:
        raise ExperimentProtocolError(f"Primary prediction matrix is incomplete: {missing}")
    return wide


def _contrast_values(frame: pd.DataFrame) -> dict[str, float]:
    metrics = {
        feature_set: float(average_precision_score(frame["label"], frame[feature_set]))
        for feature_set in PRIMARY_FEATURE_SETS
    }
    return estimands_from_metric_map(metrics)


def _resampled_frame(
    wide: pd.DataFrame,
    rng: np.random.Generator,
    method: str,
) -> pd.DataFrame:
    if method == "observation":
        sampled = rng.integers(0, len(wide), size=len(wide))
        return wide.iloc[sampled].reset_index(drop=True)
    if method == "time_step_block":
        blocks = np.array(
            sorted(int(value) for value in wide["time_step"].unique()), dtype=np.int64
        )
        sampled_blocks = rng.choice(blocks, size=len(blocks), replace=True)
        pieces = [wide.loc[wide["time_step"].eq(int(block))] for block in sampled_blocks]
        return pd.concat(pieces, ignore_index=True)
    raise ExperimentProtocolError(f"Unknown bootstrap method: {method}")


def classify_interval(lower: float, upper: float, margin: float) -> str:
    if lower > margin:
        return "helpful"
    if upper < -margin:
        return "harmful"
    if lower >= -margin and upper <= margin:
        return "practically_neutral"
    return "uncertain"


def paired_bootstrap_intervals(
    predictions: pd.DataFrame,
    *,
    repetitions: int,
    random_seed: int,
    method: str,
    alpha: float,
    practical_margin: float,
    maximum_attempt_multiplier: int = 20,
) -> pd.DataFrame:
    """Bootstrap paired PR-AUC contrasts from seed-averaged predictions."""

    if repetitions <= 0:
        raise ExperimentProtocolError("Bootstrap repetitions must be positive.")
    if not 0 < alpha < 1:
        raise ExperimentProtocolError("Bootstrap alpha must be in (0, 1).")
    wide = _primary_prediction_wide(predictions)
    point = _contrast_values(wide)
    contrast_names = ("delta_local", "delta_full", "redundancy_contrast", "full_minus_local")
    draws: dict[str, list[float]] = {name: [] for name in contrast_names}
    rng = np.random.default_rng(random_seed)
    attempts = 0
    maximum_attempts = repetitions * maximum_attempt_multiplier

    while len(draws["redundancy_contrast"]) < repetitions and attempts < maximum_attempts:
        attempts += 1
        sample = _resampled_frame(wide, rng, method)
        if sample["label"].nunique() < 2:
            continue
        values = _contrast_values(sample)
        for name in contrast_names:
            draws[name].append(values[name])

    if len(draws["redundancy_contrast"]) != repetitions:
        raise ExperimentProtocolError(
            f"Could not obtain {repetitions} valid bootstrap samples after {attempts} attempts."
        )

    rows: list[dict[str, Any]] = []
    for name in contrast_names:
        values = np.asarray(draws[name], dtype=np.float64)
        lower = float(np.quantile(values, alpha / 2))
        upper = float(np.quantile(values, 1 - alpha / 2))
        classification = "not_applicable"
        if name in {"delta_local", "delta_full", "redundancy_contrast"}:
            classification = classify_interval(lower, upper, practical_margin)
        rows.append(
            {
                "contrast": name,
                "method": method,
                "estimate": float(point[name]),
                "lower": lower,
                "upper": upper,
                "confidence_level": float(1 - alpha),
                "repetitions": int(repetitions),
                "random_seed": int(random_seed),
                "classification": classification,
            }
        )
    return pd.DataFrame(rows)


def _prediction_frame(
    evaluation: pd.DataFrame,
    scores: np.ndarray,
    *,
    window: TemporalWindow,
    feature_set: str,
) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "txId": evaluation["txId"].to_numpy(),
            "time_step": evaluation["time_step"].to_numpy(),
            "label": evaluation["label"].to_numpy(),
            "window": window.name,
            "window_role": window.role,
            "train_start": window.train_start,
            "train_end": window.train_end,
            "evaluation_start": window.evaluation_start,
            "evaluation_end": window.evaluation_end,
            "feature_set": feature_set,
            "mean_score": scores,
        }
    )


def _evaluate_prediction_group(
    frame: pd.DataFrame,
    budgets: Sequence[float],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    metric = discrimination_metrics(frame["label"], frame["mean_score"].to_numpy())
    alert_rows: list[dict[str, Any]] = []
    for budget in budgets:
        alert_rows.append(
            {
                **alert_budget_metrics(
                    frame["txId"], frame["label"], frame["mean_score"].to_numpy(), budget
                ),
            }
        )
    return metric, alert_rows


def _fit_windows(
    analysis: pd.DataFrame,
    manifest: FeatureManifest,
    plan: ExperimentPlan,
    windows: Sequence[TemporalWindow],
    feature_sets: Sequence[str],
    *,
    model_factory: ModelFactory = make_xgboost_model,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    prediction_frames: list[pd.DataFrame] = []
    seed_metric_frames: list[pd.DataFrame] = []

    grouped_by_training: dict[tuple[int, int], list[TemporalWindow]] = {}
    for window in windows:
        grouped_by_training.setdefault((window.train_start, window.train_end), []).append(window)

    for (train_start, train_end), training_windows in grouped_by_training.items():
        train = _slice_time(analysis, train_start, train_end)
        evaluations = {
            window.name: _slice_time(analysis, window.evaluation_start, window.evaluation_end)
            for window in training_windows
        }
        for feature_set in feature_sets:
            columns = manifest.feature_set(feature_set).features
            means, seed_metrics = fit_predict_mean_across_seeds(
                train,
                evaluations,
                columns,
                feature_set=feature_set,
                parameters=plan.model_parameters,
                seeds=plan.seeds,
                n_jobs=int(plan.xgboost_runtime["n_jobs"]),
                model_factory=model_factory,
            )
            for window in training_windows:
                prediction_frames.append(
                    _prediction_frame(
                        evaluations[window.name],
                        means[window.name],
                        window=window,
                        feature_set=feature_set,
                    )
                )
            seed_metric_frames.append(seed_metrics)

    return (
        pd.concat(prediction_frames, ignore_index=True),
        pd.concat(seed_metric_frames, ignore_index=True),
    )


def analyze_predictions(
    predictions: pd.DataFrame,
    seed_metrics: pd.DataFrame,
    plan: ExperimentPlan,
) -> dict[str, pd.DataFrame]:
    metric_rows: list[dict[str, Any]] = []
    alert_rows: list[dict[str, Any]] = []
    estimand_rows: list[dict[str, Any]] = []
    bootstrap_rows: list[pd.DataFrame] = []
    seed_estimand_rows: list[dict[str, Any]] = []

    for (window_name, seed), group in seed_metrics.groupby(["window", "seed"], sort=False):
        metric_map = dict(zip(group["feature_set"], group["pr_auc"], strict=True))
        if set(PRIMARY_FEATURE_SETS).issubset(metric_map):
            seed_estimand_rows.append(
                {
                    "window": window_name,
                    "seed": int(seed),
                    **estimands_from_metric_map(metric_map),
                }
            )

    for window_name, window_predictions in predictions.groupby("window", sort=False):
        metric_map: dict[str, float] = {}
        for feature_set, group in window_predictions.groupby("feature_set", sort=False):
            metric, alerts = _evaluate_prediction_group(group, plan.alert_budgets)
            metric_rows.append(
                {
                    "window": window_name,
                    "window_role": str(group["window_role"].iloc[0]),
                    "train_start": int(group["train_start"].iloc[0]),
                    "train_end": int(group["train_end"].iloc[0]),
                    "evaluation_start": int(group["evaluation_start"].iloc[0]),
                    "evaluation_end": int(group["evaluation_end"].iloc[0]),
                    "feature_set": feature_set,
                    **metric,
                }
            )
            metric_map[feature_set] = float(metric["pr_auc"])
            for alert in alerts:
                alert_rows.append(
                    {
                        "window": window_name,
                        "window_role": str(group["window_role"].iloc[0]),
                        "feature_set": feature_set,
                        **alert,
                    }
                )

        if set(PRIMARY_FEATURE_SETS).issubset(metric_map):
            estimand_rows.append({"window": window_name, **estimands_from_metric_map(metric_map)})

        role = str(window_predictions["window_role"].iloc[0])
        if role != "development_descriptive":
            primary_predictions = window_predictions.loc[
                window_predictions["feature_set"].isin(PRIMARY_FEATURE_SETS)
            ].copy()
            window_offset = 0 if window_name == plan.extension_window.name else 10_000
            block = paired_bootstrap_intervals(
                primary_predictions,
                repetitions=plan.bootstrap_time_step_repetitions,
                random_seed=plan.bootstrap_seed + window_offset,
                method="time_step_block",
                alpha=plan.bootstrap_alpha,
                practical_margin=plan.practical_margin,
                maximum_attempt_multiplier=plan.bootstrap_maximum_attempt_multiplier,
            )
            block.insert(0, "window", window_name)
            block.insert(1, "interval_role", "primary")
            bootstrap_rows.append(block)

            observation = paired_bootstrap_intervals(
                primary_predictions,
                repetitions=plan.bootstrap_observation_repetitions,
                random_seed=plan.bootstrap_seed + window_offset + 1,
                method="observation",
                alpha=plan.bootstrap_alpha,
                practical_margin=plan.practical_margin,
                maximum_attempt_multiplier=plan.bootstrap_maximum_attempt_multiplier,
            )
            observation.insert(0, "window", window_name)
            observation.insert(1, "interval_role", "sensitivity")
            bootstrap_rows.append(observation)

    return {
        "window_metrics": pd.DataFrame(metric_rows),
        "alert_budget_metrics": pd.DataFrame(alert_rows),
        "estimands": pd.DataFrame(estimand_rows),
        "bootstrap_intervals": pd.concat(bootstrap_rows, ignore_index=True)
        if bootstrap_rows
        else pd.DataFrame(),
        "seed_metrics": seed_metrics.copy(),
        "seed_estimands": pd.DataFrame(seed_estimand_rows),
    }


def validate_real_execution_environment(plan: ExperimentPlan) -> dict[str, str]:
    """Require the prospectively locked reference environment before real fitting."""

    observed = {
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "pyarrow": importlib_metadata.version("pyarrow"),
        "scipy": importlib_metadata.version("scipy"),
        "scikit_learn": sklearn.__version__,
        "xgboost": xgboost.__version__,
    }
    python_version = platform.python_version()
    if python_version != plan.real_execution_python:
        raise ExperimentProtocolError(
            "Real execution requires Python "
            f"{plan.real_execution_python}; observed {python_version}."
        )
    mismatches = {
        name: (plan.real_execution_versions.get(name), observed.get(name))
        for name in plan.real_execution_versions
        if observed.get(name) != plan.real_execution_versions.get(name)
    }
    if mismatches:
        raise ExperimentProtocolError(
            f"Real execution environment differs from the prospective lock: {mismatches}"
        )
    return {"python": python_version, **observed}


def _git_commit(repo_root: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def require_clean_git_state(repo_root: Path) -> str:
    commit = _git_commit(repo_root)
    if commit is None:
        raise ExperimentProtocolError("Real execution requires a Git-tracked MIZAN-GATE checkout.")
    try:
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ExperimentProtocolError("Could not verify MIZAN-GATE Git cleanliness.") from exc
    if status:
        raise ExperimentProtocolError(
            "Real execution requires a clean Git working tree so results map to committed code."
        )
    return commit


def _write_json(payload: dict[str, Any], path: Path) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run_experiment(
    *,
    study1_root: str | Path,
    experiment_config_path: str | Path,
    runtime_config_path: str | Path,
    feature_manifest_path: str | Path,
    data_contract_path: str | Path,
    output_dir: str | Path,
    overwrite: bool = False,
) -> dict[str, Any]:
    """Execute the registered real-data experiment and persist machine-readable outputs."""

    experiment_path = Path(experiment_config_path).expanduser().resolve()
    runtime_path = Path(runtime_config_path).expanduser().resolve()
    manifest_path = Path(feature_manifest_path).expanduser().resolve()
    contract_path = Path(data_contract_path).expanduser().resolve()
    output = Path(output_dir).expanduser().resolve()
    repo_root = experiment_path.parents[2]
    execution_commit = require_clean_git_state(repo_root)

    if output.exists() and any(output.iterdir()) and not overwrite:
        raise ExperimentProtocolError(
            f"Output directory is non-empty: {output}. Use overwrite only for an intentional rerun."
        )
    output.mkdir(parents=True, exist_ok=True)

    plan = load_experiment_plan(experiment_path, runtime_path)
    locked_software = validate_real_execution_environment(plan)
    manifest = load_feature_manifest(manifest_path, expected_sha256=plan.feature_manifest_sha256)
    data: EllipticStudy1Data = load_elliptic_study1(
        study1_root,
        data_contract_path=contract_path,
        feature_manifest_path=manifest_path,
        expected_feature_manifest_sha256=plan.feature_manifest_sha256,
        verify_artifact_hashes=True,
    )
    analysis = data.analysis_frame

    development_predictions, development_seed_metrics = _fit_windows(
        analysis,
        manifest,
        plan,
        plan.development_windows,
        ALL_REGISTERED_FEATURE_SETS,
    )
    later_predictions, later_seed_metrics = _fit_windows(
        analysis,
        manifest,
        plan,
        (plan.extension_window, plan.historical_window),
        ALL_REGISTERED_FEATURE_SETS,
    )
    predictions = pd.concat([development_predictions, later_predictions], ignore_index=True)
    seed_metrics = pd.concat([development_seed_metrics, later_seed_metrics], ignore_index=True)
    tables = analyze_predictions(predictions, seed_metrics, plan)

    predictions.to_parquet(output / "predictions.parquet", index=False)
    for name, frame in tables.items():
        frame.to_csv(output / f"{name}.csv", index=False)

    metadata = {
        "status": "success",
        "completed_utc": datetime.now(UTC).isoformat(),
        "experiment_id": plan.experiment_id,
        "implementation_id": plan.implementation_id,
        "mizan_gate_git_commit": execution_commit,
        "study1_source_commit": data.source_study_commit,
        "study1_contract_id": data.contract_id,
        "study1_artifact_sha256": data.artifact_sha256,
        "file_sha256": {
            "experiment_config": sha256_file(experiment_path),
            "runtime_config": sha256_file(runtime_path),
            "feature_manifest": sha256_file(manifest_path),
            "data_contract": sha256_file(contract_path),
        },
        "software": locked_software,
        "plan": plan_as_dict(plan),
        "interpretation_constraint": (
            "This runner computes registered estimates only. Scientific novelty and external "
            "validity require separate analysis and external comparison."
        ),
    }
    _write_json(metadata, output / "run_metadata.json")
    _write_json(plan_as_dict(plan), output / "resolved_plan.json")
    return metadata
