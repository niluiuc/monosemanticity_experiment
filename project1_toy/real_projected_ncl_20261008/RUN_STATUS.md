# Source-justified projected-representation follow-up

## Why this separate test is necessary

The backbone-only experiment in `../real_network_ncl_20261008` failed both clean prerequisites and is retained as failed. Inspection of the anchor's actual evaluation code revealed a specific experimental-choice error: its classifier receives `backbone -> projector`, followed by ReLU for NCL. The predecessor's default linear-probe path had motivated testing the bare backbone, but that was not the anchor's actual released evaluation path.

Primary source: `PKU-ML/Beyond_Interpretability`, commit `d8519e994d8e0ccc98ad6d55978c58d70c72421e`, `solo/methods/linear.py` forward and `scripts/linear/cifar/{base,ncl}_clean.yaml`. The predecessor's `main_eval.py` also explicitly scores `z`, with ReLU for the NCL checkpoint.

This is a separately registered, source-justified follow-up selected after a backbone failure. It is not retrospectively the original experiment and must not be reported as one uninterrupted successful protocol. No further layer/head search is permitted after this follow-up.

## Question and smallest useful test

For the fixed native projected representations, does CL's clean advantage reverse under Gaussian pixel noise, and does a validation-only affine margin predictor forecast the crossing? Keep both full pretrained networks frozen and fit the same clean probes as before. Use actual released projector shapes, 2048 hidden and 256 output, with CL signed and NCL ReLU outputs. Reuse hash-verified clean backbone features and identical splits; evaluate the complete network on corrupted images. These releases are not the anchor's larger-projector checkpoints, so exact paper replication is not claimed.

## Settings and registration

`PROTOCOL.md` specifies the full settings, thresholds and stopping rules. `REGISTRATION.json` timestamps the decision before projected features were computed and records zero TEST images scored. Scratch root: `/scratch/idas3/ncl_projected_20261008_v1`. Heavy data, checkpoints and runtime are symlinked to the existing verified scratch dependencies.

The first sbatch submission was rejected for DOS line endings; no experiment ran from it. After converting only the batch scripts to LF, clean CPU job **11212390** and conditional CPU job **11212391** were submitted on the Physics allocation. The clean job completed; the conditional job is running. No models were retrained.

## Clean results

- CL validation error: 0.443000; NCL: 0.464800. NCL minus CL is +0.021800, with conditional paired-image 95% interval [0.011000, 0.033400]. CL's required clean advantage is established for this fitted pair.
- CL class-consistency proxy: 0.010001187; NCL: 0.114704363. Difference +0.104703176, interval [0.101658631, 0.108490251]. The required proxy contrast is established at this representation.
- Raw sparsity below 0.01: CL 0.025153125; NCL 0.937742949. Nondead coordinates: CL 256, NCL 232.
- Both clean gates pass. This is a starting-condition result, not evidence of corruption reversal or a causal monosemanticity effect. Single checkpoints and single fitted probes remain the limit of inference.
- The cached-feature clean calculation took about 5.13 seconds. Independent verification and final corruption results are still pending at this entry.

## Next decision

Run the fixed validation prediction and applicability checks, freeze successful or failed predictions, then measure the predeclared native TEST curve. Failed prediction gates reject the predictive claim, while the separately specified native phenomenon question still gets measured. Report every point and failure; do not widen the grid or substitute another head/checkpoint.


## Completed native outcome and independent checks, 8 October 2026

- Both jobs completed. The native corruption computation took 12 minutes 45 seconds on Physics CPU resources. The SSH connection remains open; no original user job was changed.
- The affine prediction failed and was frozen before TEST scoring. It predicts no crossing. Its frozen hash is c643b6e46cd7f170937cd95b0bac89d7c303463a3392e3c20d3c0443664eec00. This failure is not repaired by the subsequent observation.
- On the official 10,000-image TEST set, CL wins clean: NCL-minus-CL error +0.016500, simultaneous conditional interval [0.0048246875,0.027600]. At sigma .12, NCL wins: difference -0.0122333333, interval [-0.018684375,-0.00607489583]. At sigma .20 it also wins: -0.006500, interval [-0.0108502083,-0.00211645833]. This establishes the native ordering reversal at evaluated noise levels for this checkpoint/probe pair.
- The .08 difference is unresolved. The first point-estimate crossing lies between .04 and .08; linear interpolation .078352941176 is descriptive, not a successful forecast or a crossing confidence interval. At .30 CL regains a small advantage; both accuracies are below 3%, near 1% chance. There is no evidence for a unique permanent phase transition.
- Independent NumPy checks reproduce saved errors, paired-image simultaneous bands, decisions, prediction curve and hash. Cached-feature class consistency was separately recomputed. Complete scientific arrays and logs are in outputs; large training caches and checkpoints remain on scratch.
- The earlier reconstruction theorem has a different loss, noise location and representation. Its numerical boundary and critical exponent are not validated here. Existing monosemanticity papers already show robustness gains: this one comparison is not publication novelty by itself, a causal monosemanticity intervention, or a completed ICML contribution.
- Sections 8.35 and 8.36 retain the failed backbone prerequisites, successful native ordering reversal and failed prediction. Current derivation PDF and editable source compiled successfully; new pages 96--99 were visually checked without overflow.
- The remaining paper-critical gap is a finite-noise explanatory/predictive mechanism, with independent replication. One post-outcome, validation-only gate diagnostic is registered separately: at the already failed sigma .04, compare full affine logits with affine backbone plus exact nonlinear projector. If the latter fails existing thresholds, stop projection-only repairs. No new TEST evidence or retrospective prediction success is claimed.
