# Independent stop check (auditor, own code)

Script: `claude_agent/repair_v3/independent_check/indep_stop_check.py` (does not import author modules).
Rows loaded: train 0:256, calibration 256:512, and the 896 P rows (seed 20261008, perm[896:1792]). No E rows were touched.

## Results
| Quantity | Author | Independent |
|---|---|---|
| Sharing angle t* (720-point grid + bounded refinement, global bias fits) | -0.5806 | -0.58062 (train loss 0.37163) |
| Mono retained feature | feature 1 | feature 1 (0.4170 vs 0.7125) |
| Delta_P(0) | ~ -0.015 | -0.01507 |
| Point crossing | ~ 0.525 | 0.5249 |
| 98.33% bootstrap band of Delta(0) | includes 0 | [-0.0861, +0.0468], includes 0 |
| Fraction of resamples with Delta(0)<0 | -- | 0.712 |
| Fraction of resamples with a crossing in [0.05,0.9] | ~48% | 43.6% (bootstrap seed 12345) |
| f1, f2, p_r | -- | 0.863, 0.711, 0.457 |
| v(p_r) | -- | 0.6616 |
| B | ~0.048 | 0.04845 |
| sqrt(G/B) | ~0.558 | 0.5577 |

Delta_P(sigma) for sigma = 0, 0.1, ..., 1.0: -0.0151, -0.0145, -0.0122, -0.0089, -0.0051, -0.0011, +0.0032, +0.0076, +0.0121, +0.0166, +0.0211.

## Discrepancy
The crossing fraction is 43.6% here and about 48% for the author. Monte Carlo error with 2000 resamples is about 1.1 points, so seed noise alone may not cover the full gap. The cause could be a different resample stream or a different crossing or interpolation convention. It does not change the conclusion. All other numbers match to the stated precision.

## Conclusion
My computation supports the decision. The point estimates agree: the crossing is about 0.525, and the theory value sqrt(G/B) = 0.558 is close to it. Even so, the sign of Delta(0) is not resolved. Its 98.33% band runs from -0.086 to +0.047, and only about 44 to 48% of resamples show a crossing in [0.05, 0.9]. The crossing forecast is therefore not informative, it fails the precision gate, and stopping before final evaluation is justified.
