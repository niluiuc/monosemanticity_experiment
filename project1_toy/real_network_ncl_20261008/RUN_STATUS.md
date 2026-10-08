# Native-network test: execution record

## Motivation

Project 1 asks when a representation that benefits clean performance becomes worse under corruption than a more monosemantic representation. Earlier two-feature compressors fitted to real activations did not test the original classifier's robustness. This bounded experiment instead evaluates the released CL and NCL ResNet18 networks with identical clean linear-probe procedures.

`PROTOCOL.md` fixes the scientific settings and stopping criteria before image scoring. Semantic consistency is a class-based proxy, not a measurement of every underlying concept or a causal isolation of monosemanticity.

## Infrastructure

- Scratch root: `/scratch/idas3/ncl_native_20261008_v1`.
- Both original checkpoint hashes were verified against the local downloaded copies.
- CIFAR-100 downloads directly into the scratch root.
- An isolated `runtime` environment avoids modifying the user's existing environments. Those older scratch environments were missing Python standard-library files.
- Slurm job `11211651`, partition `secondary`, account `adshead`, requests one RTX A6000, eight CPUs, 32 GB and two hours. Submitted 8 October 2026 at 01:07:43 cluster local time.
- Access uses the user's existing authenticated SSH control connection. Configured SSH keepalives send every 60 seconds; this cannot prevent an explicit server disconnect or a network outage. No credentials or new authentication keys are stored here.

## Current evidence

At submission, no image-result claim is available. The first decision is the clean prerequisite gate: both a positive NCL semantic-consistency difference and a positive NCL-minus-CL classification-error difference must have positive lower 95% bootstrap endpoints. If either fails, this checkpoint pair stops, with all outputs retained. Do not substitute projected features for backbone features after observing failure.

## Mathematics

The conditional decision-margin/Jacobian prediction and its approximation-error bound are included in Section 8.34 of the existing derivations PDF and editable `research_notes/volume2.tex`. The 117-page PDF compiled successfully; the newly added pages were visually checked. These are standard conditional calculations, not evidence that finite-noise prediction works or a standalone novelty claim.

## Reproduction

Run `run_clean_gate.py --root <scratch-root>` in the recorded Torch/torchvision environment with the named checkpoints in `checkpoints/`. The script downloads only the training dataset, writes seeded FIT/VALIDATION indices, features, final probes, validation logits, bootstrap draws, provenance and the gate decision under `clean_run_v1`. It refuses to overwrite that directory. The official test split is not loaded in this stage.

Later results and decisions will be appended here without rewriting unsuccessful findings.

- Scheduling adjustment while pending: shortened the requested limit to one hour and allowed any GPU type instead of specifically RTX A6000. This changes resource eligibility, not data, precision settings, models or statistical criteria. The actual allocated GPU is recorded by the experiment.
- The dataset archive is downloading directly from the official Toronto source, with the torchvision MD5 checked before its final filename is installed. This is file I/O only.
- `run_prediction.py` is prepared but not run. It refuses to proceed unless the saved clean decision passes. The relative residual uses class-centered logits, aggregated RMS residual divided by aggregated RMS actual logit increment. Centering removes an arbitrary common logit shift. This definition is fixed before validation noise scoring.
- Conditional Slurm job `11211781` depends on successful completion of clean job `11211651`. Its wrapper checks the saved scientific gate decisions, running no prediction after a failed clean gate and no TEST evaluation after a failed prediction gate. An execution-success exit code is not treated as a scientific-success decision.
- Automatic follow-up `finish-bounded-ncl-cluster-test` checks this thread every ten minutes. It stops after documented completion, a scientific stopping decision, lost SSH authentication, or 13:00 UTC on 8 October 2026. It must not resubmit duplicate experiments or widen scope. At the last check both jobs remained queued and the dataset archive download had reached 16 MB; no image results were available.
- User subsequently requested that this active session also remain watching, rather than relying on scheduled follow-up. `watch_cluster.py` now polls existing jobs and download/log progress every 30 seconds, appending observations to `watch_log.txt`; it never submits jobs or changes scientific settings.
- Dummy-input local CPU smoke check passed: strict CL backbone loading and `torch.func.jvp` return finite `(2,512)` outputs. The saved `infrastructure_smoke.json` states explicitly that this uses no research images and is not a GPU-runtime equivalence or robustness result.
- After roughly twenty minutes pending on priority, the same two jobs were made eligible for `secondary,scavenger`. No duplicate run was submitted. Automatic requeue was disabled because the experiment intentionally refuses to overwrite partial run directories; any preemption requires explicit preservation and an infrastructure-only retry. Nodes ccc0496–ccc0499 were excluded to avoid allocating newer RTX6000B hardware to the CUDA 12.4 runtime. Scientific settings remain frozen.
- GPU scheduling continued to block execution. Physics primary access and idle CPUs were verified. Slurm retained a stale GPU TRES after the attempted in-place conversion, so the still-unstarted job `11211651` was cancelled and replaced with CPU-only job **11212068**, using the exact same experiment script. The conditional job **11211781** now depends on `afterok:11212068`. The replacement started on `ccc0444` at approximately 01:33 Central time. At that point it was downloading data, with no model measurements available. The CPU run records its device and runtime; conditional uncertainty remains scoped to this particular fitted run.
- The running CPU job started a redundant full download while the earlier prefetch was already far ahead. To avoid waiting for that extra download, the download-only job `11212068` was cancelled. Before replacement, the code verified its run directory contained **only provenance.json**, with no features, probes, or results. Its provenance and incomplete downloaded archive were preserved in `clean_download_only_attempt_11212068`. Replacement CPU job **11212169** started on `ccc0444`; it waits for and MD5-verifies the already-running prefetch, then invokes the unchanged experiment script. Conditional job **11211781** now depends on **afterok:11212169**. These are the current job IDs. At 01:43 Central time the prefetch had reached approximately 116 MB; no scientific images had been scored.
- **Pre-outcome scientific amendment at 06:47:51 UTC (01:47:51 Central):** measurement of the already-fixed native TEST error curve is separated from validation of the affine predictor. Clean prerequisites still must pass. If prediction gates fail, its claim is rejected but the fixed native phenomenon test proceeds. This resolves the methodological issue of stopping the central phenomenon test merely because an explanatory approximation fails. No checkpoint, data, split, probe, corruption, sample-size or success-threshold changes were made. Before installation the remote guard verified `clean_run_v1` did not yet exist. Original protocol/code are preserved on scratch under `protocol_v1_before_amendment`; the original protocol is also saved locally as `PROTOCOL_v1_before_amendment.md`. `PRE_OUTCOME_AMENDMENT.json` records the timestamp, original hashes and zero scored images. The clean script remains unchanged and will record the amended protocol hash when it starts.
