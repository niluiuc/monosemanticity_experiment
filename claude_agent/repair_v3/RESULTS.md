# Bounded held-out robustness test: results (run once; stopped at the precision gate)

**Outcome:** no informative crossing forecast, so the run **stopped before final evaluation**, exactly as the frozen protocol prescribes. The 1792 final-evaluation (E) images were never loaded for any selected pair.

**The full process:** `PREDICTION_STATEMENT.md` → `PROTOCOL_FROZEN.md` → `rt_select.py` → `rt_predict.py`, then an independent recomputation (`results/independent_stop_check.md`).

## 1. Side-by-side: mathematical prediction vs observation

### Crossing pair (700, 890)

The only qualifying crossing candidate out of 12.

| Quantity | Value | Notes |
|---|---|---|
| Clean advantage G = −Δ_P(0) | 0.0151 | 98.33% band [−0.086, +0.047] includes 0: **not resolved** |
| Empirical forecast σ\*_emp | 0.525 | Only 48% of resamples cross in [0.05, 0.9] (independent check: 43.6% on a coarser grid). Projected h = 1.65 against a gate of 0.20: **imprecise** |
| Theory forecast σ\*_th = √(G/B) | 0.558 (B = 0.0485) | B > 0 in 75% of resamples; h = 1.64. 97% of images are within 2σ\* of a sharing gate, so it is **outside its asymptotic domain** |
| Gate verdict | Fails | Empirical gate: fail. Theory gate: fail ("outside asymptotic domain") |

### Control pairs

| Pair | Theory B | Theory prediction | Observed on P (98.33% band) |
|---|---|---|---|
| (471, 649) | −0.091 | Sharing advantage grows at small σ; no small-σ crossing | Band below 0 on all of [0, 1] |
| (417, 919) | −0.144 | Same | Band below 0 on all of [0, 1] |

### Pipeline check (retrospective; archived pair 281/207, archived convention)

| Quantity | Value | Notes |
|---|---|---|
| Archived Δ curve | Reproduced to 1.3e−9 | Encoder and training losses identical |
| Theory B | −0.056 | Predicts sharing's advantage grows with noise. The archived data show this: the slope (Δ(σ) − Δ(0))/σ² is −0.059 at σ = 0.073 |

This uses archived, already-examined data, so it is not evidence.

## 2. Discrepancies and what they mean

- **Point estimates agree; precision does not.** For the crossing pair, the empirical and theory forecasts agree (0.525 vs 0.558), but neither is precise. The pair's clean advantage on the prediction images is about 0.015 with a standard error of about 0.03. Any crossing location is then dominated by sampling noise in G. The point agreement is suggestive, not evidence.
- **The clean sharing advantage is fragile out of sample.** In the screening, 4 of 12 pairs lost their training advantage on held-out selection images, and the one crossing pair's advantage is unresolved on the prediction images. With 256 training images, the scalar sharing compressor's clean advantage on these features is often small and fragile. That limits *any* forecastable reversal, theory or empirical.
- **The theory's asymptotic assumption fails here.** The leading-order law needs most images far (relative to σ\*) from every gate. Real rectified logits put most images near a sharing gate at the relevant σ, so for crossing locations of order 0.5 the law is outside its domain. In the retrospective pair and both controls, B < 0 correctly signalled "no small-noise crossing": the sign prediction worked there, but none of those were final-evaluation tests.

## 3. What this run establishes, and what it does not

**Establishes:**
- For this network and these pre-specified rules, a bounded forecastable reversal test **could not be made informative**. Only 1 of 12 candidates was a crossing candidate, and its forecast failed the precision gate.
- This is a reportable negative or inconclusive finding about the *real-feature* side of the sharing–mono tradeoff.

**Does not establish:**
- That reversals do not occur.
- That the theory is wrong.
- Anything about the Bernoulli critical law or native-network robustness.

The E images remain unused and available for a future, separately approved protocol.

## 4. Firewall and integrity

- Selection used train and S. Forecasts used calibration and P.
- E rows were never loaded for the selected pairs' columns. The retrospective pipeline check loaded rows 512:4608 **only for logits 281/207**, which are archived and excluded from this study.
- The independent recomputation (an agent with its own code) loaded only the train, calibration and P rows.
- `results/FROZEN_STATE.json` holds SHA-256 hashes of every script and result at the stop decision.

## 5. What could be done next (needs your and GPT's approval; not run)

1. **A sign-of-B test instead of a crossing test.** This is the theory's most robust real-data content: the sign of the initial slope of Δ(σ) should equal the sign of B. It can be tested prospectively on many pairs with frozen models on P or E images, and it needs no resolved crossing. It directly tests the kink-denoising mechanism, the real-data analogue of B_cal.
2. **A larger training set for the encoders,** so the clean advantage is resolved. That would mean reallocating images, so it requires a new protocol decision.
3. **Accept this as the bounded result** and write it into the paper as a limitation together with the sign-of-B observations.
