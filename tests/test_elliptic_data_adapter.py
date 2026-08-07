from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest
import yaml

from mizan_gate.data.elliptic import DataContractError, _validate_frames, sha256_file
from mizan_gate.features.registry import load_feature_manifest

ROOT = Path(__file__).resolve().parents[1]
FEATURE_MANIFEST = ROOT / "manifests" / "features" / "elliptic_v1.yaml"
DATA_CONTRACT = ROOT / "manifests" / "data" / "elliptic_study1_replication_v1.yaml"


def _mini_frames():
    manifest = load_feature_manifest(FEATURE_MANIFEST)
    supplied = (
        manifest.family("local_supplied").features
        + manifest.family("one_hop_aggregated").features
    )
    labeled_data = {"txId": [1, 2], "time_step": [1, 49]}
    for feature in supplied:
        labeled_data[feature] = [0.0, 1.0]
    labeled_data["label"] = [0, 1]
    labeled = pd.DataFrame(labeled_data)

    graph = pd.DataFrame(
        {
            "txId": [1, 2],
            "time_step": [1, 49],
            "in_degree": [0, 1],
            "out_degree": [1, 0],
            "total_degree": [1, 1],
            "pagerank_raw_snapshot": [0.5, 0.5],
            "pagerank_relative": [1.0, 1.0],
            "clustering": [0.0, 0.0],
            "k_core": [1, 1],
            "weak_component_size": [1, 1],
        }
    )
    node = graph.loc[:, ["txId", "time_step"]].copy()
    contract = yaml.safe_load(DATA_CONTRACT.read_text(encoding="utf-8"))
    contract["semantic_contract"]["labeled_rows"] = 2
    contract["semantic_contract"]["all_nodes"] = 2
    return manifest, contract, labeled, graph, node


def test_sha256_file(tmp_path: Path) -> None:
    path = tmp_path / "sample.bin"
    path.write_bytes(b"mizan-gate")
    assert sha256_file(path) == "11334dea447776383572f86b8fa2424dbb2f35d4cb30200953edde7d461947ac"


def test_validate_frames_builds_analysis_frame() -> None:
    manifest, contract, labeled, graph, node = _mini_frames()
    analysis = _validate_frames(labeled, graph, node, manifest, contract)
    assert analysis.shape == (2, 173)
    assert analysis["txId"].tolist() == [1, 2]
    assert analysis["in_degree"].tolist() == [0, 1]


def test_validate_frames_rejects_duplicate_txid() -> None:
    manifest, contract, labeled, graph, node = _mini_frames()
    labeled.loc[1, "txId"] = 1
    with pytest.raises(DataContractError, match="duplicate txId"):
        _validate_frames(labeled, graph, node, manifest, contract)


def test_validate_frames_rejects_wrong_total_degree() -> None:
    manifest, contract, labeled, graph, node = _mini_frames()
    graph.loc[0, "total_degree"] = 999
    with pytest.raises(DataContractError, match="total_degree"):
        _validate_frames(labeled, graph, node, manifest, contract)


def test_validate_frames_rejects_node_graph_mismatch() -> None:
    manifest, contract, labeled, graph, node = _mini_frames()
    node.loc[0, "time_step"] = 49
    node.loc[1, "time_step"] = 1
    with pytest.raises(DataContractError, match="identical txId/time_step"):
        _validate_frames(labeled, graph, node, manifest, contract)
