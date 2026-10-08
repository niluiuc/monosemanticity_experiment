# repair_v3: stop decision and next step

Review of supplied narrative, README, RESULTS, PREDICTION_STATEMENT, PROTOCOL_FROZEN, rt_core.py, rt_predict.py and the saved independent stop report. No experiments rerun; no final-evaluation data loaded by this review; Claude source files unchanged. Saved numerical statements below are inspected records, not a new independent reproduction.

## Decision

Stopping before final evaluation is justified. The reported clean-risk interval includes zero and only 44--48% of resamples resolve a crossing, far below the declared 95% gate. The precise projected half-width is not needed to justify this stop. The independent report does not fully reproduce the root fraction; disclose its discrepancy rather than attributing it conclusively to the coarser grid.

The finding is: this bounded selection procedure produced no informative crossing forecast. It does not establish that real-feature sharing advantages are generally too small, that reversals are absent, or that the theory has passed. Four training-to-selection sign reversals among twelve candidates are descriptive results for these candidates.

## Two interpretation/code issues

1. rt_predict.py takes bootstrap percentiles independently at each sigma. Bonferroni adjustment over pairs does not make these simultaneous confidence bands over the noise grid. Claims that controls are below zero over the entire range require a simultaneous construction, or must be labelled descriptive pointwise interval observations. The clean-sign stop uses a single sigma and remains justified.

2. The leading-order coefficient is not yet justified for the deployed estimand. The statement uses an envelope theorem for biases optimised for a distribution. The implementation fits biases on CAL and evaluates risk on P. Stationarity on CAL does not imply stationarity on P. Changes in sharing biases with sigma can therefore contribute to the held-out coefficient. The general frozen-bias and calibrated-bias coefficients are also different at mono's zero-valued kink. The proposed formula uses the calibrated mono coefficient v(p_P), although the actual calibration policy is determined by CAL. Reduction to a Bernoulli population calculation does not settle these out-of-sample issues.

Additional care: exact sharing kinks and nonzero targets at kinks need their own assumptions; a fraction-near-gates cutoff is a diagnostic, not a certified asymptotic validity domain. Compare gate distance to the actual output noise scale |w_i| sigma. B<0 means an initially improving advantage only when the coefficient applies; it does not predict the full finite-noise curve. If B=0, the displayed leading term does not decide the sign.

## Bounded instruction to Claude

Do not start a many-pair sign-of-B survey or use E. First check, on paper, whether the proposed B describes the exact calibration/deployment policy. State the distinction between distribution-profiled risk, frozen-bias risk and CAL-fitted/P-evaluated risk. Correct or restrict the coefficient accordingly; do not claim a new general theorem from a numerical match.

If a valid coefficient can be obtained without a large extension, compare it with the small-noise risk increments for the existing three selected pairs on development data only, using a short declared decreasing-noise check. This is an applicability/numerical check, not new independent confirmation. No new pairs and no new network. If the coefficient cannot be justified promptly, record this bridge as unresolved and stop extending it.

Any genuinely new mathematics must be integrated with full assumptions and derivation into the existing editable derivation source and Superposition_Recursive_Training_Derivations.pdf, per the research workflow. A separate repair preview is not the final required integration.

After this bounded check, decide whether this bridge earns a place as a limited real-feature illustration of Project 1. The central phase-diagram question must remain intact; a many-pair initial-slope study must not silently replace it.
