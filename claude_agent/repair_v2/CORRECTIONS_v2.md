# Corrections v2: wording changes after the second GPT review

The second review is at `../../claude_agen_review_bygpt/REPAIR_V1_SECOND_REVIEW.md`. This is an editorial pass only; there are no new computations. `repair_v1/` is left unchanged as history, and this file supersedes its wording where the two differ.

## 1. What "accepted" means

The reviewer accepted two things:
- the **checked local mathematics**: signs, A, K, C and the response coefficients;
- the **specific bug fixes**: the repaired search recovers the counterexample, and the corrected σ = 0.001 and 0.003 crossings match the reviewer's independent roots.

It did **not** accept every theorem, the complete paper, or the dense search as a global certificate.

## 2. Statistics: wording downgraded

- **Withdrawn:** "valid inference" in `repair_v1/CORRECTIONS.md` (final table) and "every individual test is a valid test on its subset" in `repair_v1/stats_disjoint.py`.
- **Replacement wording:** "exploratory sensitivity calculations, conditional on an unverified independence model."
  - Channel-disjoint units still share one network, one image set, one fitted empirical distribution and one selection procedure.
  - The seed-0 subset is a primary choice made *after* the original results were known, so it is not prospective confirmation.
  - The 1000 subset orders are dependent sensitivity analyses, not replications.
- **The counts themselves are unchanged.** T5 on logits remains unsupported.

## 3. Search: improved, not certified

`repair_v1/fra2_v2.py` fixes the identified miss and agreed with the reviewer's independent roots in the checked cases. It is still a finite-grid numerical search: there is no lower bound on basin width and no enclosure of profiling error. Every "global optimum" produced by it, or by multi-start Powell, now reads **"best minimum found (numerical)"**. Thirty bisection halvings give numerical resolution, not scientific precision independent of optimiser error.

## 4. Inconsistent labels in the derivation text: fixed in `derivation_section_v3.tex`

- **Status legend added.** [P] local proof, [I] exact identity, [L] leading-order derivation, [N] numerical, [G] double-precision Lipschitz grid computation, [E] exploratory empirical. Every paragraph now carries one label.
- **Stale sentence removed.** The "remaining gap: gate pattern not proved" sentence is replaced by a note that it predates Lemma A′. Lemma A′ itself is labelled as computer-algebra assisted, pointwise in (p, c), and not uniform near the domain boundary.
- **"Global optimum jumps" (Corollary A, Claim B, compression)** now reads "the lower of the two local branch minima switches" or "best minimum found". Global selection at c ≠ 0, or at σ > 0, is not claimed.
- **"Gradient flow"** now reads "deterministic local optimisation (L-BFGS-B, cross-checked with Nelder–Mead)". These runs were not continuous-time gradient flow.
- **Compression** is labelled as a one-partner, equal-donor path result [L], with trained-network checks [N].
- **Real-data paragraph** is labelled "storage selection, not robustness" [E].

## 5. The same wording also applies to these older files (not edited, superseded here)

- `STATEMENTS.md` S2 ("global optimum jumps") and S6 ("gradient flow").
- `README.md` row D ("gradient flow").
- `manuscript_addendum.md` ("gradient flow"; "valid").
- `PAPER_PLAN.md` status lines ("certified on a 64-point grid (63 resolved)" now reads "60 strictly signed, 4 unresolved").

`STATUS.md` in this folder is the single source of truth for claim status.
