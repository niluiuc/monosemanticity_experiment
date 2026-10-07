# Professor pre-execution review: four importance-family geometries

6 October 2026. Reviewed `importance_validation_protocol.md`, `run_importance_validation.py`, the reused Gaussian moment and previously reviewed calibration code, and the full uniform proof in `importance_interval_derivation.tex`. No scientific validation case was executed in this review.

## Verdict

**Approved for the prescribed four geometries and eight calibrated comparisons.** The probability/importance settings are inside the proved rectangle, globally selected clean geometry is justified, and the numerical policies and gap allocation are consistent. No broad scan, fitting, optimizer change or second larger-toy repair is involved.

## Mathematical checks

Fresh symbolic checks verified: the all-active weighted loss identity; the full three-active quartic numerator; the stationarity cubic derivative; and the regrouped three-active derivative. Their differences simplify to zero. The explicit rational lower bounds are `29/2500` for the excluded-branch derivative, `9417/68125` for its positive matching bracket, and `42399/1280000` for the root-bracketing cubic endpoint. These establish global branch selection on the declared rectangle rather than merely local stationarity.

pc(eta) lies strictly between .36 and .4 on eta=.48--.52. Subtracting epsilon=.005 or .001 therefore keeps p within .35--.42. The constants K, C, frozen B and calibrated B agree with the independently derived uniform formulas. The imported `model.geometry` is valid here because importance changes the choice of W, but a positive scalar importance does not change a feature's fixed-W clean-optimal bias. Both outputs use the correct general importance weights during risk evaluation.

## Exact field and numerical code checks

The exact arithmetic uses rational pairs in `Q(sqrt(rad))`, with positive nonsquare radicands at both prescribed eta values. Its multiplication, signs, Horner ordering and two hundred dyadic bisections are correct. The exact probability pair is pc(eta)-epsilon without rationalizing pc. The stored midpoint approximates the one globally isolated root; endpoint signs and field coefficients are archived.

The formula `2 eta/[1+eta+sqrt(rad)]` is algebraically the same critical probability and avoids unnecessary cancellation in numerical evaluation. The numerical/exact probability consistency test is appropriate at seventy digits. The frozen risk evaluator uses importance `(1,eta)` and identical mono/share outcome and noise. Missing frozen brackets remain recorded, and successful ones alone are bisected with the fixed iteration/relative-width limits.

For calibration, each feature target gap is total/(1+eta), so the weighted model gap meets its declared total target. Both models receive the same scalar calibration class, precision, slack and budget. Thirty-two feature ledgers are retained for the eight comparisons, including eight exact mono dropped-column objectives. Unresolved expansion/gap cases remain visible in model flags and difference intervals. A sign supported by a still-valid wider numerical interval should not be mistaken for meeting the requested loss-gap precision.

Sources, proof, protocol and review are snapshotted before computation; the output contains the exact geometry settings and complete calibration ledgers, then a manifest. Root should independently audit the resulting ledgers and weighted intervals before numerical claims are integrated.

## Scope and finite-failure rule

This is a focused implementation/finite-validation check of a mathematical family theorem. The derived exponent is not fitted from four points. A predicted asymptotic endpoint bracket may fail at a finite epsilon and must not be rescued with unplanned points. High-precision numerical calibration gaps remain distinct from rigorous directed-rounding interval proofs. No novelty or acceptance guarantee is attached.
