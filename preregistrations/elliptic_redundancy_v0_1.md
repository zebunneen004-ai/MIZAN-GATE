# Design Registration: MIZAN-GATE 0.1A — Elliptic Relational Redundancy Audit

**Status:** Design frozen locally before MIZAN-GATE redundancy results; external timestamp pending  
**Feature manifest:** `manifests/features/elliptic_v1.yaml`  
**Pinned manifest SHA-256:** `3574062ab2bdaddd3eb17e33f39355ad1158854b2a60678b236abbce159a2e8b`  
**Study 1 lineage:** `zebunneen004-ai/graph-financial-crime-detection`, release `v2.0.2`, commit `bf807ef4e3af534d1d0eaa26b1a6cc56c7715b95`

This document becomes an externally timestamped preregistration only after publication in an immutable or versioned public record, such as a GitHub commit/release or an OSF registration. Until then, it is a locally frozen design document.

## 1. Motivation

Study 1 found that five completed-snapshot topology variables did not produce a statistically reliable or practically material PR-AUC improvement beyond Elliptic's full supplied feature matrix. The full supplied matrix, however, contains 72 anonymous one-hop aggregate variables in addition to 93 anonymous local variables. The present study tests whether the observed non-incremental topology result is consistent with relational redundancy.

This study does not assume that the one-hop aggregates and topology variables are mathematically equivalent, causally interchangeable, or available at the same decision time. It tests conditional predictive increment under a fixed temporal protocol.

## 2. Primary research question

Does completed-snapshot topology provide materially greater incremental predictive information when added to the 93 local supplied predictors than when added to the full 165 supplied predictors containing the 72 one-hop aggregate predictors?

## 3. Registered feature families

- **Local supplied (`L`):** `feature_1` through `feature_93`.
- **One-hop aggregated (`A`):** `feature_94` through `feature_165`.
- **Full supplied (`F`):** `L ∪ A`.
- **Completed topology (`T`):** `in_degree`, `out_degree`, `pagerank_relative`, `clustering`, and `k_core`.

`txId`, `time_step`, labels, descriptive graph variables, and snapshot-size sensitivity variables are prohibited predictors in this experiment. Any new family or set requires a new manifest version and a recorded design amendment before affected results are viewed.

## 4. Primary estimand

Let `M(S)` denote PR-AUC for feature set `S`, calculated from the same observations and the mean predicted probability across the five matched technical seeds.

- `ΔL = M(L + T) − M(L)`
- `ΔF = M(F + T) − M(F)`
- **Relational-redundancy contrast:** `R = ΔL − ΔF`

A positive `R` indicates that completed topology contributes more when one-hop aggregates are absent. This is evidence consistent with relational redundancy, not proof of semantic or causal duplication.

## 5. Hypotheses

### Primary hypothesis

`R > 0`, with `R ≥ 0.01 PR-AUC` treated as practically material.

The `0.01` margin is inherited prospectively from Study 1's feature-selection policy. It is a project-defined materiality threshold, not an accepted scientific, regulatory, or industry standard.

### Secondary hypotheses

1. `M(F) − M(L) > 0`.
2. `ΔL > 0`.
3. `|ΔF| ≤ 0.01` as the practical-neutrality target, evaluated using an equivalence interval rather than a non-significant null test.
4. The direction of the primary contrast is reasonably stable across temporal folds and matched random seeds.

Only `R` is the primary inferential contrast. Other comparisons are secondary and will not be used to redefine the hypothesis after results are viewed.

## 6. Primary model and seed protocol

The primary model is XGBoost using the hyperparameters selected in Study 1. The same fixed hyperparameters, preprocessing, observations, temporal folds, class-weight calculation, and matched seeds `[11, 23, 42, 71, 101]` will be used for every feature family.

For the primary analysis, each feature set's predicted probability is averaged across the five matched seeds before PR-AUC and paired contrasts are calculated. The seeds are technical replicates used to reduce stochastic model variation; they are not treated as five independent statistical samples. Per-seed contrasts are reported only as descriptive stability evidence.

A later sensitivity analysis may tune each feature set, but only with an identical search space, trial count, fold structure, and seed budget. Its results will be labelled sensitivity evidence.

## 7. Temporal evidence policy

- Time steps 1–30 are used for expanding-window development analysis.
- Time steps 31–40 form a locked temporal extension window for the new feature-family contrasts. They are not wholly unobserved data because Study 1 used portions of this era for calibration and operating selection.
- Time steps 41–49 are a historically known holdout from Study 1. They may be reported as secondary extension evidence but are not a newly untouched confirmatory test for hypotheses formulated after Study 1.
- Independent confirmation requires a new dataset, a new preserved temporal environment, or another genuinely unobserved evaluation sample.

## 8. Metrics and operating analysis

PR-AUC is the primary discrimination metric. Secondary reporting includes ROC-AUC and fixed alert-budget precision, recall, and F1 at 1%, 5%, 10%, and 20%. Accuracy is not a lead metric.

Thresholds will not be optimized separately to make one feature family appear superior. Fixed alert budgets compare rankings directly and are the preferred operational comparison for this audit.

## 9. Uncertainty and practical classification

The primary interval is a paired time-step block bootstrap with 2,000 repetitions. A paired observation-level bootstrap is reported as sensitivity evidence because connected transactions are not independent observations. Development-fold differences are reported descriptively; four temporal folds are not treated as independent inferential replicates.

The extension and historical windows contain only 10 and 9 time steps. Their block-bootstrap intervals may therefore be unstable and will be interpreted cautiously rather than treated as decisive external confirmation.

Using practical margin `ε = 0.01 PR-AUC`:

- **Helpful:** lower confidence bound exceeds `+ε`.
- **Harmful:** upper confidence bound is below `−ε`.
- **Practically neutral:** the complete interval lies inside `[-ε, +ε]`.
- **Uncertain:** all other cases.

An interval containing zero is not, by itself, evidence of equivalence.

## 10. Interpretation constraints

The study will not claim that:

- one-hop aggregates and topology are identical;
- graph information is universally useful or useless;
- completed-snapshot features were available at transaction decision time;
- Elliptic results generalize directly to UAE VASPs;
- a predictive association establishes criminal intent or regulatory compliance;
- a positive contrast is a breakthrough before comparison with current literature and external validation.

## 11. Deviations

Any deviation from this document must be recorded before the affected results are viewed, with the date, reason, affected analyses, and whether the change converts an analysis from confirmatory to exploratory.
