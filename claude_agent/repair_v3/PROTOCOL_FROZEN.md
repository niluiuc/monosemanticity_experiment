# Frozen protocol: bounded held-out robustness test (repair_v3)

Written after pair selection (step 1) and **before** any prediction-image or final-evaluation outcome is computed. It implements GPT's `SPECIALIST_REVIEW_AND_PROTOCOL_DECISION.md`. The mathematical prediction is in `PREDICTION_STATEMENT.md`.

## Data and firewall

- **Source:** cached ResNet18 (IMAGENET1K_V1) class logits on 4608 CIFAR-10 images, rectified at zero.
- **Train:** rows 0:256. **Calibration:** rows 256:512.
- **Excluded:** rows 512:1024, which earlier pooled analyses used.
- **New pool:** rows 1024:4608, split once by seeded permutation (seed 20261008):
  - S, 896 images (selection);
  - P, 896 images (prediction);
  - E, 1792 images (final evaluation).
- **Reuse disclosure.** The archived 281/207 experiment used rows 512:4608 for that pair only; logits 281 and 207 are excluded here. This is a prospective selected-pair follow-up on reused cached data, not a fresh dataset.
- **What each split is used for:**
  - Normalisation (training RMS) and encoders: train only.
  - Selection biases: train. Deployed biases: calibration.
  - Forecasts: P only.
  - **E is loaded only by `rt_evaluate.py`**, after the frozen file is written and the code hashes are verified.

## Models

- **Code:** energy-one scalar code, tied ReLU decoder, importances (1, 0.5). Feature 1 is the lower logit index.
- **Sharing:** the clean-optimal angle on train (1440-point grid, all local minima refined; competing minima within 1e−6 recorded).
- **Mono:** both orientations fitted. The primary orientation is the one with lower clean training loss; the other is reported as secondary.
- **Noise:** absolute Gaussian code noise σ in training-RMS units. Exact expectation per image.
- **Calibrated policy (primary):** biases refit on calibration at each σ on the grid 0:0.01:1, for every model. Encoders fixed.

## Step 1: selection (done)

Candidate pairs were 12 eligible pairs in seed order: train zero fraction in [0.2, 0.8], logits 281 and 207 excluded, and pairs analysed earlier excluded. The rule was the first two crossing and first two control candidates, classified on S with train-fitted biases (`results/selection.json`).

| Category | Selected |
|---|---|
| Crossing | **one pair, (700, 890)**. Only one of the 12 qualified; reported, not substituted. |
| Control | **(471, 649), (417, 919)** |

The other 9 candidates are reported as is. In 4 of the 12 (all labelled "other"), sharing was already *worse* than mono on clean S images despite being better on train.

## Step 2: forecasts on P (frozen models)

- **Bootstrap:** 2000 joint image resamples of P (seed 20261010). The same resampled images are used for all pairs and all σ.
- **Per pair:**
  - empirical forecast curve Δ_P(σ);
  - σ\*_emp: the first crossing from below zero to at or above zero, by linear interpolation on the 0.01 grid, with no-root resamples retained and coded as ∞;
  - theory forecast σ\*_th = √(G/B), using the B of `PREDICTION_STATEMENT.md` §2 with deployed σ = 0 calibration biases and P images;
  - the applicability fractions.
- **Multiplicity:** the level is Bonferroni over the 3 selected pairs, giving **two-sided 98.33%** intervals and bands (bootstrap percentiles).
- **Precision gate (crossing pair), evaluated per forecast type:**
  - (a) the upper band of Δ_P(0) is below 0;
  - (b) at least 95% of resamples have a crossing in [0.05, 0.9];
  - (c) h = z·√(Var_boot(log σ\*) · (1 + 896/1792)) ≤ 0.20, with z = 2.394.
  - For the theory forecast: B > 0 in at least 95% of resamples, (c) for log σ\*_th, and the applicability fractions ≤ 0.20 (otherwise labelled "outside domain").
- **If no crossing forecast passes the gate, stop before E** and report.

## Step 3: final evaluation on E (only if step 2 permits)

- **Clean ordering (S1):** PASS if the E interval for Δ_E(0) lies below 0; FAIL if above; otherwise INCONCLUSIVE.
- **Crossing forecasts:** D = log σ\*_E − log σ\*_forecast, interval = D ± z·√(Var_P + Var_E), with variances from independent bootstraps.

| Outcome | Condition |
|---|---|
| PASS | Interval inside (−log 1.5, log 1.5) |
| FAIL | Interval outside that range; or no E crossing in [0, 1] while the E band's upper edge is below 0 at min(1, 1.5·σ\*_forecast) |
| INCONCLUSIVE | Otherwise |

- **Controls:** PASS if the E band's upper edge is below 0 on all of [0, 1]; FAIL if the band's lower edge is above 0 at some σ ≤ 1; otherwise INCONCLUSIVE. A PASS means only "no resolved crossing in range".
- **Secondary (reported, not scored):** the frozen-bias policy, and the secondary mono orientation.

## Stopping and diagnostics

Run once. After evaluation, only these are allowed: (a) moment shifts between train/calibration/P and E; (b) checks of Gaussian-moment exactness on P images. No new pairs, σ values, policies, tolerances or networks.

## Pipeline check (retrospective, not evidence)

Pair 281/207 with its archived convention: η = 2/3, absolute σ = 0.730851 × {0, 0.05, 0.1, 0.2, 0.4}, the archived split (calibration biases, rows 512:4608). Compare with the archived calibrated differences, and report the sign of the theory B there.
