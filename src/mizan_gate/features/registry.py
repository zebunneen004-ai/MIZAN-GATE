from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


class ManifestValidationError(ValueError):
    """Raised when a feature manifest violates a registered research invariant."""


@dataclass(frozen=True)
class FeatureFamily:
    name: str
    role: str
    availability: str
    features: tuple[str, ...]


@dataclass(frozen=True)
class FeatureSet:
    name: str
    families: tuple[str, ...]
    features: tuple[str, ...]


@dataclass(frozen=True)
class FeatureManifest:
    schema_version: str
    manifest_id: str
    dataset: str
    source_study_commit: str
    forbidden_predictors: frozenset[str]
    families: dict[str, FeatureFamily]
    sets: dict[str, FeatureSet]
    manifest_sha256: str

    def family(self, name: str) -> FeatureFamily:
        try:
            return self.families[name]
        except KeyError as exc:
            raise KeyError(f"Unknown feature family: {name}") from exc

    def feature_set(self, name: str) -> FeatureSet:
        try:
            return self.sets[name]
        except KeyError as exc:
            raise KeyError(f"Unknown feature set: {name}") from exc

    def require_sha256(self, expected_sha256: str) -> None:
        normalized = expected_sha256.strip().lower()
        if self.manifest_sha256 != normalized:
            raise ManifestValidationError(
                "Feature-manifest hash mismatch: "
                f"expected {normalized}, observed {self.manifest_sha256}."
            )

    def as_provenance_record(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "manifest_id": self.manifest_id,
            "dataset": self.dataset,
            "source_study_commit": self.source_study_commit,
            "manifest_sha256": self.manifest_sha256,
            "family_counts": {
                name: len(family.features) for name, family in self.families.items()
            },
            "set_counts": {
                name: len(feature_set.features) for name, feature_set in self.sets.items()
            },
        }


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicate_values: set[str] = set()
    for value in values:
        if value in seen:
            duplicate_values.add(value)
        seen.add(value)
    return sorted(duplicate_values)


def _canonical_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _parse_families(
    raw_families: dict[str, Any], forbidden: frozenset[str]
) -> dict[str, FeatureFamily]:
    families: dict[str, FeatureFamily] = {}
    for name, raw in raw_families.items():
        features = tuple(str(value) for value in raw["features"])
        duplicates = _duplicates(features)
        if duplicates:
            raise ManifestValidationError(f"Family {name} contains duplicate features: {duplicates}")
        overlap = forbidden.intersection(features)
        if overlap:
            raise ManifestValidationError(
                f"Family {name} contains forbidden predictors: {sorted(overlap)}"
            )
        expected_count = int(raw["expected_count"])
        if expected_count <= 0:
            raise ManifestValidationError(f"Family {name} has a non-positive expected count.")
        if len(features) != expected_count:
            raise ManifestValidationError(
                f"Family {name} expected {expected_count} features, observed {len(features)}"
            )
        families[name] = FeatureFamily(
            name=name,
            role=str(raw["role"]),
            availability=str(raw["availability"]),
            features=features,
        )
    return families


def _parse_sets(
    raw_sets: dict[str, Any], families: dict[str, FeatureFamily]
) -> dict[str, FeatureSet]:
    sets: dict[str, FeatureSet] = {}
    for name, raw in raw_sets.items():
        family_names = tuple(str(value) for value in raw["families"])
        if not family_names:
            raise ManifestValidationError(f"Feature set {name} contains no families.")
        missing = sorted(set(family_names) - set(families))
        if missing:
            raise ManifestValidationError(f"Feature set {name} references unknown families: {missing}")
        features = tuple(
            feature for family_name in family_names for feature in families[family_name].features
        )
        duplicates = _duplicates(features)
        if duplicates:
            raise ManifestValidationError(
                f"Feature set {name} has cross-family duplicate features: {duplicates}"
            )
        expected_count = int(raw["expected_count"])
        if expected_count <= 0:
            raise ManifestValidationError(f"Feature set {name} has a non-positive expected count.")
        if len(features) != expected_count:
            raise ManifestValidationError(
                f"Feature set {name} expected {expected_count} features, observed {len(features)}"
            )
        sets[name] = FeatureSet(name=name, families=family_names, features=features)
    return sets


def _validate_elliptic_v1_invariants(
    families: dict[str, FeatureFamily], sets: dict[str, FeatureSet]
) -> None:
    expected_families = {"local_supplied", "one_hop_aggregated", "completed_topology"}
    if set(families) != expected_families:
        missing = sorted(expected_families - set(families))
        extras = sorted(set(families) - expected_families)
        raise ManifestValidationError(
            f"elliptic_v1 family registry mismatch; missing={missing}, extras={extras}. "
            "New families require a new manifest version."
        )

    expected_local = tuple(f"feature_{index}" for index in range(1, 94))
    expected_aggregate = tuple(f"feature_{index}" for index in range(94, 166))
    expected_topology = (
        "in_degree",
        "out_degree",
        "pagerank_relative",
        "clustering",
        "k_core",
    )
    if families["local_supplied"].features != expected_local:
        raise ManifestValidationError(
            "Elliptic local supplied predictors must be feature_1 through feature_93 in order."
        )
    if families["one_hop_aggregated"].features != expected_aggregate:
        raise ManifestValidationError(
            "Elliptic one-hop predictors must be feature_94 through feature_165 in order."
        )
    if families["completed_topology"].features != expected_topology:
        raise ManifestValidationError(
            "elliptic_v1 completed topology must match the five frozen Study 1 predictors in order."
        )

    supplied_union = (
        families["local_supplied"].features + families["one_hop_aggregated"].features
    )
    if len(supplied_union) != 165 or len(set(supplied_union)) != 165:
        raise ManifestValidationError("Local and one-hop families must form 165 unique predictors.")

    expected_set_families = {
        "local": ("local_supplied",),
        "aggregate": ("one_hop_aggregated",),
        "full_supplied": ("local_supplied", "one_hop_aggregated"),
        "topology_completed": ("completed_topology",),
        "local_plus_topology": ("local_supplied", "completed_topology"),
        "aggregate_plus_topology": ("one_hop_aggregated", "completed_topology"),
        "full_plus_topology": (
            "local_supplied",
            "one_hop_aggregated",
            "completed_topology",
        ),
    }
    if set(sets) != set(expected_set_families):
        missing = sorted(set(expected_set_families) - set(sets))
        extras = sorted(set(sets) - set(expected_set_families))
        raise ManifestValidationError(
            f"elliptic_v1 feature-set registry mismatch; missing={missing}, extras={extras}. "
            "New sets require a new manifest version."
        )
    for name, expected_families_for_set in expected_set_families.items():
        if sets[name].families != expected_families_for_set:
            raise ManifestValidationError(
                f"Feature set {name} must use families {expected_families_for_set}, "
                f"observed {sets[name].families}."
            )


def load_feature_manifest(
    path: str | Path, *, expected_sha256: str | None = None
) -> FeatureManifest:
    manifest_path = Path(path)
    raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ManifestValidationError("Manifest root must be a mapping.")

    required_root_keys = {
        "schema_version",
        "manifest_id",
        "dataset",
        "source_study",
        "forbidden_predictors",
        "families",
        "feature_sets",
    }
    missing_root_keys = sorted(required_root_keys - set(raw))
    if missing_root_keys:
        raise ManifestValidationError(f"Manifest is missing root keys: {missing_root_keys}")

    forbidden = frozenset(str(value) for value in raw["forbidden_predictors"])
    families = _parse_families(raw["families"], forbidden)
    sets = _parse_sets(raw["feature_sets"], families)
    manifest_id = str(raw["manifest_id"])
    if manifest_id == "elliptic_v1":
        _validate_elliptic_v1_invariants(families, sets)

    manifest = FeatureManifest(
        schema_version=str(raw["schema_version"]),
        manifest_id=manifest_id,
        dataset=str(raw["dataset"]),
        source_study_commit=str(raw["source_study"]["commit"]),
        forbidden_predictors=forbidden,
        families=families,
        sets=sets,
        manifest_sha256=_canonical_hash(raw),
    )
    if expected_sha256 is not None:
        manifest.require_sha256(expected_sha256)
    return manifest
