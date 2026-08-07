from __future__ import annotations

import argparse
import json
from pathlib import Path

from mizan_gate.experiments.elliptic_redundancy import run_experiment


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run registered MIZAN-GATE 0.1A on verified Study 1 data."
    )
    parser.add_argument("--study1-root", required=True)
    parser.add_argument(
        "--experiment-config",
        default="configs/experiments/elliptic_redundancy_v0_1.yaml",
    )
    parser.add_argument(
        "--runtime-config",
        default="configs/implementation/elliptic_redundancy_v0_1_runtime.yaml",
    )
    parser.add_argument("--feature-manifest", default="manifests/features/elliptic_v1.yaml")
    parser.add_argument(
        "--data-contract",
        default="manifests/data/elliptic_study1_replication_v1.yaml",
    )
    parser.add_argument("--output-dir", default="results/elliptic_redundancy_v0_1")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metadata = run_experiment(
        study1_root=Path(args.study1_root),
        experiment_config_path=Path(args.experiment_config),
        runtime_config_path=Path(args.runtime_config),
        feature_manifest_path=Path(args.feature_manifest),
        data_contract_path=Path(args.data_contract),
        output_dir=Path(args.output_dir),
        overwrite=args.overwrite,
    )
    print(json.dumps(metadata, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
