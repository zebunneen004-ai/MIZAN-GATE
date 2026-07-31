from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml

from mizan_gate.features.registry import load_feature_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENT = ROOT / "configs" / "experiments" / "elliptic_redundancy_v0_1.yaml"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the feature manifest pinned by a MIZAN-GATE experiment."
    )
    parser.add_argument(
        "--experiment-config",
        default=DEFAULT_EXPERIMENT,
        type=Path,
        help="Experiment YAML containing feature_manifest and feature_manifest_sha256.",
    )
    args = parser.parse_args()

    experiment_path = args.experiment_config.resolve()
    experiment = yaml.safe_load(experiment_path.read_text(encoding="utf-8"))
    manifest_path = ROOT / str(experiment["feature_manifest"])
    expected_sha256 = str(experiment["feature_manifest_sha256"])
    manifest = load_feature_manifest(manifest_path, expected_sha256=expected_sha256)

    record = manifest.as_provenance_record()
    record.update(
        {
            "experiment_id": str(experiment["experiment_id"]),
            "experiment_config": str(experiment_path.relative_to(ROOT)),
            "hash_lock_verified": True,
        }
    )
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
