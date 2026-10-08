# Controlled image-CNN detection boundary

Read PROTOCOL.md first. This is a bounded transfer of the already verified five-concept fixed-pentagon boundary to a CNN that directly outputs a two-dimensional code from images. No ideal binary vector is supplied at inference. The geometry is imposed by code targets; the five visual marks are synthetic, with CIFAR backgrounds. Corruption is Gaussian code noise, not pixel corruption.

## Results
Both prescribed training runs completed80epochs. Before TEST scoring, the ideal formula predicted a p=.2 crossing .17108537; calibration images predicted .16849808. Frozen files/hashes precede test codes.

Held-out clean summed detection errors: sharing .39495, mono .60000. The advantage reverses between code-noise .150 and .175. Both predictions are in that interval. The registered calibration crossing-error criterion passes. Do not call its midpoint .1625 an exact observed root.

Background bootstrap clean-gap interval is [-.207669,-.201681]. Every bootstrap first-root midpoint falls in the same grid bin; the apparent zero-width midpoint interval means grid resolution, not zero statistical uncertainty. Results are conditional on one trained model pair.

The independent verifier replays every saved noise/state/background error with zero discrepancy; Gaussian-risk grids agree to2.23e-16. Hashes, splits and prospective prediction timing check out. This establishes the controlled comparison, not naturally selected semantic geometry or ordinary real-image robustness.

## What changed from the toy
Each CNN learns image-to-code mapping directly. Both have identical architecture/initialisation and supervised targets from energy2 dictionaries. Dictionary energy is controlled; total CNN weight energy is not constrained. All5 detection errors count, including mono's3 omitted concepts. No threshold recalibration under test noise.

The ideal line ignores perception error. The green calibration line uses measured clean codes before test scoring. They are distinct predictions; the black line remains the existing mathematics.

## Reproduce
Use the workspace storage launcher at the repository root so every cache/tmp/output stays on D:. Existing torch/torchvision runtime can be executed read-only. The script stages the existing CIFAR10 cache from its legacy location onto D: with downloads disabled. Dependency/data paths can be changed for another machine without changing scientific settings.

Run run.py into a fresh output location (run_v1 must not exist), then verify.py. Preserve the archived run rather than overwriting it. The registered source/protocol, split IDs, all images, histories, models, calibration/test codes, frozen predictions, raw noise, background/state losses, bootstrap and plots are in run_v1.

## Review and stop
The code-noise formula applies exactly conditional on any fixed clean CNN code; ideal-code prediction is approximate and was tested prospectively. The black boundary aligns with held-out colours in this construction. The experiment is deliberately engineered to realise specified codes, so it is not evidence that pretrained networks naturally select those codes. No publication novelty or seed-general result is claimed. The registered pair is complete; do not add settings to improve its appearance.

Full mathematical assumptions, conditional-risk derivation and results are in the existing derivation PDF/source, Section8.45.

## Recording deviation
The protocol promised a final-window loss change in the prospective prediction record; the runner omitted that descriptive field. TRAINING_DIAGNOSTIC.json now reports it post-run from saved histories, without modifying frozen predictions. Completion of80epochs is not a CNN stationarity certificate. This field was not a stopping gate, and the registered crossing criterion is unchanged.
