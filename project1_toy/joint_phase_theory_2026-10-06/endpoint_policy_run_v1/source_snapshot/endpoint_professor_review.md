# Professor review: endpoint policy comparison

6 October 2026. Review before endpoint noise comparisons. No experiment was run by this reviewer.

## Specific paper-critical gap and resolution

The existing positive frozen coefficient goes to zero at importance 2/3. Extrapolating a finite frozen critical constant to this endpoint would be wrong. The smallest necessary resolution is to prove global clean selection there and compare the same encoder under frozen versus symmetrically calibrated biases, with the same corruption and weighted MSE. The new full derivation is `endpoint_calibration_derivation.tex`.

## Proof review

- Complete geometry coverage: one-dimensional encoder energy fixes ordered squared norms a,c; global sign is irrelevant; both relative sign sectors and importance assignments are considered. Scalar free biases use the existing complete activation-interval proof, including kink closures and all-off plateau. For p>1/4, weak two-active candidates are impossible. Weak all-active and three-active profiles exhaust the remaining minima; assigning larger importance to the stronger column is optimal by explicit loss ordering.
- At p=1/2, eta=2/3, both mixed sign sectors have strictly positive excess cr/6. Important-feature mono is unique, modulo global encoder sign; the reversed mono orientation is worse. Compactness and continuity exclude a hidden remote minimizing branch near this endpoint.
- Stronger than asymptotic localization: global opposite-sign selection is proved for the full finite strip .495<=p<.5. The three-active weak sector has positive excess via monotonicity and its positive matching value. The all-active cubic is strictly monotone and has one root in (0,1/8). Any negative same-sign competitor has k<.668 epsilon and excess greater than -.05 epsilon^3, whereas the feasible opposite geometry k=epsilon has excess less than -.16 epsilon^3. Thus same signs cannot beat the opposite minimum in either numerical case.
- Critical expansion: opposite amplitude 4epsilon/3 and clean gain 16epsilon^3/81; same-sign local amplitude 4epsilon/9 and gain16epsilon^3/2187. Their ratio27 follows from exact branch expansions, but branch comparison is not used alone to claim global optimality.
- Frozen noise: selected strong gates remain order epsilon away from zero, much larger than sigma=t epsilon^1.5. Sharing variance coefficient tends3/4, equal to frozen mono. Therefore normalized frozen excess tends -16/81 for each fixed finite t. No all-noise sign or new frozen exponent is asserted.
- Global calibration: coercive/right and separated far-left bias losses localize global minima; uniform convergence localizes them near unique limiting biases. Strong convexity plus centered-noise variance bound gives displacement O(sigma)=o(epsilon), which preserves the selected sharing gate branch and its coefficient. Mono instead has a gate exactly at zero and optimally shifts bias at order sigma. Its global coefficient v(.5) is supplied by a strictly convex scalar limiting objective. Calibrated excess tends -16/81+[.75-v(.5)]t^2. This is an evaluation-policy dependence theorem within the task, not an attacker/safety theorem.

## Pre-execution numerical review

`endpoint_policy_protocol.md` and `run_endpoint_policy.py` are approved for the two fixed epsilons .005 and .001 only, at sigma=2tc epsilon^1.5. The exact rational cubic root brackets use the correct eta2/3 coefficients, preserve endpoint rational signs after200 bisections, and lie on the globally proved branch. `model.geometry` uses eta-independent optimal scalar biases, correctly applicable here. `risk` passes eta explicitly rather than inheriting importance1/2. Both decoders get the same independent Gaussian code-noise scale. Both receive free global scalar bias calibration with encoders fixed. Feature tolerance total/(1+eta) makes each model's weighted gap no larger than the predeclared total target. The script preserves four ledgers per case, all comparisons, settings, snapshots and hashes; no scan or parameter adaptation occurs.

The script reports a finite positive calibrated sign from lower/upper bounds and the frozen population difference. These are high-precision calculations using declared slack, not directed-rounding guarantees. If an individual ledger were unresolved, a sign interval could still legitimately certify the ordering, but resolution flags must remain visible. If a sign fails, stop and report it without extending settings.

## Stopping decision

Run exactly the two declared cases, independently audit the saved ledgers and population formulas, integrate the theorem and raw outcomes in the existing PDF, then stop endpoint numerical work. The family and endpoint clarify one critical mechanism and its scope; they do not justify collecting optional special cases or claiming broad trained-model transfer is solved. Novelty must be assessed separately against the primary literature.
