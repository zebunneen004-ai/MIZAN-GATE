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

- Study 1 lineage anchored
- Exact feature families and combinations registered
- Feature manifest cryptographically pinned in the experiment specification
- Primary estimand, seed aggregation, practical margin, and uncertainty policy frozen
- External timestamp pending until the design is pushed to a versioned public record
- New redundancy models not yet run

## Disclaimer

MIZAN-GATE is a research and model-assurance implementation. It is not legal advice, regulatory approval, real-time transaction monitoring, or evidence that a person or transaction committed a crime.
