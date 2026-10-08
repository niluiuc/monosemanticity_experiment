# Native CIFAR-100 phase-boundary test — v1

Frozen before feature extraction or image scoring, 8 October 2026.

Pre-outcome amendment, 8 October 2026: if clean prerequisites pass, evaluate the already-fixed native TEST error curve even when the affine predictor fails its applicability or precision gates. Such failure rejects the predictive claim; it does not suppress the separate test of whether native corruption reverses the clean advantage. This amendment is made while the job is waiting for the prefetched archive, before any image scoring. No models, data splits, probes, corruption levels, test sample sizes or success thresholds are changed. Preserve the original protocol and the amendment timestamp/hash. A failed clean prerequisite still stops this checkpoint pair.

## Question and relation to Project 1

Does the less class-consistent CL representation have a clean classification advantage that reverses under Gaussian input noise relative to NCL? Can a validation-only decision-margin model predict the crossing? This tests the actual frozen network and its task head. It is not reconstruction by an added two-feature compressor, a causal isolation of monosemanticity, or a test of the toy's 3/2 exponent.

Use only the two official CIFAR100 checkpoints listed in the checkpoint inventory. They are predecessor releases, not proven identical to the anchor paper's numerical-table runs. Backbone and projector parameters stay frozen. Both use ResNet18, conv1 3x3/stride1/padding2, no maxpool, and the actual trained 2048-hidden/256-output projector; CL uses its signed output and NCL uses ReLU of its output. Strict checkpoint loading is required. The classifier and consistency calculation both use this same 256-dimensional representation. This is a separate experiment motivated by the anchor code, not a successful continuation of the failed backbone test.

## Fixed clean stage

- CIFAR100 standard training set: seeded stratified 450/class FIT (45,000) and 50/class VALIDATION (5,000), seed 20261008. TEST is the official 10,000-image test set and is not loaded in this stage.
- Deterministic clean images, no augmentation. ToTensor followed by the official normalization: mean (.4914,.4822,.4465), standard deviation (.247,.243,.261).
- Backbone feature standardization uses FIT mean/std only (std floor 1e-6).
- Fit one 100-class linear probe per model using standardized frozen features: 50 epochs, AdamW lr .01, weight decay 1e-4, batch size 1024, cosine lr schedule, seed 20261008. Identical procedure; no validation tuning, early stopping, hyperparameter or head search. This is our clean probing protocol, not an exact reproduction of the authors' probe training.
- Measure classification error on VALIDATION. Measure class consistency on L2-normalized 256-dimensional projected features: per active dimension, majority-class fraction among examples with absolute normalized activation >1e-5, then mean over nondead dimensions. Report sparsity at raw absolute activation <.01 separately.
- 2,000 paired class-stratified image bootstraps for clean-error difference; 200 for consistency difference. Fixed fitted models, conditional image uncertainty only; no training-seed inference. Report ordinary 95% intervals for both gates; requiring both is an intersection decision, not claiming simultaneous coverage of arbitrary other analyses.
- PASS only if the lower interval endpoint for NCL consistency minus CL consistency is positive, and the lower endpoint for NCL error minus CL error is positive. Otherwise STOP this fixed checkpoint pair and retain all outputs. No further representation substitution after failure of this source-specified follow-up.

## Conditional prediction stage

Run only if clean gates pass. Select the first five VALIDATION images per class in the seeded split order (500 total), before examining their predictions.

For each frozen classifier, compute clean logits and first-order directional derivatives for 32 predetermined independent standard-Gaussian raw-pixel directions per image. Predict classification error by applying these affine logit perturbations on the fixed sigma grid below. Use every class in the argmax; do not replace multiclass error by a squared-logit statistic or one chosen competitor. This is a local linearization hypothesis, not the previous reconstruction law and not a new novelty claim by itself.

On the same validation images, evaluate the actual network at sigma .01 and .04 with those directions. A linearization applicability gate requires each model's absolute mean error-prediction discrepancy <=.02 at both levels, and relative RMS logit-linearization residual <=.25 at .04. Failure stops a test-set crossing-prediction claim. Save actual residuals and failures.

The predicted difference curve uses the full 5,000-image clean validation gap plus the 500-image estimated noise increments. This adjustment is fixed in advance. Find the first positive-to-negative grid crossing; interpolate linearly in sigma between the two adjacent grid values. Bootstrap validation images within class, retaining each image's directions together. A predictive claim requires a predicted crossing bracket and crossing-interval half-width <=.20 of its point estimate. An absent/unresolved predicted crossing rejects that claim. Freeze this failed or successful prediction before TEST scoring. The independently specified native phenomenon test still runs after clean prerequisites pass; no scanning another pair or expanding the noise grid.

## Conditional test stage

- Raw-pixel noise X+sigma Z, independent isotropic standard Gaussian Z. No clipping, followed by the same fixed normalization. Grid: [0,.01,.02,.04,.08,.12,.20,.30]. Unclipped noise is an explicit modeling choice; it is not CIFAR100-C or a claim to reproduce the anchor's exact corruption settings.
- TEST uses three seeded directions per image, shared between CL and NCL. No head recalibration or retraining. Freeze and hash the prediction before loading TEST or saving any corrupted TEST scores.
- Save per-image/per-replicate errors and losses. Paired class-stratified image bootstrap, replicates clustered within image, 2,000 draws. Form simultaneous grid bands for the difference curve with Bonferroni quantiles over eight levels. This is conditional on fixed trained networks/heads.
- Resolved reversal requires a positive clean lower band and a negative corrupted upper band. Report all points, including an absent or unresolved crossing.
- Predictive success additionally requires all prediction prerequisites to pass, a resolved observed crossing bracket compatible with the frozen prediction interval, and a point crossing within a factor 1.5 of its prediction. If prediction prerequisites fail, report the observed native curve without a successful prediction claim. Grid interpolation is descriptive, not proof of a unique root. Passing on one pair is a limited predictive test, not universal validation or a complete multidimensional phase diagram.

## Resource and stopping rules

One existing checkpoint pair, one task, one clean probe seed, one noise grid. No backbone or projector training, width sweep, noise-family sweep, label noise, diffusion work, synthetic feature replacement or postfailure repair. Use the existing isolated runtime and Physics CPU allocation, whose availability was verified. Record device and timing. Infrastructure failures may be repaired without changing this scientific protocol; log them separately. Keep all research outputs, protocol hashes, splits, code and failure states. Never overwrite a completed run.


## Specific justification, interpretation and final stopping decision

The prior backbone-only experiment failed both clean prerequisites and remains recorded in real_network_ncl_20261008. Inspection of the anchor repository at commit d8519e994d8e0ccc98ad6d55978c58d70c72421e establishes that solo/methods/linear.py forward applies backbone, then projector, then ReLU when non_neg is set. Its CIFAR configs enable non_neg for NCL and leave CL signed. The predecessor main_eval.py likewise scores model output z and applies ReLU for the NCL checkpoint. Therefore the smallest necessary correction is one separate experiment on that explicitly defined native representation, not a search among arbitrary heads.

Use the actual released checkpoint projector shapes (hidden 2048, output 256), not the larger projector in the anchor's unreleased runs. No exact numerical reproduction of the anchor is claimed. Reuse the hash-verified cached clean backbone features and identical FIT/VALIDATION indices; apply the strictly loaded native projector to them. For corrupted images, execute the complete backbone-plus-projector-plus-clean-probe network, with NCL ReLU. No toy compressor or synthetic feature replacement is introduced.

This layer decision is made after observing the backbone failure but before computing projected features. It is a source-justified follow-up, not a retrospectively preregistered choice for the original experiment. The official TEST images remain unscored. No further heads, checkpoints, thresholds, noise grids or probes will be tried after this follow-up fails. Any successful crossing is one native-network observation, not proof of a monosemanticity cause, the toy exponent, a general phase diagram, or ICML acceptance. A failed result is retained in full.
