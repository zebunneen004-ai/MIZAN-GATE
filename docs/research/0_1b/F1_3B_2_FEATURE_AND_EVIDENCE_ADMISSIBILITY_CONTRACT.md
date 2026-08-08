# MIZAN-GATE 0.1B — F1.3B.2 Feature and Evidence Admissibility Contract

## Status

This is a prospective pre-results scientific-design record.

It is intended to become frozen only after exact artifact review, repository
commit, remote anchoring, and exact-SHA continuous-integration success.

No MIZAN-GATE 0.1B predictive feature values, labels, model results, or
predictive metrics have been inspected in selecting this contract.

## Purpose

This contract defines exactly what evidence may enter the decision-time-safe
MIZAN-GATE 0.1B feature representation.

It freezes the semantic and admissibility boundary between:

- T_b: universal target-height context control;
- C: transaction-intrinsic target features;
- A_h: point-in-time target-address history;
- G_h: point-in-time one-hop relational evidence; and
- L: the supplied historical Elliptic predictor matrix.

The contract is intentionally fixed before predictive experimentation.

## Inherited observation horizons

F1.3B.2 does not reopen F1.3A.

For target transaction i with confirmed block height b_i:

- H0 cutoff: b_i
- H+1 cutoff: b_i + 1
- H+6 cutoff: b_i + 6
- H+144 cutoff: b_i + 144
- secondary H+2016 cutoff: b_i + 2016
- retrospective R cutoff: absolute Bitcoin block 575059

All cutoffs are inclusive.

H0 remains the end of the target transaction's confirmation block.

Same-block evidence is therefore eligible at H0.

No within-block transaction order is required for the primary experiment.

## Universal target-height context control T_b

A single target-context control is frozen:

**T_b(i) = b_i**

T_b is:

- the target transaction's confirmed Bitcoin block height;
- available at H0;
- horizon-invariant for a target;
- included in every predictive model matrix used for 0.1B comparisons; and
- not counted as part of C, A_h, G_h, or L.

The purpose is control, not graph evidence.

The recovered G_h semantic family contains summaries of neighboring
transaction block heights. Without a universal target-height control, a model
receiving G_h could receive a coarse calendar-position proxy not provided to
its non-graph comparator.

Accordingly, whenever this study uses shorthand such as:

**M(C + A_h)**

the actual predictive matrix is understood as:

**M(T_b + C + A_h)**

Likewise:

**M(C + A_h + G_h)**

means:

**M(T_b + C + A_h + G_h)**

and historical L comparisons use T_b as the same universal context control.

T_b is not a substitute for strict chronological evaluation.

## C — transaction-intrinsic safe core

C contains exactly 18 predictors.

The recovered legacy feature identities are:

**2, 3, 5, 6, 7, 9–15, 17–22**

The three unresolved transaction-scoped legacy predictors:

**4, 8, 16**

are excluded.

C is recomputed from the raw reconstructed target transaction.

C does not copy supplied normalized Elliptic values.

C is horizon-invariant:

**C_i(h) = C_i**

for all frozen horizons.

### C semantic order

C uses the following fixed order:

1. Feature 2 — transaction volume
2. Feature 3 — fees
3. Feature 5 — number of inputs
4. Feature 6 — number of outputs
5. Feature 7 — number of unique input addresses
6. Feature 9 — minimum input value
7. Feature 10 — maximum input value
8. Feature 11 — standard deviation of input values
9. Feature 12 — mean input value
10. Feature 13 — Pearson correlation of input values with input positions
11. Feature 14 — Spearman correlation of input values with input positions
12. Feature 15 — number of unique output addresses
13. Feature 17 — minimum output value
14. Feature 18 — maximum output value
15. Feature 19 — standard deviation of output values
16. Feature 20 — mean output value
17. Feature 21 — Pearson correlation of output values with output positions
18. Feature 22 — Spearman correlation of output values with output positions

### C units

Bitcoin monetary values are represented internally in integer satoshis before
conversion to floating-point summary statistics where mathematically needed.

Counts are integer counts.

Correlations are dimensionless.

No USD price conversion belongs to the frozen C family.

## A_h — point-in-time address-history family

A_h contains exactly 72 predictors corresponding to recovered legacy
Features 23–94.

For target i and observation cutoff c(i,h), every target input/output address
state used in A_h must be computed using blockchain evidence with:

**block_height <= c(i,h)**

No transaction above the cutoff may contribute to the address state.

### Address occurrence sequences

Input-address and output-address sequences are treated separately.

Address occurrences are preserved in target transaction order.

They are not automatically deduplicated before aggregation.

If the same address occurs multiple times in the target input/output sequence,
its point-in-time state occurs multiple times in the corresponding sequence.

Address strings themselves are never predictive features.

### A_h base attributes

For each eligible target-address occurrence, the six point-in-time base
attributes are:

1. cumulative received satoshis;
2. cumulative sent satoshis;
3. available balance in satoshis;
4. cumulative incoming transaction count;
5. cumulative outgoing transaction count; and
6. lifetime in seconds.

Balance is frozen as:

**received_satoshis - sent_satoshis**

Lifetime is frozen as:

**last_seen_timestamp - first_seen_timestamp**

All state is inclusive through the requested observation block.

Because H0 is an end-of-target-block epoch, the target transaction itself may
contribute to the H0 address state.

### A_h six-operator schema

For each base attribute, separately over input-address occurrences and
output-address occurrences, compute in this order:

1. minimum;
2. maximum;
3. sample standard deviation;
4. arithmetic mean;
5. Pearson correlation with occurrence position; and
6. Spearman correlation with occurrence position.

This produces:

**6 attributes × 6 operators × 2 directions = 72 predictors**

The resulting feature order follows recovered legacy Feature IDs 23–94.

## G_h — point-in-time one-hop relational family

G_h contains exactly 60 predictors.

It corresponds to recovered one-hop legacy semantic Features:

**95–112, 119–148, and 155–166**

The unresolved neighborhood Features:

**113–118 and 149–154**

are excluded.

G_h is explicitly a **relational evidence** family.

It must not be described as pure graph topology.

## One-hop relation definition

Only immediate transaction relations to the target are primary.

No two-hop, three-hop, PageRank, k-core, clustering, weak-component, GNN
embedding, or other extended topology is part of the primary F1.3B.2 G_h
contract.

A separate prospective amendment would be required before predictive results
are inspected to add such a secondary family.

### Predecessor relation occurrence

Each target vin reference with a valid predecessor transaction identifier
defines a predecessor relation occurrence.

The occurrence order follows target vin order.

A predecessor transaction referenced through more than one relation may occur
more than once.

### Successor relation occurrence

Each target vout that is spent by an identifiable transaction defines a
successor relation occurrence only when the spending transaction satisfies the
frozen observation cutoff.

The occurrence order follows target vout order.

Multiple relation occurrences to the same neighboring transaction remain
multiple occurrences.

This is an edge/relation-occurrence representation rather than an automatic
unique-neighbor set.

### Relation eligibility

For target i at cutoff c(i,h), neighbor evidence is admissible only if the
neighbor transaction block height satisfies:

**neighbor_block_height <= c(i,h)**

This rule applies independently of whether the reconstruction substrate has
already fetched later transactions.

The upstream graph expansion is therefore reconstruction infrastructure, not
the scientific evidence cutoff.

Post-cutoff relations must be rejected by the MIZAN feature-composition layer.

At H0, same-block predecessor or successor relations are eligible because the
primary epoch is the end of the target block.

## G_h base attributes

For each eligible one-hop neighbor transaction occurrence, use exactly:

1. transaction value in satoshis;
2. confirmed Bitcoin block height;
3. transaction fee in satoshis;
4. number of transaction inputs; and
5. number of transaction outputs.

These attributes are label-free.

No neighbor class, label, illicit score, investigator annotation, address-risk
score, or downstream model output is admissible.

### G_h six-operator schema

For each base attribute, separately over predecessor and successor relation
occurrences, compute:

1. minimum;
2. maximum;
3. sample standard deviation;
4. arithmetic mean;
5. Pearson correlation with relation position; and
6. Spearman correlation with relation position.

This produces:

**5 attributes × 6 operators × 2 directions = 60 predictors**

Feature order follows recovered legacy Feature IDs, excluding the 12
unresolved neighborhood positions.

## Why absolute neighbor block height remains in G_h

The recovered semantic family includes neighboring transaction block height,
so F1.3B.2 retains it for semantic comparability.

However, target block height T_b is included universally in every model.

Therefore G_h is not the only feature family granted direct access to coarse
target calendar position.

Any later relative-height sensitivity must be prospectively specified before
predictive inspection rather than substituted after results are observed.

## Numerical sequence convention

The exact sequence convention applies to C sequence summaries, A_h sequences,
and G_h sequences.

Positions are deterministic ordinal positions:

**0, 1, ..., n-1**

Using one-based rather than zero-based positions would not change Pearson or
Spearman correlation, but zero-based positions are frozen for implementation
clarity.

Sequence order must never be sorted by the value being summarized.

## Standard deviation

For sequence length n >= 2:

- use the sample standard deviation;
- use an N-1 denominator.

For n = 0 or n = 1:

- standard deviation is defined as 0 under the MIZAN contract.

This deterministic edge-case convention overrides any library NaN behavior.

## Pearson correlation

For n >= 2 with non-zero variance in both:

- the value sequence; and
- the ordinal-position sequence,

compute ordinary Pearson product-moment correlation.

If n < 2, return 0.

If the value sequence is constant, return 0.

No NaN or infinity is permitted as a finished feature value.

## Spearman correlation

Spearman is computed as Pearson correlation over ranks.

Ties use average ranks.

If n < 2, return 0.

If the ranked value sequence has zero variance, return 0.

No NaN or infinity is permitted as a finished feature value.

## Structural empty sequences

A structurally empty sequence is one in which the required blockchain
structure genuinely has zero eligible occurrences.

Examples include:

- no eligible predecessor relation;
- no successor relation observed by a given horizon; or
- no address-bearing occurrence for the relevant direction.

For a structurally empty sequence, all six summary outputs are defined as:

**0**

Structural-empty status must additionally be retained in QA/audit metadata,
but the QA flag is not automatically added as a predictive feature.

## Structural absence is not reconstruction missingness

A zero-occurrence structural sequence is scientifically different from a
failed or incomplete reconstruction.

If source data required to determine C, A_h, or G_h are unavailable,
unresolved, malformed, inconsistent, or incompletely reconstructed:

- do not substitute zero;
- do not substitute a shorter horizon;
- do not substitute a later horizon;
- do not fetch above the frozen cutoff to fill the value;
- mark the target-horizon feature vector as reconstruction-missing or invalid.

The final target/common-cohort treatment of those cases is reserved for the
prospective F1.3C cohort/attrition contract.

## Arithmetic consistency failures

The feature composer must reject, rather than silently wrap or coerce:

- impossible negative balance produced by unsigned underflow;
- non-finite completed feature values outside explicitly defined degenerate
  cases;
- malformed monetary values;
- missing required neighbor heights;
- inconsistent reconstructed transaction identifiers.

Such conditions are QA/reconstruction failures, not legitimate structural
zeros.

## Raw construction before preprocessing

F1.3B.2 freezes raw decision-time feature construction.

It does not permit whole-dataset z-score normalization or other preprocessing
during feature reconstruction.

Any scaling, transformation, imputation, encoding, or preprocessing used by a
predictive model must be frozen later and fitted using training data only.

The point-in-time feature builder must not use test-window distributional
statistics.

## L — supplied historical comparator

L contains the original 165 supplied Elliptic predictor columns corresponding
to semantic Feature IDs:

**2–166**

Feature 1 / Elliptic time step is not part of L.

L is retained only as a historical benchmark comparator.

L is not called:

- decision-time-safe;
- point-in-time-safe;
- leakage-free; or
- an exact reconstruction of C + A_R + G_R.

The 15 unresolved predictor positions remain present inside L because L is the
unaltered supplied historical comparator.

They remain excluded from the recomputed C/A_h/G_h representation.

When L is evaluated predictively in 0.1B, T_b remains the same universal
context control.

## No identity predictors

The following are metadata, not predictors:

- Elliptic txId;
- Bitcoin transaction hash;
- raw address strings;
- database row identifiers;
- split identifiers;
- class labels.

They may be used for joins, reconstruction, independence checks, or audit
records only.

## Label firewall

No label-derived information may enter C, A_h, G_h, or T_b.

Forbidden examples include:

- target class as an input;
- neighbor class;
- illicit-neighbor counts;
- label propagation;
- supervised address-risk scores;
- investigator annotation;
- model predictions generated using labels outside the allowed training
  procedure.

Labels remain outcomes for later predictive evaluation.

## Primary feature-set shorthand

The following shorthand omits universal T_b only for readability.

When later defined by the predictive preregistration:

**C**
means
**T_b + C**

**C + A_h**
means
**T_b + C + A_h**

**C + A_h + G_h**
means
**T_b + C + A_h + G_h**

**L**
means
**T_b + L**

This convention must be documented wherever 0.1B results are reported.

## Frozen primary one-hop boundary

The primary 0.1B relational question is deliberately narrow:

Does point-in-time one-hop relational evidence add predictive information
beyond the transaction-intrinsic and point-in-time address-history baseline?

F1.3B.2 does not permit post-result expansion of G_h merely because the
one-hop result is null.

A future deeper-graph study remains possible, but it is a distinct prospective
analysis.

## Fixed feature ordering

Feature ordering is frozen as:

1. universal T_b control;
2. C in ascending recovered legacy Feature-ID order;
3. A_h in ascending recovered legacy Feature-ID order;
4. G_h in ascending recovered legacy Feature-ID order after removal of the
   unresolved positions.

L preserves the supplied Elliptic predictor order, preceded by universal T_b
when used in a predictive matrix.

## Recomputed predictor accounting

Decision-time reconstruction:

- C = 18
- A_h = 72
- G_h = 60
- total recomputed semantic predictors = 150

Universal context control:

- T_b = 1

Thus the complete graph model contains:

**151 columns before later preprocessing: T_b + C + A_h + G_h**

The non-graph point-in-time baseline contains:

**91 columns: T_b + C + A_h**

The intrinsic baseline contains:

**19 columns: T_b + C**

Historical comparator:

**166 columns: T_b + L**

These counts are identities, not claims about predictive performance.

## Unresolved semantic features

Exactly 15 supplied predictor semantics remain excluded from the recomputed
representation:

**4, 8, 16, 113–118, 149–154**

MIZAN does not guess their meaning.

MIZAN does not replace them with convenient proxy variables in the primary
reconstruction.

## What F1.3B.2 freezes

Upon formal seal, this contract freezes:

- T_b as universal target-height control;
- C = 18;
- A_h = 72;
- G_h = 60;
- L = 165;
- the 15 unresolved exclusions from recomputed features;
- one-hop relation depth;
- relation-occurrence rather than automatic unique-neighbor semantics;
- predecessor and successor direction separation;
- inclusive block-height admissibility;
- address-history cutoff semantics;
- satoshi monetary units;
- lifetime in seconds;
- six-operator summary order;
- sample standard deviation with N-1 denominator;
- average-rank Spearman ties;
- deterministic zero handling for structural/degenerate sequences;
- hard separation of reconstruction failure from structural absence;
- fixed feature ordering;
- label firewall;
- raw-before-preprocessing construction;
- no extra topology in the primary 0.1B G_h family.

## What remains unresolved after F1.3B.2

F1.3B.2 does not freeze:

- common eligible cohort;
- attrition thresholds;
- mapping-failure treatment at study level;
- address/entity independence rules;
- exact chronological split;
- model family;
- predictive hyperparameters;
- preprocessing implementation;
- primary predictive metric;
- practical materiality threshold;
- uncertainty procedure;
- multiplicity treatment;
- alert-budget reporting;
- final runtime infrastructure minimum.

Those remain prospective later gates.

## Predictive firewall

F1.3B.2 performs no:

- feature-value computation on the Elliptic study cohort;
- label loading;
- PR-AUC;
- ROC-AUC;
- predictive F1;
- alert-budget evaluation;
- model fitting;
- graph-utility calculation;
- Delta_G calculation.

No breakthrough claim follows from this contract.

## Commercial firewall

This feature contract is a research methodology.

It does not establish commercial effectiveness, customer willingness to pay,
regulatory acceptance, or revenue.

Commercial interpretation remains downstream of empirical validation.

## Gate conclusion

F1.3B.2 converts the decision-time evidence concept into an auditable
feature-level admissibility contract.

The primary point-in-time graph comparison is prospectively constrained to:

**T_b + C + A_h**

versus:

**T_b + C + A_h + G_h**

where G_h contains only admissible one-hop label-free relation evidence
observable at the frozen horizon.

The result is allowed to be positive, null, harmful, unstable, or
non-monotonic across horizons.

No predictive outcome has been inspected in defining this contract.
