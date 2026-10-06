# Frequency transition of clean-selected geometry

6 October 2026. Stage A of `../protocol.md`; mathematics only, with exact
symbolic checks and no new training or parameter/angle sweep. Fixed setting:
two independent Bernoulli concepts with common activation probability `p`,
one code dimension, tied ReLU decoder, free decoder biases, encoder energy
one, importance `(1,1/2)`, and `0<p<=1/2`.

Status: student derivation complete; independent teacher review passed
on 6 October 2026 (see `teacher_review.md` and `teacher_check_results.json`).
This result concerns **clean reconstruction-selected geometry**. It is not
already a noise-robustness phase boundary or a novelty claim.

## 1. The global transition

Let

\[
L_p(W,\beta)=\mathbb E\!\left[
 (\operatorname{ReLU}((W^\top Wb)_1+\beta_1)-b_1)^2
 +\tfrac12(\operatorname{ReLU}((W^\top Wb)_2+\beta_2)-b_2)^2\right],
\quad \|W\|_F^2=1.
\]

Set

\[
\boxed{p_c=\frac{3-\sqrt5}{2}=0.3819660112501051518.}
\]

**Theorem.** For `p_c<=p<=1/2`, the global clean optimum retains the
important concept alone: `W=(±1,0)`, biases `(0,p)`, loss
`L*=p(1-p)/2`. Every code with both columns nonzero has strictly greater
loss. For `0<p<p_c`, a mixed code strictly improves on this mono optimum;
hence every global minimizer uses both nonzero columns. Such an improving
code has opposite signs; same-sign sharing never beats mono in this setting.

In the convention `s=1-p`, clean selection favors sharing for
`s>(sqrt(5)-1)/2`, and mono retention for the complement, including equality.
This threshold is derived from training, not inserted into a fixed-dictionary
noise bound. The derivation below covers both signs, both norm orderings,
nonconvex bias branches, boundaries and dropped-feature endpoints.

## 2. Coordinates and fixed-bias profiling

Write `q=1-p`, `D=1-p+p²`. For a mixed code let `a>=1/2` be its larger
squared column norm, `c=1-a`, `r=sqrt(ac)`. Introduce

\[
k=\sqrt{c/a}\in[0,1],\qquad
a=\frac1{1+k^2},\quad c=\frac{k^2}{1+k^2},\quad
r=\frac{k}{1+k^2}.
\]

"Strong" below means the larger column norm, not the importance weight.
There are two ways to assign the concept importances to these columns.

For fixed geometry, each bias objective is a continuous piecewise quadratic.
Its candidates are active-interval vertices and score breakpoints, as proved
in the prior fixed-geometry derivation. The explicit profiles below also
compare possible nonconvex competing minima; feasibility is not inferred
from an optimizer's output.

## 3. Same-sign codes never beat mono

The strong feature's score offsets are `0,r,a,a+r`, with labels
`0,0,1,1`. Its bias breakpoints are
`[-a-r,-a,-r,0]`. In successive nonempty intervals, the unconstrained
stationary biases are

\[
c-r,\quad c-pr,\quad \frac{c-r}{2-p},\quad p(c-r).
\]

The first two lie beyond their intervals' right endpoints. The third lies
in `[-r,0]` because `c<=r`; the last lies at or left of zero. Thus the
global strong-feature bias and loss are

\[
\beta_s=\frac{c-r}{2-p},\qquad
S_+=\frac{pq\,c(1+2qr)}{2-p}.
\]

The weaker feature has offsets `0,c,r,c+r`, with labels `0,1,0,1`.
Any bias `beta<=-c` misses its single-feature state and costs at least `pq`.
The feasible all-active solution has bias `beta_w=p(a-r)>=0` and loss
`W_+=pq a<=pq`. For `beta>=-c`, the three-active vertex is
`(a-r)/(2-p)>=0`, so the objective decreases toward the all-active interval
and then attains its minimum at `p(a-r)`. Therefore this is the global
weak-feature solution. Possible negative-bias local minima do not improve it.

Since `2r<=1`, `S_+<=pq c<=pq a=W_+`. The smaller total loss comes from
assigning importance one to the stronger column. Even that assignment has

\[
S_++\tfrac12W_+-\tfrac12pq
=pq\,c\left(\frac{1+2qr}{2-p}-\frac12\right)
=\frac{pq\,c(p/2+2qr)}{2-p}>0
\]

for every mixed code. The swapped importance assignment is no better.
This excludes all same-sign sharing for the entire stated probability range.

## 4. Opposite-sign strong feature: exact profile

The strong feature's score offsets are `-r,0,a-r,a`; the corresponding
bias breakpoints are `[-a,r-a,0,r]`. Successive stationary biases are

\[
c,\quad c+pr,\quad \frac{p(c+pr)}D,\quad p(c+r).
\]

The first two lie to the right of their intervals. The third lies in
`[0,r]`: `p c<=q r` because `c<=r` and `p<=q`. The final root lies at or
left of `r` by the same inequality. Hence the three-active solution is
globally optimal:

\[
\boxed{\beta_s=\frac{p(c+pr)}D,\qquad
S_- =pq\,c-\frac{pq}{D}(qr-pc)^2
=\frac{pq\,c}{D}\left[p+(1-2p)c+2pqr\right].}
\]

The formula remains valid by continuity at mono and balanced endpoints.

## 5. Opposite-sign weak feature: all possible minima

Its offsets are `-r,c-r,0,c`, with bias breakpoints
`[-c,0,r-c,r]`. The candidates for a global minimum are:

| Branch | Optimal bias | Loss | Feasibility |
|---|---|---|---|
| Two active states | `pa` | `pq²a²+p²` | `pa<=r-c`, equivalently `p<=k-k²` |
| Three active states | `p(a+pr)/D` | `pq a-pq(qr-pa)²/D` | `p+Dk²-qk>=0` and `k>=p/q` |
| All active states | `p(a+r)` | `pq a` | `k<=p/q` |

The three-active loss, without abbreviated notation, is

\[
\boxed{W_3=pq\,a-\frac{pq}{D}(qr-pa)^2
=\frac{pq\,a}{D}\left[p+(1-2p)a+2pqr\right].}
\]

The first interval with only one target-one state
has its root beyond the interval. Target-one activation produces a strictly
downward derivative jump, so its kink cannot be a minimum; target-zero
activation has continuous derivative and is covered by vertices on interval
closures. The far-left constant loss is `p`; for `c>0`, the feasible bias
zero gives `pq a²+p²<p`, while the dropped-column endpoint has the optimal
constant loss `pq<p`. Thus selecting the smallest of the feasible
listed candidates gives the exact weak profile; feasible two- and
three-active minima can coexist at low `p`.

For the global transition proof we only need `p>=p_c>1/4`. Then the
two-active branch is impossible, because `k-k²<=1/4`. If `k>=p/q`, the
three-active lower-feasibility inequality follows from

\[
pa+D c-qr=[pa-(r-c)]+p(r-qc)>0.
\]

The first bracket is positive because `pa>r-c`, and the second is nonnegative.
Consequently, above the candidate threshold the weak profile is exactly
`pq a` for `k<=p/q` and `W_3` for `k>=p/q`, with agreement at the boundary.

In either branch `W>=S_-`: for the all-active branch use
`S_-<=pq c<=pq a`; for the three-active branch,

\[
W_3-S_- =\frac{pq(a-c)}D\left[q+2pqr\right]\ge0.
\]

Hence assigning importance one to the stronger column is always at least
as good in the regime needed for the global mono proof. This rigorously
covers the swapped ordering; it does not assume importance determines norms.

## 6. Global mono optimum for p>=p_c

### Weak feature all active: k<=p/q

Assign importance one to the strong feature. Its loss difference from mono is

\[
\Delta_A=S_-+\tfrac12pq a-\tfrac12pq
=\frac{pq\,c}{D}
 \left[p-\frac D2+(1-2p)c+2pqr\right].
\]

For `p_c<=p<=1/2`, each term in brackets is nonnegative:
`p-D/2=-(p²-3p+1)/2>=0`, `1-2p>=0`, and `r>=0`.
For a mixed code `c>0`, the bracket is strictly positive. Thus mono is
strictly better throughout this branch, including exactly at `p_c`.

### Weak feature three active: k>=p/q

The difference can be written

\[
\Delta_3=\frac{pq}{2D(1+k^2)^2}H_p(k),
\]

\[
H_p(k)=(1-p-p^2)k^4+4pq k^3+(-2+5p-2p^2)k^2
 +2pq k-p^2.
\]

Put `A=1-p-p²`, `B=-2+5p-2p²`. On `[p_c,1/2]`,
`A>=1/4` and

\[
B+p=-2(p^2-3p+1)\ge0.
\]

For `k>=p/q`, therefore

\[
H'_p(k)
=4Ak^3+2pk(6qk-1)+2pq+2(B+p)k>0,
\]

because `qk>=p>=p_c>1/6`. At `k=p/q`, the two weak-bias branches match,
and `H_p` is positive by the already proved all-active difference. Thus
`H_p(k)>0` throughout this branch as well.

Same-sign geometries were excluded in Section 3; importance swaps were
covered in Section 5. A dropped important concept gives loss `pq`, larger
than the optimal mono value `pq/2`. This completes the global comparison.

## 7. Sharing strictly wins below p_c

Take an opposite-sign perturbation of the important-concept mono code,
with `k>0` sufficiently small. The weak feature is all active because
`k<=p/q`, and the exact difference is the expression `Delta_A` above.
Since `c=k²+O(k⁴)` and `r=k+O(k³)`,

\[
\Delta_A=pq\left(\frac pD-\frac12\right)k^2+O(k^3).
\]

For `p<p_c`, this quadratic coefficient is strictly negative. Hence there
is a sufficiently small feasible mixed code with loss below `pq/2`.
The globally minimized fixed-bias objective is continuous in geometry
(all minimizing biases can be bounded uniformly), and the energy-one code
circle is compact, so a global optimum exists. It cannot be mono because
mixed codes have strictly lower loss; it cannot have same signs by Section 3.

This establishes the global sharing/mono threshold without asserting a
unique or explicit sharing geometry at every `p<p_c`. The exact finite
weak-profile candidates above and the previous one-case certificate remain
available to characterize selected geometries at stated frequencies.

## 8. What this predicts, and what it does not

The **local** threshold is also the **global** threshold in the declared
family: it is not preempted by an off-axis competing optimum. At the
threshold itself, mono is the unique geometry modulo global encoder sign.
Below the threshold, the geometry is mixed but generally not an equal pair.

This does not say that mixed geometry necessarily yields better binary
detection. The previously certified `p=.20` solution reconstructs the weaker
concept more accurately in squared error while never detecting it with the
decoder's `.5` threshold. Gaussian risk must be calculated using the actual
selected geometry and biases, not inferred from the clean phase label.

Stage B should verify a small, preregistered set of frequencies near the
derived threshold with the existing exact global-candidate machinery and
four-state noise integration. This Stage A calculation does not run it.

The result fixes `n/m=2`, importance ratio two and binary independent
features. It is not the full variable-load/importance theorem, a biological
application, a benchmark, a new agent system, or an ICML acceptance guarantee.
Its novelty relative to published theory remains a separate question.

## 9. Symbolic verification record

`verify_frequency_transition.py` verifies fifteen exact identities and
threshold inequalities; all pass in `verification_results.json`, using
SymPy 1.14.0. The initial checker failed two identities because it attempted
to substitute `r²=ac` before expanding squared expressions. Expanding first
repaired the checker; the formulas and research assumptions were unchanged.
That initial output is preserved in `verification_initial_checker_failure.json`.
The global inequalities and branch completeness are the arguments above,
not consequences of merely running symbolic simplification.
