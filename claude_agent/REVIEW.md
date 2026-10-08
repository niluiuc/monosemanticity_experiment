# Referee-style self-review of the claude_agent additions, with mitigations

Written in the spirit of the project's own reviewer records. The aim is to anticipate what an ICML referee would ask and record what has been done, or could be added, for each point. Nothing here removes earlier work.

## Likely objections, and the current answer

1. **"Two features in one dimension is too small."**
   - *Answer so far:* three features in one dimension (S7, with a real-data counterpart), and four features in two dimensions with closed-form shared-budget thresholds that trained networks confirm (S10).
   - *Still open:* general n/m.
   - *Suggested framing:* exact theory in the solvable cell, plus documented extension to n/m = 2. Avoid claiming general n/m.

2. **"The sign rule is nearly a tautology."** The bridge review already proved that near mono the improving direction has the sign of the covariance.
   - *Answer:* conceded for the local direction. What is *not* implied by that lemma:
     - that the **global** optimum follows the local sign (it can jump to the deep opposite branch: the first-order line c\* ∝ ε²);
     - the location of bistability at weak correlation (P2);
     - the positive/negative asymmetry of coexistence and packing.
   - *Action taken:* the significance of P2 and of the asymmetry is established under a channel-cluster bootstrap (`real_stats.py`). The paper should lead with P2 and the asymmetry, not the sign rule.

3. **"Several results are leading-order or numerical, not theorems."**
   - *Answer:* the status labels in `STATEMENTS.md` are explicit.
     - Proved: S1 (a local theorem with symbolic sign checks) and the bicritical identity.
     - S4 has a proof outline with an explicit first-order term.
     - S3 has precise numerics and a diagnosed slow convergence (the u = b1/σ variable).
   - *Still open:* global selection at c ≠ 0 and a rigorous S3.

4. **"Real-data evidence is from one network (ResNet18)."**
   - *Answer:* two representations (hidden channels and class logits) plus triples.
   - *Still open:* a language model or SAE features. The sandbox cannot download models, so this needs activations extracted on the user's machine. The pipeline (`real_pairs.py`, `real_triples.py`) only needs an (n_samples × n_features) nonnegative array.

5. **"Failed predictions."**
   - *Answer:* reported as registered. P3 (noise shrinkage) failed on layer 4 and held on logits; pooled displacement failed. The post-hoc explanations are labelled as such.

6. **"Quantitative transfer to real features is weak."**
   - *Answer:* the field transfers exactly (2ηCov, correlation 0.999999). The quadratic stiffness does not, because of a non-analytic small-θ structure. This is stated as a limitation, and the real-data claims are kept directional.

7. **"The noise model (isotropic Gaussian code noise) is narrow."**
   - *Answer:* this inherits the existing manuscript's choice. Results are stated for that model only. The adversarial literature is cited as a different threat model.

8. **"Novelty versus TMS's correlated-feature observations and Elimadi (2026)."**
   - *Answer:* positioning sentences are drafted in `manuscript_addendum.md`. The qualitative sign rule is credited to TMS-type observations. The new parts are:
     - the critical/field structure with exact coefficients;
     - the noise-induced first-order transition and spinodal;
     - the resource-convention thresholds;
     - the bicritical identity;
     - registered real tests.

## Suggested additions, ranked by value

1. Run `real_pairs.py` and `real_triples.py` on SAE features of a language model, extracted locally.
2. Prove S3, using the u = b1/σ diagnosis to control the remainder.
3. Global selection at c ≠ 0, via a branch-and-bound certificate with c as a parameter.
