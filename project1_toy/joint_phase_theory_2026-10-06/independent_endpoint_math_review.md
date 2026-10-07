# Independent professor review: singular endpoint policy contrast

6 October 2026. Reviewed `endpoint_calibration_derivation.tex` and the fixed `endpoint_policy_protocol.md`. This review covers proof completeness and relevance; it does not execute or choose endpoint validation cases.

## Verdict

Approved for the two prescribed finite checks, with all unfavorable or unresolved outcomes retained. The analytic result is a qualitative strengthening of the critical-boundary mechanism: at eta=2/3 and p approaching 1/2 from below, the same globally clean-selected representation and the same code noise can have opposite sharing-versus-mono risk orderings under frozen and symmetrically calibrated biases. This is not simply another nearby parameter sample. It isolates decoder evaluation policy as a material part of the comparison.

## Global selection

The inherited finite activation-interval proof is essential and correctly invoked: it supplies free-bias profiling, kinks, all-off and sign sectors. At p=1/2 the mixed excess in both signs is cr/6; it is strictly positive for every mixed k. The swapped importance assignment is covered by strong-loss/weak-loss ordering, and reversed mono has higher loss.

On the finite strip 99/200 <= p < 1/2, the opposite-sign cubic is strictly increasing and has one root in (0,1/8), below p/q. The three-active region's regrouped derivative has a positive lower bound from 4A+4pq/3 > -.0204+.3332 > 0 after dropping its nonnegative terms; its matching-boundary bracket is positive. Thus that whole competing region is excluded, not only sampled.

The same-sign exclusion is also valid. A negative same-sign excess requires r < epsilon/(3q) <= 2epsilon/3. Since k<=1 and r=k/(1+k^2)>=k/2, this first bounds k<4epsilon/3<=1/150. Substituting back gives k<(2/3)(1+1/22500)epsilon<(167/250)epsilon. Therefore its excess is greater than -[(167/250)^2/9]epsilon^3 > -.05epsilon^3. The feasible opposite geometry k=epsilon has bracket at most -1/2 and prefactor pq/[D(1+epsilon^2)^2]>.32, so its excess is strictly below -.16epsilon^3. It beats every same-sign candidate. No remote geometry or importance orientation is left unexamined.

The symbolic audit already independently derived the general branch formulas from four-state losses and verified the endpoint identity cr/6 for both signs. The clean expansion k*=4epsilon/3+O(epsilon^2) follows from the cubic derivative 3/4 at zero; direct substitution gives the opposite cubic clean gain 16/81. The same-sign local gain 16/2187 is consistent but is not used as a substitute for global exclusion.

## Frozen and calibrated risk limits

For fixed bounded t with sigma=t epsilon^(3/2), gate distances in the selected strong feature are order epsilon and its noise is order epsilon^(3/2). Conditional Gaussian gate corrections are exponentially small. The weak output remains uniformly all-active. Its noise variance is additionally multiplied by c=O(epsilon^2). The sharing coefficient tends to D0=3/4; frozen mono also has coefficient (1+p0)/2=3/4. Their difference is O(epsilon), hence contributes O(epsilon^4), leaving the negative clean cubic coefficient. This proves sharing wins on every fixed finite scaled-noise value asymptotically. It does not prove all-noise ordering or a replacement frozen crossing exponent.

The global calibration step is present and logically ordered: compact localization of global minimizers, convergence to unique limiting clean biases, strong-convexity plus variance perturbation to obtain displacement O(sigma)=o(k), activation-region locking, then the exponentially small derivative correction. One cannot skip localization and infer global calibration from a local root. For mono the limiting strictly convex z-problem has the unique negative root and v(1/2)<3/4; hence Bcal=3/4-v(1/2)>0. The calibrated risk limit -16/81+Bcal*t^2 and the displayed threshold follow. Numerical decimals are explicitly separated from exact formulas.

## Interpretation and next stopping decision

This theorem is a population weighted-MSE/code-noise result for a particular clean-trained tied ReLU bottleneck. It supports a decoder-policy mechanism, not a universal semantic-monosemanticity claim, adversarial margin or image-input robustness claim. It also does not establish external literature novelty by itself.

The fixed epsilon=.005 and .001 checks at t=2tc are sensible finite validation points but the theorem does not promise their signs at those finite distances. Run only them, keep a failing bracket/sign rather than adjust settings, and stop. If the predicted contrast resolves, integrate the complete result and the existing importance-family theorem into the paper's central story before considering additional variants. Genuine learned-vision transfer remains the next external-validity gap.
