# Independent GPT verification for Claude

Read this first, then README.md, results.json and followup_results.json. All review files are now in this separate folder at the user's request. Original `claude_agent` code, logs and saved results were not edited. An audit subdirectory initially created there was moved here. The existing research derivation volume was updated under the standing requirement to integrate mathematical corrections; the new section's editable fragment is `derivation_audit.tex` here.

## Blocking corrections before manuscript reuse

### 1. Signed critical coefficients

`analytic_A.py` defines epsilon=pc-p but takes `A_slope=-dc2_dp`. Correct is `A_slope=dc2_dp`: kappa(pc-epsilon)=-kappa_prime(pc)*epsilon+O(epsilon^2).

The saved `analytic_A.json` therefore has A=-.3454915028, K_pred=-1.5786893258, C_pred=-.2870182162. The existing positive K/C are correct; the claim that this signed derivation reproduces them is not.

For h=2 eta c p q, negative-c opposite-branch response is sqrt(-h/(3B)), not sqrt(h/(3B)). The positive coefficient .7344008871 is correct.

### 2. Encoder search misses a competing noisy minimum

Reproduced counterexample, same objective and original evaluator:

```text
p = .3641344889933496
c = 0
eta = .5
sigma = .003
theta_shared approximately -.02759960775549138
```

Original `fra2.solve` returns theta=0 and F_star=F_mono=.1157755274593992. The independently located sharing geometry improves loss by 1.26882326e-8. The original `fra2.F` evaluates that same geometry consistently with the independent Gaussian-moment evaluator. Thus the miss is in encoder search, not a mismatched loss convention. See original_solver_countercheck.json and results.json.

Independent local competing-well equality: epsilon=.008457112793593683 at sigma=.001, and .017781006480572594 at sigma=.003. Archived trained brackets are [.0084584879,.0084860982] and [.0178815223,.0179389539]. The first discrepancy is small; the second is resolved. Six 55-digit loss evaluations confirm the signs around both roots. The independent root search is not a formal global certificate; nevertheless the constructive feasible lower loss already disproves the original solver's claimed global optimum at the counterexample.

Suggested bounded repair: refine ALL candidate sharing wells, rather than only the winning coarse-grid/log-grid point. Recompute ONLY the existing transition checks first. Do not silently replace saved records or describe current brackets as verified.

### 3. Inferential claims

`real_stats.py` uses `set(rng.choice(..., replace=True))`. This drops multiplicities and creates a random induced subset, not the asserted standard cluster bootstrap. Coverage of those CI95 values is unestablished. Shared channels also require justification before interpreting independent-observation Fisher tests.

Native transfer: the loader concatenates train/calibration/test; outputs concern an empirical fitted compressor, not held-out or native ResNet robustness. Hidden activations and logits are from one network.

### 4. Certificate and scope labels

Archived certificate_v2 has 60 strictly signed ranges and four ranges straddling zero. A range containing zero does not prove exact mono selection. Three straddling ranges are consistent with the mono regime but should not be counted as separately proved exact optimizers from the branch certificate alone.

The floating-point slack hand estimate is not a directed-rounding enclosure. Independent agreement at four points supports the numerical calculation, not interval-proof rigour.

The shared-budget Hessian law is verified along the one-partner/equal-donor path. It is not yet a global/full-Hessian theorem for every multi-partner perturbation. Powell multiple starts do not certify global optima.

## Supported by independent checks

- Symbolic field, two clean stiffnesses and cubic coefficient.
- Exact full bias-piece enumeration: 20 saved comparisons agree to 4.17e-17; 100 sampled small-angle gate conditions passed.
- Four independently selected critical-response cases agree with leading predictions to .054-.375 percent.
- Fourteen 55-digit shared-budget path checks agree with predicted curvature to 1.36e-8, with all gate conditions valid.
- Four independent noise-smoothed curvatures support the first-order correction within 9.74e-6 at the tested settings. Uniform remainder/global claims remain separate.
- Complete pair/triple counts reproduce, including failed T2.
- Sixteen fresh expanded-range empirical bias fits reproduce saved pair/triple loss values to 1.12e-16. No inference rerun or full encoder search is claimed.
- Tied noisy-training gradient agrees with finite differences to 9.57e-9. Adam seed convergence has not been rerun.

## Research interpretation

The local phase-extension mathematics remains useful after correction. The noise-law exponent is not disproved by the missed-well bug. The current native-model robustness gap is still open. These checks do not establish novelty or conference acceptance. Do not treat negative/failure results as successes or use post-hoc explanations to overwrite registered failed predictions.

## Original files and reproduction

`verify.py` uses an independent implementation and writes only here. `resolve_noise_and_real.py` imports the original side-effect-free fra2 evaluator for the same-geometry comparison; its independent solver is separate. Reproduce commands are in README.md. Raw initial and follow-up outputs remain distinct. The review-location change did not modify reported scientific numbers.
