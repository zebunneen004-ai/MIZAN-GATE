# MIZAN-GATE 0.1B — F1.3D.1 Predictive Estimand, Metric, and Inference Contract

## Status

This is a prospective pre-results analysis contract.

It is created before:

- infrastructure provisioning;
- full reconstructed-cohort attrition measurement;
- study feature-value inspection;
- predictive model fitting; and
- predictive performance inspection.

The purpose is to prevent metric, model, horizon, uncertainty, and
multiplicity choices from adapting to later results.

## Scientific question

MIZAN-GATE 0.1B asks:

How much apparent incremental one-hop relational utility changes when evidence
is constrained to a declared observation epoch rather than allowing the
benchmark-construction-aligned retrospective evidence envelope?

The primary question is an availability question, not merely whether graph
features can predict illicit transactions.

## Positive outcome

The positive predictive class is:

**illicit = 1**

The negative class is:

**licit = 0**

Unknown-label transactions are never predictive outcomes.

## Frozen feature-set shorthand

The F1.3B.2 shorthand is inherited.

B(h), the non-graph point-in-time baseline, means:

**T_b + C + A_h**

G(h), the graph-augmented point-in-time model, means:

**T_b + C + A_h + G_h**

C-only means:

**T_b + C**

Historical L means:

**T_b + L**

All paired comparisons use identical eligible target membership.

## Frozen horizon set

Primary frontier horizons:

- H0
- H+1
- H+6
- H+144
- R575059

Secondary sensitivity:

- H+2016

No horizon may be dropped, inserted, or selected because of predictive
performance.

## Primary model family

The sole primary predictive model family is XGBoost binary classification.

The primary model is deliberately fixed rather than retuned after seeing
0.1B cohort or performance results.

Frozen parameters:

- objective = binary:logistic
- n_estimators = 300
- max_depth = 8
- learning_rate = 0.15
- subsample = 0.85
- colsample_bytree = 0.85
- min_child_weight = 10
- gamma = 0
- reg_alpha = 1
- reg_lambda = 2
- tree_method = hist
- device = cpu
- n_jobs = 1

Frozen random seeds:

**11, 23, 42, 71, 101**

A separate model is fitted for each feature family and horizon.

For each target, the five seed-specific predicted illicit probabilities are
averaged first.

All metrics and paired estimands are then computed from this averaged
probability.

Seed-specific metrics may be retained diagnostically but are not substituted
for the frozen probability-ensemble estimand.

## No model-family shopping

F1.3D.1 does not authorize:

- GNNs;
- random forests;
- neural networks;
- alternative boosting libraries;
- post-result logistic-regression substitution;
- post-result hyperparameter search; or
- choosing whichever model makes graph evidence look strongest.

A separate prospectively frozen study would be required to make another model
family confirmatory.

## Predictive preprocessing

The primary XGBoost analysis consumes the valid raw numeric T_b/C/A_h/G_h
features generated under F1.3B.2.

There is:

- no whole-dataset normalization;
- no test-fitted transformation;
- no outcome-guided feature selection;
- no post-result feature deletion; and
- no predictive zero-imputation of reconstruction failures.

Targets with reconstruction-invalid feature vectors are governed by the
already frozen F1.3C cohort rules.

## Chronological fitting and evaluation

The inherited chronological partitions remain:

- development: timesteps 1–30;
- calibration: timesteps 31–35;
- operating: timesteps 36–40;
- historical evaluation: timesteps 41–49.

Primary models are trained using the retained strict-inductive development
targets.

The primary model is not refitted on calibration, operating, or historical
evaluation outcomes before their predictions are generated.

Calibration 31–35 is reported as an intermediate chronological diagnostic
window.

Operating 36–40 is the primary predictive evaluation window.

Historical evaluation 41–49 is a pre-specified secondary replication window.

The 41–49 window is not described as untouched.

The same fixed model architecture and comparison definitions are used in all
windows.

## Primary predictive metric

The primary predictive metric is:

**Average Precision (AP)**

computed from the continuous predicted illicit score.

The implementation contract is equivalent to:

**sklearn.metrics.average_precision_score**

with illicit as the positive class.

For this study, AP is the exact operational meaning of the phrase
"PR-AUC" when that shorthand is used.

Trapezoidal interpolation of the precision-recall curve is not substituted for
AP.

## Secondary predictive metric

ROC-AUC is secondary.

ROC-AUC may provide ranking context but may not replace AP as the primary
metric merely because it appears more favorable.

## Horizon-specific graph increment

For horizon h, define:

**Delta_G(h) = AP[G(h)] - AP[B(h)]**

That is:

**Delta_G(h) =
AP(T_b + C + A_h + G_h)
-
AP(T_b + C + A_h)**

Positive Delta_G(h) indicates better AP after adding the frozen one-hop
relational family at the same observation horizon and on the same targets.

Negative Delta_G(h) is permitted.

## Address-history increment

For horizon h, define the secondary mechanistic quantity:

**Delta_A(h) =
AP(T_b + C + A_h)
-
AP(T_b + C)**

Delta_A is secondary and does not alter the primary graph-availability
hypothesis.

## Primary availability-gap estimand

The single confirmatory 0.1B estimand is:

**A_G =
Delta_G(R575059) - Delta_G(H0)**

evaluated in the strict-inductive operating window on the frozen common
primary cohort.

Interpretation:

- A_G > 0 means the measured graph increment is larger under the retrospective
  evidence envelope than at the frozen H0 decision epoch;
- A_G = 0 means no measured availability gap in graph increment;
- A_G < 0 means the graph increment is smaller under the retrospective
  evidence envelope.

No monotonicity is assumed.

## Why A_G is primary

A_G directly targets the 0.1B research question.

It separates:

1. the incremental effect of adding G_h over the same-horizon non-graph
   baseline; and
2. the change in that increment between H0 and the retrospective envelope.

The study therefore does not declare success merely because G(R) has high
absolute AP.

## Practical materiality

The frozen absolute AP materiality threshold is:

**0.01**

For A_G:

- estimate >= +0.01 with a confidence interval excluding zero in the positive
  direction is evidence consistent with a practically material positive
  availability gap;
- positive estimate below +0.01 is practically small under this contract even
  if statistically distinguishable from zero;
- an interval containing zero is statistically uncertain;
- negative values remain reportable and scientifically valid.

The 0.01 threshold is a study-specific interpretive threshold, not a universal
AML law.

## Decision-time graph utility at H0

Delta_G(H0) is a key secondary estimand.

It asks whether one-hop relational evidence available by the end of the
target's confirmation block adds predictive ranking value over T_b+C+A_H0.

A materially positive A_G does not by itself establish useful decision-time
graph utility.

Likewise, a positive Delta_G(H0) does not establish that retrospective
availability bias exists.

Both quantities are reported separately.

## Frontier reporting

The complete primary frontier reports:

- Delta_G(H0)
- Delta_G(H+1)
- Delta_G(H+6)
- Delta_G(H+144)
- Delta_G(R575059)

in the frozen order.

H+2016 is a secondary sensitivity and is reported separately on its
pre-specified secondary cohort.

No best horizon is selected.

No horizon is called optimal based on these results.

## Historical L comparator

Historical L is reported on the matched cohort.

It remains a historical comparator rather than a decision-time-safe feature
family.

Relevant quantities may include:

- AP(T_b + L);
- AP difference versus T_b + C;
- AP difference versus T_b + C + A_R + G_R.

These are secondary/descriptive.

L is not inserted into the primary A_G formula.

## Alert-budget operating summaries

Operational ranking summaries are secondary.

Frozen alert-budget fractions are:

- 0.5%
- 1%
- 2%
- 5%

For evaluation size n and budget fraction q, the alert count is:

**max(1, ceiling(q × n))**

Targets are sorted by:

1. predicted illicit probability descending; then
2. Elliptic txId ascending as a deterministic metadata-only tie break.

At each budget report:

- number alerted;
- illicit targets captured;
- recall at budget;
- precision at budget; and
- lift over evaluation-set illicit prevalence.

For graph-versus-non-graph comparisons, also report paired differences in
recall and precision at the same budget.

Alert-budget results are secondary and cannot override the primary AP
estimand.

## Dependence-aware uncertainty

All uncertainty calculations are paired.

The same resampled targets or clusters are used simultaneously for all model
variants entering an estimand.

### Primary entity-component bootstrap

Within each evaluation partition construct an undirected target-dependence
graph.

Connect two retained targets if they share either:

- at least one direct-address identity in their frozen E footprints; or
- at least one transaction identity in their frozen X footprints.

Connected components of this graph are the primary bootstrap clusters.

This uses identity metadata only, not labels or predictions, to construct the
clusters.

For each bootstrap replicate:

1. sample the same number of connected components with replacement;
2. include every target in each sampled component;
3. preserve duplicate sampled components as repeated bootstrap observations;
4. compute both sides of every paired estimand on the identical replicate.

Use:

**5,000 valid bootstrap replicates**

with bootstrap random seed:

**301**

A replicate lacking either predictive class is discarded and redrawn.

## Bootstrap estimability safeguard

Inferential confidence intervals require:

- at least 20 entity-dependence components in the evaluation window; and
- at least two components containing illicit targets.

If this safeguard fails, the corresponding estimand remains descriptive and
must not be presented with a conventional inferential claim.

The threshold is frozen before observing the component counts.

## Primary confidence interval

The primary A_G interval is the paired 95% percentile interval from the
entity-component bootstrap.

The point estimate is always the full eligible evaluation-sample estimate,
not the bootstrap mean.

## Temporal-block sensitivity

A paired timestep-block bootstrap is a pre-specified dependence sensitivity.

Evaluation timesteps, rather than individual targets, are resampled with
replacement.

All targets from a sampled timestep enter together.

Use:

- 5,000 valid replicates;
- seed 302.

This sensitivity does not replace the entity-component bootstrap merely
because one produces a more favorable interval.

Material disagreement between the two uncertainty approaches must be reported.

## Multiplicity hierarchy

There is exactly one confirmatory inferential estimand:

**A_G in operating timesteps 36–40**

Therefore no multiplicity correction is applied to that single primary
quantity.

All of the following are secondary:

- horizon-specific Delta_G values;
- Delta_A values;
- ROC-AUC differences;
- alert-budget differences;
- calibration-window results;
- historical-evaluation results;
- L comparisons;
- H+2016 sensitivity;
- temporal-block-bootstrap sensitivity.

Secondary confidence intervals may be shown, but no collection of unadjusted
secondary p-values may be promoted as multiple confirmatory discoveries.

The study does not search across secondary outputs for a favorable
"significant" result.

## Historical replication interpretation

The same A_G formula is evaluated in timesteps 41–49 as a pre-specified
secondary historical replication.

Agreement in sign and magnitude strengthens evidence of stability.

Disagreement is reported directly.

A favorable historical result does not retroactively convert a failed
operating primary result into a confirmatory success.

## Calibration-window role

Timesteps 31–35 provide chronological diagnostic reporting.

They are not used to choose:

- horizons;
- model families;
- hyperparameters;
- materiality threshold;
- alert-budget fractions; or
- the primary metric

after results are observed.

No post-result calibration-window tuning is permitted.

## Predictive result hierarchy

The result interpretation order is frozen as:

1. feasibility and cohort validity;
2. A_G operating point estimate and uncertainty;
3. practical materiality of A_G;
4. Delta_G(H0);
5. full graph-availability frontier;
6. historical replication;
7. Delta_A mechanism;
8. alert-budget summaries;
9. L historical comparator.

Lower-level results cannot overwrite a failure at a higher-level gate.

## No universal graph claim

Even a strong positive result is restricted to:

- Elliptic;
- the mapped/reconstructed cohort;
- the frozen post-confirmation block-end epoch;
- the frozen one-hop relational family;
- the frozen model and evaluation design.

It cannot establish that graph ML is universally useful or useless.

## Breakthrough language

F1.3D.1 itself establishes no breakthrough.

A later positive empirical result may support language such as:

"evidence consistent with a material decision-time availability gap in
incremental one-hop relational utility within the reconstructed Elliptic
setting."

It may not support universal or "first-ever" claims without separate evidence.

## Predictive firewall

This gate performs no:

- cohort attrition measurement;
- feature-value computation;
- model fitting;
- AP computation;
- ROC-AUC computation;
- bootstrap computation;
- alert-budget computation;
- Delta_G computation;
- Delta_A computation;
- A_G computation.

## Gate conclusion

The primary confirmatory 0.1B estimand is prospectively fixed as:

**A_G =
[AP(T_b+C+A_R+G_R) - AP(T_b+C+A_R)]
-
[AP(T_b+C+A_H0+G_H0) - AP(T_b+C+A_H0)]**

in the strict-inductive operating window.

All model, metric, materiality, bootstrap, horizon, and interpretation choices
above are fixed before predictive results are observed.
