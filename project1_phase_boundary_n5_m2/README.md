# Project 1: from the n=2,m=1 boundary to n=5,m=2 and a learned visual bottleneck

This folder packages the completed progression with original outcomes intact. The larger completed experiment is **five concepts in two dimensions**, not m=3.

## What is established

| Stage | Result | Limit |
|---|---|---|
| Original fixed n2/m1 codes | Independent simulated colours agree with the exact mathematical contour | Specified geometry and decoder |
| Fixed n5/m2 regular pentagon, energy2 | p=.2 clean error .40352 versus mono .6; crossing .17108537 | Not a learned or globally optimal geometry |
| Detection-trained n5/m2 encoders | Three local numerical convergence checks pass; crossings .202698/.185423/.184090 | Small-noise objective can be flat; fitted decoders; not global optima |
| Controlled image CNN pair | Held-out clean .39495 versus .6; reversal .150-.175, containing both ideal prediction .17108537 and calibration prediction .16849808 | Geometry taught via targets; synthetic marks/CIFAR backgrounds; bottleneck noise |

The image predictions were frozen before TEST scoring. Independent output verification replays all saved error counts exactly and checks hashes/splits/timing. This is a controlled visual test of the existing mathematics, not naturally occurring semantic geometry or pixel-noise robustness. One trained model pair does not establish seed generality or publication novelty.

## Read in order

1. `project1_toy/detection_repair_20261008/README.md`, both protocols, `run_v1/fixed_pentagon_results.json`, plots and verification.
2. `project1_toy/visual_detection_boundary_20261008/PROTOCOL.md` and README, then `run_v1/prediction.json`, `result.json`, `independent_verification.json` and the heatmap.
3. `project1_toy/learned_four_concepts_20261008/` and `learned_five_concepts_20261008/` retain earlier bounded training outcomes, including failed stability checks. They must not be presented as uninterrupted successful detection training.

## Reproduce or independently verify

Install Python3 with NumPy, SciPy and Matplotlib; image training additionally needs torch and torchvision. Run each saved-output `verify.py` from its experiment directory; these checks require no model/dataset downloads. The image verifier needs only NumPy/SciPy and the supplied saved codes/noise.

For fresh experiments copy the scripts, protocols, required initial encoders and trainer dependencies into a **new** directory with this same structure, leaving original `run_v1` evidence untouched. `run.py` refuses to overwrite a recorded run. Detection training reads the supplied archived five-concept initial encoders. Run detection `run.py`, `fixed_geometry.py`, then `verify.py`. For visual training prepare CIFAR10 with `prepare_visual_data.py --root YOUR_FRESH_PACKAGE_ROOT --download`, then run visual `run.py` and `verify.py`. Dataset cache is under that package's `cache/visual_boundary_data`; no raw CIFAR download or runtime is committed. The source's legacy C: path is bypassed when that expected cache exists.

Model checkpoints, rendered experimental images, histories, raw noise/states, thresholds, all risk grids, calibration/test codes, bootstrap records and SHA manifests are included. No favorable seeds/checkpoints were substituted. `focused_bridge_2026-10-06/toy/` supplies the original earlier-training dependencies.

The workspace storage launcher redirects all new research caches and temporary files to the assigned D: workspace. Adjust its workspace path on another machine. None of the published experimental files needs access to passwords, SSH or the cluster.

## Documents and upload exclusions

The updated approved mathematical document is at the repository's `output/pdf/Superposition_Recursive_Training_Derivations.pdf`; it includes full derivations and printed programs. Updated research notes and editable Overleaf source remain local under the owner's requested upload exclusions. No .tex files, other PDFs, personal chat archives, receipts, runtime caches or credentials are included in this package.

All publication-facing claims must retain the stated controlled-geometry, decoder, data-construction, corruption and single-model-pair limitations.
