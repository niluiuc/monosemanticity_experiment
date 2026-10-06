# Finite verification of the predicted frequency transition

Recorded 6 October 2026, after Stage A identified a candidate transition and before new numerical execution. Execute only after independent mathematical review supports the prediction; otherwise report the blocker without substituting a sweep.

## Question

Does exact geometry selection at a few fixed frequencies agree with the clean-storage prediction pc=(3-sqrt(5))/2? For those same selected geometries, what is the actual trained decoder's noise-risk difference from mono? The two questions remain distinct.

## Smallest useful test and fixed settings

- Five frequencies only: p=1/20,1/5,7/20,3/8,2/5 (.05,.20,.35,.375,.40).
- All other settings remain the preceding protocol's binary independent concepts, n=2,m=1, encoder energy one, tied ReLU/free bias decoder, importance [1,1/2].
- .05 checks the previously local-only rare case; .20 rechecks the certified anchor; .35 and .375 test sharing approaching the predicted transition; .40 tests the mono side.
- For each below-transition p, reuse the reviewed rational geometry/root-isolation backend and exhaustive feasible bias-branch comparison. Retain full candidates, feasibility/root/value bounds and ties. A strict winning interval is a computer-assisted global certificate; unresolved overlaps must remain unresolved, with no automatic additional p values.
- Above the transition, use the proved mono solution w=(1,0), biases (0,p). Keep both mono controls and identify the primary comparator by the clean objective, not noise outcomes.
- No optimizer/training campaign is required for this exact population selection check. Reuse the prior training agreement as an existing anchor; do not imply that every optimizer reaches a global optimum.
- Primary noise settings remain sigma=0,.05,.15,.30,.60. Evaluate both actual decoder and separately labeled midpoint detector, per-feature errors/FP/FN and continuous decoder MSE with the existing exact integration functions.
- Geometry is specified by an algebraic root but converted to float64 for noise evaluation. The evaluation uses analytical Gaussian CDF formulas; it is finite-precision numerics, not an exact-sign certificate of every noisy comparison.

## Plots and bounded crossings

- Save a clean-storage plot with the proved phase boundary, and certified geometry/loss at the five selected p values. Do not imply a sampled curve is a global geometry theorem between points.
- Save actual-decoder risk-difference curves over 240 predefined log-spaced positive sigma values from .001 to 4, using the same selected encoders. This evaluates the existing analytic formula for visualization; it does not train or search new geometries. Save every plotted value.
- Primary reporting still shows all five prescribed noise points. Preserve zero-noise decisions and numerical ties separately.
- A display-curve sign change with endpoint magnitudes above 1e-12 may receive one Brent root check within that existing bracket, to describe the visualized crossing. Save brackets, residuals and iteration diagnostics. These roots are numerical and their count is not a completeness theorem; roots beyond the display interval or too small for reliable sign evaluation may be missed.
- Save source code, protocol, environment, all outputs, hashes and original failures before interpretation. Do not overwrite earlier runs or choose a favorable detector.

## Stopping criterion and review

Stop after the five geometry cases, fixed risk evaluations and specified plots/root diagnostics. Any unresolved global certificate, numerical tie or contrary risk pattern is reported honestly. Root independently verifies candidate coverage/results, selected geometries and scalar-noise risk calculations and inspects the plots. No additional frequencies, solver configurations, loads or pretrained models are added automatically. The result does not establish the complete variable-load phase diagram, novelty or real-model transfer.
