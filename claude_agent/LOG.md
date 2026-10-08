# claude_agent running log

Plain-language log of what the agent did and found, in order. The numbers are in the result files named in each entry.

## 2026-10-07, session 1 (results A–F)

See README.md §0–§9.

## 2026-10-07, session 2 (Insen away; continuing autonomously)

### A made exact (`analytic_A.py`, `results/analytic_A*.{json,txt}`)

- **What was done.** For σ = 0 and small θ, each branch's optimal biases lie on one fixed gate pattern, so the bias-profiled loss has an exact closed form. I expanded it symbolically to θ⁴ with general (p, c, η).
- **Agreement with the numerical solver:** 3.3e−17.
- **Linear term:** −2ηcpq θ, exactly. This is the "field".
- **Opposite-branch θ² coefficient at c = 0:** pq(p − ηD)/D. Its numerator is the same A = p − ηD that appears in the manuscript's cubic. It vanishes exactly at p_c.
- **Cubic coefficient, derived independently:** B = 2p²q²/D, which equals 2ηpq² at p_c and 0.145898 at η = 1/2. This is identical to 2C/K³. The existing K_η and C_η are re-derived from (A, B) to machine precision.
- **Consequence:** Result A no longer relies on inferring B from (K, C). The critical response 0.7344|c|^{1/2}, the same-sign response 4.236c and the first-order line 0.8664ε² all follow from exact Taylor coefficients.
- **Still a local statement.** It assumes the gate pattern stays fixed near θ = 0. That was checked numerically at 20 points, not proved globally.

### B: closing the open steps (`result_B_checks.py`, `spinodal.py`, `results/resultB/`)

- **Encoder re-optimisation is higher order.** I compared two precise bisections:
  - the noise-trained transition ε_train(σ), where θ and the biases are both trained under noise;
  - the fixed-encoder crossing ε_fix(σ), where the clean encoder is kept and only the biases are re-optimised under noise (this is the existing calibrated policy).

| η | σ | predicted | ε_fix | ε_train |
|---|---|---|---|---|
| 0.5 | 0.001 | 0.008316 | 0.008445 (+1.5%) | 0.008472 (+1.9%) |
| 0.5 | 0.003 | 0.017297 | 0.017795 (+2.9%) | 0.017910 (+3.5%) |
| 0.5 | 0.01 | 0.038597 | 0.04022 (+4.2%) | 0.03997 (+3.6%) |
| 0.48 | 0.003 | 0.017634 | 0.01814 | 0.01808 (+2.6%) |
| 0.52 | 0.003 | 0.016948 | 0.01744 | 0.01744 (+2.9%) |
| 2/3 | 0.003 | 0.013531 | 0.01419 | 0.01419 (+4.9%) |

  - ε_train and ε_fix differ by at most 0.7%.
  - Both approach the zero-fit prediction (B_cal/C)^{1/3} σ^{2/3}, and the relative correction shrinks as σ → 0.
  - The law holds at all four η tested, including η = 2/3, where the frozen coefficient vanishes. This makes the "heuristic step" numerically well supported, but it is still not a proof.
- **New result B2: the mono spinodal does not depend on σ.**
  - I expanded the noise-smoothed loss for |θ| ≪ σ, taking the Schur complement over the re-optimised bias. The curvature at mono is κ₀(p) = pq[p + qΦ(z_p) − η], where z_p solves p z + q[zΦ(z) + φ(z)] = 0. That is the same z as in the manuscript's v(p).
  - Finite-difference curvatures converge to κ₀ with an O(σ) correction of about +0.28σ (σ = 0.001: 0.02314 vs 0.02289 at p = 0.38).
  - Spinodal p_sp, where κ₀ = 0: η = 0.48 → 0.2604; η = 0.5 → 0.2791; η = 0.52 → 0.2985; η = 2/3 → 0.4628.
  - **Meaning: any nonzero training noise makes mono locally stable on [p_sp, p_c), an O(1)-wide window** (≈0.10 wide at η = 0.5), even though sharing is globally better below p_c − 0.83σ^{2/3}. The σ → 0 limit is singular. The barrier height is O(σ²), so stochastic optimisers can cross it at small σ, while gradient flow cannot. This is consistent with the hysteresis runs.

### Real-activation test (`real_protocol.md` written before running; `real_pairs.py`, `analyse_real.py`; `results/real/`; fig 7)

- **Data and setup.** The saved ResNet18 layer4 activations (1024 images × 512 channels; no new extraction), 200 channel pairs stratified by correlation, and 8 training-noise levels. It took about 27 minutes.
- **P1, sign rule: SUPPORTED.**
  - corr < −0.05 → opposite-sign storage in **37/37** pairs.
  - corr > 0.15 → same-sign storage in **17/17**.
  - In the middle band, a logistic fit gives a positive density coefficient, b2 = +14.5 ± 4.3. Denser pairs switch to same-sign at lower correlation, the direction the toy predicts.
  - Fig 7a shows the toy's two-branch structure in real data: a same-sign branch growing linearly with c, a deep opposite-sign branch, and coexistence at small positive c.
- **P2, bistability needs weak correlation: SUPPORTED.**
  - Bistable pairs: **36/67** in the lowest |corr| tercile, 20/66 in the middle, 6/67 in the highest.
  - Robustness check with a finer bias profile (`check_real_bistability.py`): 10/10 low-|corr| cases reproduce, with barriers of 1e−4 to 2e−3. Only 4/6 high-|corr| cases reproduce, so the high-tercile rate is if anything an overestimate.
  - Most bistable pairs have a deep opposite-sign minimum next to a near-mono or small same-sign minimum, as in the toy's c > 0 coexistence.
  - Caveat: this bistability is already present at σ = 0.005, so it tests the *clean* first-order structure, not the noise-induced one.
- **P3, noise shrinks the shared weight: NOT SUPPORTED.**
  - The median weak/strong ratio *rises* from 0.152 to 0.170 between σ = 0.005 and 0.4, then falls to 0.142 at 0.6.
  - Only 37.5% of pairs shrink.
  - Post-hoc note, labelled as such: the toy's noise penalty dominates only near p_c, but the median pair activity here is 0.55 > p_c = 0.38. So P3 was a poorly specified prediction for these dense channels. This explains the failure; it does not rescue the prediction.
- **Limits.** Pairs share channels, so they are not independent; the empirical distribution is fixed (n = 1024); features are continuous, so only qualitative directions were tested.

### Replication on class logits (registered in `real_protocol.md` before running; `results/real_logits/`; fig 8)

- **Setup.** 120 pairs of rectified ImageNet-class logits (first 1024 saved images), with the same code and the same unchanged predictions.
- **P1: SUPPORTED.** Opposite sign for corr < −0.05 in **49/49**; same sign for corr > 0.15 in **26/26**.
  - Middle band: the logistic fit is uninformative (near-separation, huge standard errors). Raw rates are in the predicted direction: sparse pairs are same-sign in 1/22, dense pairs in 8/23, even though the dense pairs have *lower* mean correlation.
- **P2: SUPPORTED.** Bistable in **23/40** of the low-|corr| tercile, 7/40 of the middle, 3/40 of the high. The fine-profile check reproduces 7/8 low-|corr| cases.
- **P3: SUPPORTED here.** The median weak/strong ratio falls from 0.550 to 0.449, and 71.7% of pairs shrink. Median activity here is 0.40, close to p_c. This fits the post-hoc explanation of the layer4 failure, but that explanation remains post hoc.

### Post-hoc refinement: where real pairs show branch coexistence (`branch_coexistence.py`, fig 9)

This is labelled post hoc. It counts only true *branch* coexistence: an opposite-sign minimum (θ < −0.1) together with a near-mono or same-sign minimum (θ > −0.05). Several minima within one branch, which come from finite-sample roughness, are excluded.

| Dataset | Low \|corr\| tercile | Mid | High |
|---|---|---|---|
| layer4 | 27/67 | 16/66 | 6/67 |
| logits | 21/40 | 7/40 | 2/40 |

- **The key match is the asymmetry.** Coexisting pairs sit overwhelmingly at small **positive** correlation (layer4: 43 positive, 6 negative; logits: 24 positive, 6 negative). Every negative case lies within −0.021 of zero.
- That is the toy phase diagram's structure (fig 5): a first-order line on the c > 0 side, extending only slightly onto c < 0, ending at the endpoint c_e.
- The sampled pairs include plenty of negative-correlation pairs (equal-count bins), so the asymmetry is not a sampling artifact.

### Escape statistics in the metastable window (`sgd_escape.py`, `results/escape/`)

- **Setting.** p = 0.29 at η = 0.5 and c = 0. This is inside [p_sp, p\*(σ)), so sharing is globally better and mono is metastable. Adam runs for 6000 steps from θ0 = −0.01.

| σ | Batch 8192 escaped | Batch 1024 escaped | Global gain of sharing |
|---|---|---|---|
| 0.003 | 16/16 | 16/16 | 2.1e−4 |
| 0.01 | 16/16 | 16/16 | 1.9e−4 |
| 0.03 | 9/16 | 10/16 | 3.1e−5 |

- **Gradient flow (exact loss, L-BFGS-B) stays at mono** for every σ tested: σ = 0.003 from θ0 = −0.001, σ = 0.01 from −0.003, and σ = 0.03 from −0.01.
- **Correction to my own first reading.** At small σ the mono basin is only about σ wide in θ. The θ0 = −0.01 start is *outside* that basin when σ ≤ 0.01, so those "escapes" are mostly an initialisation and step-size effect, not barrier crossing.
  - Check (`results/escape/stepsize_check.json`): σ = 0.003, θ0 = −0.001 (inside the basin), lr 3e−4. 4/6 runs remain near mono after 6000 steps; 2 are drifting out (−0.014 and −0.043).
- **Batch size** made no visible difference (9 vs 10 of 16).
- **Takeaway.**
  - The metastability is exact for deterministic training.
  - For stochastic training it matters when σ is comparable to the initialisation and learning-rate scales of the weak column. At σ = 0.03, about 40% of runs stay mono while sharing is optimal.
  - So which storage gets reported depends on the optimiser. This is a practical caveat for any "trained under noise" empirical claim.

### Refined critical endpoint c_e(σ) (`endpoint_refine.py`, `results/endpoint_refined/`, fig 10c)

- **Method.** One c per call. A 36-point p window above p\*(σ), and the exact landscape on 300 log-spaced θ down to 10⁻⁵. Bistable means at least 2 local minima.

| σ | 0.002 | 0.003 | 0.005 | 0.01 | 0.02 | 0.03 |
|---|---|---|---|---|---|---|
| \|c_e\| | 3.8e−4 | 5.6e−4 | 8.6e−4 | 1.38e−3 | 2.13e−3 | 2.33e−3 |

- **Precision is about ±5%.** Near the endpoint the bistable p window is narrower than the 0.001 p grid, and some detections were non-monotone in c (σ = 0.01, 0.02, 0.03). All tests are saved, including those.
- **Local log-log slopes** are 0.93, 0.86, 0.68, 0.62, 0.22. Equivalently, |c_e|/σ falls from 0.19 to 0.08.
- **Reading, labelled a conjecture.** As σ → 0 the trend approaches linear, c_e ≈ −0.19σ. That fits a simple picture: the field must overcome the restoring force of a mono well that is about σ wide, with curvature κ₀ = O(1), so h_e ~ κ₀σ. At larger σ the endpoint bends toward the deep-branch region.
- **Asymptotic exponent: not established.** My earlier naive σ^{4/3} guess is rejected.
- **Figure.** fig 10 adds (a) κ₀(p) against finite differences and (b) the transition location against the zero-fit prediction at 4 η.

### Exploratory: three features in one dimension (`fra3.py`, `results/three_feature/`)

- **Setup.** Independent Bernoulli(p) features, importances (1, 0.5, η3), clean training. Global search over the sphere: a coarse (a, b) grid, then Nelder–Mead from the 4 best points. Each solve takes about 4 s.
- **Result.** Feature 2 enters exactly as in the two-feature theory: continuously at p_c(0.5) = 0.382, with w2 = −0.019 at p = 0.37 (two-feature Kε = 0.0189). The same jump appears near p ≈ 0.21 (result E).
- **Feature 3 is never stored** for p ∈ [0.05, 0.44], at either η3 = 0.25 or η3 = 0.45.
  - Check at p = 0.05, η3 = 0.45: Nelder–Mead from six starts, including w2 = w3. Every start converges to w3 = 0, except one that finds a worse local minimum storing feature 3 instead of feature 2 (worse by 1.1e−3).
- **Reading.** A scalar ReLU code can filter interference for one opposite-sign partner only; a third feature necessarily shares a sign with one of the others. So for independent features in m = 1, the two-feature theory, and with it the existing critical law, appears to be the *complete* answer for any n, with the extra features dropped.
- **Limits.** Only n = 3, two values of η3, clean, independent features; numerical global search, not a proof.
- **Natural next question (not run).** Can a feature *positively correlated* with feature 1 enter as a same-sign partner? That would be correlation-enabled packing of three features in one dimension, and it follows directly from result A's field picture.

### Exploratory follow-up: correlation-enabled packing (C13 option in `fra3.py`; `results/three_feature/*_c13_*.json`)

- **Setup.** Features 1 and 3 have correlation c13; feature 2 is independent. Importances (1, 0.5, 0.45), clean training.

| c13 | p = 0.30: selected w | p = 0.15: selected w |
|---|---|---|
| 0 | (0.991, −0.131, 0) | (0.889, −0.458, 0) |
| 0.05 | (0.996, 0, +0.095) | (0.888, −0.458, +0.039) |
| 0.1 | (0.988, 0, +0.155) | (0.885, −0.458, +0.079) |
| 0.2 | (0.969, 0, +0.248) | (0.875, −0.458, +0.158) |

- **Sparse case (p = 0.15).** A positively correlated feature joins as a **same-sign** partner, *in addition to* the opposite-sign partner. That is **three features in one dimension**, beyond the independent-feature limit above.
- **Denser case (p = 0.30).** The correlated same-sign partner **displaces** the independent opposite-sign partner: feature 2 is dropped.
- **Reading.** This is result A's field acting in a larger system. Correlation opens the same-sign channel, which independent features cannot use. Packing capacity in one dimension therefore depends on the correlation structure, not only on sparsity.
- **Limits.** Exploratory: a single (η, p) slice, clean training, numerical search. It is not part of any claim yet.

## 2026-10-07, session 3 (continuing)

### Lemma closing Result A's gap (`gate_lemma.py`, `results/gate_lemma*.json`)

- **What it proves.** For σ = 0 and each output on each branch (opposite-sign and same-sign), the gate pattern used in `analytic_A.py` is the **unique global bias optimum for all sufficiently small |θ|**, at every interior feasible (p, c).
- **Method.** For fixed θ, the per-output loss in b is piecewise quadratic. I listed every piece and every breakpoint as a series in k = |θ|.
  - Every competing *interior* minimiser lies outside its own piece at leading order, so it is not a valid candidate.
  - Every *breakpoint* value exceeds the chosen value by a leading coefficient that is strictly positive (orders k⁰ or k²).
  - The chosen minimiser lies strictly inside its piece, at orders k⁰ or k¹.
- **The sign checks are symbolic, not just numerical.** Every leading coefficient factors into ratios of the feasible joint probabilities. The identities are checked with sympy and saved in `gate_lemma_factor_identities.json`:
  - cp² − cp − p² + p − 1 = −(1 − P01)
  - cp − c − p + 2 = 1 + P10/p
  - cp − c − p = −P11/p
  - cp − p + 1 = P00/q
  - (c − 1)(p − 1) = P10/p
  
  So the signs hold on the whole open feasible domain. A dense (p, c) grid confirms them as well.
- **Consequence.** Result A's expansion, F(θ) − F(0) = −2ηcpq·θ + κ±θ² + B±θ³ + …, is now a **local theorem**, with exact closed-form coefficients for all (p, c, η). The threshold "small |θ|" depends on (p, c) and is not uniform near the boundary of the feasible domain.
- **Still open.** Global selection over all θ for c ≠ 0. The existing global strip proof covers c = 0 only. The corollaries (field response, first-order line) are leading-order consequences of this local theorem plus that global input.

### Three-feature packing map (`packing_map.py`, `results/three_feature/packing_map.json`, fig 11)

- **Setup.** One code dimension, importances (1, 0.5, 0.45). Feature 2 is independent; feature 3 has correlation c13 with feature 1. That is 133 feasible (p, c13) points with p from 0.05 to 0.40 and c13 from −0.1 to 0.2, clean training.
- **c13 = 0.** Only feature 2 is ever added (as an opposite-sign partner), below p_c = 0.382. This reproduces the two-feature theory.
- **Any c13 ≠ 0 stores feature 3, with the sign of c13**, even c13 = ±0.01 or ±0.02. This is the field acting: there is no threshold. At sparse p, w3 grows roughly linearly in c13 (p = 0.1: 0.009, 0.019, 0.038, 0.075, 0.149 at c13 = 0.01, 0.02, 0.05, 0.1, 0.2).
- **Positive c13.** At sparse p, all three features are stored ({1, 2−, 3+}). Above a displacement line, feature 2 is dropped ({1, 3+}). That line moves to lower p as c13 grows: about p ≈ 0.34 at c13 = 0.01–0.02, falling to about 0.21 at c13 = 0.2.
- **Negative c13.** At c13 = −0.02 and p ≤ 0.175, *both* weak features are stored opposite-sign ({1, 2−, 3−}). Negative correlation with feature 1 makes a second opposite-sign partner affordable. At c13 ≤ −0.05, feature 3 displaces feature 2 entirely.
- **Reading.** In one dimension, *which* features get packed is decided by their correlations with the dominant feature. Independent features only ever get one slot. Correlated features enter through the field, and they can either add capacity or displace an independent partner. This is a concrete, testable "correlation decides packing" rule.
- **Limits.** Clean training, one importance vector, numerical global search (grid plus Nelder–Mead).

### Real triples test (`real_triples_protocol.md` written before running; `real_triples.py`; `results/real_triples/`; fig 12)

- **Setup.** 120 ResNet18 layer4 channel triples, 20 per c13 bin. Channel j is uncorrelated with both i and k. Clean training of the three-feature, one-dimension model, using global grid search plus Nelder–Mead. About 25 minutes.
- **T1, sign rule for the correlated third channel: SUPPORTED, 60/60.**
- **T3, correlation pulls feature 3 in: SUPPORTED.** Stored in 60/60 triples with |c13| ≥ 0.05, against 6/20 in the near-zero bin.
- **T2, displacement as registered (both strong bins pooled): NOT SUPPORTED.** Feature 2 is stored in 17/40 strong-bin triples, against 7/20 near zero.
- **Post-hoc structure, labelled as such. It matches the toy map in sign.**
  - When the uncorrelated feature 2 is stored, it is opposite-sign relative to feature 1 in **40/41** cases. That is the toy's opposite-sign slot.
  - Strongly negative c13 puts feature 3 in the *same* opposite-sign slot. Feature 2 is then stored in only 4/20 triples: displacement.
  - Strongly positive c13 uses the *same-sign* slot. Feature 2 is stored in 13/20, and **all three channels are stored together** in 13/20 (0.15–0.6 bin) and 11/20 (0.05–0.15 bin), against 0/20 near zero and 4/20 for strongly negative c13.
  - So in real data too, positive correlation adds a storage slot and negative correlation competes for the existing one. That is the asymmetry of fig 11.
  - My registered T2 pooled the two signs, which the toy map itself says behave oppositely. The registered result stands as a failure.
- **Limits.** Triples share channels, the empirical distribution is fixed, and features are continuous and dense.

### Quantitative linear response on real pairs (`real_linear_response.py`, `results/real*/linear_response.json`)

- **The field formula is exact on real data.** The measured linear term h = −∂F/∂θ at mono matches the bridge-review formula 2η·Cov(X1, X2) with correlation 0.999999 in both datasets; the maximum absolute difference is 1e−3.
- **Predicting the selected same-sign weight with θ_pred = h/(2κ₊), using κ₊ measured at δ = 2e−3:**
  - The ordering is right on layer 4: corr(pred, actual) = 0.92 over 112 pairs. It is poor on logits: 0.15 over 34 pairs.
  - The magnitude is **systematically overestimated by about 1.35–1.5×**, at every |θ\*| range.
- **Diagnosis (6 layer-4 pairs).** The secant curvature (F(θ) − F(0) + hθ)/θ² is small or even negative at θ ≲ 10⁻³. It rises to a plateau of 0.20–0.25 by θ ≈ 0.03–0.1. That plateau matches the curvature needed to reproduce θ\* (0.19–0.29).
  - So for continuous ReLU activations the loss near mono is *not* a clean quadratic. Likely cause: gates sweeping through the continuous activation density near zero adds non-analytic corrections. At tiny θ, finite-precision effects also add noise.
  - The Bernoulli expansion (S1) does not transfer quantitatively.
  - Linear response with the stiffness *at the right scale* is self-consistent, so it is not an independent prediction.
- **Verdict.** The field term transfers exactly; the stiffness does not. The real-data support for the field picture stays directional (sign, ordering), not quantitative.

### Compression axis: four features in two dimensions (`fra_nm.py`, `compression_theory.py`, `results/compression/`)

- **Setup.** Independent Bernoulli(p) features, importances (1, 1, 0.5, 0.5), shared encoder budget ‖W‖_F² = m = 2, clean training. Biases are profiled *exactly* by piecewise-quadratic enumeration. Global search uses structured plus random starts, each polished with Powell.
- **Numerical phases at η = 0.5:**
  - **Mono** for p ≥ 0.4225.
  - **One partner only**, for 0.20 ≲ p < 0.42. This breaks the symmetry between the two equivalent dimensions: energy moves *from the other important feature* into the dimension holding the partner, and that dimension's important feature is stored with amplitude > 1.
  - **Two partners**, one per dimension, at p ≤ 0.15. These exactly equal the two-feature solution: (0.8888, −0.4582) at p = 0.15.
  - p = 0.25 gave a non-decomposed configuration. It is unverified and may be a search artefact.
- **New result: the shared budget moves the storage transition up, to p_c^shared(η) = 1 − √((1−η)/(1+η)).**
  - Derivation: extend the exact opposite-branch closed form with an amplitude variable r² = 1 + u for the important feature, paid for by the donor (s² = 2 − r² − k²).
  - The Hessian in (k, u) at mono gives κ_eff = κ₋ − (cross term)²/(u-stiffness) = pq[ηp² − 2ηp + 2η + p² − 2p]/(p² − 2p + 2), up to sign.
  - κ_eff = 0 ⇔ (1+η)p² − 2(1+η)p + 2η = 0.
  - At η = ½: p_c^shared = 1 − 1/√3 = **0.42265**, against the fixed-norm 0.38197, which the same code recovers.
  - **Numerical bisection: transition in [0.4219, 0.4225]** (gain 8.8e−13 at 0.4225, consistent with the ε³ scaling). This matches the zero-fit prediction to about 1e−4.
- **Reading.** Compression is not just "two copies of the two-feature problem". The resource convention again decides the boundary: a per-dimension energy budget gives the existing p_c, while a shared budget gives a higher p_c with symmetry-broken single-partner storage. This ties directly to the manuscript's emphasis that resource matching must be stated.
- **Limits.** One importance vector, independent features, a numerical global search (12–22 starts per p). The theory is a local (Hessian) statement. The one-partner → two-partner boundary (between p = 0.20 and 0.15) is not explained.

### Compression follow-up: both branches, other η, and what the manuscript's special endpoint is

- **Same-sign branch under the shared budget** (`compression_theory_same.py`): κ₊,eff = 0 ⇔ **p = (3η − 1)/(η + 1)**. The fixed-norm same-sign instability is at p = 2 − 1/η, which comes from κ₊ = pq(1 − η(2 − p))/(2 − p).
- **Shared-budget checks, all zero-fit:**

| η | Branch | Predicted | Bisection bracket |
|---|---|---|---|
| 0.5 | opposite | 0.42265 | [0.4219, 0.4225] |
| 0.3 | opposite | 0.26620 | [0.26558, 0.26620] |
| 0.7 | same-sign | 0.64706 | Gain-threshold bracket [0.6456, 0.6463]; weight-criterion bracket [0.6463, 0.6475] (weight 0.0008, gain 2.6e−11 at 0.64625) |

  At η = 0.7 the *opposite* prediction (0.58) is not where storage begins, because the same-sign branch destabilises first. The run shows a same-sign partner (w = +0.039 at p = 0.6), as theory says.
- **Which branch goes first.**
  - Fixed norm: the same-sign branch destabilises first for η > 2/3. The two branches cross exactly at **(η, p) = (2/3, 1/2)**.
  - Shared budget: the crossing is at (0.6, 0.5).
- **Insight about the existing manuscript.** Its "singular endpoint" at η = 2/3, p_c = 1/2 (where B_frozen = 0 and the frozen and calibrated orderings disagree) is exactly the point where the opposite-sign and same-sign storage instabilities coincide, i.e. a bicritical point of the fixed-norm model. That gives a structural explanation for why it is special.
  - This is an observation: I have not re-derived B_frozen from this picture.

### Bicritical identity (`bicritical_identity.py`, `results/bicritical_identity.json`)

- **Exact identity, verified with sympy.** On the critical line η = p/D (where κ₋ = 0), the manuscript's frozen noise coefficient B_frozen = q(1 − 2p)/2 is proportional to the same-sign stiffness κ₊ = pq(1 − η(2 − p))/(2 − p):
  - **B_frozen = κ₊ · D(2 − p)/(2pq).**
  - Derivation: on the critical line, 1 − η(2 − p) = (1 − p)(1 − 2p)/D.
- **Meaning.** The frozen corrupted-risk penalty of the selected sharing code vanishes exactly where the same-sign storage direction goes soft. The manuscript's singular endpoint (η = 2/3, p = 1/2) is therefore not a coincidence: it is the bicritical point where both storage directions are soft. This upgrades the earlier "observation" to an identity.
- **Not established.** A similar statement for B_cal; I have not checked it.
- **B_cal checked.** No analogous simple proportionality: the ratios B_cal/κ₀ along the critical line vary from 6.6 to 46. The only exact statement is the trivial decomposition B_cal = B_frozen + G_mono(p), where G_mono = (1 + p)/2 − v(p) is mono's denoising gain from calibrating its bias. That gives B_cal = κ₊·D(2 − p)/(2pq) + G_mono(p) on the critical line. Recorded; no further claim.

### Trained networks confirm the compression phases (`train_compression.py`, `results/compression/trained_adam_v2.json`)

- **Setup.** Minibatch Adam on sampled data: n = 4, m = 2, Frobenius budget 2, η = ½, batch 4096, 8000 steps, 3 seeds per p. No exact solver involved.
- **0.20 ≤ p ≤ 0.38: every seed stores exactly one partner**, i.e. the symmetry-broken phase. Partner norms match the exact global optimum: p = 0.30 gives 0.205 / 0.203 / 0.206 (exact 0.204); p = 0.38 gives 0.073 / 0.069 / 0.066 (exact 0.069).
- **p = 0.40–0.42, between the fixed-norm p_c = 0.382 and the shared p_c = 0.4226:** 2/3, 2/3 and 1/3 seeds store a small partner (0.015–0.042). The exact weights there are tiny (0.02–0.05), close to SGD resolution, so this region is mixed, as expected near a continuous transition.
- **p ≥ 0.43: all seeds are mono**, as predicted.
- **p = 0.15:** 2 partners in 2/3 seeds (one seed is asymmetric, with norms 0.747 and 0.096); 1 partner in 1/3. This is near the 1 → 2 partner boundary, which is not derived.
- **Reading.** Ordinary training reproduces the shared-budget phase structure: partners are stored *above* the fixed-norm threshold, single-partner symmetry breaking happens, and the transition region falls where Proposition C predicts.

### The one-partner → two-partner boundary (n = 4, m = 2, η = ½; `results/compression/one_two_partner_bisection.json`)

- **Bisection of the global optimum:** the boundary is at p ∈ [0.1594, 0.1609].
- **It is first order.** Just above it, the optimum has one partner of norm 0.572, and the important features have unequal norms (0.926 and 0.903). Just below it, the optimum is the symmetric state with two partners of norm 0.449, both important features at 0.892, i.e. two copies of the two-feature solution. The partner configuration jumps discontinuously.
- **Reading.** Going from sparse to dense: symmetric two-pair storage, then a first-order switch to symmetry-broken one-pair storage at p ≈ 0.160, then a continuous transition to mono at p_c^shared = 0.4226.
- **Theory for the 0.160 point:** not derived (it is a crossing of two distinct branches).

### S4 sharpened: the first-order-in-σ correction to the mono curvature (`spinodal_first_order.py`)

- **Formula: κ_σ(p) = κ₀(p) − 2p z_p σ + O(σ²).** Note z_p < 0, so noise *stiffens* mono.
- **Where the terms come from.** At (θ, b1) = (0, z_pσ), every second-order term of the Gaussian-smoothed output-1 loss is exact up to exponentially small tails: g₀″ = 2Φ(z_p) and g₁″ = 2 − O(e^{−1/(2σ²)}/σ).
  - The θ-gradient vanishes exactly at c = 0, by independence plus bias stationarity.
  - The amplitude a = cos²θ adds G_a·a″/2 = −2p z_pσ, where G_a = 2p·z_pσ.
  - The cos θ factor on the noise scale enters only at O(σ²).
  - Output 2 is gate-open up to exponentially small tails and contributes −ηpq + O(σ²).
- **Check against all 12 saved finite-difference curvatures (σ = 0.001, 0.01, 0.03; p = 0.15–0.38).**
  - Before correcting, the error scales with σ (2.5e−4 at σ = 0.001, 8.6e−3 at σ = 0.03).
  - After correcting, the residual is ≤ 1.3e−4 and does *not* scale with σ. That matches the finite-difference step: δ/σ = 10⁻² is held fixed, so the step error is roughly constant.
- **Status.** This is now a proof sketch with explicit terms and exponentially small remainders; writing out the tail bounds is routine. It upgrades S4 from a leading-order statement to a leading-plus-first-order statement with a proof outline. The spinodal is therefore p_sp(σ) = p_sp − 2p z_pσ/κ₀′(p_sp) + O(σ²).

### Why S3 converges slowly (`results/resultB/correction_diagnosis.json`)

- **The controlling quantity** is how far the sharing code's gate sits from the ReLU kink, in units of noise: u = b1/σ. Here b1 = 0.30ε, consistent with b1\* ≈ P11 K ε/(1 − P01).
- **At the measured transition points:**

| σ | u = b1/σ | Relative deviation from (B_cal/C)^{1/3}σ^{2/3} |
|---|---|---|
| 0.001 | 2.52 | +1.6% |
| 0.003 | 1.75 | +2.9% |
| 0.01 | 1.15 | +4.2% |

- **Reading.** The leading law assumes the sharing gates are fully in the linear regime (u ≫ 1). Along the transition u ∝ σ^{−1/3}, so it grows only slowly, and the corrections are a function of u, not a simple power of ε.
- **The same caveat applies to the existing critical law** σ = tε^{3/2}: there u = 0.30/(t√ε), which diverges only like ε^{−1/2}. That explains why the manuscript's finite brackets approach their coefficients slowly.
- **Status.** Diagnosis only. The full correction function of u is not derived.

### Consistency pass (`consistency_check.py`, `results/consistency_check.json`)

- **Recomputed from the result files:** every headline count (pair sign rule, bistability terciles, triples T1–T3), the Monte Carlo z-score, the analytic-A coefficients, the gate-lemma flag, the compression brackets and the bicritical identity. All match the documents, with two corrections:
  1. **η = 0.7 compression bracket.** The bisection (gain threshold 1e−10) gives [0.6456, 0.6463], not the [0.6463, 0.6475] I quoted. That was the weight-based criterion. Both are now stated in LOG, STATEMENTS and LaTeX, and agreement is quoted as "within 1.5e−3" (README, addendum).
  2. **Layer-4 post-hoc coexistence count.** The saved list was rounded and shows one correlation as −0.0. Its true value is −0.00024, so "43 positive vs 6 negative" stands.

### A theory for the c < 0 critical endpoint (`endpoint_theory.py`, `results/endpoint_theory*.json`)

- **Mechanism.** In the scaled angle x = |θ|/σ near p_c, the noise-smoothed landscape is F(−xσ) − F(0) = σ²Φ(x).
  - Φ rises like κ₀x² inside the mono well.
  - Φ′ reaches a **local maximum ≈ 0.04 at x ≈ 1.8–1.95**. This is the maximum restoring slope of the mono well.
  - At larger x, Φ′ dips, and then the clean cubic B|θ|³ = Bσx³·σ² takes over.
- **Endpoint law.** A negative correlation adds a linear tilt −|h|σx, with |h| = 2η|c|pq. The near-mono minimum merges with the barrier when |h|/σ = (local max Φ′). Therefore
  - **|c_e| = σ·max Φ′ / (2ηpq)**, i.e. **linear in σ**. This explains the small-σ trend seen numerically and replaces my earlier naive σ^{4/3} guess.
- **Coefficient.** Local max Φ′ = 0.0385, 0.0393, 0.0412 at σ = 0.0005, 0.001, 0.002 (at p = p_c). This gives |c_e|/σ → about 0.16 as σ → 0.
- **Quantitative check at σ = 0.002.** The measured endpoint sits at p_e = 0.3848, slightly above p_c. Evaluating Φ there gives max Φ′ = 0.0448 and a **predicted |c_e|/σ = 0.189, against 0.1906 measured**. The measurement has a ±5% detection uncertainty.
- **The decline of |c_e|/σ at larger σ** (0.14 at σ = 0.01, 0.08 at σ = 0.03) is where the cubic term and the larger p-offsets matter. It is not derived.
- **Status.** A semi-analytic mechanism and law. Φ is computed numerically, not in closed form, and the endpoint location p_e is taken from measurement.

### Significance of the real-data contrasts, allowing for shared channels (`real_stats.py`, `results/real_stats.json`)

- **Method.** A channel-cluster bootstrap (2000 resamples): resample channels with replacement and keep a pair only if both of its channels were drawn. This respects the fact that pairs share channels. Fisher exact tests are also reported; they ignore that dependence.

| Contrast | Layer 4 | Logits |
|---|---|---|
| P2: bistability rate, low − high \|corr\| tercile | +0.45, CI [0.27, 0.63], Fisher p = 2e−8 | +0.50, CI [0.27, 0.71], Fisher p = 2e−6 |
| Post hoc: coexistence among \|corr\| < 0.1, positive − negative correlation | +0.39, CI [0.23, 0.55] | +0.69, CI [0.43, 0.93] |

- **Triples T3** (correlated channel pulled in, strong vs near-zero c13): Fisher p = 3e−11.
- **Reading.** The registered P2 and the post-hoc asymmetry are both well outside chance, even under dependence-respecting resampling.

### S3: the deviation from the leading law is accounted for (`S3_scaling_function*.py`, `results/resultB/S3_scaling_function*.json`)

- **Construction.** Write the sharing output-1 bias as b1 = σy. With the x1 = 1 gates treated as open, the calibrated sharing penalty is an explicit one-dimensional minimisation over Gaussian ReLU moments H:
  - Π(r) = min_y [P00 H(y) + P01 H(y − r) + P10((y − α)² + 1) + P11((y − α − r)² + 1)] − (clean loss)/σ²
  - with r = |sinθ cosθ|/σ and α = sin²θ/σ.
  - As r → ∞, Π → D, which recovers B_cal = D − v(p).
- **Crossing condition:** G_clean(p) = σ²[Π − v(p) + η sin²θ]. G_clean is the exact clean gain at p.

| σ | Leading law: error vs measured ε_fix | Scaling function, α dropped | Scaling function with α |
|---|---|---|---|
| 0.001 | +1.6% | −0.15% | **−0.18%** |
| 0.003 | +2.9% | +0.30% | **−0.10%** |
| 0.01 | +4.2% | +2.3% | **−0.73%** |

- **Reading.** The 2–5% deviation of S3 is explained by two explicit effects. First, the finite gate offset in units of noise (the scaling variable r ∝ σ^{−1/3}). Second, the amplitude offset α = sin²θ/σ, which is not small at σ = 0.01 (α ≈ 0.36). What remains is under 1% and comes from the neglected x1 = 1 gate tails and output-2 terms.
- Together with the ≤ 0.7% encoder re-optimisation effect (B′), S3's location is now quantitatively understood. A formal proof still needs remainder bounds for those neglected terms.

### Global selection with correlation: computer-assisted certificate (`certify_global.py`, `results/certificate_v2/`)

- **Method (σ = 0).**
  - Evaluate F(θ) exactly by vectorised enumeration of every piece and breakpoint of the bias problem. It matches the solver to 6e−17.
  - Use a rigorous Lipschitz bound |F′| ≤ L = 2(1 + 2√2)(2√2)(1 + η). This holds because an optimal bias can always be chosen in [−√2, 1 + √2], so |ReLU − t| ≤ 1 + 2√2, and |∂o/∂θ| ≤ 2√2.
  - Run branch and bound over θ ∈ [−π/2, π/2]: discard any interval with F(mid) − L|I|/2 > F_best + 1e−12.
  - Double precision, no directed rounding.
  - The first pass (v1) used a bound of 3.5 instead of 1 + 2√2, which is too small. It is kept in `results/certificate/`; v2 is the valid one. The outcomes are identical.
- **Result on a 64-point grid** (p ∈ {0.25, …, 0.45}, c ∈ {−0.05, −0.02, −0.005, 0, 0.002, 0.005, 0.02, 0.05}): every surviving set lies **entirely on one side**, where the field picture places it.
  - All c < 0: opposite-sign branch.
  - c = 0: opposite-sign for p < p_c; a small interval around θ = 0 (mono) for p ≥ 0.38.
  - c > 0: opposite-sign below the first-order line (p = 0.25 and 0.30 at c = 0.002 and 0.005), same-sign above it.
  - The certificate's classification matches the exact-solver sweep at 48 of the 49 overlapping points. The one exception is p = 0.38, c = 0, just below p_c. There the true opposite-branch gain is only 2.2e−9, and the certified surviving interval [−0.022, 0.0066] contains both mono and the true optimum θ = −0.0031. That is a resolution limit, not a contradiction.
- **Consequence.** The *global* branch-selection statements of S2 are now **certified on this grid**, not just observed numerically. The location of c\* comes from bisection, so the certificate confirms which side of the line each grid point is on. Away from the grid, S2 remains a leading-order statement.

### Triples replication on class logits (registered in `real_triples_protocol.md` before running; `results/real_triples_logits/`)

- **Setup.** 120 triples of rectified ImageNet-class logits, with identical code and settings.

| Test | Result | Status |
|---|---|---|
| T1: sign rule for the correlated third feature | 55/57 (96.5%; threshold 90%) | Supported |
| T2: pooled displacement | 29/40 vs 10/20 | Not supported (as on layer 4) |
| T3: correlation pulls feature 3 in | 57/60 vs 10/20, Fisher p = 2e−5 | Supported |
| T4 (newly registered): three-feature storage, c13 ≥ 0.05 vs ≤ −0.05 | 36/40 vs 8/20, Fisher p = 8e−5 | Supported |
| T5 (newly registered): uncorrelated partner kept, strong negative vs strong positive bin | 11/20 vs 18/20, Fisher p ≈ 0.03 | Supported |

- When the uncorrelated partner is stored, it is opposite-sign in 80/82 cases.
- **Reading.** The asymmetry found post hoc on layer 4 (positive correlation adds a same-sign slot, negative correlation competes for the opposite-sign slot) is now **confirmed prospectively** on a second representation. Pooled displacement fails again, because the two signs act in opposite directions.

### Compression for general m (`compression_theory_m.py`, `train_compression_m.py`, `results/compression/*general_m*`, `trained_adam_m*.json`)

- **Theory.** With n = 2m features (m important, m weak), the first partner can draw energy equally from the m − 1 other important features, so the donor cost becomes pq(u + k²)²/(m − 1). The opposite-branch Hessian gives
  - **p_c^shared(η, m) = [m(1+η) − √(m(m(1−η)² + 4η(1−η)))] / (2(m + η − 1)).**
  - This recovers the m = 2 result exactly.
  - At η = ½: 0.4226 (m = 2), 0.4417 (m = 3), 0.4531 (m = 4), and → η as m → ∞.
  - Reading: the more dimensions there are to borrow from, the earlier, i.e. at denser p, the first partner is stored.
- **Trained-network check** (Adam, Frobenius budget m, 2–4 seeds per point):

| m | Predicted threshold | p = 0.40 | p = 0.43 | p = 0.45 | p = 0.47 |
|---|---|---|---|---|---|
| 2 | 0.4226 | 2/3 stored (mean norm 0.026) | 0/3 | — | — |
| 3 | 0.4417 | 4/4 (0.058) | 2/4 (0.013) | 0/4 | — |
| 4 | 0.4531 | 3/3 (0.084) | 3/3 (0.020) | 1/3 (0.008) | 0/3 |

- **Reading.** The predicted ordering in m holds: storage persists to higher p, and partner norms at fixed p grow with m. The transition regions sit where predicted, within SGD resolution.
- **Limits.**
  - The exact global optimum for m ≥ 3 was not computed: Powell in 18 dimensions was too slow (a single m = 3 solve timed out).
  - The trained check is qualitative near threshold, because partner norms there are close to SGD noise.
  - Assumes equal energy drawing from all donors, which the symmetric Hessian supports.

### Training noise in the compression setting (`train_compression_noise.py`, `results/compression/trained_adam_noise.json`)

- **Setup.** n = 4, m = 2, shared budget, η = ½, Adam with isotropic code noise h = Wx + σZ, 3 seeds.

| σ | Partner stored | Partner absent |
|---|---|---|
| 0 (earlier) | p ≤ 0.41 (one partner, small norms near threshold) | p ≥ 0.43 |
| 0.03 | p = 0.28 in 3/3 (norm ≈ 0.22); p = 0.31 in 2/3 (norm ≈ 0.155) | p ≥ 0.34 in all seeds |
| 0.1 | p = 0.20 in 2/3 (norm ≈ 0.50) | p ≥ 0.25 in all seeds |

- **Reading.** Two predictions carry over from the one-dimensional theory (S3/S4) to the compression setting:
  - **The transition is abrupt.** Partners appear at large norm or not at all; there are no small partners near the threshold, unlike σ = 0.
  - **It shifts to sparser p.** At σ = 0.03 the shift is about 0.09–0.11 from 0.4226; the one-dimensional law gives 0.080 for comparison.
  - **Seed dependence at the edge** (2/3 storing at p = 0.31 and p = 0.20) is the metastability signature.
- **Status.** Qualitative transfer only. No shared-budget noise coefficient has been derived.
- **Heuristic coefficient** (`results/compression/noise_shift_prediction.json`).
  - The shared-budget clean gain near its threshold scales as C′ε³ with C′ ≈ 0.267 (exact solver; gain/ε³ = 0.277, 0.271, 0.267 at ε = 0.04, 0.02, 0.01).
  - Taking the calibrated penalty as B_cal evaluated at p0′ = 0.4226 (0.122) gives the predicted noise-trained threshold p0′ − (B/C′)^{1/3}σ^{2/3}: **0.348 at σ = 0.03 and 0.257 at σ = 0.1**.
  - Trained networks: storage ends between 0.31 and 0.34 at σ = 0.03, and between 0.20 and 0.25 at σ = 0.1.
  - So the predictions sit 0.01–0.04 above the trained edges. That is the expected direction, since stochastic training from random initialisation is biased toward the metastable mono state (S6), and finite-u corrections apply at σ = 0.1.
  - Heuristic; not a test of a derived coefficient.

### Note on floating-point rigour of the certificate

- **Error estimate.** Each exact F(θ) evaluation in `certify_global.py` is at most about 200 floating-point operations on quantities of magnitude ≤ 10, using two cos/sin calls that are correctly rounded to within 1 ulp. A standard forward error bound gives an absolute error of roughly 200 × 2⁻⁵² × 10 ≈ 4e−13.
- **Why the 1e−12 margin is enough.** The margin exceeds this bound. F_best is an *attained* value, so its own error is covered in the same way.
- **Status.** The grid certificate is rigorous modulo this hand error analysis. It is not interval arithmetic; replacing the evaluations with mpmath.iv would make it fully formal.

## 2026-10-07: response to the GPT review (`../claude_agen_review_bygpt/`)

I checked each blocking point against my own code and accept all four. Repairs are pending the user's go-ahead.

1. **Sign error.** `analytic_A.py` used A = −dκ₋/dp. With ε = p_c − p it must be +dκ₋/dp. The magnitudes of K and C were right, but my claim of a "signed" re-derivation was wrong, and the LaTeX repeats the error. For c < 0 the response should read √(−h/(3B)); the 0.7344 coefficient is correct.
2. **Missed noisy well.** Confirmed independently. At p = 0.36413, σ = 0.003, the sharing well sits at θ ≈ −0.0276 and is only about 0.006 wide. My exact small-angle grid has points at 0.025 and 0.032, and both lie *above* F(mono), so `solve()` returned mono.
   - This invalidates the ε_train brackets at σ = 0.001 and 0.003. The reviewer's crossings are 0.0084571 and 0.0177810.
   - It also invalidates my "trained vs fixed encoder differ ≤ 0.7%" comparison as stated: with the correct crossing the two essentially coincide.
   - The noise sweeps (figs 3 and 5) used the same solver, so their jump locations need rerunning with a fixed search. Results built on exact landscapes (bistability, endpoint, spinodal, hysteresis) are unaffected.
3. **Bootstrap.** `set(rng.choice(...))` discards multiplicities, so it is random subsampling, not a cluster bootstrap. The CIs are withdrawn as stated.
4. **Certificate count overstated.** 60 ranges are strictly signed and 4 straddle zero. A range that straddles zero does not prove mono, so "63/64 certified" is withdrawn.

Also agreed (scope): the real tests fit a compressor to the pooled empirical distribution; hidden channels and logits come from one network; the compression threshold is a one-partner-path Hessian result; the floating-point margin is a hand estimate, not interval arithmetic.

## 2026-10-07: repairs completed (`repair_v1/`)

R1 (signs), R2 (search bug, all bisections and sweeps rerun), R3 (channel-disjoint Fisher tests replace the bootstrap) and R4 (certificate and scope labels) are done. Details are in `repair_v1/CORRECTIONS.md`; the reviewer entry point is `repair_v1/README_FOR_GPT.md`.

Headline changes:
- The noise transitions at σ = 0.001 and 0.003 were corrected to match the audit.
- No figure's transition location moved.
- The registered T5 on logits is not supported under valid inference.
- The certificate covers 60/64 points.


## 2026-10-07: repair_v2 (editorial, after the second GPT review)

- Added `repair_v2/STATUS.md`: one status label per claim.
- Added `repair_v2/CORRECTIONS_v2.md`: wording downgrades for statistics, search and the global-optimum statements.
- Added `repair_v2/derivation_section_v3.tex`: status-labelled; compiles to 6 pages.
- Added `repair_v2/ROBUSTNESS_PROTOCOL_DRAFT.md`: **not run**.
- No new computations.


## 2026-10-07: repair_v3 (corrections, frozen protocol, one bounded run, stopped at the precision gate)

See `repair_v3/RESULTS.md` and `repair_v3/README_FOR_GPT.md`.

- One crossing pair out of 12; its forecast was not informative.
- The final-evaluation images were not used.
- The controls and the retrospective pipeline check are consistent with the sign of the theory coefficient B.
- An independent agent recomputation confirmed the stop decision.
