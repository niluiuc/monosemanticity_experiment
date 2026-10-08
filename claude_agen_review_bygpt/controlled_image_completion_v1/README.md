# Controlled learned-image comparison: completed, recovery gate failed

## Motivation and prior decision

Project 1 asks when sharing's clean coverage gain reverses under corruption. The original ResNet pair studies do not meet the independent-binary assumptions needed for the critical law. An existing, prospectively reviewed fixture therefore trains a CNN to infer two planted visual factors from nuisance-varying CIFAR backgrounds, then compresses its continuous scores while scoring reconstruction of the actual factors. This is controlled/semi-synthetic learned vision, not native semantic-feature or input-adversarial robustness.

The fixture and stopping rules were fixed before its original training. This continuation reused its final saved checkpoint, all settings and learned scores; no retraining, new seed, score thresholding or noise search occurred. The archived protocol is in project1_toy/controlled_image_phase_20261007/protocol_snapshot/continuation_design_experiment.md. The theory/proof is controlled_vision_coupling.tex in project1_toy/professor_bridge_review_20261007/.

## Settings

- 256 training, 64 calibration, 256 test backgrounds, disjoint, each with all four equally weighted disk/bar factor states.
- Existing CPU CNN, final 80-epoch checkpoint; continuous float64 sigmoid scores.
- Compress first 64 training quartets only: 256 observations; true planted labels remain reconstruction targets.
- Scalar energy-one tied-ReLU sharing code versus both mono orientations; choose mono on training only.
- Clean selection at the prescribed 256/512 angle resolutions and local refinement. No global-optimality assertion from grid agreement.
- Calibrate each model fairly at Gaussian code-noise standard deviations 0 and .30 only, using existing finite bias profiles and numerical gap-based Gaussian calibration.
- Freeze actual parameters, checkpoint/script hashes, ideal four-state risks and transported sign intervals before constructing any test images.
- Stop after this fixture. Required recovery RMS <=.0005; optimisation-excess upper bound <=.0015; both predicted signs strict.

## Prediction and actual result

Train-subset recovery was .0000481727; optimisation-excess upper bound .0000480169. Calibration and prediction gates passed.

| Noise sigma | Predicted risk-difference interval | Held-out sharing-minus-mono |
|---|---|---|
| 0 | [-.00457085, -.00257802] | -.00357219308 |
| .30 | [.00430211, .00654786] | +.00542582972 |

But test recovery RMS was **.00120416846**, above **.0005**. Therefore **the predeclared experiment did not pass**. Both observations are inside the prediction intervals; this favourable agreement must not be used to hide the failed recovery gate.

The deterministic coupling bounds computed using actual test recovery still have negative/positive signs respectively. They describe the finite tested distribution with its measured perception error; they do not retroactively satisfy the prospective recovery requirement, establish population generalisation or validate the critical exponent. No thresholds, parameters or model were changed.

Independent saved-result verification (separate Gaussian-risk implementation) reproduced differences within 1.65e-17 and checked state balance, split disjointness and the failed-gate verdict. Numerical calibration gaps are floating-point calculations, not directed-rounding certificates. No bootstrap inference was needed for these finite-record risk identities.

## Reproduction

From the repository root, use Python with NumPy/SciPy/Matplotlib:

1. Read prediction.json, evaluation.json and independent_verification.json.
2. Run `python claude_agen_review_bygpt/verify_controlled_completion.py` to recompute stored-test risk and plots. This writes only verification/plot outputs here; it does not train or select new settings.
3. For complete repetition, copy the protocol/checkpoint and use a fresh working directory; the original prediction script intentionally refuses to overwrite this archive. Save changes limited to output paths. Test inference also requires the cached CIFAR data and original PyTorch runtime.

Relevant code is ../controlled_image_completion.py and ../verify_controlled_completion.py. Test inference used the original archived source_snapshot.py; its checkpoint and source hashes are recorded in prediction.json and test_inference/provenance.json. Per-image differences, raw scores, generated test images and recovery failure are retained.

## Research decision

This gives a concrete controlled learned-image ordering reversal, with a failed prospective quality gate. It is supporting numerical evidence, not a main-track achievement by itself. The mathematics explains how perception errors can preserve or obscure the risk signs. Native-network and critical-boundary transfer remain unresolved. Do not repair the image model or search new pairs to turn this protocol into a pass.
