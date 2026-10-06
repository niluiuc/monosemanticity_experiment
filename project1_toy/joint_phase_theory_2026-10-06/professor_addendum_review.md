# Independent senior addendum: joint critical/support derivations

6 October 2026. Reviewed the complete revised
`research_notes/joint_phase_derivations_20261006.tex`, the saved four-case
verification record and the corrected `week_plan.md`. No new scientific
experiment or parameter sweep was performed for this review. Preliminary
independent calculations are in
`../paper_decision_2026-10-06/near_critical_professor_review.md`.

## Final mathematical source verdict

**Approved for integration into the existing derivation volume.** No
incorrect constants or remaining material proof gaps were found in the
revised source. Approval concerns the stated asymptotic/fixed-geometry
results, not an arbitrary-load clean optimizer, finite-epsilon guarantee,
publication novelty or acceptance prediction.

### Clean critical geometry and cubic gain

The exact branch difference expands with
A=-(sqrt(5)/2)*epsilon-epsilon^2/2. Stationarity gives the stated
K=sqrt(5)/(6*pc*qc), squared weak storage K^2*epsilon^2 and clean advantage
C*epsilon^3, C=5*sqrt(5)/(216*Dc*pc*qc).

The source correctly supplements the local series with compact argmin
continuity and the unique global mono geometry at pc. Every global clean
optimizer must enter the relevant important-strong, opposite-sign,
all-active-weak neighborhood. The nonzero stationarity equation has a
nonzero k derivative there, so the implicit-function solution is the
selected optimum rather than merely an arbitrary local branch.

### Frozen first and second noise scales

At sigma=t*epsilon^(3/2), strong shared gate distances are Theta(epsilon)
and weak distances stay positive. Gaussian switching tails are negligible
uniformly for compact t ranges, with exact zero-noise handling at t=0.
Shared noise coefficient Da+c/2 minus mono coefficient p+q/2 gives
B=qc*(1-2pc)/2>0. The resulting asymptotic local crossing constant
sqrt(C/B) is correct. The source does not assert global uniqueness or
a finite-epsilon bracket guarantee.

For sigma=k*x, the revised source now explicitly weights the conditional
unit-target expression by pc and the weak loss difference by importance
1/2. Its full pre-cancellation state sum reduces to the stated F(x), using
the displayed critical cancellation identity. Small-x positive B*x^2 and
large-x negative linear behavior are correct. Distinct fixed x brackets
give another crossing at the k scale, separated from epsilon^(3/2).
This establishes at least two FROZEN reconstruction-MSE crossings near
pc, not the earlier detection-error result and not an oracle-calibrated
second-crossing theorem.

### Oracle localization: requested proof completion is satisfied

The original draft stated localization without its global/uniform
justification. The revised source supplies the necessary argument:
uniform coercivity/negative-plateau comparison first localizes global
calibrated biases to strong zero and weak pc. Target-one means then stay
positive. Zero-target rectified-square smoothing changes the loss by at
most the noise variance because its derivative is 2-Lipschitz; target-one
terms obey the same order bound with exponentially small clipping terms.
Strong clean curvature at least 2p gives bias displacement O(sigma)=o(k),
so the minimizer lies strictly within the clean gate branch. Positive
noisy local curvature and the exponentially small gradient at the clean
bias then give negligible bias gain at the cubic scale. The weak profile
has nonvanishing gate distances and the analogous argument applies.

Mono's global localization and quadratic clean lower bound force bias
O(sigma), so minimizing the bounded scaled variable z is legitimate.
The strictly increasing stationarity equation p*z+q*M1(z,1)=0 has its
unique negative solution. Its coefficient v(p) is strictly below the
frozen mono coefficient p+q/2. Thus B_cal=Dc-v(pc)>B and the calibrated
epsilon^(3/2) exponent, with changed prefactor, follows. The source
correctly refrains from transferring F(x)'s second crossing to calibration.

### Arbitrary-load fixed-support calibrated bound

For nonnegative features with finite third moments, conditional Gaussian
density bounds and the integral of positive gain over [0,2X_i] give the
factor 4*E[X_i^3]/3. The bound is uniform over bias. The upper infimum is
supplied by bias tending to minus infinity, justified by finite second
moments. Dropped columns attain the prior-mean constant and its variance.
The support-dependent limit and finite full-support-versus-retention
bound P-Q/sigma follow with the correct importance weights.

The source uses infima rather than assuming finite-bias attainment.
The ReLU/L2 coupling inequality proves continuity of calibrated values
including zero, sufficient for a crossing from strict clean advantage
and positive dropped-mean mass. Feature dependence is allowed. The limit
concerns fixed support exposed to code noise, not coherence alone;
noise-dependent W or freely learned output gains are explicitly excluded.

## Finite checks and numerical plan

The saved finite checks are honestly reported. The failed upper critical
bracket at epsilon=.02 and negative gate-scale x=.05 checks are retained,
not replaced by preferred signs. They do not verify the complete two-
crossing diagram at these finite values, and the source does not claim
that they do. An asymptotic existence proof remains distinct from finite
bracket validation.

The initial calibrated plan had an actual precision incompatibility:
ordinary 1e-12 slack cannot attain the smallest requested cubic-scale
total gaps. The corrected plan applies 70-digit arithmetic to moment,
gradient AND lower/upper-bound calculations, with predeclared 1e-40 slack
and unchanged expansion cap. This resolves the predictable numerical
floor; it does not guarantee convergence within that cap. Failures must
remain unresolved rather than trigger unlogged retries.

The plan is bounded to six critical epsilon values, fixed map/bracket
counts, one larger binary family and one nonbinary amplitude check on the
same frozen dictionaries. These larger tests concern the general support
bound, not globally optimal larger geometry or a variable-load training
law. Keep that distinction in any resulting figure or manuscript.

## Research relevance and stopping decision

The critical law predicts a robustness boundary from clean-selected
geometry and distinguishes frozen versus calibrated decoder policy.
This is more informative than adding more isolated toy minima. The
general bound supplies a complementary fixed-geometry result under
broader amplitude/load assumptions. Its density technique is standard;
scientific novelty must be assessed at the level of this composition and
prediction, not claimed from correctness alone.

GO with the saved numerical validation plan, retaining finite failures.
Close the toy section after its prespecified limits and the independent
checks. No additional root-count, optimizer, architecture or distribution
campaign is authorized by this approval. Integrate the final finite
results into the same editable TeX/PDF and then use one prospective
real-model transfer of the surviving mechanism.
