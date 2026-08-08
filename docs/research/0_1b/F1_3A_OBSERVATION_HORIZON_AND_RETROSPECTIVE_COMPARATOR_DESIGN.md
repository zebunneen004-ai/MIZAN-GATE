# MIZAN-GATE 0.1B — F1.3A Observation-Horizon and Retrospective-Comparator Design

## Status

This is a prospective, pre-results scientific-design record.

It is intended to become the frozen F1.3A horizon design only after the exact
artifact is committed to the research branch, pushed to the remote research
branch, and the corresponding continuous-integration checks pass.

No MIZAN-GATE 0.1B predictive model has been fitted or evaluated in selecting
these horizons.

## Purpose

MIZAN-GATE 0.1B studies whether the apparent incremental utility of graph
evidence depends on when that evidence becomes observable relative to a target
Bitcoin transaction.

The horizon design must therefore be fixed before predictive utility is
inspected.

Horizon selection is based on:

- the already-frozen H0 decision epoch;
- Bitcoin block-height semantics;
- source-supported Bitcoin target block spacing;
- prior work proposing transaction-time or fixed-delay point-in-time features;
- the approximate temporal scale of the original Elliptic benchmark; and
- the benchmark-construction reference point recovered by the 2026 Elliptic
  forensic audit.

Horizon selection is not based on predictive performance.

Horizon selection is not constrained to produce a positive result.

Horizon selection is not allowed to be changed merely because one horizon is
more commercially attractive.

## Inherited frozen primary decision epoch

The primary H0 epoch remains unchanged from the sealed pre-provisioning record:

**end of the target transaction's confirmation block**

For target transaction i with confirmed block height b_i:

**H0 evidence eligibility: block_height <= b_i**

Consequences:

- same-block evidence is eligible at H0;
- evidence above b_i is future relative to H0;
- within-block ordering is not required for the primary experiment;
- H0 is a post-confirmation block-end risk assessment;
- H0 must not be described as transaction-arrival, mempool-time, or
  pre-confirmation prediction.

This F1.3A record does not reopen H0.

## Horizon parameterization

For a nonnegative relative block horizon h, define the admissible blockchain
cutoff for target transaction i as:

**B(i,h) = b_i + h**

A blockchain-derived observation is eligible at relative horizon h only when:

**observation_block_height <= B(i,h)**

The horizon variable h counts **additional blocks after H0**.

It does not directly denote a confirmation count.

Accordingly, H+6 must not be described as "six confirmations."

## Frozen core frontier horizons

The intended core frontier is:

**H_core = {0, 1, 6, 144} additional blocks**

### H0

Cutoff:

**b_i**

Role:

- primary decision-time baseline;
- no post-H0 blocks admitted.

### H+1

Cutoff:

**b_i + 1**

Role:

- immediate next-block evidence;
- measures the earliest discrete post-H0 expansion of admissible evidence.

### H+6

Cutoff:

**b_i + 6**

Role:

- short delayed-assessment horizon;
- approximately one target-hour under Bitcoin's 10-minute target block spacing.

The approximation is an expected-target-time interpretation only.

Observed Bitcoin block intervals vary.

H+6 remains block-height-defined even if six realized blocks take materially
less or more than one wall-clock hour.

### H+144

Cutoff:

**b_i + 144**

Role:

- delayed-assessment horizon at approximately one target-day under Bitcoin's
  10-minute target block spacing.

Again, this is an expected-target-time interpretation only.

The scientific eligibility rule remains block-height-based rather than
wall-clock-based.

## Pre-specified long-horizon sensitivity

A secondary long-horizon sensitivity is fixed at:

**H+2016**

Cutoff:

**b_i + 2016**

This is not part of the primary retrospective contrast.

Its purpose is to examine a longer information-availability scale with two
source-grounded interpretations:

1. 2016 target-spaced Bitcoin blocks correspond to approximately two weeks
   under the mainnet target spacing; and
2. the original Elliptic benchmark time steps are spaced approximately two
   weeks apart.

H+2016 is therefore a bridge between transaction-level block-height
observability and the benchmark's much coarser temporal cadence.

It must not be described as exactly fourteen elapsed days for each target.

## Retrospective comparator R

The retrospective comparator is frozen as the absolute Bitcoin block:

**R = 575059**

For R, the eligibility rule is:

**observation_block_height <= 575059**

R is not target-relative.

R is named:

**benchmark-construction-aligned retrospective comparator**

## Rationale for R = 575059

The sealed 2026 peer-reviewed Elliptic audit reports that the recovered
address-scoped features were evaluated at one common dataset-construction
reference point:

**Bitcoin block height 575059**

The same audit reports that supplied aggregated neighborhood features used
predecessor and successor transactions available at dataset construction,
rather than only transactions represented in the released sampled graph.

Therefore block 575059 is a scientifically grounded retrospective reference
for studying how graph/address evidence can differ between decision time and
benchmark-construction time.

## Limits of the R interpretation

R = 575059 must not be described as an exact reconstruction of every supplied
Elliptic feature.

The permitted interpretation is narrower:

**R is aligned to a source-supported benchmark-construction reference point.**

Reasons for this restriction include:

- not every original feature semantic is fully recovered;
- legacy preprocessing has its own leakage properties;
- the released sampled graph is not identical to the full blockchain
  neighborhood used during feature construction;
- MIZAN will recompute its own explicitly defined C, A_h, and G_h feature
  families rather than silently copy legacy feature semantics.

The legacy supplied Elliptic matrix remains a historical comparator.

## No current-tip comparator

The retrospective comparator must not be replaced by:

- the Bitcoin tip at experiment execution time;
- the final physical tip reached by the provisioned Bitcoin Core node;
- "all future data";
- an arbitrary maximum block supported by available storage.

Such alternatives would make the scientific comparator depend on execution
date or infrastructure rather than the benchmark-construction question.

## Primary horizon contrast

The primary horizon contrast is:

**decision-time H0 versus retrospective R**

The eventual feature/model estimand will be frozen only after C, A_h, G_h,
evaluation, and uncertainty definitions are formally specified.

F1.3A therefore freezes the observation horizons and their scientific roles,
not the final model or metric implementation.

## Frontier role of intermediate horizons

H+1, H+6, and H+144 characterize how admissible evidence changes between H0
and the retrospective comparator.

They are pre-specified before predictive modeling.

They must not be retained, removed, or reordered based on eventual predictive
performance.

H+2016 is a pre-specified secondary long-horizon sensitivity.

## No monotonicity assumption

MIZAN makes no assumption that graph utility must increase with additional
evidence.

For example, eventual estimates at H0, H+1, H+6, H+144, H+2016, and R may:

- increase;
- decrease;
- remain effectively unchanged;
- vary non-monotonically.

All such outcomes are scientifically admissible.

The term "frontier" describes evaluation across observation horizons and does
not mathematically assert monotonicity.

## Block-height eligibility versus wall-clock time

Primary eligibility is defined entirely by Bitcoin block height.

Realized elapsed wall-clock time between b_i and b_i+h may later be reported
descriptively.

Realized timestamps must not alter which blocks belong to a frozen relative
horizon.

This preserves deterministic eligibility and avoids post-hoc timestamp
tolerances.

## Cohort and missingness boundary

This record does not freeze the common-cohort or attrition policy.

Those rules remain for a later prospective design gate.

If a target cannot be reconstructed at a required horizon, MIZAN must not
silently substitute:

- a shorter horizon;
- a later horizon;
- the current chain tip;
- a partially reconstructed feature vector.

Such cases must be handled under the subsequently frozen cohort/attrition
rules.

## Infrastructure independence

The scientific horizon design is intentionally independent of the already
estimated infrastructure envelope.

The sealed pre-provisioning baseline covered Bitcoin history through block
487975 before future-horizon extension.

Because R is now scientifically fixed at block 575059, infrastructure and
storage planning must be updated before provisioning.

This is an infrastructure consequence of the scientific design.

It is not a reason to weaken or change the scientific comparator.

No claim is made here that the prior 1-TB working baseline is sufficient or
insufficient for full R reconstruction.

That question requires a new no-results capacity update.

## Predictive firewall

F1.3A performs no predictive evaluation.

Forbidden during this gate:

- PR-AUC;
- ROC-AUC;
- predictive F1;
- precision or recall at alert budget;
- model comparison;
- graph-utility estimation;
- Delta_G estimation;
- retrospective graph-utility inflation estimation;
- horizon selection using predictive outcomes.

No 0.1B breakthrough is established by this design record.

## Commercial firewall

The horizons are scientific observation regimes, not marketing tiers.

No horizon is selected because it would create a stronger commercial claim.

Any future commercial interpretation must follow the evidence generated under
the frozen scientific design.

A null, harmful, unstable, or positive graph-utility result remains admissible.

## Source basis

The horizon design inherits the sealed F1.1 prior-art and temporal-semantics
audit.

Key external source basis:

1. Weber et al. (2019), "Anti-Money Laundering in Bitcoin: Experimenting with
   Graph Convolutional Networks for Financial Forensics", arXiv:1908.02591.

2. Safar, Pluskal, Vesely, and Rysavy (2026), "The Enemy of Reproducibility is
   Opacity: What's Inside the Elliptic Bitcoin Dataset (and Why It Is Wrong)",
   Forensic Science International: Digital Investigation 57 Supplement,
   302124, DOI 10.1016/j.fsidi.2026.302124.

3. Frozen Bitcoin Core v31.1 source,
   commit 9be056a8a72b624dae9623b2f7bded92c2a21c91.

Source-supported claims and MIZAN design choices must remain distinguishable.

## F1.3A intended frozen decisions

Upon formal repository seal, F1.3A freezes:

**Primary inherited epoch**
- H0 = end of target confirmation block.

**Relative core frontier**
- +0 blocks;
- +1 block;
- +6 blocks;
- +144 blocks.

**Secondary long-horizon sensitivity**
- +2016 blocks.

**Retrospective comparator**
- absolute Bitcoin block 575059.

**Eligibility convention**
- block-height based;
- inclusive upper cutoff.

**Interpretive restrictions**
- relative h counts additional blocks after H0, not confirmations;
- approximate hour/day/week descriptions are target-time interpretations,
  not realized wall-clock guarantees;
- no monotonicity assumption;
- R is benchmark-construction-aligned, not an exact legacy-feature replica;
- no current-tip retrospective comparator.

## Explicitly unresolved after F1.3A

This record does not freeze:

- exact mapped-subset block-height envelope;
- safe transaction-intrinsic feature core C;
- point-in-time address-history definitions A_h;
- label-free graph/topology feature definitions G_h;
- graph hop depth;
- common eligible cohort;
- attrition thresholds;
- temporal/entity-disjoint split implementation;
- preprocessing specification;
- model family;
- hyperparameter protocol;
- primary predictive metric;
- practical materiality margin;
- uncertainty procedure;
- multiplicity treatment across frontier horizons;
- final alert-budget reporting;
- measured infrastructure usage;
- final minimum VM;
- runtime reconstruction coverage.

These must be resolved prospectively before predictive experimentation.

## Required consequence before provisioning

Because the retrospective comparator extends beyond the previously sealed
487975 baseline ceiling, a no-results infrastructure/capacity update covering
the R requirement must be completed before infrastructure is provisioned.

Infrastructure feasibility must follow the scientific horizon choice rather
than determine it.

## Gate conclusion

F1.3A defines a deterministic, source-grounded observation-horizon structure
for MIZAN-GATE 0.1B without inspecting predictive performance.

The design isolates:

- genuine decision-time evidence at H0;
- short delayed evidence at +1, +6, and +144 blocks;
- a pre-specified longer +2016-block sensitivity; and
- a benchmark-construction-aligned retrospective comparator at block 575059.

No predictive conclusion follows from this design.

The breakthrough claim remains unestablished.
