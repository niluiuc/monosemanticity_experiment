# Two-case angular solver diagnostic

6 October 2026. This is the bounded follow-up specified in
`../followup_protocol.md` after the independent teacher identified nonstationary
projected-Adam trajectories. Original `run_v1` is untouched.

## Question and implementation

Does direct descent on the exact bias-profiled angular objective leave the
analytically nonstationary equal-amplitude antipodal geometry and reach a local
stationary point? This tests a solver blocker in the training-to-geometry link;
it does not prove global optimality or publication novelty.

Exactly two deterministic cases were run: independent Bernoulli rate 0.05 or
0.20, importance `[1,0.5]`, one storage dimension and encoder energy one.
Starting angle is `-pi/4`. Fixed-geometry biases are globally optimized by the
finite activation-interval calculation at every iterate. The angle derivative
contracts the weighted tied gradient with `(-sin(theta),cos(theta))`.

Each Armijo iteration starts with step 0.1, accepts sufficient decrease with
coefficient `1e-4`, and may halve at most 30 times. Stopping is absolute angle
gradient at most `1e-8` or 4,000 iterations, retaining the stopping iterate. No
extra initializations, hyperparameters or optimizer retries were used.

## Results

| Activation rate | Accepted updates | Final angle, radians | Final weighted reconstruction loss | Absolute angle gradient | Stop |
|---|---:|---:|---:|---:|---|
| 0.05 | 1,279 | -0.5745808452382377 | 0.017742880541346515 | 9.978e-9 | Gradient tolerance |
| 0.20 | 678 | -0.41625677289385893 | 0.07775208251629454 | 9.792e-9 | Gradient tolerance |

All accepted steps were 0.1: no halving was required. Recorded objective values
are nonincreasing. Both final losses are slightly lower than the previous fixed
angular-grid minima (differences `-1.072e-7` and `-7.897e-7`). An off-grid local
stationary point is not a global geometry theorem.

The two initial angle derivatives are `-0.024872047244094492` and
`-0.09142857142857144`, respectively. Central finite-difference checks at the
initial and final points agree with the envelope gradient to at most `6.491e-12`.
Each path changes its selected ReLU-active mask once, at recorded iteration 13
or 41. No recorded iterate has a tied finite bias minimizer, all-off minimizing
plateau or preactivation within `1e-12` of zero. This does not assert that a
continuous trajectory avoids activation boundaries between sampled iterates.

## Detection outcomes and an unfavorable result

The table below uses the actual decoder's strict threshold and importance-weighted
**sum** of feature errors. The clean-preferred mono control retains feature 0.
Both mono controls and the separate centered-midpoint detector are retained in
the full raw CSV; no baseline is selected retrospectively by noise performance.

| p | Code | sigma=0 | 0.05 | 0.15 | 0.30 | 0.60 |
|---|---|---:|---:|---:|---:|---:|
| 0.05 | Angular stopping iterate | 0.027500 | 0.027500 | 0.028901 | 0.058316 | 0.223667 |
| 0.05 | Mono retaining 0 | 0.025000 | 0.025000 | 0.025429 | 0.072790 | 0.227328 |
| 0.20 | Angular stopping iterate | 0.100000 | 0.112228 | 0.117826 | 0.159442 | 0.310097 |
| 0.20 | Mono retaining 0 | 0.100000 | 0.100000 | 0.100429 | 0.147790 | 0.302328 |

**Better clean reconstruction is not automatically better binary detection.**
At p=0.20, this local stationary superposed code has clean MSE 0.07775208, lower
than mono's 0.08, but ties mono's actual-decoder clean detection error and has
higher error at every positive tested noise level. At p=0.05, its actual decoder
has higher errors at the lowest noise levels but lower errors at 0.30 and 0.60
than the clean-preferred mono control. These observations prevent a universal
"superposition is less robust" conclusion from this small setting.

The alternative centered-midpoint detector gives different numbers: clean
weighted errors 0.00375 and 0.02 for the two superposed stopping codes, with errors
0.195742 and 0.265819 at sigma 0.30. These diagnostics cannot replace actual-decoder
outcomes. All per-feature false positives, false negatives and exact decoder MSE
are recorded in `run_angle_diagnostic_v1/risks.csv`.

## Files, reproduction and limits

- Runner: `run_angle_diagnostic.py`.
- Fresh archived run: `run_angle_diagnostic_v1/`.
- `settings.json`, `environment.json`, source/protocol snapshots and SHA-256
  manifest were saved; settings and snapshot precede both solver runs.
- Each case includes every iterate, every Armijo trial, exact scalar-bias
  candidates and active-mask/tie information, stopping weights/biases and summary.
- The run stops after these two cases. No additional angles, seeds, models or
  solver settings are evaluated as an exploratory campaign.

To reproduce from the toy directory, use a fresh output directory:

```powershell
& 'C:/Users/indra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' run_angle_diagnostic.py --output run_angle_reproduction
```

After independent teacher review, the **working** runner received only this
`--output` interface option. Its default directory is unchanged and existing
directories are refused. The archived original source snapshot and all raw
outputs remain untouched; the numerical algorithm/settings are unchanged. Only
`--help` was checked after this interface edit, without new scientific runs.
Existing `run_v1` angular landscapes are the explicit reference input and must
remain beside the runner. Use the bundled Python/NumPy/SciPy environment; no
new dependency installation is required.

This solver diagnosis addresses the observed projected-Adam stall. The independent
teacher checked the implementation, all saved iterates and the reported risks;
see `../review/angle_teacher_review.md` and `../review/angle_verification.json`.
The mathematical stream separately supplies a bounded one-case global certificate;
this numerical report does not substitute a local stationary point for that proof.
