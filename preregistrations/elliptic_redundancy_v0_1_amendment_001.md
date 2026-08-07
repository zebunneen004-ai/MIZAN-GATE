# MIZAN-GATE 0.1A — Preregistration Amendment 001

**Date:** 2026-08-07
**Experiment:** `elliptic_redundancy_v0_1`
**Status:** Prospective clarification recorded before any MIZAN-GATE 0.1A model results were viewed.

## Purpose

The frozen preregistration specifies the development, extension, and historical evaluation windows but does not explicitly state whether labels from time steps 31–40 may be used to refit a model before evaluating time steps 41–49.

This amendment resolves that implementation ambiguity prospectively. It does not change the research question, feature families, hypotheses, estimands, practical margin, matched seeds, model family, or uncertainty policy.

## Locked training and evaluation policy

### Development analysis

The registered expanding-window folds remain unchanged:

- train 1–10, validate 11–15
- train 1–15, validate 16–20
- train 1–20, validate 21–25
- train 1–25, validate 26–30

### Locked temporal extension

For evaluation on time steps 31–40:

- fit using labeled observations from time steps 1–30 only;
- evaluate on labeled observations from time steps 31–40;
- do not use labels from time steps 31–40 during fitting.

### Historical known-holdout extension

For evaluation on time steps 41–49:

- use models fitted using labeled observations from time steps 1–30 only;
- do not refit using labels from time steps 31–40;
- evaluate on labeled observations from time steps 41–49.

This fixed-training policy is chosen to isolate temporal transport of the registered feature-family contrasts and to prevent an additional model-update step from confounding comparison between the extension and historical windows.

Time steps 41–49 remain historically known Study 1 data and are not described as a newly untouched confirmatory test.

## XGBoost implementation clarification

For every feature set and matched seed:

- use the fixed hyperparameters already registered in `configs/experiments/elliptic_redundancy_v0_1.yaml`;
- use `objective="binary:logistic"`;
- use `eval_metric="logloss"`;
- use `tree_method="hist"`;
- set `random_state` to the matched technical seed;
- compute `scale_pos_weight = n_licit / n_illicit` from that model's training window only;
- use the same observations and training policy across matched feature-set comparisons.

The five seed-level probabilities are averaged observation-wise before calculating the primary PR-AUC estimands.

## Alert-budget implementation clarification

For each registered budget (1%, 5%, 10%, 20%):

- rank observations by predicted probability descending;
- break exact score ties by `txId` ascending;
- alert count is `max(1, ceil(N * budget))`;
- report precision, recall, and F1 at each registered budget;
- no budget is selected post hoc to favor a feature family.

## Scientific status

This amendment is an implementation clarification made before the affected MIZAN-GATE results were viewed. The original hypothesis and primary estimand remain unchanged:

`R = [M(L+T) - M(L)] - [M(F+T) - M(F)]`.
