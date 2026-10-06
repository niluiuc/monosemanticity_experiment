# Independent teacher approval: clean frequency transition

6 October 2026. Reviewed `derivation.md`, the symbolic checker and its
successful and failed records, and `../noise_limits.md`. This reviewer
did not write those student derivations. No training or frequency/angle
sweep was run for this review.

## Verdict

**Approved. The exact global clean storage transition is proved in the
declared two-feature family at importance `(1,1/2)` and energy one:**

`pc=(3-sqrt(5))/2=0.3819660112501051518`.

For `pc<=p<=1/2`, the unique optimal Gram geometry retains the important
concept alone. For `0<p<pc`, every global optimum shares the code with
both columns nonzero, and has opposite relative signs. The proof does
not give the complete selected mixed geometry as a formula at every
frequency; it does establish the sharing-versus-mono transition.

No material mathematical repair is required. The student deserves
credit for proving that the local stability threshold is also global,
rather than assuming away other sign sectors or nonconvex decoder-bias
minima. The explicit scope limits are appropriate.

## Independent algebra checks

`teacher_frequency_checks.py` constructs population quadratics from
explicit state masks, using the four Bernoulli state probabilities.
It independently derives strong/weak, same/opposite-sign bias and loss
expressions, including the weak two-active competitor. It verifies
25 exact identities and threshold inequalities; all pass in
`teacher_check_results.json`.

The test is symbolic, not a parameter scan. These identities alone do
not prove globality; the following interval and inequality review does.
The student's initially failed two checker identities were caused by
substituting `r^2=ac` before expanding squared expressions. The corrected
identities and the independent mask calculations agree. That logged
checker repair does not hide a changed mathematical assumption.

## Coverage review

Every energy-one rank-one geometry has two column norms with
`a>=c`, `a+c=1`, `r=sqrt(ac)`, and `k=sqrt(c/a)` in `[0,1]`.
The two relative-sign sectors and both assignments of importance to
the norm orderings are considered. Global sign has no effect on the
Gram matrix. Endpoints represent the two mono controls.

Fixed-geometry bias profiling is not assumed convex. Interval roots,
target-one derivative jumps, all-off plateaus and competing active
branches are accounted for.

### Same signs

For the strong column, the ordered bias roots place the global minimum
in the three-active interval. For the weak column, a bias `<=-c` misses
the single weak-feature state and incurs loss at least `pq`. The
feasible all-active bias has loss `pq*a`, strictly below that bound
when the code is genuinely mixed. Thus a possibly nonconvex negative
bias local minimum cannot improve the global profile.

For biases `>=-c`, the three-active stationary point is nonnegative,
so the objective decreases into the all-active interval. This proves
the student's weak global minimum for the entire probability range,
including below `pc`; it is not justified merely by feasibility.

The strong feature loss is no greater than the weak feature loss,
using `2r<=1`. Putting the greater importance on the strong column
minimizes the total. Even that ordering exceeds mono by

`pq*c*(p/2+2q*r)/(2-p)>0`.

Same-sign sharing is therefore excluded at every stated positive
frequency, not only above the transition.

### Opposite signs

The strong feature's three-active bias is globally optimal: earlier
interval roots lie beyond their right edges, the three-active root
lies in `[0,r]` because `p*c<=q*r`, and the all-active root lies to
the left of its interval. The student checks the full interval
direction rather than just one stationary equation.

The weak feature's potential two-active minimum is feasible only when

`p<=k-k^2<=1/4`.

Since `pc>1/4`, this competitor is absent throughout the claimed mono
region. This is the important nonconvex-branch exclusion; it cannot be
replaced by assuming the all-active weak decoder always wins.

Above `pc`, the remaining weak global profile is all-active for
`k<=p/q` and three-active for `k>=p/q`. Its lower feasibility follows
from the student's strictly positive decomposition of
`p*a+D*c-q*r`. The profiles agree at `k=p/q`. The all-off plateau
cannot be optimal: bias zero already improves it for a mixed code,
and the dropped-column constant optimum is `pq<p`.

For either remaining weak branch, the weak loss is at least the
strong loss. Thus assigning importance one to the stronger column is
best; the importance-swapped sector cannot evade the comparison.

## Global inequalities and threshold

For the all-active weak branch, the mixed-minus-mono difference is

`pq*c*[p-D/2+(1-2p)c+2pq*r]/D`.

On `[pc,1/2]`, all bracket terms are nonnegative, and the overlap term
is strictly positive for a mixed geometry. At `p=pc` the vanishing
first term therefore does not create an additional minimizing mixed
geometry.

For the three-active weak branch, its difference is a positive
prefactor times the student's quartic `H_p(k)`. Its derivative is

`4A*k^3 + 2p*k*(6q*k-1) + 2pq + 2(B+p)*k`.

Here `A>=1/4`, `B+p=-2(p^2-3p+1)>=0`, and `q*k>=p>=pc>1/6`.
Every term is nonnegative and the derivative is strictly positive.
At `k=p/q`, `H` is already positive by branch agreement and the
all-active inequality. Hence it stays positive on the whole remaining
domain. Both mixed branches, both importance orderings, and the
same-sign sector are excluded globally.

Below `pc`, the all-active weak branch is valid for sufficiently small
positive `k`. Its leading loss difference is

`pq*(p/D-1/2)*k^2+O(k^3)`,

with strictly negative coefficient. A feasible opposite-sign mixed
code therefore beats the best mono code. A global minimizer exists
by compact geometry and uniformly bounded representative minimizing
biases. It cannot be mono or same-sign. This proves the asserted
global storage label below `pc` without incorrectly claiming an
explicit or unique mixed optimum.

## Noise endpoint statements

The formula in `noise_limits.md` correctly uses Gaussian **code** noise
and the actual decoder threshold. For a nonzero column, conditioning
on each state gives the displayed normal CDF with standard deviation
`sigma*abs(w_i)`. Zero-noise ties require direct evaluation.

The clean-selected mono comparator has retained bias zero, omitted
bias `p`, and risk

`R_mono=Phi(-1/(2sigma))+p/2` for positive noise.

For a fixed mixed code with both columns nonzero and finite biases,
both feature errors approach `1/2`, giving weighted risk `3/4`.
Thus its difference from mono tends to `1/4-p/2`, strictly positive
for `0<p<1/2`. The document appropriately excludes `p=1/2` from that
strict inequality and states the fixed-geometry assumption.

These endpoint facts do not establish a negative-risk region, a
single monotone crossing, or an adversarial guarantee. A negative
finite-noise difference, if independently verified, must eventually
return positive. The limits of vanishing weak-column norm and
infinite noise need not commute.

## Approval and stopping boundary

This approval permits the separately preregistered Stage B numerical
verification of the theorem's specific predictions. It does not
authorize dense searches, training campaigns, new distributions or
larger model families. The global theorem concerns clean storage
selection at fixed importance and load; the operational noise-risk
diagram remains a separate calculation. Larger-load validity,
publication novelty and real-model transfer remain unresolved.
