# Exact-claim comparison and paper decision

Date: 6 October 2026. Scope: the five directly relevant primary sources named below, using the preserved source archive and the earlier broad novelty audit. This is a targeted assessment of the completed claim, not another general survey. No experiments, additional mathematical derivations, or new literature search were conducted for this assessment.

## Decision

**There is real mathematical progress, but the current two-feature result does not yet establish a distinct ICML main-track contribution.** We now prove properties of the geometry selected by a specified clean training objective, rather than merely comparing two supplied dictionaries. That is a meaningful improvement in rigor. However, clean sparsity/importance phases, exact two-feature loss analysis, and clean-performance/robustness tradeoffs already appear in the direct literature. Changing to binary amplitudes, enforcing equal energy, retaining free biases, and deriving a particular transition constant do not by themselves establish a new scientific mechanism.

I did not identify the exact globally optimized, norm-one, biased Bernoulli result or the certified two-crossing detector result in these five inspected sources. This supports a **specific analytic extension**, not a certificate of publication novelty. It does not justify claims that we first discovered a monosemanticity phase diagram or that the motivating ICLR paper is generally wrong.

The strongest existing anchor reported by the senior reviewer is the dense equal-importance example: globally clean-optimal shared geometry has lower **reconstruction MSE** on clean inputs, but higher **reconstruction MSE** under code noise than mono retention. This uses the same outcome before and after corruption and avoids the fixed binary-detector threshold issue. It remains a sharper controlled instance of an established qualitative tradeoff until we show what its trained-geometry theory predicts beyond the two-feature example.

## Precisely what has been completed

The main frequency result concerns independent binary features `b_i ~ Bernoulli(p)`, two concepts in one code dimension, `W = (u,v)` with `u²+v²=1`, and reconstruction

\[
\widehat b_i=\operatorname{ReLU}((W^\top Wb)_i+\beta_i).
\]

Biases are freely optimized on the clean population weighted reconstruction objective. With importance weights `(1,1/2)`, the global clean geometry becomes important-feature-only retention at

\[
p_c=(3-\sqrt5)/2.
\]

For `0<p<p_c`, an opposite-sign mixed geometry improves clean reconstruction over mono retention. This is an analytic global transition statement with all sign/order/bias branches covered; it is stronger than a grid minimum or a local stability calculation. Exact algebraic clean minima at `p=.2` and `p=.05` were separately certified by finite branch comparison.

For the globally selected `p=.05` code, latent Gaussian noise is added as `h=Wb+sigma*epsilon`. The fixed actual trained decoder declares feature presence only when its reconstructed value is **strictly greater than .5**. Relative to the equally resourced mono code, the importance-weighted detection-risk difference has the proved signs

\[
\Delta(0)=1/400>0,\qquad \Delta(.3)<0,\qquad
\lim_{\sigma\to\infty}\Delta(\sigma)=9/40>0.
\]

Continuity gives at least two positive crossings. It does not establish exactly two roots, nonmonotonic absolute model risk, or improved performance as noise increases. It establishes a nonmonotone **ordering between two specified decoders**.

The additional dense equal-importance result has a globally derived clean optimum with unequal amplitudes and clean loss

\[
L_{\rm shared}=\tfrac14-(3-2\sqrt2)/48<\tfrac14=L_{\rm mono}.
\]

The senior reviewer reports existing numerical corrupted-MSE values `.3186828187` versus `.3174638806` at `sigma=.3`, and `.512993809` versus `.5054497711` at `.6`. Those numbers are reported experiment evidence from the parallel review; this document does not independently certify them or convert them into a new theorem.

## Direct comparisons

### Elhage et al., Toy Models of Superposition (2022)

Primary sources: [research article](https://transformer-circuits.pub/2022/toy_model/index.html), [arXiv](https://arxiv.org/abs/2209.10652). Archived PDF: `sources/elhang2022/paper.pdf` (the archive key is misspelled). Locations below refer to PDF pages.

- **Pages 10–11, model definition:** tied linear encoder/decoder, free decoder biases, ReLU reconstruction, sparse continuous feature amplitudes and importance-weighted squared reconstruction loss. The basic model and the role of biases are established here. A different bias sign convention is immaterial.
- **Pages 14–15, “Superposition as a Phase Change”:** the article explicitly studies **two features in one hidden dimension**, varying sparsity and relative importance. It compares retaining feature 1, retaining feature 2, and an antipodal shared code; a linked analytical notebook provides closed-form loss comparisons. The published training plot already concerns geometry selected by clean reconstruction, not just noisy supplied codes.
- **Pages 29–30, adversarial robustness:** the article studies attacks exploiting interference and the capacity cost of adversarial training. The qualitative claim that a clean-trained shared representation can be more vulnerable is already present.
- **Website comments, “Replication & Further Results,” Tom McGrath:** this primary disclosure goes further than the three named codes. It reports exact expected loss for the two-feature ReLU model **without biases**, solving the full loss surface and observing continuously moving unequal-amplitude minima and same-direction feature confusion. It directly limits a claim to be first to solve clean two-feature geometry. The linked notebook itself was not separately inspected in this task, so no claim is made about every equation or its complete constraint set.

**Our increment:** global free-bias optimization under an explicitly equal energy constraint, binary states, a proved fixed-importance transition, and actual selected-code corrupted risk. These matter to the correctness of the comparison. They are a narrow strengthening of a pre-existing research question. Equal resource control is a useful control, not itself a new mechanism. It would be inaccurate to claim that prior work only ever supplied arbitrary dictionaries.

### Zhang et al., Beyond Interpretability: The Gains of Feature Monosemanticity on Model Robustness (ICLR 2025)

Primary sources: [arXiv](https://arxiv.org/abs/2410.21331), [conference PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/11822e84689e631615199db3b75cd0e4-Paper-Conference.pdf). The conference version is the 33-page archived source `sources/zhang_iclr2025/`.

- **Page 9, Section 4.2 and Figure 5:** a clean-reconstruction-trained toy with 40 features and 20 code dimensions is followed by a downstream classifier. The polysemantic representation improves clean accuracy but loses to the monosemantic comparator under input noise and label noise. Thus clean-selected representation plus corrupted-performance reversal already has an empirical example in the starting paper.
- **Pages 9–10, Section 4.3:** the two-feature theory assumes `nu_mono=x1` and `nu_poly=x1-x2`, continuous spike-and-uniform features, and a classification task based on `argmax_i x_i`. Its theoretical outcome is a conditional-moment separability quantity, not the exact binary-presence detection error used here.
- **Pages 24–25, Appendix B.3, Theorems B.7–B.9, Eqs. (49)–(53):** input Gaussian noise increases the variances of the mono and poly scores differently; the normalized separation ordering can reverse. This is already an analytic noisy tradeoff for specified representations.
- **Pages 25–28, Appendix B.4:** the authors extend the supplied polysemantic combination to unequal positive weights. That is not a global clean objective optimization with norm-one resources and free decoder biases.

**Our increment:** a proved link from a specified global clean optimizer to its corrupted performance, rather than assuming the two theoretical combinations; exact operational risk rather than a moment surrogate; and a matched energy budget. Our code-noise, detection task, binary amplitudes and resource constraints differ materially. Consequently a two-crossing result for our decoder does not contradict their one-crossing separability analysis. Their larger trained toy already establishes the broad phenomenon, so our exactness must explain a nonroutine additional mechanism or predictive boundary to carry a paper.

### Scherlis et al., Polysemanticity and Capacity in Neural Networks (2022; archived updated version)

Primary source: [arXiv](https://arxiv.org/abs/2210.01892), archive `sources/scherlis2022/`, 23 pages.

- **Page 5, Eq. (3):** feature capacity is `(w_i^T w_i)^2 / sum_j (w_i^T w_j)^2`, exactly the square of the previously proposed alignment quantity `M_i`. Renaming it is not novelty.
- **Page 7, Section 3.1, Eqs. (9)–(12):** a different solvable model predicts a quadratic target using quadratic neurons and centered feature inputs. The expected loss separates norm allocation and overlap terms, with feature importance and fourth moments controlling the objective.
- **Pages 8–9, Sections 3.4–3.5, Eqs. (15)–(18):** analytic optimal capacity allocations include ignored, partially represented and fully represented features, with importance/kurtosis phase boundaries. Appendix C establishes feasibility of the proposed allocation.

**Our increment:** tied-ReLU reconstruction with learned biases, fixed encoder energy and subsequent corrupted risk is a different model. The paper does not supply our Bernoulli `p_c` theorem. Nevertheless, optimal importance-dependent capacity phases are already a mathematical contribution in the literature; we cannot sell their general existence as our discovery. A specific exact constant at importance ratio two is a result within that established program.

### Gorton and Lewis, Adversarial Examples Are Not Bugs, They Are Superposition (2025)

Primary source: [arXiv](https://arxiv.org/abs/2508.17456), archive `sources/gorton2025/`, 14 pages.

- **Pages 3–4, Section 3.1:** clean and adversarial training of a tied-ReLU reconstruction toy, uniform importance, source-distribution sparsity, learned biases, and input-space L2 attacks maximizing reconstruction error.
- **Pages 4–5, Section 3.2 and Figure 2:** the authors observe a vulnerability dip associated with antipodal superposition. Geometry structure changes robustness even when a coarse amount-of-superposition proxy does not capture the difference.
- **Page 9, discussion of unexpected findings:** temporary robustness improvement near antipodal configurations and different vulnerabilities at similar superposition amounts are explicitly identified as needing further explanation.

**Our increment:** exact global clean allocation and latent Gaussian risk are not their adversarial input-risk experiment. Our calculations could support an analytic explanation of how learned geometry and resource allocation alter robustness, but the first observation of a nonmonotone geometry/robustness relationship is not ours. Their code has learned biases already; recognizing bias suppression itself is also not new. A connection to their phenomenon must be derived or tested, not inferred merely from the word “antipodal.”

### Elimadi et al., Why Does Robustness Reduce Superposition? (2026)

Primary source: [arXiv](https://arxiv.org/abs/2608.22155), archive `sources/elimadi2026/`, 9 pages. The source identifies itself as accepted at the COLM 2026 Workshop on AI Interpretability.

- **Section 3.6, Eq. (8), PDF page 3:** combined clean/adversarial reconstruction objective.
- **Section 3.7 and results in Section 4:** robustness training, feature retention and interference are studied across chosen sparsities.
- **Section 5:** a controlled robust/non-robust feature partition uses different amplitudes; adversarial training preferentially abandons designated non-robust features. The explanation is conceptual rather than a global clean geometry theorem.

**Our increment:** this paper does not give the globally optimized Bernoulli clean transition or Gaussian selected-decoder risk. It does already support the feature-retention explanation of reduced superposition. We cannot claim that robustness reducing superposition by dropping features is a new observation.

## Component-level novelty assessment

| Component | Status after direct comparison |
|---|---|
| Clean sparsity/importance-dependent superposition phase | Established by Elhage and by analytic capacity models; our exact constraint-specific theorem is an extension |
| Full two-feature clean loss surface | Already disclosed by McGrath for the bias-free model; our free-bias global proof is stronger within its specified setup |
| Finite ReLU active-interval bias profiling | Correct and useful exact optimization technique; no independent methodological novelty established |
| Global `p_c=(3-sqrt(5))/2` at importance ratio two | No exact matching theorem identified in the inspected sources; narrow new analytic result, publication significance still unestablished |
| Clean globally selected code versus equally resourced mono | The exact global proof/resource controls improve rigor; larger clean-trained noisy reversal already present in Zhang |
| At least two Gaussian detection-risk crossings | No matching exact result identified here; interpretation depends on fixed trained readout and prevalence |
| Same-MSE noisy reversal for dense global clean optimum | Cleaner evidence of the intended capacity/robustness tradeoff; qualitative tradeoff already known, general explanatory contribution not established by one example |
| A robustness boundary predicted from clean-selected geometry across meaningful resources | Still the potential paper-level contribution; not solved by writing the exact two-feature formulas |

## Paper-critical interpretation: geometry versus readout calibration

The two-crossing result is valid for the actual specified decoder. It is not a comparison of optimal noisy detectors. For rare isolated features, a midpoint threshold is not Gaussian-noise Bayes optimal. The existing research notes already derive, for `h=ab+epsilon` with noise variance `sigma²`,

\[
\theta_{\rm Bayes}=a/2+(\sigma^2/a)\log((1-p)/p).
\]

This is not a new derivation made during this review. See `output/overleaf/monosemanticity_notes/main.tex`, subsection “Rarity also affects the best decision threshold.” The source notes explicitly warn that threshold optimization is an important ablation.

For `p=.05`, the mono detector with threshold `.5` is therefore not optimal under noisy rare-feature detection. The globally selected shared code has different trained biases and different effective thresholds. An intermediate-noise advantage can consequently reflect **clean-objective readout calibration as well as representational interference**. Current evidence has not separated those causes. It would be an overclaim to label the certified ordering a universal geometry-dependent robustness boundary or to say superposition itself beats monosemanticity even with equally capable noisy readouts.

The dense same-MSE reversal avoids this specific binary-threshold problem and is therefore the stronger current foundation. Re-optimizing reconstruction biases under corruption remains a separate meaningful control: the existing result evaluates the clean-trained model, which is scientifically legitimate, but it is not an optimum over noise-adapted decoders. Calibration should be treated symmetrically, and a change in the operational question should be explicitly named.

## Consequence for the paper decision

1. **Keep the direction.** Monosemanticity, superposition, clean allocation and corrupted risk remain the subject. The global clean-selection proof is legitimate mathematical progress and useful infrastructure.
2. **Do not present the two-feature theorem as a completed main-track paper.** Neither acceptance nor spotlight strength follows from an exact transition or certified counterexample. The direct literature is too close for that claim.
3. **Use the same-MSE clean-selected/noisy reversal as the primary existing anchor.** Retain the detector two-crossing result as a carefully labeled operational result rather than the sole geometry mechanism.
4. **Resolve one central blocker before widening scope:** does the corrupted ordering survive symmetric readout/bias calibration, or is its main cause clean-training calibration? This is a bounded falsification check on an already completed case, not a new survey or exploratory sweep. The reviewer is arranging that check separately; no new run is proposed or executed here.
5. **The paper-worthy advance must explain a predictive boundary or mechanism beyond the example:** how the geometry actually selected by clean training changes the useful capacity/robustness tradeoff, which controls matter, and whether the derived mechanism predicts a controlled larger toy and a real representation. The current proofs are the smallest exact anchor for that contribution, not a substitute for it.

If calibration removes an apparent shared-code advantage, report it directly and drop the stronger representational interpretation. That would not invalidate the global clean theorem or require abandoning the original research direction. It would identify the controlling quantity the robustness boundary must include. Conversely, a persistent same-outcome reversal with matched calibration would make the geometry contribution substantially more defensible, while still requiring evidence of scope and explanatory value.

## Evidence limits and provenance

The earlier broad survey archived 39 PDFs representing 38 works, with heterogeneous reading depth. Its search breadth and limits are documented in `project1_toy/literature_review/novelty_audit.md`; its source versions and hashes are in `source_index.md`. This targeted review re-examined the five direct sources and Elhage's preserved web comments, not every archived paper afresh. No claim is made that all existing literature or all private/unindexed work has been checked. The McGrath linked notebook was not separately inspected. This report distinguishes absence of an exact match from evidence of a substantial new contribution.

Our proof provenance is `focused_bridge_2026-10-06/math/student_derivation.md`, `low_p_certificate.md`, `frequency_boundary_2026-10-06/math/derivation.md`, and the corresponding independent teacher reviews and rational noise certificate. The additional dense corrupted-MSE numbers were communicated by the senior reviewer during this assessment. Plan files and archived experiment outputs were not modified.
