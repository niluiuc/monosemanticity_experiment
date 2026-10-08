# Project 1: current paper claims and the remaining gap

## The question has not changed

When does storing more predictive features through sharing improve clean performance, and when does monosemantic storage become preferable under corruption? How does the boundary depend on representation geometry and the decoder's calibration policy?

The intended paper remains mathematics, controlled toy validation, and a genuine real-model test. It is not a benchmark, agent project, symbolic-regression exercise, or claim that monosemanticity improves every robustness measure.

## What can be written as results now

1. **Restricted mathematical phase boundary.** The existing reviewed two-feature scalar tied-ReLU family has an exact clean storage transition in its stated parameter rectangle and a derived noise crossing with critical scale proportional to epsilon^(3/2), for the specified fixed-clean encoder and decoder policies. Full hypotheses, constants and proofs are in the existing derivation volume. These are reconstruction-risk results with code-space corruption, not general classification theorems for deep networks.
2. **Controlled numerical validation.** Existing saved toy checks test those predictions in the corresponding regimes. Claims about correlation, training-noise selection and shared resource budgets have mixed proof/leading-order/numerical status; keep those labels. Do not upgrade all Claude extensions to global theorems.
3. **Actual native ordering reversal.** Released CL/NCL CIFAR-100 ResNet-18s with their native projectors and clean probes reverse ordering between clean and intermediate Gaussian pixel corruption. NCL's advantage at .12 and .20 is resolved for the original probe. The observed curve returns to a small CL advantage near chance at .30; a permanent unique phase boundary is not established.
4. **Limited probe reliability.** Two additional clean probe seeds reproduce the clean versus .12 reversal. This is a post-outcome check on the same pretrained networks and images, not independent backbone replication.
5. **Measurement qualification.** A single rank-prevalence control retains a smaller NCL class-purity contrast. Many NCL cutoff ties are zero, so this is not exact matching of positive firing rates. Class purity is not ground-truth monosemanticity or an intervention isolating its causal effect.
6. **Explicit negative result.** The prospective local-affine native predictor fails. Allowing only projector gates to switch also fails. Saved residual analysis shows substantial image-dependent coherent shifts, with smaller global class-only shifts. These facts identify the failure of one proposed bridge; they are not a successful boundary law.

## What cannot be written

- The toy critical exponent or numerical crossing predicts the real network's Gaussian input-noise boundary.
- A class-consistency difference proves that monosemanticity caused the native reversal.
- The predecessor's released checkpoints exactly reproduce the anchor's own larger-projector experiments.
- Three probe seeds are three independently trained representation models.
- An observed interpolation near .078 is a successfully forecast crossing or an uncertainty interval.
- This work is guaranteed ICML main track, spotlight, or novel merely because this checkpoint pair exhibits a reversal. The anchor already reports robustness improvements and related clean/robustness tradeoffs.

## The specific paper-critical gap

The native phenomenon now exists in the saved data. The remaining scientific bridge is a finite-noise mechanism that links measured representation properties to the ordering boundary and survives prospective evaluation, rather than treating local input derivatives or a Gram matrix as sufficient for the whole CNN.

Do not expand the project into optional toy special cases or unrelated modalities to hide this gap. Any next proposed mechanism must specify what it predicts before its new evaluation, what measured native property motivates it, the smallest useful test and a stopping criterion. A calibrated noise-risk curve computed from every test outcome is not a new predictive law.

## Reviewable paper structure using supported claims

- Motivation: the clean capacity/robustness tradeoff, and the anchor's empirical monosemanticity result.
- Formal setup and restricted phase theorem, including decoder policy.
- Controlled toy checks of the theorem, with extensions separated by proof status.
- Native CL/NCL experiment, full failed prediction and source-justified representation correction disclosed.
- Probe reliability and measurement sensitivity, with post-outcome status and limitations.
- Discussion: qualitative native reversal versus unestablished quantitative transfer; the remaining predictive mechanism must not be presented as achieved.

This is a concrete research record and a potential draft structure. It is not an assertion that the current package already meets the main-track novelty/evidence bar.
