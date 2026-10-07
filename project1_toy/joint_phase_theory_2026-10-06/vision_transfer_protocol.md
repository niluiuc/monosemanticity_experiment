# Fixed learned-vision pilot: decoder-policy risk ordering

6 October 2026. Prospective protocol saved before any extracted feature or noise outcomes. The root authorized one bounded isolated environment setup. This is a narrow mechanism-transfer pilot, not an assertion that ResNet channels are semantic concepts, a test of adversarial/image-input robustness, or a test of the Bernoulli critical exponent.

## Question, mechanism and smallest test

Does the weighted reconstruction-risk ordering between a clean-trained sharing code and coordinate-retaining mono depend on symmetric bias calibration when their two targets are genuine learned post-ReLU vision activations? The Project1 endpoint theorem motivates preserving ReLU-zero support and distinguishing encoder geometry from decoder calibration. Use exactly one frozen checkpoint, one feature pair and five prescribed code-noise levels. Do not scan for a favorable channel pair, importance, model or noise crossing.

## Genuine inputs and fixed split

- Official torchvision ResNet18 `IMAGENET1K_V1`, inference mode, official weights transforms; CIFAR10 training partition only. Official pretrained weights must actually load; no random initialization substitute.
- Shuffle the50000 CIFAR10 training indices once with NumPy `default_rng(20261006).permutation(50000)`. First256 are train, next256 calibration, next512 test. Save image indices, dataset/checkpoint hashes, transform specification, software versions and extracted arrays.
- Extract post-ReLU layer4 output at spatial index `(height//2,width//2)` **before average pooling**. One observation per image. This fixed central cell preserves possible ReLU-zero mass and avoids treating correlated spatial cells as independent images.
- Feature arrays have keys `train`, `calibration`, `test`, each shape `(N,512)`, plus image index arrays in the supplied NPZ. Select from train only the first two channel indices with positive empirical mean and variance. Do not select on coactivation, risk or crossing. Normalize each by its train RMS without centering; preserve raw arrays and factors.
- Weights are `(1,2/3)`; encoder squared energy1; scalar code; tied ReLU reconstruction with two free biases.

## Clean selection and eligibility before noisy comparisons

For continuous nonnegative targets, enumerate every scalar bias activation interval's quadratic stationary vertex and interval boundaries, including the all-off plateau. Minimize each feature exactly within this empirical piecewise-quadratic objective for any fixed encoder. Save all bias candidates at each final geometry.

Use angle grids256 then512 on `[0,pi)`, and exactly one bounded best-cell refinement at each resolution. Best cell is the interval of half-grid-step width about that resolution's best grid angle, with periodic geometry. No restarts or alternative cells. Save every grid candidate and refinement evaluation. Compare the two refined clean minima within absolute weighted MSE1e-6. This is a numerical stability check; it is not a global clean-optimum certificate.

Choose the better of the two coordinate-retaining mono orientations from train loss alone. Save both. Eligibility requires:

1. Both selected channels nonconstant with positive mean/RMS and nonnegative finite values; at least one selected channel has exact ReLU-zero observations in train. Save both zero fractions and coactivation frequency; zero support is mechanism context, not semantic validation.
2. Clean selection resolution agreement within1e-6; selected mixed solution improves on selected mono by more than1e-6; both squared column norms exceed1e-8. Report actual values. Failure means this fixed pair is non-diagnostic, not that generic policy dependence is disproved.
3. Genuine source metadata/hashes and adaptation correctness review exist.

Stop before noisy comparisons if any gate fails. Do not replace the channel pair, grid, checkpoint, weight or threshold.

## Matched policies and primary evaluation

Freeze train-selected encoders. For each model, fit its optimal zero-noise biases on the calibration split; these become the primary frozen biases. At each positive noise, calibrate both models' two biases on that same split, with encoders fixed. Thus the policies coincide at sigma0; train/calibration mismatch cannot create a baseline policy difference. Save clean-training biases and their test risks as secondary records.

Define the common absolute code-noise reference from normalized train targets as `sqrt((Var(x1)+Var(x2))/2)`, with population empirical variance (`ddof=0`). Absolute sigma values are this reference times `{0,.05,.1,.2,.4}`. Both models receive identical independent scalar Gaussian code noise. Use exact Gaussian conditional ReLU moment formulas averaged over the held-out512 test images; no sampled favorable corruption realization.

Continuous-target calibration uses actual target amplitudes, right endpoint `max(y)-min(offset)` and valid left moment-tail bounds. Scalar branch-and-bound uses conservative float arithmetic slack1e-12, weighted total calibration-objective gap1e-7 per model, at most20000 expansions per output, and a shared300second time budget for all calibration profiles. Retain all interval ledgers and unresolved flags. These numerical bounds are not directed-rounding proofs.

At each prescribed sigma report both policies' risks and their signed differences, the contrast `Delta_cal-Delta_frozen`, each model's bias-calibration improvement, per-image conditional losses, final biases and all calibration gaps. Test data never fit or choose anything. Fixed paired bootstrap:2000 image-index resamples with NumPy seed20261006, preserving paired model/policy losses. Save95% percentile intervals and bootstrap outputs. These quantify finite test-sample variability conditional on fitted models, not training/calibration uncertainty or population certificates.

## Bounded setup and stopping

- Isolated dependency setup outside workspace:5minutes total; download5minutes total; extraction10minutes total. Preserve errors; no retries beyond a deterministic initial setup attempt and no random-feature fallback.
- Downstream numerical limits are the fixed clean grids/refinements and300second shared calibration budget above. Do not retune risk thresholds, tolerance, maximum expansions or noise after seeing a failed/undesired comparison.
- A failed/no-zero/no-mixed/resolution gate is a stopped non-diagnostic pilot. A negative or unresolved policy ordering remains in the report. Finish and stop after the five sigma levels if eligible; no second pair/backbone or wider noise grid.
- A resolved policy contrast and opposite orderings would justify considering an identical independent reproduction. This two-channel pilot alone does not establish universal monosemanticity robustness or sufficient ICML main-track generality.

## Code and input contract

`vision_transfer.py` supplies continuous-target clean profiling, bounded clean selection, Gaussian moments, global-gap empirical bias calibration and fixed evaluation. `verify_vision_adaptation.py` checks one predetermined three-target adaptation case before real input execution. The root must provide the genuine feature NPZ and an independent implementation-review record before invoking real evaluation. No real feature/noise execution is authorized for the professor before that notification.
