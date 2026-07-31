from pathlib import Path

import pytest
import yaml

from mizan_gate.features.registry import ManifestValidationError, load_feature_manifest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "features" / "elliptic_v1.yaml"
EXPERIMENT = ROOT / "configs" / "experiments" / "elliptic_redundancy_v0_1.yaml"
EXPECTED_SHA256 = "3574062ab2bdaddd3eb17e33f39355ad1158854b2a60678b236abbce159a2e8b"


def test_manifest_has_exact_registered_counts_and_order() -> None:
    manifest = load_feature_manifest(MANIFEST)
    assert manifest.family("local_supplied").features == tuple(
        f"feature_{index}" for index in range(1, 94)
    )
    assert manifest.family("one_hop_aggregated").features == tuple(
        f"feature_{index}" for index in range(94, 166)
    )
    assert manifest.family("completed_topology").features == (
        "in_degree",
        "out_degree",
        "pagerank_relative",
        "clustering",
        "k_core",
    )


def test_local_and_aggregate_partition_the_supplied_matrix() -> None:
    manifest = load_feature_manifest(MANIFEST)
    local = manifest.family("local_supplied").features
    aggregate = manifest.family("one_hop_aggregated").features
    assert len(local) == 93
    assert len(aggregate) == 72
    assert set(local).isdisjoint(aggregate)
    assert manifest.feature_set("full_supplied").features == local + aggregate
    assert len(manifest.feature_set("full_supplied").features) == 165


def test_preregistered_feature_set_counts_and_composition() -> None:
    manifest = load_feature_manifest(MANIFEST)
    expected = {
        "local": (93, ("local_supplied",)),
        "aggregate": (72, ("one_hop_aggregated",)),
        "full_supplied": (165, ("local_supplied", "one_hop_aggregated")),
        "topology_completed": (5, ("completed_topology",)),
        "local_plus_topology": (98, ("local_supplied", "completed_topology")),
        "aggregate_plus_topology": (77, ("one_hop_aggregated", "completed_topology")),
        "full_plus_topology": (
            170,
            ("local_supplied", "one_hop_aggregated", "completed_topology"),
        ),
    }
    for name, (count, families) in expected.items():
        assert len(manifest.feature_set(name).features) == count
        assert manifest.feature_set(name).families == families


def test_forbidden_variables_are_absent_from_every_set() -> None:
    manifest = load_feature_manifest(MANIFEST)
    for feature_set in manifest.sets.values():
        assert manifest.forbidden_predictors.isdisjoint(feature_set.features)


def test_manifest_hash_is_frozen_and_pinned_by_experiment() -> None:
    experiment = yaml.safe_load(EXPERIMENT.read_text(encoding="utf-8"))
    assert experiment["feature_manifest_sha256"] == EXPECTED_SHA256
    manifest = load_feature_manifest(MANIFEST, expected_sha256=EXPECTED_SHA256)
    assert manifest.manifest_sha256 == EXPECTED_SHA256


def test_hash_mismatch_is_rejected(tmp_path: Path) -> None:
    text = MANIFEST.read_text(encoding="utf-8").replace(
        "Feature names are positional", "Predictor names are positional", 1
    )
    changed = tmp_path / "changed.yaml"
    changed.write_text(text, encoding="utf-8")
    with pytest.raises(ManifestValidationError, match="hash mismatch"):
        load_feature_manifest(changed, expected_sha256=EXPECTED_SHA256)


def test_unknown_family_is_rejected() -> None:
    manifest = load_feature_manifest(MANIFEST)
    with pytest.raises(KeyError):
        manifest.family("invented_after_results")


def test_duplicate_features_are_rejected(tmp_path: Path) -> None:
    text = MANIFEST.read_text(encoding="utf-8").replace("  - feature_2\n", "  - feature_1\n", 1)
    invalid = tmp_path / "invalid.yaml"
    invalid.write_text(text, encoding="utf-8")
    with pytest.raises(ManifestValidationError):
        load_feature_manifest(invalid)


def test_extra_family_requires_new_manifest_version(tmp_path: Path) -> None:
    raw = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    raw["families"]["post_hoc_family"] = {
        "role": "Invalid post-hoc family",
        "availability": "unknown",
        "expected_count": 1,
        "features": ["feature_999"],
    }
    invalid = tmp_path / "extra_family.yaml"
    invalid.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    with pytest.raises(ManifestValidationError, match="New families require a new manifest version"):
        load_feature_manifest(invalid)


def test_extra_feature_set_requires_new_manifest_version(tmp_path: Path) -> None:
    raw = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    raw["feature_sets"]["post_hoc_set"] = {
        "families": ["local_supplied"],
        "expected_count": 93,
    }
    invalid = tmp_path / "extra_set.yaml"
    invalid.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    with pytest.raises(ManifestValidationError, match="New sets require a new manifest version"):
        load_feature_manifest(invalid)


def test_changed_topology_definition_is_rejected(tmp_path: Path) -> None:
    raw = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    raw["families"]["completed_topology"]["features"][-1] = "invented_topology"
    invalid = tmp_path / "changed_topology.yaml"
    invalid.write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    with pytest.raises(ManifestValidationError, match="completed topology"):
        load_feature_manifest(invalid)
