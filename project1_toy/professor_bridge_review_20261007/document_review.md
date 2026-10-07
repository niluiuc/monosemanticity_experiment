# Mathematical document review

7 October 2026 UTC. Reviewed `research_notes/project1_covariance_applicability_20261007.tex`. No new experiment, fitting, numerical sweep or proof extension was performed.

## Verdict: mathematically and interpretively supported

- The constructive proof preserves encoder energy and the tied decoder. ReLU Lipschitzness bounds retained squared error by O(theta^2), including zero gates and either perturbation sign.
- Strictly positive omitted-feature mean and finite second moments justify the dropped-output L2 expansion through dominated convergence. The resulting linear coefficient is exactly -2 eta Cov(X1,X2).
- A feasible-path improvement suffices to exclude retention from the jointly optimized objective. The document correctly does not infer differentiability of the profiled loss.
- Exchanging coordinate roles gives the stated second-orientation exclusion; the importance factor and angular-versus-weak-amplitude sign convention are correct.
- Recorded covariance values, predicted slopes and grid secants match the reviewed diagnostic. Finite secants are explicitly identified as profiled finite-angle observations, not exact derivatives or population estimates.
- The high-noise calibrated result is correctly identified as already established in the existing arbitrary-load support-bound section. The frozen L2 scaling is derived with sufficient assumptions and has the correct importance-weighted coefficient.
- Population-optimal calibration is explicitly distinguished from finite calibration/test-split guarantees. The limit eta*(E X2)^2 is not asserted as a held-out limit for an empirically fitted omitted constant.
- Stopping an importance sweep for the unchanged saved pairs follows from the empirical obstruction. Neither the proof nor the generic high-noise crossing is presented as successful real critical-law transfer or a major novel contribution.

No mathematical correction is required. The current document preserves the specific unresolved research gap and does not authorize a replacement feature/noise hunt.

One future-use qualification, not a correction to this section: if an empirical follow-up ever applies the high-noise limit on held-out data with an omitted constant m fitted on calibration data, its corresponding difference is eta*(2*m*E_test[X2]-m^2), not eta*(E_test[X2])^2 unless m equals the test-population mean. The section already warns against silently replacing finite-split statements by the oracle limit.
