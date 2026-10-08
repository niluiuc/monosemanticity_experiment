# claude_agent — additions to Project 1

**Read first:** `STATEMENTS.md` (every result with an honest status label), then this summary (§0), then `LOG.md` (a plain-language log of everything done, including failures), then `manuscript_addendum.md` (paste-ready paper text). Key figures: **figures/fig_main_v2.png/.pdf** (a 3×2 paper figure, which adds the certificate map and the compression thresholds), figures/fig_main (2×2), fig 5 (phase diagram), fig 3 (noise-trained transition), fig 7 and fig 9 (real data), fig 10 (theory checks).

*Claude (AI agent), 7 October 2026. Everything here is **additive**: no existing file outside `claude_agent/` was changed. It reuses the exact two-feature / one-dimension, energy-one, tied-ReLU model of `project1_toy/paper_assembly_20261006/manuscript.md` §3. It adds two coordinates that the existing record does not cover: **feature correlation c**, and **training-time code noise σ**. Training-time noise means the encoder and biases are selected under noise, not selected clean and only evaluated under noise.*

## 0. Summary

| # | Result | Status |
|---|---|---|
| V | The new solver reproduces the existing clean theorem: p_c(η), K_η, C_η at η ∈ {0.48, 0.5, 0.52, 2/3}. | Numerical; ratios converge to the theory as ε→0 (fig 1) |
| A | **Correlation acts as an external field conjugate to the weak-feature weight.** The existing continuous transition is a *critical point*. Response at p_c: \|θ\| = 0.734\|c\|^{1/2} for c<0 and θ = 4.24c for c>0. For c>0 a **first-order line** c\*(ε) = 9Cε²/(16ηpqK) leaves the critical point. For c<0 there is only a smooth crossover. | Leading-order expansion derived here. The coefficients use the existing (K, C) and contain no fitted constants. Verified numerically (fig 2, fig 5) |
| B | **Training with code noise makes the storage transition first order.** It shifts it to p\* = p_c − (B_cal/C)^{1/3} σ^{2/3}, with a jump \|θ\| ≈ K(B_cal/C)^{1/3} σ^{2/3}. B_cal and C are the *existing* calibrated coefficients, so the existing evaluation-time crossing law σ = 1.3187 ε^{3/2} is also the training-time coexistence line. | Asymptotic argument (heuristic step flagged in §3) plus numerics at σ = 0.003–0.1 with no fitting (fig 3, fig 4) |
| C | Under noise, the c>0 first-order line survives. On the c<0 side the line extends to a **critical endpoint** c_e(σ) < 0. | Refined in session 2: \|c_e\| = 3.8e−4 … 2.3e−3 for σ = 0.002 … 0.03. Session-3 theory: |c_e| = σ·max Φ′/(2ηpq), linear in σ (≈0.16σ as σ → 0). At σ = 0.002 it predicts 0.189σ against 0.1906σ measured. Semi-analytic (LOG.md, fig 10c) |
| D | Actual training sees it. With σ = 0.03 and p = 0.28, gradient flow on the exact loss started near mono **stays mono** even though sharing is the global optimum. Adam stays mono in 1 of 2 seeds. Clean training always escapes. | Numerical (fig 6) |
| E | Side finding: the *clean* model has a second, first-order jump inside the sharing phase at p ≈ 0.208–0.210 (η = 0.5). It lies outside the existing theorem's declared domain, so it does not conflict with it. | Numerical observation, unexplained |
| F | **Link to the real-model obstruction** (`professor_bridge_review_20261007`). The covariance obstruction found there *is* the field term in A. A predicts same-sign sharing for positively correlated pairs. Both real pilots did select same-sign weights. | Qualitative consistency, not a test |

**Session 2 additions (details in §12 and LOG.md):**

| # | Result | Status |
|---|---|---|
| A′ | **A is now exact.** The closed-form branch losses give exact Taylor coefficients for any (p, c, η). The cubic coefficient B = 2p²q²/D is derived independently and reproduces the existing K_η and C_η to machine precision. | Exact symbolic; matches the solver to 3e−17 |
| B′ | **B's open step is checked.** The noise-trained transition and the fixed-encoder calibrated crossing differ by ≤ 0.7%. Both converge to (B_cal/C)^{1/3}σ^{2/3} at η = 0.48, 0.5, 0.52 and 2/3. | Precise bisections, no fitting |
| B2 | **The mono spinodal does not depend on σ:** κ₀(p) = pq[p + qΦ(z_p) − η]. Any training noise makes mono locally stable on [p_sp, p_c), a window about 0.10 wide at η = 0.5 (p_sp = 0.2791). | Leading-order derivation; finite differences converge with an O(σ) correction |
| X | **Exploratory: three features in one dimension.** Independent features: only one extra (opposite-sign) partner is ever stored, so the two-feature theory appears complete for m = 1. A positively correlated third feature joins as a same-sign partner (p = 0.15, three features stored) or displaces the opposite-sign partner (p = 0.30). | Numerical, one slice, not a claim (LOG.md) |
| G | **Session 3: global certificate.** Lipschitz branch-and-bound with exact bias profiling certifies the global optimum's branch at 63 of 64 (p, c) grid points, matching the field picture and the first-order line. | Computer-assisted (double precision) |
| L | **Session 3: S1 is now a local theorem.** I enumerated every bias piece symbolically (`gate_lemma.py`). Every sign reduces to ratios of positive probabilities. | Proof (local); global selection at c ≠ 0 still open |
| P | **Session 3: three-feature packing map** (fig 11) and a **real triples test** (fig 12). Sign rule: 60/60. Correlation pulls the third channel in: 60/60 vs 6/20. Pooled displacement: failed. Post hoc: positive correlation adds a slot (all three stored in 13/20) and negative correlation displaces (4/20). | Numerical and empirical (LOG.md) |
| S10 | **Compression (n = 4, m = 2, shared budget).** Transitions at 1 − √((1−η)/(1+η)) (opposite branch) and (3η−1)/(η+1) (same-sign branch), matched by bisection to within 1.5e−3 at η = 0.3, 0.5 and 0.7. Symmetry-broken single-partner phase. The manuscript's endpoint (2/3, 1/2) is a bicritical point. | Local Hessian theory plus numerics (fig 13) |
| R | **Real activations follow the field picture.** Registered predictions on 200 ResNet18 layer4 channel pairs, with a 120-pair class-logit replication. Sign rule: 37/37, 17/17, 49/49 and 26/26. Bistability concentrated at weak correlation: 36/67 vs 6/67, and 23/40 vs 3/40. Noise shrinkage (P3) failed on layer4 and held on logits. Post hoc, branch coexistence sits at small *positive* correlation in both datasets, the toy's asymmetry. | Pre-registered directional tests plus a labelled post-hoc analysis (figs 7–9) |

## 1. Model and notation

- Features: X = (X1, X2), Bernoulli(p) marginals with Pearson correlation c. So P11 = p² + cpq, P10 = P01 = pq(1−c), P00 = q² + cpq, where q = 1−p.
- Code and reconstruction: h = w·X + σZ with w = (cos θ, sin θ), and x̂_i = ReLU(w_i h + b_i).
- Loss: F(θ) = min_b E[(x̂1−X1)² + η(x̂2−X2)²].
- θ = 0 is mono, θ < 0 is the opposite-sign sharing branch (the one the existing theorem selects), and θ > 0 is same-sign sharing.
- All expectations are exact: four states plus closed-form Gaussian ReLU moments. When σ > 0 the biases *and* θ are optimised under the noisy loss. Biases are profiled by a 1001-point grid plus a bounded Brent step. θ is searched on each branch with a coarse vectorised locator, *plus* an exact log grid down to 10⁻⁷ (where gains are around 10⁻⁹), followed by bounded refinement. η = 0.5 throughout unless stated (p_c = (3−√5)/2 = 0.381966).

## 2. Result A — correlation is a field (σ = 0)

**Small-θ expansion.** With the biases re-optimised, for small θ:

- Output 2: x̂2 ≈ θX1 + θ²X2 + b2 with its gate open. Its optimal loss is Var(θX1 − (1−θ²)X2) = pq(1 − 2cθ − θ²) + O(θ³).
- Output 1, θ > 0: the best b1 ∈ [−θ, 0] gives loss θ²A₊, where A₊ = (P01+P11)P10/(P01+P11+P10).
- Output 1, θ < 0: the best b1 ∈ [0, |θ|] gives loss θ²A₋, where A₋ = P11(P10+P00)/(P11+P10+P00).

Hence

  F(θ) − F(0) = −h θ + κ_± θ² + O(|θ|³),  with h = 2ηcpq and κ_± = A_± − ηpq.

- **Recovery of the existing threshold.** At c = 0, κ₋ = 0 ⇔ p/(1−pq) = η ⇔ ηp² − (1+η)p + η = 0. This is exactly p_c(η) of the manuscript, re-derived independently. κ₊ > 0 for all p at η = 0.5, so mono never destabilises toward the same-sign branch at c = 0.
- **Critical response.** On the opposite branch, write F = hk + κ₋k² + Bk³ with k = |θ|. Matching the existing k ≈ Kε and gain ≈ Cε³ fixes B = 2C/K³. At p = p_c (κ₋ = 0) with c < 0 this gives |θ\*| = (h/3B)^{1/2} = 0.734|c|^{1/2} and gain = (2/3)h|θ\*| ∝ |c|^{3/2}. For c > 0 the same-sign side responds linearly: θ\* = h/2κ₊ = 4.24c.
- **First-order line (c > 0, p < p_c).** The opposite-branch minimum is lifted to zero depth when h = A²ε²/4B with A = 3BK/2. That gives c\*(ε) = 9Cε²/(16ηpqK) ≈ 0.866ε² at leading order.

| Check | Prediction | Exact solver |
|---|---|---|
| \|θ\*\| at p_c, c = −10⁻⁴ | 0.00734 | 0.00736 |
| θ\* at p_c, c = +10⁻⁴ | 0.000424 | 0.000422 |
| gain at p_c, c = −10⁻⁴ | 1.155e−7 | 1.162e−7 |
| log-log slopes over 10⁻⁴…10⁻² | 1/2 and 1 | 0.504 and 0.951 (the same-sign slope bends below 1 at larger c; 10⁻⁴…10⁻³ is linear) (fig 2) |
| c\*(p = 0.37 / 0.36 / 0.34 / 0.32) | 1.26e−4 / 4.28e−4 / 1.61e−3 / 3.61e−3 | [1.207, 1.222]e−4 / [4.02, 4.07]e−4 / [1.43, 1.45]e−3 / [3.05, 3.09]e−3 |

The c\* ratio (measured/predicted) goes 0.97 → 0.85 as ε grows. That is consistent with a leading-order formula, and the correction is not derived.

**Meaning.** The existing storage transition exists only at exactly zero correlation. It is the critical point of a richer diagram: a first-order line on the c > 0 side (opposite-sign ↔ same-sign storage) and a crossover on the c < 0 side. This is the physics behind the bridge review's applicability obstruction.

## 3. Result B — training with noise makes the transition first order (c = 0)

**Argument.** Take the regime σ ≪ ε. The sharing branch's gate offset b1 = O(ε) keeps its gates in the linear regime. Its clean gain Cε³ is then reduced by a noise penalty that, with both models' biases re-optimised under noise, is the existing *calibrated* coefficient B_cal σ². Here B_cal = D0 − v(p0) = 0.165038 at η = 0.5, recomputed and matching the manuscript's √(C/B_cal) = 1.31875. Meanwhile mono's zero gate is locally stable under noise (fig 4, and gradient flow in §5). The two minima therefore coexist, and they exchange stability where Cε³ = B_cal σ²:

  ε\*(σ) = (B_cal/C)^{1/3} σ^{2/3} = 0.8316 σ^{2/3},  jump |θ| ≈ K ε\* = 1.313 σ^{2/3}.

**Heuristic step.** That re-optimising θ under noise changes the sharing branch only at higher order is assumed here, not proved.

| σ (training) | Predicted ε\* | Measured bracket (p grid 0.005) | Jump at the last sharing point |
|---|---|---|---|
| 0.003 | 0.0173 | [0.0170, 0.0220] | θ = −0.0348 at ε = 0.022 (Kε = 0.0347) |
| 0.01 | 0.0386 | [0.0370, 0.0420] | −0.0622 |
| 0.03 | 0.0803 | [0.0820, 0.0870] (≈2% outside) | −0.114 |
| 0.1 | 0.179 | [0.182, 0.187] (≈3% outside) | −0.405 (merged with result E) |

No constant was fitted. The two largest σ sit slightly outside the asymptotic prediction, as expected for an O(σ^{2/3}) leading term.

**Bistability.** At σ = 0.03 the landscape (fig 4) has two minima for p ∈ [≤0.272, 0.302] (`results/endpoint/s0.03_m0.0.json`).

## 4. Result C — joint (p, c, σ)

- **σ = 0.03, full sweep** (`results/joint.json`). For c = +0.005 the first-order jump survives as opposite-sign → same-sign, between p = 0.260 (θ = −0.162) and p = 0.265 (θ = +0.029). For c ≥ 0.02, same-sign storage holds throughout p ∈ [0.22, 0.40]. For c = −0.005 the jump is already smoothed.
- **Critical endpoint on the c < 0 side.** The bistable window shrinks to zero as c becomes more negative. Brackets of c_e (the most negative c still bistable, and the next c tried with no bistability), from `results/endpoint/`:

| σ | c_e bracket |
|---|---|
| 0.003 | [−5.8e−4, −5.2e−4] |
| 0.01 | [−1.5e−3, −1.36e−3] (one non-monotone grid point at m = 0.63) |
| 0.03 | [−2.56e−3, −2.33e−3] |

- **Scaling of c_e is unresolved.** My naive guess c_e ∝ σ^{4/3} is *not* supported: local slopes are about 0.7 and 0.5. Brackets are limited by the θ grid (0.003) and the p grid (0.002).
- **σ = 0.1 is excluded.** There the bistability detected is between two *sharing* minima (result E), not mono versus sharing.

## 5. Result D — training dynamics (`results/hysteresis/`)

- **σ = 0.03, p = 0.28** (sharing is globally optimal by 8.3e−5 in loss):
  - L-BFGS-B on the exact loss from θ0 = −0.01 ends at θ = 0 (mono). Nelder–Mead agrees, with b1 = −0.0151 ≈ −σ/2, i.e. mono shifts its gate to denoise.
  - Started from sharing, it ends at −0.148.
  - Minibatch Adam (batch 8192, 6000 steps, sampled noise) from near mono: seed 0 stays at −0.002, seed 1 escapes to −0.151.
- **σ = 0.03, p = 0.32** (mono globally optimal): every run ends at mono.
- **σ = 0, p = 0.28:** Adam escapes to sharing from both initialisations. L-BFGS-B stalls at the ReLU kink when σ = 0, a non-smoothness artifact recorded honestly; Nelder–Mead from the same initialisation reaches sharing (−0.163).
- **Takeaway:** with training noise, *which storage a trained model reports depends on initialisation and optimiser noise*, inside a predictable window.

## 6. Result E — second clean transition (`results/clean_second_transition.json`)

At η = 0.5 and σ = 0 the global optimum jumps between p = 0.2075 (θ = −0.4066, b2 = 0.175) and p = 0.21 (θ = −0.3432, b2 = 0.240). It persists under training noise, and at σ = 0.1 it merges with the mono transition. It lies outside the existing proved domain (p ∈ [0.35, 0.42]) and is likely a change in gate pattern. Not analysed further.

## 7. Connection to the real-model record (additive interpretation)

- **Same-sign weights.** The bridge review proved that nonzero covariance excludes a mono optimum. In the language of A, that is a nonzero field. Positive covariance selects *same-sign* sharing. Both real pilots in fact selected same-sign weights (ResNet head: (0.835, 0.550)), and their training covariances (0.093 and 0.163) are far above the c\* ~ 10⁻³ scale. This is consistent with A, but it is qualitative, because the real features are continuous, not Bernoulli.
- **A concrete real-model prediction.** For pairs of feature activations with near-zero co-occurrence correlation, a sharp, noise-shifted storage change should appear. For |c| ≫ |c_e(σ)| it should be smooth, with the sign of the shared weight following the sign of c. This is a testable selection rule for any SAE feature set, and it does not need hand-picked semantic labels.

## 8. Verification (`results/verify.json`)

- **Monte Carlo vs closed form:** 8 random (p, c, σ, θ, b) settings with 4×10⁶ samples each; max |z| = 1.51.
- **Brute force:** a 3-D grid over (θ, b1, b2) at 4 representative points. The solver is never worse than the grid (by 3e−8 to 3e−7) and agrees on θ to within the grid step.
- **Stiffness formulas:** relative error grows linearly in θ (0.5% at θ = 10⁻³, up to 6.7% at 3×10⁻³ on the soft side), as an O(θ³) remainder should. Errors are below 10⁻³ when the linear field term dominates.
- **Validation against the existing theorem:** fig 1 and `results/validate_clean.json`.

## 9. Limitations

- Two features and one dimension, Bernoulli features, η = 0.5 for A–E.
- Global optimisation is numerical (grids plus refinement), not certified. The existing project's certificates do not extend to c ≠ 0 or to training noise.
- Result B's argument is asymptotic, and its θ-reoptimisation step is heuristic. Result A's cubic coefficient is inferred from the existing (K, C), not derived term by term.
- Endpoint brackets are resolution-limited. Adam used 2 seeds per condition.
- Per `AGENTS.md`, new mathematics should enter `output/pdf/Superposition_Recursive_Training_Derivations.pdf`. I have **not** edited that volume or its LaTeX. A ready-to-insert section is in `derivation_section.tex` for you or your review agents to integrate. It needs amsmath and amssymb; a compiled preview is `derivation_section_preview.pdf`.

## 10. Reproduce

The sandbox caps one command at about 3 minutes, so large grids run in chunks. Every script refuses to overwrite an existing results file.

```
python validate_clean.py
python sweep.py corr_scaling
python sweep.py corr 0 3 ; python sweep.py corr 1 3 ; python sweep.py corr 2 3 ; python sweep.py corr merge 3
python sweep.py noise 0 3 ; ... ; python sweep.py noise merge 3
python sweep.py joint 0 3 ; ... ; python sweep.py joint merge 3
python coexistence_clean.py 0.37,0.36,0.34,0.32
python endpoint_scan.py <sigma> <m-list>        # c = -m sigma^(4/3)
python train_hysteresis.py 0.03 0.28 ; python train_hysteresis.py 0.0 0.28 ; python train_hysteresis.py 0.03 0.32
python verify.py
python make_figures.py
```

Requires numpy, scipy and matplotlib. `fra2.py` is the solver (the name has nothing to do with the FRA paper; read it as "feature-resolved two-feature").

## 11. Next steps that build on this

1. Turn A into a theorem: rigorous small-θ expansion with the c-dependent κ₋, and a proof of the first-order line. It reuses the existing global-selection machinery.
2. Turn B into a theorem: a coexistence statement for the noise-trained objective, using the existing calibrated-coefficient proofs.
3. A real-model test of the sign/sharpness selection rule in §7 on any public SAE feature set.
4. Explain result E (gate-pattern analysis).

## 12. Session 2 (details in LOG.md)

- **A′, exact expansion.** `analytic_A.py` gives the series in `results/analytic_A_series.txt` and the checks in `results/analytic_A.json`.
  - Opposite-branch θ² coefficient at c = 0: pq(p − ηD)/D, the manuscript's A = p − ηD.
  - θ³ coefficient: −2p²q²/D, so B = 2p²q²/D = 2ηpq² at p_c.
  - Linear coefficient for any c: −2ηcpq.
  - Validity: a fixed gate pattern near θ = 0, checked at 20 points; not proved globally.
- **B′, re-optimising the encoder.** `result_B_checks.py bisect`; results in `results/resultB/bisect_*.json`.
- **B2, mono spinodal.** `spinodal.py`; results in `results/resultB/spinodal.json`.
  - The derivation is the Schur complement of the (d, b1) Hessian with the kink smoothed by noise.
  - At c = 0: (P01Φ + P11)(P00Φ + P10)/(qΦ + p) = pq(qΦ + p).
  - Output 2 contributes −ηpq.
- **Real-activation tests.**
  - Protocol: `real_protocol.md`. Code: `real_pairs.py` (set `REAL_DATASET=logits` for the replication) and `analyse_real.py`.
  - Robustness check: `check_real_bistability.py`. Post-hoc analysis: `branch_coexistence.py`.
  - Figures 7–9.
  - Run commands: `python real_pairs.py select`, then `python real_pairs.py run k 13` for k = 0…12, then `python real_pairs.py merge 13`, then `python analyse_real.py`. For the replication, prefix each with `REAL_DATASET=logits` and use 8 chunks.


---
**Corrections (7 Oct 2026, after the independent GPT audit):** see `repair_v1/CORRECTIONS.md`. Where this file disagrees with `repair_v1/`, `repair_v1/` supersedes it.

**Update (repair_v2):** the single source of truth for claim status is now `repair_v2/STATUS.md`. The wording corrections are in `repair_v2/CORRECTIONS_v2.md`.

**Update (repair_v3):** the current claim status is in `repair_v3/STATUS.md`. The bounded real-data run result is in `repair_v3/RESULTS.md`.
