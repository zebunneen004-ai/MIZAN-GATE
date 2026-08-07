# MIZAN-GATE

**A Decision-Time Graph Assurance System for Virtual-Asset AML Research**

MIZAN-GATE investigates when graph information improves AML detection, when it duplicates existing relational evidence, when it relies on information unavailable at the required decision time, and when authentic transaction topology becomes neutral or harmful under temporal change.

## Current scope

The initial bounded study is **MIZAN-GATE 0.1 — Elliptic Graph Evidence Audit**. Its first frozen design is the **93-local versus 72-one-hop relational-redundancy audit**.

This repository is separate from the completed Study 1 repository. Study 1 remains frozen at release `v2.0.2` and commit `bf807ef4e3af534d1d0eaa26b1a6cc56c7715b95`.

## First research contrast

The primary contrast compares topology's incremental PR-AUC contribution conditional on local predictors with its incremental contribution conditional on the full supplied matrix:

`R = [M(local + topology) - M(local)] - [M(full + topology) - M(full)]`

A positive result is evidence consistent with relational redundancy; it is not proof of causal or semantic equivalence.

## Validate the locked feature schema

```bash
python -m pip install --no-build-isolation -e ".[dev]"
python scripts/validate_feature_manifest.py
python -m pytest
```

The validation command checks both the manifest structure and the SHA-256 pinned by the experiment configuration.

## Research status

- Study 1 lineage is anchored to release `v2.0.2` and commit `bf807ef4e3af534d1d0eaa26b1a6cc56c7715b95`.
- The MIZAN-GATE 0.1A design, feature contract, temporal policy, and implementation were versioned before the first real 0.1A result run.
- The result-producing MIZAN-GATE implementation was commit `3a4270a237774ceb9d17e3893f6ccf822cbe4e22`.
- The first real MIZAN-GATE 0.1A run completed successfully on 2026-08-07.
- In the locked 31-40 extension, the registered redundancy contrast was `R = 0.003155`, with a 95% paired time-step block bootstrap interval of `[0.001195, 0.006566]`; under the preregistered `0.01 PR-AUC` practical margin, the result was classified as `practically_neutral`.
- In the historically known 41-49 extension, `R = -0.001970`, with a 95% paired time-step block bootstrap interval of `[-0.004565, 0.002381]`; this result was also classified as `practically_neutral`.
- The registered primary practical-materiality hypothesis was therefore not supported, and breakthrough status is `not_established`.
- Time steps 41-49 remain historically known secondary evidence and are not described as a newly untouched confirmatory sample.
- Human-readable post-result record: [`docs/results/elliptic_redundancy_v0_1_results.md`](docs/results/elliptic_redundancy_v0_1_results.md).
- Machine-readable post-result manifest: [`manifests/results/elliptic_redundancy_v0_1_post_result.json`](manifests/results/elliptic_redundancy_v0_1_post_result.json).

## Disclaimer

MIZAN-GATE is a research and model-assurance implementation. It is not legal advice, regulatory approval, real-time transaction monitoring, or evidence that a person or transaction committed a crime.
