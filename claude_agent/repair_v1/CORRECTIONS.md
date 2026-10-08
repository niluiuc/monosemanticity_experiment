# Corrections to claude_agent after the independent GPT audit

The audit is at `../../claude_agen_review_bygpt/`. All four blocking points were accepted. The original files are kept unchanged as history; this file and `repair_v1/` supersede them wherever the two disagree.

## 1. Signed critical coefficients (R1): fixed

- **Error.** `analytic_A.py` used A = −dκ₋/dp. With ε = p_c − p the correct choice is **A = +dκ₋/dp|_{p_c} = (5 − √5)/8 = 0.3454915**. The saved `results/analytic_A.json` therefore lists negative A, K_pred and C_pred.
- **Corrected** (`repair_v1/results/analytic_A_signed.json`): A > 0, K = 2A/(3B) = 1.5786893, C = 4A³/(27B²) = 0.2870182. These match the existing theorem to 1e−16.
- **Negative-c critical response.** For c < 0, h = 2ηcpq < 0, so k\* = **√(−h/(3B))**, not √(h/(3B)). The coefficient 0.7344009·√|c| was already correct.
- **Unchanged:** the positive response 4.2360680·c and the first-order line c\* = 0.8664195·ε².
- **LaTeX:** both fixes are in `repair_v1/derivation_section_v2.tex`.

## 2. Missed noisy sharing wells (R2): fixed and every affected number recomputed

- **Cause.** `fra2.solve` searched small angles on a grid with about 28% relative spacing. A narrow, shallow noisy well (width ≈ 0.006 at θ ≈ −0.028, depth ≈ 1e−8, σ = 0.003) fell between grid points, so mono was returned.
- **Repair.** `repair_v1/fra2_v2.py` uses a dense grid (1.8% spacing) with near-exact bias profiling and refines *every* local minimum. It uses the same, audited, loss evaluator `fra2.F`. It recovers the audit's counterexample (gain 1.27e−8 at θ = −0.0276).
- **Corrected noise-trained transitions** (`repair_v1/results/bisect_v2_*.json`, 30 halvings):

| η | σ | ε_train (new) | Old bracket (does it contain the new value?) | Deviation from leading law | Train vs fixed encoder |
|---|---|---|---|---|---|
| 0.5 | 0.001 | 0.0084571128 | [0.008458, 0.008486] (no) | +1.70% | −0.001% |
| 0.5 | 0.003 | 0.0177810065 | [0.017882, 0.017939] (no) | +2.80% | −0.06% |
| 0.5 | 0.01 | 0.0399463322 | [0.039902, 0.040030] (yes) | +3.49% | −0.76% |
| 0.48 | 0.003 | 0.0181031862 | [0.018054, 0.018113] (yes) | +2.66% | −0.08% |
| 0.52 | 0.003 | 0.0174452781 | [0.017408, 0.017464] (yes) | +2.94% | −0.05% |
| 2/3 | 0.003 | 0.0141664645 | [0.014168, 0.014212] (no, just above it) | +4.70% | −0.05% |

  The values at σ = 0.001 and 0.003 reproduce the audit's independent roots (0.008457112794 and 0.017781006481). The old claim "trained and fixed encoder differ by ≤ 0.7%" is replaced by the last column.
- **S3 scaling function** against the corrected crossings (`repair_v1/results/S3_scaling_vs_v2.json`): −0.03%, −0.12%, −0.65% versus the fixed encoder; −0.03%, −0.18%, −1.41% versus the trained encoder. This replaces the old −0.18%, −0.10%, −0.73%.
- **Every sweep that used `fra2.solve` was rerun** (`repair_v1/results/*_v2_compare.json`):

| Sweep | Points | Points changed | Notes |
|---|---|---|---|
| Noise | 220 | 1 | p = 0.215, σ = 0.01, inside the deep branch: Δθ = 0.001, ΔF = 6e−8 |
| Joint | 222 | 3 | All deep-branch points at p ≤ 0.24: Δθ ≤ 0.0024 |
| Correlation | 231 | 0 | One ±0 sign artefact at mono |
| Correlation scaling | 26 | 0 | — |

  **No transition location on the 0.005 p-grid moved.** Figures 3, 5 and `fig_main_v2` panels (a) and (b) stand.
- **Escape study.** The global optima at p = 0.29 are unchanged (`repair_v1/results/escape_global_v2.json`).
- **Not affected**, because they use exact landscape evaluations or no search: bistability, endpoint scans and theory, spinodal, hysteresis flows, gate lemma, compression and the real-data fits.

## 3. Statistics (R3): the invalid bootstrap is withdrawn

- **Withdrawn.** `real_stats.py`'s "channel-cluster bootstrap" used `set(rng.choice(...))`, which drops multiplicities and is not a bootstrap. Its confidence intervals are withdrawn. The Fisher p-values that treated channel-sharing pairs as independent are also withdrawn.
- **Replacement** (`repair_v1/stats_disjoint.py`, `results/stats_disjoint.json`): Fisher tests on channel-disjoint subsets, so that no channel appears in two units. The primary test uses the subset with seed 0; the distribution over 1000 subsets is reported descriptively.

| Test | Layer-4 hidden channels | Class logits |
|---|---|---|
| Pairs P2: bistability, low vs high \|corr\| (registered) | primary p = 1.5e−5 (27/47 vs 4/35); median 1.1e−5; 100% < 0.05 | primary p = 8.3e−5; median 2.8e−5; 100% < 0.05 |
| Pairs: coexistence asymmetry, \|corr\| < 0.1, c > 0 vs c < 0 (post hoc) | primary 3.3e−5 | primary 3.1e−5 |
| Pairs: sign rule | exact in every disjoint subset | exact in every disjoint subset |
| Triples T3 (registered) | primary 2.6e−7 | primary 0.0018; median 0.006 |
| Triples T4: three-channel asymmetry | primary 0.20, median 0.040: **not established** (post hoc here) | primary 0.019, median 0.0035: **supported** (registered) |
| Triples T5: partner displacement | primary 0.11, median 0.035: **not established** (post hoc here) | primary 0.13, median 0.13: **NOT supported** (registered) |

  The earlier "T5 supported, p = 0.03" for logits is withdrawn. That p-value came from a test that ignored shared channels.
- **Remaining caveats.**
  - Hidden channels and logits come from the **same** ResNet18. They are two representations, not independent model replications.
  - The real tests fit a compressor to pooled train/calibration/test activations. They are not held-out tests and not native-network robustness results.
  - Channels within one network are still not independent draws from a population of networks.

## 4. Certificate and scope labels (R4)

- **Certificate count** (`repair_v1/results/certificate_relabel.json`): **60 of 64** grid points have a surviving set strictly on one side of θ = 0. The four points with c = 0 and p ∈ {0.38, 0.40, 0.42, 0.45} straddle 0 and are **not certified**, because a straddling interval does not prove mono. "63/64 certified" is withdrawn.
- **The floating-point margin** is a hand estimate in double precision, not interval arithmetic.
- **Compression thresholds** come from a Hessian along one perturbation path: one partner, with equal energy drawn from all donors. They are not a full-Hessian or global theorem. Powell multi-starts do not certify global optima.

## Status of the main claims after correction

| Claim | Status |
|---|---|
| Local field expansion, gate lemma, bicritical identity | Unchanged (local theorem / exact identity) |
| Corollary A coefficients | Unchanged magnitudes; signs corrected |
| Noise-trained first-order transition and σ^{2/3} law | Holds with corrected numbers (deviation +1.7% to +4.7%, explained to ≤ 0.65% by the scaling function for the fixed encoder) |
| Spinodal, endpoint law, hysteresis | Unchanged (exact landscapes) |
| Compression thresholds | Unchanged numbers; now labelled path-local |
| Real data | Sign rules and P2 strongly supported under valid inference. The three-channel asymmetry is supported on logits (registered). Partner displacement (T5) is not supported. |
