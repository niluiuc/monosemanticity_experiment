# Consolidated statements and their status (claude_agent)

These build on the existing two-feature, one-dimension, energy-one, tied-ReLU model of `project1_toy/paper_assembly_20261006/manuscript.md`. Notation: q = 1 − p, D = 1 − p + p², P_ab = P(X1 = a, X2 = b) for Bernoulli(p) features with correlation c, and importances (1, η).

Each statement carries one status label:

- **Theorem (local):** proved, with assumptions stated. Symbolic sign checks count as proof only where every factor is shown to be a ratio of positive probabilities.
- **Leading-order derivation:** an asymptotic derivation with numerical confirmation, but not a full proof.
- **Numerical:** exact-loss computation with a numerical global search.
- **Empirical:** saved real activations. Registered predictions are kept separate from post-hoc readings.

## S1. Local expansion near mono with correlation [Theorem (local)]

Fix σ = 0 and an interior feasible (p, c). There is k₀(p, c) > 0 such that for 0 < |θ| < k₀:

1. The bias-profiled loss on each branch is given exactly by the closed forms in `analytic_A.py`. The gate pattern used there is the unique global bias optimum (`gate_lemma.py`).
2. F(θ) − F(0) = −2ηcpq·θ + κ_±θ² + B_±θ³ + O(θ⁴). The coefficients are the explicit rational functions listed in `results/analytic_A_series.txt`. At c = 0: κ₋ = pq(p − ηD)/D and B₋ = 2p²q²/D, with the sign chosen so the cubic term is +B₋|θ|³ on the opposite branch. Also κ₊ = pq(1 − η(2 − p))/(2 − p).

**Corollary.** At c = 0, κ₋ = 0 exactly at p_c(η), which recovers the manuscript's threshold. B₋ = 2C_η/K_η³, which recovers K_η and C_η.

## S2. Field response and first-order line [Leading-order derivation]

These follow from S1, valid where the local branch minima are global (proved at c = 0 by the existing strip theorem; for c ≠ 0, numerically).

- At p = p_c: |θ\*| = (2ηpq|c|/3B)^{1/2} for c < 0, and θ\* = ηpqc/κ₊ for c > 0. At η = ½ these are 0.7344|c|^{1/2} and 4.236c.
- For c > 0 and p < p_c, the global optimum jumps from the opposite-sign to the same-sign branch at c\*(ε) = 9Cε²/(16ηpqK) + o(ε²), which is 0.866ε² at η = ½.
- **Checks:** exact-solver agreement at the 10⁻³–10⁻² level; bisection ratios 0.97 → 0.85 as ε grows.

**S2 addendum (session 3): global certificate on a grid.** A Lipschitz branch-and-bound over all θ, with exact bias profiling (`certify_global.py`, v2), certifies the global optimum's branch at 63 of the 64 grid points p ∈ [0.25, 0.45], c ∈ [−0.05, 0.05], consistent with the field picture and the first-order line. The remaining point (p = 0.38, c = 0, gain 2e−9) is unresolved at the certificate's resolution, but its surviving interval contains the true optimum. This is double precision with a 1e−12 margin, not directed rounding.

## S3. Noise-trained transition [Leading-order derivation]

With θ and the biases trained under code noise σ (c = 0):

- The storage transition is first order, at ε\*(σ) = (B_cal/C)^{1/3} σ^{2/3} (1 + o(1)).
- The jump in |θ| is K_η ε\*.
- B_cal = D0 − v(p0) is the existing calibrated coefficient.
- **Checks:** 1.9–4.9% agreement at four η, with the error shrinking as σ → 0. Re-optimising the encoder changes the location by ≤ 0.7%.

**S3 addendum (session 3).** The 2–5% deviation is explained quantitatively by an explicit scaling function Π(r, α) (Gaussian ReLU moments, r = |d|/σ, α = sin²θ/σ). With it, the predicted fixed-encoder crossing matches the measurement to −0.18%, −0.10% and −0.73% at σ = 0.001, 0.003 and 0.01 (`S3_scaling_function2.py`). Status: the leading law plus explicit corrections; formal remainder bounds are still to be written.

## S4. Mono spinodal under training noise [Leading-order derivation]

- For |θ| ≪ σ → 0, the curvature at mono is κ₀(p) = pq[p + qΦ(z_p) − η], where p z_p + q[z_pΦ(z_p) + φ(z_p)] = 0.
- Mono is therefore metastable on [p_sp, p_c), with p_sp = 0.2604, 0.2791, 0.2985 and 0.4628 for η = 0.48, 0.5, 0.52 and 2/3, independent of σ at leading order. The barrier is O(σ²).
- **Checks:** finite differences converge to κ₀ with an O(σ) correction (≈ +0.28σ).

**S4 addendum (session 3):** κ_σ(p) = κ₀(p) − 2p z_p σ + O(σ²). The first-order term comes from the cos²θ amplitude acting on mono's noise-shifted gate. All other terms are O(σ²) or exponentially small. It is checked against 12 finite-difference curvatures, with residual ≤ 1.3e−4 set by the step size (`spinodal_first_order.py`). Status: proof outline with explicit terms.

## S5. Critical endpoint on the c < 0 side [Numerical]

|c_e(σ)| ≈ 3.8e−4 … 2.3e−3 for σ = 0.002 … 0.03 (±5%). The small-σ trend is ≈ 0.19σ (a conjecture). The asymptotic exponent is not established.

**S5 addendum (session 3), semi-analytic.** In the scaled angle x = |θ|/σ the mono well has a fixed shape Φ(x) with a maximum restoring slope max Φ′ ≈ 0.04 (at x ≈ 1.9). A correlation field removes the well when 2η|c|pq = σ·max Φ′. That gives |c_e| = σ·max Φ′/(2ηpq), linear in σ: ≈ 0.16σ as σ → 0. At σ = 0.002, using the measured endpoint p_e = 0.3848, the prediction is 0.189σ against 0.1906σ measured (`endpoint_theory.py`).

## S6. Training dynamics [Numerical]

- Gradient flow on the exact noisy loss stays at mono inside the metastable window.
- Adam's outcome depends on σ relative to the initialisation and step scales. At σ = 0.03, about 40% of runs stay stuck.

## S7. One-dimensional packing with three features [Numerical]

- **Independent features:** only one opposite-sign partner is ever stored.
- **A third feature correlated with feature 1:** it enters for any c13 ≠ 0, with sign(c13).
  - Positive c13 adds a same-sign slot. All three features are stored at sparse p; at denser p the uncorrelated partner is displaced.
  - Negative c13 competes for the opposite-sign slot. Both partners coexist only at small |c13| and sparse p.

## S8. Real activations [Empirical; ResNet18, saved arrays]

**Registered predictions:**

| Test | Result |
|---|---|
| Pair sign rule | 37/37, 17/17 (layer 4); 49/49, 26/26 (logits) |
| Bistability concentrated at weak \|corr\| | 36/67 vs 6/67; 23/40 vs 3/40 |
| Noise shrinkage | Fails (layer 4); holds (logits) |
| Triple sign rule | 60/60 |
| Correlation pulls the third channel in | 60/60 vs 6/20 |
| Pooled displacement | Fails |

**Post hoc:**

- Pair branch coexistence sits at small positive correlation: 43 vs 6 pairs (layer 4), 24 vs 6 (logits).
- In triples, positive c13 enables three-channel storage (13/20 and 11/20, against 0/20 near zero), while negative c13 displaces the opposite-sign partner (feature 2 is kept in only 4/20).

**S8 addendum (session 3): triples replication on class logits, registered in advance.** T1 sign rule 55/57. T3: 57/60 vs 10/20. The positive/negative asymmetry, now registered: three-feature storage in 36/40 (c13 ≥ 0.05) vs 8/20 (≤ −0.05), Fisher p = 8e−5; uncorrelated partner kept in 11/20 (strong negative) vs 18/20 (strong positive), p = 0.03. Pooled displacement (T2) failed again.

## S9. Second clean transition [Numerical, unexplained]

At η = ½ and σ = 0, the global optimum jumps between p = 0.2075 and p = 0.21 inside the sharing phase. This is outside the existing proved domain.

## Open problems, in order of value for the paper

1. Global selection for c ≠ 0, which would upgrade S2 to a theorem. A route: extend the existing strip certificate with c as a parameter.
2. Rigorous versions of S3 and S4. Both look tractable with the existing calibrated-coefficient machinery.
3. A theory of the c_e(σ) scaling (S5).
4. The S7 displacement line, extended to m ≥ 2 to address the "compression" axis.

## S10. Compression with a shared energy budget (n = 4, m = 2, importances (1, 1, η, η), independent) [Leading-order derivation + Numerical]

- **Local theory.** A partner can be paid for by borrowing energy from the other dimension, raising the important feature's amplitude r² = 1 + u. Profiling u in the 2×2 Hessian at mono gives these storage instabilities:
  - opposite-sign branch at **p = 1 − √((1−η)/(1+η))**;
  - same-sign branch at **p = (3η − 1)/(η + 1)**.
  - The fixed-norm counterparts are p_c(η) and 2 − 1/η.
- **Numerical bisections (zero-fit):** η = 0.5 → [0.4219, 0.4225] vs 0.42265; η = 0.3 → [0.26558, 0.26620] vs 0.26620; η = 0.7 (same-sign first) → [0.6456, 0.6463] by the gain threshold 1e−10, or [0.6463, 0.6475] by the weight criterion (a partner weight of 0.0008 is still present at 0.64625, with gain 2.6e−11), vs 0.64706. The criteria differ because gains near a continuous transition scale like ε³.
- **Phases at η = ½ (numerical):** mono; then symmetry-broken *single*-partner storage, in which energy moves from the other important feature; then one partner per dimension, identical to the two-feature solution, at p ≤ 0.15.
- **Branch ordering.** Fixed norm: the branches cross at (η, p) = (2/3, 1/2), the manuscript's singular endpoint, which is therefore a bicritical point. **Exact identity:** on the critical line, B_frozen = κ₊·D(2 − p)/(2pq), so the frozen noise coefficient vanishes exactly where the same-sign direction goes soft (`bicritical_identity.py`). Shared budget: they cross at (0.6, 0.5).
- **General m (session 3):** p_c^shared(η, m) = [m(1+η) − √(m(m(1−η)² + 4η(1−η)))] / (2(m + η − 1)). At η = ½ this gives 0.4226, 0.4417 and 0.4531 for m = 2, 3, 4, tending to η as m → ∞. Adam-trained networks with m = 3 and 4 reproduce the predicted upward shift (LOG). For m ≥ 3 the exact global optimum was not computed.
- **Trained networks** (Adam on sampled data, 3 seeds): a single partner in every seed for 0.20 ≤ p ≤ 0.38, with norms matching the exact optimum (0.205 vs 0.204 at p = 0.30). The 0.40–0.42 window is mixed; all seeds are mono at p ≥ 0.43.
- **Limits.** Independent features, one n/m ratio, a Hessian-level (local) statement plus a numerical global search. The 1 → 2 partner boundary is not derived.


---
**Corrections (7 Oct 2026, after the independent GPT audit):** see `repair_v1/CORRECTIONS.md`. It corrects the signs in S2, the S3 numbers, the S2 certificate count (60/64, not 63/64), the S8 statistics (T5 on logits is not supported under valid inference) and the scope labels.

**Update (repair_v2):** superseded by `repair_v2/STATUS.md`. This includes the wording of S2 ("global optimum jumps" now reads "local branch minima switch") and S6 ("gradient flow" now reads "deterministic local optimisation").
