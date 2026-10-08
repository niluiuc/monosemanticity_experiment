# Native CL/NCL robustness experiment

## Research question

Does the more class-consistent, nonnegative representation lose to its conventional counterpart on clean classification, then win as input corruption increases? Can a representation-based calculation predict that reversal?

This is Project 1's real-network arm. Both complete frozen ResNet-18 networks, their original projectors, and clean fitted classifiers process actual corrupted CIFAR-100 images. This is not a two-feature toy compressor fitted to real activations.

## Current answer

- **Observed ordering reversal:** CL wins clean; NCL wins at Gaussian pixel-noise standard deviations .12 and .20. At .30 CL returns to a small advantage when both models are near chance. There is no evidence for a permanent single crossing.
- **Prediction failed:** a validation-only affine margin/Jacobian predictor forecasts no crossing and fails its finite-noise applicability checks. It was frozen before TEST scoring; the failed forecast remains unchanged.
- **Proposed gate repair failed:** permitting the native projector gates to switch after an affine CNN approximation does not meet the existing thresholds. Stop projection-only repairs.
- **Descriptive diagnosis:** much of the saved affine residual energy is a coherent mean over sampled noise directions. This does not by itself explain the ordering reversal or yield a crossing law.
- **Probe-seed reliability:** both prespecified additional probe seeds reproduce the resolved clean-versus-.12 reversal. This is the same backbone pair and reused TEST images.

These are one released checkpoint pair, one dataset and one corruption family. Class consistency is a proxy; NCL changes the training method and does not isolate monosemanticity causally. The toy reconstruction theorem has different assumptions/loss/noise and is not quantitatively validated here. A novelty claim or finished ICML contribution is not established.

## Why the projected representation

The preceding bare-backbone test failed its prerequisites and remains failed in `../real_network_ncl_20261008`. The anchor's actual evaluation code applies the native projector, with final ReLU for NCL. This source-justified follow-up was registered before projected features were computed, after the backbone failure. It must not be rewritten as an uninterrupted successful original protocol.

Sources: [anchor code](https://github.com/PKU-ML/Beyond_Interpretability), commit d8519e994d8e0ccc98ad6d55978c58d70c72421e; [released checkpoint predecessor](https://github.com/PKU-ML/non_neg). The released projectors are smaller than the anchor's own training runs. No exact replication claim is made.

## Read and verify

1. `PROTOCOL.md`, `REGISTRATION.json` and `RUN_STATUS.md`: motivation, settings, chronology and limitations.
2. `outputs/clean_run_v1/results.json`: clean prerequisite contrast.
3. `outputs/prediction_run_v1/prediction.json` and `frozen_prediction_hash.json`: unsuccessful frozen prediction and timestamp.
4. `outputs/test_run_v1/results.json`: all eight actual noise levels and simultaneous conditional intervals.
5. `outputs/independent_output_verification.json`: independent recomputation.
6. `GATE_DIAGNOSTIC_PROTOCOL.md`, `outputs/gate_diagnostic_v1/`: saved actual/approximate logits, failed repair, independent verification and residual decomposition.
7. `PROBE_REPLICATION_PROTOCOL.md`, `PROBE_REPLICATION_JOB.json`: bounded follow-up settings; its outcome is retained separately.

Plots are under `outputs/figures/` and `outputs/gate_diagnostic_v1/`. The derivations PDF includes the standard conditional affine calculation, observed native outcome, failures and diagnostic identity in Sections 8.34--8.40. Editable LaTeX remains local, as requested.

## Reproduction

Python 3, PyTorch 2.6.0, torchvision .21.0 and NumPy 2.1.3 were used on cluster CPU. Checkpoints, CIFAR archive, runtime and full training-feature caches remain outside Git under `/scratch/idas3/ncl_projected_20261008_v1`, with shared dependencies under `/scratch/idas3/ncl_native_20261008_v1`. Source paths and hashes are recorded in provenance. Never overwrite an existing run directory: scripts deliberately fail if their output directory already exists.

For a fresh scratch root with the recorded checkpoints/data and cached training features, run `run_clean_gate.py --root ROOT`, `run_prediction.py --root ROOT`, then `run_test.py --root ROOT` under the protocol's gates. The clean script's `PRIOR_ROOT` points to the recorded backbone cache; update only that infrastructure path for a new machine. Use the immutable original source and protocol for exact reproduction.

Saved-output verification requires no checkpoint download: run `verify_saved_outputs.py`, `audit_consistency.py` where the documented cache is available, and `retrieve_gate_diagnostic.py` for the cluster-backed diagnostic retrieval plus independent saved-logit check. `residual_analysis.py` uses only the retrieved diagnostic arrays. Never edit original outcomes to fit a narrative.

The prevalence-control and finite-response screen records are in their named protocol files and outputs. The latter fails; do not replace the original frozen prediction with it. See PAPER_CLAIMS.md for the supported contribution versus remaining scientific gap.
