# Statistics review of `repair_v2/ROBUSTNESS_PROTOCOL_DRAFT.md` (pre-run)

Reviewer role: an independent statistics and ML-evaluation methodologist. I did not run the experiment. No test-split quantity was computed. The only data touched were the 256 **train** rows of `raw_logits.npy` (rows 0–255, which match `targets.npz['train_indices']` through `image_indices.npy`), used for the feasibility counts in Section 7. I also used the archived 281/207 held-out interval that is already public in `head_transfer_20261007/README.md` to get an order of magnitude for variance.

## Summary verdict: **run with changes.** Two of the changes come close to a redesign.

The firewall is procedurally sound, and computing risk in exact Gaussian expectation is a good choice. As written, though, the protocol has four problems.

- **(i) The prediction is too noisy.** Its precision is limited by about 128–256 evaluation images, against 4096 test images. The predicted σ\* interval will usually be so wide that S2 is close to vacuous.
- **(ii) Selection bias.** Pair selection and prediction use the same calibration data, which produces a winner's-curse bias toward an overestimated clean gain and an overestimated σ\*.
- **(iii) Ill-defined uncertainty targets.** The bootstrap refits the encoder, but the deployed encoder is fixed. Root intervals with "no-root" mass are undefined. Cross-fitting inside bootstrap resamples leaks duplicates between folds.
- **(iv) Criteria ignore test uncertainty.** S1–S3 compare against test *point* estimates and have no precision gate or "inconclusive" outcome.

The most important framing point: Δ_pred is an empirical risk of the same fixed models on images drawn i.i.d. from the same pool as the test images. Agreement with the test is therefore expected under sampling alone. The primary test checks **held-out reproducibility of the empirical boundary**, not the theory. Only the secondary √(G/B) carries theory content, and its B is mis-specified (Issue 9). Say this explicitly.

---

## Issues

### 1. [Important: framing] The primary "prediction" is a held-out replication, not a theory test
Δ_pred(σ) is the cross-fitted empirical risk difference of the same encoder on calibration images. The test images are i.i.d. draws from the same CIFAR-10 training pool. Under correct code, E[Δ_pred] ≈ E[Δ_test] up to bias-fit sample size. Passing S1–S3 therefore shows that the empirical comparison generalises and is not an n = 256 artefact. That question is legitimate and worth asking, given that the hidden-channel pilot flipped sign on held-out data. It does not show that "theory predicts real behaviour."

The project's own reviewers also noted (manuscript §6, applicability diagnosis) two further points:
- A calibrated crossing at large enough σ is generically implied by the support bound, because mono's omitted constant bypasses code noise.
- These continuous pairs have no Bernoulli-type retention onset.

Selecting pairs with crossings in [0.1, 0.8] thus tests the location of a generic crossing, not the critical law.

**Fix.** Rename the primary claim to "held-out reproducibility of the train/dev-estimated sharing–mono boundary." State in §8 that this does not test the Bernoulli critical exponent or the critical mechanism. Keep σ\*_th as the only theory-content prediction, and fix its definition (Issue 9).

### 2. [Blocking] Prediction precision is far worse than test precision; S2 becomes vacuous
Order of magnitude from the archived 281/207 interval (η = 2/3, so only indicative): the per-image SD of the share−mono loss difference is about **0.60**. The resulting standard error of Δ at fixed σ is:

| n images | SE(Δ) |
|---:|---:|
| 128 (one cross-fit half) | ≈ 0.053 |
| 256 (all of calibration) | ≈ 0.038 |
| 4096 (test) | ≈ 0.009 |

Typical clean gains are of the same order. The 281/207 gain was 0.071, and it was the "large-gain" pair.

With Δ ≈ −G + Bσ², the delta method gives SE(σ\*)/σ\* ≈ SE(Δ)/(2G). For G = 0.07 and n = 256 this is about 27%, so the 95% interval spans roughly ×0.5 to ×1.5 of σ\*. Encoder-refit variability (Issue 4) adds to this. S2 ("σ\*_test inside the 95% pred interval") will then pass for almost any outcome, while S1/S3 rarely apply because the predicted intervals do not exclude 0.

The split itself is badly unbalanced for a prediction-versus-test design: the prediction is the bottleneck and the test is over-powered.

**Fix (recommended).** Before anything else, reallocate part of the test split with a seeded, label-blind rule into a development ("dev") split.
- Suggested sizes: dev = 1792 of the 4096 test images, leaving test = 2304.
- This is legitimate because no test number has been computed for any candidate pair. Only 281/207 has been looked at, and it is excluded and in any case ineligible (see Issue 12).
- Resulting SEs: about 0.0127 for prediction (dev 1792 + cal 256 = 2048) and about 0.0126 for test, so the design becomes balanced.

**Fallback (if the splits must stay fixed).** Keep the splits but add a pre-test precision gate (Issue 6). Accept up front that few or no pairs may pass it, and report that outcome rather than relaxing the gate.

### 3. [Blocking] Selection and prediction use the same data, causing winner's curse
The pre-screen ranks 300 pairs by the *calibration-based* Δ_pred(0) and keeps the 10 largest gains. It truncates to σ\*_pred ∈ [0.1, 0.8], then picks the 2 narrowest bootstrap intervals. Each step conditions on noise in the very quantity later compared with the test:
- Top-10-of-300 selection on −Δ_pred(0) inflates G, which inflates σ\*_pred (σ\* rises with G). The test will then tend to show an *earlier* crossing.
- "Narrowest interval" favours pairs whose resample happened to understate variance.
- For controls, choosing the largest margin overstates the margin. This is harmless for "no crossing" but makes the controls nearly uninformative.

**Fix.** Sample-split selection from prediction.
- Use **train only** for screening: the encoder fit, in-sample clean gain, and a crude train-fitted noisy-bias crossing.
- Alternatively, use a seeded half of the dev split for screening, as "dev-S".
- Compute the prediction and its uncertainty only on data not used for selection: calibration plus the remaining dev ("dev-P").
- Because the images are i.i.d., a prediction conditional on selection by independent data is unbiased for the selected pairs.
- State that selection-time numbers are never reported as predictions.

### 4. [Important] The bootstrap targets the wrong uncertainty, leaks between folds, and is undefined for roots
- **Wrong target.** The test evaluates one *fixed* deployed encoder: the one fit on the actual training images. Refitting the encoder in every bootstrap resample adds encoder-sampling variability that the deployed system does not have. Near-degenerate angles make this worse: same-sign versus opposite-sign branches with almost equal training loss (60% of the pairs sampled in Section 7 have negative correlation) can flip between resamples and make σ\*_pred bimodal. The prediction should be **conditional on the deployed encoder**: resample only the prediction-evaluation images and refit the biases inside each resample. Report encoder instability as a separate pre-test diagnostic, moving diagnostic (c) from post-failure to pre-test, and use it as an eligibility gate.
- **Duplicate leakage.** Two-fold cross-fitting inside a with-replacement resample puts copies of the same image in both the fit half and the evaluation half, so it is no longer out of sample. Split the folds by unique original image ID (grouped folds), or use the out-of-bag image set for evaluation.
- **Root intervals are undefined with no-root mass.** A "95% interval for σ\*" is meaningless when, say, 20% of resamples have no root. Define σ\* on an extended range with "no root in [0, 1]" coded as > 1, and use percentile limits on that extended range. Or, preferably, use a **test-inversion confidence set**: CS = {σ ∈ [0, 1] : the simultaneous band for Δ_pred(σ) contains 0}, computed with a sup-t bootstrap band over a fine σ grid.
- **Two-fold is a high-variance, single arbitrary split** with bias fits on 128 images, while the deployed biases are fit on 256. Use repeated K-fold (K = 10, 20 repetitions) cross-fitting of the biases, so that bias-fit sample sizes are close to deployment. Average across repetitions; do not pick one.

### 5. [Important] S1–S3 compare with test point estimates and lack an "inconclusive" category
- **S1** compares the sign of the Δ_test(0) point estimate. If the true Δ is near 0 this is a coin flip, and the criterion is undefined when the predicted interval contains 0.
- **S2** checks interval containment of the σ\*_test point estimate. It ignores test uncertainty and rewards imprecise predictions. The control criterion "no test root on [0, 1]" can fail from noise alone where Δ_test is near zero at large σ. It is also range-limited by construction, since a calibrated crossing is eventually expected (Issue 1).
- **S3** makes up to 40 pointwise sign checks with no simultaneity or multiplicity treatment.
- **Overall**, the "all 4 pass" rule has an unknown error rate, because the criteria are not calibrated tests. Even with nominal 95% coverage, a 4-way conjunction passes with probability ≤ 0.81 when everything is correct.

**Fix.** Use a three-way outcome per pair (PASS / FAIL / INCONCLUSIVE) built on intervals from *both* sides, an equivalence margin for σ\*, and a pre-test precision gate (Issue 6). See the revised protocol text below.

### 6. [Important] No minimum precision requirement
**Fix.** Before the test, project the 95% interval half-width of D = log σ\*_test − log σ\*_pred:
- Use the prediction bootstrap SE.
- Use a projected test SE, computed from the per-image variance on the prediction images scaled by √(n_pred/n_test).
- Add the two variances; the prediction and test images are disjoint.

A crossing pair is eligible only if all three hold:
1. ≥ 95% of resamples have a root in [0.05, 1].
2. The projected half-width is ≤ ½·log 1.5 ≈ 0.20.
3. The clean-gain interval excludes 0.

Under (2), a true ratio of 1 passes the equivalence criterion (margin log 1.5) with probability > 0.97.

- If fewer than 2 pairs pass, run the test on the pairs that pass. If 0 pass, the result is "prediction not precise enough; test not run". Gates are not relaxed.
- In the fallback design (n_pred = 256), expect a half-width near 0.35–0.5. Few pairs will pass, and that should be disclosed rather than adjusted away.

### 7. [Important] Multiplicity and dependence across σ and pairs
- **Across σ:** the 10 grid points are strongly positively dependent. Use one sup-t simultaneous band per pair, from a joint bootstrap over σ, rather than 10 pointwise intervals. Report pointwise intervals only descriptively.
- **Across pairs:** all pairs share the same test images, so their statistics are dependent. Use one joint image bootstrap (resample images once and compute every pair and every σ) whenever statements span pairs.
- The overall "all crossing pairs PASS" claim is an intersection–union test: no Bonferroni correction is needed for the conjunction, but power falls (Issue 5). Claims of the form "at least one pair FAILS, so the prediction is wrong for this network" should use Holm across pairs.
- Do not pool p-values across pairs. Report counts descriptively.

### 8. [Important] Encoder search instability and multiple near-degenerate minima
The dense-grid search is numerical, not certified (CORRECTIONS_v2 §3). For each pair, before the test, record:
- all local minima within Δloss ≤ 1e-3 (relative) of the best;
- the bootstrap branch frequency, with the encoder refit on train resamples, for diagnosis only.

**Exclude** pairs where a second branch lies within that tolerance, or where the best branch's bootstrap frequency is < 0.8. Otherwise "sharing" names an unstable object, and S1–S3 become uninterpretable even though prediction conditional on the encoder is well defined.

Calibrated bias refits can also jump discontinuously between bias basins as σ changes (for example, an output switching "off"). A "root" of Δ may then be a jump. Pre-specify that the crossing is a sign-change *bracket*, reported with any discontinuity flag. Use the same bias-search settings (gap 1e-7, multistart) for prediction and test.

### 9. [Important] The secondary σ\*_th = √(G/B) is not well defined as specified
- The finite difference (Δ(0.02) − Δ(0))/0.02² multiplies estimation and optimiser error by 2500.
- It also depends on step size. These are zero-inflated features: the median both-zero fraction is 0.26 on train. Many pre-activations lie within 0.02 of a ReLU kink, so non-quadratic σ³ and boundary terms contaminate the value at σ = 0.02.
- In the empirical (finite-n) problem the σ → 0 limit is in fact simple. If no image sits exactly at a kink with a nonzero target, both risks are smooth in σ². By the envelope theorem, the calibrated and frozen B coincide at leading order when both start from the same σ = 0 biases: B = Σ_i η_i [w_i² · (fraction of images with output gate i open + ½ · fraction exactly at the gate)], share minus mono.
- That limit is computable in closed form from gate fractions, with no finite difference. It does not equal the Bernoulli-theory B_cal, which arises in the ε^{3/2} scaling at a critical onset these pairs do not have.
- σ\* ∈ [0.1, 0.8] is far from "small σ", so the quadratic extrapolation is uncontrolled.

**Fix.** Define B_gate analytically as above, and B_fit as the least-squares quadratic coefficient on the grid σ ≤ 0.15, using the paired curve. Report σ\*_th for both, labelled as a "quadratic heuristic, not the Bernoulli critical law". Assess it with the same log-ratio statistic D, as a descriptive measure only.

### 10. [Minor → Important for retrodiction] The 281/207 retrodiction is not like-for-like
The archived run used importance η = 2/3, an absolute noise SD of 0.7309 × {0, 0.05, 0.1, 0.2, 0.4}, and biases calibrated on cal. The draft uses η = 0.5 and a different σ grid. Logit 281 also has a train zero-fraction of 0.176, so the pair would be *ineligible* under the draft's own rule.

**Fix.** Run the retrodiction with the archived η and noise levels. Label it a pipeline check with a known answer, not evidence.

### 11. [Minor] Leakage and firewall details
No direct path by which test information enters selection, normalisation, calibration or prediction was found. Normalisation uses train RMS, and splits are fixed by seed. The remaining risks are procedural or indirect:
- **281/207 test values have been inspected.** Other cat/dog logits correlate with them. Disclose this. Optionally exclude pairs containing a logit with train |r| > 0.8 with 281 or 207.
- **Freeze code, not only predictions.** Hash the selection script, the prediction script, *the test-evaluation script*, the seeds, and the selected-pair list. Send these hashes to the external reviewer, timestamped, before the test. The test script should refuse to run unless the hashes match, and should load test rows only after that check.
- **Move post-failure diagnostic (d)** (Monte Carlo versus exact risk) to *pre-test*, run on calibration images. It needs no test data, and running it after a failure invites post hoc rescue.
- **Diagnostic (a)** (test moments) after failure is fine, but label it descriptive.
- The "first root" definition must be fixed for prediction and test alike, including the cases Δ(0) ≥ 0, multiple roots, and discontinuities.

### 12. [Minor] Feasibility and eligibility (train-only numbers below)
Eligibility is easy to meet: 505 logits and 127,260 pairs qualify. The zero-fraction window has binomial SE ≈ 0.031 at n = 256, so the boundary is soft. That does not matter much, but fix it by train-only computation, as the draft does.

Correlations are mostly moderate and **negative**. Because of the covariance mechanism, nearly every pair will show an in-sample clean sharing gain, so "Δ_pred(0) < 0" filters little; most gains will be small. Pairs with large |corr| (≥ 0.4) make up only about 5–10% of the pool.

### 13. [Minor] Test-uncertainty method and wording
A paired bootstrap over test images, conditional on the fitted encoder and biases, is appropriate. Each image contributes an exact-expectation loss for fixed models, so Δ_test is a sample mean of i.i.d. terms.

The losses are heavy-tailed (max/RMS of features up to about 7 on train, and squared in the loss). Use BCa or studentised intervals with B ≥ 5000, pre-specified. Do not switch methods afterwards.

Required wording:
- "intervals reflect finite test-image sampling only, conditional on one network, the fitted models, and the selected pairs";
- "no population inference over pairs, layers, or networks";
- "pairs were selected by a train-only rule and are not a random sample of features";
- avoid "significant"; prefer intervals. Any p-value is conditional and exploratory.

### 14. [Answer to reviewer question 3] Calibrated versus frozen
**Keep calibrated as primary.** It removes a trivial bias-mismatch disadvantage, matches the theory's fair-comparison convention, and was pre-declared in both pilots.

Define the frozen biases precisely: clean biases refit on calibration, so that both policies coincide at σ = 0, as in the hidden pilot. The hidden pilot showed that the choice of clean-bias source can flip the clean sign. Report frozen as secondary, with the same intervals and no criteria.

### 15. [Answer to reviewer question 2] Four pairs
Four pairs is fine as a bounded first test, *provided* the precision gate holds. Better: take **all** gate-passing crossing pairs up to a cap of 6, in a pre-specified train-only rank order, plus 2 controls. This raises the information yield without opening a search: the cap and order are fixed in advance and there is no substitution afterwards. Control pairs carry little evidential weight because they are selected far from zero. Describe them as negative controls.

---

## 7. Feasibility on TRAIN data only (n = 256 images, 1000 logits, rectified at 0)

| Quantity | Value |
|---|---|
| Overall fraction of zeros after rectification | **0.535** (raw logits > 0: 46.5%) |
| Per-logit zero-fraction quantiles (0/5/10/25/50/75/90/95/100%) | 0 / .023 / .062 / .254 / .605 / .82 / .911 / .945 / .996 |
| Logits by zero fraction: [0, .2) / [.2, .5) / [.5, .8) / [.8, .95) / ≥ .95 | 217 / 210 / 295 / 235 / 43 |
| **Eligible logits** (zero fraction in [0.2, 0.8]) | **505** |
| Eligible pairs | **127,260**, so a pool of 300 is trivially available |
| 281 / 207 zero fractions | 0.176 / 0.223 (281 is ineligible) |
| 300 random eligible pairs (illustrative seed 12345, not the protocol's 20261008): corr quantiles (0/5/25/50/75/95/100%) | −.54 / −.30 / −.17 / −.04 / .10 / .43 / .76 |
| Share with corr < 0; corr < −0.05; \|corr\| < 0.05; corr > 0.15 | 60%; 48%; 21%; 22% |
| Both-zero fraction per pair (median, IQR) | .26 (.16–.38) |
| Distinct logits in the 300 pairs; max reuse | 342; 6 |
| Max/RMS of eligible logits (5/50/95%) | 3.1 / 4.6 / 7.0 |

**Conclusion.** Rectified logits are about half zeros overall. They are not "mostly zero", but they are strongly zero-inflated with substantial (0, 0) atoms. Eligible pairs are plentiful. The binding constraint is precision of the prediction (Issue 2), not availability of pairs.

---

## Proposed revised protocol text (paste over draft §§2, 4–7)

> **§2 (addition) Splits.** Train (256) and calibration (256) are unchanged. Before any pair-specific computation, a seeded (seed 20261009), label-blind rule moves 1792 of the 4096 test images into a development split, leaving **test = 2304**. Dev is divided once, by the same seed, into dev-S (896, used for selection) and dev-P (896, used for prediction). The prediction-evaluation set is P = calibration ∪ dev-P (1152 images). Logits 281/207 were inspected on the former test split; this is disclosed, and they are excluded. *(Fallback if splits stay fixed: selection uses train only, and P = calibration only. The precision gate below applies unchanged and is expected to exclude most pairs.)*
>
> **§4 Prediction (conditional on the deployed encoder).**
> 1. Encoder w_tr: best minimum found on train (repaired dense grid with refinement of all local minima). Record every local minimum within 1e-3 relative loss of the best.
> 2. Δ_pred(σ): 20× repeated 10-fold cross-fitting of the calibrated biases (for both models, at every σ) within P. Fit on 9/10, evaluate the exact-expectation loss on 1/10, then average over all evaluations. Clean (σ = 0) biases are refit the same way.
> 3. Uncertainty: 2000 bootstrap resamples of P images, with fold assignment by unique image ID and the encoder held fixed at w_tr. Produce a sup-t simultaneous 95% band for Δ_pred over a fine grid of σ (0 to 1, step 0.01). σ\*_pred is the first sign change from negative to positive, with "no root in [0, 1]" coded as > 1. The 95% interval is the percentile interval on this extended range, and the confidence set is CS = {σ : the band contains 0}. Record the no-root fraction.
> 4. Projected test SE at each σ: per-image SD on P × (1/√2304). Projected half-width h of the 95% interval for D = log σ\*_test − log σ\*_pred.
> 5. Secondary: σ\*_th,gate = √(G/B_gate), with B_gate the closed-form gate-fraction coefficient. σ\*_th,fit uses the least-squares quadratic on σ ≤ 0.15. Both are labelled quadratic heuristics, not the Bernoulli law.
> 6. Pre-test checks on calibration images: Monte Carlo versus exact risk (3 images, 10^6 draws). Bootstrap branch frequency of the train encoder (500 train resamples), diagnostic only.
>
> All outputs, selected pairs, seeds and the SHA-256 hashes of the selection, prediction and test scripts are written to a frozen file. That file is sent to the external reviewer before the test. The test script verifies the hashes before it loads test rows.
>
> **§5 Selection (train and dev-S only).** Pool: 300 eligible pairs (seed 20261008; train zero fraction in [0.2, 0.8]; excluding 281 and 207).
> - Screening statistics are computed with the encoder from train and biases fit on train, evaluated on dev-S.
> - Crossing candidates: dev-S Δ(0) < 0 and a dev-S crossing in [0.1, 0.8], ranked by dev-S clean gain.
> - Controls: dev-S Δ < 0 on the whole grid, ranked by margin.
> - Walk down each ranking and apply the eligibility gates, computed on P after the ranking is frozen:
>   - (a) no second encoder minimum within tolerance, and bootstrap branch frequency ≥ 0.8;
>   - (b) the band for Δ_pred(0) excludes 0;
>   - (c) for crossing pairs, ≥ 95% of resamples have a root in [0.05, 1] and h ≤ 0.20;
>   - (d) for controls, the band for Δ_pred lies below 0 on [0, 1].
> - Take up to 6 crossing pairs and 2 controls. No substitution after the test. If no crossing pair passes, report this and stop.
>
> **§6 Test and criteria.** Δ_test(σ) is computed on the 2304 test images with w_tr and the calibrated biases refit on all of P. A joint paired bootstrap over test images (B = 5000, BCa) gives per-pair simultaneous bands over σ and the interval for σ\*_test (same root definition). D's 95% interval combines the prediction and test variances, which are independent. Per pair:
> - **S1 (clean ordering).** PASS if the test 95% interval for Δ_test(0) excludes 0 on the predicted side. FAIL if it excludes 0 on the opposite side. Otherwise INCONCLUSIVE.
> - **S2 (crossing, primary; crossing pairs).** PASS if the 95% interval of D ⊂ (−log 1.5, log 1.5). FAIL if it lies entirely outside that range, or if the test band is below 0 over the entire predicted σ\* interval (no crossing where one was predicted). Otherwise INCONCLUSIVE. The point ratio σ\*_test/σ\*_pred is always reported. Factor 2 is a secondary margin.
> - **S2 (controls).** PASS if the test band lies below 0 on [0, 1]. FAIL if the band lies above 0 at some σ ≤ 1. Otherwise INCONCLUSIVE. This is a range-limited statement; a crossing above σ = 1 is expected under calibration.
> - **S3 (descriptive).** Agreement of the simultaneous-band signs over σ, reported without a criterion.
> - **Overall.** The confirmation statement holds if every crossing pair is PASS on S1 and S2, and no control FAILs. A refutation statement requires at least one FAIL that survives Holm across pairs. Results are reported per pair, with counts of PASS/FAIL/INCONCLUSIVE.
> - **Secondary.** D for σ\*_th,gate and σ\*_th,fit, and the frozen policy, are descriptive only.
>
> **§7 Stopping.** Run once. After any FAIL or INCONCLUSIVE, the only additions allowed are the pre-listed descriptive diagnostics: (a) train/P versus test moment shifts; (b) cross-fit versus full-P biases; (c) the encoder-branch diagnostics already computed pre-test. No new pairs, σ values, policies, margins, interval methods or networks. Wording: intervals are conditional on one network, the fitted models and train-rule-selected pairs. There is no population inference over features or networks. Any p-value is exploratory.
