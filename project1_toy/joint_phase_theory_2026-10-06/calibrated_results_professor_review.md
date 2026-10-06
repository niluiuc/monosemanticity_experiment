# Independent professor review of the twelve critical calibration results

6 October 2026. Scope: the saved `calibrated_run_v1` results only. No additional frequencies, noise values, optimizer run, or representation search was performed. The independent audit is reproducible with `calibrated_professor_checks.py`; its fresh output is `calibrated_professor_check_results.json`.

## Verdict

**Passed.** All twelve saved differences have the reported signs, using the importance-weighted global numerical bias-loss bounds. At the prescribed lower noise multiplier, sharing has lower calibrated MSE for every one of the six frequencies. At the prescribed upper multiplier, mono has lower calibrated MSE for every frequency. Each individual model's numerical loss gap meets its declared target. No failed or ambiguous sign was relabeled.

This provides six finite calibrated sign brackets consistent with the derived critical scaling. It does not by itself prove a unique crossing, locate all crossings, or establish the asymptotic exponent from data. The exponent and leading coefficient come from the preceding derivation. Bisection inside these existing sign brackets is a bounded localization step; an ambiguous midpoint should retain the previous bracket and stop rather than imply a sign.

## Evidence checked

The independent checker used 90-digit arithmetic and fresh Gaussian moment, derivative, and local-curvature functions rather than calling the experiment's calibration routines. It checked:

- All **56** hashes in the frozen run manifest, including the immutable geometry input and code/protocol/review snapshots.
- All **48** feature ledgers: **36** nonzero-column noisy objectives and **12** exact mono zero-column constant-prediction objectives.
- All **3,944** saved interval nodes: objective, gradient, interval-specific curvature, midpoint Taylor lower bound, and midpoint/domain coordinates.
- The full binary interval partition, including matching children and every terminal leaf. Each terminal leaf is either retained in the active heap or has a lower bound at least the final feasible upper bound. Thus no unsearched low-bound leaf is silently omitted from the recorded gap.
- Both excluded half-line bounds and the final active-heap minimum used to form the global numerical lower bound.
- The feasible risk at the retained incumbent bias, the per-feature gap, and the importance-weighted reconstruction of the model bounds.
- Every difference interval, computed as `[sharing_lower-mono_upper, sharing_upper-mono_lower]`, and its associated sign.

Maximum absolute discrepancy in these independent recomputations was **3.7496e-63**, below the check tolerance `1e-52`. This includes saved node quantities of substantially different magnitudes; the discrepancy is far below the run's numerical slack `1e-40` and its smallest scientific loss-gap target.

## Gap and sign interpretation

The per-feature tolerance is the model target divided by `1.5`. With importances `(1,0.5)`, the total model gap is therefore at most the declared model target. Each model meets that target; the difference interval width is the sum of the two model gaps, and need not itself be smaller than one model target. The interval arithmetic and reported signs use the correct two-model construction.

All six lower-noise intervals are wholly negative and all six upper-noise intervals wholly positive. This remains true at the smallest epsilon, where the differences are much smaller than those in the dense example. Both comparators receive free population bias calibration at identical noise, using the same outcome and encoder energy. The reversal is therefore not explained by leaving one decoder bias uncalibrated.

## Boundary and calculus assumptions

The methods reviewed before execution remain applicable: Bernoulli targets are in `[0,1]`, probabilities sum to one, Gaussian code noise is independent, and each nonzero feature has positive scalar decoder noise scale. The upper bias boundary puts every conditional mean at least one, making the derivative positive beyond it. The lower half-line bound uses monotonicity of the first ReLU moment and discards a nonnegative squared-output term. The local curvature bound uses the maximum Gaussian density on each conditional-mean interval. None of these arguments requires convexity of the bias objective.

Local stationary root finding supplies feasible upper bounds only. The saved intervals and their exterior bounds supply the numerical global-gap evidence. The dropped mono feature is a genuine zero column, hence its exact prior-mean prediction and variance loss are appropriate; this is not a generic zero-noise bias solution for a nonzero column.

## Limits and research relevance

Give credit for a disciplined implementation: the specified cases were retained, inputs archived, the symmetry of calibration respected, and the finite effects checked against a noise-aware optimum rather than a fixed threshold. The additional interval-specific curvature improves efficiency without changing the objective or comparator.

The calculation uses high-precision floating arithmetic with declared slack, **not rigorous directed-rounding intervals**. The mathematics of the analytical lower bounds is valid, and their saved numerical evaluation is independently verified; the precision limitation must remain explicit. Root's separate quadrature checks can provide another independent numerical route, but do not convert the entire branch-and-bound ledger into an exact arithmetic proof.

For manuscript purposes, these results support a **calibration-resistant local reconstruction-robustness boundary at clean-selected geometry**, within the stated two-feature tied-ReLU model. They strengthen the proposed mechanism and predicted scaling; they do not establish arbitrary-load clean training, modality transfer, or novelty relative to the complete literature. No additional scientific case is required to approve these twelve recorded comparisons.
