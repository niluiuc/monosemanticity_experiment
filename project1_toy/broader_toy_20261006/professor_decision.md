# Professor decision after the prescribed broader clean-training stage

6 October 2026. This is a research decision and analysis of the existing five runs, not a new experiment. Root alone decides and records any follow-up protocol. No polishing, new training or noisy calibration was run for this assessment.

## Decision

**Stop the prescribed huge-Q/P calibration arm. Permit at most one bounded, identical optimization repair of all five saved final dictionaries, then close this toy family.** A pure learning-rate decay of the same Adam-plus-Euclidean-projection update is not my preferred repair. Use the already verified population gradient in tangent projected gradient descent with bounded monotone backtracking. This targets an evidenced optimizer blocker; it is not another search over scientific settings.

The paper's potentially new result is the critical boundary and its calibration-resistant prediction. A numerical demonstration of the already proved fixed-support limit at sigma approximately 11--15, and approximately 461,785 in one case, adds little to that contribution. A successful optimizer repair could provide credible higher-dimensional clean-trained examples for later transfer design. It would not establish a general training-selected load law or independently supply main-track novelty.

## What the existing runs establish

All five fixed-step runs completed without nonfinite failure, but all fail the predeclared loss-stability diagnostic. Tangent gradient norms at their final iterates are between .102 and .226. Only seed 0 beats mono in final clean reconstruction loss. Scalar bias reoptimization changes the losses very little and does not resolve the encoder issue.

Analysis of the existing final 100 records and checkpoint pairs shows continuing motion, not just a misleading scalar diagnostic:

| Seed | Final-100 loss range | Encoder change over final 100 updates | Earliest recorded minimum step |
|---:|---:|---:|---:|
| 0 | .24938585--.24942832 | .02136 | 1113 |
| 1 | .34942099--.35098363 | .14733 | 337 |
| 2 | .29704023--.29705205 | .02137 | 67 |
| 3 | .32598537--.32771341 | .08560 | 137 |
| 4 | .29824422--.29831574 | .04217 | 97 |

The earlier minima are reported as diagnostics only. They are not substituted for final dictionaries, and no favorable checkpoint is selected. In particular seed 1 previously attained .24502679 but ended at .35094817. Some runs are slowly drifting rather than rapidly oscillating, so describing all five as simple learning-rate oscillations would be unsupported.

The weighted tied-gradient finite-difference check passed with maximum error approximately 5.97e-11. Energy projection also preserves the intended resource constraint. Thus there is no evidenced gradient-algebra bug or resource mismatch. The evidence demonstrates inadequate optimization behavior of the fixed method, not an impossibility of the tied-ReLU architecture to outperform mono.

## Specific optimization blocker

The existing training routine forms Adam moments from the **full Euclidean gradient**, applies a coordinatewise preconditioned update, then rescales the encoder onto its Euclidean energy sphere. Its reported tangent gradient uses the correct Euclidean sphere tangent, but that tangent is not the update supplied to Adam.

At a smooth constrained optimum, the encoder gradient must be normal to the energy sphere. A normalized preconditioned update being radial does not in general imply that the unpreconditioned gradient is radial. Therefore a small step size or a small change in loss under this particular Adam-plus-normalization method is not by itself a stationarity certificate. Learning-rate decay may reduce drift, but it does not necessarily resolve the difference between these conditions. This is a reason to test a direct tangent descent repair rather than assume a decay schedule will suffice. It is not a claim that this mismatch has been proved to be the unique cause of all five outcomes.

At exact ReLU kinks, a selected ordinary gradient is not a complete nonsmooth stationarity test. A repair that stalls at kinks must remain explicitly unresolved; a large selected tangent gradient must not be hidden, and a tiny accepted step must not be relabeled as global convergence.

## Smallest repair, if root accepts it

Record a separate follow-up protocol before execution. Preserve every original run and its unfavorable summary. Use all five saved final encoders and biases; retain their identities, and make no seed or checkpoint choice.

- Same n=8, m=4, p=.2, importance, energy, population and objective; no other model family or data setting.
- Use the existing verified encoder and bias gradient, remove its radial encoder component, then retract the proposed encoder onto energy 4. Update biases with the same trial step. Do not reuse Adam moments for this repair.
- Start each trial at learning rate .01. Require actual objective decrease by the usual Armijo condition with constant 1e-4 and the squared tangent-plus-bias gradient norm; halve at most twelve times. A failed backtracking search is a recorded stop, not permission for another optimizer.
- At most 2,000 accepted updates per seed, with a hard total wall-clock budget of two minutes for all five. Save trial/backtracking decisions, complete accepted-update traces, final parameters and all failures. This is a fixed budget, not a promise of convergence.
- Report the original diagnostic alongside the repair diagnostic: final loss, fixed-W clean-bias optimum, energy, tangent and bias gradients, last-two-window loss change, minimum score distance to kinks, and stopping reason. Away from kinks, a small tangent-plus-bias gradient is stronger evidence than loss stability; at kinks or unsuccessful backtracking, stationarity remains unresolved.

This repair is much smaller than evaluating and globally calibrating 256-state objectives across approximately 80 noisy feature objectives at deliberately loose bound scales. It addresses why four final runs are worse than their earlier traces without retrospectively selecting those traces.

## Go / no-go after the one repair

**GO for using broader clean-trained evidence** only if the repaired outputs genuinely satisfy the declared convergence checks or have a separately justified nonsmooth stationarity assessment. Retain all five outcomes, including converged models worse than mono. A local optimum is still not a global optimum. Do not require a favorable comparison as the definition of successful optimization.

**NO-GO for further optimizer work** if this one repair fails, stalls, or retains unresolved diagnostics. Preserve the broader result as an optimization limitation and proceed with the proved two-feature critical mechanism. No second learning-rate schedule, optimizer sweep, restart, extra seed or alternative checkpoint is warranted by this protocol.

Even a successful repair does not warrant resuming the huge-Q/P arm automatically. Its support-limit interpretation is narrow and its finite scales may be non-informative. Review the repaired clean outcome first; any later corruption test must target whether the surviving mechanism transfers at useful finite noise, under a separate small protocol. The next paper-critical direction remains one matched-capacity vision representation experiment, with the same reconstruction outcome and calibration policies, after the controlled toy section closes.

## Why the support arm stops now

The general support result is mathematically valid for fixed nonzero columns and bias-only tied ReLU decoders. It is not a coherence theorem, and the high-noise support penalty also arises for orthogonal full-support codes. Seed 0's approximately 2e-6 columns expose the nonuniformity of this limit: tiny but nonzero columns cause a very large Q/P, even while clean decoding is almost constant for those concepts. The bound being loose is already a meaningful adverse finding. Spending substantial time verifying the limit at enormous sigma would neither cure the training blocker nor demonstrate a tight, useful robustness boundary.

Keep the theorem and this limitation in the manuscript, but do not sell this arm as the central new mechanism. The exact critical prediction, fair calibrated comparisons, and eventual finite-noise transfer deserve the remaining time.
