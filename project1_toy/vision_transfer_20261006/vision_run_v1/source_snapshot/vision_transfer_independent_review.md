# Independent review: fixed continuous-activation vision pilot

6 October 2026. Reviewed `vision_transfer_protocol.md`, `vision_transfer.py`, `verify_vision_adaptation.py`, its archived `vision_adaptation_run_v1` results, and the separate frozen extractor `../vision_transfer_20261006/vision_extract.py`. No real feature/noise outcomes were executed or inspected in this review.

## Verdict

Approved for the single prescribed extraction and eligibility-gated pilot. The adaptation preserves the population code-noise mechanism with empirical nonnegative image-feature targets and a common weighted-MSE target. It is a narrow numerical mechanism check; neither semantic monosemanticity nor the Bernoulli critical exponent is inferred from ResNet channels. No pair/model/noise replacement is approved after a failed eligibility gate.

## Clean profiling and geometry selection

Sorting thresholds -offset groups all simultaneous ReLU activation changes. In each interval the included active observations have a scalar quadratic squared-error objective; its stationary vertex clipped to the interval and each kink closure, together with the all-off plateau, exhaust the global empirical scalar-bias minima. Recomputing every candidate directly avoids deciding on prefix-sum cancellation. The positive output importance scales the scalar loss without changing its bias minimizer.

Angles in [0,pi) cover all energy-one two-column scalar geometries modulo global encoder sign. Both sign sectors and both mono orientations are therefore represented. The two grids and one bounded best-cell refinement are a declared numerical resolution check, not a global geometry proof. The code keeps an incumbent if refinement fails or worsens the grid result, and its gate requires both refinement-success flags. No restarts or favorable cell substitution occur.

## Gaussian risk and continuous-target calibration

The Gaussian first/second ReLU moments and derivative 2*mean[(mu-y)Phi(mu/s)+s phi(mu/s)] apply to continuous nonnegative y, not just Bernoulli targets. The interval curvature envelope follows from f''=2*mean[Phi(mu/s)-y phi(mu/s)/s]; replacing |phi| by its maximum at the interval's nearest distance to zero is valid for nonnegative targets. The factor y is correctly included, unlike a binary-only bound.

For beta >= max(y)-min(offset), every mu is at least y, making every scalar derivative nonnegative, so the right exterior objective bound is valid. On the left, dropping the nonnegative second moment and using monotonicity of the first moment gives mean(y^2)-2*mean[y M1(offset+lo,s)] as a valid lower bound. Branch-and-bound retains both exterior bounds, every node and unresolved expansion/time flags. The scalar minimizer gives an incumbent only; its success is not asserted to prove globality.

The common feature gap target GAP/(1+2/3) yields a weighted total model gap at most GAP. The zero-noise calibration is profiled exactly in the empirical piecewise objective, including a zero column's prior-mean predictor. The finite floating slack is an engineering tolerance, not a rigorous interval-arithmetic certificate; the protocol states that limit. Large continuous amplitudes and cancellation must remain visible if a numerical check fails.

The predeclared adaptation record passes its exact clean solution, three direct Gaussian quadrature comparisons, finite-difference derivatives, and one noisy calibration ledger. Its maximum formula/quadrature discrepancy is 5.55e-17; its largest derivative discrepancy is 1.09e-10 and its resolved calibration gap is 3.37e-9. These are implementation checks for one case, not a universal numerical-error bound or a real vision result.

## Data, policies and uncertainty

The extractor loads actual official pretrained weights, frozen inference, official weight transforms, and post-ReLU layer4 central cells before averaging. It saves all 512 channels and deterministic train/calibration/test indices, acquisition hashes, source snapshot and runtime fields. Pair selection uses train mean and variance, not zero-support magnitude, coactivation, test risk or a crossing. Exact-zero support is a subsequent go/no-go check. The full feature NPZ supports independently repeating the channel rule.

Both policies start from the same zero-noise calibration-split biases. This avoids mistaking a train/calibration bias mismatch for a noise-dependent policy effect. At positive noise both decoders get the same free-bias calibration class and data. Encoders remain fixed; test targets do not fit or select any model. Conditional Gaussian test expectations remove sampled-corruption selection, while paired bootstrap intervals describe test-image variability conditional on the fitted models. They do not include training/calibration uncertainty or certify population signs.

## Operational stopping limits

The root must externally enforce acquisition/extraction wall time because a blocking network call cannot be interrupted by an internal clock checked between calls. A dependency/download/selection failure is retained. The shared calibration clock is checked inside expansion loops; finite incumbent initialization and later bookkeeping can cause a small wall-time overrun, so a strict external bound can be applied if required. Once the clock expires, later ledgers may be unresolved and cannot support a resolved-calibration claim. Stop after the five prescribed levels; no new settings or optimizer repair are justified by this review.

## Full derivation review

Subsequently reviewed `vision_calibration_derivation.tex` against the approved implementation. The complete empirical bias proof covers the all-off half-line, every grouped threshold, clipped interval vertices and the final half-line; it does not incorrectly assume global convexity. The Gaussian integration uses the correct truncated second moment Phi(z)-z*phi(z). Its differentiated risk, target-amplitude-dependent curvature envelope and both exterior bounds match the implementation. The Taylor interval bound plus feasible incumbent and exterior minimum establish the stated global empirical gap in exact arithmetic. The text explicitly separates this statement from the code's non-directed floating arithmetic and finite sample uncertainty. Proof completeness is approved for integration. These are necessary correctness derivations for the pilot, not a claim of a novel independent mathematical contribution or a Bernoulli exponent for continuous features.
