# Applicability review: the missing real-feature transition

7 October 2026 UTC. This reviewer is an AI mathematical reviewer, not a human professor. Scope: existing importance-family theorem, continuous-target adaptation, manuscript, saved real-test protocols and reviews. No new feature extraction, model training, importance/noise sweep, or literature search was conducted.

## Verdict

The existing theorem is supported within its explicit two-independent-Bernoulli-feature model. Its extension to the two saved real-feature distributions was never justified. Their same-sign selected geometry, continuous amplitudes and dependence are not minor violations: covariance can remove the coordinate-retention storage transition altogether in the stated tied-decoder class. Searching for an importance-driven transition before checking this obstruction would be an avoidable experiment.

The paper-critical check is therefore a covariance/applicability check on the already fixed training arrays. If either real pair has nonzero empirical covariance, exact mono cannot be a local optimum of its empirical clean objective for any strictly positive importance. No new importance sweep is required to learn that fact. A numerical tolerance may nevertheless make a very small sharing benefit look like retention; that is not a proved population transition.

## What the established critical law actually assumes

- Two independent binary features with equal activation probability p, positive importances (1, eta), one scalar code, squared encoder energy one, a tied ReLU decoder, and free output biases.
- Global clean training over signs, importance assignments and bias branches. The importance-family proof covers eta in [0.48,0.52], p in [0.35,0.42]; its selected sharing branch has opposite signs.
- At the transition, weak amplitude is proportional to epsilon=pc-p and weak energy is quadratic. The exact clean advantage is cubic, not simply an unspecified small training gain.
- Selected sharing gates have distances of order epsilon from zero. On noise scale sigma of order epsilon^(3/2), Gaussian gate corrections are exponentially small, while mono has a retained-feature atom at its zero gate.
- The cubic clean gain and positive quadratic difference in corruption cost produce the 3/2 crossing scale. Calibration changes that quadratic coefficient. The special eta=2/3 endpoint has a separate proof and a frozen-coefficient cancellation.

Independence alone is not sufficient to import the exponent into continuous data. Conversely, approximate covariance zero alone does not establish independence, binary support, the necessary clean expansion, or the gate separation. A generic transition, even if observed, is not validation of this law.

## A paper-critical local obstruction, with full proof

### Assumptions and claim

Let X1,X2 be nonnegative random variables with finite second moments. Let mu2=E[X2]>0. Fix positive importance eta and the same energy-one, scalar-code, tied-ReLU architecture. Clean weighted risk is

L(w,b)=E[(ReLU(w1(w1 X1+w2 X2)+b1)-X1)^2]+eta E[(ReLU(w2(w1 X1+w2 X2)+b2)-X2)^2].

The coordinate-retaining geometry w=(1,0), b=(0,mu2) has risk eta Var(X2). If Cov(X1,X2) is nonzero, this geometry is not a local minimum of the jointly optimized clean objective. The analogous statement applies to retention of X2 if E[X1]>0.

This is a feasibility obstruction inside this particular comparator/decoder class. It is not a theorem that correlated concepts cannot be monosemantic in neural networks.

### Feasible perturbation

For |theta|<1 choose w(theta)=(sqrt(1-theta^2),theta), retaining b1=0 and b2=mu2. This exactly preserves encoder energy; the tied decoder is unchanged. Let s=sqrt(1-theta^2). The preactivations are

u1=(1-theta^2)X1+theta s X2,

u2=mu2+theta s X1+theta^2 X2.

The retained output has no first-order loss. Since ReLU(X1)=X1 and ReLU is 1-Lipschitz,

||ReLU(u1)-X1||_2 <= theta^2 ||X1||_2+|theta| ||X2||_2,

so its squared loss is O(theta^2), including observations with X1=0 and either sign of theta. Thus a retained-feature gate at zero does not invalidate the argument.

For the dropped output, write vtheta=theta s X1+theta^2 X2. Then vtheta/theta converges to X1 in L2. Because mu2>0, for every finite realization the gate is positive for sufficiently small |theta|. The clipping residual dtheta=ReLU(mu2+vtheta)-(mu2+vtheta) satisfies

|dtheta| <= |vtheta| 1{mu2+vtheta<0}.

For |theta|<=1/2, |vtheta/theta| <= |X1|+|X2|/2, an L2-dominating bound, while the indicator converges pointwise to zero. Dominated convergence gives ||dtheta||_2=o(|theta|). Consequently

ReLU(u2)=mu2+theta X1+rtheta, with ||rtheta||_2=o(|theta|).

Expanding its squared error and using Cauchy-Schwarz on terms involving rtheta gives

E[(ReLU(u2)-X2)^2]=Var(X2)+2 theta E[(mu2-X2)X1]+o(|theta|)

=Var(X2)-2 theta Cov(X1,X2)+o(|theta|).

Combining both outputs yields the feasible-path risk expansion

L(w(theta),(0,mu2))=eta Var(X2)-2 eta Cov(X1,X2) theta+o(|theta|).

Choose theta with the same sign as the nonzero covariance. The negative linear term dominates the remainder for sufficiently small |theta|, proving a strict improvement over coordinate retention. Allowing biases to be reoptimized can only improve on this feasible path. The same proof with indices exchanged covers the other orientation. Therefore, if both means are positive and covariance is nonzero, neither coordinate-retaining geometry can be a global clean optimum in this class, irrespective of strictly positive eta.

For finite empirical data this proof is simpler: bounded values and positive mu2 ensure the dropped output remains exactly active for sufficiently small |theta|, so its expansion is an elementary finite-sum expansion. Empirical nonzero covariance proves an obstruction for the empirical training objective; it does not by itself prove nonzero population covariance.

### Limits and interpretation

- Nonzero covariance is sufficient to exclude exact mono. Zero covariance is only a necessary condition for a mono optimum, not a sufficient condition for a transition or the 3/2 law.
- The benefit comes from first-order prediction of the omitted coordinate's deviations by the retained coordinate. Mono's decoder predicts that coordinate by a constant. A richer untied mono readout would be a different model and invalidate this exact comparison; changing it requires a separately specified question.
- Small importance multiplies both the constant-coordinate loss and its linear improvement. Thus eta approaching zero can make the improvement arbitrarily small without creating a positive-eta exact local retention optimum. A coarse angular grid can miss this distinction.
- Do not advertise this calculation as a major novel theorem: it is the familiar covariance/linear-regression mechanism expressed in the current constrained ReLU model. It is useful because it diagnoses the specific experimental mismatch without fitting anything or searching for a favorable outcome. A prior-work claim would require its own check.

## Saved-array diagnostic reviewed

The collaborating experiment reviewer saved `covariance_diagnostic.json` and a reproducible saved-record-only script. This mathematical reviewer read the recorded moments and neighboring grid losses; it did not rerun inference, fitting or corruption evaluation. TRAIN results are:

| Fixed pair | Means | Covariance | Correlation | Predicted retain-X1 slope at eta=2/3 | Saved 512-grid positive-side secant |
|---|---|---:|---:|---:|---:|
| Hidden channels | (.52040617, .65005986) | .0933814261 | .14391205 | -.1245085681 | -.1235423792 |
| Class evidence | (.69959241, .66504437) | .1633140130 | .30604766 | -.2177520173 | -.2170654913 |

Both means are strictly positive and both empirical covariances are nonzero. Both coordinate orientations also improve toward positive sharing in the archived grids. The secants are finite-step numerical agreement, not proofs of population derivatives. The constructive argument supplies the exact empirical obstruction; neither covariance nor a finite angular search is an inference about the unknown population. Calibration/test covariances are additionally positive in the saved records but were not used to choose a new pair or fit a prediction.

The displayed analytic slope is for the explicit fixed-bias feasible path, whereas the saved grid secant comes from profiled bias minima at a finite angle. Their agreement is an illustrative numerical consistency check, not identification of the profiled envelope's derivative. The local nonoptimality conclusion needs only the constructive path. At retention of X2, positive weak first-coordinate amplitude corresponds to decreasing the angular coordinate, so the angular secant has the opposite sign to the weak-amplitude slope.

These records resolve the immediate applicability blocker negatively: neither existing empirical training pair has the exact coordinate-retention onset needed by the current critical theorem. This does not prove that no corrupted-risk crossing exists at any noise level, and it does not discredit the Bernoulli theorem. It explains why extending the existing pair with an importance scan is not a justified route to validate that theorem.

## Consequences for the actual research direction

The broader mono-versus-sharing corruption question remains legitimate. The current paper already answers a narrow, globally selected model exactly. However, the central real-transfer target cannot be fulfilled by arbitrary correlated score pairs plus a few noise levels. The two existing pilots give different operational comparisons; neither tests the Bernoulli critical onset.

There are two distinct future claims:

1. **Validate the specific critical law.** Use an independently justified distribution that approximates the theorem's support, independence, gate behavior and selected clean branch. A deliberately generated Bernoulli feature intervention is controlled/semi-synthetic validation, even when feature amplitudes or images originate in a pretrained vision model. Do not call it natural real-model transfer.
2. **Validate a broader real-feature tradeoff.** Derive a prediction for the actual correlated continuous distribution and the stated comparator, then freeze that prediction and test it on held-out observations. No reason currently guarantees an importance-driven onset, a 3/2 exponent or a noise-induced winner reversal. Merely seeing a curve cross after tuning is insufficient.

Under the binding time constraint, first run only the saved-array covariance check and preserve its outputs. If nonzero, stop the proposed importance sweep for these pairs. Do not add a new pair/noise hunt, semantic resource search, diffusion loop, or optimization repair. Root must integrate this full applicability proof and saved-moment results into the existing derivation PDF before presenting it as a mathematical result. The next protocol must state which of the two future claims it tests and justify why its prerequisites hold.

## Specific extension decision: correlated Bernoulli phase analysis

Root asked whether to immediately replace independence by the fixed-marginal joint law P00=q^2+c, P10=P01=pq-c, P11=p^2+c. This mathematical reviewer recommends **NO-GO for a full new correlated critical-phase analysis now**. This is separate from the joint reviewers' agreed NO-GO for importance scans of the saved real pairs.

The four-state model is analytically tractable using existing finite bias profiling, but it is not a plug-in correction to the existing theorem. Nonzero c is exactly nonzero covariance and removes exact mono clean onset for every positive importance. A new transition story would therefore require comparison of genuinely different sharing branches, complete global selection, new local expansions and a new corruption prediction. Showing correlated clean sharing improves by a covariance term is not itself a strong novel paper contribution. Extending it into a full phase law would be substantial additional research, and would still not validate transfer to the continuous real pair merely because both distributions are correlated.

The exact blocker has already been resolved by the constructive covariance proof and saved moments. No new four-state sweep is necessary to establish that blocker. A correlated phase theorem would be justified only by an explicit new central question about how dependence changes the robustness boundary, with a separately reviewed global-selection/proof target and stopping budget. It should not be launched as an automatic reaction to an unsuccessful real transfer or advertised as an experiment that closes that gap. No new crossover exponent or correlation scale has been proved or asserted in this review.

## Specific alternative decision: eventual calibrated crossing

Root also proposed predicting a high-noise calibrated crossing for any fixed real sharing geometry, without a clean storage onset. The relevant statement is **already derived** in `research_notes/volume2.tex`, section `An arbitrary-load bound for fixed geometries under bias calibration` (lines 1777--1847 at the time of this review). It allows dependence, nonnegative targets with finite third moments and a fixed encoder. Its bias-uniform conditional-density bound is

E[X_i^2] - 4 E[X_i^3]/(3 sigma ||w_i|| sqrt(2 pi)) <= r_i(sigma) <= E[X_i^2]

for each nonzero decoder column, while zero columns attain Var(X_i) through an uncorrupted constant. Consequently the high-noise calibrated limit is the weighted sum of variances plus squared means for exactly those outputs exposed to code noise. Full-support sharing versus retention of coordinate1 therefore has limiting excess eta (E[X2])^2, and the existing P-Q/sigma bound gives a sufficient finite mono-favored region. The volume already proves continuity and the consequent existence of a crossing given a strict clean sharing advantage. Finite saved activation arrays satisfy the existing third-moment assumptions; strengthening it to only finite second moments is not needed for these data.

The corresponding frozen leading term follows by scaling the fixed-bias noisy preactivation by sigma and using ReLU Lipschitz continuity in L2: each output contributes I_i w_i^2/2 to R/sigma^2. Thus sharing-minus-retain1 divided by sigma^2 tends to -(1-eta)w2^2/2 when encoder energy is one. This leading scaling is elementary noise exposure, not a new critical law.

**NO-GO as the replacement central real-model validation.** A very-large-noise crossing would be forced by the comparator: mono's omitted-coordinate constant bypasses noise, whereas both mixed outputs receive it and eventually become effectively off under calibration. The existing volume explicitly notes that even a full-support orthogonal geometry has the same limit. Observing this forced high-noise crossing would not validate the Bernoulli storage onset, the 3/2 law, semantic monosemanticity, or robustness of the pretrained model. It can legitimately be reported as verification of the declared support/noise-allocation bound, but that is a different, already established within-project statement and should not be marketed as repairing the missing critical transfer.

No further noise fitting or widened grid is recommended merely to obtain the guaranteed crossing. A read-only P,Q calculation, if root needs it to assess bound usefulness, does not authorize a new risk experiment. Any such experiment requires a new prospective protocol and an explicit reason why it supplies evidence beyond the existing theorem's forced asymptotic behavior.
