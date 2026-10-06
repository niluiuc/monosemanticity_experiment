# Senior review: calibrated reconstruction comparison

6 October 2026. Reviewed the pre-run protocol, frozen
`run_v1/source_snapshot/run_calibration_control.py`, settings, raw outcome
table, per-feature boundary/results and interval ledgers, derivative checks,
and `calibration_section.tex`. No new scientific experiment was executed
for this review. The root's separate quadrature record is
`independent_review/results.json`.

## Verdict

**Approved as a bounded numerical control and mathematical exposition.**
The calibration control materially strengthens the research result:
globally clean-selected sharing still loses on the SAME reconstruction
outcome after both geometries receive oracle noisy-bias calibration.
This is not a binary-threshold scoring effect or a frozen-bias mismatch
alone. It remains a fixed-geometry comparison within the tied-ReLU decoder
class, not an assertion about every possible readout or robust optimum.

## Implementation and saved evidence

- Only the three prescribed geometries and sigma 0/.30/.60 were executed.
  Both relative-sign shared codes use the proven dense global norms.
  Mono's omitted feature remains in the loss with its optimal constant.
- All 85 archived hashes match. All 12 feature results resolve, including
  two exactly constant dropped-feature solutions. Numerical scalar gaps
  satisfy the per-feature 1e-8 criterion; intervals require 47--58 expansions.
- The numerical queue and parent/child ledgers retain interval coverage;
  pruning uses feasible upper values and global curvature lower bounds.
  A local bounded minimizer supplies only a feasible incumbent, not the
  proof of numerical globality. Excluded-region bounds pass for all cases.
- Gradient finite differences agree within 1e-10. The root independently
  verified risk formulas and all interval/boundary calculations, and 36
  frozen/calibrated per-feature Gaussian quadratures agree within 1.95e-16,
  with omitted-tail bound below 3.92e-31.
- Summed numerical comparison brackets are [.0054250912846,.0054251096957]
  at sigma .30 and [.0240419131602,.0240419366371] at .60, well separated
  from zero. Both relative-sign variants agree as predicted.
- Floating slack and ordinary floating-point arithmetic are explicitly
  declared. The numerical global-gap checks are not relabeled exact
  interval proofs. No raw result was changed for this review.

## Source derivation checks

The Gaussian first/second moment integrals and their derivatives are
correct. The scalar objective includes inactive/rectified outcomes and
the complete four-state probability measure. Calibration separates by
feature despite correlated output noises because the loss is additive.

The displayed second derivative can be negative, and the conservative
absolute curvature bound is valid globally. Taylor's lower quadratic
over a midpoint interval has its minimum at an endpoint; the displayed
absolute-gradient/radius formula follows. The large positive bias tail
has positive derivative. The negative tail lower bound uses monotone
first moments and nonnegative second moments; its exclusion is checked
against an attained upper value rather than assumed from a cutoff.
The zero-column constant calculation is exact.

The bit-complement transformations preserve each marginal target/population
and translate its bias by r. They need not be one joint state relabeling:
the summed risk uses marginal losses. Thus both sign classes' clean and
calibrated profiles agree, without assuming joint output independence.

Every table entry matches the frozen outcome table. The text correctly
explains that two feature gaps can sum to more than 1e-8, and limits the
conclusion to oracle bias recalibration at two previously selected noise
values. No main-track novelty or acceptance is claimed.

## Delivery and research decision

No mathematical correction is required. The root handles typeset table
fit and integration/cross-references in the existing companion PDF.
Adding the completed independent verification metrics and the existing
short linear-tie context is useful exposition, not another experiment.
If the linear control is included, its interpretation must be that ReLU
gating is necessary to break the dense linear tie; it does not prove
that gating uniquely explains every nonlinear difference.

The final research decision is in `professor_decision.md`: stop optional
toy elaboration and preregister one bounded real-model mechanism test.
The prior literature already establishes the qualitative clean/noisy
tradeoff. The contribution being developed is the resource-controlled
global selection link and corruption cost surviving this readout control,
with predictive transfer still required for a strong manuscript.
