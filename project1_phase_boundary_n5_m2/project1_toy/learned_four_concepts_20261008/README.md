# Learned four-concept detection comparison

Read PROTOCOL.md for the registered question and settings, then REVIEW.md for interpretation and limitations.

From this directory, run `python run.py`, then `python verify.py`. The saved run is in run_v1. Preserve it before rerunning; do not overwrite the archived outcomes.

The experiment learns four binary concept directions in two dimensions with total encoder energy two. Reconstruction selects the geometry; fixed midpoint detectors measure concept-detection error under Gaussian code noise. All concepts, including omitted ones, count toward risk.

At activation probability 0.2, seeds 0 and 1 have clean summed error 0.16 versus mono's 0.40, with numerical crossings near noise standard deviation 0.2799. These encoders repeat two antipodal pairs; this is not a new arbitrary-load boundary. Seed 2 has no strict clean advantage. Seven of fifteen trainings pass the registered loss-stability diagnostic; eight fail and remain reported.

Independent state enumeration reproduces all 2265 risk values within 1.6e-15. Three fresh simulation checks agree. This verifies risk calculations, not globally optimal training or real-network transfer.

Outputs: results.json, independent_verification.json, risk_map.csv and learned_boundary.png under run_v1; each case retains training arrays, traces and risk arrays. Full derivation and results are in research_notes/volume2.tex, Section 8.42, compiled to research_notes/volume2.pdf. Updating output/pdf/Superposition_Recursive_Training_Derivations.pdf was blocked by that file being open in another process.

This bounded experiment is complete. The remaining load question requires a non-pair-block comparison, such as three or five concepts in two dimensions, retaining the same detection outcome and budget. No additional experiment is claimed here.
