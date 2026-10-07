# Professor manuscript review

6 October2026. Reviewed `manuscript.md` against the existing importance/endpoint proofs, archived endpoint outputs, vision results and contribution hierarchy. No manuscript, central source, proof or experiment was edited.

## Verdict

The skeleton preserves the original phase-boundary question and accurately separates its broader organizing scope from the proved two-feature class. The global clean selector, cubic gain, critical corrupted-risk boundary and policy-dependent endpoint appear in the right dependency order. I found no numerical contradiction in the displayed endpoint or vision findings. It does not overclaim an actual held-out vision winner, reversal, critical exponent, semantic association or arbitrary-load result.

The following are indispensable qualifications/additions before this becomes reviewer-ready; they are not optional stylistic polishing.

## Required corrections/clarifications

1. **State the numerical-enclosure qualification directly in Section5.** The table calls the calibrated intervals “enclosures,” but the saved computations use70-digit arithmetic with declared slack, not directed-rounding interval arithmetic. Add that these are numerical global-loss bounds independently recomputed at90 digits, with no formal machine-rounding certificate. The mathematical branch-and-bound lower/upper arguments are valid in exact arithmetic; the archived numerical implementation is audited evidence rather than a rigorous computer-assisted proof. This distinction should not be recoverable only from the98-page companion.
2. **Define the vision frozen baseline explicitly in Sections3/6.** The abstract policy definition says frozen uses clean-optimal biases. In the actual pilot, the primary frozen biases were zero-noise fits on the **calibration split**, not the clean-training biases; noisy policies refit on that same split. This makes the two primary policies coincide at sigma0 and avoids ordinary training/calibration mismatch masquerading as a noise-policy effect. The displayed .3792952/.3702662 risks belong to this primary baseline. Clean-training-bias risks are separate archived secondary measurements. An explicit sentence is necessary to reproduce and interpret the numerical comparison.
3. **Put the exact central coefficients in the actual theorem statement.** The skeleton currently sends K_eta,C_eta and B_j to the companion. The submission must display them, together with q0,D0 and the mono calibration minimization v(p0). Otherwise the main claim reduces to a familiar abstract cubic-versus-quadratic balance, and a reviewer cannot assess the claimed parameter-dependent prediction. This adds no new mathematics: use the already proved expressions and domain. An explicit stationary cubic/proof appendix reference must accompany the globally selected branch.

## Checks that pass and must remain

- Model width, encoder/decoder energy and absolute code-noise matching are transparent; per-output noise redistribution is disclosed rather than hidden as generic equal capacity.
- Mono may retain either coordinate, its omitted feature is a constant predictor with its loss included, and richer untied/correlation-aware readouts are expressly outside comparator coverage.
- The storage threshold and corrupted-risk crossing are distinct; equality above the threshold is not misrepresented as a noisy reversal.
- The family theorem is restricted to eta∈[.48,.52], p∈[.35,.42]; the endpoint has its separately proved strip. Calibration does not silently expand either domain.
- An asymptotic crossing/sign bracket is not promoted to a unique complete all-noise phase diagram. Ambiguous numerical bisections and the nonstationary larger toy remain visible.
- Endpoint eta2/3 is called a special cancellation. The same fixed encoder/noise/task comparison under symmetric policy rights is correctly stated; its special character is not hidden as universal robustness.
- Vision geometry is numerically selected and same-sign, and its training advantage does not give a held-out advantage. All individual difference intervals includezero. The positive paired policy contrast is presented as a different estimand with pointwise conditional bootstrap limits.
- Saved zero/positive decomposition is explicitly observational. Positive-target calibration harms are retained; no new subgroup significance/causal claim is invented.
- The semantic follow-up is pending eligibility rather than asserted as completed evidence. Do not alter this before the prospective gate resolves.

## Paper-critical critique, not a request for more toy work

The theory's genuine value must be the globally selected, parameter-dependent phase construction, not the number3/2 itself or a familiar qualitative mono/noisy reversal. The endpoint sharpens that construction but does not replace it. The semantic-linked real-model test is the indispensable next empirical step if the intended framing promises concept-level monosemanticity; the current arbitrary-channel pilot alone cannot close that gap.

The related-work comparison is unusually explicit about inherited components and the residual analytical-notebook gap. Preserve its modest “candidate increment” wording until the exact audit and semantic-resource decision are complete. Proof correctness and this audited toy-plus-channel story do not establish main-track significance. Assemble and evaluate the resulting evidence rather than compensating with optional toy families or broader novelty language.

After the three clarifications above, the skeleton is suitable as a faithful working paper assembly. It is not yet a submission-ready empirical/theoretical contribution statement with resolved semantic evidence.
