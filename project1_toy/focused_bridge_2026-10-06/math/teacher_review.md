# Independent mathematics teacher review

6 October 2026. Reviewed `student_derivation.md`, `verify_derivation.py`,
and `verification_results.json`. This reviewer did not write those files.
No new model was trained and no experimental scope was expanded.

## Verdict

**The mathematical claims in the student's bounded derivation are correct
under the stated binary-concept, tied-ReLU, energy-one assumptions.**
The work does establish global clean geometry optima for the two prescribed
dense (`p=1/2`) importance cases, not only a numerical counterexample.
It does not establish the low-frequency global geometry optima or the full
Project 1 robustness phase diagram. Those limits are accurately stated.

The student made useful progress by optimizing the decoder biases rather
than assuming zero bias, and by checking every sign sector instead of
assuming the equal-amplitude antipodal code is optimal. The resulting
dense-case counterexample is substantive and is strengthened to an exact
special-case theorem by the activation-interval proof. No obligatory
criticism or cosmetic rewrite is warranted.

## Independent checks

The teacher's `teacher_checks.py` uses **all sixteen possible active-state
subsets**, plus kink candidates and an all-off representative. This differs
from the student's ordered-interval implementation. For each consistent
subset it evaluates its quadratic stationary point; the direct population
loss selects the smallest candidate value.

The check covers 48 supplied-geometry/feature cases at the three
prescribed activation rates. Maximum minimum-loss discrepancy against the
student's interval optimizer is `1.6697788640876666e-34`. Equal-pair bias
and feature-loss formulas disagree by at most `0` and
`1.3877787807814457e-17`, respectively. Independent dense-case checks at
the protocol's 361 angles yield a maximum profiled-loss formula discrepancy
of `8.326672684688674e-17` and a maximum loss-at-analytic-bias discrepancy
of `5.551115123125783e-17`.

These numbers check implementations. The global claims below rest on
the interval and derivative arguments, not on the angle grid. Results
are saved in `teacher_check_results.json`.

## Checked mathematical arguments

### Fixed-geometry bias optimum

For fixed offsets `z_b`, the finite-state bias loss is continuous and
piecewise quadratic, with breakpoints `-z_b`. On an activation interval
its coefficients are exactly the student's `A_0`, `B_0`, and `C_0`.
The interval's best point is the clipped stationary point when `A_0>0`.
The all-off interval is constant; its finite right endpoint attains the
same value, so it is not omitted. The far-right interval is coercive
because the probabilities are positive. Evaluating every interval and
boundary therefore gives a global bias minimum even though the whole
function need not be convex.

Positive importance only multiplies each fixed-geometry feature loss,
so it does not alter that feature's bias minimizer. It can change the
jointly selected encoder. This distinction is correct and important.

### Angle reduction and equal pair

Global sign reversal leaves the Gram matrix unchanged. The closed
half-circle parameterization covers all rank-one energy-one geometries,
including same-sign codes, opposite-sign codes, and omitted-feature
endpoints. No representation family has been silently excluded.

For the supplied equal antipodal pair and `p<=1/2`, the active-branch
quadratic has mass `D=1-p+p^2`, linear coefficient
`N=p(1+p)/2`, and constant `p(1-p)/4+p^2`. Its minimizer
`N/D` lies in the required interval. The roots on neighboring intervals
point toward this branch, establishing the stated global bias optimum.
The alternative all-active formula for `p>=1/2` agrees at the boundary.

The noisy detection formula follows by conditioning on the four binary
states and integrating the projected Gaussian. The variance is
`sigma^2/2` per matched score, and the actual threshold is `1/2-beta`.
The supplied-code threshold `1/4` generally is not the trained decoder's
threshold. The student's distinction is mathematically correct.

### Local importance direction

At the balanced opposite-sign pair and `0<p<1/2`, the three-active-state
branch is locally valid. Holding its overlap derivative zero at balance,
the per-feature loss derivative with respect to that feature's squared
norm is

`-p(1-p)^2(1+p)/(1-p+p^2)`.

Consequently the student's total derivative is this value multiplied
by `I_1-I_2`. An importance-unequal equal pair is not stationary.
This is a local statement; the document correctly does not call it a
general global optimum. The separate weaker-feature branch's bias
`pa`, loss `p(1-p)^2 a^2+p^2`, and feasibility condition agree with
direct substitution into its two-active-state objective.

### Global dense geometry theorem

Put `a=max(w_i^2)`, `c=1-a`, and `r=sqrt(ac)`, so
`a>=r>=c` and `2r<=1`. Independently checking the student's interval
roots confirms the optimum bias in **both relative-sign sectors**.
The inequalities that place those roots are supplied in the document;
in particular `a/2>=r-c` follows from `1+c>=2r`.

The resulting feature losses are

`L_strong=c(1+r)/6`, `L_weak=a/4`.

For equal importance this gives

`F=1/4+c(2sqrt(c(1-c))-1)/12`.

Its interior stationary equation is
`sqrt(c(1-c))=c(3-4c)`. On `0<c<1/2`, squaring is legitimate
because both sides are positive. The resulting polynomial factors as
`(1-2c)(1-8c+8c^2)=0`. There is exactly one interior root,
`c=(1-1/sqrt(2))/2`. The endpoints have loss `1/4`, and the
interior value is strictly lower. Thus this is a global geometry result,
not merely a grid argmin.

An exact attaining opposite-sign code is
`W=[sin(pi/8),-cos(pi/8)]`. With `t=1/sqrt(2)`, its biases
are `[(1+2t)/4,(2-t)/6]` and feature losses are
`[(1+t)/8,(3-2t)/48]`. Their sum is

`(9+2sqrt(2))/48 = 0.24642556509887895`.

The strict improvement over the equal pair and mono code is
`(3-2sqrt(2))/48 = 0.0035744349011210355`.
Direct population evaluation agrees to `2.7755575615628914e-17`.
Same-sign codes also attain the profiled optimum; treating antipodality
as uniquely necessary would be unsupported, and the student does not do so.

For weights `[1,1/2]`, if the important feature is the stronger column,
the objective exceeds `1/8` by
`c[(1+r)/6-1/8]`, positive for every `c>0`. If the important feature
is weaker, its `a/4` contribution already is at least `1/8`, with a
positive additional loss at `a=1/2`. Both sign sectors are covered.
Retaining the important feature alone is therefore the global optimum.

## Repairs and bounded direction

**No material algebraic repair is required.** Successful clean optimization
and Gaussian detection robustness remain separate questions. The student's
global dense theorem does not imply that projected Adam reaches its optimum,
nor that the reconstruction-optimal code minimizes binary detection risk.
The toy experiment and its independent numerical reviewer address those
distinctions; this review does not sign off on the experiment.

If a further mathematical step is authorized, the bounded next target is
to certify the competing activation branches for **one existing low-p,
unequal-importance case**, rather than launching a new distribution or
large search. The fixed-bias interval method already supplies the relevant
branch expressions. That would extend the learned-geometry link inside
the existing protocol. It is not necessary to weaken the honest unfinished
status of the general phase diagram meanwhile.

Novelty remains a separate literature question. None of these correctness
checks establishes that the special-case theorem is new, transfers to a
real model, or guarantees conference acceptance.
