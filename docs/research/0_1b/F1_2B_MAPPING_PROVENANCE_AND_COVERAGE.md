# MIZAN-GATE 0.1B ? F1.2B Mapping Provenance and Coverage

**Status:** Technical provenance and coverage verified; rights unresolved

**Scientific status:** Prospective feasibility / non-result-producing

**Predictive modeling performed:** No

**Parent commit:** `f2737079d3709d2b2647f02decad5c04bafdb98f`

## Purpose

F1.2B determines whether the external Elliptic transaction-ID-to-Bitcoin-
transaction-hash mapping required for prospective blockchain reconstruction
can be identified, frozen, validated against the cryptographically verified
Elliptic source, and handled without publishing the raw mapping.

No predictive performance is evaluated in this phase.

## Mapping source

Kaggle dataset:

`alexbenzik/deanonymized-995-pct-of-elliptic-transactions`

Observed source metadata:

- version: `1`;
- last updated: `2019-11-18T11:30:49.563Z`;
- observed license field: `Unknown`;
- license/rights status: **UNRESOLVED**;
- redistribution approval: **NO**;
- commercial-use approval: **NO**.

Technical identity and rights status are intentionally separate.
Public accessibility is not interpreted as redistribution or commercial-use
permission.

## Frozen artifact identity

Archive SHA-256:

`05bc9d176a1d25c871bda6ec176fbc61e67b866e76b6f102ff5ca6eb9b987803`

`Result.csv` SHA-256:

`7ba5831196c108590b88a4ac488bfc6a7753890f9ea1b2e28c1d2fdff6b27dc8`

Physical mapping rows:

`202,804`

The raw archive and mapping remain in isolated non-repository quarantine
storage.

## Frozen Elliptic identity

`elliptic_txs_features.csv` SHA-256:

`fd7f83573443c9e302e371d3f110e3b6224160f5d1ed8a287757936127800ff0`

`elliptic_txs_classes.csv` SHA-256:

`93e2e7b2405c735ba752bf6ba06b947561deddd1f5a8fc91e46f6a4c0e439493`

Frozen Elliptic transaction count:

`203,769`

Timestep support:

`1?49`

## Exact mapping integrity

The mapping contains:

- `202,804` physical rows;
- `202,804` unique Elliptic transaction IDs;
- `202,804` unique valid Bitcoin transaction hashes;
- zero duplicate transaction IDs;
- zero duplicate transaction hashes;
- zero invalid transaction IDs;
- zero invalid transaction hashes;
- zero malformed rows;
- zero IDs outside the frozen Elliptic universe.

Exactly `965` Elliptic transactions are
unmapped.

Exact mapped coverage:

`99.526424529737%`

The mapping is therefore an exact subset of the frozen Elliptic transaction-ID
universe.

## Coverage by observed Elliptic label

| Raw label | Total | Mapped | Missing | Coverage |
|---|---:|---:|---:|---:|
| `1` | 4,545 | 4,545 | 0 | 100.00000000% |
| `2` | 42,019 | 41,500 | 519 | 98.76484448% |
| `unknown` | 157,205 | 156,759 | 446 | 99.71629401% |

Mapping eligibility is not uniform across observed benchmark labels.
This is a feasibility/sample-selection observation, not a predictive result.

## Temporal coverage

All 49 Elliptic timesteps are represented.

The lowest observed mapping coverage occurs at timestep `43`:

`97.15583646%`

The largest missing count occurs at timestep `43`:

`144` transactions.

Complete timestep counts are preserved in the accompanying sanitized
machine-readable manifest.

No predictive result was used to choose or prioritize any timestep.

## Canonical fingerprints

Elliptic transaction-ID set:

`e3483c717347bbc5e0a4b360fea79a6415774679f86c66263f6454d18cc3f3f1`

Mapped transaction-ID set:

`eff802cd010020b8d0fc30b34a8efa6392e9e31be02406e8876b46b37888f5af`

Missing transaction-ID set:

`9c27e427893cc70dbf05d53af07abbad71817e30ee4e32c349c25cfc4d9c98e3`

Canonical sorted mapping-pair fingerprint:

`309760907589320cf35e74c5b0c1398a3abc5bd6b730e60fe3efcf91ea0cba87`

These permit later identity verification without publishing raw mapping pairs.

## Repository firewall

The repository record contains aggregate counts, coverage statistics, source
hashes and canonical fingerprints only.

The raw mapping must not be:

- committed to MIZAN-GATE;
- uploaded to the public repository;
- redistributed as a MIZAN artifact;
- treated as commercially licensed.

## Prospective design implication

Mapping/reconstruction eligibility is itself a source of sample selection.

Later preregistration must define a common eligible target cohort before
predictive outcomes are inspected and must prevent cross-horizon comparisons
from silently changing target populations.

This phase establishes neither graph utility nor predictive superiority.

## F1.2B verdict

**Technical mapping provenance: VERIFIED.**

**Exact Elliptic coverage: VERIFIED.**

**Raw-data repository isolation: VERIFIED.**

**Predictive contamination: NONE.**

**Redistribution/commercial rights: UNRESOLVED / NOT APPROVED.**

No reconstruction-software installation is authorized by this record.
