# Detection boundaries: direct extension and learned repair

## Motivation
The original lecture figure was generated entirely from exact risk formulas for two fixed codes. Its colours were not measured experimental outcomes. Directly extending that figure requires specifying a dictionary and computing the same detection risk, not solving a reconstruction-training problem first.

Two bounded protocols are kept separate: PROTOCOL.md fixes the three-seed detection-training repair; FIXED_GEOMETRY_PROTOCOL.md specifies the direct n5/m2 pentagon calculation. Both precede execution of their tests.

## Direct extension
Regular-pentagon dictionary, five binary concepts in two dimensions, total energy2, matched midpoint detectors; mono has two orthogonal unit columns and three constant-absence outputs. All five errors count.

At activation probability .2: sharing clean summed error .40352, mono .60000, numerical crossing .17108537. Heatmap colours count errors from independent random states and Gaussian noise; black contours are calculated from exact conditional-state risk. This establishes the boundary for the stated fixed geometry, not the best geometry or a trained real network.

## Learned repair
Start from all three archived five-concept p=.2 encoders. Optimise exact detection error at fixed training noise .02, rather than reconstruction. Unit-direction score thresholds are fitted too. Training-only comparison chooses fitted detector or constant absence/presence per concept, then freezes that output rule for evaluation. Parameterisation maintains energy2 and avoids dividing scores by tiny norms.

All three L-BFGS-B runs pass the prescribed solver-success and projected-gradient <=1e-5 check. Clean errors are .28/.32/.32 versus mono .6; detected crossings at p=.2 are .20269779/.18542321/.18409017. Seeds 0/2 choose one constant-absence output. The objective is smoothed by training noise and can have nearly flat local plateaus; local convergence is not global optimality. These repaired detector rules differ from the lecture's fixed midpoint rule.

The learned heatmaps vary evaluation frequency for encoders trained only at p=.2. They do not show encoders retrained at every frequency. No native-model-transfer or publication-novelty claim is made.

## Verification
Separate conditional-state calculations reproduce all 14400 formula-grid values to 2.67e-15. Forty-five simulation checkpoints are independently replayed. Colour grids use 20000 random states/noise per frequency, with paired differences and saved standard errors. Raw draws are retained. Cell correlations prevent treating the grid as independent statistical replications.

For the original and learned grids, 99.94% of 12000 cells are within three cellwise standard errors; the maximum standardised discrepancy is 3.53. Pentagon grid: 99.21%, maximum3.21. Agreement tests exact risk computation; it does not independently predict learned geometry.

## Reproduce
Install NumPy, SciPy and Matplotlib. Run `python run.py`, then `python fixed_geometry.py`, then `python verify.py`. run.py refuses to overwrite run_v1; preserve this archived run and change the output directory for an authorised replication. Starting encoders are read from learned_five_concepts_20261008/run_v1. Constants, bounds, seeds and optimiser settings are explicit in scripts and protocols.

run_v1 contains raw draws, final models/thresholds/output choices, optimiser traces, results.json, fixed_pentagon_results.json, verification.json and all heatmap arrays/images. Full derivations and assumptions are in research_notes/volume2.tex Section8.44 and output/pdf/Superposition_Recursive_Training_Derivations.pdf.

## Review and stopping
The fixed-geometry extension preserves the pictured comparison. The learned repair addresses the mismatch and decoder problem with a disclosed change to detection training at small positive noise. The solver's numerical check passes, but flat local plateaus limit interpretation. At p>.5, omitted-concept absence is not the best constant prior predictor. No geometry or seed search was added. These registered tests are complete.
