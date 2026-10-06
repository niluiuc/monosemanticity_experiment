# Student derivation: clean training, selected geometry, and noisy decisions

6 October 2026. Scope: the six cases in `../protocol.md`. This is a bounded
mathematical bridge for Project 1, not a claim of publication novelty or a
general load theorem. Independent teacher review is required.

## 1. The precise objective

Let independent concepts have `b_1,b_2 ~ Bernoulli(p)`, with `0<p<1` and
positive importance weights `I_1,I_2`. For a rank-one tied autoencoder,

\[
w=(u,v),\quad u^2+v^2=1,\quad G=w^\top w,
\quad \widehat b_i=\max\{(Gb)_i+\beta_i,0\}.
\]

Clean training minimizes

\[
L(w,\beta)=\sum_i I_i\sum_{b\in\{0,1\}^2}
 P_p(b)\big(\max\{(Gb)_i+\beta_i,0\}-b_i\big)^2.
\]

The four state probabilities are `(q²,pq,pq,p²)` in order `00,01,10,11`,
where `q=1-p`. A positive importance weight scales one feature's objective
but does not change its optimal bias **at supplied geometry**. Importance
can change the geometry selected by joint training.

## 2. Exact global bias minimization at supplied geometry

Fix feature `i` and write `z_b=(Gb)_i`, `y_b=b_i`, and `P_b=P_p(b)`.
The bias breakpoints are the distinct values `-z_b`. Between consecutive
breakpoints, the active set `A={b:z_b+beta>0}` is constant and

\[
\ell_i(\beta)=A_0\beta^2-2B_0\beta+C_0,
\]

\[
A_0=\sum_{b\in A}P_b,\quad
B_0=\sum_{b\in A}P_b(y_b-z_b),\quad
C_0=\sum_{b\in A}P_b(y_b-z_b)^2+
 \sum_{b\notin A}P_by_b^2.
\]

For `A_0>0`, the minimum on the interval closure is its vertex `B_0/A_0`
clipped to that interval. For `A_0=0`, the loss is constant and an interval
boundary is sufficient. Evaluate all these candidates and all breakpoints;
their smallest loss is the **global** fixed-geometry bias minimum. The
objective is continuous at breakpoints, though it need not be globally
convex. At the far left it is constant; at the far right it is coercive.
Consequently this finite candidate comparison omits no minimum.

This theorem is elementary finite-state optimization. Its correctness does
not establish scientific novelty.

## 3. Exact reduction of geometry selection

The irrelevant global sign of `w` can be removed because it leaves `G`
unchanged. Every remaining geometry is represented by

\[
w(\theta)=(\cos\theta,\sin\theta),\qquad
-\pi/2\le\theta\le\pi/2.
\]

After bias minimization, define

\[
F_{p,I}(\theta)=\sum_iI_i\min_{\beta_i}\ell_i(\beta_i;w(\theta)).
\]

Thus population geometry selection is exactly the one-dimensional problem
`min_theta F`. Evaluating a finite grid does **not** prove its global
minimum. The interval formulas supply a piecewise analytical objective;
the global geometry conclusions below are proved only for `p=1/2`.

## 4. Monosemantic retention: exact clean optimum

For `w=(1,0)`, the retained feature is reconstructed perfectly with
`beta_1=0`. The omitted feature is reconstructed as the optimal constant
`beta_2=p`, and

\[
L_{\mathrm{mono},1}=I_2p(1-p).
\]

For `w=(0,1)`, similarly `L_mono,2=I_1p(1-p)`. The clean-selected mono
comparator retains the higher-importance feature. Both codes are evaluated
in the experiment; a noise-dependent baseline switch is not substituted
for the clean-selected comparator.

The omitted feature has nonzero squared error even though its constant
prediction may have low binary error when it is rare. Reconstruction loss
and detection error are distinct tasks.

## 5. Equal-amplitude antipodal pair: exact clean bias and risk

For `w=(1/sqrt(2),-1/sqrt(2))`, each feature's score takes values
`0,+1/2,-1/2,0`; its desired label is respectively `0,1,0,1` when states
are ordered by that feature. Put `D=1-p+p²` and `N=p(1+p)/2`.

For `0<p<=1/2`, its globally optimal bias is

\[
\boxed{\beta_{\rm pair}^*=\frac{N}{D}
 =\frac{p(1+p)}{2(1-p+p^2)}}.
\]

On the interval `[0,1/2]`, the loss is

\[
\ell(\beta)=D\beta^2-2N\beta+pq/4+p^2.
\]

The interval below zero has its stationary point to the right; the interval
above `1/2` has its stationary point `p` at or to the left when `p<=1/2`.
The inactive interval gives the constant loss `p`. These intervals show
the displayed bias is a global minimum, not merely a stationary point.
Its per-feature loss is

\[
\boxed{\ell_{\rm pair}^*=pq/4+p^2-N^2/D}.
\]

For `p>=1/2`, the all-active solution is instead `beta*=p` with per-feature
loss `pq/2`; both formulas agree at `p=1/2`. Total pair loss is
`(I_1+I_2) ell_pair*` because a supplied equal pair has the same per-feature
loss regardless of importance.

Actual decisions are `reconstruction>1/2`, equivalent to

\[
(Gb)_i>t,\qquad t=1/2-\beta^*_{\rm pair}.
\]

The former supplied-code calculation used threshold `1/4`. It generally
does **not** describe this clean-trained decoder. At `p=.05`, `beta` is
`.0275590551` and `t=.4724409449`; at `p=.2`, `beta=1/7` and `t=5/14`.
Near a very rare concept, the trained detector puts its threshold close
to the single-feature score `.5`: clean squared-error training can leave
little detection margin for a present concept.

With Gaussian code noise of standard deviation `sigma>0`, define
`s=sigma/sqrt(2)` (this `s` is a noise scale here, not feature sparsity).
Per-feature error is exactly

\[
e_{\rm pair}=q^2\Phi(-t/s)
 +pq\Phi((t-1/2)/s)
 +pq\Phi((-1/2-t)/s)
 +p^2\Phi(t/s).
\]

At `sigma=0`, apply the strict decision directly; do not divide by zero.
For `0<p<=1/2`, the per-feature clean error is `p²`, including `p=1/2`
under the strict tie rule. The clean mono detector has weighted error
`I_dropped p`. At positive noise, its retained-feature error is
`Phi(-1/(2sigma))`, and its dropped-feature error remains `p` for the
prespecified `p<=1/2`.

## 6. Importance forces an unequal pair locally

For opposite signs, write `a=u²`, `c=1-a`, and `r=sqrt(ac)`.
Near `a=1/2`, for `0<p<1/2`, both feature losses use the three-active-state
branch. For a feature of squared norm `d`, this branch is

\[
\ell_3(d)=pq(1-d)^2+p^2(1-d+r)^2
 -\frac{p^2(1-d+pr)^2}{D},\qquad
\beta_3(d)=\frac{p(1-d+pr)}{D}.
\]

It is valid when the selected bias lies between the appropriate score
breakpoints. At the balanced pair these inequalities are strict for
`0<p<1/2`, so differentiation is valid locally. Since `r'(1/2)=0`,

\[
\left.\frac{dF}{da}\right|_{a=1/2}
 =-(I_1-I_2)\frac{p(1-p)^2(1+p)}{D}.
\]

Thus for unequal importance the equal pair is **not even a stationary
geometry**: shifting energy toward the more important feature decreases
clean loss. This is an exact training-to-geometry statement, not a grid
inference. It does not determine the global optimum at general `p`.

When the weaker feature's collision state becomes inactive, another branch
has `beta_2=pa` and `ell_2=pq²a²+p²`; its feasibility requires
`0<=pa<=r-c`. This branch occurs at the numerical minima for the two
prespecified rare, unequal-importance settings.

## 7. A global geometry theorem for p=1/2

Let `a>=1/2` be the **larger** squared column norm, `c=1-a`,
`r=sqrt(ac)`. Strong and weak mean column norms here, not importance.

For opposite signs the globally optimal biases are

\[
\beta_{\rm strong}=\frac{2c+r}{3},\qquad
\beta_{\rm weak}=\frac{a+r}{2}.
\]

The strong feature has three active states; the weak feature has all four.
For same signs the globally optimal biases are instead

\[
\beta_{\rm strong}=\frac{2(c-r)}{3},\qquad
\beta_{\rm weak}=\frac{a-r}{2}.
\]

The strong feature excludes state `00`, while the weak feature has all four
states (allowing zero-valued boundaries). In both sign sectors the losses
are identical:

\[
\boxed{\ell_{\rm strong}=(c^2+cr+r^2)/6=c(1+r)/6,
\qquad \ell_{\rm weak}=a/4.}
\]

### Why these are global bias optima

For opposite signs, strong-feature breakpoints are
`[-a,r-a,0,r]`. The roots in successive nonconstant intervals are
`c`, `c+r/2`, `(2c+r)/3`, and `(c+r)/2`.
The first two lie to the right of their intervals; the third lies inside
`[0,r]` because `c<=r`; the final lies at or left of `r`. Therefore the
objective decreases to the third root and increases afterward.

Weak opposite-sign breakpoints are `[-c,0,r-c,r]`; successive roots are
`a`, `a/2`, `(2a+r)/3`, `(a+r)/2`. The first three lie to the right of
their intervals, using `a/2>=r-c` and `a>=r`; the final is feasible.

For same signs, strong-feature breakpoints are
`[-a-r,-a,-r,0]`; roots are `c-r`, `c-r/2`, `2(c-r)/3`, `(c-r)/2`.
The first two lie to the right, the third lies in `[-r,0]`, and the last
lies to the left of its interval.

Weak same-sign breakpoints are `[-c-r,-r,-c,0]`; roots are
`a-r`, `(a-2r)/2`, `2(a-r)/3`, `(a-r)/2`.
The first three lie to the right and the last is feasible. In particular,
`1+c>2r` places the second root beyond `-c`. These signs establish global
minima across every active interval. Degenerate endpoints follow by
continuity and direct evaluation.

### Equal importance: exact selected geometry

For `I_1=I_2=1`, the globally profiled objective is

\[
F(a)=a/4+c(1+r)/6
 =1/4+\frac{c(2r-1)}{12}.
\]

This covers every rank-one geometry, up to signs and swapping features.
For every `1/2<a<1`, it is strictly below the equal pair and mono value
`1/4`. Differentiating `c(1-2r)` gives the stationary condition
`c(4a-1)=r`. On `(1/2,1)`, its unique solution is

\[
\boxed{a^*=\frac{1+1/\sqrt2}{2},\quad
c^*=\frac{1-1/\sqrt2}{2},\quad
L^*=\frac14-\frac{3-2\sqrt2}{48}
 =0.246425565098879.}
\]

The endpoints have loss `1/4`, and the interior stationary point is the
minimum. This is a **global geometry result** for this one case, not just
an exact constructive counterexample. Both same-sign and opposite-sign
encoders attain it. Symmetric concept importance does not force equal
column norms; the optimum spontaneously selects one stronger concept.

### Prespecified unequal importance: exact mono optimum

For `(I_1,I_2)=(1,1/2)`, suppose first the important feature is the stronger
column. Its loss is

\[
F=c(1+r)/6+a/8=1/8+c[(1+r)/6-1/8]\ge1/8,
\]

with equality only at `c=0`. If the important feature is the weaker column,
`F=c(1+r)/12+a/4>=a/4>=1/8`, with a positive extra term at `a=1/2`.
Hence the global optimum is to retain the important feature alone,
with loss `1/8`. This covers both sign sectors.

## 8. Prespecified numerical diagnostic and verification

`verify_derivation.py` independently implements the finite-interval
optimizer and the protocol's 361-angle diagnostic. It also includes the
two exact pair angles as candidates. `verification_results.json` contains
all six cases; `angular_profile.csv` contains all evaluated angles.

| p | importance | grid best angle | grid best loss | equal-pair loss | clean mono best loss |
|---|---|---:|---:|---:|---:|
| .05 | 1,1 | -45 degrees | .0273031496 | .0273031496 | .0475 |
| .05 | 1,.5 | -33 degrees | .0177429877 | .0204773622 | .02375 |
| .20 | 1,1 | -45 degrees | .1257142857 | .1257142857 | .16 |
| .20 | 1,.5 | -24 degrees | .0777528723 | .0942857143 | .08 |
| .50 | 1,1 | -67.5 degrees | .2464255651 | .25 | .25 |
| .50 | 1,.5 | 0 degrees | .125 | .1875 | .125 |

The first four rows remain **grid observations**, not global proofs. The
last two global optima are proved above. Because equal-importance symmetry
allows feature swaps and different sign sectors, an argmin angle is one
representative, not a unique solution.

Maximum equal-pair bias formula discrepancy: `6.94e-18`. Maximum pair-loss
formula discrepancy: `2.78e-17`. Maximum bias derivative discrepancy against
central finite differences away from kinks: `2.00e-11`. These are numerical
checks of the algebra, not independent theorem proofs.

The full dense-case global profile formula was also compared with the
finite-interval optimizer at every prespecified angle. Maximum discrepancy
was `1.11e-16`.

For the grid-best clean representations, importance-weighted actual
decoder detection errors are:

| p | importance | sigma=0 | .05 | .15 | .30 | .60 |
|---|---|---:|---:|---:|---:|---:|
| .05 | 1,1 | .005000 | .025695 | .042770 | .070936 | .290004 |
| .05 | 1,.5 | .027500 | .027500 | .028914 | .058254 | .223677 |
| .20 | 1,1 | .080000 | .080009 | .108939 | .215473 | .444691 |
| .20 | 1,.5 | .100000 | .113206 | .118165 | .159487 | .310257 |
| .50 | 1,1 | .500000 | .500000 | .502205 | .515959 | .638511 |
| .50 | 1,.5 | .250000 | .250000 | .250429 | .297790 | .452328 |

These are conditional exact Gaussian integrals at **grid-selected**
geometries; the lower-frequency geometries are not globally certified.
For example, at `p=.20`, importance `(1,.5)`, the clean MSE is below mono,
but clean detection error equals mono's `.10`: the weaker concept never
crosses the decoder's `.5` threshold even when present alone. At
`p=.05`, unequal importance, the grid-best clean detection error `.0275`
is worse than the clean-selected mono error `.025`, despite better MSE.
Thus improved reconstruction is not interchangeable with improved feature
detection, and the bridge must retain both reported quantities.

## 9. What is complete, and what remains

**Proved:** exact global bias minimization at any supplied rank-one code;
exact clean and noisy formulas for the bias-trained equal pair; a local
importance direction; global clean geometry optima for both prespecified
`p=.5` importance settings.

**Numerical only:** the angle minima at `.05` and `.2`; how projected Adam
converges to these profiles is the separate toy student's experiment.

**Unresolved:** a global low-p/importance geometry formula, its complete
noise-crossing boundary, larger loads, and real-model transfer. The method
retains the intended direction but does not finish the full Project 1
phase diagram. Neither this calculation nor successful validation is an
ICML acceptance guarantee or a verified novelty claim.
