# One decisive decoder-calibration control

This directory contains a retrospective evidence audit, senior research decision
and one prospectively specified control. `calibration_protocol.md` was saved
before execution; `professor_decision.md` approves its method and scope.

The question is whether the existing dense, globally clean-optimal shared code's
noisy reconstruction disadvantage survives fair oracle bias calibration of both
shared and mono codes. Read `calibration_results.md` for the result and scope.
Nothing here trains a new geometry, introduces a new dataset or switches from
reconstruction MSE to a detection metric.

## Reproduce

Python, NumPy and SciPy are already available in the bundled environment. From
this directory, use a fresh output directory:

```powershell
& 'C:/Users/indra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' run_calibration_control.py --senior-review professor_decision.md --output run_reproduction
```

The runner refuses to overwrite an existing directory. Sources, protocol,
approval, settings and environment are saved before calculation. The immutable
source used in the recorded run is inside `run_v1/source_snapshot/`.

## Fixed scientific settings

- Independent fair binary concepts, equal importance, n=2,m=1, encoder energy 1.
- Two relative-sign representatives of the already proved clean sharing optimum
  and the important-feature-retention mono code. Equal-importance mono swaps are
  symmetric, not a noise-selected baseline.
- Sigma zero is the clean anchor. Only sigma .30 and .60 receive noisy-bias
  calibration; those corruption levels already showed frozen-decoder reversal.
- Every geometry receives the same freely optimized scalar decoder biases.
- Primary outcome is population sum reconstruction MSE, also retained per feature.
- Bias calibration is oracle population information, not finite-data deployment.
- No linear arm, new training, frequency/load sweep or extra model is added.

## Numerical global-gap method

For each nonzero column, exact Gaussian ReLU moments give loss and first
derivative. A bounded local minimizer supplies only a feasible upper incumbent;
it is never treated as proof of global optimality. Branch-and-bound tracks
interval lower bounds from midpoint Taylor expansion and a uniform absolute
second-derivative bound. The lower excluded half-line and monotone upper
half-line are explicitly checked against the feasible upper value.

Stop at per-feature global-loss gap `<=1e-8`, floating slack `1e-12`, or 100,000
interval expansions. An unresolved gap or failed exclusion stops execution;
no tolerance/optimizer change is silently substituted. A zero column is solved
exactly as an optimal constant predictor. This is a finite-precision global-gap
diagnostic, not an outward-rounded exact-rational theorem.

## Raw archive

- `outcomes.csv`: every geometry/sigma, frozen and calibrated biases,
  per-feature/sum MSE, numerical global lower/upper bounds and status.
- Per geometry: supplied W, encoder energy and clean-optimal bias candidates.
- Per nonzero feature/sigma: excluded-region checks, initial feasible candidates,
  every generated interval, pruning/expansion actions, remaining intervals,
  stopping bias/gradient/loss and global-gap calculation.
- Exact zero-column results and all final arrays are retained.
- Settings, environment, original source/protocol/approval snapshots,
  gradient checks, timings and SHA-256 manifest.
- Failures, if present, are recorded without replacing them with a new run.

The independent root teacher verifies quadrature, tail bounds, gradients and
numerical comparison gaps separately. A surviving control alone does not
establish novelty, a full load phase diagram or real-model validity.

## Completed independent verification

`independent_review/results.json` records the passed review: 85 archived hashes
match; 36 direct Gaussian-quadrature feature-loss checks agree within
1.943e-16; the maximum omitted-tail bound is 3.913e-31. Curvature constants,
interval lower bounds, excluded half-lines and the final global gaps also pass.
The reviewer does not import the experiment's moment or calibration functions.

Reproduce that review using a fresh directory:

```sh
python independent_verify_calibration.py --output independent_review_reproduction
python plot_calibration_control.py --output my_calibration_plot.png
```

The plot reads only saved population-loss rows. It performs no additional
training or noise evaluation; connecting lines are display guides.

The senior verdict in `professor_decision.md` is to stop optional toy extensions
and specify one bounded real-model mechanism test. The current two-feature
result is reportable evidence, but a full load-dependent boundary and strong
publication distinctiveness remain unestablished.
