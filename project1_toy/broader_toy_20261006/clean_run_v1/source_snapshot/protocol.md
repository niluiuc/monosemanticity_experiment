# Prescribed broader support-bound test: clean training stage

Recorded before execution, 6 October 2026. This is the next fixed deliverable in `joint_phase_theory_2026-10-06/week_plan.md`.

## Question and Project 1 connection

Does the arbitrary-load, fixed-geometry support penalty give a usable calibrated-noise comparison for clean-trained representations beyond the two-feature example? The immediate stage produces the five prescribed dictionaries and their clean risks, support penalty P, and bound constant Q. The mathematical support theorem concerns each fixed dictionary, not its global training optimality. The later noise comparisons will test its quantitative usefulness with symmetric bias calibration.

## Smallest useful test and fixed settings

- Independent Bernoulli concepts: n=8, m=4, common p=0.2; enumerate all 256 population states.
- Importance I_i=2^(-i/4), indices i=0,...,7; encoder Frobenius energy 4.
- Tied ReLU reconstruction, free biases; exact population importance-weighted sum MSE.
- Seeds 0,...,4; retain each final iterate and any failure. Exactly 5,000 projected-Adam steps; no best-checkpoint selection.
- Reuse `focused_bridge_2026-10-06/toy/bridge_math.py` and its original `toy_math_snapshot.py` without modifying their optimizer. Existing learning rate 0.01, beta1 0.9, beta2 0.999, epsilon 1e-8, ReLU derivative zero at the kink, projection after every update.
- Save all 5,001 loss/energy/tangent-gradient/bias-gradient records per successful run, 100-step checkpoints, final parameters and optimizer state. Loss-stability diagnostic uses the existing last two 100-step mean windows and tolerance 1e-5; passing is not stationarity or global optimality.
- Mono retains indices 0,...,3 with orthogonal unit columns (same energy 4), and predicts p for omitted features. Report both raw trained clean MSE and fixed-geometry clean-bias-profiled MSE; do not replace an unfavorable raw training result silently.
- P is the difference of support-weighted squared prior means between sharing and mono. Q is `(4/(3 sqrt(2pi))) sum_stored I_i E[X_i^3]/||w_i||`. In this Bernoulli case E[X_i^3]=p. Use actual nonzero columns; no post-training threshold that turns a small column into a dropped concept.

## Prechecks and records

Archive protocol, exact settings, reused source and environment before training. Check weighted tied gradients by centered finite differences on one declared deterministic eight-feature test point away from kinks, verify population normalization and mono clean loss, and preserve failures if a check does not pass. This check does not adjust experimental parameters.

All files belong to this isolated directory. Original scripts/runs and plan.md remain unchanged. Save code, source snapshots, hashes, full raw traces/checkpoints, five output dictionaries, P/Q, clean comparisons and numerical diagnostics.

## Stop / extend decision

Stop after the five prescribed fixed-step trainings and clean evaluation. No additional seeds, frequencies, optimizer repair/search or training extension. A poor clean result, non-small gradient, incomplete loss stability, tiny column, or very large Q/P is a reported limitation. The subsequent prescribed calibration at sigma=0, Q/P, 2Q/P may run only after root reviews method and runtime budget; this stage does not launch it. No nonbinary amplitude or real-model test is included here.
