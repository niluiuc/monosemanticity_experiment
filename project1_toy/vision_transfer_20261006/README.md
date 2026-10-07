# Fixed learned-vision transfer pilot, 6 October 2026

## Question fixed before the test

Does noise-dependent decoder bias calibration change the reconstruction-risk comparison between channel isolation and sharing on a genuine trained vision representation? The Project 1 endpoint theorem proves that this policy can reverse the comparison for specified Bernoulli features. This pilot tests policy dependence outside those inputs; it does not assume the Bernoulli critical law transfers.

Read `../joint_phase_theory_2026-10-06/vision_transfer_protocol.md` and its professor/independent reviews first. Channels are operational coordinates, not independently identified semantic concepts. No labels select the pair or fit the reconstruction task.

## Settings

- Frozen official ResNet18 IMAGENET1K_V1; official resize/crop/normalization, inference mode.
- CIFAR10 training set; NumPy seed 20261006 permutation, first 1024 images, split 256 train / 256 calibration / 512 test.
- Post-ReLU layer4 central spatial cell (3,3) in a 7 by 7 feature map, before average pooling.
- First two channels with positive mean and variance on train: channels 0 and 1. Normalize by train RMS only; no centering.
- Two targets, one scalar latent dimension, encoder energy one, tied ReLU decoder with free biases, importance (1,2/3).
- Both mono orientations retained; sharing fitted using 256/512 angle grids and one prescribed best-cell bounded refinement per grid. Resolution agreement and nontrivial sharing gates required. This is numerical geometry selection, not a global certificate.
- Common code-noise reference 0.8082696313648098. Five multipliers 0, .05, .1, .2, .4 only.
- Primary frozen biases fitted at zero noise on calibration. The calibrated policy refits each model's biases on the same calibration data at each noise. Conditional Gaussian test MSE; no sampled-noise selection.
- Numerical weighted calibration gap target 1e-7; slack 1e-12, 20000 expansions/output, 300-second shared calibration limit. Floating-point bounds are not directed-rounding proofs.
- Paired image bootstrap: 2000 resamples, seed 20261006. Uncertainty is conditional on the fitted models, not training/calibration uncertainty.

## Outputs, including unfavorable findings

Extraction completed in 229.203 seconds including acquisition. Train zero fractions were .48828125 and .30859375, coactivation .37109375. All raw 512-dimensional activations and split indices are retained.

Clean train sharing gain was .01788302194236413; both numerical resolutions agreed and both refinements passed. That training advantage did not clearly transfer to the held-out split: at zero noise the primary sharing-minus-mono test difference was +.009029018418079036, with a paired interval [-.015774569470647332, .03717005826727063].

| Noise multiplier | Frozen test difference | Calibrated test difference | Policy contrast |
|---|---:|---:|---:|
| 0 | .009029018418 | .009029018418 | 0 |
| .05 | .008768297083 | .008866302820 | .000098005737 |
| .1 | .008118167409 | .008517622562 | .000399455154 |
| .2 | .006140968533 | .007738687851 | .001597719318 |
| .4 | .001454334241 | .007400884924 | .005946550683 |

Both representation-risk intervals include zero at every tested level. **No held-out mono/share ordering reversal is demonstrated.** Positive-noise policy-contrast intervals are positive at all four levels; at .4 the contrast interval is [.003553610227, .008243150735]. This supports policy dependence in this fixed operational reconstruction task, not a semantic or universal robustness claim. All calibration gaps resolved.

The independent evaluation audit verified 35 artifacts, 978 calibration nodes, raw split/channel rules, official-source file hashes, per-image Gaussian losses and all saved bootstrap summaries. Maximum independent per-image discrepancy was 5.329070518200751e-15. Forward inference was not independently duplicated.

## Reproduction without overwriting evidence

Extraction uses torch/torchvision and official downloads. The recorded runtime was Python3.12.4, torch2.14.1+cpu, torchvision0.29.1+cpu, NumPy2.3.0. Downstream uses NumPy/SciPy; plotting uses matplotlib. Large dependencies, weights and CIFAR cache live outside this repository.

From this directory, use fresh output folders:

```powershell
python vision_extract.py --protocol ../joint_phase_theory_2026-10-06/vision_transfer_protocol.md --output extraction_reproduced --cache C:/Users/indra/.cache/monosemanticity_vision_reproduction
python ../joint_phase_theory_2026-10-06/vision_transfer.py --features extraction_reproduced/vision_activations.npz --review ../joint_phase_theory_2026-10-06/vision_transfer_independent_review.md --output vision_reproduced
python audit_vision_outputs.py --extraction extraction_reproduced --evaluation vision_reproduced --output audit_reproduced
python ../joint_phase_theory_2026-10-06/plot_vision_transfer.py --run vision_reproduced --output plots_reproduced
```

Enforce an outer acquisition/extraction timeout because blocking downloads cannot obey an internal clock. The original run used 660 seconds outside and 600 seconds inside. Do not substitute random weights if download fails. Fresh inference on another library/device may have numerical differences; compare provenance rather than implying bitwise reproducibility everywhere.

## Stopping decision

The completed [saved-record mechanism audit](mechanism_audit_summary.md) used
only existing targets, weights, biases and conditional losses. Target0 is zero
on271/512 held-out images. Mono sits at its zero gate there; sharing's gate
distances are displaced and heterogeneous. Those images contribute68.7% of the
largest-noise contrast. Positive-target images contribute the remaining31.3%,
but calibration increases held-out error on that group in both models, more
in sharing. All groups/outputs/noise cases are saved in `mechanism_audit_v1`.
This is a descriptive association, not a causal gate intervention, and adds
no subgroup significance claims or ordering reversal.

This fixed pilot is complete. Do not replace the channels, extend the noise grid or choose another checkpoint to obtain a preferred sign. The theory remains proved in its declared scope. Learned semantic monosemanticity and a real-model phase boundary remain unresolved. Review the professor's post-pilot decision before choosing any further experimental work.
