# Specialist-review response and bounded protocol decision

Date: 2026-10-07. Review only: no model fitting, pair selection, risk evaluation or new experiment was run. Claude's folder was read only. This document supersedes conflicting recommendations in the earlier protocol review, but preserves its data-provenance and comparator requirements.

## Decision

Do not run the existing draft unchanged. Apply the finite corrections below, freeze the implementation and predictions, then run one bounded pilot. No additional literature search, model extraction or broad parameter exploration is required to prepare that pilot.

## 1. Editorial and mathematics status

The editorial corrections are useful, but the labels are not yet fully consistent or sufficient to establish proof completeness:

- STATUS T7 still has two labels; separate its leading-order argument from numerical crossings. Separate numerical toy triples from exploratory real-activation triples, and align the endpoint-law label between STATUS and LaTeX.
- The gate lemma's written competing-interior argument is partly grid-based. The specialist's convexity argument is a plausible way to close this local gap, but must be written into the derivation with fixed interior parameters, bounds excluding distant bias regions, and the pointwise small-angle domain. An audit asserting a proof is not a substitute for the proof in the manuscript.
- Correct the particular output-1 state expansion's remainder from O(theta^4) to O(theta^3). Do not replace unrelated fourth-order remainders indiscriminately.
- State the donor-loss one-sidedness. Retain the compression threshold as a result for the specified energy-transfer path unless the full perturbation-space minimum is proved. Finite multistart minimisation cannot promote it to a theorem about every direction.
- Separate the exact bicritical identity from a causal interpretation. Remove or qualify the underived barrier-order statement.
- Report compression-search brackets that exclude the analytic threshold as numerical discrepancies/detection limitations, not as brackets containing that threshold.

These are specific completion/correction tasks, not a request to rebuild the project. Integrate completed proof repairs in the existing derivation PDF and editable source. This review supplies no new independently established theorem.

## 2. Statistical critique: agreement and qualifications

Agree: selection on the prediction sample biases the forecast; selecting the narrowest intervals is inappropriate; test uncertainty matters; rootless bootstrap draws must be retained; and an empirical held-out risk forecast is different from a theory prediction.

The claimed roughly +/-50% crossing uncertainty is an illustrative calculation using a previously studied pair and a quadratic approximation. It is not a measured uncertainty for the new pairs. Sample count alone does not determine root precision: image-level variability and the slope near the crossing matter.

The proposed 20 repeated 10-fold fits inside 2000 bootstrap replicates at every noise value, plus encoder bootstraps, is unnecessary for this first conditional pilot. It also leaves a cross-fitted-bias versus full-sample-bias estimand mismatch. Use the same fixed deployed encoders and calibration-fitted biases for independent prediction and test evaluation instead.

A near-degenerate encoder need not be excluded to estimate the risk of a specified frozen encoder. Record competing minima and numerical tolerances, but do not turn encoder-instability exploration into a new blocking experiment. Population claims about the training algorithm would require a different uncertainty target.

The gate-fraction B formula requires its kink, target and bias-optimum assumptions to be checked and derived for the actual model. Do not treat it as already established by this review. A finite-noise quadratic extrapolation is a heuristic. Do not add a fitted quadratic as the project's theoretical contribution.

## 3. Data and model firewall

The earlier pooled experiments used raw-logit rows 0:1024: 256 train, 256 calibration, and 512 nominal test rows. Therefore the statistician's statement that only pair 281/207 was examined on test data is incomplete.

Keep the existing training and calibration sets. Exclude rows 512:1024 from new evaluation. Subject to verifying that no additional pooled analyses used later rows, use rows 1024:4608 (3584 images) for the new development/final-evaluation allocation:

- 896 development-selection images;
- 896 development-prediction images;
- 1792 final-evaluation images.

Partition once by seeded image-ID rule, before new pair-specific outcomes are computed. The archived 281/207 evaluation also used this cached pool: exclude those coordinates, disclose the historical use, and describe this as a prospective selected-pair follow-up on reused cached data, not a wholly untouched dataset. If later-row outcomes for the new candidates were already used in development, this allocation must be revised accordingly.

Normalisation and encoder fitting use training only. Evaluate both mono orientations, choose the better training comparator and freeze it. Use calibration to fit biases for each declared noise level equally for sharing and mono. Freeze those same biases for development-prediction and final evaluation. Calibration images must not also contribute prediction-evaluation losses.

## 4. Bounded selection and prediction

- Cap fitted candidates at 12 eligible pairs in a fixed seeded order, using the already available infrastructure. No top-ten-of-300 search and no narrowest-interval selection.
- Use training plus development-selection only to choose up to two crossing candidates and two range-limited non-crossing controls. Selection uses training-fitted biases; subsequent calibration may change the forecast. Freeze identities before examining development-prediction outcomes.
- Forecast the risk-difference curve on development-prediction using the fixed calibrated models. Preserve all selected pairs in the report if the forecast changes, is imprecise or has no root. Do not substitute new candidates.
- Use paired image resampling jointly across pairs and noise values. With fixed models, this resamples stored per-image losses and requires no repeated optimisation. Produce simultaneous curve bands and retain no-root outcomes explicitly.
- Freeze root definition, numerical scan/refinement tolerances, seeds, model parameters, selected identities, code hashes, predictions and success criteria before loading final-evaluation outcomes.

This design targets conditional risk reproducibility for the selected fitted compressors. It does not target variability over networks or encoder retraining.

## 5. Minimum precision and decision rule

A useful explicit pilot target is factor-1.5 agreement between predicted and final-evaluation crossing locations. This is an engineering tolerance, not a mathematical constant or an ICML criterion.

Before final evaluation, require for an informative crossing forecast:

- resolved clean sharing advantage;
- at least 95% of prediction resamples with a resolved crossing in the prespecified interior range;
- projected 95% half-width for the log crossing-ratio difference no greater than 0.20, approximately half the log(1.5) equivalence margin.

Estimate projected evaluation variability from prediction per-image losses and the planned evaluation size, stating the sampling assumptions. Use the log-ratio approximation only for a resolved, isolated crossing away from zero with locally regular behaviour. Otherwise classify root precision as unresolved; do not manufacture a log interval. The precision target may fail even with the proposed larger development sample.

Do not select replacement pairs to satisfy this gate. If no crossing forecast is informative, report that and stop before final evaluation. If some are informative, evaluate the frozen selected set once and label outcomes PASS, FAIL or INCONCLUSIVE. Assess crossing agreement using uncertainty from both independent evaluation sets, not containment of a test point estimate in the prediction interval. Predeclare a conservative joint bootstrap/band construction and any across-pair error control. Do not present an uncalibrated 'all four pass' rule as a formal confidence claim.

For controls, state 'no resolved crossing within the prescribed range'; a finite noise scan does not certify absence of every possible root.

## 6. Interpretation and stopping

The paper-critical question remains: when does sharing's clean advantage reverse under corruption, and can the derived tradeoff predict that reversal? This pilot addresses the real-activation, fitted-compressor part. Agreement of two empirical curves alone does not establish the Bernoulli critical law, native-network robustness, diffusion transfer or main-track readiness. Keep any analytic/heuristic prediction separate and report its error even if the empirical forecast succeeds.

Run the existing archived pair check with its original importance, normalisation and noise convention; treat it as a pipeline check. Resolve numerical expectation checks on development/calibration data before final evaluation. After evaluation, allow only the existing bounded diagnostics, with no replacement pairs or post-hoc policy/tolerance changes.

Saved numerical specialist results show very close solver agreement at the checked points (the saved summary reports a maximum v2-minus-independent loss difference of 6.939e-17 across 340 rows). This supports numerical reliability on that finite set; the measured well widths do not certify an exhaustive search over all parameters. The literature scout remains a targeted, incomplete novelty assessment, not proof that no existing paper addresses the question.
