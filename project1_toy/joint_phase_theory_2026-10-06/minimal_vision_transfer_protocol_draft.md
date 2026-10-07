# One bounded learned-vision transfer: decoder-policy ordering

6 October 2026. Prospective, read-only feasibility proposal. No image download, checkpoint download, feature extraction or model training has been performed. This protocol requires review before execution.

## Specific gap and question

The toy theorem is a trained two-feature Bernoulli result. A real learned representation must be tested before claiming its mechanism matters outside that distribution. The smallest direct question is: does the risk difference between a clean-trained sharing bottleneck and a coordinate-retaining bottleneck depend on whether both decoders receive bias calibration, when the targets come from a genuinely learned vision representation?

The target remains weighted squared reconstruction error and the perturbation remains Gaussian noise added to the bottleneck code. This does not test image-input corruption, adversarial robustness, semantic interpretability of ResNet channels, image generation or the Bernoulli 3/2 exponent. Those are separate claims.

## Single model and fixed data

Use one frozen ImageNet-pretrained ResNet18 checkpoint (`IMAGENET1K_V1`), inference mode, official checkpoint transforms. Extract its nonnegative average-pooled penultimate features from one fixed public natural-image dataset, using an independently defined train/calibration/test split with 256/256/512 images. CIFAR-10 can supply the images; class labels do not enter the reconstruction target. Save exact image indices, checkpoint/data hashes, transforms and extracted activations.

The official model/weights/transforms are described at https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.resnet18.html . No pretrained weight is available by default merely because the architecture is instantiated.

From train activations only, select the two lowest-index channels with nonzero variance and nonzero empirical mean; no search for favorable overlap, clean gain or noise crossing. Normalize each by its train RMS without centering, to retain nonnegative targets and make coordinate scale explicit. If either selection fails, stop and report the failure. Do not try another pair. Use fixed importance (1,1/2).

## Matched models and evaluation

Both models have two targets, one code dimension, encoder squared energy one, tied linear weights, ReLU decoder and two biases. The mono comparator is the better of the two coordinate-retaining geometries on clean training loss, chosen using training data only. The sharing encoder/biases are fitted on the same clean training target. Reuse finite clean bias profiling and a bounded deterministic one-dimensional angle search; archive its resolution, candidates and selected geometry. It is an approximate empirical clean selection unless an actual global certificate is supplied. A failed optimization check blocks a selection claim rather than triggers additional restarts.

Freeze both encoders. Evaluate sigma in {0,.05,.1,.2,.4}, measured in the saved normalized code units, once under the clean-trained biases and once under free bias calibration for both models on the disjoint calibration split. The test split is used only to evaluate the resulting fixed models. Use the existing Gaussian conditional moment equations, averaged over saved test activations, so no favorable random-noise realization can be selected. Calibration code must support continuous nonnegative targets; the current binary-state implementation cannot silently be reused without adapting and verifying that assumption.

Report both models' test risks, their signed difference, model/bias parameters and per-image losses at every prescribed point, including unfavorable orderings. A deterministic conditional expectation over code noise is still an empirical estimate over a finite image sample. Paired image resampling can give uncertainty intervals with fixed seed and fixed count; it does not certify a population sign or global calibration optimum.

## Stop/extend gate

Stop after this one channel pair, one checkpoint and five noise levels. Proceed only if the trained sharing model has a measurable clean held-out advantage and the optimization/calibration quality is adequate to distinguish the compared risks. Otherwise retain all outputs and classify the transfer as inconclusive or negative. No second pair, noise-grid expansion, new backbone, nonlinear decoder or diffusion training is authorized by this draft.

If the predefined test yields a resolved ordering change and a resolved policy difference, the next decision is whether it deserves one independent reproduction using the identical protocol. It must not be presented as main-track evidence of semantic monosemanticity or a universal phase exponent. Its contribution would be a narrow learned-feature check of the decoder-policy mechanism.

## Present feasibility limitation

The bundled Python currently lacks torch/torchvision and no genuine image features/checkpoint were found in the existing experiment assets. This is not executable from the available local artifacts without new dependencies/data. Do not replace it with random features or synthetic pixels and call that real-model transfer. A team member with an existing vision environment can extract the frozen activations; the downstream numerical work can then run in the current NumPy/SciPy environment.
