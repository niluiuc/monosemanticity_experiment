# One-case global clean-geometry certificate

6 October 2026. Bounded follow-up to the existing protocol, **only**
`p=1/5`, importance `(1,1/2)`, two concepts, one code dimension, tied ReLU
decoder, free decoder biases and encoder energy one. This does not extend
to other frequencies, feature loads, correlations or real models.

Status: student completed an exact-rational, computer-assisted global
certificate; independent teacher review passed on 6 October 2026 (see
`teacher_low_p_review.md` and `teacher_low_p_check_results.json`). The low-frequency
claims in the initial derivation and initial experiment remain correctly
labeled numerical. This separate follow-up strengthens only this one case.

## 1. Exact selected geometry

Up to the irrelevant global sign, parametrize

\[
W(t)=\frac{(1,t)}{\sqrt{1+t^2}},\qquad t\in\mathbb R.
\]

The omitted parameter point `t=±infinity` is the code retaining concept 2.
Every finite rank-one geometry at energy one is represented.

The global population clean optimum has negative `t=t*`, the algebraic root

\[
\boxed{20t^3+175t^2-60t-59=0,\qquad
-0.442090239023400245<t^*<-0.442090239023400243.}
\]

Its globally minimizing clean decoder biases are

\[
\boxed{\beta_1^*(t)=\frac{t(5t-1)}{21(1+t^2)},\qquad
\beta_2^*(t)=\frac{1}{5(1+t^2)}.}
\]

Their active states are `{00,10,11}` for concept 1 and `{00,01}` for
concept 2, where the states list `(b_1,b_2)`.
The objective on this active branch is

\[
\boxed{F(t)=\frac{905t^4-320t^3+410t^2+441}
 {5250(1+t^2)^2}.}
\]

Its derivative is

\[
F'(t)=\frac{8t(20t^3+175t^2-60t-59)}
 {2625(1+t^2)^3}.
\]

The optimum's clean weighted population loss satisfies

\[
0.07775208251629429<L^*<0.07775208251629430.
\]

Retaining concept 1 alone gives `2/25=.08`; retaining concept 2 alone gives
`4/25=.16`. Thus the selected mixed code strictly improves clean squared
reconstruction loss over either monosemantic retention code.

## 2. Deriving the attaining branch

For the opposite-sign sector `-1<t<0`, write

\[
a=\frac1{1+t^2},\quad c=\frac{t^2}{1+t^2},\quad
r=\frac{-t}{1+t^2},\quad D=1-p+p^2=\frac{21}{25}.
\]

The stronger concept 1 uses the three-active-state minimum already derived:

\[
\beta_1=\frac{p(c+pr)}D,\quad
L_1=pq c^2+p^2(c+r)^2-\frac{p^2(c+pr)^2}D.
\]

For concept 2, the coactivation state is inactive. Its two-active-state
quadratic gives

\[
\beta_2=pa,\qquad L_2=pq^2a^2+p^2.
\]

The second active set is feasible when `pa<=r-c`, namely

\[
t^2+t+\frac15\le0,
\quad\text{or}\quad
\frac{-1-1/\sqrt5}{2}\le t\le\frac{-1+1/\sqrt5}{2}.
\]

The first active set is feasible throughout this interval: `beta_1>=0`,
`beta_1<=r`, and `a-r+beta_1>0`. The root interval above lies strictly
inside this domain. Substituting `p=1/5` into `L_1+L_2/2` yields the
displayed rational objective. This alone proves an exact stationary branch;
the following comparison is what upgrades it to a global optimum.

## 3. Why the global comparison is finite

For each concept, fixed-geometry optimal bias is among:

1. Four distinct ReLU score breakpoints.
2. The stationary point in each of the four nonempty active intervals,
   provided it lies in that interval.

The far-left inactive constant loss is attained at the first breakpoint.
These eight candidates therefore include every global bias optimum at a
generic geometry. The candidates extend continuously to degenerate
geometries; coincident breakpoints are harmless duplicates there.

Score order changes only at `t=-1,0,1`. Consequently there are four
geometry regions, each with `8 x 8=64` joint bias candidates. Every candidate
loss is a rational function whose denominator is a positive constant times
`(1+t²)²`. Its validity is determined by polynomial inequalities from
interval membership, plus the region bounds. The feasibility polynomials
have degree at most two; stationary polynomials have degree at most four.

On any feasible interval, a rational candidate achieves its finite minimum
at a stationary point or a feasibility/region endpoint. If its feasible
domain is unbounded, the only additional possible minimum is its limit at
infinity. The optimal infinity geometry is known independently to have loss
`.16`. Therefore exact isolation and comparison of these finitely many
real roots, together with the mono endpoints, covers the whole problem.

This includes candidate biases that are not themselves globally optimal at
their geometry. That is intentional: every evaluated candidate is feasible,
and the collection includes all true global bias optima. Adding extra
feasible biases cannot produce a loss below the global optimum of the
original problem.

## 4. The computer-assisted certificate

`certify_low_p.py` performs this finite comparison using SymPy exact
rationals and univariate real-root isolation, not a numerical angular scan.

- Enumerated joint bias branches: **256**.
- Raw stationary/feasibility root candidates: **1,031**.
- Feasible candidates before duplicate removal: **296**.
- Distinct feasible function/root candidates after removal: **265**.
- Candidates whose certified objective interval overlaps the winner's:
  **zero**.

Polynomial signs at algebraic roots are certified by rational interval
evaluation. Where the interval contains zero, polynomial gcd detects exact
root sharing; otherwise the isolating interval is refined. No floating-point
sign test is used to decide feasibility. Objective values are enclosed by
rational interval arithmetic. The winning upper bound is strictly below
every other candidate's lower bound and below `.08`.

The smallest competing candidate lower bound exceeds
`0.07827150837086602`, leaving a separation greater than `.0005194`.
The optimum in each geometry region is summarized below for readability;
the actual certificate uses rational bounds rather than these decimals.

| t region | certified candidate count | regional minimum (approx.) |
|---|---:|---:|
| `t<=-1` | 61 | .0942857142857143 |
| `-1<=t<=0` | 87 | .0777520825162943 |
| `0<=t<=1` | 81 | .0800000000000000 |
| `t>=1` | 36 | .156926217598989 |

The full candidate ledger is `low_p_certificate_candidates.json`. The
summary, winning cubic, certified rational root and value enclosures are
`low_p_certificate_results.json`. Reproduction:

```powershell
python project1_toy/focused_bridge_2026-10-06/math/certify_low_p.py
```

Dependencies: Python and SymPy 1.14.0 in the checked environment. The first
execution completed the comparisons but failed while serializing a SymPy
Boolean. Converting that Boolean to the native Python `bool` repaired output
serialization; the mathematical settings and comparison algorithm were
unchanged. The successful rerun took about 21 seconds.

## 5. Relation to training and robustness

The toy student's independent direct angular solver converged locally to
`theta=-.41625677289385893` and clean loss `.07775208251629454`. The exact
certificate has `t*=tan(theta*)` approximately `-.44209023902340024406`
and loss `.077752082516294294514`. This agreement supplies a concrete
training-to-geometry bridge in the existing assumptions. It is not proof
that every training algorithm or initialization reaches this solution.

The selected weaker concept's maximum clean reconstruction, attained in
state `01`, is

\[
c+\beta_2=\frac{t^{*2}+1/5}{1+t^{*2}}<\frac12.
\]

Thus this trained decoder never detects concept 2 under the strict
`.5` decision rule, despite using a nonzero encoder column for it. Its
clean squared-error benefit comes from improving continuous reconstruction,
not from correctly detecting that weak concept. The supplied midpoint
detector is a different readout and is reported separately by the toy
experiment.

The corruption risk follows by substituting the **selected** geometry and
biases into the existing exact Gaussian state integration. That is the
intended link: clean objective → certified selected geometry → operational
noise risk. This certificate does not prove a complete noise crossing,
an arbitrary-p importance law, a larger-load phase boundary, publication
novelty, or real-model transfer.
