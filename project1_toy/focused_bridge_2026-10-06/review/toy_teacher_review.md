# Independent toy teacher review: protocol v1

6 October 2026. Root independently inspected the student's weighted gradient,
fixed-bias optimizer, solver, source snapshots, settings and saved results.

## What the student did correctly

The protocol was implemented faithfully: all six cases, six seeds per case,
4,000 steps, equal encoder energy, both detector definitions and every specified
noise value were retained. No unfavorable seed was dropped or replaced. Weighted
gradients use both appearances of the tied encoder. Bias minimization includes
all ReLU-active intervals and boundaries rather than assuming convexity.
The student appropriately reported nonstationary optimizer outcomes and the
floating-point threshold caveat instead of presenting them as theorem evidence.

The independent audit used all sixteen active-state masks, latent scalar Gaussian
thresholds and numerical quadrature of the rectified noisy decoder. It verified
163 saved file hashes, 96 evaluated models and 960 detector/model/noise rows.
All 36 training trajectories, final weights and biases replayed exactly in the
recorded environment (maximum difference zero). The maximum positive-noise
risk discrepancy was 6.66e-16; bias-optimal loss discrepancy 2.78e-17; independent
decoder-MSE integration discrepancy 7.78e-14. Evidence is in
`toy_verification.json` and `toy_verification_direct.json`.

## Material limitations requiring action or qualification

1. **Loss stability is not stationarity.** Nine runs fail even the prespecified
   loss-stability check. Some passing runs still have large tangent gradients.
   In the low-p unequal-importance cases, the equal-amplitude pair is analytically
   nonstationary, but projected coordinatewise Adam remains close to it. This
   algorithm's outcome cannot be substituted for clean optimal geometry.
2. **Global geometry is not certified by the grid.** The dense-case math proof
   supplies two actual global results; low-p grid minima remain numerical.
3. **Two final-iterate clean detection claims are numerically unstable.** For
   p=.5 and weights [1,.5], seeds 1 and 4 give algebraic-threshold weighted error
   .125 but direct float64 ReLU-threshold error .25. Reoptimized seed 4 has the
   same discrepancy. Nearly zero column weights and a bias at .5 make rounding
   change a strict decision. Raw outputs are preserved; these values do not show
   robust recovery of the omitted concept. Positive tested noise risks do not
   have this discrepancy.
4. **Reconstruction and detection differ.** The numerical low-p unequal-weight
   clean-MSE minimizer need not beat mono in binary detection. The student correctly
   retained that unfavorable fact. A reconstruction theorem is not a detection
   theorem without an additional argument.

These are evidenced limitations, not reasons to criticize the correct bias
derivation or demand cosmetic changes. No source-code repair to the population
gradient or Gaussian risk calculation is required by this review.

## Bounded educated direction

For the optimizer blocker, test the already derived one-angle profiled objective
on the two rare unequal-importance cases, starting at the analytically
nonstationary equal pair. This removes the coordinatewise projected-Adam radial
stall while retaining the model, objective and energy. An Armijo angle step with
exact fixed-geometry biases is a numerical solver diagnostic, not a new geometry
family or a guarantee of global convergence. Use one recorded algorithm and no
hyperparameter search; retain failures.

The mathematics teacher's complementary next direction is to certify one
already tested low-p geometry by checking its active branches. Those two focused
actions address the identified blocker. They do not authorize new model families,
new data distributions or broad sweeps.
