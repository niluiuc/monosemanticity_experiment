# Noise comparison: endpoint facts before the new numerical run

6 October 2026. These observations use the unchanged actual decoder rule and do not select a new detector after seeing the numerical outcome.

For a supplied clean-selected encoder/bias pair, set z_i(b)=(Gb)_i+beta_i and add scalar Gaussian code noise of standard deviation sigma. For a nonzero encoder column, feature error is

\[
r_i(p,\sigma)=\sum_b P_p(b)\Phi\left(
\frac{(1-2b_i)(z_i(b)-1/2)}{\sigma |w_i|}\right).
\]

The weighted error is R=r_1+r_2/2. This formula follows by conditioning on each binary state and computing the Gaussian threshold probability. The sigmas in the numerical verification are fixed before execution.

## Mono control

The clean-preferred mono code has w=(1,0), biases (0,p), and 0<p<=1/2. Its omitted feature always has prediction zero under the strict detection rule, including the p=1/2 tie. Therefore

\[
R_{\rm mono}(p,\sigma)=\Phi(-1/(2\sigma))+p/2,
\qquad \sigma>0,
\]

and its clean error is p/2. The first term is independent of the concept's activation probability because the retained feature has symmetric threshold gaps +1/2 and -1/2. This is a property of the supplied trained decoder, not the Bayes-optimal threshold for a rare concept.

## Infinite-noise limit of any genuinely shared code

For any fixed encoder with both columns nonzero and finite biases, each Gaussian threshold probability tends to 1/2 as sigma tends to infinity. Consequently

\[
R_{\rm shared}(p,\sigma)\longrightarrow 3/4,\qquad
R_{\rm mono}(p,\sigma)\longrightarrow 1/2+p/2,
\]
\[
\boxed{\Delta(p,\sigma)\longrightarrow 1/4-p/2>0
\quad(0<p<1/2).}
\]

Thus a sharing code cannot beat this mono control at arbitrarily large noise under the fixed rule. A negative difference at a finite noise strength need not define a single permanent robust phase: it must eventually return to a positive difference. Continuity for sigma>0 gives an intervening crossing when a negative finite value is established. This statement does not prove that any particular frequency has a negative value, or count every crossing.

The limits of vanishing weak-column norm and infinite sigma need not commute. A code approaching mono can retain a nonzero weak column at every finite parameter value, while exactly mono never adds noise to that omitted feature.

## Interpretation limits

At zero noise, strict thresholds require direct evaluation, and they can be discontinuous under threshold ties. The midpoint detector is a separate diagnostic. These endpoint facts concern binary detection under the current Gaussian corruption model; they do not prove an adversarial claim, a monotone noise boundary or the full variable-load theorem.
