# Review of saved protocol v1 results

**No additional training or simulation was performed for this review.**
The original run remains unchanged. This file separates observations from interpretation.

## Presentation correction

The original `plots/learned_vs_mono_risk.png` has a plotting defect: successive
bottom-only limits on shared y axes froze an upper limit of about 0.30, clipping
some high-noise values. That original file and its code are preserved for audit.
The corrected plot here sets one upper limit after considering **all** exact values
and all displayed Monte Carlo confidence limits. It does not change any measurement.
All six views are regenerated from the existing data in this review directory.
An initial attempt to create the review plots failed because their parent directory
did not exist; the plotting utility was repaired to create parent directories.

## Observations

- All 12 trained settings have lower final clean reconstruction MSE than the specified restricted mono baseline.
- 6/12 settings fail the prespecified loss-stability diagnostic. Their outcomes remain included.
- At p=0.05, 0.15 and 0.30, both detectors favor the learned code without noise;
  at sigma=0.60 both favor the restricted mono baseline for every seed.
- Detector choice materially affects the intermediate-noise comparison: at sigma=0.30
  the matched detector favors mono for those three activation rates, while the
  trained decoder favors the learned code. Reporting only one would conceal this.
- At p=0.50, both detectors favor the learned code at every tested noise level for
  all seeds. There is no observed reversal within this noise range in that case.
- The error bound has no observed violations, but its learned-feature median
  slack is 0.588103 probability units. It is too loose here to claim a sharp boundary.
- Exact risk versus Monte Carlo agreement supports the calculation for a fixed
  dictionary and detector. It does not establish a theorem selecting trained geometry.

## Geometry: post-run descriptive inspection

The saved Gram matrices suggest antipodal pair organization at the three lower
activation rates and less pair-specific organization at p=0.50. The following
quantities describe all seeds and were computed **after** inspecting the matrices;
they were not preregistered hypothesis tests. See `geometry_review.json` for partners.

| p | Seed | Mean most-negative cosine per feature | Maximum absolute nonpartner cosine | Partners all mutual |
|---|---|---|---|---|
| 0.05 | 0 | -0.999988294 | 0.017845524 | True |
| 0.05 | 1 | -0.999988774 | 0.010874459 | True |
| 0.05 | 2 | -0.999993829 | 0.004700877 | True |
| 0.15 | 0 | -0.999991684 | 0.035158103 | True |
| 0.15 | 1 | -0.999995302 | 0.015376472 | True |
| 0.15 | 2 | -0.999998051 | 0.015151735 | True |
| 0.30 | 0 | -0.999988793 | 0.056521252 | True |
| 0.30 | 1 | -0.999999857 | 0.025816696 | True |
| 0.30 | 2 | -0.999999731 | 0.025317281 | True |
| 0.50 | 0 | -0.536727655 | 0.678531435 | False |
| 0.50 | 1 | -0.562940360 | 0.846287268 | False |
| 0.50 | 2 | -0.358164456 | 0.761786838 | False |

These angles are descriptive, not a claim of global optimality, semantic
monosemanticity in natural models, or a causal intervention.

## Rare concepts: report conditional errors too

A detector that mostly predicts absence can look accurate when p is small.
The table below averages exact conditional rates across all features and seeds.
These are different quantities from unconditional error.

| p | Detector | sigma | False-positive rate | False-negative rate |
|---|---|---|---|---|
| 0.05 | matched | 0.00 | 0.00000000 | 0.05000000 |
| 0.05 | matched | 0.30 | 0.13722551 | 0.13534086 |
| 0.05 | matched | 0.60 | 0.28523357 | 0.28061742 |
| 0.05 | decoder | 0.00 | 0.00000000 | 0.05000000 |
| 0.05 | decoder | 0.30 | 0.01232832 | 0.47521680 |
| 0.05 | decoder | 0.60 | 0.12666020 | 0.49374166 |
| 0.15 | matched | 0.00 | 0.00000000 | 0.15000000 |
| 0.15 | matched | 0.30 | 0.17418708 | 0.17268928 |
| 0.15 | matched | 0.60 | 0.29738336 | 0.28757436 |
| 0.15 | decoder | 0.00 | 0.00000000 | 0.15000000 |
| 0.15 | decoder | 0.30 | 0.02496591 | 0.41815865 |
| 0.15 | decoder | 0.60 | 0.14892735 | 0.47086009 |
| 0.30 | matched | 0.00 | 0.00000000 | 0.30000000 |
| 0.30 | matched | 0.30 | 0.22410764 | 0.22535977 |
| 0.30 | matched | 0.60 | 0.30852200 | 0.29913647 |
| 0.30 | decoder | 0.00 | 0.00000000 | 0.30000000 |
| 0.30 | decoder | 0.30 | 0.08182510 | 0.35133001 |
| 0.30 | decoder | 0.60 | 0.20421159 | 0.41387202 |
| 0.50 | matched | 0.00 | 0.16829427 | 0.16829427 |
| 0.50 | matched | 0.30 | 0.23091588 | 0.23091588 |
| 0.50 | matched | 0.60 | 0.31207887 | 0.31207887 |
| 0.50 | decoder | 0.00 | 0.16048177 | 0.17740885 |
| 0.50 | decoder | 0.30 | 0.22142689 | 0.24095751 |
| 0.50 | decoder | 0.60 | 0.30401080 | 0.32033221 |

## What this does and does not establish

The experiment is a successful initial implementation and a controlled example
of a noise-dependent tradeoff in some tested regimes. It is not the complete
phase diagram over sparsity, load and importance, and it does not establish
ICML novelty or transfer to a real model. The dense-case result and differing
detector comparisons prevent a universal "superposition hurts robustness" claim.

## Proposed next work; not executed

1. Resolve optimizer stability with a logged, fixed-duration follow-up using
   all original settings. Preserve this run and compare convergence diagnostics;
   do not pick a checkpoint based on robustness or discard a failed seed.
2. If the geometry and comparisons are stable, extend this same controlled
   setup to feature load. State the energy convention and baseline before running.
3. Only then choose the smallest real-model experiment testing the established
   mechanism. Do not add model downloads or recursive loops at this stage.
