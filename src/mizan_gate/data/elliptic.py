"""Read-only adapter for the independently reproduced Elliptic Study 1 artifacts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from mizan_gate.features.registry import FeatureManifest, load_feature_manifest


class DataContractError(ValueError):
    """Raised when Study 1 artifacts violate the registered MIZAN-GATE contract."""


@dataclass(frozen=True)
class EllipticStudy1Data:
    """Validated, analysis-ready Elliptic tables sourced from frozen Study 1."""

    labeled_features: pd.DataFrame
    graph_features: pd.DataFrame
    node_index: pd.DataFrame
    analysis_frame: pd.DataFrame
    contract_id: str
    source_study_commit: str
    artifact_sha256: dict[str, str]


def sha256_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _load_yaml(path: Path) -> dict[str, Any]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise DataContractError(f"YAML root must be a mapping: {path}")
    return raw


def _require_columns(frame: pd.DataFrame, expected: tuple[str, ...], name: str) -> None:
    observed = tuple(str(column) for column in frame.columns)
    if observed != expected:
        raise DataContractError(
            f"{name} column contract mismatch. Expected {len(expected)} ordered columns, "
            f"observed {len(observed)}."
        )
    if frame.columns.duplicated().any():
        raise DataContractError(f"{name} contains duplicate column names.")


def _require_unique_txid(frame: pd.DataFrame, name: str) -> None:
    if frame["txId"].isna().any():
        raise DataContractError(f"{name}.txId contains missing values.")
    duplicate_count = int(frame["txId"].duplicated().sum())
    if duplicate_count:
        raise DataContractError(f"{name} contains {duplicate_count} duplicate txId values.")


def _require_finite(frame: pd.DataFrame, columns: tuple[str, ...], name: str) -> None:
    values = frame.loc[:, list(columns)].to_numpy(dtype=np.float64, copy=False)
    if not np.isfinite(values).all():
        raise DataContractError(f"{name} contains NaN or infinite values in registered predictors.")


def _validate_frames(
    labeled: pd.DataFrame,
    graph: pd.DataFrame,
    node: pd.DataFrame,
    feature_manifest: FeatureManifest,
    contract: dict[str, Any],
) -> pd.DataFrame:
    local = feature_manifest.family("local_supplied").features
    aggregate = feature_manifest.family("one_hop_aggregated").features
    supplied = local + aggregate
    topology = feature_manifest.family("completed_topology").features

    expected_labeled = ("txId", "time_step", *supplied, "label")
    expected_graph = (
        "txId",
        "time_step",
        "in_degree",
        "out_degree",
        "total_degree",
        "pagerank_raw_snapshot",
        "pagerank_relative",
        "clustering",
        "k_core",
        "weak_component_size",
    )
    expected_node = ("txId", "time_step")

    _require_columns(labeled, expected_labeled, "labeled_features")
    _require_columns(graph, expected_graph, "graph_features")
    _require_columns(node, expected_node, "node_index")

    _require_unique_txid(labeled, "labeled_features")
    _require_unique_txid(graph, "graph_features")
    _require_unique_txid(node, "node_index")

    semantic = contract["semantic_contract"]
    if len(labeled) != int(semantic["labeled_rows"]):
        raise DataContractError(
            f"labeled_features row count mismatch: {len(labeled)} != {semantic['labeled_rows']}"
        )
    if len(graph) != int(semantic["all_nodes"]) or len(node) != int(semantic["all_nodes"]):
        raise DataContractError("All-node graph and node-index counts do not match the contract.")

    minimum = int(semantic["time_steps"]["minimum"])
    maximum = int(semantic["time_steps"]["maximum"])
    for name, frame in (("labeled_features", labeled), ("graph_features", graph), ("node_index", node)):
        observed_min = int(frame["time_step"].min())
        observed_max = int(frame["time_step"].max())
        if (observed_min, observed_max) != (minimum, maximum):
            raise DataContractError(
                f"{name} time-step range {(observed_min, observed_max)} != {(minimum, maximum)}"
            )

    observed_labels = {int(value) for value in labeled["label"].unique()}
    expected_labels = {int(value) for value in semantic["label_values"]}
    if observed_labels != expected_labels:
        raise DataContractError(
            f"Observed label values {sorted(observed_labels)} != {sorted(expected_labels)}"
        )

    node_sorted = node.sort_values("txId", kind="mergesort").reset_index(drop=True)
    graph_index = graph.loc[:, ["txId", "time_step"]].sort_values(
        "txId", kind="mergesort"
    ).reset_index(drop=True)
    if not node_sorted.equals(graph_index):
        raise DataContractError("graph_features and node_index do not have identical txId/time_step pairs.")

    labeled_membership = labeled.loc[:, ["txId", "time_step"]].merge(
        node,
        on=["txId", "time_step"],
        how="left",
        validate="one_to_one",
        indicator=True,
    )
    if not (labeled_membership["_merge"] == "both").all():
        raise DataContractError("At least one labeled transaction is absent from node_index.")

    if not np.array_equal(
        graph["total_degree"].to_numpy(),
        (graph["in_degree"] + graph["out_degree"]).to_numpy(),
    ):
        raise DataContractError("total_degree is not exactly in_degree + out_degree.")

    if (graph["pagerank_relative"] < 0).any():
        raise DataContractError("pagerank_relative contains negative values.")
    if ((graph["clustering"] < 0) | (graph["clustering"] > 1)).any():
        raise DataContractError("clustering falls outside [0, 1].")
    if (graph["k_core"] < 0).any():
        raise DataContractError("k_core contains negative values.")
    if (graph["weak_component_size"] < 1).any():
        raise DataContractError("weak_component_size must be positive.")

    _require_finite(labeled, supplied, "labeled_features")
    _require_finite(graph, topology, "graph_features")

    topology_frame = graph.loc[:, ["txId", "time_step", *topology]]
    analysis = labeled.merge(
        topology_frame,
        on=["txId", "time_step"],
        how="left",
        validate="one_to_one",
    )
    if len(analysis) != len(labeled):
        raise DataContractError("Topology merge changed the number of labeled rows.")
    if analysis.loc[:, list(topology)].isna().any().any():
        raise DataContractError("Topology merge produced missing registered topology values.")

    expected_analysis = ("txId", "time_step", *supplied, "label", *topology)
    if tuple(analysis.columns) != expected_analysis:
        raise DataContractError("Analysis-frame column ordering is not deterministic.")

    return analysis


def load_elliptic_study1(
    study1_root: str | Path,
    *,
    data_contract_path: str | Path,
    feature_manifest_path: str | Path,
    expected_feature_manifest_sha256: str,
    verify_artifact_hashes: bool = True,
) -> EllipticStudy1Data:
    """Load and validate frozen Study 1 outputs without modifying them."""

    root = Path(study1_root).expanduser().resolve()
    contract_path = Path(data_contract_path).expanduser().resolve()
    manifest_path = Path(feature_manifest_path).expanduser().resolve()

    if not root.is_dir():
        raise DataContractError(f"Study 1 root does not exist: {root}")

    contract = _load_yaml(contract_path)
    feature_manifest = load_feature_manifest(
        manifest_path,
        expected_sha256=expected_feature_manifest_sha256,
    )

    source_commit = str(contract["source_study"]["commit"])
    if source_commit != feature_manifest.source_study_commit:
        raise DataContractError(
            "Study 1 data contract and feature manifest reference different source commits."
        )

    frames: dict[str, pd.DataFrame] = {}
    artifact_hashes: dict[str, str] = {}
    for name, spec in contract["processed_artifacts"].items():
        artifact_path = root / str(spec["relative_path"])
        if not artifact_path.is_file():
            raise DataContractError(f"Missing Study 1 artifact: {artifact_path}")

        observed_hash = sha256_file(artifact_path)
        artifact_hashes[name] = observed_hash
        if verify_artifact_hashes and observed_hash != str(spec["sha256"]).lower():
            raise DataContractError(
                f"Artifact hash mismatch for {name}: expected {spec['sha256']}, observed {observed_hash}"
            )

        frame = pd.read_parquet(artifact_path)
        expected_shape = (int(spec["rows"]), int(spec["columns"]))
        if frame.shape != expected_shape:
            raise DataContractError(
                f"Artifact shape mismatch for {name}: expected {expected_shape}, observed {frame.shape}"
            )
        frames[name] = frame

    analysis = _validate_frames(
        frames["labeled_features"],
        frames["graph_features"],
        frames["node_index"],
        feature_manifest,
        contract,
    )

    return EllipticStudy1Data(
        labeled_features=frames["labeled_features"],
        graph_features=frames["graph_features"],
        node_index=frames["node_index"],
        analysis_frame=analysis,
        contract_id=str(contract["contract_id"]),
        source_study_commit=source_commit,
        artifact_sha256=artifact_hashes,
    )

