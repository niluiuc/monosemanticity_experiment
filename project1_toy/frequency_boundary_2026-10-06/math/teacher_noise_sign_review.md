# Independent teacher review: one-case rigorous noise sign

6 October 2026. Reviewed `noise_crossing_protocol.md`,
`certify_noise_sign.py`, its saved rational result, the source global
geometry certificate, and root's `noise_crossings.md` exposition.
Scope remains exactly `p=1/20`, importance `(1,1/2)`, energy one,
actual decoder threshold `1/2`, and the previously tested `sigma=3/10`.
No new frequency, noise level, training or root search was run.

## Verdict

**Approved. The rational certificate proves that the shared-minus-mono
weighted detection-risk difference is negative at `sigma=3/10`.**
Together with the positive clean limit and positive infinite-noise limit,
it establishes **at least two distinct positive noise roots** for this
fixed globally clean-selected geometry. It does not establish the exact
number of roots, their locations, or an interval theorem for other
frequencies.

No material mathematical correction is required. Credit is warranted
for replacing an approximate sign observation with a rigorous enclosure
and checking the strict clean gaps needed to use the zero-noise limit.
The student saved source and results before a tool usage limit interrupted
its reporting turn. Root completed the exposition from those saved
artifacts; the interruption is a workflow limitation, not a failed
certificate calculation.

## Geometry and probability mapping

The certificate uses the same rational root interval as the archived
globally optimal sharing geometry. Its monic polynomial matches the
scaled form

`380t^3+14800t^2-1140t-6839=0`.

The interval isolates exactly one negative root. The bias formulas match
the archived global certificate exactly:

`beta1=(20t^2-t)/(381(1+t^2))`,
`beta2=1/(20(1+t^2))`.

The Gram entries and encoder norms are therefore those of
`W=(1,t)/sqrt(1+t^2)`, not a different supplied pair. Both columns
have strictly positive norm throughout the root enclosure.

For a binary state, the error CDF argument is

`-(2*b_i-1)*[(Gb)_i+beta_i-1/2]/(sigma*abs(w_i))`.

This has the correct signs for false positives and false negatives.
The state probabilities and feature weights are summed without assuming
independence between the two output errors. Their common scalar noise
does not invalidate linearity of expectation for the weighted sum.

At zero noise all eight margins are strictly separated from zero.
The important concept fails only in state `11`, with probability `1/400`.
The weak concept is never detected and contributes weighted error `1/40`.
Thus shared clean risk is `11/400`, mono clean risk is `1/40`, and their
difference is exactly `1/400`. There are no threshold ties that could
make the positive-noise limit differ from this clean value.

## Rational interval implementation

Addition, negation, multiplication and inversion use valid outward
enclosures. Inversion rejects intervals containing zero. The square-root
routine takes an integer floor after exact scaling; its returned lower
and upper rationals satisfy the asserted squared inequalities. Applying
this at interval endpoints is valid by square-root monotonicity.
The Gram/bias/norm expressions contain repeated occurrences of `t`;
treating them as separate interval occurrences may widen bounds but
cannot invalidate enclosure.

Outward decimal rounding of Gaussian arguments uses exact Fraction
floor/ceiling operations. Normal CDF monotonicity justifies evaluating
the rounded interval endpoints rather than relying on a floating-point
CDF for a sign decision.

### Machin identity and pi enclosure

For `x=1/5`, `y=1/239`, the exact tangent doubling/subtraction arithmetic
gives `tan(4atan(x)-atan(y))=1`. The correct quadrant is also justified:

`4x/(1+x^2)-y < 4atan(x)-atan(y) < 4x=4/5`.

The lower bound is positive. Furthermore `atan(1)>1/2` by its integral,
so `pi/2=2atan(1)>1>4/5`. The angle therefore lies in `(0,pi/2)`
and equals `pi/4`. This proves the stated Machin identity without
ambiguity from tangent periodicity.

For these arctangent arguments, successive alternating terms decrease
in magnitude. The even partial sum through index 30 is an upper bound;
adding index 31 gives the lower bound. The resulting pi interval, square
root and inverse enclose the positive constant `1/sqrt(2*pi)`.

### Gaussian CDF enclosure

For `v>=0`, Taylor's theorem with Lagrange remainder makes the even-degree
polynomial for `exp(-v)` an upper bound and the following odd polynomial
a lower bound. This statement holds even where the initial alternating
terms do not decrease. Substituting `v=u^2/2` and integrating over
`[0,x]` gives the coefficients used in the script:

`(-1)^j*x^(2j+1)/(2^j*j!*(2j+1))`.

The degree-80 integral is the upper bound and the degree-81 integral
the lower. Exact rational arithmetic prevents cancellation roundoff.
Symmetry handles negative CDF arguments. Clipping a valid CDF enclosure
to `[0,1]` remains valid. Interval multiplication with the enclosed
normalizing constant and the exact state probabilities then gives
valid risk bounds and a strictly negative difference upper bound.

## Independent verification and fresh reproduction

The source was reproduced with `HERE` redirected to the new
`teacher_noise_sign_reproduction/` directory and its source geometry
path preserved. Original results were not overwritten. All saved fields
except runtime reproduce identically.

`teacher_noise_sign_checks.py` independently checks the polynomial and
bias mapping, reconstructs the arctangent and integrated Taylor sums
using different recurrences, and recomputes all eight state arguments
and CDFs at 100-digit precision. All reference values lie inside the
saved rational enclosures. These high-precision values are crosschecks,
not the sign proof; the sign proof uses the exact rational bounds.

The independent numerical reference difference is approximately
`-0.0144745067127706407821`. The saved exact interval has displayed
endpoints approximately

`[-0.014474506712828471, -0.014474506712749220]`.

Its midpoint display is not claimed to be the exact risk value. The
whole enclosure is negative with substantial separation from zero.
Check results are saved in `teacher_noise_sign_check_results.json`.

## Crossing implication and limits

For positive noise the finite CDF mixture is continuous. Strict clean
gaps establish its continuous limit at zero. Both columns remain nonzero
and biases fixed, so the shared weighted risk tends to `3/4`; mono risk
tends to `1/2+1/40`. Their limiting difference is exactly `9/40>0`.

Therefore the negative value at `3/10`, the positive small-noise limit,
and the positive large-noise limit give a root in `(0,3/10)` and a
distinct root in `(3/10,infinity)` by continuity. The certificate does
not count all roots or certify the numerical crossing locations.
It proves a nonmonotone comparison for one clean-selected toy code.

The bounded calculation and review are complete; stop under this
protocol. Higher feature load, variable importance, other frequencies,
real-model transfer and scientific novelty remain separate questions.
