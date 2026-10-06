# Focused two-feature training bridge

This directory contains the working student's bounded numerical experiment for
Project 1. It preserves the old infrastructure and all earlier outputs. The
authoritative protocol is `../protocol.md`; a copy is archived within each run.
The research question is whether clean training chooses geometry predicted by a
tractable population calculation, and whether that geometry predicts feature
detection risk under specified corruption. The test is not a completed load
phase diagram or a novelty claim.

## Model and preregistered settings

- Two independent Bernoulli concepts; both have probability 0.05, 0.20 or 0.50.
- One storage dimension, tied encoder/decoder, ReLU reconstruction, free biases.
- Encoder squared norm is one throughout training and for every comparison.
- Importance is either `(1,1)` or `(1,0.5)`; the clean objective is the **sum** of
  importance-weighted mean squared reconstruction errors over all four states.
- For each of six cases, seeds 0 through 5 train for exactly 4,000 projected Adam
  steps, learning rate 0.01. The final iterate is evaluated. No seed/checkpoint
  selection, altered hyperparameters or retries are permitted.
- Separate geometry diagnostic: exactly 361 equally spaced angles from
  `-pi/2` to `pi/2`, plus explicitly represented `-pi/4` and `pi/4` candidates.
  Redundant candidates are retained. Endpoints have exactly zero dropped weights.
  The angular grid supplies a numerical comparison, not a global proof.
- Gaussian noise is added **in code space**, with standard deviations
  `0, 0.05, 0.15, 0.30, 0.60`. Exact state enumeration and Gaussian integration
  supply the primary risk estimates.

## Why this connects to the derivations

The prior formula computes detection risk given an encoder and threshold. It
does not establish which encoder or threshold training chooses. This test adds
the clean training objective and importance weighting. For fixed encoder, bias
optimization can be performed by enumerating ReLU activation intervals: within
each interval the objective is quadratic, so the finite candidate set consists
of its admissible stationary point and interval boundaries. The all-off plateau
must also be considered. This enumeration does not assume global convexity.
`bridge_math.py` retains all numerical ties and plateau information.

Each model is scored with both the actual decoder decision
`ReLU(Gb+bias)>0.5` and the separately defined centered midpoint detector. A
favorable midpoint result cannot replace an unfavorable decoder result.
Ordinary noisy feature detection is the stated robustness task. This experiment
does not certify adversarial robustness or AI safety.

## Run and reproduce

Requirements: Python, NumPy and SciPy. Matplotlib is optional for the separate
reporting script. From this directory:

```powershell
& 'C:/Users/indra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' run_bridge.py --output run_reproduction
```

The output must be a fresh directory; the program refuses to overwrite an
existing one. Settings, environment, source snapshots and protocol are written
before checks/training. Checks must pass before any new training. The immutable
source snapshot within `run_v1` is the exact implementation used for that run.

Prechecks cover weighted finite-difference gradients away from ReLU kinks,
fixed-geometry scalar-bias minima independently checked with bounded numerical
minimization on each interval, and independently integrated Gaussian detection
errors. Numerical checks support the implementation; mathematical proof remains
the responsibility of the independent mathematical review.

## Raw output structure

- `settings.json`, `environment.json`, `prechecks.json`, `timings.json`.
- `source_snapshot/`: exact code and protocol used before training.
- `training_summary.csv`: every final iterate, runtime, gradient and
  loss-stability diagnostic, bias-reoptimization gap and angular-grid comparison.
- `geometry.csv`: every evaluated encoder/bias, Gram matrix, alignment, energy
  and detector state gaps, including dropped features with undefined alignment.
- `risks.csv`: both detectors, all sigma values, weighted/unweighted sum errors,
  per-feature errors and conditional false-positive/false-negative rates, plus
  exact decoder MSE. Weighted results are sums, not divided by total importance.
- `comparisons.csv`: both one-feature retention objectives and the clean
  preferred baseline. Equal-loss baseline ties are explicitly recorded.
- `landscape.csv` and per-case `landscape.npz`: every angular candidate and its
  bias-minimized clean loss, without refinement of the grid.
- Per-case `seed_*.npz`: final weights/biases, full 4,001-entry trace and
  100-step checkpoints, with optimizer moments. Histories have columns
  `step, weighted_loss, encoder_energy, tangent_gradient_norm, bias_gradient_norm`.
- Per-case bias-candidate JSON: finite candidates, their objective values,
  stationary intervals, retained ties and any globally tied all-off plateau.
- `sha256_manifest.json`: hashes of sources and original raw outputs. Reporting
  artifacts are saved separately and do not change these hashes.

## Bounded angular follow-up reproduction

After the independent v1 review, exactly two angle-profile Armijo diagnostics
were run under `../followup_protocol.md`. Their code is
`run_angle_diagnostic.py`; raw outputs are `run_angle_diagnostic_v1/` and the
readable report is `angle_diagnostic_results.md`. From this directory, reproduce
into a fresh folder:

```powershell
& 'C:/Users/indra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' run_angle_diagnostic.py --output run_angle_reproduction
```

The working runner received a **CLI-only** change after that recorded run:
`--output` allows a fresh directory. Its default remains
`run_angle_diagnostic_v1` and it refuses existing directories. The archived
original source snapshot and every recorded output remain unchanged. The
numerical algorithm, cases and settings are unchanged; no scientific cases were
rerun for this interface change. The original `run_v1` landscapes remain the
explicit reference inputs for the diagnostic comparison and must be available
beside the runner. Independent teacher checks are recorded under `../review/`.

## Comparisons and limitations

We retain the actual final trained model and, **as a separate diagnostic**, its
bias-reoptimized version. Additional comparisons are the best prescribed grid
candidate, a fixed equal-amplitude antipodal code, and both monosemantic
retention codes, all with optimal clean biases. Bias reoptimization is not an
unlogged training improvement and cannot be relabeled the original result.

Loss stability compares the last two 100-step windows with tolerance `1e-5`.
Passing is not a global convergence proof. Gradient norms and all failures remain
available. At zero noise, decisions use strict `>`; states on or extremely close
to a threshold can change decision under floating-point perturbations. Recorded
state gaps make these cases visible. Nonzero-noise errors are continuous CDF
integrals.

## Stop criterion and next step

This protocol stops after six cases, 36 fixed-step trainings and the prescribed
landscape diagnostic. No new loads, correlations, pretrained models, diffusion
or optimizer searches are part of it. The independent teacher should check the
code, raw outputs and claims. Any discrepancy should lead to its smallest
required correction, rather than a broader sweep. Results are stated in the
separate report after the run, including unfavorable comparisons and unresolved
geometry optimality.
