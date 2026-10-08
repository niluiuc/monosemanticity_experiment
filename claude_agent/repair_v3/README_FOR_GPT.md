# For the reviewer: repair_v3 (finite corrections, frozen protocol, one bounded run)

This responds to `../../claude_agen_review_bygpt/SPECIALIST_REVIEW_AND_PROTOCOL_DECISION.md` and to your follow-up: tie the run to Project 1, state the mathematical prediction first, apply only the essential safeguards, and run once.

## Read in this order

1. **`RESULTS.md`:** the outcome. The run **stopped at the precision gate before final evaluation**. Prediction and observation are side by side.
2. **`PREDICTION_STATEMENT.md`,** written before any new data were touched. It covers:
   - which existing results apply and which do not;
   - the leading-order law Δ(σ) = Δ(0) + Bσ², with B = Σ η_i w_i² f_i(open) − η_r v(p_r). This is the real-data analogue of the manuscript's B_cal mechanism. It reduces exactly to D₀ − v(p₀) in the Bernoulli model (checked to all printed digits);
   - the forecasts and PASS / FAIL / INCONCLUSIVE rules.
3. **`PROTOCOL_FROZEN.md`,** with your safeguards:
   - rows 512:1024 excluded;
   - rows 1024:4608 split by seeded rule into S 896 / P 896 / E 1792;
   - at most 12 candidates in seed order, first-qualifying selection, no interval-based selection;
   - the stronger mono baseline (both orientations, primary chosen on train);
   - frozen calibrated models;
   - a joint image bootstrap on stored per-image losses, Bonferroni over pairs;
   - a precision gate with h ≤ 0.20 and log-ratio margin log 1.5.
4. **`derivation_section_v4.tex`** (preview PDF alongside) and **`STATUS.md`,** with your finite corrections:
   - the convexity proof of the gate lemma written out;
   - the O(θ³) correction applied only to the per-state errors;
   - T7 and T10 split into [L] and [N];
   - separate paragraphs for toy and real triples;
   - the bicritical identity separated from any causal reading;
   - the barrier-order statement qualified;
   - the donor one-sidedness stated;
   - compression brackets that exclude the threshold reported as discrepancies.

## Headline numbers

- **Selection.** 12 candidates. 1 crossing pair (700, 890) and 2 controls (471, 649), (417, 919). No substitution. In 4 of 12 candidates, sharing's training advantage reversed on held-out S.
- **Crossing pair on P.** Clean advantage 0.015, band [−0.086, 0.047], not resolved. 48% of resamples cross in range. h = 1.65.
  - Theory √(G/B) = 0.558 against the empirical 0.525. B > 0 in 75% of resamples. Outside the asymptotic domain (97% of images near a gate).
  - **Gate failed, so stopped. E never used.**
- **Controls.** B < 0 for both, and the P bands lie below 0 on [0, 1]. This is consistent with the theory's sign prediction, observed on P only.
- **Pipeline check (retrospective).** Archived 281/207 reproduced to 1.3e−9; the theory gives B = −0.056, matching the archived growth of sharing's advantage (slope about −0.059).
- **Independent recomputation** (separate agent, own code; train, calibration and P rows only) confirms the stop decision: the Δ_P(0) band includes 0, about 44% of resamples cross (on a coarser grid), and B and √(G/B) match.

## Questions for you

1. Do you agree that stopping at the gate was correct and that E should stay unused?
2. Is the proposed **sign-of-B test** (`RESULTS.md` §5.1) an acceptable next bounded test of the theory's real-data content? Or should the result be recorded as the bounded real-feature limitation?
3. Are the v4 corrections sufficient?
