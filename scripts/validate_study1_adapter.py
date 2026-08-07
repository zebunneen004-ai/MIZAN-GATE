from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from mizan_gate.data.elliptic import load_elliptic_study1

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT = ROOT / "manifests" / "data" / "elliptic_study1_replication_v1.yaml"
DEFAULT_FEATURE_MANIFEST = ROOT / "manifests" / "features" / "elliptic_v1.yaml"
DEFAULT_EXPERIMENT = ROOT / "configs" / "experiments" / "elliptic_redundancy_v0_1.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate MIZAN-GATE's read-only adapter against reproduced Study 1 artifacts."
    )
    parser.add_argument("--study1-root", required=True, type=Path)
    parser.add_argument("--data-contract", default=DEFAULT_CONTRACT, type=Path)
    args = parser.parse_args()

    experiment = yaml.safe_load(DEFAULT_EXPERIMENT.read_text(encoding="utf-8"))
    data = load_elliptic_study1(
        args.study1_root,
        data_contract_path=args.data_contract,
        feature_manifest_path=DEFAULT_FEATURE_MANIFEST,
        expected_feature_manifest_sha256=str(experiment["feature_manifest_sha256"]),
    )

    result = {
        "status": "PASS",
        "contract_id": data.contract_id,
        "source_study_commit": data.source_study_commit,
        "artifact_sha256": data.artifact_sha256,
        "labeled_shape": list(data.labeled_features.shape),
        "graph_shape": list(data.graph_features.shape),
        "node_index_shape": list(data.node_index.shape),
        "analysis_shape": list(data.analysis_frame.shape),
        "analysis_duplicate_txid": int(data.analysis_frame["txId"].duplicated().sum()),
        "time_step_min": int(data.analysis_frame["time_step"].min()),
        "time_step_max": int(data.analysis_frame["time_step"].max()),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
