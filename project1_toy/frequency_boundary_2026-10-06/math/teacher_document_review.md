# Teacher review of the integrated Volume II additions

6 October 2026. This is a source/proof review, not a new scientific
calculation. It accompanies `teacher_project_readiness.md`. The final
typeset document also requires the root agent's compilation and layout
checks.

## Noise chapter: reviewed source

Reviewed `research_notes/project1_noise_update_20261006.tex`.

**Mathematical verdict: approved.** The chapter retains the correct
scope and substantially explains the derivations instead of listing
results. No incorrect risk formula, certificate argument or tail bound
was found. One short explanatory completion is recommended below to
meet the user's request for full derivations.

### Checks passed

- ReLU exceeds the positive threshold exactly when preactivation exceeds
  it. The actual clean decoder is correctly fixed during noise testing.
- The false-positive and false-negative CDF arguments have the correct
  signs and scale `sigma*abs(w_i)`. The four-state margin table correctly
  maps `00`, `10`, `01` and `11` to Gram entries. Shared scalar noise
  does not imply independent output errors and no such assumption is used.
- Zero columns and zero noise are explicitly handled by direct decisions,
  rather than divisions by zero or treating dropped features as perfect.
- The mono risk, rare-prior qualification and p=.20 weak-feature detection
  limitation agree with the independently certified records.
- The infinite-noise statement requires both nonzero columns and fixed
  finite biases. The strict positive difference excludes p=.5 correctly.
- The p=.05 cubic, rational root interval and bias formulas match the
  globally certified clean geometry, not the previous supplied equal pair.
- The two-root theorem proves strict clean margins, exact clean risk,
  a certified negative intermediate value and positive large-noise limit.
  The continuity argument produces two distinct positive roots without
  claiming exact counts or certified numerical locations.
- Interval addition, multiplication, reciprocal signs, square-root scaling
  and outward argument rounding are correct. Repeated root occurrences
  can widen enclosures without undermining their containment.
- Machin's tangent calculation includes its necessary angle/quadrant
  bound. The arctangent partial-sum indices 30 and 31 are correct.
- Even/odd exponential Taylor bounds use the signed Lagrange remainder,
  which holds for all nonnegative arguments regardless of initial term
  magnitudes. Integration gives the displayed CDF polynomials. Negative
  arguments and `[0,1]` clipping are justified.
- The exact risk enclosure is distinguished from displayed decimal
  endpoints and the 100-digit reference calculation. Every sign decision
  still belongs to the rational certificate.
- The selected-loss table, primary risk table and numerical crossing
  table agree with the saved reports. Approximate zeros and tiny gains
  are not relabeled exact or practically large. The clean phase proof
  is not inferred from discrete markers.
- The Gaussian ReLU tail bound follows from
  `|ReLU(mu+sZ)-b|<=|mu|+1+|sZ|` and squaring with
  `(x+y)^2<=2x^2+2y^2`. The two-sided Gaussian probability and second
  moment give precisely the displayed coefficients four. The review
  correctly treats the quadrature repair as a checker correction,
  preserving scientific outputs and acceptance tolerances.

### Requested explanatory completion: noncommuting limits

The sentence that weak-column and infinite-noise limits need not commute
is correct, but the new chapter currently states it without the short
derivation. Since the user asks for full derivations, add this existing
model argument rather than another experiment.

For fixed `0<p<1/2`, take a family approaching mono,
`W_e=(sqrt(1-e^2),-e)`, `e>0`, with biases tending to `(0,p)`.
For each fixed finite positive sigma, the weak coordinate's Gram score
and noise coefficient vanish, its reconstruction tends to constant p,
and its detection error tends to p. The strong score tends to the mono
score, so `R_e(sigma)->R_mono(sigma)`. On the other hand, at every fixed
e>0 both columns receive nondegenerate noise; `R_e(sigma)->3/4` as
sigma tends to infinity. Consequently

`lim_sigma->infinity lim_e->0 R_e = 1/2+p/2`,

`lim_e->0 lim_sigma->infinity R_e = 3/4`.

They differ for p<1/2. A supplied family with biases `(0,p)` suffices
to illustrate this statement; do not claim that every member of that
example family is the global clean optimum. The conclusion concerns
limits and does not alter any recorded numerical result.

### Remaining integration conditions

The preceding clean chapter must supply the reusable global certificate
procedure to which the noise chapter refers. The overall volume must
also distinguish supplied-pair threshold results from these selected
decoder results, retain the projected-Adam shortcomings, and explicitly
state the binary/code-noise/resource differences from the starting paper.
The readiness assessment provides the minimal next-step decision.

The source is approved as mathematics; final integration approval awaits
the clean chapter and cross-reference review. No scientific scope expansion
is needed to satisfy these document corrections.

## Clean chapter: completed independent source review

Reviewed all 647 lines of
`research_notes/project1_clean_update_20261006.tex` against the previously
reviewed derivations, exact certificates and independent checks. This was
a substantive proof and interpretation review, not a new parameter sweep.

**Mathematical verdict: approved.** No material mathematical error or
missing geometry sector was found. The fragment explains the mechanism
from the population training objective through globally selected geometry
to the actual detection rule, without treating a grid or an optimizer's
final iterate as a proof of optimality.

### Bias coverage and equal-pair result

- Expanding the fixed-active-set squared loss gives exactly the displayed
  coefficients A0, B0 and C0, including inactive target-one contributions.
  Positive-probability active sets have A0>0. Interval vertices, clipped
  endpoints, every breakpoint and the all-off plateau cover the global
  scalar minimum. The target-one downward derivative jump correctly
  explains why the entire objective need not be convex.
- Global sign equivalence and the half-circle angle interval cover all
  real energy-one rank-one encoders. Sign sectors and norm assignments
  remain distinct where they need to be compared.
- The mono comparator has biases (0,p), clean MSE I2*p*q and strict
  dropped-feature detection error p. The comparator is selected under
  the same training objective and resource budget.
- For the equal antipodal pair, the three nonconstant-interval roots
  are 1/2, N/D and p. Their interval positions prove the given bias is
  global for p<=1/2; the p>=1/2 completion agrees at the endpoint. The
  p=.05 and p=.20 score thresholds are the trained values, not a supplied
  midpoint. All four CDF terms and the zero-noise error p^2 are correct.
- The unequal-importance derivative follows on an open three-active
  branch at the balanced code, with r'(1/2)=0. Its stated sign and scope
  are correct: it establishes nonstationarity, not a global optimum for
  arbitrary probability or importance.

### Dense global optima

- The four roots in each strong and weak bias profile, for both relative
  signs, are correctly ordered against the respective breakpoints. The
  bounds c<=r<=a and 1+c>=2r establish the comparisons used in the proof;
  direct evaluation or continuity covers degenerate endpoints.
- Both sign sectors give the same profiled strong and weak losses at
  p=1/2. The reduced equal-importance objective has only the stated
  interior minimizing squared norm in [1/2,1]. The stationary equation
  is squared only where both sides are positive, so extraneous algebraic
  roots do not become claimed minima. Endpoint losses and the strictly
  better interior loss establish globality.
- At importance (1,1/2), assigning the important feature either norm is
  explicitly compared. The retained-important mono optimum is global;
  the reversed assignment cannot tie its loss. Equal importance does
  not force equal amplitudes or unique antipodality.

### Probability-one-fifth certificate

- The attaining branch, its feasibility interval, bias formulas,
  quartic rational objective, derivative cubic and stated algebraic root
  agree with the exact certificate reviewed previously.
- The full-real-line t parametrization plus its point at infinity covers
  every encoder modulo global sign. The regions separated by -1,0,1,
  joint bias candidates, stationary roots, feasibility boundaries and
  regional endpoints give a complete finite global comparison. Coincident
  scores on boundaries are not excluded by the generic-region counting.
- The chapter distinguishes the explicit attaining-branch calculation
  from the computer-assisted comparison. Its 256 branches, 1,031 raw
  candidates, 265 retained candidates, enclosure separation and mono
  endpoint values match the saved audit. The distinct active-subset
  reproduction supports the winner, while sharing the checked root
  backend is already disclosed in the review records.
- The weaker feature's maximum reconstruction is below 1/2, so clean MSE
  improvement does not improve its detection. The important feature's
  four strict decisions are correct, and total clean detection error is
  0.1, equal to mono's error.

### Full frequency-transition theorem

- The same-sign weak profile does not quietly assume convexity: its
  competing negative-bias part has a false-negative loss floor p*q,
  exceeded in quality by the feasible all-active candidate. The strong
  profile, best importance assignment and positive loss difference exclude
  all same-sign mixed encoders throughout the declared probability range.
- The opposite-sign weak profile includes two-, three- and all-active
  candidates and their feasibility restrictions. Target-one kinks cannot
  be minima; target-zero kink minima are covered by neighboring vertices
  on their closures. The all-off plateau is separately excluded. In the
  upper phase p>1/4 excludes the two-active candidate, rather than dropping
  it without evidence.
- Both surviving upper-phase profiles are at least the strong feature's
  loss, so swapping importance assignments cannot introduce an overlooked
  lower solution. The all-active loss difference is positive for every
  mixed encoder, including at the proposed threshold.
- The displayed H polynomial and derivative decomposition are correct.
  A>=1/4, B+p>=0 and q*k>=p>1/6 establish strict increase on the entire
  remaining three-active branch. Its boundary value agrees with the
  already positive all-active difference. This rules out off-axis
  preemption of the local transition.
- Below the threshold the small opposite-sign perturbation is feasible
  and its k^2 coefficient is negative. Compactness does supply a global
  minimizer: score magnitudes are bounded, the all-off plateau has a
  bounded representative, and sufficiently large positive biases only
  worsen squared loss. Restricting biases to [-3,3] loses no optimum.
- The equality case p=pc belongs to mono's region and has no mixed tie.
  Below pc the theorem correctly claims globally selected sharing without
  asserting a closed-form unique sharing geometry for every p.

The proof establishes a global **clean allocation transition at fixed
load and importance**, not an arbitrary-load robustness theorem. The
source says this plainly and gives corruption risk as a separate outcome.

## Updated noise chapter and final integration verdict

Re-read the revised noncommuting-limit argument, optimizer records and
paper-critical scope sections in
`research_notes/project1_noise_update_20261006.tex`.

**The earlier explanatory completion is now satisfied.** The supplied
W_epsilon family with fixed biases (0,p) proves both iterated limits for
0<p<1/2. It is explicitly a supplied family rather than a family claimed
to be clean-optimal. No additional experiment is needed.

The new optimizer paragraph retains all 36 projected-Adam outcomes and
the 27/9 loss-stability split, while distinguishing stability from
stationarity and global certificates from optimizer guarantees. The
readiness paragraph correctly limits pair replication to additive risk,
states the binary/code-noise/objective differences from the motivating
paper, and requests one prospective transfer protocol before substantial
compute. These are scientifically necessary qualifications, not reasons
to discard the valid toy result.

The subsequent p=1/20 explanatory addition is also approved. Independently
substituting p=1/20 into the three-active strong and two-active weak
population quadratics gives precisely the displayed quartic rational
objective. Exact symbolic subtraction verifies that objective, its
derivative, both bias formulas and the weak-branch feasibility inequality
against their separately written expressions (five identities passed).
The resulting cubic is explicitly a stationary equation; global selection
still comes from the existing complete branch certificate. This adds the
missing derivation to the document without adding a new scientific case.

**Final source verdict: both new chapters are approved for integration.**
No mathematical correction is required in the reviewed fragments. The
preceding pending-clean condition is resolved. The earlier request to add
the noncommuting-limit derivation is resolved. Compilation, figures,
cross-references and typeset layout remain the root agent's delivery
checks. Nothing in this approval establishes publication novelty,
real-model transfer or conference acceptance.

The disciplined next decision is the one in
`teacher_project_readiness.md`: integrate these completed proofs, compare
their exact assumptions and claims against direct prior theory, and
preregister a single bounded real-model transfer. Do not add extra toy
axes, root-count projects or a recursive diffusion pipeline merely to
increase the quantity of mathematics.
