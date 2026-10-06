# One decisive decoder-calibration control for the Project 1 claim

Recorded 6 October 2026 before executing the control. This is a follow-up to
existing results, not a new frequency/geometry campaign. The evidence audit
is retrospective and is labeled separately.

## Question and connection to Project 1

The already globally proved clean optimum at p=1/2, equal importance, two
concepts/one code dimension and encoder energy one beats mono on clean
population reconstruction MSE. The saved noisy reconstruction MSE reverses
at sigma=.30 and .60. Does that SAME-OUTCOME reversal survive optimizing
the free decoder biases for each noisy distribution while freezing geometry?

This separates a geometric cost from a clean/noisy decoder-calibration
mismatch. A disappearing reversal weakens a claim of intrinsic geometric
fragility. A surviving reversal gives a stronger controlled result, but
does not by itself establish novelty or a complete load phase diagram.

## Smallest useful test

- One existing distribution only: independent b1,b2 Bernoulli(.5),
  importance [1,1], n=2,m=1, squared encoder norm one.
- Two shared geometries already known to be globally clean-optimal:
  squared norms a=(1+1/sqrt(2))/2, c=1-a, W=(sqrt(a),+/-sqrt(c)).
  Retain both relative signs; swapping equally important concepts has
  identical population risk. Mono retains concept 1 with W=(1,0);
  retaining concept 2 is symmetric, not a noise-selected baseline.
- No geometry optimization or new training. Evaluate the exact supplied
  optimum, distinguished from the original projected-Adam final iterates.
- Sigma=0 is the analytic clean anchor; only .30 and .60 are new
  bias-calibration controls, both previously tested corruption levels.
- Primary outcome remains summed population reconstruction MSE, with
  per-feature MSE. Detection is not substituted for reconstruction.
- Report clean-optimal biases and their corrupted MSE first; then allow
  EVERY geometry to calibrate its own free biases on the same noisy
  population. Label this oracle population calibration, not a practical
  finite-data transfer result. A linear/unrestricted decoder is not added.

## Global scalar calibration and implementation checks

Reuse existing exact Gaussian ReLU first/second moments. Each bias objective
is a four-state scalar mixture; scalar bounded local minimization alone
must not be claimed globally correct. Use branch-and-bound with the
analytical derivative and a uniform absolute second-derivative bound on
the finite interval. Keep best feasible upper values and lower bounds for
every remaining interval. Stop when the global loss gap is <=1e-8 per
feature, or after 100,000 interval expansions; report unresolved gaps.

The upper bias limit is 1-min(state offsets), above which every derivative
term is positive. For the excluded lower half-line use the lower bound
p-2*sum(P_b*b_i*E[ReLU(z_b+B+sZ)]) for beta<=B, by monotonicity of the
ReLU first moment and nonnegativity of its second moment. Choose
B=-max(offsets)-12*s-1. Check this excluded-region bound against a saved
feasible upper value; otherwise mark the calibration unresolved rather
than broaden the search. A zero column is optimized exactly as a constant.

Use a declared floating-point slack (1e-12) in interval risk lower bounds;
this is a numerical global-gap check, not an exact-rational theorem. Keep
the full branch ledger, interval count, final bias, boundary checks and
reported lower/upper gap. Independently check objective/gradient agreement
and integrate the calibrated risk directly with Gaussian quadrature plus
a tail bound. No unreported optimizers, changed stopping tolerance or
noise settings are permitted.

## Stop and decision

Stop after the three supplied geometries, clean anchor and two noise levels.
Preserve unfavorable outcomes and ambiguous global checks. A reversal is
supported only if its sign is separated from the summed numerical gaps
and independent integration discrepancy. Do not tune another frequency
or solver to recover a preferred sign. The senior reviewer's prior-source
comparison decides whether this evidence supports a distinct paper claim
or is only a sanity-check/known mechanism. No real-model pipeline launches
before that judgment and a prospective transfer protocol.

All new mathematical formulas/derivations for the calibration method must
be integrated into the existing derivation PDF and editable TeX source.
