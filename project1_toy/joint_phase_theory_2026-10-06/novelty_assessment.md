# Claim-level novelty assessment — 6 October 2026

Read together with ../paper_decision_2026-10-06/exact_claim_comparison.md and the earlier literature audit. This update does not certify that all existing literature has been exhausted.

## Established foundations we do not claim

- Elhage et al., Toy Models of Superposition (2022), https://transformer-circuits.pub/2022/toy_model/index.html: sparsity/importance storage phases, biased tied-ReLU reconstruction, and analytical two-feature comparisons. Our architecture and basic phase concept are inherited.
- Zhang et al., Beyond Interpretability (ICLR 2025), https://arxiv.org/abs/2410.21331: monosemantic robustness gains and clean/noisy tradeoff analysis. Another qualitative reversal is insufficient novelty.
- Scherlis et al., https://arxiv.org/abs/2210.01892: analytic capacity allocation in a different model. Renaming its capacity metric is not a contribution.
- Gorton and Lewis, https://arxiv.org/abs/2508.17456: geometry-dependent adversarial vulnerability and an antipodal robustness dip. Nonmonotone robustness alone is not ours.
- Elimadi et al., https://arxiv.org/abs/2608.22155: robust training/feature retention. Dropping features to improve robustness is already discussed.

## Specific candidate addition

Compose a proved global clean selector with exact corrupted MSE in the SAME resource-matched model. Near its storage transition derive weak energy proportional to epsilon^2, clean advantage proportional to epsilon^3, and a risk boundary at sigma proportional to epsilon^(3/2). Derive how symmetric oracle bias calibration changes the coefficient, and prove at least two frozen-MSE crossings in the asymptotic neighborhood. These constitute a predictive calculation, not a collage of established observations.

The independent review verified these derivations under the stated model. The inspected direct sources do not supply this particular selected-geometry/calibrated critical boundary. Targeted searches for critical scaling, calibration and monosemantic noise phases found no exact matching claim; search results were often irrelevant. This is evidence of a plausible specific addition, NOT proof of absence from all literature or sufficient main-track significance.

The arbitrary-load support-exposure bound is useful mathematical context and a falsifiable extension of our fixed-decoder model. Its proof is elementary and its effect depends on decoder restrictions; do not position it alone as the flagship novelty. A general learned decoder can output prior means without dropping encoder columns.

## Gates before asserting a strong paper contribution

1. Resolve finite toy predictions under the prespecified plan, including unfavorable results.
2. Establish that the critical/calibration phenomenon explains a measurable mechanism beyond two bits. The larger toy is a test, not a guarantee.
3. Demonstrate one meaningful real-representation consequence. A proof plus toys can be rigorous yet still too narrow for ICML.
4. In the paper, compare assumptions explicitly rather than claiming to subsume the different Elhage, Zhang and Scherlis models. The term 'superset' here means our broader organizing question, not a proved universal literature superset.
