# Status of every claim (single source of truth, as of repair_v3)

This supersedes `repair_v2/STATUS.md`. The changes are listed at the end.

**Labels:**
- **[P]** local proof: pointwise in the stated parameters, computer-algebra assisted where noted.
- **[I]** exact identity.
- **[L]** leading-order derivation with numerical support; not a proof.
- **[N]** numerical: finite searches and evaluations; not a global certificate.
- **[G]** grid computation with a Lipschitz bound in double precision; not interval arithmetic.
- **[E]** exploratory empirical: one network, pooled train/calibration/test activations; storage selection only, not robustness; p-values conditional on an unverified independence model.
- **[X]** withdrawn or failed.

## Theory: two-feature, one-dimension model

| # | Claim | Label | Key evidence |
|---|---|---|---|
| T1 | Local expansion near mono with correlation: F(θ) − F(0) = −2ηcpq·θ + κ±θ² + B±θ³ + …, exact rational coefficients | [P] given T2 | `analytic_A.py`, series file; independently re-derived by GPT |
| T2 | Lemma A′: fixed gate pattern is the unique bias optimum for small \|θ\| | [P], pointwise in (p, c), non-uniform near the boundary | Convexity proof written into `repair_v3/derivation_section_v4.tex` (from the math audit). `gate_lemma.py` is kept as a cross-check only |
| T3 | Signed coefficients: A = (5−√5)/8, K = 2A/(3B), C = 4A³/(27B²) recover the existing theorem | [I] at η = ½ | `repair_v1/analytic_A_signed.py`; confirmed by GPT |
| T4 | Field response at p_c: √(−h/(3B)) for c < 0, h/(2κ₊) for c > 0 | [L] | Solver agreement 0.05–0.4% (GPT check) |
| T5 | Local branch competition line c\* ≈ 0.866ε² | [L] | Bisections (ratio 0.97 → 0.85 as ε grows) |
| T6 | Branch of the best minimum on a 64-point (p, c) grid | [G]: 60 strictly signed, 4 unresolved (c = 0, p ≥ 0.38) | `certify_global.py` v2 |
| T7a | Training noise makes storage first order at ε\* ≈ (B_cal/C)^{1/3}σ^{2/3} | [L] | Asymptotic argument; the re-optimisation step is not proved |
| T7b | Noise-trained crossings ε\* = 0.0084571, 0.0177810, 0.0399463 (η = ½; σ = 0.001, 0.003, 0.01) and those at η = 0.48, 0.52, 2/3 | [N] | `repair_v1/results/bisect_v2_*`; σ = 0.001 and 0.003 match GPT's independent roots |
| T8 | Explicit scaling function explains the deviation from T7 | [N] (−0.03%, −0.12%, −0.65% vs fixed encoder) | `repair_v1/results/S3_scaling_vs_v2.json` |
| T9 | Mono curvature under noise: κ₀(p) − 2p z_p σ + O(σ²); spinodal p_sp (0.2791 at η = ½) | [L], remainder bounds not written | `spinodal*.py`; 4 GPT checks agree within 9.7e−6 |
| T10a | Endpoint law \|c_e\| = σ·max Φ′/(2ηpq) | [L], semi-analytic with Φ computed numerically | `endpoint_theory.py` |
| T10b | Measured endpoints \|c_e\|(σ) | [N] | `endpoint_refine.py` |
| T11 | Bicritical identity on the critical line: B_frozen = κ₊·D(2−p)/(2pq) | [I]. A shared zero at p = ½, possibly a symmetry; no causal mechanism is claimed | `bicritical_identity.py` |
| T12 | Second clean jump at p ≈ 0.208 | [N], unexplained | — |

## Extensions

| # | Claim | Label | Key evidence |
|---|---|---|---|
| X1 | Three features in one dimension: independent features use one opposite-sign slot; correlated features enter with sign(c13) and can add or compete | [N] | `fra3.py`, `packing_map.py` |
| X2 | Shared-budget compression thresholds: 1 − √((1−η)/(1+η)) and (3η−1)/(η+1), plus the general-m formula | [L] along the one-partner equal-donor path. The donor loss is one-sided, which is harmless since u\* > 0. A full-space quadratic search (math audit) found no earlier instability: [N] support, not proof | `compression_theory*.py`; GPT 55-digit path checks agree within 1.4e−8 |
| X3 | Best minima found (m = 2) and Adam-trained networks (m = 2, 3, 4) near these thresholds | [N]. Two bisection brackets (η = 0.5; η = 0.7 by gain threshold) lie just *below* the threshold and exclude it; consistent with a detection limit, but not containment | `fra_nm.py`, `train_compression*.py` |
| X4 | Training noise makes compression storage abrupt and shifts it to sparser p | [N], qualitative | `train_compression_noise.py` |
| X5 | Deterministic local optimisation stays at mono in the metastable window; Adam sometimes escapes | [N] | `train_hysteresis.py`, `sgd_escape.py` |

## Real activations (ResNet18: layer-4 channels and class logits from the same network)

| # | Claim | Label | Key evidence |
|---|---|---|---|
| E1 | Sign rule for pairs (corr < −0.05 → opposite-sign; > 0.15 → same-sign): 37/37, 17/17, 49/49, 26/26 | [E] | Exact in every channel-disjoint subset |
| E2 | Bistability concentrated at weak \|corr\| (registered) | [E]; disjoint-subset p ≈ 1e−5 (exploratory) | `repair_v1/stats_disjoint.py` |
| E3 | Opposite/same-sign coexistence at small positive correlation | [E], post hoc | Disjoint-subset p ≈ 3e−5 |
| E4 | Triples: correlated third channel stored with sign(c13) (60/60, 55/57) and pulled in more (T3) | [E] | — |
| E5 | Triples T4, three-channel asymmetry: registered on logits | [E]; primary p = 0.019 (exploratory). Not established on layer 4 (post hoc there) | — |
| E6 | Field equals 2η·Cov on real pairs; quadratic stiffness does not transfer (≈1.4× overshoot) | [E] | `real_linear_response.py` |

## Withdrawn or failed

| # | Claim | Label |
|---|---|---|
| F1 | Noise shrinkage P3 on layer 4 (registered) | [X] failed |
| F2 | Pooled displacement T2 (registered, both representations) | [X] failed |
| F3 | Partner displacement T5 on logits (registered) | [X] not supported (p = 0.13) |
| F4 | Set-based "bootstrap" intervals and independence-assuming Fisher p-values | [X] withdrawn |
| F5 | "63/64 certified"; "trained vs fixed ≤ 0.7%" (old numbers); old σ = 0.001 and 0.003 brackets; negative signed K, C | [X] withdrawn (see `repair_v1/CORRECTIONS.md`) |
| F6 | Any statement of global optimality at c ≠ 0 or σ > 0, or of native-network robustness | [X] not claimed |

## Open: the target question

**When does sharing beat mono on clean held-out data, and when does corruption reverse that advantage, in a real network?** This is *not* answered by anything above. See `ROBUSTNESS_PROTOCOL_DRAFT.md`, which has not been run.

## Changes from repair_v2

- **T2:** the proof is now written in the derivation, so the label is no longer only computer-algebra assisted.
- **T7 and T10:** each split into an [L] part and an [N] part.
- **T11:** the interpretation is qualified.
- **X2:** one-sidedness of the donor loss and the full-space numerical support are stated.
- **X3:** the brackets that exclude the threshold are flagged.
- **Toy versus real triples** were already separate (X1 is [N]; E4 and E5 are [E]); the LaTeX now splits them into separate paragraphs as well.
- **Corrected remainder:** in the derivation, the per-state error in Proposition A reads O(θ³), not O(θ⁴).
