# Fixed class-evidence transfer protocol — prospective

6 October 2026. Written before forward inference or score inspection for this pair. This is a bounded alternative after the unmapped feature export failed. It reuses the official cached ResNet and existing continuous reconstruction machinery. It does not silently satisfy the earlier hidden-semantic-feature requirement: its claim ceiling is **storage and noisy reconstruction of independently class-mapped evidence coordinates**, not validated monosemantic hidden features.

## Question, connection and smallest useful test

Does clean sharing of two named real-model class-evidence scores outperform coordinate retention on held-out images, and where does Gaussian scalar-code corruption alter their ordering under frozen and symmetric bias calibration? The mathematical reference is the Project 1 selected-geometry risk comparison. One fixed pair and five fixed noise levels suffice for a transfer check. No critical exponent, full-model robustness, universal semantics or safety claim follows.

## Independent class mapping and feature definition

- Official torchvision ResNet18 `IMAGENET1K_V1`, checkpoint `resnet18-f37072fd.pth`, official transforms, frozen inference mode. Exact checkpoint hash must match the previous official extraction's hash.
- Fix output indices **281 (`tabby`) and 207 (`golden retriever`)**, in that order, from the official weights' category list. Verify these names before inference. This choice uses only external class names, not activation or risk outcomes.
- Targets are `max(logit_281,0)` and `max(logit_207,0)`. Save signed logits and the deterministic transformation. Zero is a declared checkpoint-dependent truncation threshold, NOT concept absence. Class supervision provides a named evidence association; it does not prove monosemanticity, causal feature identity or an identifiable logit zero. Never change the threshold, pair or class aggregation after inspecting scores.
- CIFAR10 has coarse cat/dog labels, which do not identify tabby/breed specifically. Labels are used only to check broad association with the intended cat/dog category, not to fit the reconstruction task or claim exact subclass accuracy.

## Data, extraction and limits

- Cached CIFAR10 training set, no new downloads/model/environment. Permute 50,000 indices once with NumPy default_rng(20261007); use first 256 train, next 256 calibration, next 4,096 test. Preserve all image IDs and CIFAR labels. One observation per image. Do not choose by class.
- Official 256-resize/224-crop/ImageNet normalization, CPU four threads, batch32. One fixed forward pass over 4,608 images. Save all 1,000 signed logits so mapping can be independently checked, and save the two raw targets. Check the time before each batch; 1,200 seconds total extraction budget, preserve partial outputs on failure, no retry with a changed model/transform or fewer observations.
- Label-association gate uses TRAIN ONLY: rectified tabby evidence versus CIFAR cat indicator and rectified golden-retriever evidence versus dog indicator must each have AUROC > .65, with both label classes represented. This is a prespecified sanity check of broad association, not an optimized classification metric. Save labels and scores; failed gate stops risk evaluation with no replacement pair. Report test association descriptively only if the run passes, without using it to select anything.

## Reconstruction protocol

Reuse every numerical rule in `semantic_followup_protocol.md`: importance(1,2/3), train-RMS normalization, scalar energy-one tied-ReLU encoder/decoder, both mono orientations, grids256/512 plus one best-cell refinement each, absolute loss agreement1e-6, sharing gain>1e-6, both mixed column energies>1e-8, and at least one exact zero fraction in train. Failed clean/semantic gate stops before noisy comparisons.

Freeze train-selected encoders. Zero-noise biases fitted on calibration are the frozen baseline; calibrated biases refit on the same split at each sigma. Noise reference is sqrt(mean training variance of normalized coordinates), multipliers{0,.05,.1,.2,.4}. Exact conditional Gaussian risk on the 4,096 test images. Same calibration gap1e-7, slack1e-12, 20,000 expansions per output, shared300second calibration budget. No tolerance changes on failure.

Primary outcome: calibrated sharing-minus-mono test MSE at multiplier .4. Secondary: frozen difference and policy contrast at .4. Save all five levels and all failures. Paired bootstrap2,000 samples, seed20261007, 95% pointwise percentile intervals conditional on fitted models, with full indices/outputs saved. A reversal needs resolved opposing clean/noisy orderings; policy contrast alone is insufficient.

## Teacher review, reproducibility and stop

Before forward inference, professor must review the feature-definition/semantic claim ceiling. Before evaluation, independent review must check fixed-ID loading, label gate, numerical adapter and loss/paired-bootstrap correspondence. Use existing functions without changing their mathematics; do not invoke the old channel-selecting CLI unchanged.

Run this one pair once. No replacement pair, output aggregation, threshold tuning, additional noise/model, symbolic fitting, SAE training or optimizer repair. Full extraction, settings, failures and source/protocol hashes are retained. If eligible and complete, plot actual risk differences, audit them independently, integrate actual results/limitations in the existing derivation volume, and make a paper-strength decision. This test cannot close a claim specifically about hidden-feature monosemanticity even if favorable.
