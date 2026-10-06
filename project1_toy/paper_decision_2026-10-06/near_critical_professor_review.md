# Independent senior review of the proposed critical and support laws

6 October 2026. This is a proof review of the proposed extension, not a
new experiment or sweep. The parent is preparing the full derivation;
final source approval remains contingent on that written proof. The
calculations below identify valid steps and the precise global/uniform
arguments needed, without opening another research direction.

## Near-critical clean selection: constants and global route check out

Use the already proved unique important-concept mono optimum at
pc=(3-sqrt(5))/2, importance (1,1/2), and the exact all-active weak branch.
Set p=pc-epsilon, A=p-D/2 and q=1-p. Then

    A=-(sqrt(5)/2)*epsilon-epsilon^2/2,
    Delta=(p*q/D)[A*k^2+2*p*q*k^3+O(k^4)].

For the nonzero critical point this gives

    k*=(sqrt(5)/(6*pc*qc))*epsilon+O(epsilon^2),
    Delta(k*)=-C*epsilon^3+O(epsilon^4),
    C=5*sqrt(5)/(216*Dc*pc*qc).

These constants were independently derived by substitution into the
existing exact loss, not estimated by a fit. They are correct.

A local series alone does not establish that the selected global optimizer
follows this branch. The required route is short and uses completed work:
compactness/continuity and uniqueness at pc imply every global clean
optimizer approaches mono as p approaches pc. Its strong column must be
the important one; same signs are already globally excluded. It therefore
enters the all-active weak neighborhood. Divide the stationarity derivative
by k and apply the implicit-function theorem at (pc,0), where its k
derivative is nonzero. This gives a unique small positive minimizing
stationary point. The existing strict clean improvement excludes k=0.
This is a bounded completion of the global result, not a new optimizer
campaign.

## Frozen first-noise scaling: valid with a uniform gate argument

For sigma=t*epsilon^(3/2), both clean-selected shared biases have their
stated active patterns with strong zero-target gate distances Theta(k),
while weak gate distances stay positive. The strong active probability is
D and the weak column is all active. Its MSE noise coefficient is
D*a+(1/2)*c. Mono's coefficient is p+q/2. At pc their difference is

    B=Dc-(1+pc)/2=qc*(1-2*pc)/2=pc^2/2>0.

With k=Theta(epsilon), gate-switch corrections at this sigma scale are
exponentially small in 1/epsilon, uniformly for bounded t. Thus the
proposed expansion

    Delta=-C*epsilon^3+B*sigma^2+o(epsilon^3)

is supported, and sign brackets locate a crossing with scale
sqrt(C/B)*epsilon^(3/2). Do not assert uniqueness among all noise roots.
If naming this the FIRST crossing, the proof must include uniform
negativity for the entire interval t in [0,t_left], not merely two
pointwise signs. Uniform gate-error estimates on [0,t_max] supply that
extra statement without additional experiments.

## A distinct frozen scale: formula and signs check out

At sigma=k*x, with fixed x>0, the strong zero-target states contribute
the nontrivial rectified Gaussian moments. Target-one strong states remain
away from the gate; weak-column noise is of order k^2 and is negligible
at the k^2 loss scale. With t0=pc^2/Dc=pc/2,

    Delta/k^2 -> F(x),
    F(x)=qc[qc(M2(t0,x)-t0^2)+pc*M2(t0-1,x)-x^2/2].

For small x, F(x)=B*x^2 plus exponentially small terms, so it is positive.
For large x, the quadratic terms cancel and

    F(x)=2*qc*(t0-pc)*x/sqrt(2*pi)+O(1),

which is negative. Choosing fixed positive x brackets with these opposite
signs gives another frozen reconstruction-MSE crossing at scale Theta(k),
distinct from the epsilon^(3/2) crossing. This proves existence, not a
total root count or uniqueness at this second scale. It is a reconstruction
result, distinct from the earlier thresholded-detection crossings.

## Oracle calibration: coefficient changes; an assumption is insufficient

Mono's retained-feature calibrated bias is of order sigma. Its leading
coefficient z_p<0 is the unique solution of

    p*z+q*(z*Phi(z)+phi(z))=0.

Strict increase follows from derivative p+q*Phi(z)>0. Define

    v(p)=min_z {p*(1+z^2)+q*M2(z,1)}.

This is strictly below p+q/2 because the derivative at z=0 is positive
and the minimizing z is negative. The calibrated mono noise coefficient
is v(p). The corresponding proposed first-crossing coefficient is

    B_cal=Dc-v(pc)>B,
    sigma_cal ~ sqrt(C/B_cal)*epsilon^(3/2).

To use this law, prove that shared bias calibration changes the frozen
loss by o(epsilon^3) uniformly on the relevant scale. A valid route:
global calibrated minimizers localize to strong bias zero and weak bias
pc by the clean limit. In a small strong-bias neighborhood, target-one
preactivations stay near one, giving uniformly positive curvature;
the weak-feature means stay positive, also giving positive curvature.
At the clean-selected biases, derivative corrections are exponentially
small because strong gate gaps are Theta(k) and sigma is smaller than k.
Strict local convexity then makes bias displacement and objective gain
negligible at the cubic scale. This global localization/convexity argument
must be written. Assuming that shared biases simply stay unchanged would
leave a material gap.

No inference about the calibrated second crossing follows automatically
from the frozen F(x); it is a different optimization regime.

## General calibrated support law: verified under explicit assumptions

Let features X_i be nonnegative with finite third moments, importance
weights positive, W fixed and finite, and code noise an independent
isotropic Gaussian. Write g_i=ReLU(w_i^T(WX+sigma Z)+beta_i).
For a stored column w_i!=0, conditional on the entire X, the positive
output density is bounded by 1/(sigma*||w_i||*sqrt(2*pi)). Its atom at
zero contributes zero to positive gain. Since

    (2*y*g-g^2)_+ vanishes outside 0<g<2*y,
    integral_0^(2*y) (2*y*g-g^2) dg=4*y^3/3,

uniformly over beta_i,

    E[X_i^2]-E[(g_i-X_i)^2]
       <=4*E[X_i^3]/(3*sigma*||w_i||*sqrt(2*pi)).

Taking an infimum over biases preserves this lower risk bound. Bias
going to minus infinity supplies the upper infimum E[X_i^2], using
dominated convergence from finite second moments. A zero column exactly
predicts its mean, with risk Var(X_i). Hence

    R_cal(sigma) -> sum_i I_i*Var(X_i)
                    +sum_stored I_i*(E[X_i])^2.

Use INFIMUM unless finite-bias attainment is separately proved. This
distinction accommodates the all-zero target and other limiting cases.
The theorem is a fixed-support architectural limit, not a universal
monosemanticity theorem. A full-support orthogonal code has the same
limiting form. Jointly optimizing W(sigma), shrinking column norms with
sigma, arbitrary decoder gains and other readout classes are not covered.

For full support versus a mono comparator retaining subset S, the finite
comparison is

    R_full_cal-R_mono_cal
      >= sum_(i notin S) I_i*(E[X_i])^2
          -sum_i 4*I_i*E[X_i^3]/(3*sigma*||w_i||*sqrt(2*pi)).

If the dropped-mean mass is positive, sufficiently large finite sigma
strictly favors mono. This bound is valid at arbitrary fixed load; it
does not optimize geometry or derive a variable-load packing boundary.

## Continuity and the crossing claim

There is a uniform continuity proof not requiring existence of a bias
minimizer. Couple the same X,Z at two sigma values. ReLU is 1-Lipschitz,
so for every bias

    ||g_sigma,beta-g_tau,beta||_2
      <=abs(sigma-tau)*||w_i||.

Reverse triangle inequalities, followed by taking infima in both
directions, give

    abs(sqrt(inf_beta f_i(beta,sigma))
        -sqrt(inf_beta f_i(beta,tau)))
      <=abs(sigma-tau)*||w_i||.

Calibrated feature risks and weighted sums are continuous including zero.
A strict calibrated clean advantage and the positive high-noise support
gap therefore imply an actual finite crossing, rather than only an
eventual change in ordering.

## Research judgment and final approval condition

The critical law is a prediction from clean-selected geometry, not a
curve fit or another isolated root calculation. The support bound supplies
a controlled arbitrary-load statement, although its simple density-bound
technique is standard mathematics and its application is architecture-
dependent. These are stronger candidate contributions than collecting
more special cases. Verification does not establish novelty; direct
prior comparisons must be about these precise laws and restrictions.

The next numeric protocol should test the predicted rates/brackets with
a small fixed set and a stop criterion, not search for a favorable phase.
This review runs no such numerical test. Final source approval awaits
the complete written global and uniform proofs and their integration into
the existing companion PDF.
