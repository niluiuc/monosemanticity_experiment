# Paper-critical evidence audit: same-outcome robustness and mechanism

6 October 2026. Postdoctoral experimental assessment, using saved outcomes only.
No experiment, new risk grid, root search, training or raw-file edit was performed
for this audit. The proposed next test below requires a new bounded protocol
and independent reviewer approval before execution.

## Decisive finding

The frequency family at importance `[1,1/2]` does **not** supply a noisy
reconstruction-MSE reversal on the five primary noise settings. Every certified
mixed code has lower weighted MSE than clean-preferred mono throughout those
settings. Its binary-detection crossings cannot be presented as reversal of the
same objective used for clean training.

There is, however, an existing stronger same-outcome anchor in the focused
bridge: `p=1/2`, importance `[1,1]`, energy one. Its globally certified clean
mixed geometry beats mono in clean MSE and loses in noisy MSE at sigma .30 and
.60. This should be considered before launching a new experiment or model.

## 1. Existing dense anchor: clean benefit and noisy reversal on the same MSE

Raw source:
`../focused_bridge_2026-10-06/toy/run_v1/risks.csv`.
Filter `case=p_0.50_importance_1.00`, `label=grid_diagnostic_best` or
`mono_retain_0`, `detector=actual_decoder`. Read
`weighted_sum_decoder_mse`; the midpoint rows duplicate MSE because thresholds
do not enter reconstruction. Both mono controls have identical summed MSE here.

| Code | sigma=0 | .05 | .15 | .30 | .60 |
|---|---:|---:|---:|---:|---:|
| Certified dense mixed optimum | .24642556509887897 | .24839220729113390 | .26439383316486250 | .31868281868245574 | .51299380896784230 |
| Clean-preferred mono | .25000000000000000 | .25187499999999996 | .26687499999971154 | .31746388060216080 | .50544977108947600 |
| Mixed minus mono | -.00357443490112103 | -.00348279270886606 | -.00248116683484906 | +.00121893808029494 | +.00754403787836633 |

These are importance-weighted sums (both weights one), fixed clean-trained
biases, analytical Gaussian code-noise integration in float64. There is no
switch from reconstruction to classification between clean and noisy results.
No empirical noise crossing location was newly calculated in this audit.

The geometry is not globally certified by the grid label. Its independent
global proof is in
`../focused_bridge_2026-10-06/math/student_derivation.md`, Section 7, checked in
`../focused_bridge_2026-10-06/math/teacher_review.md`. The grid's discrete candidate
attains this already proved solution:

\[
a_*=(1+1/\sqrt2)/2,\quad c_*=(1-1/\sqrt2)/2,\qquad
L_*=(9+2\sqrt2)/48.
\]

One representative is `W=[sin(pi/8),-cos(pi/8)]`, with the weaker column first.
Its optimal biases are `[(1+sqrt(2))/4,(2-1/sqrt(2))/6]`. Same- and opposite-sign
representatives, and feature swaps, attain the clean optimum. Their per-feature
Gaussian-MSE profiles agree up to feature swaps: at p=.5 complementing the
*other* independent bit maps the same-sign affine score and its optimal bias
to the opposite-sign affine score, while leaving the target bit unchanged.
Projected Gaussian sign does not change its marginal law. Thus the dense anchor
does not depend on choosing a favorable clean minimizer from a grid tie.

The frozen encoder energy, free clean biases, population distribution, noise
location and evaluation objective are matched. Nevertheless these particular
biases have not been optimized for the corrupted distribution. That control is
needed before a strong robustness mechanism claim.

## 2. Frequency family: actual weighted reconstruction values

Raw source: `../frequency_boundary_2026-10-06/toy/run_v1/primary_risks.csv`.
Filter `label=clean_selected` or `mono_retain_0`, `detector=actual_decoder` and
read `weighted_sum_mse`. Geometry/importance remain fixed as declared; mono
retains the important concept by the clean objective. Values in each cell are
`selected / mono`.

| p | sigma=0 | .05 | .15 | .30 | .60 |
|---|---|---|---|---|---|
| .05 | .0177428805413461 / .0237500000000000 | .0193561142252694 / .0250625000000000 | .0295165134370685 / .0355624999999712 | .0606724560819892 / .0709963880602161 | .1783367042074818 / .2112949771089476 |
| .20 | .0777520825162943 / .0800000000000000 | .0796053834041468 / .0815000000000000 | .0916968571071191 / .0934999999998846 | .1288072562057747 / .1339855522408644 | .2653417292211299 / .2901799084357905 |
| .35 | .1137405821908572 / .1137500000000000 | .1153429089123392 / .1154375000000000 | .1284174598086755 / .1289374999997981 | .1732610961596413 / .1744747164215126 | .3434566975796713 / .3465648397626332 |
| .375 | .1171874027176620 / .1171875000000000 | .1188630711354670 / .1189062500000000 | .1325106899052895 / .1326562499997837 | .1787342597258137 / .1790354104516206 | .3530653586614299 / .3537748283171070 |
| .40 | .1200000000000000 / .1200000000000000 | .1217500000000000 / .1217500000000000 | .1357499999997693 / .1357499999997693 | .1829711044817287 / .1829711044817287 | .3603598168715808 / .3603598168715808 |

The binary detector's high-noise limit is a different statement. It gives mixed
error 3/4 versus mono 1/2+p/2 in the weighted family, but does not establish an
MSE reversal. For fixed finite biases, rectified Gaussian second moments have
leading term `sigma^2*||w_i||^2/2`. Consequently the weighted mixed-MSE leading
coefficient is `(d_0+d_1/2)/2`, compared with mono's `1/2`. Since `d_0+d_1=1`,
the mixed-minus-mono quadratic coefficient is `-d_1/4`. It is negative for
genuine sharing. This makes a permanent large-noise MSE disadvantage impossible
for these fixed mixed codes against this fixed mono code, despite the detection
disadvantage. This deduction uses fixed geometry/biases and must not be carried
over to noise-dependent decoder recalibration without another argument.

## 3. Readout dependence in existing binary comparisons

Raw source: same frequency `primary_risks.csv`; compare `weighted_sum_error`
using the two detector labels. Each number below is mixed minus mono:

| p | sigma | Actual decoder | Centered midpoint |
|---|---:|---:|---:|
| .05 | .30 | -.014474506713 | +.122951834793 |
| .05 | .60 | -.003661118545 | +.186588050172 |
| .35 | .30 | -.000144223139 | +.080938665244 |
| .35 | .60 | -.000862825250 | +.071719572144 |
| .375 | .30 | -.000134650793 | +.069570697294 |
| .375 | .60 | -.000222913071 | +.063000392312 |

The observed actual-decoder sharing advantages disappear at these settings
under the supplied midpoint diagnostic. This does not make either readout
"wrong": they are different decisions. It prevents treating the operational
binary advantage as an intrinsic, readout-independent monosemanticity law.
The actual decoder's .5 threshold follows reconstruction training; the midpoint
is a separately imposed diagnostic, not an optimized Bayes rule.

## 4. Mechanism: nonlinear gates break an exact linear tie

The following structural deductions use the existing dense model; they are
proposed for the independent mathematics reviewer, not reported as a new run.

### Linear control

Replace ReLU by identity, retaining rank-one energy-one W, tied G and a freely
optimized bias. At p=.5 and equal importance, `Cov(b)=I/4`, `G^2=G` and
`trace(G)=1`. The optimal bias is `E[b]-G E[b]`. Thus

\[
L_{\rm linear}(\sigma)
=\tfrac14\operatorname{tr}[(I-G)^2]
 +\sigma^2\operatorname{tr}(G)
=\boxed{\tfrac14+\sigma^2}.
\]

Every geometry, including mono and the certified sharing code, has identical
linear reconstruction loss. Optimizing the mean bias for noise does not change
this because the injected noise has mean zero. In this dense anchor,
interference/coherence alone cannot explain a comparative MSE reversal:
the nonlinear gating is necessary to break that linear tie.

### Small-noise response of the nonlinear codes

At the certified dense sharing code, the strong feature is active on three
states, with probability 3/4, and the weak feature is active on all four. Their
clean preactivation gaps are nonzero. The leading small-noise excess MSE is
therefore `(3*a_*/4+c_*)*sigma^2`. For mono, the retained feature is active when
its bit is one (probability 1/2), and is exactly at the ReLU boundary when zero
(probability 1/2), contributing half the noise variance on those zero states.
Mono's coefficient is `3/4`. Sharing's larger coefficient differs by `c_*/4`.
The clean sharing advantage is `(3-2sqrt(2))/48`.

This is a plausible exact local mechanism: sharing lowers clean loss via the
nonlinear activation pattern but exposes more weighted feature variance to
small code noise. At moderate noise other gates can switch, so a quadratic
expansion cannot determine the full crossing. The existing exact MSE rows, not
that approximation, establish the bounded reversal at .30 and .60.

## 5. ONE smallest next test

Use only the **already certified dense anchor** p=.5, importance `[1,1]`,
energy one, fixed globally clean-selected sharing geometry and clean-preferred
mono. At the same existing five sigma values, recalibrate **decoder biases
symmetrically for both codes** against the noisy population objective, without
changing W. Report frozen-clean-bias and calibrated-bias MSE separately, retain
both mono controls, and keep the exact linear-tie control above.

This answers one paper-critical question: does the same-outcome reversal survive
matched noise-aware decoder calibration, or is it mainly a clean-head mismatch?
The archives do not contain those recalibrated outcomes, so the answer is
currently **unknown**. No claim of survival should be made from existing data.

For sigma>0, the scalar noisy-bias objective is smooth but not necessarily
globally convex. Its derivative is available from the rectified Gaussian
moments:

\[
\ell_i'(\beta)=2\sum_bP_b[
 (\mu_b-b_i)\Phi(\mu_b/s_i)+s_i\phi(\mu_b/s_i)],
\quad \mu_b=(Gb)_i+\beta,\quad s_i=\sigma|w_i|.
\]

The teacher should approve a bounded, all-stationary-candidate/bracket method
or an explicit global certificate before execution. A generic bounded minimizer
alone should not silently be called the noisy global optimum. Store objective
values, all candidates/failures and verification against independent integration.
If calibration removes the reversal, report that result and stop this claim;
do not manufacture it with a new threshold, distribution or model. If it survives,
the nonlinear gate mechanism has a stronger control and is more ready to guide
an analogous real-model intervention. Neither outcome supplies a full load
diagram, transfer validation or novelty guarantee by itself.

## Scope decision

The existing dense anchor is the strongest same-objective evidence available.
The importance-dependent frequency theorem remains useful training-to-geometry
mathematics but should not be presented as its noisy-MSE reversal. Build the
next causal check on the proved dense anchor, rather than expanding frequencies
or starting pretrained/diffusion infrastructure before this blocker is resolved.
