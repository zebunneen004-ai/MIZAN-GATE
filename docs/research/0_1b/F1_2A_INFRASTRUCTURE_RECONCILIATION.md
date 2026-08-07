# MIZAN-GATE 0.1B - F1.2A Infrastructure Reconciliation

**Status:** Completed with documented host-side deviation
**Phase:** F1.2A machine and infrastructure feasibility
**Scientific status:** Non-result-producing
**Parent F1.1 commit:** `c9d7691cd231ed41ae93062866037b3359ab0840`
**Created UTC:** `2026-08-07T19:06:05.3085039Z`

## 1. Purpose

This record reconciles the F1.2A machine inventory before any predictive
modeling or blockchain reconstruction is performed.

F1.2A was intended to be read-only with respect to both the MIZAN repository
and the host operating system.

The MIZAN repository remained unchanged throughout the inventory.

However, one host-side configuration change occurred and is documented below.

## 2. Repository integrity

At the end of the final F1.2A inventory:

- branch: `research/0.1b-feasibility`;
- HEAD: `c9d7691cd231ed41ae93062866037b3359ab0840`;
- working tree: clean;
- predictive models fitted: none;
- predictive metrics inspected: none;
- research data modified: none.

Therefore the host-side deviation did not contaminate the prospective
scientific record.

## 3. Observed host capability

The final inventory established the following non-identifying host facts:

- operating system: Windows 11 Home;
- architecture: x64;
- Windows version: 10.0.26200;
- CPU: Intel Core i7-1165G7;
- logical processors: 8;
- physical memory: approximately 15.8 GiB;
- C: free space: approximately 16.39 GiB;
- D: free space: approximately 324.13 GiB;
- Git: 2.55.0.windows.2;
- Git `core.autocrlf`: `true`;
- Windows Python: 3.14.6;
- previously validated MIZAN Python: 3.14.6;
- Docker: not found;
- .NET SDK/runtime command: not found;
- Conda: not found;
- Mamba: not found;
- Micromamba: not found;
- `bitcoind`: not found;
- `bitcoin-cli`: not found;
- `bitcoin-qt`: not found;
- GitHub DNS/HTTPS connectivity: available.

User account names, machine names, and similar identifying host metadata are
intentionally excluded from this repository record.

## 4. Documented host-side deviation

During the first F1.2A inventory pass, invoking the Windows `wsl.exe`
inspection commands encountered a system state in which WSL was not installed.

Windows then presented an installation prompt and proceeded to:

- install Windows Subsystem for Linux version 2.7.11;
- enable/install the Virtual Machine Platform optional component;
- report that a reboot was required before all changes became effective.

This was not an intended action of F1.2A.

The final sentence printed by the inventory script stating that "No software
was installed" must therefore not be interpreted as a summary of the entire
F1.2A sequence. It accurately describes only the later rerun after the WSL
installation had already occurred.

This record supersedes that misleading summary.

## 5. Current WSL state

On the later inventory pass:

- WSL version 2.7.11 was present;
- no Linux distribution was installed;
- WSL2 reported that it could not start because required virtualization was
  not currently available/enabled to WSL;
- no Linux environment was used for MIZAN work.

No BIOS/firmware change, Linux distribution installation, Docker installation,
or additional WSL configuration is authorized by this record.

## 6. Local-storage feasibility

The largest observed free local volume was approximately 324.13 GiB.

Current Bitcoin Core public requirements list approximately 750 GB of disk
space for default full-node operation and an initial blockchain download of
approximately 740 GB.

Source checked prospectively during F1.2A reconciliation:

`https://bitcoin.org/en/bitcoin-core/features/requirements.html`

Accordingly, the current machine is not treated as suitable for an archival
Bitcoin Core plus blockchain-indexing stack on its existing internal storage.

This does not prevent:

- small deterministic reconstruction tests;
- use of remote archival infrastructure;
- use of an appropriately sized external storage device;
- later use of a reproducibly provisioned cloud environment.

No final infrastructure architecture is frozen yet.

## 7. Pinned reconstruction-tool requirements

The F1.1-pinned repository

`nesfit/BitcoinTxSubgraphBuilder`

at commit

`8e01503c0f9f384402288509bdd5fc102590bcfb`

documents the following top-level environment requirements:

- x86_64 Linux;
- .NET 8 SDK;
- Python 3.10.16;
- Conda.

Its dataset-construction documentation additionally requires:

- PostgreSQL;
- one or more Blockbook endpoints;
- Bitcoin Core RPC for address-statistics collection.

The published `environment.yml` contains a much broader experimental
environment, including GPU/DGL/CUDA dependencies. MIZAN must not assume that
the entire environment is necessary for the narrow F1 reconstruction task.

A minimal reconstruction-only dependency contract must be derived before
software installation.

## 8. Transaction-hash mapping dependency

Inspection of the pinned implementation identified a critical input contract.

`python/libs/elliptic/data/dataset.py` reads:

`all_txs_hashes.csv`

from the Elliptic dataset directory when transaction hashes are requested.

The expected mapping columns are renamed from:

- `txId`
- `transaction`

to the implementation's internal transaction identifier and Bitcoin
transaction hash representation.

`python/import_elliptic_to_postgres.py` then imports the resulting real Bitcoin
transaction hashes into PostgreSQL.

The mapping file is not part of the original Elliptic benchmark release.

A public dataset claiming approximately 99.5% Elliptic transaction
deanonymization has historically been published on Kaggle and used by several
prior studies. However, MIZAN has not yet frozen:

- the exact mapping artifact;
- its byte hash;
- its current availability;
- its license/terms;
- its provenance chain;
- its mapping coverage on the exact frozen Elliptic raw files.

Therefore the mapping is a **feasibility dependency**, not yet an approved
research input.

## 9. F1.2B priority order

Before installing a reconstruction stack, F1.2B must:

1. locate the exact transaction-hash mapping artifact expected by the pinned
   implementation;
2. verify provenance, terms, schema, row count, and SHA-256;
3. determine mapping coverage against the frozen Elliptic transaction IDs;
4. derive the minimal reconstruction-only dependency set from the pinned code;
5. determine which functions require Blockbook and which require Bitcoin Core;
6. determine whether remote archival services can support a tiny deterministic
   feasibility sample without weakening verification;
7. define an independent second-source verification path;
8. only then choose local, hybrid, external-storage, or cloud infrastructure.

## 10. Scientific contamination boundary

F1 remains non-result-producing.

The following remain prohibited:

- predictive model fitting;
- PR-AUC / ROC-AUC / F1 evaluation;
- alert-budget predictive evaluation;
- predictive feature selection;
- predictive horizon selection;
- result-driven split selection.

Infrastructure and reconstruction feasibility may proceed.

## 11. F1.2A verdict

**F1.2A: COMPLETE WITH DOCUMENTED DEVIATION.**

The repository/scientific record remained intact.

The host-side WSL installation deviation is explicitly recorded and must not
be concealed or retrospectively described as a fully read-only inventory.

The next gate is F1.2B: mapping provenance and minimal reconstruction
dependency audit.
