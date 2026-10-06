# Project 1: clean training, interference and noisy concept detection

6 October 2026. This is a bounded continuation of the monosemanticity / superposition-to-robustness project. It contains derivations, controlled toy experiments, original outputs and independent reviews. Project 2, recursive training and real-model transfer have not been executed here.

## Research question and motivation

At fixed representational capacity and encoder energy, when does storing concepts together help clean prediction, and when does it cost robustness? The intended contribution is a quantitative account of the effects of activation frequency, feature load and importance, followed by a small real-model test.

The literature audit found that feature packing, generic superposition/noise tradeoffs, the squared alignment statistic and several interference bounds already exist. Merely observing those phenomena again is insufficient. The specific missing link addressed here is:

**Clean objective → selected geometry and decoder biases → risk under a specified corruption.**

Previous prescribed encoders could give exact risk formulas without showing that training would select them. The two-feature setting lets us test that link with exact population calculations. This is the smallest useful check, not the full load phase diagram. See the [literature audit](../literature_review/novelty_audit.md) and the historical [plan](../plan.md).

## What is modeled

Two independent concepts satisfy `b_i ~ Bernoulli(p)`. One code dimension stores them through a row encoder `w=(w_1,w_2)` with `w_1²+w_2²=1`. The tied decoder reconstructs

\[
G=w^\top w,\qquad \widehat b_i=\operatorname{ReLU}((Gb)_i+\beta_i).
\]

Training minimizes the exact four-state population objective

\[
L(w,\beta)=\sum_{i=1}^2 I_i\sum_{b\in\{0,1\}^2}P_p(b)
  \left(\operatorname{ReLU}((Gb)_i+\beta_i)-b_i\right)^2.
\]

This is a **reconstruction** objective. Binary detection is a distinct evaluation. A better reconstruction value need not imply a better detector.

The corruption is scalar Gaussian noise in code space: `h=w b + eta`, `eta ~ N(0,sigma²)`. Actual decoder detection is the strict rule `ReLU(w_i h + beta_i) > .5`. For a nonzero stored column and positive sigma, its exact feature error is

\[
r_i(\sigma)=\sum_b P_p(b)\,
\Phi\!\left(\frac{(1-2b_i)((Gb)_i+\beta_i-.5)}{\sigma |w_i|}\right).
\]

Zero-noise and zero-column cases are evaluated separately. The reported weighted detection error is `I_1 r_1 + I_2 r_2`, a sum, not an average. All feature false-positive/false-negative probabilities are retained. A separately labeled centered midpoint detector is also evaluated; it does not replace the actual decoder.

This is ordinary noise robustness under the stated distribution. It does not establish adversarial robustness, OOD generalization or AI safety. It does not treat an SAE dictionary extracted from a real model as automatically equivalent to this planted-feature Gram matrix.

## Settings, stopping and archive policy

The [initial protocol](protocol.md) was recorded before the runs:

- Six cases: `p=.05,.20,.50` and importance `[1,1]` or `[1,.5]`.
- Six seeds per case, 4,000 projected-Adam updates each, learning rate `.01`.
- Exact population loss; tied ReLU decoder; encoder energy one throughout.
- Fixed angular diagnostic with 361 regular angles and two supplied pair candidates. A grid is not a global proof.
- Gaussian code-noise standard deviations `0,.05,.15,.30,.60`.
- Both monosemantic retention controls with optimal clean biases, and the clean-preferred control identified independently of noisy performance.

The [bounded follow-up protocol](followup_protocol.md) was recorded after the independent review found a solver blocker. It authorized only two deterministic angle-descent diagnostics (`p=.05,.20`, importance `[1,.5]`) and one mathematical global certificate attempt (`p=.20`, importance `[1,.5]`). It did not authorize a broad optimizer search, new loads, pretrained models or diffusion training.

Original run directories are immutable. Failed convergence checks, unfavorable comparisons, zero-noise rounding discrepancies and source snapshots are retained. Any later numerical or documentation correction is recorded separately.

## Mathematical findings and their status

The [student derivation](math/student_derivation.md) and [independent teacher review](math/teacher_review.md) establish the following within this toy family:

1. At fixed geometry, scalar decoder-bias minimization is globally solved by a finite comparison of ReLU breakpoints and feasible quadratic stationary points. Importance changes geometry selection, but a positive importance weight does not change the optimal bias of its own feature at fixed geometry.
2. For an equal-amplitude antipodal pair and `p<=.5`, the optimal bias is `p(1+p)/(2(1-p+p²))`. The actual detector threshold is `.5` minus this learned bias, rather than a supplied midpoint.
3. At `p=.5` and equal importance, the global squared column norms are `(1+1/sqrt(2))/2` and `(1-1/sqrt(2))/2`; both relative-sign sectors attain loss `(9+2sqrt(2))/48 = .2464255651`. Equal-amplitude pair and mono loss `.25` are higher.
4. At `p=.5`, importance `[1,.5]`, the globally optimal geometry retains only the more important concept, with loss `.125`.
5. At `p<.5` and unequal importance, the equal antipodal pair has a nonzero descent direction. Treating it as the trained optimum would be wrong.

The bounded [one-case certificate](math/low_p_certificate.md) further gives the global clean optimum for `p=1/5`, importance `[1,1/2]`:

\[
w^*=\frac{(1,t^*)}{\sqrt{1+t^{*2}}},\qquad
20t^{*3}+175t^{*2}-60t^*-59=0,
\quad t^*\approx-.44209023902340024406.
\]

Its biases and loss are

\[
\beta_1^*=\frac{t^*(5t^*-1)}{21(1+t^{*2})},\qquad
\beta_2^*=\frac{1}{5(1+t^{*2})},
\]
\[
L^*=\frac{905t^{*4}-320t^{*3}+410t^{*2}+441}
 {5250(1+t^{*2})^2}\approx .07775208251629429 < .08=L_{\rm mono}.
\]

This computer-assisted certificate compares finite feasible bias branches using exact rational root isolation and objective bounds. It is not a numerical scan. The [independent mathematical review](math/teacher_low_p_review.md) passed, with no material repair required. A fresh reproduction and a different active-subset construction both identify the same optimum; the alternative construction shares the reviewed algebraic root backend, as explicitly disclosed. The p=.05 angle solution is only locally stationary; it has no global certificate in this record.

These are correctness statements under specified assumptions. Scientific novelty, a general frequency/importance law, the variable-load boundary and real-model transfer remain separate unresolved questions.

## Numerical results, including unfavorable outcomes

The [initial report](toy/report_v1/results.md) retains all 36 trainings. Twenty-seven pass the loss-stability diagnostic and nine fail. Some trajectories remain nonstationary despite nearly flat loss; loss stability is not convergence. In particular, the unequal-importance low-frequency projected-Adam runs stall near the equal pair even though the mathematical descent direction and angular grid show lower loss.

The follow-up angle solver resolves that bounded optimization blocker. The [full report](toy/angle_diagnostic_results.md) and [independent review](review/angle_teacher_review.md) give:

| p | Accepted updates | Final angle | Clean weighted MSE | Absolute angle gradient |
|---|---:|---:|---:|---:|
| .05 | 1,279 | -.5745808452 | .01774288054 | 9.978e-9 |
| .20 | 678 | -.4162567729 | .07775208252 | 9.792e-9 |

All accepted trial steps were `.1`; no halving or added starts were used. At p=.20, the local solver agrees with the separate global certificate, rather than supplying that proof itself.

Actual-decoder weighted detection errors, rounded for this display only:

| p | Code | sigma=0 | .05 | .15 | .30 | .60 |
|---|---|---:|---:|---:|---:|---:|
| .05 | Angle solution | .027500 | .027500 | .028901 | .058316 | .223667 |
| .05 | Clean-preferred mono | .025000 | .025000 | .025429 | .072790 | .227328 |
| .20 | Angle solution | .100000 | .112228 | .117826 | .159442 | .310097 |
| .20 | Clean-preferred mono | .100000 | .100000 | .100429 | .147790 | .302328 |

At p=.20, the reconstruction-optimal mixed code never detects the weaker concept using the trained decoder's `.5` threshold, despite its nonzero encoder column. Its clean detection ties mono, and it is worse at every positive noise level tested. At p=.05, the mixed code is worse at low noise but better at `.30` and `.60`. Neither outcome supports a universal statement that superposition always helps or always hurts robustness.

The original p=.5 unequal-importance run also contains material zero-noise float64 rounding discrepancies for nearly dropped columns. The algebraic threshold and direct ReLU implementations are both retained in the [independent toy review](review/toy_teacher_review.md). Those threshold coincidences are not evidence of recovered concepts.

## Where to inspect the evidence

- `math/`: derivations, verification scripts, teacher review, exact certificate and complete candidate ledger.
- `toy/run_v1/`: initial raw settings, environment, all 36 trajectories, grid, biases, 960 detector/noise rows, source snapshots and hashes.
- `toy/run_angle_diagnostic_v1/`: follow-up raw settings, all iterates and Armijo trials, bias branches, 60 detector/noise rows, source snapshots and hashes.
- `toy/report_v1/` and `toy/angle_diagnostic_results.md`: interpretation saved separately from raw outputs.
- `review/`: independent replay, active-subset bias checks, direct gradient checks, Gaussian risk checks and review reports.

The delivery ZIP and its SHA-256 sidecar are in the workspace's `output/` directory. The ZIP preserves this directory layout, the living plan and the literature audit/index; the full archived literature PDFs remain in the workspace. `package_results.py` creates a fresh archive, verifies every delivered file and refuses to overwrite a prior artifact.

The initial independent audit reproduced all 36 trajectories exactly in the recorded environment and verified 163 archived hashes. The angle audit verified 21 hashes, all 1,959 recorded iterates and all 60 risk rows. An exact rerun across different numerical libraries is not promised; the recorded numerical environment and tolerances are explicit.

## Reproduce without overwriting the original runs

Use Python 3.12 or later and the packages in `requirements.txt`. The archived environment JSON files give the exact Python/library versions used. From the repository root, the commands below use a working `python` interpreter; the bundled interpreter used here is recorded in the environment files.

```powershell
# Check the original saved initial experiment; does not train new cases.
python project1_toy/focused_bridge_2026-10-06/review/verify_toy.py --report project1_toy/focused_bridge_2026-10-06/review/reproduction_audit.json

# Reproduce the initial scientific protocol into a fresh directory.
python project1_toy/focused_bridge_2026-10-06/toy/run_bridge.py --output project1_toy/focused_bridge_2026-10-06/toy/reproduction_v1

# Reproduce the two bounded angle diagnostics into a fresh directory.
python project1_toy/focused_bridge_2026-10-06/toy/run_angle_diagnostic.py --output project1_toy/focused_bridge_2026-10-06/toy/reproduction_angle

# Check the original angle archive; updates only its review JSON.
python project1_toy/focused_bridge_2026-10-06/review/verify_angle.py

# Reproduce the standalone exact certificate in a fresh folder.
# This script writes results beside itself, so copy it before executing.
New-Item -ItemType Directory -Path project1_toy/focused_bridge_2026-10-06/math/reproduction_certificate
Copy-Item -LiteralPath project1_toy/focused_bridge_2026-10-06/math/certify_low_p.py -Destination project1_toy/focused_bridge_2026-10-06/math/reproduction_certificate/certify_low_p.py
python project1_toy/focused_bridge_2026-10-06/math/reproduction_certificate/certify_low_p.py
```

Both runners resolve a relative `--output` against the working directory; the commands supply the intended paths explicitly. Both refuse existing output directories. The angle runner's working copy gained this CLI after the scientific run; its archived source remains unchanged. The angle report also references the existing v1 landscape as a separately labeled grid comparison.

## Stop and next bounded question

This work stops at the prescribed cases and their independent reviews. It does not launch another optimizer campaign or real-model training.

The next mathematical question is whether the certified active branch can be extended over a stated range of frequency and relative importance, with valid competing-branch comparisons and a specified noise-risk crossing. That is a direct route toward Project 1's tradeoff boundary. A larger load test should follow a stated derivation or a specific unresolved claim, rather than an unguided sweep. Real-model transfer remains the later stage of the research structure.
