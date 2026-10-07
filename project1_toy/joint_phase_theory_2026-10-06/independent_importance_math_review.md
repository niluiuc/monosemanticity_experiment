# Independent review: importance-family critical theorem

6 October 2026. Scope: proof completeness, interpretation and saved arithmetic for `importance_interval_derivation.tex`, the four previously executed cases in `importance_run_v1/results.json`, and their implementation. No new scientific cases, optimizer runs or scans were performed.

## Verdict

The global-selection and uniform frozen/calibrated critical laws are mathematically supported on the explicitly declared rectangle eta in [12/25,13/25], p in [7/20,21/50]. This is a real parameter-family extension of the fixed-importance result; it does not establish arbitrary importance, arbitrary load or real-network transfer. The crossing conclusion is existence and asymptotic location, not unique all-noise crossing count. Numerical calibration intervals remain high-precision bounds with declared slack, not a directed-rounding certification.

## Independent algebra and exact-root audit

The independent checker derives each branch's loss directly from the four Bernoulli states, rather than importing the production geometry evaluator. In a fresh `importance_exact_independent_review_v1/` run all ten symbolic checks passed, including the weighted all-active excess, three-active quartic, derivative cubic and derivative regrouping. For all four saved cases it independently reconstructed p and cubic coefficients in the quadratic field, enclosed the positive square root with 300 rational bisections, and verified the signs of the archived endpoint values by rational interval arithmetic. All saved 200-bisection root widths equal (1/8)/2^200; the 70-digit roots lie strictly inside them. No rounding of the algebraic probability to a rational surrogate occurred.

The production pair-sign rule is correct for positive nonsquare radicands: when rational and radical parts oppose, comparison of u^2 with rad*v^2 is decisive, reversed when the rational part is negative. Both chosen radicands are nonsquares. Multiplication and Horner coefficient ordering are correct. The numerical constants use the rationalized expression for pc without changing the exact probability.

## Global proof coverage

The proof invokes the existing complete finite bias-interval profiling result, including activation kinks and the all-off plateau. Positive importance does not change the fixed-output bias minimizer. It then covers both encoder sign sectors and both assignments of importance to column lengths. The strong/weak ordering makes that assignment reduction valid. For opposite signs the two-active weak branch is impossible because p>1/4; the three-active branch's lower feasibility condition is positive, so no additional disconnected weak branch is omitted.

The three-active quartic is strictly increasing on its entire feasible region: its regrouped derivative lower bound is 29/2500, and its matching-boundary excess bracket is at least 9417/68125. This excludes that region globally. In the surviving branch J'(k)>0, J(0)=A and J(1/8)>0 with the stated uniform rational bound. Thus below pc the stationary root is the sole global mixed minimum, while at and above pc every mixed excess is positive. Mono orientation and same-sign mixed alternatives were excluded separately. The endpoint k=0 and importance-swap degeneracy at a=c cause no competing global minimizer.

## Uniform asymptotic and calibration proof

The exact identity A(pc-epsilon)=-sqrt(1+2 eta-3 eta^2)*epsilon-eta*epsilon^2 and the nonzero uniformly bounded cubic derivative give the implicit-function expansion uniformly on the compact eta interval. Direct substitution yields the displayed positive C_eta and cubic clean gain. No fit is used.

For bounded sigma/epsilon^(3/2), the strong clean gate distances are order k=order epsilon, whereas noise is order epsilon^(3/2); Gaussian gate errors are therefore exponentially small uniformly. The weak output remains uniformly separated from zero. Those facts justify the frozen variance coefficient rather than a generic Gram-matrix margin interpretation.

The calibrated proof includes the needed global step: coercivity on the right, a uniform loss gap on the far left, compact localization, uniform convergence to the unique limiting bias optimum, and strong convexity of the clean local objective. The variance perturbation bound first gives an O(sigma) displacement, which is o(k), locking sharing into its clean activation branch. Only then can the exponentially small derivative correction justify the sharper bias displacement. This ordering avoids the common mistake of treating a local root as a global calibration optimum. For mono the bias scales as sigma*z; its strictly convex limiting scalar problem has the unique negative root displayed. Its minimum v(p) is strictly below p+q/2, so calibrated B exceeds frozen B and stays uniformly positive.

## Relevance and stopping decision

The result resolves a specific weakness: the 3/2 law is not restricted to an isolated importance ratio and survives symmetric decoder calibration. Four saved cases check implementation and finite signs; they neither prove the family theorem nor establish novelty. Do not add further nearby eta samples just to enlarge a plot. The next critical gap is a genuine learned representation transfer, or a materially different policy conclusion already identified by the endpoint protocol. Preserve the declared rectangle and code-noise/weighted-MSE target in the paper wording.
