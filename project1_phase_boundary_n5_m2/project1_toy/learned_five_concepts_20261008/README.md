# Five concepts in two dimensions

## Question
Does the lecture's concept-detection advantage of sharing reverse under Gaussian code corruption when five directions are learned in two dimensions? The registered settings are in PROTOCOL.md. All concept errors, including omitted ones, count. Reconstruction trains geometry; fixed midpoint detectors evaluate it.

## Results
All 15 final iterates are saved. Only the three p=.10 runs pass the loss-stability check. They have four substantial columns and one very small column. Their numerical crossings are 3.1531e-7, 5.4746e-7 and 6.7183e-5, associated with almost sacrificing a concept. They do not show a robust five-concept storage mechanism.

At p=.20, seeds 0 and 1 have clean gaps -0.25408 and -0.28, and crossings .03271669 and .18002500. Both fail loss stability. Other final encoders give different results; none is hidden or discarded. This run does not establish a reliable learned five-concept phase boundary.

Independent state-loop calculation agrees with all 2265 risk values to 3.11e-15; both controls and three fresh simulation checks pass. Calculation verification does not certify optimizer convergence, global optimality, novelty or real-model transfer. At p>.5 the omitted-concept absence baseline is worse than the best constant-prior decision.

## Reproduction and records
From this folder, use `python run.py` then `python verify.py`. The runner refuses to overwrite run_v1; preserve the original results and use a separately named output for any authorized replication. No additional settings or retries were performed.

run_v1 contains settings.json, results.json, independent_verification.json, risk_map.csv, learned_boundary.png, raw simulation draws and per-case training/risk arrays. source_snapshot retains the registered runner and training dependencies. The verifier separately enumerates conditional states and refines roots only within detected sign brackets; it does not certify root absence.

Full assumptions, formulas and all outcomes are in research_notes/volume2.tex, Section 8.43, and its compiled PDF.

## Review and stopping decision
The experiment retains the intended risk and budget. Its useful finding is a specific training blocker: stable four-concept pair blocks are easier to obtain than stable storage of five concepts. A loss-stability pass is not a global-optimum certificate. Low-frequency tiny-column roots are real numerical roots for the saved finite encoder, but should not be portrayed as a strong additional boundary. The registered run is complete; do not expand it by fishing for favorable seeds or additional loads.
