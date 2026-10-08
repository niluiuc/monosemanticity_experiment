# Mathematical prediction statement (written before any new data are touched)

**Question (Project 1).** For two real features, does sharing beat monosemantic retention on clean held-out data? And at what Gaussian code-noise level σ does corruption reverse that advantage?

## 1. Which existing result applies, and whether its assumptions hold

| Existing result | Applies to these real activations? |
|---|---|
| Bernoulli critical law: σ ~ ε^{3/2} near the storage onset, coefficient √(C/B_cal) | **No.** It needs an independent-Bernoulli storage onset. The bridge review proved that nonzero covariance between nonnegative features removes the exact mono optimum, so these pairs have no onset and no ε. The exponent is not tested here. |
| Support bound: under calibration, a crossing eventually occurs at large σ | **Yes, but uninformative.** It guarantees that a crossing exists, not where it is. Finding a reversal therefore establishes nothing by itself. |
| The *mechanism* behind the manuscript's calibrated coefficient, B_cal = D₀ − v(p₀): sharing pays the full linear-regime noise on every open gate, while mono's retained feature sits exactly at the ReLU kink on its zero-valued images and is partly denoised, giving v(p) | **Yes, at leading order in σ**, for any finite empirical distribution with frozen encoders (derivation in §2). This is the theory-content prediction tested here. |

## 2. The leading-order noise coefficient for an arbitrary empirical distribution

**Setup.** Freeze the encoders and the clean (σ = 0) biases. Write the per-image pre-activation of output i as μ_{n,i} = w_i (w·x_n) + b_i, with code-noise scale s_i = |w_i|σ.

**Per-image noise penalties as σ → 0:**

- **Gate open** (μ > 0, at a fixed distance from 0): E[(μ + s_i Z − t)²] − (μ − t)² = s_i² + (exponentially small terms). The penalty is w_i²σ².
- **Gate closed** (μ < 0, at a fixed distance from 0): the penalty is exponentially small.
- **Calibration:** re-fitting the biases changes the loss only at higher order (envelope theorem), unless images sit *exactly at* a kink.
- **Mono retained feature r** (w = e_r, clean optimal bias 0): every image with x_r = 0 sits exactly at the kink. Re-fitting the bias to zσ gives the coefficient v(p_r) = min_z [p_r(1 + z²) + (1 − p_r)H(z)], where p_r is the fraction of images with x_r > 0 and H(z) = (z² + 1)Φ(z) + zφ(z). This is the *same* function v that appears in the manuscript's B_cal.
- **Mono omitted feature:** its weight is zero, so its constant reconstruction receives no noise.

**Leading-order law.** This gives

  **Δ(σ) = Δ(0) + B σ² + o(σ²),  with  B = Σ_i η_i w_i² f_i − η_r v(p_r),**

where f_i is the fraction of images whose output-i gate is open in the sharing model.

**Theory prediction for the crossing:**

  **σ\*_th = √(G/B), where G = −Δ(0) > 0 is the clean sharing advantage and B > 0.**

If B ≤ 0, the theory predicts that the sharing advantage *grows* at small noise, so it predicts no crossing at small σ and gives no location.

**Checks of the formula:**

- **Reduction to the existing coefficient.** In the Bernoulli model the formula reduces exactly to the manuscript's B_cal = D₀ − v(p₀). With the clean-selected geometry at p = 0.30, 0.25 and 0.34, it matches finite-σ calibrated computations to all printed digits (B = 0.26354, 0.33035, 0.21384), at σ = 0.0005–0.002.
- **Retrodiction (not evidence).** For the archived pair 281/207, the archived result shows sharing's advantage growing with noise, which corresponds to B < 0. Whether the formula gives B < 0 there is checked as a pipeline check in the run log.

**Status: [L], a leading-order derivation.** Its remainder is not controlled when σ\* is comparable to the distance of many images from a gate. For continuous features with mass near zero, there are additional O(σ³) terms.

## 3. Applicability check (declared now, evaluated on prediction images only)

For each pair, compute:
- the fraction of prediction images with any sharing pre-activation |μ_{n,i}| < 2σ\*_th;
- the fraction with 0 < x_r < 2σ\*_th for the retained feature.

If either fraction exceeds 0.20, the theory prediction is labelled **"outside its asymptotic domain"** before final evaluation. It is still reported, but cannot PASS or FAIL as a test of the theory.

## 4. What would support, contradict, or leave it unresolved

There are two distinct forecasts for each crossing pair. Both are frozen before final evaluation.

1. **Empirical forecast σ\*_emp.** The crossing of Δ on the prediction images, using the same frozen models. **What it tests:** held-out transfer of the sharing–mono tradeoff on real features. **What it does not test:** the critical law.
2. **Theory forecast σ\*_th = √(G/B)**, from §2.

**Agreement rule (per GPT's decision).** D = log(σ\*_test / σ\*_forecast).

| Outcome | Condition |
|---|---|
| **PASS** | The 98.75% interval for D (Bonferroni over ≤ 4 pairs) lies inside (−log 1.5, log 1.5) |
| **FAIL** | The interval lies entirely outside that range, or no crossing is observed where one was predicted with the test band below zero |
| **INCONCLUSIVE** | Otherwise |

**Precision gate before final evaluation.** A forecast is evaluated only if:
- the clean advantage is resolved;
- at least 95% of bootstrap resamples have a crossing in [0.05, 0.9];
- the projected half-width for D is at most 0.20.

If no crossing forecast passes the gate, stop before final evaluation and report that.

**Controls** (predicted to have no crossing in range): PASS means the test band stays below 0 on [0, 1]; FAIL means it lies above 0 somewhere; otherwise INCONCLUSIVE. A control PASS means only "no resolved crossing within the prescribed range".

## 5. What a successful run can and cannot establish

**It can establish:**
- that sharing's clean reconstruction advantage reverses under code noise on held-out real activations, at a forecastable location;
- whether the leading-order gate/kink law, the real-data analogue of the manuscript's B_cal mechanism, predicts that location.

**It cannot establish:**
- the Bernoulli critical exponent;
- robustness of the native network to input corruption;
- results for other networks.

The results are conditional on one network, the fitted compressors, and pairs selected by a fixed rule on reused cached data.
