# Fixed class-evidence reconstruction transfer

This is the one bounded real-model follow-up performed after the unmapped SAE archive failed its eligibility gate. Read the prospective protocol and teacher reviews in `../paper_assembly_20261006/` before running anything. The research question remains where clean-trained scalar sharing beats coordinate retention under corruption; this experiment evaluates one class-mapped operational slice of that question.

## Motivation and claim ceiling

The previous ResNet hidden-channel pilot lacked independently documented concept names and had unresolved held-out representation orderings. Here the official ResNet18 class head independently maps indices281/207 to tabby/golden retriever before score inspection. Rectified head logits supply reproducible named evidence coordinates, not validated monosemantic hidden features or ground-truth concepts. The fixed zero threshold is checkpoint-gauge dependent; zero does not imply absence. CIFAR cat/dog labels do not certify these subclasses. Reconstruction of an auxiliary code is not full-network/image-input robustness.

## Fixed settings and gates

- Official frozen `IMAGENET1K_V1` ResNet18 and transforms; cached checkpoint/data reused, CPU4threads/batch32, no model training. Full forward pass, not a hidden central-cell approximation.
- 4,608 seeded CIFAR training images:256 train/256 calibration/4,096 test, NumPy seed20261007. No class or outcome-based selection.
- Fixed targets `max(logit281,0)` and `max(logit207,0)`; all1,000 signed head logits, labels and image indices retained.
- TRAIN-only coarse cat/dog association AUROC>.65 each; nonconstant targets, zero support and original clean selection gates fixed before inference.
- Train-only RMS scaling; importance(1,2/3); scalar encoder energy1; tied ReLU reconstruction with two biases. Both mono orientations considered; omitted-feature constant error included.
- Clean angle grids256/512, one best-cell refinement each; same numerical profiler as the first pilot. Numerical selection is not a global certificate.
- Frozen baseline biases fitted at zero noise on the calibration split; both models may refit biases on that same split at each prescribed noise. Encoders remain fixed.
- Absolute Gaussian scalar-code noise SD `.730851028581592 * {0,.05,.1,.2,.4}`. Same gap1e-7, slack1e-12,20,000 expansions/output,300second shared calibration budget. Conditional Gaussian MSE, not sampled favorable corruptions.
- Primary: calibrated difference at .4. Paired bootstrap2,000 image resamples, seed20261007; default integer draw then lossless uint16 storage. Intervals are pointwise and conditional on fixed fits.

## Actual results, including what did not happen

Extraction completed in304.453seconds; both association gates passed (.904952/.808194 train, .870035/.817291 held-out descriptive). Training clean losses were .300735002 sharing and .371810660 mono, with same-sign sharing weights(.83541738,.54961605). Both clean-search resolutions agreed and every gate passed.

| Noise multiplier | Frozen sharing−mono | Calibrated sharing−mono |
|---:|---:|---:|
| 0 | −.0710555300 | −.0710555300 |
| .05 | −.0711332655 | −.0711548026 |
| .10 | −.0713038655 | −.0713725079 |
| .20 | −.0718532322 | −.0719331061 |
| .40 | −.0738861898 | −.0732688755 |

All ten pointwise difference intervals were belowzero. At primary .4, calibrated interval was[−.0916031457,−.0538851969]; sharing/mono absolute MSE was .398223291/.471492166. **No ordering reversal occurred.** Sharing's point advantage slightly grew with noise while both absolute risks rose. Do not describe this as noise improving either model or reproducing the Bernoulli critical transition/exponent.

Policy contrast(calibrated−frozen difference) was negative with intervals belowzero at .05/.10, negative but unresolved at .20, and positive at .40 (.0006173143,[.0003468203,.0008997372]). It changed the relative benefit, never the winner. Both models' risk improved with calibration at the primary level; their benefits were .002236486 sharing/.002853800 mono. All calibration gaps resolved within the unchanged target.

The ordinary encoder and tied-decoder total energies match; importance-weighted output sensitivity and each coordinate's noise scale need not match. Redistribution of that sensitivity is part of the declared comparison. Neither this result nor the earlier pilot isolates geometry from every decoder/noise effect. This is a held-out sharing-favored slice, not a completed real phase diagram.

## Independent verification

`independent_audit_v1/` checks9 extraction/38 evaluation manifest files, seeded indices and cached labels, category/checkpoint provenance, exact rectification, training RMS, pair-count/tie-aware AUROC, clean-grid losses, every conditional Gaussian risk,896 calibration nodes, and all bootstrap outputs. Maximum risk discrepancy4.44e-15. The audit did not repeat forward inference or add cases. All original outputs are immutable. `audit_saved.py` imports no experiment risk function.

First-generation figure captions clipped at the edge. `plots_v2/` corrects caption wrapping using the same saved rows; `plots_v1/` remains preserved. No outcome changed.

## Reproduction

Dependencies for extraction: Python/NumPy/PyTorch/torchvision; evaluation/audit: NumPy/SciPy; figures: Matplotlib. The original isolated extraction runtime is outside the repository. Required caches are the official checkpoint and CIFAR10 archive, with hashes in extraction provenance. Check the protocol/source hashes and reviews first.

For a saved-record verification from the repository root, run:

```sh
python project1_toy/head_transfer_20261007/audit_saved.py --extraction project1_toy/head_transfer_20261007/extraction_run_v1 --evaluation project1_toy/head_transfer_20261007/evaluation_run_v1 --output project1_toy/head_transfer_20261007/teammate_audit_v1
```

Use a new audit output path every time. The auditor also checks cached CIFAR labels when the original cache exists; read its source for that dependency. For fresh forward/evaluation reproduction, the original scripts intentionally refuse to overwrite the archived `extraction_run_v1`/`evaluation_run_v1`. Use a separate reproduction working copy and change only output/cache path constants for your host, preserve a source diff documenting those path changes, and retain the fixed settings and reviews. Do not delete original public evidence to make the scripts run. The evaluation script expects the saved fixed-ID extraction and reviewed adapter, and imports the existing `../joint_phase_theory_2026-10-06/vision_transfer.py` functions. Use `python plot_saved.py --output <new-plot-directory>` to plot saved results only.

## Stop and next paper work

This pair/grid is complete and stopped. No replacement class, truncation, larger noise, optimizer repair or another model is authorized by its protocol. Incorporate the actual outcomes and earlier unfavorable pilot in the manuscript and existing derivation PDF. Theory supplies the scoped critical boundary; this test supplies a resolved labeled operational sharing advantage. A direct real training-transition-linked phase boundary and validated hidden-feature monosemanticity remain unestablished. New experiments require a specific paper-critical gap and prospective design, not a hunt for a reversal.
