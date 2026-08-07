# MIZAN-GATE 0.1A — Post-Result Scientific Record

**Experiment:** `elliptic_redundancy_v0_1`
**Record type:** Post-result closure record
**Created UTC:** `2026-08-07T17:07:07.639515+00:00`
**Result-producing MIZAN-GATE commit:** `3a4270a237774ceb9d17e3893f6ccf822cbe4e22`
**Study 1 source commit:** `bf807ef4e3af534d1d0eaa26b1a6cc56c7715b95`

## Post-result declaration

This document was created **after** MIZAN-GATE 0.1A results had been generated and inspected. It is not a preregistration. It does not modify the frozen research question, feature families, estimands, model, temporal policy, practical margin, matched-seed protocol, or uncertainty policy.

## Research question

The registered question asked whether five completed-snapshot topology features contribute materially more incremental PR-AUC when added to the 93 local supplied predictors than when added to the full 165 supplied predictors, which already contain 72 one-hop aggregate predictors.

The primary registered contrast was:

`R = [M(L+T) - M(L)] - [M(F+T) - M(F)]`

The preregistered practical-materiality margin was `0.01 PR-AUC`. A positive contrast was defined only as evidence consistent with relational redundancy, not proof of semantic, mathematical, or causal equivalence.

## Evidence identity

- Frozen result archive: `MIZAN_GATE_0_1A_RESULTS_ORIGINAL.zip` — SHA-256 `f7889bb380607288a0dc239dee78e29bf26aed52752e811873e275983b718247`.
- Output-hash manifest: `MIZAN_GATE_0_1A_OUTPUT_HASHES.csv` — SHA-256 `8d5c00b8112e62ba56c6f7d89495293fcf759ad488ffc3fa569522f412aa1310`.
- Run log: `MIZAN_GATE_0_1A_run.log` — SHA-256 `1053254b4673d224aa0a05a88f2bef6e12de9e36b0dc3e1b5bae6658e79b920f`.
- Registered result artifacts verified: `9`.
- Run completed UTC: `2026-08-07T16:30:24.988362+00:00`.

## Primary and secondary point estimates

| Window | M(L) | M(L+T) | M(F) | M(F+T) | Delta_L | Delta_F | R | M(F)-M(L) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 31-40 locked extension | 0.948910 | 0.952090 | 0.958967 | 0.958993 | 0.003181 | 0.000025 | 0.003155 | 0.010058 |
| 41-49 historical known extension | 0.620024 | 0.618043 | 0.645144 | 0.645134 | -0.001981 | -0.000010 | -0.001970 | 0.025120 |

## Registered uncertainty

The primary uncertainty procedure is the paired time-step block bootstrap with 2,000 repetitions. The paired observation bootstrap with 2,000 repetitions is reported as sensitivity evidence.

| Window | Role | Contrast | Estimate | 95% lower | 95% upper | Classification |
| --- | --- | --- | ---: | ---: | ---: | --- |
| 31-40 | primary | delta_local | 0.003181 | 0.000763 | 0.007111 | practically_neutral |
| 31-40 | primary | delta_full | 0.000025 | -0.000932 | 0.001329 | practically_neutral |
| 31-40 | primary | redundancy_contrast | 0.003155 | 0.001195 | 0.006566 | practically_neutral |
| 31-40 | primary | full_minus_local | 0.010058 | 0.004306 | 0.022976 | not_applicable |
| 31-40 | sensitivity | delta_local | 0.003181 | 0.001725 | 0.004824 | practically_neutral |
| 31-40 | sensitivity | delta_full | 0.000025 | -0.000676 | 0.000736 | practically_neutral |
| 31-40 | sensitivity | redundancy_contrast | 0.003155 | 0.001648 | 0.004783 | practically_neutral |
| 31-40 | sensitivity | full_minus_local | 0.010058 | 0.006153 | 0.014400 | not_applicable |
| 41-49 | primary | delta_local | -0.001981 | -0.003696 | 0.001207 | practically_neutral |
| 41-49 | primary | delta_full | -0.000010 | -0.001850 | 0.002178 | practically_neutral |
| 41-49 | primary | redundancy_contrast | -0.001970 | -0.004565 | 0.002381 | practically_neutral |
| 41-49 | primary | full_minus_local | 0.025120 | 0.001420 | 0.040035 | not_applicable |
| 41-49 | sensitivity | delta_local | -0.001981 | -0.004907 | 0.000980 | practically_neutral |
| 41-49 | sensitivity | delta_full | -0.000010 | -0.001810 | 0.001759 | practically_neutral |
| 41-49 | sensitivity | redundancy_contrast | -0.001970 | -0.004888 | 0.001073 | practically_neutral |
| 41-49 | sensitivity | full_minus_local | 0.025120 | 0.016577 | 0.034534 | not_applicable |

## Hypothesis verdicts

- **primary_R_material — not_supported_as_practically_material:** Extension R was positive, but the complete primary 95% interval was inside [-0.01, +0.01]; historical R was negative with a primary interval that also remained inside the practical-neutrality region.
- **secondary_full_minus_local — supported_in_both_later_windows_as_secondary_evidence:** The point estimate was positive in both later windows and the registered paired time-step bootstrap interval for full_minus_local was entirely above zero.
- **secondary_delta_local — not_supported_as_temporally_stable:** Delta_L was positive in the 31-40 extension but negative in 41-49; development-fold directions were also mixed.
- **secondary_delta_full_neutrality — supported_as_practically_neutral_in_both_later_windows:** The complete registered primary intervals for Delta_F lay inside [-0.01, +0.01] in both later windows; observation-bootstrap sensitivity evidence agreed.
- **secondary_directional_stability — not_supported:** Development-fold signs were mixed, all five extension seed contrasts were positive, and four of five historical seed contrasts were negative.

## Temporal and seed stability

- Development-fold R signs: `2` positive, `2` negative.
- Extension 31-40 matched seeds: `5/5` positive.
- Historical 41-49 matched seeds: `1/5` positive and `4/5` negative.

The positive extension contrast therefore did not demonstrate stable temporal transport.

## Fixed alert-budget operating evidence

No alert budget was selected post hoc. The registered 1%, 5%, 10%, and 20% budgets are reported for the four primary feature sets.

| Window | Feature set | Budget | TP | FP | Precision | Recall | F1 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 31-40 | local | 1% | 97 | 0 | 1.0000 | 0.0909 | 0.1667 |
| 31-40 | local | 5% | 485 | 0 | 1.0000 | 0.4545 | 0.6250 |
| 31-40 | local | 10% | 925 | 44 | 0.9546 | 0.8669 | 0.9086 |
| 31-40 | local | 20% | 1012 | 926 | 0.5222 | 0.9485 | 0.6735 |
| 31-40 | local_plus_topology | 1% | 97 | 0 | 1.0000 | 0.0909 | 0.1667 |
| 31-40 | local_plus_topology | 5% | 485 | 0 | 1.0000 | 0.4545 | 0.6250 |
| 31-40 | local_plus_topology | 10% | 932 | 37 | 0.9618 | 0.8735 | 0.9155 |
| 31-40 | local_plus_topology | 20% | 1020 | 918 | 0.5263 | 0.9560 | 0.6789 |
| 31-40 | full_supplied | 1% | 97 | 0 | 1.0000 | 0.0909 | 0.1667 |
| 31-40 | full_supplied | 5% | 485 | 0 | 1.0000 | 0.4545 | 0.6250 |
| 31-40 | full_supplied | 10% | 952 | 17 | 0.9825 | 0.8922 | 0.9352 |
| 31-40 | full_supplied | 20% | 1015 | 923 | 0.5237 | 0.9513 | 0.6755 |
| 31-40 | full_plus_topology | 1% | 97 | 0 | 1.0000 | 0.0909 | 0.1667 |
| 31-40 | full_plus_topology | 5% | 484 | 1 | 0.9979 | 0.4536 | 0.6237 |
| 31-40 | full_plus_topology | 10% | 954 | 15 | 0.9845 | 0.8941 | 0.9371 |
| 31-40 | full_plus_topology | 20% | 1016 | 922 | 0.5243 | 0.9522 | 0.6762 |
| 41-49 | local | 1% | 100 | 0 | 1.0000 | 0.1908 | 0.3205 |
| 41-49 | local | 5% | 295 | 204 | 0.5912 | 0.5630 | 0.5767 |
| 41-49 | local | 10% | 322 | 676 | 0.3226 | 0.6145 | 0.4231 |
| 41-49 | local | 20% | 352 | 1643 | 0.1764 | 0.6718 | 0.2795 |
| 41-49 | local_plus_topology | 1% | 100 | 0 | 1.0000 | 0.1908 | 0.3205 |
| 41-49 | local_plus_topology | 5% | 297 | 202 | 0.5952 | 0.5668 | 0.5806 |
| 41-49 | local_plus_topology | 10% | 320 | 678 | 0.3206 | 0.6107 | 0.4205 |
| 41-49 | local_plus_topology | 20% | 354 | 1641 | 0.1774 | 0.6756 | 0.2811 |
| 41-49 | full_supplied | 1% | 100 | 0 | 1.0000 | 0.1908 | 0.3205 |
| 41-49 | full_supplied | 5% | 311 | 188 | 0.6232 | 0.5935 | 0.6080 |
| 41-49 | full_supplied | 10% | 322 | 676 | 0.3226 | 0.6145 | 0.4231 |
| 41-49 | full_supplied | 20% | 345 | 1650 | 0.1729 | 0.6584 | 0.2739 |
| 41-49 | full_plus_topology | 1% | 100 | 0 | 1.0000 | 0.1908 | 0.3205 |
| 41-49 | full_plus_topology | 5% | 310 | 189 | 0.6212 | 0.5916 | 0.6061 |
| 41-49 | full_plus_topology | 10% | 323 | 675 | 0.3236 | 0.6164 | 0.4244 |
| 41-49 | full_plus_topology | 20% | 351 | 1644 | 0.1759 | 0.6698 | 0.2787 |

The operating comparisons are small and mixed. They do not establish a stable material advantage for adding the five topology features to the full supplied representation.

## Additional registered descriptive evidence

- **31-40:** aggregate-only PR-AUC `0.804108`, aggregate+topology `0.810929`, topology-only `0.179917`.
- **41-49:** aggregate-only PR-AUC `0.538538`, aggregate+topology `0.542847`, topology-only `0.059054`.

These secondary descriptive sets show that topology is not a competitive standalone representation here, while small incremental effects can depend on what baseline information is already available.

## Scientific conclusion

**Breakthrough status:** `not_established`.

### Allowed claim

Within the Elliptic dataset and the frozen MIZAN-GATE 0.1A protocol, five completed-snapshot topology features showed a small positive incremental PR-AUC contribution relative to the 93 local supplied predictors in time steps 31-40, but essentially no incremental contribution after the full 165 supplied feature matrix was already available. The registered redundancy contrast was classified as practically neutral under the preregistered ±0.01 PR-AUC margin and did not retain its positive direction in time steps 41-49.

### Claims not supported by 0.1A

- The one-hop aggregate variables and topology variables are mathematically or semantically identical.
- Graph information is universally useful or universally useless for AML.
- The five completed-snapshot topology variables have no information in every representation or time period.
- Completed-snapshot topology was available at transaction decision time.
- The Elliptic result directly generalizes to UAE VASPs or production AML systems.
- Predictive association establishes criminal intent, legal liability, or regulatory compliance.
- MIZAN-GATE 0.1A establishes a universal Graph Utility Boundary.
- MIZAN-GATE 0.1A is a breakthrough result.

## Limitations

- Single public Elliptic dataset.
- Anonymous supplied predictors limit semantic interpretation.
- Transaction nodes are not equivalent to customer or entity graphs.
- Labels are incomplete and class prevalence changes through time.
- The five topology features are simple completed-snapshot statistics.
- Decision-time availability of completed topology is not established in 0.1A.
- The 31-40 and 41-49 windows contain only 10 and 9 time-step blocks respectively.
- Time steps 41-49 were historically known from Study 1 and are not a newly untouched confirmatory sample.
- No external dataset replication is provided by 0.1A.
- No neural graph representation is evaluated in 0.1A.
- No UAE operational transaction data are used.

## Closure interpretation

MIZAN-GATE 0.1A is a valid negative/neutral primary result rather than a failed experiment. The registered practical-materiality criterion was not met, and the positive direction observed in the 31-40 extension did not persist in 41-49. The study therefore narrows the research space without establishing a universal law of graph utility or relational redundancy.

Any subsequent MIZAN-GATE experiment must be designed, frozen, and externally timestamped prospectively. This post-result record must not be used to relabel exploratory follow-up choices as confirmatory 0.1A analyses.
