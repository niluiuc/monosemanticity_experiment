# Senior research decision: the next claim must survive the right controls

6 October 2026. This assessment uses frozen experimental records and the
independently reviewed proofs. No new experiment was run for this document.
This is a research judgment, distinct from an algebraic correctness review.
The targeted exact-claim prior comparison is recorded separately in
`exact_claim_comparison.md` and informs the decision below.

## Decision in plain language

The current work contains a defensible result, but it is not yet a
paper-ready general phase diagram. The strongest existing robustness
example is **not** the two crossings of thresholded rare-feature detection.
It is a globally clean-optimal shared representation that improves clean
reconstruction MSE and then loses on the **same reconstruction MSE** under
Gaussian corruption. That existing dense, equal-importance example is the
appropriate anchor for the next decision. It avoids confusing training
MSE with a downstream threshold chosen for detection.

Stop new special-case mathematics. Perform one small, symmetric decoder
calibration control at this existing case, alongside the exact-claim prior
comparison. Those two answers decide the manuscript claim and whether a
single real-model transfer is warranted. They do not require changing
Project 1 or adding Project 2.

## What the existing evidence really says

### The rare-feature two-crossing example is legitimate but decoder-specific

At p=.05 and importance (1,.5), the certified code has lower clean MSE
than mono but worse clean thresholded detection. The intermediate detection
advantage and eventual disadvantage are correctly proved for its specified
decoder. They are not evidence that the training outcome itself has a
two-crossing phase. Both the low-frequency false-negative behavior and
mono's exactly dropped column enter the phenomenon. The centered-midpoint
diagnostic changes its comparison substantially.

All four certified shared geometries in the fixed-importance frequency
validation have lower reconstruction MSE than the clean-selected mono
control at every positive primary sigma. A different mono retention choice
can beat some of them at high noise. These facts must remain visible.
Calling the detection window an intrinsic, decoder-independent property
of monosemanticity would be unsupported.

### A stronger same-outcome reversal already exists

The focused-bridge archive contains p=1/2, importance (1,1), energy one.
The clean optimum is globally established over all energy-one rank-one
encoders and free ReLU biases, not just a finite grid:

    a*=(1+1/sqrt(2))/2, c*=(1-1/sqrt(2))/2,
    L*=(9+2*sqrt(2))/48=0.246425565098879...

The saved row happens to assign the stronger norm to concept 2:
W=(0.38268343236508984,-0.9238795325112867), with biases
(0.6035533905932737,0.21548220313557545). It matches that theorem.
Either mono orientation has clean MSE .25 and the same noisy MSE.

| Gaussian code sigma | Globally clean-selected shared code MSE | Mono MSE | Shared minus mono |
|---|---:|---:|---:|
| 0 | .246425565099 | .250000000000 | -.003574434901 |
| .05 | .248392207291 | .251875000000 | -.003482792709 |
| .15 | .264393833165 | .266874999999 | -.002481166835 |
| .30 | .318682818682 | .317463880602 | +.001218938080 |
| .60 | .512993808968 | .505449771089 | +.007544037878 |

These are archived floating-point evaluations of exact conditional
Gaussian moment formulas, independently checked previously. They are not
new measurements or certified exact sign intervals. The effects are
modest: the clean improvement is about 1.43% relative to mono; the .30
disadvantage is about .38%; the .60 disadvantage about 1.49%.

The equal-importance sign/order degeneracy does not invalidate this anchor.
At p=.5, complementing the other independent fair bit transforms the
same-sign conditional offsets into the opposite-sign offsets for each
feature; Gaussian noise is symmetric and output-noise magnitudes agree.
Thus all the proved equivalent clean optima have the same marginal MSE
profiles up to exchanging features. The saved grid label alone was not
the source of globality.

Evidence sources:

- `../focused_bridge_2026-10-06/toy/run_v1/geometry.csv`
- `../focused_bridge_2026-10-06/toy/run_v1/risks.csv`
- `../focused_bridge_2026-10-06/math/student_derivation.md`, dense global theorem
- `../focused_bridge_2026-10-06/math/teacher_review.md`
- `../focused_bridge_2026-10-06/review/toy_teacher_review.md`
- `../frequency_boundary_2026-10-06/toy/run_v1/primary_risks.csv`

### What remains a possible artifact or restriction

The dense MSE reversal cannot be caused by the arbitrary binary detection
threshold: no threshold is used in MSE. Equal importance also removes
the choice between differently weighted mono orientations. Both classes
have the same latent width, tied architecture and exact encoder energy.

However, this is still a **clean-trained geometry-and-decoder comparison**.
The clean biases are frozen under corruption. Different sensitivity to
bias mismatch may explain some or all of the noisy reversal. That is a
legitimate deployment effect, but a stronger representation-level claim
needs a symmetric calibration control. Neither current record nor proof
settles that control.

The mono control drops one concept and estimates its prior by a constant;
coverage loss is included in total reconstruction MSE. Its immunity on
the dropped output is a consequence of the model, not cheating, provided
the same outcome and full feature accounting are kept. The exact energy
equality is a declared constraint, not a proof about every architecture
whose energy is bounded above. At large noise an unconstrained constant
prior predictor can be preferable; current comparisons do not prove
noise-optimality across all predictors.

## Strongest defensible manuscript claim now

> In an explicitly resource-matched nonlinear compressed representation,
> the clean population objective selects a shared feature geometry whose
> reconstruction advantage can reverse under corruption. A separate
> globally solved frequency slice predicts when storage switches from
> sharing to important-feature retention. The learned geometry, decoder,
> coverage and corruption must all be specified to interpret robustness.

The global selection result makes this stronger than comparing arbitrary
supplied codes. The full frequency proof is substantial within its scope.
The calculation does not yet locate a general robustness surface across
load and importance decay. The qualitative clean/noisy reversal is already
present in the motivating literature, so globality plus new constants in
a two-feature model alone should not be assumed enough for main-track
novelty. Mathematical infrastructure and a potential contribution must be
distinguished. A targeted prior comparison and one meaningful real-model
mechanism test are still required for a strong submission claim.

## One minimal decisive next experiment

**Question:** does the dense same-MSE noisy reversal survive when both
fixed representations receive equally allowed noise-aware bias calibration?

**Connection:** Project 1 asks whether the geometry selected by clean
training creates a robustness cost. If a fair bias adjustment removes the
observed reversal, the present cost cannot be advertised as intrinsic to
the shared geometry. If it survives, it is a stronger representation-and-
decoder-class comparison worth carrying into one real model.

**Use only this existing case:** p=.5, importance (1,1), n=2, m=1,
energy one, both relative-sign variants of the proved shared W*, and mono
W=(1,0). Do not search for a new favorable encoder. Keep the exact
four-state distribution and Gaussian code corruption. Calibrate only at
the already tested sigmas .30,.60; retain the saved zero-noise anchor.
The .15 row remains archival context, not a new calibration setting.
Both mono orientations are equivalent here. Including both shared signs
numerically checks the relevant clean-minimizer degeneracy instead of
selecting one favorable representative.

**Primary outcome:** the same total continuous reconstruction MSE, never
thresholded classification accuracy. Record per-feature MSE as well.
For each fixed geometry and sigma, minimize over its two bias coordinates
separately in the same tied-ReLU decoder class using the existing exact
Gaussian moment function. Keep the original frozen clean biases as the
baseline arm. This is one calibration control, not a new training campaign.

The authoritative pre-run settings are now saved in
`calibration_protocol.md`. Its branch-and-bound procedure improves on a
bounded local optimizer by maintaining a numerical lower/upper global-gap
check. Stop at per-feature gap 1e-8 or 100,000 interval expansions; failures
remain unresolved. No new theorem is necessary to begin this diagnostic.

Preserve every bias, objective value, failure and comparison. Noise-aware
calibration is explicitly a different deployment protocol; it must not
overwrite the frozen-decoder result.

**Time budget:** one working session, at most two hours for implementation,
execution and independent review. This is a wall-clock work cap, not a
fabricated runtime estimate. The exact expected-risk computations are
small; difficult global proofs or additional axes are outside the cap.

## Go/no-go decisions

- **GO toward one transfer pilot** if the exact-claim prior comparison
  identifies a substantive distinction and the same-MSE reversal survives
  the symmetric calibration diagnostic at the prespecified .30 or .60
  setting. Then preregister one real-model test of the same mechanism,
  with a fixed outcome, resource/coverage controls and falsification rule.
  The teacher and postdoc must select its concrete implementation together;
  this document does not authorize a diffusion pipeline without a protocol.
- **NARROW the claim** if calibration removes the reversal. Retain the
  valid clean allocation theorem and frozen-decoder deployment result;
  state that recalibration changes the comparison. Do not launch multiple
  models hoping to recover a desired sign. Decide within the same working
  day whether the decoder-sensitive mechanism has a distinct, useful real
  setting; otherwise stop presenting it as the paper's central robustness
  contribution.
- **NO-GO for a current main-track claim** if the exact result is already
  covered or is merely a routine special case with no nonroutine explanatory
  advance. A large-model demonstration cannot repair that deficit. The
  original direction remains available, but any next extension needs one
  central unresolved question and a bounded protocol rather than another
  collection of special cases.

No branch of this decision promises ICML acceptance or spotlight. At this
stage the work has verified theory and real research evidence; it does not
yet have a justified acceptance prediction. The practical priority is a
decisive claim, not a larger pile of proofs.

## Senior-team verdict and implementation approval

The numerical postdoc's `evidence_audit.md` identifies the dense anchor,
checks the global theorem and spells out the symmetry. The teacher
independently read the saved geometry and MSE rows. The math postdoc's
`exact_claim_comparison.md` finds direct prior clean geometry phases and
clean-trained corrupted-performance reversals. Elhage's article and
McGrath's primary comments already go beyond merely supplied geometries;
Zhang's larger trained toy already exhibits the qualitative reversal.
The exact norm-one/free-bias theorem was not found in the inspected primary
sources, but this is a narrow analytical extension, not a verified new
mechanism or an established main-track contribution. This limits the GO
decision: survival of calibration is useful evidence, not publication
readiness by itself.

**Calibration implementation approved before execution.** For each feature
and each conditional Gaussian mean mu=z+beta and standard deviation s>0,
the exact first derivative is

    f'(beta)=2 sum P [(mu-y) Phi(mu/s)+s phi(mu/s)].

Differentiating gives

    f''(beta)=2 sum P [Phi(mu/s)-(y/s) phi(mu/s)].

Thus the protocol's bound H=2*(1+1/(s*sqrt(2*pi))) is valid globally,
and midpoint Taylor bounds give

    f(beta)>=f(m)-abs(f'(m))*h-H*h*h/2

on an interval of center m and radius h. The upper excluded half-line is
safe: beta>=1-min(z) gives mu>=1>=y, so all derivative terms are positive.
On beta<=B, expanding MSE as p-2*sum(P*y*M1)+sum(P*M2), using M2>=0
and monotonicity of M1, gives the stated lower excluded-region bound.
The finite B and upper limits are fixed by the saved protocol; their
acceptance against a feasible upper bound must be checked, not assumed.
The zero-column bias is solved exactly as a constant.

The 1e-12 numerical slack does not turn floating-point evaluations into
outward-rounded exact certificates. The result is explicitly a numerical
global-gap diagnostic with independent gradient and Gaussian quadrature
checks. A comparison sign must exceed all summed gaps and numerical
discrepancies. A failed exclusion or exhausted interval budget is an
unresolved control; it does not authorize extra settings or tolerances.

No additional experiment is necessary for this decision. There is a useful
analytical context control already identified by the numerical postdoc:
with ReLU removed and a mean-correcting bias, every energy-one rank-one
code in this dense case has linear MSE 1/4+sigma^2, because G^2=G,
Cov(b)=I/4 and tr(G)=1. The nonlinear gating is therefore necessary to
break the linear tie. This is context, not proof that gating alone uniquely
explains the full nonlinear ordering. Any new calculus explanation belongs
in the existing companion PDF, as the user requested.

No calibrated noisy-bias result exists in the archive at the time of this
approval, so whether the reversal survives remains unknown.
