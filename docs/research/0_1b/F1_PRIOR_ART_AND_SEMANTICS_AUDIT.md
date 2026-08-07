# MIZAN-GATE 0.1B - F1 Prior-Art and Temporal-Semantics Audit

**Status:** Prospective feasibility evidence record
**Phase:** F1.1 Authoritative Evidence Lock
**Study:** MIZAN-GATE 0.1B
**Working title:** Decision-Time Availability Frontier of Graph Evidence
**Parent closure tag:** `elliptic-redundancy-v0.1a`
**Parent closure commit:** `10e647d196d0f8c5794883cad8e7884658f2deb0`
**Research branch:** `research/0.1b-feasibility`
**Created UTC:** `2026-08-07T18:34:41.5662636Z`

## 1. Purpose and contamination boundary

This document is a prospective feasibility and prior-art record created before
any MIZAN-GATE 0.1B predictive model is fitted and before any 0.1B predictive
performance is inspected.

It is not a preregistration and does not freeze the final 0.1B hypothesis,
information horizons, model, split, uncertainty procedure, practical margin,
or primary estimand.

During F1, permitted analyses are limited to:

- source and license verification;
- transaction/block/address mapping feasibility;
- blockchain reconstruction checks;
- feature-semantic verification;
- observability and horizon feasibility;
- neighborhood completeness diagnostics;
- sample counts and class counts;
- address/entity overlap;
- split attrition;
- runtime, storage, dependency, and infrastructure feasibility.

During F1, the following are prohibited:

- fitting predictive classification models;
- computing PR-AUC, ROC-AUC, F1, precision-at-budget, recall-at-budget,
  or other predictive utility comparisons for candidate 0.1B regimes;
- selecting information horizons based on predictive performance;
- selecting graph features based on predictive performance;
- selecting split rules because they make a model perform better;
- describing any 0.1B result as a breakthrough.

## 2. Evidence hierarchy

Claims are classified using the following hierarchy:

1. protocol / ledger fact - Bitcoin transaction semantics;
2. original benchmark source - original Elliptic paper and dataset card;
3. peer-reviewed audit - later forensic reverse engineering of Elliptic;
4. exact source repository - version-pinned implementation/documentation;
5. preprint prior art - relevant but not treated as settled peer-reviewed fact;
6. MIZAN inference - interpretation that must remain explicitly labeled as such.

No MIZAN inference may silently replace or strengthen a source claim.

## 3. Locked facts about the original Elliptic benchmark

### 3.1 Graph and feature structure

The original Elliptic benchmark contains:

- 203,769 transaction nodes;
- 234,355 directed payment-flow edges;
- 166 node features;
- 94 features in the original "local" family, including the time-step feature;
- 72 one-hop aggregated neighborhood features.

The neighborhood features include backward and forward transaction information.

For continuity with MIZAN-GATE 0.1A, note that the earlier term `local93`
referred to the 93 predictor columns remaining after excluding the explicit
time-step field from the original 94-feature local family. The terminology
must not be confused.

### 3.2 Time-step semantics

The benchmark contains 49 time steps spaced approximately two weeks apart.

Each time step is a single connected component containing transactions that
appeared on the blockchain within less than approximately three hours of one
another.

There are no released graph edges connecting different time steps.

A source-level semantic discrepancy exists:

- the original Weber et al. paper describes the node timestamp as an estimate
  of when the transaction was confirmed by the Bitcoin network;
- the official Elliptic Kaggle data card describes the time step as a measure
  of when the transaction was broadcast to the Bitcoin network.

Therefore:

**MIZAN must not treat Elliptic `time_step` as an exact transaction-level
decision timestamp.**

Until independent blockchain mapping resolves transaction-level timing,
the time step may be used only as a coarse benchmark temporal index.

## 4. Locked facts from the 2026 peer-reviewed Elliptic audit

The peer-reviewed forensic reverse-engineering study by Safar, Pluskal,
Vesely, and Rysavy reports the following.

### 4.1 Recovered feature semantics

The study reports recovery of:

- 91 of the 94 original local feature semantics;
- 60 of the 72 aggregated neighborhood feature semantics.

Excluding the explicit time-step field, it reports that 21 local predictors
(features 2-22 in the recovered feature numbering) are scoped directly to
the transaction itself.

Three of those 21 transaction-scoped feature meanings remained unidentified.

The remaining nominally local features are predominantly aggregates of
properties of Bitcoin addresses participating in the transaction.

### 4.2 Future-scoped address information

The recovered address-scoped features include quantities such as:

- BTC received and sent;
- available balance;
- incoming transaction count;
- outgoing transaction count;
- address lifetime.

The audit reports that these address-scoped features were evaluated relative
to one common reference point:

`Bitcoin block height 575059`

rather than relative to each transaction's own occurrence time.

This creates a decision-time validity problem when a feature contains
address activity that occurred after the transaction being classified.

### 4.3 Neighborhood semantics

The audit reports that original aggregated neighborhood features were not
constructed solely from neighbors present in the released sampled Elliptic
graph.

They were constructed from neighboring transactions available during dataset
construction, including predecessor and successor transaction information.

Therefore the released sampled graph and the information used to construct
the supplied neighborhood feature matrix are not equivalent objects.

### 4.4 Dataset-wide normalization

The audit reports that z-score normalization parameters were calculated using
the full dataset rather than the training partition alone.

For prospective MIZAN experiments, learned preprocessing parameters must be
estimated from training data only unless a preregistered alternative has an
explicit scientific justification.

### 4.5 Entity nonindependence

The audit reports that Bitcoin addresses recur across standard temporal
training and test partitions.

Because address-derived feature values are reused across transactions and
transaction labels are linked to initiating/input-address entities, temporal
splitting alone does not guarantee entity independence.

MIZAN must therefore quantify address overlap before deciding whether a
strict entity-disjoint evaluation is feasible.

### 4.6 Truncated released neighborhoods

The audit reports that Elliptic's isolated time-window components omit real
blockchain predecessors and related transactions.

As a result, the released edge list is not a complete causal transaction
history for a target transaction.

Primary 0.1B decision-time graph reconstruction must therefore not assume
that `elliptic_txs_edgelist.csv` is a complete historical neighborhood.

### 4.7 Proposed mitigation from prior work

The audit recommends:

- time-scoped address features evaluated at transaction time or at one
  consistently defined relative delay;
- training-only estimation of preprocessing parameters;
- reconstruction of complete fixed-hop transaction neighborhoods;
- strict graph/entity separation between evaluation partitions.

The audit identifies delayed prediction, such as approximately one hour or
one day later, as an area requiring further study rather than an already
established optimal operating policy.

## 5. Bitcoin observability rules

A non-coinbase Bitcoin transaction input spends a specific output of a
previous transaction.

Therefore a predecessor transaction required by an input necessarily exists
before the spending transaction can validly consume that output.

A later transaction that spends an output of the target transaction is a
successor and cannot be part of the target's pre-existing historical evidence
before that successor exists.

These protocol relationships provide an independently verifiable causal
ordering for transaction-dependency edges.

MIZAN will distinguish at minimum:

- predecessor evidence already present by the declared prediction epoch;
- target-transaction intrinsic evidence;
- successor evidence that becomes available only later.

The final 0.1B prediction epoch is not yet frozen.

A confirmation-block-relative epoch is currently a candidate because block
membership and chain order are reproducible from blockchain history, whereas
the released Elliptic time step does not establish a precise globally
observed broadcast timestamp.

## 6. Prior-art boundary

### 6.1 Time-respecting handcrafted graph features

Khaleghpour and McKinney, arXiv:2603.06632v1, already study graph features
computed on edges observed up to an Elliptic time step.

Therefore MIZAN must not claim novelty merely for:

- constructing `G <= t`;
- computing causal/time-respecting degree;
- causal/time-respecting PageRank;
- causal/time-respecting HITS;
- causal/time-respecting k-core;
- using a chronological Elliptic train/test split.

### 6.2 Strict inductive GNN evaluation and topology controls

Maganti, arXiv:2604.19514v1, studies strict-inductive versus transductive
GNN evaluation on Elliptic and reports edge-shuffle and no-edge controls.

Therefore MIZAN must not claim novelty merely for:

- preventing training-time GNN message passing over test-period graph data;
- comparing strict-inductive and transductive GNN evaluation;
- comparing real edges against shuffled or absent edges.

These remain important controls, but they are not by themselves the proposed
0.1B contribution.

## 7. Provisional MIZAN research gap

The following is a working hypothesis about the literature gap, not a frozen
novelty claim:

> Graph utility may be a function of the evidence-availability horizon at
> which a decision is required, rather than a fixed property of a graph model
> or benchmark.

A prospective MIZAN study may therefore investigate the marginal utility of
graph evidence under multiple explicitly reconstructed information horizons,
while matching the non-graph information available at the same horizon.

This prospective direction remains subject to:

- broader prior-art review;
- reconstruction feasibility;
- transaction mapping coverage;
- address/entity independence feasibility;
- common-cohort feasibility across horizons;
- computational feasibility.

MIZAN must not claim that no prior work has studied an equivalent frontier
until a substantially broader novelty review has been completed.

## 8. Terminology controls

Until F1 is complete, the following phrases are prohibited for reconstructed
Elliptic evidence unless specifically proven:

- exact real-time evidence;
- exact broadcast-time evidence;
- production-time evidence;
- leakage-free in every sense;
- fully causal model;
- unbiased benchmark;
- independent test set;
- breakthrough.

Preferred provisional language includes:

- confirmation-relative evidence;
- block-height-scoped evidence;
- information available by the declared reconstruction horizon;
- leakage-resistant with respect to the explicitly tested mechanism;
- reconstructed historical blockchain context;
- prospective feasibility result.

## 9. Licensing and commercial firewall

The original Elliptic dataset is distributed under CC BY-NC-ND 4.0.

Accordingly, MIZAN treats Elliptic and Elliptic-derived restricted artifacts
as research-validation material, not as commercial product data.

The peer-reviewed 2026 audit states that a corrected/modified Elliptic dataset
cannot simply be redistributed under those terms.

The version-pinned `nesfit/BitcoinTxSubgraphBuilder` repository contains a
GPL-3.0 license.

GPL-3.0 does not by itself prohibit commercial use. However, redistribution
of a derivative or modified covered program may impose source-code and
copyleft obligations.

Therefore:

- the external tool may be studied and executed for research where lawful;
- MIZAN must not casually copy GPL-covered implementation code into a
  proprietary commercial core;
- any eventual commercial implementation should have independently authored
  code and separately reviewed dependencies unless legal review establishes
  an acceptable licensing architecture;
- this document is a research-engineering policy, not legal advice.

The `nesfit/DeanonymizedEllipticBitcoinDataset` repository is used here as
version-pinned scientific documentation of recovered semantics. No separate
commercial reuse right is assumed by MIZAN merely because the repository is
public.

## 10. Version-pinned external repositories

For F1, the following external repository states are pinned:

### DeanonymizedEllipticBitcoinDataset

Repository:

`nesfit/DeanonymizedEllipticBitcoinDataset`

Pinned commit:

`a5dbbcc655783003d942d0d54ad8404f0b7b3b93`

Pinned README Git blob:

`4dd6695526d5deaec04e84f85ce5fe50009412ff`

### BitcoinTxSubgraphBuilder

Repository:

`nesfit/BitcoinTxSubgraphBuilder`

Pinned commit:

`8e01503c0f9f384402288509bdd5fc102590bcfb`

Pinned README Git blob:

`2565a03c22fecd8d9e4a16e55a656d304c0f2e7e`

Observed environment requirements at the pinned state include:

- x86_64 Linux;
- .NET 8 SDK;
- Python 3.10.16;
- Conda.

The repository's license file identifies GNU GPL version 3.

No external repository will be allowed to float silently to a newer commit
during F1.

## 11. F1 exit conditions

F1 may advance to formal 0.1B design only if we can establish, without using
predictive performance:

1. sufficiently reliable Elliptic-ID-to-Bitcoin-transaction mapping;
2. reproducible confirmation block heights;
3. reproducible predecessor and successor relations;
4. a precise definition of information admissible at each candidate horizon;
5. time-scoped address statistics for a meaningful sample;
6. complete or explicitly bounded transaction neighborhoods;
7. candidate horizon coverage and common-cohort counts;
8. labeled class counts after each feasibility restriction;
9. address/entity overlap and attrition statistics;
10. an explicit license-safe research and commercial separation;
11. computational feasibility for the intended full reconstruction.

If these conditions cannot be satisfied, 0.1B must be redesigned before
predictive results are inspected.

## 12. Source register

- **S1:** Weber et al. (2019), *Anti-Money Laundering in Bitcoin:
  Experimenting with Graph Convolutional Networks for Financial Forensics*,
  arXiv:1908.02591.
- **S2:** Official Elliptic Kaggle dataset card,
  dataset slug `ellipticco/elliptic-data-set`.
- **S3:** Safar, Pluskal, Vesely, Rysavy (2026), *The Enemy of
  Reproducibility is Opacity: What's Inside the Elliptic Bitcoin Dataset
  (and Why It Is Wrong)*, DOI `10.1016/j.fsidi.2026.302124`.
- **S4:** `nesfit/DeanonymizedEllipticBitcoinDataset`,
  commit `a5dbbcc655783003d942d0d54ad8404f0b7b3b93`.
- **S5:** `nesfit/BitcoinTxSubgraphBuilder`,
  commit `8e01503c0f9f384402288509bdd5fc102590bcfb`.
- **S6:** Bitcoin developer transaction and blockchain documentation.
- **S7:** Khaleghpour and McKinney (2026),
  *Leakage Safe Graph Features for Interpretable Fraud Detection in Temporal
  Transaction Networks*, arXiv:2603.06632v1.
- **S8:** Maganti (2026), *When Graph Structure Becomes a Liability:
  A Critical Re-Evaluation of Graph Neural Networks for Bitcoin Fraud
  Detection under Temporal Distribution Shift*, arXiv:2604.19514v1.

## 13. Current gate verdict

**F1.1 document status: prospective source lock, pending local validation and
commit.**

No 0.1B scientific hypothesis has yet been tested.

No 0.1B predictive result exists.
