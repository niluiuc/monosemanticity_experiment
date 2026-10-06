# Generated results: Project 1 toy protocol v1

This report is generated from saved measurements. The complete protocol is
`plan_before_run.md`; exact per-feature values are in the CSVs. No seeds are excluded.

## Mathematical and simulation checks

- Pre-run checks: passed.
- Gradient relative difference: 1.35562816273e-10.
- Pair closed versus state-enumerated risk maximum difference: 1.11022302463e-16.
- Trained feature comparisons: 1920.
- Maximum trained absolute simulation-minus-exact difference: 0.00599948979.
- Maximum pair absolute simulation-minus-exact difference: 0.00233758004.
- Familywise-tolerance failures: trained 0, pair 0.
- Matched-bound violations: 0.
- Learned bound minus exact risk: min 0.354057, median 0.588103, max 0.638304.

The upper bound is not a fitted prediction. A valid but loose bound does not
locate a sharp boundary. Exact risk agreement verifies the specified probability
calculation and implementation, not novelty or generalization to other models.

## Fixed-code crossings

| Pair amplitude | Pair energy | Mono energy | p | Exact crossing sigma |
|---|---|---|---|---|
| 0.707106781 | 1.000000 | 1 | 0.2 | 0.279938913 |
| 1.000000000 | 2.000000 | 1 | 0.2 | 0.658349502 |

These crossings compare specified fixed codes, not optimized trained networks.

## Training: every final iterate

| p | Seed | Final clean reconstruction MSE | Restricted mono MSE | Loss-window change | Diagnostic passed | Weak columns |
|---|---|---|---|---|---|---|
| 0.05 | 0 | 0.109264326 | 0.190000000 | 3.72936e-06 | True | 0 |
| 0.05 | 1 | 0.109228685 | 0.190000000 | 9.53182e-07 | True | 0 |
| 0.05 | 2 | 0.109217194 | 0.190000000 | 2.92411e-07 | True | 0 |
| 0.15 | 0 | 0.367426058 | 0.510000000 | 3.48025e-05 | False | 0 |
| 0.15 | 1 | 0.366871650 | 0.510000000 | 5.45385e-06 | True | 0 |
| 0.15 | 2 | 0.366879411 | 0.510000000 | 4.94752e-06 | True | 0 |
| 0.30 | 0 | 0.759645109 | 0.840000000 | 2.24347e-05 | False | 0 |
| 0.30 | 1 | 0.755567060 | 0.840000000 | 7.34971e-06 | True | 0 |
| 0.30 | 2 | 0.755500671 | 0.840000000 | 1.00173e-05 | False | 0 |
| 0.50 | 0 | 0.981212927 | 1.000000000 | 6.77806e-05 | False | 0 |
| 0.50 | 1 | 0.980740928 | 1.000000000 | 0.000413351 | False | 0 |
| 0.50 | 2 | 0.979961817 | 1.000000000 | 0.000350191 | False | 0 |

This convergence diagnostic measures recent loss stability. It is not a proof
of stationarity, global optimality, or agreement between initialization seeds.

## Learned versus restricted mono detection risk

Negative differences favor the learned code. Values below are **total errors
summed over all eight concepts**, averaged across the three retained seeds.
Min/max show initialization variation, not confidence intervals. See
`paired_comparisons.csv` for individual-seed simulation estimates and paired SEs.

| p | Detector | sigma | Mean exact learned-minus-mono | Seed min | Seed max | Seeds learned better |
|---|---|---|---|---|---|---|
| 0.05 | matched | 0.00 | -0.18000000 | -0.18000000 | -0.18000000 | 3/3 |
| 0.05 | matched | 0.05 | -0.18000000 | -0.18000000 | -0.18000000 | 3/3 |
| 0.05 | matched | 0.15 | -0.05779039 | -0.05786721 | -0.05768428 | 3/3 |
| 0.05 | matched | 0.30 | +0.70588880 | +0.70583291 | +0.70596074 | 0/3 |
| 0.05 | matched | 0.60 | +1.27070861 | +1.27069487 | +1.27072184 | 0/3 |
| 0.05 | decoder | 0.00 | -0.18000000 | -0.18000000 | -0.18000000 | 3/3 |
| 0.05 | decoder | 0.05 | -0.09701242 | -0.09714013 | -0.09684433 | 3/3 |
| 0.05 | decoder | 0.15 | -0.03065401 | -0.03072236 | -0.03061190 | 3/3 |
| 0.05 | decoder | 0.30 | -0.10737944 | -0.10741196 | -0.10735573 | 3/3 |
| 0.05 | decoder | 0.60 | +0.15080069 | +0.15069288 | +0.15098472 | 0/3 |
| 0.15 | matched | 0.00 | -0.42000000 | -0.42000000 | -0.42000000 | 3/3 |
| 0.15 | matched | 0.05 | -0.41999676 | -0.41999767 | -0.41999495 | 3/3 |
| 0.15 | matched | 0.15 | -0.14192034 | -0.14304540 | -0.13972044 | 3/3 |
| 0.15 | matched | 0.30 | +0.60053790 | +0.60009049 | +0.60141358 | 0/3 |
| 0.15 | matched | 0.60 | +0.95798256 | +0.95788660 | +0.95817237 | 0/3 |
| 0.15 | decoder | 0.00 | -0.42000000 | -0.42000000 | -0.42000000 | 3/3 |
| 0.15 | decoder | 0.05 | -0.41691971 | -0.41722330 | -0.41631540 | 3/3 |
| 0.15 | decoder | 0.15 | -0.24163692 | -0.24207785 | -0.24091757 | 3/3 |
| 0.15 | decoder | 0.30 | -0.11960282 | -0.11986311 | -0.11908345 | 3/3 |
| 0.15 | decoder | 0.60 | +0.16842456 | +0.16825815 | +0.16857283 | 0/3 |
| 0.30 | matched | 0.00 | -0.48000000 | -0.48000000 | -0.48000000 | 3/3 |
| 0.30 | matched | 0.05 | -0.46491720 | -0.47040560 | -0.45421645 | 3/3 |
| 0.30 | matched | 0.15 | +0.07887190 | +0.07425701 | +0.08785941 | 0/3 |
| 0.30 | matched | 0.30 | +0.40470482 | +0.40310425 | +0.40782400 | 0/3 |
| 0.30 | matched | 0.60 | +0.43633719 | +0.43543309 | +0.43810203 | 0/3 |
| 0.30 | decoder | 0.00 | -0.48000000 | -0.48000000 | -0.48000000 | 3/3 |
| 0.30 | decoder | 0.05 | -0.47999999 | -0.48000000 | -0.47999998 | 3/3 |
| 0.30 | decoder | 0.15 | -0.43443277 | -0.43675089 | -0.42992352 | 3/3 |
| 0.30 | decoder | 0.30 | -0.08974883 | -0.09202019 | -0.08532398 | 3/3 |
| 0.30 | decoder | 0.60 | +0.12756423 | +0.12681657 | +0.12902262 | 0/3 |
| 0.50 | matched | 0.00 | -0.65364583 | -0.67187500 | -0.63281250 | 3/3 |
| 0.50 | matched | 0.05 | -0.63002342 | -0.64790148 | -0.62016473 | 3/3 |
| 0.50 | matched | 0.15 | -0.49506786 | -0.49698433 | -0.49127777 | 3/3 |
| 0.50 | matched | 0.30 | -0.34383441 | -0.34812708 | -0.33591440 | 3/3 |
| 0.50 | matched | 0.60 | -0.31268258 | -0.31894006 | -0.30098213 | 3/3 |
| 0.50 | decoder | 0.00 | -0.64843750 | -0.68359375 | -0.62109375 | 3/3 |
| 0.50 | decoder | 0.05 | -0.62547867 | -0.64193819 | -0.61724831 | 3/3 |
| 0.50 | decoder | 0.15 | -0.49166489 | -0.49397717 | -0.48749872 | 3/3 |
| 0.50 | decoder | 0.30 | -0.34162382 | -0.34618164 | -0.33344374 | 3/3 |
| 0.50 | decoder | 0.60 | -0.31194149 | -0.31819850 | -0.30016277 | 3/3 |

## Limits on interpretation

- Binary independent concepts, uniform importance, one feature load (8/4).
- Training uses the exact population, not finite noisy training samples.
- The mono baseline uses known concepts; it is a restricted, idealized control.
- Noise is isotropic Gaussian in code space. No input-space or adversarial claim.
- The matched detector knows p and differs from the learned decoder.
- A low detection error for rare features can hide frequent missed presences;
  false positive and false negative rates are reported separately in the CSV.
- Geometric overlap is not by itself a semantic assessment of natural-model features.
- This run contains no load sweep, importance sweep, recursive loop or real model.

## Next decision

Stop here and review these results. The next experiment requires a new dated
entry in the living plan. Do not retrospectively select a detector, seed or
noise range that makes the preferred story look stronger.

## Plots

- `plots/training_losses.png`: all training traces, including unsuccessful cases.
- `plots/learned_vs_mono_risk.png`: both detectors, every initialization seed.
- `plots/exact_vs_measured.png`: all learned-feature prediction checks.
- `plots/bound_vs_exact.png`: bound looseness as well as validity.
- `plots/all_learned_gram_matrices.png`: every learned interference matrix.
- `plots/fixed_pair_phase_diagram.png`: exact fixed-code risk comparison.
