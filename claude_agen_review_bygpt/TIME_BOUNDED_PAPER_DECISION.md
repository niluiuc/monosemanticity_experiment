# Project 1: decision from the existing evidence

Decision date: 7 October 2026. This assessment uses the assembled manuscript, claim-level source comparisons, notebook overlap addendum, saved delivery record, and Claude's independent review. No experiment, new mathematical extension, or search for favorable feature pairs was performed. Existing results below are restated, not newly proved here.

## Decision

**GO: finish one narrow paper around the clean-selected mono-versus-sharing corruption boundary and its dependence on decoder calibration.**

**NO GO: present the current evidence as a completed broad real-model phase diagram or as an established strong ICML main-track submission.** These are different judgements. There is a concrete theoretical result to write; its breadth and real-model validation fall short of the original ambition. Correctness does not settle publication significance.

Do not restart the project. Do not start a twenty-pair predictive-law project, diffusion training, additional audit cycle, or larger-toy repair as a prerequisite to finishing this version. Those require new scientific success, not a few hours of assembly.

## The exact question this paper answers

For representations selected by clean training in an energy-constrained, two-feature tied-ReLU bottleneck, when does corruption erase sharing's clean reconstruction advantage, and how does allowing both decoders to recalibrate their biases move that boundary?

This remains Project 1: a mono-versus-sharing robustness phase boundary. Calibration is a mathematically necessary evaluation condition inside that question, not a replacement with an unrelated project. Project 2 remains deferred.

The noise is scalar Gaussian **code noise**. The outcome is weighted reconstruction MSE. Neither adversarial image robustness nor recursive-training stability has been established by this result.

## The existing research contribution

1. **Clean selection:** the reviewed global result selects retention or opposite-sign sharing, including competing signs and bias regions, on explicitly restricted importance-frequency domains. It does not merely compare two handpicked vectors.
2. **Risk boundary:** near that clean storage transition, selected weak-feature energy is quadratic and sharing's clean gain is cubic in distance epsilon from the transition. The existing proved law is Delta_j/epsilon^3 -> -C_eta + B_j t^2 when sigma=t epsilon^(3/2). Its coefficients are derived rather than fitted.
3. **Policy dependence:** symmetric noisy-bias calibration changes B_j. At the special eta=2/3 endpoint, the same representations, task and noise have opposite frozen and calibrated risk orderings on the stated critical scale. This is a tuned endpoint, not generic evidence that mono always wins.

These three results belong in one argument: clean training selects a representation, then its robustness boundary depends on what the decoder may adapt. The Gaussian identities and numerical audits are supporting machinery, not additional contributions.

## Why this is more than repeating the anchor paper

[Zhang et al., ICLR 2025](https://arxiv.org/abs/2410.21331) already supplies the broad clean-versus-noisy mono/sharing tradeoff. Another example of reversal is insufficient originality. The proposed increment is the *globally clean-selected quantitative boundary with explicit symmetric decoder-policy coefficients*, under our stated resource constraint and distribution.

The existing source and notebook reviews identify no exact matching theorem for that increment. This is evidence of plausible narrow originality, not an exhaustive proof of priority. Exact clean risks, storage phases, continuous clean minima and the historical Gram alignment diagnostic already have antecedents.

The fresh bounded check also found an author-uploaded May 2026 preprint, [Truong, Superposition Phase Transitions in ReLU Networks](https://www.researchgate.net/publication/405430445_Superposition_Phase_Transitions_in_ReLU_Networks_Rigorous_Theory_and_Cross-Domain_Information-Theoretic_Connections). Its displayed model and main results concern sparse reconstruction capacity, prescribed tight frames, and clean loss comparisons. The inspected passages do not provide our external-code-noise frozen/calibrated critical-risk comparison. It further rules out marketing clean phase diagrams themselves as new. This assessment does not endorse that preprint's proof claims or certify every appendix against ours.

[Stevinson et al.](https://arxiv.org/abs/2510.11709) already studies interference-based adversarial vulnerability. [Prieto et al.](https://arxiv.org/abs/2603.09972) studies correlation-driven constructive interference. These are reasons to keep our actual task, assumptions and quantitative increment precise, rather than claim a general new theory of superposition and robustness.

## Evidence that must stay visible

| Evidence | What it establishes | What it does not establish |
|---|---|---|
| Global clean-selection proofs and scoped risk asymptotics | A quantitative controlled-model boundary | Arbitrary feature load, correlated continuous features, or a universal exponent |
| Fixed population checks and independent high-precision audits | Numerical agreement with the scoped theory | Directed-rounding certification of every numerical enclosure |
| Hidden ResNet channel pilot | A resolved differential calibration contrast | A resolved held-out mono/sharing winner or crossing |
| Prespecified class-evidence ResNet test | Sharing wins throughout the tested grid | A real-model phase boundary; no crossing occurred |
| Controlled image CNN | Existing toy reversal survives a learned perception front end | Independent native-network mechanism evidence; the recovery gate failed |
| Calibration-aware continuous-feature coefficient | Correct initial small-noise behavior | A prediction of the finite-noise crossing around sigma approximately 0.5 |

The independent review reproduced the coefficient and image risks and verified hashes/splits/prediction timing. It correctly judged the latest coefficient, coupling bound and image illustration insufficient as standalone contributions. That review does not by itself dismiss the earlier globally selected boundary theorem.

## Main-track assessment

My present judgement is that the theoretical core merits a focused manuscript, but I cannot responsibly call the current package a strong main-track paper. The two-feature scope, specialized decoder/noise class, special endpoint and missing native real-model boundary are substantive limitations. They cannot be repaired by stronger wording or more verification.

The controlled image illustration belongs as supporting evidence. Presenting it as independent real-model discovery would overstate the result. Likewise, the negative ResNet outcomes must not be converted into validation by retrospectively redefining success.

## Finish within the user's few-hour limit

- Freeze the question and the three contributions above.
- Use the existing mathematics and population outputs for the central argument and figures. No additional special cases are needed to explain that argument.
- Assemble the short manuscript; move audit history and failed optional directions to appropriately labelled limitations or supplement. Preserve the underlying records.
- Include the actual real-model outcomes, without claiming they validate the critical law.
- End with a submission-readiness decision based on this package. A stronger native-model claim remains unmet; it is not a hidden commitment to another week of exploration.

**Stopping decision:** close this research version by writing what has actually been established. Do not promise that hours of further work will produce the missing empirical mechanism or a guaranteed venue outcome.
