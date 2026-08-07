from __future__ import annotations

import argparse
import json
from pathlib import Path

from mizan_gate.experiments.elliptic_redundancy import load_experiment_plan, plan_as_dict
from mizan_gate.features.registry import load_feature_manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate MIZAN-GATE 0.1A implementation locks without fitting a model."
    )
    parser.add_argument(
        "--experiment-config",
        default="configs/experiments/elliptic_redundancy_v0_1.yaml",
    )
    parser.add_argument(
        "--runtime-config",
        default="configs/implementation/elliptic_redundancy_v0_1_runtime.yaml",
    )
    parser.add_argument("--feature-manifest", default="manifests/features/elliptic_v1.yaml")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    plan = load_experiment_plan(args.experiment_config, args.runtime_config)
    manifest = load_feature_manifest(
        Path(args.feature_manifest), expected_sha256=plan.feature_manifest_sha256
    )
    payload = plan_as_dict(plan)
    payload["manifest_id"] = manifest.manifest_id
    payload["status"] = "PASS"
    payload["real_models_fitted"] = False
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
