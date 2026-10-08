# Draft protocol: held-out robustness boundary on one existing network (not yet run)

*Status: a draft for review. Nothing below has been executed, and no test-split number has been looked at.*

## 1. Question (the original Project 1 target)

For a fixed pair of real features, does sharing beat monosemantic retention in **clean held-out** reconstruction risk? And at what code-noise level σ does corruption **reverse** that advantage, if at all?

The test is whether a quantitative prediction, computed only from training and calibration images under the actual feature distribution, matches what is measured on untouched test images.

## 2. Data: one existing network, no new extraction

- **Source.** The cached ResNet18 (IMAGENET1K_V1) class logits on 4608 CIFAR-10 images, `project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy`, rectified at zero. This is the same checkpoint and the same seed-20261007 splits as the archived head experiment.
- **Splits (already fixed and disjoint).** Train 256, calibration 256, test 4096 images (`targets.npz` indices).
- **Normalisation.** Each feature is divided by its *training* RMS.
- **Firewall.** Test images are used only in step 6. All selection, fitting and prediction use train and calibration only.

## 3. Models (the manuscript's comparison, unchanged)

- **Code.** Energy-one scalar code h = w·x + σZ with tied ReLU decoder x̂_i = ReLU(w_i h + b_i). Importance (1, η = 0.5).
- **Sharing.** The clean-optimal angle on the *training* images. Search: the repaired dense grid with refinement of all local minima (`repair_v1/fra2_v2.py` logic applied to the empirical distribution), with exact per-image bias profiling.
- **Mono.** w = (1, 0): feature 1 is retained and feature 2 is predicted by its best constant.
- **Corruption.** Scalar Gaussian code noise. Risk is computed in exact expectation over Z per image (no Monte Carlo).
- **Primary policy: calibrated.** For each σ, the biases of *both* models are refit on the calibration images under the noisy loss; the encoders stay fixed at their clean training values. The frozen-bias policy is reported as secondary.
- **Outcome.** Δ(σ) = R_share(σ) − R_mono(σ), the importance-weighted reconstruction MSE on test images. Δ < 0 means sharing is better.
- **σ grid,** fixed now, in training-RMS units: {0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0}. The crossing σ\* is found by root-finding on [0, 1] (the risk is exact, so any σ can be evaluated).

## 4. Quantitative prediction, computed before any test evaluation

For each selected pair:

1. **Encoder** from the training images.
2. **Predicted curve Δ_pred(σ)** by 2-fold cross-fitting on the calibration images: fit the noisy biases on one half, evaluate on the other half, and average both directions. This makes the prediction out of sample for the biases.
3. **Predicted crossing σ\*_pred:** the first root of Δ_pred on [0, 1], or "no crossing".
4. **Uncertainty:** 500 bootstrap resamples of the train and calibration images, refitting the encoder and biases each time. This gives 95% intervals for Δ_pred at each grid σ and for σ\*_pred, plus the fraction of resamples with no root.
5. **Secondary theory prediction (not a success criterion):** σ\*_th = √(G/B). Here G = −Δ_pred(0) is the clean sharing gain, and B is the small-σ coefficient of the calibrated penalty (Δ_pred(σ) − Δ_pred(0))/σ² at σ = 0.02. This tests whether the theory's "clean gain versus quadratic noise penalty" balance carries over to the real distribution.

All predictions are saved and hashed before step 6.

## 5. Pair selection: deterministic, train and calibration only, bounded

- **Pool.** 300 random eligible pairs (seed 20261008). Eligible means a training zero-fraction in [0.2, 0.8] for both features, excluding the archived pair 281/207.
- **Pre-screen** with the point predictions (step 4, items 1–3, without bootstrap).
- **Crossing pairs (2).** Among pairs with Δ_pred(0) < 0 and σ\*_pred ∈ [0.1, 0.8], take the 10 with the largest clean gain −Δ_pred(0). Bootstrap those, and choose the 2 with the narrowest σ\*_pred interval.
- **Control pairs (2).** Among pairs with Δ_pred(σ) < 0 on the whole grid, take the 2 with the largest minimum margin max_σ Δ_pred(σ) < 0 after bootstrap. These are predicted to have no reversal.
- **Fixed at 4 pairs.** No substitution after the test.
- **Retrodiction (pipeline check only, not evidence).** Apply step 4 to the archived pair 281/207. Its archived held-out result had no reversal up to multiplier 0.4. Report whether the prediction agrees.

## 6. Test and success criteria

Compute Δ_test(σ) on the 4096 test images. Use the training encoder and biases refit on the *full* calibration split, both fixed before the test. Report pointwise test uncertainty with a paired bootstrap over test images, conditional on the fitted models.

| Criterion | Pass condition |
|---|---|
| **S1, clean ordering** | sign Δ_test(0) = sign Δ_pred(0), when the predicted interval excludes 0 |
| **S2, crossing (primary)** | Crossing pairs: σ\*_test lies inside the 95% σ\*_pred interval. Control pairs: no test root on [0, 1] |
| **S3, pointwise signs** | At every grid σ whose predicted interval excludes 0, sign Δ_test matches |

- **Overall:** success if all 4 pairs pass S1 and S2. Each pair is reported separately.
- **Secondary:** the error of σ\*_th = √(G/B) against σ\*_test. The frozen policy is reported, not tested.

## 7. Stopping rule and failure handling

- **Run once.** If any criterion fails, report the failure as the result.
- **Then run only these four pre-listed diagnostics:**
  - (a) the shift in feature moments (means, variances, zero fractions, covariance) between train/calibration and test;
  - (b) cross-fit versus full-calibration biases;
  - (c) the bootstrap spread of the encoder angle, i.e. encoder instability;
  - (d) a check of the exact Gaussian-moment risk against Monte Carlo on 3 test images.
- **No new pairs, σ values, policies, representations or networks** may be added in search of a crossing.
- More networks can be added later, only to replicate a successful result.

## 8. What this does and does not test

- **It tests** whether the model-class computation (exact clean selection plus calibrated Gaussian code-noise risk) predicts the **held-out** clean advantage and its corruption reversal on real features.
- **It does not test** robustness of the native ResNet to input corruptions, adversarial robustness, or the Bernoulli critical exponents.
- **It uses one network.** Results are about these feature pairs, not a population of networks.

## 9. Reviewer questions

1. Is 2-fold cross-fitting on the calibration images an acceptable out-of-sample prediction, or should a train/calibration split of the training images be used instead?
2. Are 4 pairs (2 crossing, 2 control) enough as a first bounded test?
3. Should the primary policy be calibrated (as here) or frozen?
