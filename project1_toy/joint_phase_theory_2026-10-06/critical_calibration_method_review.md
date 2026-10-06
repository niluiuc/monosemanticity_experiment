# Independent method review: twelve prescribed critical calibration comparisons

6 October 2026. Reviewed `calibration_precision_protocol.md`, `run_critical_calibration.py`, the imported Gaussian moment routines in `run_frozen_map.py`, and the existing midpoint-Taylor global-gap method. No calibration comparison or new experimental case was run for this review.

## Verdict

**Mathematical method approved, with the input-archival repair below required before execution.** The interval-specific curvature bound is a valid specialization of the previously reviewed scalar objective. The twelve comparisons remain exactly the planned six geometries at two prescribed noise multipliers. No additional search over representations or frequencies is necessary.

## Calculus and bounds

For conditional score `mu = offset + beta`, Gaussian scale `s > 0`, and target `y` in `{0,1}`, the population objective and its derivative in the code agree with the Gaussian ReLU moment formulas. Its second derivative is

`f''(beta) = 2 sum P [Phi(mu/s) - y phi(mu/s)/s]`.

On the interval `[lo,hi]`, let `d_j` be the distance from zero to `[offset_j+lo, offset_j+hi]`. Since `0 <= Phi <= 1`, targets are nonnegative and `phi` decreases with absolute argument,

`abs(f'') <= 2 [1 + sum P y phi(d_j/s)/s] = H_interval`.

Thus the code's midpoint lower bound `f(mid)-abs(g(mid))*radius-H_interval*radius^2/2` is valid throughout that interval in exact arithmetic. This does not assume convexity. The density terms may vary between children; each child's own bound is computed for its full interval. Clipping the result at zero is valid because this is a squared-error objective.

The far-left lower bound is valid: dropping the nonnegative squared-output term gives `E y^2 - 2 E[y ReLU(score)]`, and the latter moment increases with beta, so evaluating it at the excluded half-line's right endpoint bounds all smaller biases. For the right endpoint `1-min(offsets)`, all conditional means are at least one, hence at least the target; the displayed derivative is positive beyond that point. Its endpoint risk bounds the excluded upper half-line from below.

Feasible stationary roots improve upper bounds only. The code correctly does not treat local root finding as global evidence. The active-heap lower bound, exterior lower bounds, and retained feasible upper bound give a global numerical gap; unresolved gaps remain unresolved at the declared expansion limit. The per-feature tolerance allocation `total_target/(1+1/2)` correctly bounds the importance-weighted total gap by `total_target`.

The zero-scale branch is used here only for the zero-column mono feature, whose tied decoder is a constant and whose optimum is the exact prior mean. It is not a generic clean nonzero-geometry bias optimizer. This use is correct for the twelve positive-noise comparisons.

## Arithmetic status

The entire objective, gradient, curvature, and heap calculation uses 70-digit `mpmath` arithmetic, with the declared `1e-40` numerical slack. Gaussian CDF uses `erfc`, avoiding the basic `1-erf` negative-tail cancellation. This is much stronger numerical checking than the previous float64 routine, but it is **not directed-rounding interval arithmetic**. The protocol accurately states that limitation. Preserve that wording in the results and manuscript. An independent moment/quadrature or precision check remains appropriate for the eventual signed differences; it should not be described as an exact arithmetic certificate.

## Required reproducibility repair before running

The script reads `frozen_run_v1/results.json` for p, weights and clean biases, but originally copied only program/protocol/review files to the source snapshot. Copy that exact frozen input JSON into the calibration snapshot and include its hash, or save an equivalent immutable input-settings record with those quantities. Otherwise per-feature node ledgers cannot be reproduced from the calibration archive alone. Preserve the original frozen result; do not rewrite its historical pending-global-certificate flags. Archive the exact root-bracket verification separately.

With that repair, the implementation is accepted for the prescribed twelve comparisons. No extra control or experiment is required before this bounded run. Certify a sign numerically only when the archived difference enclosure excludes zero, and keep unsuccessful gap or sign cases visible.

### Pre-execution repair verification

The reviewed script now copies the frozen input JSON to `source_snapshot/frozen_geometry_results.json`, and the end-of-run manifest covers that snapshot. The required archival repair is complete. **Approved to execute the twelve prescribed comparisons.**
