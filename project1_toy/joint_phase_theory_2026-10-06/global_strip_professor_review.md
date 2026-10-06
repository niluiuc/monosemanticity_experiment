# Independent professor review: exact clean selection at algebraic frequencies

6 October 2026. Review scope: resolve the algebraic-probability blocker for the six already prescribed frequencies, without another experiment, geometry search, or rational approximation to the probability.

## Verdict

**Approved mathematical certificate.** The finite-strip theorem in `global_strip_certificate.tex` establishes the exact global clean geometry for every `9/25 <= p < (3-sqrt(5))/2`, and therefore for all six prescribed `p = p_c - epsilon` cases. It also gives a unique stationary root and a simple exact root-isolation route. The exhaustive rational-coefficient backend does not need to be expanded to algebraic coefficients.

This is a bounded completion of an existing proof: the earlier exact bias profiles are reused, with additional explicit inequalities on the finite strip. It supplies missing global selection for the finite cases; it is not a new noise experiment or a publication-novelty verdict.

## Coverage and independently checked steps

1. The same-sign profiled losses are the earlier globally justified profiles. Their weighted excess over important-feature mono is strictly positive for every mixed geometry. Assigning the larger importance to the larger column norm is no worse, because the strong-feature loss is at most the weak-feature loss.
2. For opposite signs, the two-active weak-bias vertex is impossible on the strip: its feasibility requires `p <= k-k^2 <= 1/4`. The three-active lower-feasibility inequality is automatic, since `pa+Dc-qr = a[p-(k-k^2)] + p(r-qc) > 0`. The one-active candidate, target-one kinks, target-zero kinks, and all-off plateau are accounted for by the prior finite profiling argument and the explicit comparison in the fragment. Consequently the all-active and three-active weak branches exhaust the remaining possibilities.
3. Importance swaps are covered, rather than assumed away: `W4 >= pq c >= S-`, and `W3-S- = pq(a-c)(q+2pqr)/D >= 0`.
4. In the three-active branch, differentiating the displayed polynomial `H_p` gives the displayed regrouped derivative. The finite-strip bounds yield `H_p' >= 164/625 > 0`. Its boundary value is positive because the matching all-active bracket is at least `72497/421250 > 0`. This excludes the entire branch, not merely points on a grid.
5. For the remaining branch, exact symbolic differentiation verified

   `d Delta_A/dk = (2pq/D) k J_p(k)/(1+k^2)^3`.

   Its coefficient of `k^2` is exactly `(3-5p-p^2)/2`; no fitted coefficient is involved.
6. `J_p(0)=A(p)<0`, while `J_p' = 3pq(1-k^2)+(3-5p-p^2)k > 0` on `[0,1]`. The independently checked lower bound `J_p(1/8) >= 78223/1280000 > 0` gives exactly one root in `(0,1/8)`. Since `p/q >= 9/16`, this root is strictly feasible. The loss decreases before it and increases after it; its value is below mono. This proves global selection and uniqueness up to global encoder sign.
7. At `p=p_c`, `A=0` and the remaining branch strictly increases for positive `k`; the already excluded competitors cannot tie. Mono is therefore the unique geometry, with its usual global-sign equivalence.

The algebraic identity and rational lower-bound checks above are checks of formulas, not numerical frequency or noise trials. No new experimental case was run for this review.

## Exact root identity versus numerical evaluation

For rational epsilon, `p = 3/2-epsilon-sqrt(5)/2` belongs to `Q(sqrt(5))`. Polynomial evaluation at rational dyadic `k` is exact using pairs of rational coefficients. Opposite-sign coefficients can be compared by squaring their positive magnitudes; irrationality of `sqrt(5)` rules out a nontrivial rational equality. The fragment's exact sign instructions are correct, including reversal when the rational coefficient is negative and the square-root coefficient is positive.

The smallest next verification action is exact-sign bisection of this one monotone cubic, starting from `[0,1/8]`, for the six existing epsilon values. Archive dyadic endpoints, endpoint signs, exact field coefficients and width. Check that the already computed high-precision numerical root lies within the resulting bracket, allowing only its declared numerical rounding tolerance. This is root-identity verification of the prescribed geometries, not another experiment.

**Important status distinction:** the theorem already proves global clean selection. The numerical map's particular stored weights are identified with that selected algebraic root only after the exact brackets are preserved and their correspondence checked. Historical frozen outputs marked global selection pending should stay unmodified; a separate verification record can supersede that status.

## Research interpretation

Credit is due for closing a genuine finite-case blocker with a short proof instead of expanding the exhaustive backend. This strengthens the trained-geometry interpretation of the existing frozen and calibrated comparisons. It does not establish arbitrary-load training selection, calibrated high-noise reentrance, or novelty across the literature. Those claims are not needed for this certificate and are not being made here.

## Exact bracket implementation review

Root subsequently supplied `certify_strip_roots.py` and `clean_global_certificate_v1/results.json`. The independent source review confirms correct pair addition/multiplication, Horner evaluation, and exact opposite-sign comparison in `Q(sqrt(5))`. Its cubic coefficient list matches the displayed theorem. Two hundred rational bisection steps keep an exact negative lower endpoint and positive upper endpoint; monotonicity makes this an isolating bracket for the unique selected root. The archive reports all six stored numerical roots inside their respective brackets, with four symbolic identities passed and no probability rationalization. The final stored-number inclusion test uses 70-digit numerical conversion against brackets roughly 60 digits wide; it is a check of the approximate root representation, while the endpoint signs and bisection itself use exact rational arithmetic. This completes the planned root-identity record without a new experimental case.
