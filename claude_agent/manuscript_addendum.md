# Manuscript addendum: draft text for the new results

*An additive draft for `project1_toy/paper_assembly_20261006/manuscript.md`. Nothing in that file was changed. The text is written so it can be pasted in or adapted. All numbers trace to `claude_agent/results/`; derivations are in `derivation_section.tex`.*

## Possible title and abstract (an extension of the existing draft, not a replacement)

**Working title:** *Storage phases of superposition: correlation as a field, noise as a first-order driver.*

**Abstract addition.** Beyond the clean critical boundary, we show that the storage transition of the two-feature bottleneck is a critical point of a richer phase diagram.

- **Feature correlation acts as an external field conjugate to the weak-feature weight.** Exact small-angle expansions give a linear response on the same-sign side and a square-root response on the opposite-sign side. They also give a first-order line c\*(ε) ∝ ε² separating opposite-sign from same-sign storage.
- **Training with code noise turns the continuous transition first order.** The transition shifts by (B_cal/C)^{1/3} σ^{2/3}. These are the same coefficients that govern the evaluation-time risk boundary, with no new constants.
- **Mono becomes metastable over an O(1) window**, bounded by a spinodal κ₀(p) = pq[p + qΦ(z_p) − η] = 0 that does not depend on σ.
- **Real data.** In pre-registered tests on 200 ResNet18 hidden-channel pairs, with a 120-pair class-logit replication, the selected shared weight follows the predicted sign rule without exception (129/129 pairs outside the ambiguous band). Bistability concentrates at weak correlation, and opposite-sign/same-sign coexistence sits on the positive-correlation side, as the phase diagram predicts.

## Contributions to add to the existing list

5. **The field picture: an exact local theory of how correlation breaks the storage transition.**
   - The linear term is −2ηcpq·θ.
   - The branch stiffnesses are κ± in closed form.
   - The cubic coefficient is B = 2p²q²/D, which reproduces the proved K_η and C_η.
   - Consequences: exponents 1/2 and 1 at criticality, and a first-order line c\* ≈ 0.866ε² at η = 1/2.
6. **The noise-trained storage transition.** Training noise makes the transition first order, at ε\* = (B_cal/C)^{1/3}σ^{2/3}. The jump is K_ηε\*. Mono is metastable on [p_sp, p_c).
7. **A real-representation selection rule with pre-registered tests and a replication.** It explains why the earlier real pilots showed no reversal and same-sign weights: real pairs are correlated, which places them away from the critical point.

## Related-work sentences that must be added (honest positioning)

- **TMS.** Elhage et al. (2022) already report that correlated features tend toward orthogonal arrangements and anti-correlated features toward antipodal pairs in larger toy models. Our sign rule in the one-dimensional bottleneck is the scalar-code counterpart of that observation, so the rule itself is not new. What we add is:
  - the critical-point and field structure, with exact exponents and the first-order line;
  - the noise-induced first-order transition and its σ-independent spinodal;
  - quantitative links to the existing clean and calibrated coefficients.
- **Robustness and superposition.** Elimadi (2026) and Gorton & Lewis (2025) study adversarial robustness and superposition. Training noise here is isotropic Gaussian code noise, not adversarial. The finding that noise pushes training toward mono storage is directionally consistent with "robustness reduces superposition", in a different threat model and with an explicit transition law.
- **Denoising.** The mono gate shifts to b1 = z_pσ (z_p < 0), so mono acts as a denoiser. This is the mechanism behind both the existing risk boundary and the new spinodal. Standard ReLU-thresholding intuition is related and should be cited as background.

## Results section draft

**§X. Correlation is a field.** For correlated Bernoulli features, the bias-profiled loss near mono has the exact expansion

F(θ) − F(0) = −2ηcpq·θ + κ±θ² + B±θ³ + …

At c = 0, κ₋ = pq(p − ηD)/D vanishes exactly at p_c, and B = 2p²q²/D. The existing transition is therefore a critical point.

- For c < 0 the opposite-sign weight responds as |θ\*| = (2ηpq|c|/3B)^{1/2} (0.734|c|^{1/2} at η = ½).
- For c > 0 the same-sign weight responds linearly (4.24c).
- Below p_c, a first-order line c\* = 9Cε²/(16ηpqK) separates the two sign branches.
- The exact solver confirms all coefficients (fig 2, fig 5).

**§Y. Training noise makes storage selection first order.** When θ and the biases are selected under Gaussian code noise, the sharing branch keeps its clean gain Cε³ but pays the calibrated penalty B_calσ². The transition therefore moves to ε\* = (B_cal/C)^{1/3}σ^{2/3}, with a jump K_ηε\*.

- Precise bisections at η ∈ {0.48, 0.5, 0.52, 2/3} agree to within 1.9–4.9%, with the relative error shrinking as σ → 0.
- Re-optimising the encoder changes the location by at most 0.7%.
- Below the noise-smoothed kink, mono's curvature tends to κ₀(p) = pq[p + qΦ(z_p) − η]. Mono is metastable for p ∈ [p_sp, p_c), with p_sp = 0.279 at η = ½, for every small σ.
- Gradient flow started near mono stays there even where sharing is globally better. Minibatch Adam sometimes escapes (fig 6).

**§Z. Real representations.** On saved ResNet18 activations, the pre-registered predictions hold as follows.

| Prediction | Layer 4 channels (200 pairs) | Class logits (120 pairs) |
|---|---|---|
| P1: corr < −0.05 → opposite-sign | 37/37 | 49/49 |
| P1: corr > 0.15 → same-sign | 17/17 | 26/26 |
| P2: bistability, lowest vs highest \|corr\| tercile | 36/67 vs 6/67 | 23/40 vs 3/40 |
| P3: noise shrinks the shared weight | Fails | Holds |

- **P3 detail.** Layer 4 pairs are dense (median activity 0.55 > p_c), where the toy's noise penalty does not dominate. This explanation is post hoc.
- **Post-hoc observation.** Opposite/same-sign branch coexistence occurs almost entirely at small positive correlation (43 vs 6; 24 vs 6). This mirrors the asymmetric phase diagram (fig 9).
- These are mechanism tests on fixed empirical distributions. They are not tests of the Bernoulli coefficients.

## Figure plan additions

fig2 (field response), fig3 + fig4 (noise-trained first-order transition and landscapes), fig5 (joint phase diagram), fig6 (training metastability), fig7–fig9 (real pairs and replication). All are in `claude_agent/figures/`.

## Limitations to add

- Two features and one dimension.
- A′ assumes the fixed gate pattern is the global bias optimum near θ = 0. This was checked numerically, not proved.
- B′ is an asymptotic statement with numerical support. B2 is leading order in σ.
- The scaling of the c < 0 endpoint is unresolved. The small-σ trend is ≈0.19σ, a conjecture; local slopes fall from 0.93 to 0.22 (fig 10c).
- Stochastic training escapes the metastable mono state when σ is small compared with the initialisation and step scale (LOG: escape statistics). The metastability is exact only for deterministic gradient flow.
- Real tests: pairs are not independent, n = 1024, only directional predictions were tested, and one of the three predictions failed in one dataset.

## Session 3 additions

- **Local theorem (S1).** The bias-profiled expansion near mono is exact for all feasible (p, c, η), and the gate pattern is provably globally optimal for small |θ| (`gate_lemma.py`). Cite this in the derivations appendix as a lemma.
- **Correlation decides packing.** In one dimension, independent features get one opposite-sign slot. A feature correlated with the dominant feature enters for any c ≠ 0 with sign(c). Positive correlation adds a same-sign slot, so three features can be stored; negative correlation competes for the opposite slot (fig 11).
- **Real triples (fig 12).** In 120 ResNet18 channel triples, a correlated third channel is stored with the sign of its correlation in 60/60 strongly correlated cases. It is pulled in far more often than an uncorrelated one (60/60 vs 6/20). The registered pooled displacement prediction failed. Post hoc, the signs separate as the toy map predicts: all three channels are stored in 13/20 triples with strong positive correlation, against 0/20 near zero, and the opposite-sign partner is displaced in 16/20 with strong negative correlation.

## Triples replication (session 3)

- On a second representation (class logits), the positive/negative packing asymmetry holds as a *registered* prediction. Three-channel storage: 36/40 vs 8/20 (p = 8e−5). Partner displacement under negative correlation: 11/20 vs 18/20 kept (p = 0.03).
- The sign rule holds (55/57). Pooled displacement fails, as on layer 4.

## Compression axis (session 3)

- **Proposed contribution.** The resource convention also decides the *compression* phase boundary.
  - With four features in two dimensions and a shared encoder budget, the important feature can borrow amplitude from the other dimension. This moves the storage transition to p = 1 − √((1−η)/(1+η)) on the opposite-sign branch and p = (3η−1)/(η+1) on the same-sign branch.
  - The fixed-norm counterparts are p_c(η) and 2 − 1/η.
  - Zero-fit agreement with numerical bisection at η = 0.3, 0.5 and 0.7 is within 1.5e−3.
  - Below the shared-budget transition, storage breaks the symmetry between equivalent dimensions: one partner first, one per dimension only at sparser p.
- **Insight about the existing endpoint.** In the fixed-norm model the opposite-sign and same-sign storage instabilities coincide at (η, p) = (2/3, 1/2), the manuscript's singular endpoint, which is therefore a bicritical point. Exact identity: on the critical line, B_frozen = κ₊·D(2 − p)/(2pq), so the frozen noise penalty vanishes exactly where the same-sign direction goes soft.
- **Trained networks** (minibatch Adam, 3 seeds per p) reproduce the single-partner phase, with partner norms matching the exact optimum, and are mono at p ≥ 0.43.
- **Figure:** fig13.
