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


## Bounded gate diagnostic completed

- Physics CPU job 11212585 completed. This is explicitly post-outcome validation analysis, not a revised successful prediction.
- At sigma .04, affine CNN plus exact nonlinear projector fails both networks: error discrepancies .0599375/.0830000 and relative centered-logit RMS residuals 1.145880/.960406 for CL/NCL. Stop projection-only repairs.
- All actual/approximate logits are saved, unlike the first prediction run's aggregate residual record. Independent NumPy recomputation reproduces errors and residuals. No TEST images were loaded.
- The exact saved-record energy decomposition attributes .716019/.678497 of full-affine residual energy to the empirical direction mean for CL/NCL. This mean includes sampling variation. It is descriptive evidence of a substantial coherent component, not causal attribution or a crossing law.
- Full assumptions, derivation of the standard residual identity, outcomes and plot are integrated in Section 8.37 of the existing derivation volume and editable source. No new novelty claim is made.


## Two additional probe seeds completed and stopped

- Physics CPU job 11212673 completed. Fixed seeds 20261018/20261019 both reproduce resolved CL-clean/NCL-corrupted ordering on the same native networks. Clean differences +.0162/+.0151; sigma .12 differences -.0119333333/-.0115666667, with all four simultaneous conditional intervals excluding zero.
- Independent saved-record verification reproduces validation argmax/errors, TEST differences, all 2,000 bootstrap draws, intervals and decision. Protocol, weights, histories and raw outcomes are retained in outputs/probe_replication_v1.
- This is a post-outcome reliability check on reused TEST images and fixed backbone checkpoints, not a blinded boundary prediction or backbone-seed replication. Stop at two additional probes; do not search more seeds/noise points.
- Methods, outcomes, limits and plot are integrated in Section 8.38 of the derivations volume and its local editable source.


## Saved native decision accounting

- No new forwards or fitting. Exact clean-to-noisy error accounting reproduces the saved curve at every fixed level.
- At .12, clean deficit +1.6500 points, new-error difference -2.2667 and recovery contribution -0.6067 sum to -1.2233. Different clean populations make the unconditional loss difference insufficient by itself for conditional robustness.
- Among the same 4,502 images both classifiers get right clean, CL has lower sampled error at .04, but NCL has lower sampled error at .12. Their unconditional contributions are +1.6433 and -.7867 points. This is descriptive evidence that the native reversal also occurs within a common initially correct population, not a geometry attribution or boundary prediction.
- The standard exact identity and its derivation, numbers, limits and plot are integrated in Section 8.39. Stop this accounting at the saved fixed grid; no new subgroup search or significance claim.


## Matched-rank prevalence control and class-bias prerequisite

- Physics CPU job 11212722 completed. At one declared 7% selection budget, CL/NCL purity is .06608259/.08959360. Difference .02351101, conditional interval [.02009444,.02587170]. Independent selection/count/bootstrap verification passes.
- NCL has 127 zero cutoffs among 232 nondead coordinates. This is equal rank-selection count, not equal positive firing rates. It is a sensitivity control on a class proxy, not ground-truth monosemanticity or causal attribution. Stop at one budget.
- Saved-record common-drift check finds 12.095%/3.983% of affine residual energy in a common class-only shift for CL/NCL, below the declared 25% criterion. No global-bias calibration experiment is run. This does not prove calibration irrelevant.
- Outcomes and measurement definition are integrated in Section 8.40; the class-bias stopping decision is in Section 8.37. No new novelty claim or successful native boundary prediction.


## Single finite-response screen rejected

- No new forwards. Replacing the zero-noise derivative with the saved actual logit change at sigma .04, scaled linearly on the existing grid, predicts no ordering reversal. This post-outcome candidate fails its declared qualitative screen; no anchor or exponent search follows.
- Individual responses at the anchor agree by construction, not as evidence of a predictive law. Population prediction still uses the registered clean-baseline/increment construction.
- The approximation, its affine-ray assumption, failed points and stopping decision are added to Section 8.37. Original frozen prediction and native outcomes remain unchanged.
