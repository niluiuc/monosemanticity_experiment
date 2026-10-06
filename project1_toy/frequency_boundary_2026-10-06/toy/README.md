# Finite verification of the frequency-dependent storage transition

This is a bounded Project 1 verification using the existing two-feature,
one-dimensional tied-ReLU population model. The authoritative pre-run documents
are `../protocol.md` and `../verification_protocol.md`.

The question is whether the exact clean-storage selections at five fixed
frequencies support the reviewed mathematical prediction
`pc=(3-sqrt(5))/2`, and how those selected codes compare with mono under the
existing Gaussian code-noise detector. Storage selection, continuous
reconstruction error and thresholded feature detection remain different claims.

## Approval gate and fixed settings

No cases are to be executed before the root independent teacher approves the
frequency theorem. The runner requires an existing saved mathematical review
file. This is an execution gate, not a substitute for reading that review.

- Frequencies: exactly `1/20, 1/5, 7/20, 3/8, 2/5`.
- Independent Bernoulli bits; importance `[1,1/2]`; encoder squared norm one.
- Tied decoder `ReLU(W^T W b+bias)`, freely optimized clean biases.
- Below the transition: exact rational active-branch/root comparisons must
  supply a strictly separated global sharing optimum. Unresolved intervals
  cause a stop, without extra frequencies or automatic refinement.
- Above the transition: the independently reviewed mono theorem supplies
  `W=(1,0), bias=(0,p)`. No new branch search is asserted for that case.
- Both mono retention controls remain in the output. Retaining concept 0 is
  the primary comparator because it minimizes clean weighted reconstruction.
- Primary code-noise standard deviations: `0,.05,.15,.30,.60`.
- Both actual-decoder and centered-midpoint detection are retained, with all
  per-feature errors, conditional false positives/negatives and decoder MSE.
- No training, new encoder class, load scan or optimizer campaign is performed.

## Certificate implementation and scope

`certificate_backend_snapshot.py` is the unmodified backend from the reviewed
low-p certificate. The wrapper assigns its population probabilities exactly as
`((1-p)^2,p(1-p),p(1-p),p^2)` for each prescribed rational frequency, and computes
mono endpoint objectives from that same p. Its old single-case `main()` is never
called.

Geometry is parameterized by `W=(1,t)/sqrt(1+t^2)` up to global sign. Four
sign/order regions, separated by `t=-1,0,1`, enumerate each feature's decoder
bias kinks and feasible interval stationary candidates. The first kink includes
the all-off constant plateau. Every joint branch contributes stationary and
feasibility-boundary roots; signs are checked with exact polynomial arithmetic
and rational isolating intervals. All branches, rejected/accepted root checks,
feasible value bounds and overlaps are saved. `t=0` and both infinite chart
endpoints are explicitly retained; the infinity code retains concept 1.

A strict interval separation is a computer-assisted global certificate for
that fixed frequency. It is not a numerical-grid global-optimality claim.
The five discrete geometry points do not establish the full continuous family
by themselves; the frequency theorem must come from the separate mathematics.

Algebraic geometry/bias formulas are converted to float64 for noise evaluation.
The Gaussian CDF formulas are analytical, but their numerical values are not
exact-sign certificates. Zero-noise decisions use strict inequalities; no
favorable detector or geometry is selected after seeing noise outcomes.

## Display-only evaluations and crossing checks

The actual-decoder risk-difference plot evaluates each of the five selected
encoders on exactly 240 logarithmically spaced positive sigma values from .001
through 4. This is visualization of an existing formula, not selection of new
geometries. Every plotted value is saved. The difference is selected-code error
minus the mono-retaining-0 error; negative values favor the selected code.

An adjacent display pair with opposite signs and both magnitudes above `1e-12`
permits one Brent calculation in that bracket. Its root, residual, bracket and
iteration count are retained. These are numerical crossings only. No claim is
made that all roots were found, that there are no roots outside the interval, or
that near-zero signs are reliable.

## Reproduce in a fresh output directory

From this toy directory, after reading the independent approval:

```powershell
& 'C:/Users/indra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' run_frequency_verification.py --math-review ../math/teacher_review.md --output run_reproduction
```

The saved independent approval is `../math/teacher_review.md`. Python requires NumPy,
SciPy, SymPy and Matplotlib, already available in the bundled environment.
The output directory must be fresh: overwriting is refused. Settings,
environment, source snapshots, both protocols and the approval file are written
before any cases. `--help` performs no scientific calculations.

## Outputs and stopping rule

- Per-frequency full branch, root-feasibility and candidate interval records;
  explicit chart endpoints; selected weights/biases and certificate summary.
- `geometry.csv`: every selected code and both controls, norm allocation,
  interference, alignment and clean reconstruction error.
- `primary_risks.csv`: all fixed settings, both detectors, per-feature FP/FN,
  weighted/unweighted sum errors and continuous decoder MSE.
- `display_risk_curves.csv` and `display_crossings.json`: every plotted point
  and narrowly prescribed numerical crossing check.
- `storage_transition.png`: five certified discrete geometry/loss points and
  the separately proved frequency boundary; no connecting geometry curve.
- `actual_risk_difference.png`: display-only noise curves and primary points.
- Frozen sources/settings/protocols/review, environment, timings and SHA-256
  manifest. Failures are saved and not replaced with a wider experiment.

Stop after these five cases and independent review. The result remains a fixed
load/importance theorem and toy validation; it does not establish variable-load
generalization, publication novelty or real-model transfer.
