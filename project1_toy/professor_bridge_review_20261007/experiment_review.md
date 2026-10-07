# Empirical reviewer: applicability decision and the smallest justified next step

7 October 2026 UTC. This review is performed by an AI research reviewer assigned a senior empirical-research role, not by a real professor. Expertise is a review standard, not a credential claim.

## Research objective preserved

The objective is the clean-selected monosemantic-retention versus sharing corrupted-reconstruction phase boundary, including how feature frequency, importance and noise affect that comparison. A favorable sharing result by itself is not completion of this objective. The actual completed mathematical claim is considerably narrower than an arbitrary-load real-model phase diagram.

## Records inspected

Read workspace AGENTS.md, recent plan entries, the working manuscript, fixed head protocol and teacher decision, both real-test READMEs, and immutable normalized targets and clean angular-grid outputs. No model was trained, no representation extracted, no clean fit repeated and no new noise value evaluated. The companion theory reviewer and I exchanged critiques before choosing the diagnostic. We rejected an immediate importance schedule because the more elementary local-optimality prerequisite might already fail.

## Prospective diagnostic and stopping rule

Question: do the two archived target distributions have nonzero empirical covariance that permits first-order clean sharing improvement from an exact retained-coordinate solution?

Connection: the Bernoulli critical law relies on the absence of such a first-order term. A nonzero term can obstruct the storage transition before any corrupted-risk curve is drawn.

Minimum test: recompute train/calibration/test covariance and correlation from the saved normalized targets, and read only the closest already saved angular-grid neighbours at both coordinate-retention endpoints and both archived resolutions. Do not optimize, change importance, permute inputs, infer covariance significance, extrapolate to a natural population or evaluate noise.

Stop after these two pairs regardless of signs. The original records are immutable; diagnostic inputs are hashed and the script refuses to replace its original result file.

## Actual findings

| Fixed pair | Train covariance | Train correlation | Retain-first derivative along the explicit feasible bias path | Already saved 512-grid profiled same-sign angular secant |
|---|---:|---:|---:|---:|
| Hidden ResNet channels 0/1 | 0.09338142610709144 | 0.14391205255427922 | -0.12450856814278857 | -0.12354237918141961 |
| Class evidence tabby/golden retriever | 0.16331401299655118 | 0.3060476573493342 | -0.21775201732873490 | -0.21706549131802602 |

The derivative uses the existing importance eta=2/3 and fixed feasible biases (0, mean of the omitted coordinate). It is not asserted to equal the derivative of the globally bias-profiled value. The saved finite secants profile biases at each angle; their numerical agreement is corroboration, not an envelope-theorem proof. At the retain-second endpoint pi/2, adding the first coordinate with positive weak amplitude moves the angle downward: its angular derivative has the opposite sign to the weak-column feasible-path derivative. At both angular resolutions, the archived same-sign neighbour improves clean loss at each retention endpoint, including retaining the other coordinate. Negative-sharing neighbours instead increase loss. Positive covariance also occurs on the calibration and test splits; this is descriptive, without confidence intervals or a population-covariance claim. The hidden test correlation is only 0.04435; the head test correlation is 0.32496. The diagnostic JSON's `empirical_mono_directional_slopes` field records the feasible-path derivatives only; it should not be read as a profiled derivative claim.

The theory reviewer separately supplies the full assumptions and constructive local proof: nonnegative square-integrable coordinates with positive means and nonzero covariance permit a signed infinitesimal weak column to reduce clean reconstruction risk to first order. This is a proof about the declared model/distribution, not a proof about the entire ResNet or a novel regression principle. When applied to the saved empirical training distributions, it rules out exact coordinate retention as a clean global optimum for every strictly positive importance on both outputs. Optimization can only improve on the constructive candidate, so a separate profiled-optimizer certificate is unnecessary for that exclusion.

## Decisions

1. **NO-GO: treat either existing ResNet pair as a test of the independent-Bernoulli 3/2 storage-transition law.** Continuous target support and the same-sign selected geometry already differ; the covariance diagnostic now identifies a concrete lower-order obstruction, rather than merely listing mismatched assumptions.
2. **NO-GO: importance scanning these unchanged empirical pairs to find an exact clean mono/share transition.** The constructive obstruction persists for all positive importances. Numerical snapping of a tiny weak weight to zero would not establish the theoretical mono phase.
3. **NO-GO: extend noise until the desired sign appears.** A fixed noisy winner crossing, if found, would not alone validate the clean storage critical mechanism or its exponent. The earlier fixed-pair stopping rules remain in force.
4. **GO: integrate the applicability result and diagnostic into the existing derivation PDF and evidence hierarchy.** It explains why the completed real tests cannot validate the stronger phase-law claim. Keep their original risk results, including the unresolved hidden-pair winner and head-pair sharing advantage.

## Independent criticism and proof check

Read the companion theory review's full constructive proof. Its nonnegative, finite-second-moment and positive omitted-mean assumptions are necessary parts of the statement. The strong coordinate's reconstruction loss is quadratic even when its ReLU is at zero; the omitted output's strictly positive mean bias makes its first-order recovery accessible. The dominated-convergence clipping argument handles either perturbation sign and unbounded square-integrable inputs. Selecting a beneficial sign establishes a strict feasible improvement; it does not require differentiating a globally profiled optimizer. I found no missing step in this exclusion argument. The wording must retain 'feasible-path derivative' and must not claim an exact profiled-value derivative without a separate envelope proof. Neither this diagnostic nor its theorem causally identifies semantic features in the ResNet.

Both reviewers agree on the immediate stopping decision: terminate the unchanged-pair importance-transition proposal; integrate the constructive proof and saved diagnostic; make the next protocol depend on a mathematical prediction under the actual feature distribution. Do not execute a manufactured independence test as natural real-model transfer, and do not add a noise or pair hunt. This review identifies a blocked prerequisite, not an achieved native-transfer phase result.

## What a defensible further experiment would require

A new natural real-feature transition experiment is not ready to execute. A proposal must first identify the relevant native distribution, the actual local critical mechanism and a derived prediction under its correlations and support. Removing correlation by random permutations, reweighting or Bernoulli gating is an intervention on the input distribution, not evidence that naturally trained features obey the same transition. Such a test can be useful only when explicitly described as controlled or semi-synthetic.

Simply converting the saved outputs into independent binary gates would reproduce the existing Bernoulli toy in model-derived notation. That could check implementation or a finite-sample estimator, but it would not establish native real-model transfer or a new scientific contribution. Likewise, forcing independent features by permuting images breaks the original semantic co-occurrence and cannot be marketed as natural data.

The smallest next research decision is therefore mathematical applicability, not another extraction: decide whether the paper claims the exact controlled independent-feature law or develops a justified correlated-feature extension. The covariance exclusion is a relevant negative diagnostic but not itself the missing strong phase theorem. An extension must have an independently reviewed central claim and a bounded proof target before experiments. This review does not authorize a broad sweep or promise that a correlated extension is tractable within the remaining time.

## Correctness, novelty and significance are separate

The audited phase mathematics may be correct in its stated domain; successful code checks do not establish novelty. The new obstruction is ordinary first-order covariance exploitation, not a main-track contribution by itself. Its significance here is methodological: it prevents spending time on a setup that cannot contain the desired exact training-selected mono phase. It makes the paper's real-model limitation sharper, not its success stronger. The currently available real evidence still does not establish the critical boundary, the 3/2 exponent, semantic monosemanticity or improved full-model robustness.

Reproducible diagnostic: `covariance_diagnostic.py`; immutable output and input hashes: `covariance_diagnostic.json`. No plots are necessary for this two-row prerequisite check. No confidence or venue claim follows.

## Criticism of two proposed repairs

### A correlated Bernoulli extension

The proposed family P00=(1-p)^2+c, P10=P01=p(1-p)-c, P11=p^2+c preserves binary marginals but introduces covariance c. For c nonzero, the exclusion just proved already removes the exact coordinate-retaining clean optimum for every positive importance. A joint small-c/small-distance critical crossover could be mathematically interesting, but a global new correlated phase law would add substantial theory work and would not automatically explain the continuous saved ResNet distributions. The two reviewers recommend **NO-GO for a full correlated-Bernoulli extension as the immediate rescue**. No distribution/gate manipulation should be launched merely to keep the old exponent looking transferable.

### A guaranteed calibrated high-noise crossing on the actual score distribution

The alternative proposal is mathematically plausible but already covered by the existing derivation volume's section 'An arbitrary-load bound for fixed geometries under bias calibration'. It proves an asymptotic sharing-minus-mono limit P=sum of importance-weighted squared omitted means and the finite sufficient bound Delta>=P-Q/sigma, allowing correlated nonnegative inputs with finite third moments. Thus clean sharing gain and P>0 guarantee a calibrated crossing somewhere. This is an existing result, not new mathematics discovered by this review.

The source explicitly identifies the mechanism: every nonzero sharing column exposes its output to Gaussian code noise; optimally biased noisy outputs can asymptotically shut off, while mono's zero-column omitted output preserves a noiseless constant. Even a full-support orthogonal code has the same support-exposure effect. It is therefore a real property of the declared architecture and corruption, but not evidence of hidden-feature monosemanticity, the selected Bernoulli critical onset, its 3/2 exponent, or full-network robustness. A high-noise crossing would be a supplementary check of this existing conservative bound; it would not repair the missing strong transfer claim.

There is also an empirical calibration qualification. The population theorem optimizes biases for the same population on which risk is measured. In a finite calibration/test split, the omitted constant is the calibration mean, not automatically the test mean. When noisy outputs shut off, its test-risk improvement over zero is determined by the actual calibrated constant and test mean. One cannot plug the population squared-mean limit into held-out results without establishing that relationship and documenting estimation uncertainty.

**Decision: NO-GO as a new central real-model experiment justified by novelty or strong transfer.** Reopening the stopped noise grid until eventual constant-versus-noisy-output degradation appears would add an expected decoder/noise effect, not the missing critical mechanism. If root explicitly chooses a supplementary bound-verification claim, a genuinely new protocol must state this limited role, derive its bracket from training/calibration data without test outcome selection, use an unchanged held-out set honestly as reused data rather than fresh confirmatory validation, and retain all unresolved or absent signs. Neither reviewer presently recommends spending the binding time budget on that supplement.
