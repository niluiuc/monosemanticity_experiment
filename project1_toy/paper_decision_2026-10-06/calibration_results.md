# Same-outcome reversal after symmetric decoder calibration

6 October 2026. Student numerical report. Protocol and senior method approval
preceded execution. This report is separate from frozen raw archive `run_v1`.
The independent root teacher's integration/global-gap review is a separate step.

## Result

**The dense example's noisy reconstruction-MSE reversal survives symmetric
oracle population bias calibration at both prescribed corruption levels.**
Geometry is frozen, but EVERY shared/mono code may optimize its free decoder
biases for the same noisy population. Both globally clean-optimal relative-sign
sharing variants give equal MSE to floating precision. There is no detection
threshold in this comparison.

| Code/decoder policy | sigma=0 | sigma=.30 | sigma=.60 |
|---|---:|---:|---:|
| Sharing, frozen clean biases | .24642556509887897 | .31868281868245574 | .5129938089678424 |
| Mono, frozen clean biases | .25000000000000000 | .31746388060216080 | .5054497710894760 |
| Sharing, oracle calibrated biases | .24642556509887897 | .31793051367078850 | .49113473370400085 |
| Mono, oracle calibrated biases | .25000000000000000 | .31250541096332785 | .46709280699917590 |
| Calibrated sharing minus calibrated mono | -.00357443490112103 | +.00542510270746065 | +.02404192670482495 |

The noisy calibrated disadvantages are about 1.74% and 5.15% relative to the
calibrated mono MSE. They exceed all recorded numerical global gaps by large
margins, but independent integration verification must precede a final signed
research claim. No exact-arithmetic certificate of the noisy optimum is asserted.

## Global-gap and boundary diagnostics

All ten positive-noise/nonzero-column scalar problems reached the prescribed
per-feature numerical gap `<=1e-8`; both mono zero-column calibrations are exact.
Each used 47–58 interval expansions, far below the fixed 100,000 budget.
No failed tail exclusion, exhausted budget or derivative check occurred.

| Code | sigma | Sum upper-minus-lower gap |
|---|---:|---:|
| Same-sign sharing | .30 | 1.142385357e-8 |
| Opposite-sign sharing | .30 | 1.142385345e-8 |
| Mono | .30 | 6.987186149e-9 |
| Same-sign sharing | .60 | 1.354560977e-8 |
| Opposite-sign sharing | .60 | 1.354560977e-8 |
| Mono | .60 | 9.931263173e-9 |

Thus combined comparison uncertainties from these numerical gaps are at most
approximately `2.06e-8` and `2.35e-8`, versus positive differences `.00543`
and `.02404`. The declaration is `1e-8` per feature, not per summed code; a
two-feature sum gap slightly above `1e-8` does not violate that protocol.

Every lower excluded half-line bound is about `.5-1e-12`, above its feasible
upper value. Every upper-half-line bound also exceeds its feasible upper value.
All B/U values, incumbents, interval midpoints/gradients/lower bounds,
pruning/expansion actions and remaining intervals are retained for verification.
The local bounded optimizer serves only as a feasible incumbent.

Twenty finite-difference derivative checks agree to at most `9.1433e-11`.
All 85 archived hashes match. Numerical work took `.1289` seconds, excluding
Python startup. All nine geometry/sigma rows are retained. There were no retries
or additional levels .05/.15 in this calibration run.

## Interpretation

Oracle calibration improves BOTH geometries. Mono improves more, so the noisy
sharing disadvantage grows rather than disappearing. This rules out a simple
explanation in which the recorded reversal was solely an unadjusted free bias
for one code. It supports a representation/decoder-class cost within this
specific nonlinear, energy-one comparison.

The control remains restricted: no geometry is retrained for noise, the tied
decoder and gain constraint remain, mono drops one concept and predicts its
prior, and all coverage loss is included in total MSE. No conclusion is made
about optimal predictors outside that class, adversarial robustness, larger
loads, LLMs or diffusion. The linear tie `1/4+sigma^2` is context from existing
mathematics, not an extra experimental arm or a unique explanation of all
nonlinear effects.

The next decision is independent verification and the senior prior-source
comparison. If those support a substantive claim, only a separately specified
single real-model mechanism test is warranted. This result by itself is not a
publication-novelty or ICML-acceptance guarantee.

## Completed independent review and final decision

The independent review has now passed. All 85 raw hashes matched and all 36
frozen/calibrated per-feature MSE checks agreed by bounded direct Gaussian
quadrature within 1.943e-16. The largest omitted-tail bound was 3.913e-31.
Curvature constants, saved interval lower bounds, tail exclusions and final
active-interval global bounds were also checked. The raw archive was unchanged.

The numerical calibrated sharing-minus-mono brackets are
[.005425091284607053, .0054251096956468015] at sigma .30 and
[.02404191316021509, .024041936637088035] at .60. These are floating-point
global-gap diagnostics, not exact interval-arithmetic theorems.

The senior review approves moving to one prespecified real-model mechanism
test and stopping optional toy elaboration. The supported claim is restricted
to globally clean-selected geometry, equal width/energy, the tied-ReLU decoder
class and a corruption cost not removed by bias calibration alone. The broad
clean/noisy tradeoff is established prior knowledge; novel predictive scope
still has to be demonstrated.
