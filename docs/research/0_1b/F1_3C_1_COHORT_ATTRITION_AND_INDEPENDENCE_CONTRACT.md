# MIZAN-GATE 0.1B — F1.3C.1 Cohort, Attrition, and Independence Contract

## Status

This is a prospective pre-results scientific-design record.

The rules below are frozen before measuring their resulting cohort sizes,
class-specific attrition, or entity-overlap burden.

No predictive model, predictive metric, graph-utility estimate, or horizon
performance result may be used to change these rules.

## Purpose

F1.3C.1 defines who may enter the MIZAN-GATE 0.1B experiment and how temporal
and entity independence will be enforced.

Its goals are:

1. prevent horizon-specific complete-case cohorts from creating artificial
   performance differences;
2. distinguish mapping/reconstruction failure from legitimate blockchain
   structural absence;
3. preserve chronological evaluation;
4. prevent repeated entities or repeated one-hop transaction structures from
   silently appearing across modeling partitions; and
5. make any resulting attrition visible before predictive modeling.

## Target outcome universe

Only Elliptic targets with a known binary outcome:

- licit; or
- illicit

are eligible as predictive targets.

Elliptic transactions with unknown class remain excluded as predictive
outcomes.

Unknown-class blockchain transactions may still contribute label-free
reconstruction context when they are legitimately observable under the frozen
F1.3A/F1.3B evidence rules.

Their unknown labels are never used as predictive evidence.

## Mapping eligibility

A predictive target must have:

- one structurally valid Elliptic txId;
- one exact mapped Bitcoin transaction hash;
- a resolvable confirmed Bitcoin block height; and
- internally consistent reconstruction identity.

The 965 currently unresolved Elliptic mappings are not assigned guessed hashes.

Unmapped targets are excluded from the reconstructed 0.1B target cohort.

Mapping absence is recorded as attrition, not encoded as a feature.

## Feature-vector validity

A valid target-horizon feature vector requires:

- valid T_b;
- valid C;
- valid A_h;
- valid G_h; and
- finite completed values under the frozen F1.3B.2 numerical rules.

A genuine structural-empty sequence remains valid and receives the
prospectively defined zero summaries.

A reconstruction failure is invalid and never converted to structural zero.

## Primary common-horizon cohort

The primary common cohort requires valid reconstruction for every target at:

- H0;
- H+1;
- H+6;
- H+144; and
- R575059.

A target that is invalid at any one of these horizons is excluded from all
primary-horizon predictive comparisons.

This means primary H0, H+1, H+6, H+144, and R analyses use the same target
membership.

There is no per-horizon complete-case substitution.

This is necessary for paired interpretation of the availability frontier.

## Secondary H+2016 cohort

H+2016 remains a pre-specified secondary sensitivity.

The H+2016 cohort is:

**primary common cohort intersect valid H+2016 reconstruction**

H+2016 is not allowed to reduce the primary H0/H+1/H+6/H+144/R cohort.

When H+2016 is reported, H0 and R must also be re-evaluated on the H+2016
subset for within-cohort sensitivity comparison.

## Historical L comparator cohort

The supplied historical L comparator must use the same target membership as
the corresponding reconstructed analysis.

A larger L-only sample may be reported descriptively, but it may not replace
the matched-cohort L comparison in the primary scientific result.

This prevents sample composition from being confused with feature-family
performance.

## Chronological partitions

Original Elliptic timestep membership defines the chronological partition.

The frozen partitions are:

- development: timesteps 1–30;
- calibration: timesteps 31–35;
- operating: timesteps 36–40;
- historical evaluation: timesteps 41–49.

No random repartition of targets is permitted for the primary analysis.

The 41–49 window must be described as historical evaluation rather than an
untouched holdout because earlier MIZAN/Study-1 work has already inspected it.

## Primary decision-time temporal boundary

For primary decision-time horizons H0 through H+144, earlier-partition
feature evidence must not extend into the target-block period of the next
chronological partition.

At each chronological boundary, define:

- earlier target block height b_i;
- maximum primary decision-time offset = 144 blocks; and
- minimum target block height in the next partition.

The required condition is:

**b_i + 144 < minimum next-partition target block height**

for every earlier-partition target allowed to influence modeling of that next
partition.

If this condition is violated, violating earlier targets are removed in
descending target-block-height order until the condition is satisfied.

This purge uses block height only.

It may not use labels, predictive metrics, feature values, or model behavior.

The resulting temporal-purge count is recorded explicitly.

## H+2016 temporal boundary

H+2016 has its own secondary temporal-independence check using:

**b_i + 2016 < minimum next-partition target block height**

If additional earlier targets must be removed to satisfy this secondary rule,
that creates an H+2016-specific modeling subset.

It does not change the primary H0–H+144 cohort.

## R575059 temporal status

R575059 is intentionally retrospective.

It is not required to satisfy the prospective evidence-time embargo above.

R must never be described as a decision-time-independent or deployment-time
feature horizon.

The entity-independence rules below still apply to R comparisons.

## Direct address entity footprint

For target i, define E_i as the set of unique valid Bitcoin addresses directly
present on the target transaction's:

- input side, after resolving spent outputs; and
- output side.

E_i is identity metadata only.

Raw address strings never become predictive model inputs.

## One-hop transaction footprint

For target i, define X_i using the R575059 relation envelope:

- the target transaction hash itself;
- every immediate predecessor transaction hash; and
- every immediate successor transaction hash

eligible by the frozen R575059 cutoff.

R is used for the independence footprint because it dominates the frozen
relative horizons and therefore gives one common relational-overlap boundary.

The transaction hashes in X_i are identity metadata only.

## Strict chronological entity independence

Strict-inductive partition construction is chronology-first.

Development targets are considered first.

For every target in a later partition, retain it only if both conditions hold:

**E_i intersection prior retained address footprint = empty**

and

**X_i intersection prior retained transaction footprint = empty**

where "prior retained" means targets retained in all chronologically earlier
partitions.

Thus:

- calibration must be unseen relative to retained development;
- operating must be unseen relative to retained development + calibration;
- historical evaluation must be unseen relative to all retained earlier
  partitions.

When a cross-partition conflict exists, the later target is excluded.

Earlier retained targets are not reassigned to later partitions.

This rule is deterministic and may not use class label or predictive result to
choose which side of a conflict survives.

## Why both address and one-hop transaction overlap are checked

Address overlap tests repeated economic/entity identifiers used by A_h.

One-hop transaction overlap tests repeated relational transaction structures
used by G_h.

A later target must pass both to qualify for the strict-inductive analysis.

## Within-partition overlap

Targets inside the same chronological partition are not removed merely because
they share an address or one-hop transaction.

Within-partition dependence must instead be respected later by the uncertainty
and validation procedure.

Any internal cross-validation used later must apply a group/purge rule
consistent with the same identity footprints.

The exact CV implementation is deferred to F1.3D.

## Primary versus secondary entity analysis

The strict-inductive cohort is the primary entity-independence analysis.

A non-purged chronological cohort may be retained as a pre-specified
sensitivity describing the effect of entity recurrence.

It must never replace the strict-inductive result merely because its predictive
performance is larger.

## Attrition accounting

Every excluded target must receive one deterministic primary exclusion reason.

The exclusion-reason precedence is:

1. outcome unknown;
2. mapping unavailable;
3. malformed or non-unique mapping;
4. target block height unresolved;
5. target transaction reconstruction failure;
6. C invalid;
7. primary-horizon A_h reconstruction invalid;
8. primary-horizon G_h reconstruction invalid;
9. historical L row invalid;
10. primary temporal-boundary purge;
11. cross-partition direct-address overlap;
12. cross-partition one-hop transaction-footprint overlap.

Secondary H+2016 exclusions are recorded separately and do not overwrite the
primary exclusion reason.

Multiple diagnostic flags may also be preserved, but only the first applicable
reason in the precedence above is used in the mutually exclusive primary
attrition table.

## Pre-specified reconstruction retention thresholds

Before strict entity purging, the primary common cohort must retain at least:

- 90% of mapped labeled targets overall;
- 90% of mapped illicit targets; and
- 90% of mapped licit targets.

The absolute difference between illicit and licit retention rates must not
exceed 5 percentage points.

These are pre-results feasibility thresholds, not universal scientific laws.

If any threshold fails, predictive modeling remains prohibited.

The failure triggers a documented feasibility review rather than an automatic
change of the threshold.

## Post-purge class support

After temporal/entity purging, every chronological partition used for a
predictive evaluation must contain both licit and illicit targets.

If either class is absent from a required partition, predictive modeling is
prohibited pending an additive pre-results design review.

Exact statistical precision requirements are deferred to F1.3D, where the
uncertainty and estimand design is frozen.

## Attrition reporting

F1.3C.2 must report, before predictive modeling:

- starting Elliptic target count;
- known-label target count;
- mapped known-label count;
- primary common reconstruction count;
- retention rate overall;
- retention by licit/illicit class;
- retention by timestep;
- retention by chronological partition;
- every mutually exclusive primary exclusion reason;
- primary temporal-purge count;
- direct-address overlap exclusions;
- one-hop transaction-overlap exclusions;
- final strict-inductive partition counts;
- class support in every final partition; and
- H+2016 secondary attrition separately.

No predictive metric may appear in the F1.3C.2 feasibility record.

## Cohort immutability

Once F1.3C is formally sealed, target membership may not be changed because:

- a model performs poorly;
- a graph increment is null;
- a horizon is inconvenient;
- a class is difficult;
- a target is an outlier; or
- removing cases improves PR-AUC.

Any later correction must be a documented data-integrity erratum rather than
a performance-driven cohort adjustment.

## Label firewall during cohort construction

Labels may be used only for:

- determining whether a target is a known binary outcome;
- reporting class-specific attrition;
- verifying class support; and
- later supervised modeling after all pre-results gates are complete.

Labels may not be used to:

- choose entity-conflict winners;
- alter temporal purges;
- decide which reconstruction failure to retain;
- select horizons;
- modify the common cohort; or
- tune attrition thresholds.

## Predictive firewall

F1.3C performs no:

- model fitting;
- PR-AUC;
- ROC-AUC;
- predictive F1;
- alert-budget metric;
- graph-utility estimate;
- Delta_G estimate;
- horizon selection from predictive outcome.

## Gate conclusion

The primary decision-time analysis will use a common reconstructed cohort,
strict chronological partitions, block-based prospective temporal purging, and
chronology-first address/one-hop transaction entity independence.

R575059 remains intentionally retrospective rather than being mislabeled as
prospective evidence.

Null, harmful, unstable, or non-monotonic future predictive findings remain
permitted outcomes.
