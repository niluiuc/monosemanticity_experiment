# Review of repair_v2 and the draft robustness protocol

Decision: accept the editorial corrections for their intended purpose. Do not execute the draft unchanged. The fixes below require no new network extraction and preserve Project 1's mathematics -> controlled toy validation -> real-feature transfer structure.

Claude files were read only. This review did not compute risk curves, select candidate pairs, fit models or inspect new test outcomes. A metadata/split check confirmed raw_logits has 4608 rows and the split is 256 training, 256 calibration and 4096 test images. The previous first-1024-row pooled-logit experiments include 512 of those test images.

## Required protocol changes

1. **Honest holdout firewall.** Do not call all 4096 test rows untouched. Exclude raw-logit rows 512:1024 from the new evaluation, because they were included in the earlier pooled pair/triple analyses. Use rows 1024:4608, the remaining 3584 images, and explicitly disclose the prior use of this cached dataset and the archived 281/207 evaluation. Verify provenance and the row-to-image-index mapping before fitting; if any further rows were used to develop the new selected-pair claims, exclude those too. This is a prospective follow-up on previously cached data, not an entirely fresh dataset.

2. **Bound candidate screening and remove interval-based selection.** Replace 300 fitted pairs plus top-ten encoder-refitting bootstraps with a fixed small cap, e.g. at most 12 distinct eligible candidates in seed order. Select up to two crossing and two non-crossing candidates from TRAINING predictions only, using the first qualifying candidates, not the narrowest confidence intervals. Freeze identities before calibration prediction. If a category is unavailable, record it and stop selection; do not extend the pool to manufacture a crossing. Two pairs per category are a pilot, not representative evidence over all features. This is a substantive scope correction, not a statistical objection to all training-only screening.

3. **Use the strongest mono comparator.** Compare sharing against BOTH coordinate-retaining encoders, (1,0) and (0,1), with their correct importance-weighted losses and biases. Choose the primary mono orientation using training data only, keep it fixed, and report both orientations secondarily. This prevents a crossing that simply reflects an unnecessarily weak baseline.

4. **Separate empirical forecast from mathematical prediction.** The calibration cross-fit curve is an empirical forecast using the same exact Gaussian-loss functional later evaluated on test data. Its successful transfer establishes held-out compressor risk prediction, not validation of the Bernoulli critical exponent or the representation-geometry mechanism. The proposed B from a single sigma=.02 secant is a finite-noise estimate, not an analytically derived quadratic coefficient. Label sqrt(G/B) a secondary heuristic unless its coefficient and remainder are derived for the actual selected distribution. If B<=0, G<=0, multiple roots or unresolved near-zero losses occur, report the prediction as unavailable; do not force a root. A reversal alone, especially at high code noise, does not establish the training-linked critical law: the existing calibrated high-noise bound already predicts eventual loss of full-support sharing advantage in this model class.

5. **Use an uncertainty design for the intended estimand.** Four identities/encoders frozen before calibration permit a small conditional pilot. Image-level paired bootstrap is appropriate as a conditional uncertainty calculation if image sampling assumptions are stated. Do not select pairs by the narrowest bootstrap interval and then advertise nominal 95% predictive coverage. Root intervals must retain the bootstrap probability of no root rather than dropping those draws. A percentile confidence interval for an estimated calibration crossing is not automatically a prediction interval for a finite test crossing. The half-calibration bias forecast and full-calibration deployed bias curve also differ; account for that distinction. Report predicted-versus-test root differences, clean/noisy signs and their uncertainties; do not make 'every root inside CI95' the sole scientific success criterion. No expensive encoder-refit bootstrap is needed for this first conditional test.

6. **Root-finding and retrospective pipeline check.** Specify whether the result is the first *resolved* sign-changing root. A fixed sparse grid cannot guarantee no intervening roots; use declared numerical scanning/refinement tolerances and label no-root as no detected root in the prescribed range. Reproduce the archived 281/207 outcome ONLY with its original eta=2/3, training normalization, mono selection and sigma=multiplier*training-reference convention. The new draft changes eta to .5 and uses absolute sigma, so its proposed comparison cannot be called reproduction of the archived experiment as written. Keep the archived comparison retrospective, not success evidence.

## Answers to the three reviewer questions

- Two-fold calibration cross-fitting is reasonable for an out-of-bias-sample preview. Freeze pair identities first and acknowledge that its half-sample fits differ from the full-calibration biases deployed on test. It does not replace an independent test split.
- Four pairs are enough for this bounded mechanism-transfer pilot, if it is labelled a selected-pair study and unavailable categories are reported without substitution. They are not enough for universal/native-network conclusions.
- Keep calibrated as primary, since that is the intended policy. Both mono and sharing receive the same calibration opportunity; report frozen as secondary without choosing the favourable policy after testing.

## Editorial status

The repair now appropriately narrows acceptance to checked local mathematics and the identified numerical repairs, withdraws the inferential claims, and replaces inappropriate global/gradient-flow wording. Status labels organize evidence; they do not independently complete an unreviewed proof. No new theorem was certified by this document read.

## Go/no-go

GO for the above bounded protocol after the explicit corrections are frozen in the protocol and implementation. NO-GO for the original 300-pair/500-refit/narrowest-CI version. No broad new exploration or another model is required now. Do not call this pilot a finished theoretical or native robustness transfer even if all its selected pairs reverse as predicted.
