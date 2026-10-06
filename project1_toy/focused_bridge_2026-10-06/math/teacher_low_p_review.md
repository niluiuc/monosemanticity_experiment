# Independent teacher review: one-case low-frequency global certificate

6 October 2026. Scope is exactly the authorized follow-up:
`p=1/5`, importance `(1,1/2)`, binary independent concepts, two features,
one code dimension, encoder energy one, tied ReLU reconstruction with
free biases. No training, parameter sweep, new distribution, or larger
model was run for this review.

## Verdict

**The student's computer-assisted global clean-geometry certificate is
valid for this one specified case. No material mathematical repair is
required.** It upgrades the earlier low-p grid observation to a global
population optimum, using a finite exact branch comparison rather than
assuming a numerical optimizer is globally correct.

Credit is warranted for checking all sign/retention sectors, preserving
the free-bias training objective, isolating roots exactly, and reporting
the uncomfortable consequence that a mixed reconstruction-optimal code
does not necessarily detect its weaker concept. The student correctly
does not claim a general phase diagram, a verified novel theorem,
universal optimizer convergence, or a real-model result.

## Student files and fresh reproduction

Reviewed `low_p_certificate.md`, `certify_low_p.py`,
`low_p_certificate_results.json`, and the candidate ledger. The original
script was imported and its output location redirected to the fresh
`teacher_low_p_reproduction/` directory. Original student results were
not overwritten.

The fresh reproduction completed in approximately 20.45 seconds. It
reproduced 256 joint ordered-interval branches, 1,031 raw root candidates,
265 distinct feasible candidate points, and zero competing candidate
intervals overlapping the winner. The winning cubic, bias formulas,
root isolating interval, and rational objective enclosure agree with
the student's records.

Reproduction alone is not independent confirmation of the proof's
completeness. The additional mathematical checks below address that.

## Completeness and exact arithmetic checks

### Geometry and bias coverage

`W=(1,t)/sqrt(1+t^2)` covers all finite geometries up to global sign.
The missing point has first column zero and retains concept 2, with
optimal clean loss `4/25`. Both infinities approach this same Gram
geometry. It is explicitly included as a competing endpoint.

For either feature, score order changes only at `t=-1,0,1`.
The four regions therefore cover every finite geometry. At a boundary
some score breakpoints coincide; evaluating the adjacent branch formula
remains valid by continuity. There is no omitted sign sector.

Within a region, the student's four breakpoint biases and four
nonempty-interval stationary biases contain every global fixed-geometry
bias minimum. Interval vertices outside their interval need not be
included because their constrained minimum is a breakpoint already
present. The all-off plateau attains its loss at the first breakpoint.
Jointly combining the two features' candidate lists is valid because
their bias objectives separate at supplied geometry.

Every resulting candidate is a rational function of `t`, with denominator
a positive constant times `(1+t^2)^2`. Its feasible domain is closed
under the interval inequalities. A finite minimum is stationary or on
a feasibility/region boundary; unbounded domains add infinity limits.
Constant branches are also covered by region/feasibility endpoints or
the infinity comparison. Consequently comparing those root candidates
does cover the entire population problem.

### Root and sign implementation

The code factors rational polynomials and isolates each irreducible
factor's real roots with rational endpoints. Feasibility signs are
decided by rational interval evaluation. When an interval straddles
zero, the gcd check detects an exactly shared root; otherwise the root
interval is refined until its sign is separated. It raises an error if
separation fails. No approximate floating-point sign is accepted.

The numerator-sign helper is valid here because all relevant denominators
are fixed-sign constants times powers of `1+t^2`. This assumption should
not be reused without checking it in a different problem.

Objective bounds use rational polynomial interval arithmetic and division
by an interval certified to exclude zero. All four numerator/denominator
endpoint combinations are considered. The selected winner's upper bound
is below every other candidate's lower bound and below both mono losses.
Duplicate removal only merges identical rational functions at identical
algebraic roots, so it cannot erase a lower candidate.

## Independent branch construction

`teacher_low_p_checks.py` constructs a different candidate family:
**all fifteen nonempty active-state subsets for each feature**, without
using score-order regions or kink names. This yields 225 joint subset
branches. Consistency requires every active state's preactivation to be
nonnegative and every inactive state's preactivation to be nonpositive.
The subset's stationary bias and loss are calculated directly from its
population quadratic. The reviewed root-isolation/interval backend is
shared; branch construction and coverage reasoning are separate.

This smaller family still contains the true optimum. At a ReLU kink,
activating a state with target one makes the bias derivative jump
**downward**. Such a kink cannot be a local minimum: the necessary
left derivative `<=0` and right derivative `>=0` are incompatible with
a downward jump. Kinks involving only target-zero states have a continuous
derivative and are captured by a feasible subset stationary point.
The remaining all-off plateau is excluded safely: either all-off feature
alone costs at least `1/10`, greater than the exhibited candidate.

The independent family has 30 distinct feasible candidate points after
deduplication. Its exact comparison identifies the same winning cubic,
root interval, objective and bias formulas, with zero nonseparated
competitors. Infinity and all-off losses are explicitly checked. This
is an independent confirmation of the mathematical candidate construction,
not a claim of an independently implemented computer-algebra library.

The attaining branch is `{00,10,11}` active for concept 1 and `{00,01}`
active for concept 2. Its exact formulas match the student:

`20t^3+175t^2-60t-59=0`, `t≈-0.44209023902340024406`,

`beta1=t(5t-1)/(21(1+t^2))`, `beta2=1/(5(1+t^2))`,

`F=(905t^4-320t^3+410t^2+441)/(5250(1+t^2)^2)`.

The symbolic derivative agrees exactly with the displayed derivative.
The optimal clean reconstruction loss is
`0.077752082516294294514`, strictly below mono loss `0.08`.
The first bias's three-state feasibility and the second bias's two-state
feasibility hold strictly at the isolated winner, rather than relying
on a numerical angle's rounded location.

## Clean detection implication and research interpretation

The teacher checks the exact sign of

`1/2-(t^2+1/5)/(1+t^2)`

at the isolated algebraic root; it is strictly positive. Thus the weak
concept's **maximum** clean decoder reconstruction is below `1/2` and
it is never detected by the stated strict threshold. Separately, the
teacher checks the strong feature's threshold-gap signs in all four
states; it is detected correctly in every clean state.

Therefore the selected mixed decoder has clean weighted detection error
`(1/2)p=1/10`, exactly the same as the clean-selected mono comparator.
Its advantage is in continuous squared reconstruction, not clean binary
detection. This distinction is a supported consequence, not a failure
of the algebra or grounds for changing the evaluation after seeing it.
The existing noisy-risk curves must likewise keep their decoder and
task definitions explicit.

The certificate addresses selected **population** geometry. A local
angular solver agreeing with it validates that one trajectory's solution;
it does not prove that projected Adam or all seeds converge there.
Gaussian risks can now be evaluated at a certified selected geometry,
but this proof does not supply a general noise-crossing theorem. The
reported finite noise values cannot establish a statement about all
positive noise strengths.

## Required repairs and stopping decision

No material repair is required. The student's serialization failure was
transparently recorded and did not alter scientific settings or algebra.
The bounded proof and independent review are complete; stop here under
the current follow-up protocol. Any next scientific extension needs a
new specific question and time-budget decision. The full frequency/load/
importance robustness boundary and publication novelty remain unresolved.
