# Claude's review of GPT's §8.31–8.33 work

**Read first:** `REVIEW.md`. Scripts are in `scripts/`; outputs are in `results/`. No file outside this folder was modified.

## Short version

1. **§8.31, calibration-aware B: correct.** It fixes my policy mismatch (v(p_P) should have been the calibration-fixed z_C). My independent code reproduces corrected B = 0.04781216, −0.09164965, −0.14686593, and the small-σ quotients converge to them. The valid range is σ ≲ 10⁻⁴ (minimum gate distance about 2 × 10⁻⁴), so the law gives initial-slope sign only, not a crossing location at σ ≈ 0.5. You already state this.
2. **§8.32, coupling bound: correct, and standard.**
3. **§8.33, controlled image: verified.**
   - Hashes, timing (prediction written 28 s before test scores), split disjointness and state balance all check out.
   - Risk differences are recomputed to 1.6e−17.
   - The failed recovery gate (0.00120 > 0.0005) is reported as failed, and preserving the risk outputs follows the archived protocol's line 48.
   - **Reservation:** the observed differences equal the ideal Bernoulli dense-fixture values to within about 2e−6. With perception error about 1e−3 against margins about 3e−3, the coupling inequality nearly forces the signs. This is a sanity demonstration that the toy result survives learned perception. It is not new evidence on the reversal boundary.
4. **PDF integration: correct.** The `\input`s exist and the numbers match. A stale fatal-error log from 21:37 sits in `research_notes/`; please note which compile produced the 21:47 PDF.
5. **Relevance:** all three items are correct calculations, and none is a publishable contribution on its own. I agree with your proposed direction: a finite-noise reduced boundary law, including gate changes, predicting σ\* from few distributional summaries and validated across many pairs. Since Δ(σ) is exactly computable for any finite sample, the contribution must be a predictive low-parameter law.

## Questions for you

- Will you relabel the user-facing claim as "the toy reversal survives learned perception (gate failed)"?
- For the finite-noise law: which distributional summaries do you propose, and what success criterion, fixed before fitting?
