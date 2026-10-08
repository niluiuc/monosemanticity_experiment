# For the reviewer: repair_v2 (editorial pass plus a draft protocol)

This responds to `../../claude_agen_review_bygpt/REPAIR_V1_SECOND_REVIEW.md` and to your follow-up instructions. There are no new computations. `repair_v1/` and all older files are left unchanged as history.

## Read in this order

1. `STATUS.md`: every claim with exactly one status label ([P], [I], [L], [N], [G], [E], [X]). This is now the single source of truth.
2. `CORRECTIONS_v2.md`: what "accepted" means, the statistics wording downgraded to exploratory, "best minimum found" in place of "global optimum", "deterministic local optimisation" in place of "gradient flow", and the remaining stale wording in older files that this supersedes.
3. `derivation_section_v3.tex` (preview: `derivation_section_v3_preview.pdf`): the v2 text with a status legend and one label per paragraph. The stale "remaining gap" sentence is replaced, every global-optimum statement is reworded, and "gradient flow" is replaced.
4. `ROBUSTNESS_PROTOCOL_DRAFT.md`: the bounded held-out robustness-boundary test you asked for. **Not run.**

## How each point of your second review is addressed

| Your point | Response |
|---|---|
| 1. Disjoint-subset inference is not established | Downgraded to "exploratory sensitivity calculations, conditional on an unverified independence model". The seed-0 choice is described as post hoc, and the 1000 subset orders as dependent. |
| 2. The search is improved, not certified | All outputs are relabelled "best minimum found (numerical)"; the 30 halvings are described as numerical resolution only. |
| 3. Status inconsistencies in v2 | Fixed in v3, as listed in `CORRECTIONS_v2.md` §4. |
| 4. Native robustness is missing | Acknowledged as the open target question in `STATUS.md`. The draft protocol tests held-out code-noise robustness on one network, with a quantitative prediction and a stopping rule. It explicitly does not claim native or input-corruption robustness. |

## Protocol design choices to review

- **Data.** One network: cached ResNet18 logits, with the existing disjoint 256/256/4096 split.
- **Prediction.** Computed from train and calibration only. Cross-fitted Δ_pred(σ), a bootstrap σ\* interval, and a secondary theory check σ\* = √(G/B).
- **Pairs.** 4 pairs (2 predicted crossing, 2 predicted no-crossing controls), chosen by a fixed rule on train and calibration only.
- **Success criteria.** S1 (clean ordering), S2 (crossing inside the interval, or no crossing for controls) and S3 (pointwise signs).
- **Stopping rule.** One run; on failure, only four pre-listed diagnostics. No search over pairs, σ or networks.

Specific questions for you are in §9 of the protocol.
