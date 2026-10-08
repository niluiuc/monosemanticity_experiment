# Prospective continuation: one controlled learned-image phase check

This is an executable proposal, not a completed experiment. Root selected this fixture before training. AI theory and empirical reviewers must approve the coupling prediction and implementation before execution.

## Question and declared scope

Can a small image model recover two known independent visual factors accurately enough that the existing clean sharing advantage and calibrated noisy mono advantage remain predictable after learned perception is inserted before the compression model?

This tests perception error propagation into the declared reconstruction mechanism. It is controlled/semi-synthetic vision validation, not evidence that native ResNet features have independent binary semantics or the critical 3/2 law. The image encoder must actually infer factors from pixels, and its continuous soft outputs must actually drive the compression code. Replacing them with known binary labels or thresholding would make this a disguised repetition of the toy model and is forbidden.

## Fixed fixture and prediction

Use independent fair binary factors, p=.5, equal importance eta=1, scalar energy-one tied-ReLU compressor, and calibrated Gaussian code noise at sigma=0 and .30 only. Existing archived population results give an ideal clean sharing-minus-mono difference -.0035744349 and calibrated .30 difference +.0054251027 at the clean-optimal ideal sharing geometry. These reference values justify the fixture; they are not automatically predictions for new learned fitted parameters.

The actual train-fitted compressor and calibration biases must be frozen. Their exact four-state reference risks and theory-review-approved perception-error intervals must be recorded BEFORE held-out image inference. Prediction requires a strictly negative clean difference interval and strictly positive .30 interval, accounting for numerical calibration/optimization error. If these sign gates fail, stop with an unsuitable learned-model result; do not change noise, fixture, encoder, classes, nuisance, or interpretation.

The critical epsilon=.01 fixture was rejected prospectively because its cubic gaps are about 1e-7, requiring unrealistically stringent perception-error guarantees for a bounded CNN run. The dense fixture tests a finite mono/share boundary, not the critical exponent. This choice is made before model outcomes and is not a post-failure fallback.

## Images and genuine nuisance variation

- Reuse cached CIFAR10 training pixels ONLY as backgrounds; original class labels are irrelevant and never used. No dataset acquisition or benchmark is created.
- One seeded permutation selects disjoint background IDs: 256 train, 64 calibration, 256 test. For every background, render all four factor states with equal weight. Thus binary state weights are exactly .25 and nuisance does not induce factor covariance.
- Convert each background to grayscale RGB and map intensities to [.05,.25]. Independently fix left-disk and right-bar positions within +/-2 pixels, and their intensities in [.75,.95], using split-specific generators. The same nuisance realization is shared across a background's four states, so the planted factors remain independent of nuisance.
- Factor1 is a radius3 disk near pixel(8,16); factor2 is a width5/height7 bar near(24,16). Overlays are visible but the encoder receives only image pixels, not coordinates or labels.
- Save exact rendered float32 train/calibration images, labels, nuisance and background IDs. Test images and outputs are constructed only after the prospective prediction is saved. Holdout uses new background images and new nuisance realizations, not four memorized prototypes.

## One fixed image model and training budget

- CPU runtime already installed for vision, four threads, one initialization/shuffle seed20261008.
- CNN: Conv(3,8,k5,stride2,pad2), ReLU, Conv(8,16,k3,stride2,pad1), ReLU, flatten, Linear(1024,32), ReLU, Linear(32,2).
- Adam learning rate .005, BCE-with-logits supervision on the two planted factors, batch128, maximum80 epochs and180 training seconds; no hyperparameter search, restarts, best-validation checkpoint or noise training. Train/calibration/test background IDs remain disjoint.
- Retain complete training losses, final checkpoint, source/config hashes and failure/timeout logs. A time-exhausted model is archived as incomplete and cannot be silently treated as converged.
- Compute soft factor values by applying sigmoid in float64 to saved logits. No hard threshold, snapping to zero/one, post-hoc temperature, image exclusion or replacement factor.
- Train/calibration factor-recovery RMS error must each be <=5e-4 before proceeding to the risk protocol. This is the theory-review-approved prospective quality gate, finalized before any training; passing does not guarantee held-out recovery. A failed gate stops this single model, retaining its actual errors. No repair is authorized.

## Compression, calibration and prediction discipline

Fit clean scalar reconstruction from learned soft scores r(image) to true planted labels X using existing clean bias-profile and angle-grid infrastructure. Use the first64 preselected TRAIN background quartets only (256 examples) for this compressor fit, because the existing continuous profiler scans every interval and its direct checks are quadratic in sample count. This subset is fixed before training and retains exactly equal four-state weights. The image encoder itself uses all1024 training images. Include both coordinate-retention orientations and count omitted-coordinate reconstruction loss. Adapt offsets versus targets explicitly: encoding uses r; scoring uses X. Do not call an old routine that encodes and scores the same array unchanged. The compressor's quality/near-optimality calculation must use recovery on its actual fixed subset.

Use the same angular resolutions256/512 and one local refinement per resolution. Preserve disagreement and optimizer failures. The theory reviewer must qualify empirical near-optimality via perception error relative to the proved ideal global optimum; grid agreement alone is not a global proof.

Fit each model's biases fairly on the calibration images at each of the two fixed noise levels, with the established numerical gap rules. Encoders remain clean-trained and fixed. The noiseless comparator is calibrated by the same rule. The mathematical coupling guarantee applies to the fixed labels and the actual parameter values, not a substituted ideal encoder.

Save a prospective JSON containing all actual parameters, reference four-state risks, the predeclared held-out recovery budget5e-4, calibration/solver errors, and the complete signed prediction intervals. Require both prescribed signs before evaluating held-out images. Never select parameters by test risk or gate.

## Held-out measurement, failures and stop

After a signed prediction passes review, infer the untouched 1,024 held-out images exactly once. Record actual soft-recovery error and every image's conditional Gaussian reconstruction loss. If test recovery exceeds5e-4, report the prediction's applicability failure rather than relaxing its bound. Preserve risk outputs regardless; a sign match outside the guaranteed interval is numerical coincidence, not verified coupling transfer.

Finite held-out weighted risk includes all images/states. Bootstrap, if required, resamples background groups with their four paired states, not images as if independent. Population extrapolation beyond this generated nuisance distribution is not claimed. The primary conclusion is whether the predetermined signed risk intervals contain the observed differences at the two fixed noise levels and establish opposite orderings.

Falsification/failure: training budget exhaustion; recovery gate failure; unresolved clean selection/calibration; reference signs absent; held-out recovery exceeding budget; or measured risks outside valid prediction bounds. Archive all failures without changing the design. Stop after this one image model/fixture/two noise values. Successful outcome demonstrates a controlled learned-perception finite phase comparison, not native semantic critical-law transfer or guaranteed venue novelty.
