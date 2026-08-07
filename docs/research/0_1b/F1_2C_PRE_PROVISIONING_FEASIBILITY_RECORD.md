# MIZAN-GATE 0.1B — F1.2C Pre-Provisioning Feasibility Record

## Status and scope

This record consolidates the no-results reconstruction and infrastructure feasibility evidence developed after the sealed F1.2B mapping-provenance record.

The underlying F1.2C C/D-series gates recorded here passed their stated static or bounded feasibility checks. Formal repository sealing is established by committing this additive record on the research branch and subsequently verifying the remote commit and CI.

This record is pre-provisioning evidence only.

It contains no predictive modeling, no PR-AUC or ROC-AUC evaluation, no predictive graph-utility result, and no raw deanonymized mapping data.

## Scientific purpose

MIZAN-GATE 0.1B asks how apparent incremental graph utility changes when evidence is constrained to what is admissible at a declared observation horizon.

Its primary experiment therefore requires authentic point-in-time blockchain reconstruction rather than treating the supplied Elliptic benchmark representation as decision-time-safe by default.

The legacy Elliptic representation remains a historical comparator, not the primary point-in-time representation.

## Frozen primary decision epoch

The primary observation epoch is:

**end of the target transaction's confirmation block**

For target transaction i at block b_i, H0 admits evidence with:

**block height <= b_i**

Consequences:

- same-block evidence is eligible at H0;
- block height > b_i is future evidence;
- within-block transaction ordering is not required for the primary design;
- this is a post-confirmation, block-end risk assessment;
- it must not be described as transaction-arrival, mempool-time, pre-confirmation, or within-block prediction.

This decision is frozen.

## Mapping status inherited from sealed F1.2B

Elliptic contains 203,769 transaction IDs.

The quarantined external mapping contains exact mappings for 202,804 Elliptic transaction IDs:

- mapped: 202,804
- unresolved: 965
- exact txId coverage: 99.526424529737%

All 49 Elliptic timesteps remain represented.

Mapping missingness differs across observed labels. Therefore mapping coverage must not be described as 100% mapping correctness, and later reconstruction must report attrition explicitly.

The raw mapping remains outside MIZAN and is not committed by this record.

## Authentic-chain feasibility evidence

A deterministic three-target Elliptic micro-reconstruction previously demonstrated that, for that bounded feasibility sample, the external mapping connected Elliptic transactions to authentic Bitcoin transactions and all six mapped immediate blockchain relations observed were represented consistently in the frozen Elliptic edge set.

That evidence establishes bounded feasibility only.

It does not establish:

- global mapping correctness;
- global Elliptic edge completeness;
- correctness for every mapped transaction;
- final reconstruction coverage.

## Builder historical-cutoff semantics

Frozen builder:

- repository: nesfit/BitcoinTxSubgraphBuilder
- commit: 8e01503c0f9f384402288509bdd5fc102590bcfb
- tree: 13b6abadc955973535b547c4aabe5c6711f3ee1c

Static source inspection supports an explicit historical target-height ceiling for the address-history collector.

The collector exposes and propagates targetHeight and retrieves blocks through a height-bounded loop.

By contrast, the transaction-graph expansion path is graph-distance bounded and no native block-height cutoff was identified in that expansion path.

Therefore graph evidence for 0.1B requires a separate explicit block-height eligibility filter. Graph expansion itself must not be assumed decision-time-safe merely because the collector is height-bounded.

These are source-supported conclusions, not yet runtime-certified conclusions.

## Blockbook historical-range semantics

Frozen Blockbook:

- repository: trezor/blockbook
- commit: 6ce54d0b22cccccabf09aea3b096197195b5bb5a
- tree: 1a921173d48d1769a741199ba8e301ccb5150c34

Static source inspection supports fixed historical range indexing using explicit lower and upper block bounds.

The normal fixed-range BulkConnectBlocks path iterates through an explicit upper bound.

Continuous synchronization is tip-aware.

Accordingly:

- fixed historical range behavior is source-supported;
- continuous synchronization must not be treated as equivalent to a frozen historical range;
- public bulk Blockbook reconstruction is not authorized for the controlled study;
- dedicated Blockbook remains the upstream-compatible architecture;
- exact runtime behavior remains to be certified after provisioning.

The claim is not that Blockbook never consults chain-tip state. Error, retry, reorganization, or continuous-sync paths may do so.

## Bitcoin Core provenance and stop-height semantics

Frozen Bitcoin Core:

- release: v31.1
- commit: 9be056a8a72b624dae9623b2f7bded92c2a21c91
- tree: 109dc8b3413dae47f00add3e30e50cde454c6f8c

Static source and upstream functional-test inspection support -stopatheight as a shutdown trigger reached when connected chain height is at least the configured value.

However, Bitcoin Core explicitly permits blocks beyond the configured stop height to be processed while shutdown occurs.

Therefore:

- -stopatheight is not an exact hard final-data ceiling;
- the final physical Bitcoin Core tip must not define scientific evidence eligibility;
- -stopatheight may serve as a historical capacity/control mechanism;
- scientific eligibility remains enforced downstream by explicit reconstruction and feature-height rules;
- exact behavior of the Linux binary used for the study still requires runtime certification.

## Elliptic source-declared block envelope

The pinned builder source declares block-height sets covering all 49 Elliptic timesteps.

Source-declared envelope:

- minimum block height: 391,200
- maximum block height: 487,975
- timesteps represented: 49
- distinct explicit source-declared block heights: 473

This is the source-declared Elliptic inclusion envelope.

It is not claimed to be the exact transaction-level minimum and maximum height of the 202,804 mapped subset.

## Conservative historical chain requirement

Without a validated checkpoint, the builder's address-history reconstruction begins from genesis.

In addition, predecessor relationships for an Elliptic-era transaction may originate substantially before the first Elliptic source-declared block.

No validated checkpoint shortcut has been adopted.

The conservative reproducible baseline is therefore:

- Bitcoin Core historical data: block 0 through block 487,975
- Blockbook historical index: block 0 through block 487,975

This baseline applies before any future observation-horizon extension is added.

The final scientific horizon set remains unfrozen.

## Reconstruction architecture

The frozen working reconstruction architecture is:

- dedicated x86_64 / AMD64 Linux host;
- PostgreSQL;
- .NET 8;
- Bitcoin Core;
- dedicated Blockbook;
- pinned BitcoinTxSubgraphBuilder reconstruction path.

Not required for the reconstruction closure:

- CUDA;
- DGL;
- PyTorch;
- the full upstream machine-learning Conda environment.

Public bulk Blockbook use is not authorized.

## Storage contract and engineering envelope

The pinned Blockbook reference describes approximately 32 GB RAM for current-mainnet initial synchronization, more than 180 GB of Blockbook disk for current mainnet, approximately 10 GB RAM after synchronization, and recommends fast SSD storage.

Its pinned Bitcoin backend configuration includes txindex=1 and does not enable pruning.

Capacity planning must therefore account separately for:

- historical raw Bitcoin block data;
- Bitcoin Core txindex;
- Core chainstate and metadata;
- Blockbook RocksDB;
- PostgreSQL;
- reconstruction artifacts;
- temporary synchronization/build/log space;
- engineering headroom.

The present conservative planning arithmetic is:

- historical raw-chain allowance: 130 GB
- Core txindex reserve: 20 GB
- Core state/metadata: 10 GB
- Blockbook RocksDB reserve: 180 GB
- PostgreSQL plus reconstruction artifacts: 50 GB
- temporary/log/build/workspace: 50 GB
- component total: 440 GB
- safety headroom: 25% = 110 GB
- conservative planning envelope: 550 GB

The 550 GB value is an engineering envelope, not measured historical usage.

## Working provisioning recommendation

Working baseline research provisioning:

- 32 GB RAM
- 8 vCPU
- 1 TB fast SSD
- Debian/AMD64-compatible Linux environment

High-headroom option:

- 64 GB RAM
- 16 vCPU
- 2 TB fast SSD

Neither configuration is asserted to be the measured minimum requirement.

The 8-vCPU baseline is an engineering choice, not a scientific requirement.

## Horizon-capacity sensitivity

Capacity sensitivities were evaluated only to determine whether short future-horizon extensions could plausibly invalidate the 1-TB planning envelope.

These are engineering cases, not frozen scientific horizons.

Using the Bitcoin Core v31.1 consensus maximum serialized block size of 4,000,000 bytes:

| Added blocks | Maximum raw serialized increment |
|---:|---:|
| 1 | 0.004 GB |
| 6 | 0.024 GB |
| 144 | 0.576 GB |
| 2,016 | 8.064 GB |
| 10,080 | 40.320 GB |

Under the 550-GB planning envelope on a nominal 1,000-GB decimal planning disk, residual capacity is 450 GB.

For the 144-block sensitivity case, 0.576 GB is the absolute maximum raw serialized-block increment, leaving approximately 781.25x amplification room before that residual capacity would be exhausted.

This calculation is not a prediction of RocksDB, Core index, PostgreSQL, or reconstruction-artifact growth.

It does not freeze 144 blocks or any other listed case as a scientific observation horizon.

## Rights and licensing firewall

Relevant research dependencies remain segregated from any future commercial implementation.

Current status:

- Elliptic dataset: CC BY-NC-ND 4.0;
- deanonymized mapping dataset: license unresolved / displayed as Unknown;
- BitcoinTxSubgraphBuilder: GPL-3;
- raw mapping: quarantined outside the MIZAN repository.

No claim is made that the mapping license has been resolved.

No raw deanonymized mapping is included in this record.

Any future commercial implementation must use appropriately licensed, proprietary, customer-owned, or otherwise contractually suitable data and implementation.

## Explicit unresolved items

This record does not freeze or resolve:

- numerical scientific observation horizons;
- retrospective comparator horizon R;
- exact mapped-subset transaction-height envelope;
- recomputed transaction-intrinsic safe core C;
- point-in-time address-history feature definitions A_h;
- primary label-free graph feature definitions G_h;
- common eligible cohort rules;
- strict temporal/entity-independence rules;
- attrition and coverage thresholds;
- uncertainty procedure;
- final alert-budget reporting rules;
- measured Core disk consumption;
- measured Blockbook disk consumption;
- measured PostgreSQL/reconstruction storage;
- measured runtime;
- final minimum VM specification;
- runtime certification of Bitcoin Core -stopatheight;
- runtime certification of Blockbook fixed-range service behavior;
- full mapped-set reconstruction coverage.

These remain downstream feasibility/design questions.

## Predictive-modeling firewall

No predictive 0.1B model has been executed.

In particular, this record contains no evidence about:

- Delta_G(0);
- Delta_G(h);
- Delta_G(R) - Delta_G(0);
- PR-AUC improvement;
- ROC-AUC improvement;
- alert-budget utility;
- whether a Decision-Time Availability Frontier exists empirically.

The 0.1B breakthrough claim remains not established.

## Gate conclusion

The pre-provisioning architecture is sufficiently supported by frozen-source analysis and bounded feasibility evidence to be recorded before infrastructure provisioning.

The following are supported at this stage:

- frozen end-of-confirmation-block H0 semantics;
- authentic-chain reconstruction is feasible in principle;
- explicit downstream height filtering is required for graph evidence;
- dedicated historical Blockbook is the preferred controlled path;
- Bitcoin Core -stopatheight cannot serve as the scientific evidence cutoff;
- genesis-through-487,975 is the conservative baseline historical chain requirement;
- a 1-TB working research disk clears the present 550-GB conservative planning envelope;
- short-horizon capacity is not presently the reason to choose or reject a scientific horizon.

Runtime certification and the remaining scientific design choices must occur before predictive experimentation.

No predictive result is inferred from this feasibility record.
