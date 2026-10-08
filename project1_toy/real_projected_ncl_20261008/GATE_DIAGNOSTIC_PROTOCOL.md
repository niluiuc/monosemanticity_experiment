# One-point gate diagnostic (post-outcome)

Question: does permitting the native projector gates to switch resolve the failed finite-noise affine classifier approximation, or does the upstream CNN require nonlinear treatment?

Connection to Project 1: a predictive robustness boundary needs a finite-noise mechanism. The prospective all-gates-frozen approximation failed at sigma 0.04. This diagnostic isolates a specific proposed correction, rather than searching representations or fitting the observed crossing.

Smallest test: the same predetermined 500 validation images, 32 paired Gaussian directions, seed 20261010, and only sigma 0.04. Compare the actual native network, the full affine classifier, and an affine backbone followed by the exact frozen nonlinear projector and probe. No TEST images, new checkpoints, probe training, or corruption-grid expansion.

Criterion fixed before this diagnostic: the backbone-affine/nonlinear-projector approximation must meet both existing thresholds for both models: absolute classification-error discrepancy <= 0.02 and centered-logit relative RMS residual <= 0.25. If either model fails, stop projection-only repairs. A pass would justify further gate-aware analysis, not retrospectively rescue the failed prospective prediction.

All logits are saved for independent recomputation. This protocol is registered after the native test was examined: it is explicitly a post-outcome diagnostic, not confirmatory prediction evidence. Earlier predictions and outcomes remain unchanged.
