# Project 1: literature survey and novelty audit

Audit cutoff: **5 October 2026, America/Chicago**. Sources were retrieved on 5 October local time / 6 October UTC. This audit does not include Project 2's recursive-training contribution.

## Verdict

**Substantial parts of Project 1 have already been studied, and several of our current mathematical quantities are established results under different names. The present calculations and first toy experiment do not yet establish a sufficiently distinct central contribution for an ICML main-track paper.**

However, this review did **not identify a paper solving the whole proposed boundary for a clean-trained, nonlinear compressed representation under matched resources, as activation frequency, feature load, importance distribution and a specified corruption vary**. That stronger result is also not established by our project yet. Its status is **potentially open, not verified novel**.

The appropriate conclusion is neither “the entire project is already done” nor “the project is novel because no paper has exactly our setup.” The broad phenomenon is established; some formulas are equivalent to existing quantities; some calculations are routine specializations; a more demanding result remains a possible contribution. Publication strength would depend on actually obtaining that result and demonstrating what it explains beyond prior work.

This is a judgment of novelty, not a rejection of the research direction. The monosemanticity → superposition geometry → robustness direction remains scientifically coherent. The existing derivations and code are useful foundations and verification tools. They should not be represented as a completed novel paper.

## What was compared

The full research question is:

> When does representing more concepts in fewer dimensions improve useful performance, and when does the resulting interference cost more under corruption than a capacity-controlled monosemantic representation? Can we derive a boundary from activation sparsity, feature-to-dimension load and importance, predict it in trained toy models, and test it in a small real model?

The implemented experiment is narrower:

- Independent Bernoulli concepts, eight features and four code dimensions.
- A tied ReLU autoencoder trained on clean population reconstruction error.
- A fixed total encoder-energy budget, with uniform feature importance.
- Test-time additive isotropic Gaussian noise in **code space**.
- Two specified detection rules: a centered matched detector and the actual trained decoder threshold.
- A restricted orthogonal four-feature monosemantic comparator.
- Separate exact comparisons of two specified two-feature codes and their specified thresholds.

The general load/importance boundary has not been established by that experiment. A crossing between two supplied codes is not a proof about globally optimal learned representations. A fixed eight-to-four experiment does not establish a boundary across feature loads. Uniform importance does not test an importance-decay law.

## Search breadth and evidence limits

The search covered primary literature in neural superposition and monosemanticity, robustness and representation stability, capacity allocation and neural scaling, sparse coding and compressed sensing, frame geometry, overloaded multiuser detection, hyperdimensional codes and relevant neural population coding. It included recent preprints, older mathematical literature, and references from a September 2026 survey rather than only papers sharing our terminology.

The archive contains **39 PDF documents representing 38 distinct works**, including both the original and conference versions of the starting paper. Additional primary web disclosures and publisher previews were screened. Full-text availability is not the same as reading every page: the evidence matrix below states which sections, equations or experiments were inspected. Some background works were screened only at their abstract/introduction level. The Nature Machine Intelligence article was available only as a publisher preview. A failed ELUDe publisher download was subsequently resolved through its arXiv version.

The search does not certify that every existing publication, unindexed manuscript or private project was checked. It supplies a broad, inspectable audit with concrete mathematical comparisons. Absence of an exact match is evidence to investigate a gap, not proof of novelty. All judgments below concern material publicly available by the cutoff.

Primary PDFs, extracted page-numbered text, retrieval URLs, available arXiv histories and hashes are preserved in `sources/`. See `source_index.md` and `search_ledger.md` for provenance and coverage. No new model experiments were run for this audit. **`project1_toy/plan.md` was not edited.**

## Claim-by-claim assessment

| Proposed contribution | Evidence from prior work | Assessment |
|---|---|---|
| Sparse features can share dimensions; interference creates a capacity/error tradeoff | Elhage et al. 2022 and Scherlis et al. 2022 | Established starting point, not a new finding |
| Greater monosemanticity can improve robustness | Zhang et al., ICLR 2025 | The motivating result already exists; its scope depends on task and corruption |
| Superposition can give better clean performance but worse corrupted performance | Zhang et al.'s two-feature Gaussian-noise analysis; other superposition/robustness studies | The qualitative finding is already covered |
| Feature overlap predicts adversarial vulnerability | Elhage et al.; Gorton and Lewis; Stevinson et al.; sparse-coding stability literature | Established in multiple mathematical and empirical settings |
| The quantity `M_i = G_ii / sqrt(sum_j G_ij^2)` | Scherlis et al. Eq. (3); Elhage et al.'s feature dimensionality | Its square is an existing capacity/dimensionality quantity |
| A width/load lower bound on total squared overlap | Classical tight-frame/frame-potential theory | Standard linear algebra/frame geometry |
| A sparsity/load/noise sufficient region for matched recovery | Ben-Haim et al.; Thomas et al.; Vompa 2026 | Already studied, including neural-feature terminology; our bound needs a nonroutine distinction |
| Exact Gaussian error by conditioning on finitely many binary feature states | Standard threshold detection; nearby sparse-code and multiuser-detection settings | Useful exact specialization, not by itself a strong new theorem |
| An exact noisy crossing between two particular antipodal/monosemantic codes under equal energy | No literal identical formula identified in inspected sources | Setup-specific calculation; scientific novelty not established merely by the formula's absence |
| Importance-dependent allocation between ignored, monosemantic and polysemantic features | Scherlis et al.'s analytic capacity phases; Liu et al.'s scaling theory | Already developed in other models; our nonlinear corrupted-risk boundary is a stronger, different target |
| Predict the robustness boundary of the geometry selected by training across load, frequency and importance | No complete match identified under all our assumptions | Potential contribution; neither solved here nor certified novel by this audit |
| Toy models followed by a real neural model | Several direct papers already use this structure | Validation strategy, not a novelty claim |

### 1. The proposed alignment metric has an exact predecessor

For a stored feature, let `G = W^T W`. Our quantity is

\[
M_i=\frac{G_{ii}}{\sqrt{\sum_jG_{ij}^2}}.
\]

The capacity in [Scherlis et al., *Polysemanticity and Capacity in Neural Networks*](https://arxiv.org/abs/2210.01892), Eq. (3), is

\[
C_i=\frac{(w_i^\top w_i)^2}{\sum_j(w_i^\top w_j)^2}=M_i^2.
\]

This is an algebraic identity, not merely a similar intuition. Elhage et al.'s feature-dimensionality measure is also equivalent. We can use this quantity and derive new consequences, but we cannot claim to introduce it. For a dropped feature, our ratio is undefined; assigning a zero capacity is a convention, not a proof of a robustness radius.

An operational perturbation radius still needs a sample, decision threshold and perturbation location. The noise sensitivity of a code-space detector is not determined by this ratio alone. Establishing a new relationship involving an existing metric could be a contribution; renaming that metric is not.

### 2. The main qualitative tradeoff is already present in the starting paper

[Zhang et al., *Beyond Interpretability*](https://arxiv.org/abs/2410.21331) includes both a noisy toy experiment and a two-feature analysis. Its theory compares retaining one feature with combining two features, showing a clean-data advantage that can disappear under Gaussian corruption. The [conference version](https://proceedings.iclr.cc/paper_files/paper/2025/file/11822e84689e631615199db3b75cd0e4-Paper-Conference.pdf), Appendix B.3, explicitly tracks the greater noise variance of the polysemantic combination.

Our binary concepts, code-space noise, error metric and equal-energy control differ. Those are material for a correct comparison. They do not make “superposition helps clean performance but can hurt noisy performance” a new discovery. A wider predictive law, with justified resource controls and a proven relationship to trained geometry, would go beyond this example.

### 3. General sparsity/interference/noise bounds have substantial prior coverage

Three particularly relevant precedents are:

- [Ben-Haim, Eldar and Elad, 2009/2010](https://arxiv.org/abs/0903.4579): threshold recovery guarantees involving dictionary coherence, sparsity, feature amplitudes and Gaussian noise.
- [Thomas, Dasgupta and Rosing, 2020/2021](https://arxiv.org/abs/2010.07426), Theorem 10 and Lemma 11: sum encoded feature vectors, recover membership by inner-product thresholding, and bound both white Gaussian corruption and bounded adversarial corruption through coherence, set size and code length.
- [Vompa, September 2026](https://arxiv.org/abs/2609.09556), Theorem 1 and Corollary 1: high-probability linear accessibility with random spherical feature directions, fixed sparse support, bounded coefficients and observation noise.

Our centered Bernstein bound retains a variance term and a largest-overlap term, which can be preferable to a worst-coherence bound for some dictionaries. But using these concentration tools is not automatically a new contribution. It would require a demonstrable improvement, a substantially different applicable theorem, or a new connection to learned geometry and the actual performance crossing.

The distinction is particularly important for the latest preprint: it analyzes supplied random directions, not directions selected by our clean-trained nonlinear autoencoder. That leaves a possible gap, but it rules out presenting generic “sparsity + width + noise imply a recoverability boundary” as unexplored.

### 4. The proposed load bound is classical

For unit feature directions `u_i` in `m` dimensions, the frame potential obeys

\[
\sum_{i,j}(u_i^\top u_j)^2\geq \frac{n^2}{m},\qquad
\frac1n\sum_{i\ne j}(u_i^\top u_j)^2\geq\frac nm-1.
\]

This follows from the rank and trace of the frame operator, with equality for an appropriate unit-norm tight frame. See [Ambrus's proof and its references to the classical frame-potential results](https://arxiv.org/abs/1403.7382). The inequality constrains interference, but it does not characterize which geometry training selects or establish an equality contour for corrupted risk. It is background mathematics to cite, not our new theorem.

### 5. There is a close communication-theory interpretation of our detector

With Bernoulli concepts and additive code noise, our centered detector has the statistic

\[
w_i^\top[W(b-p)+\sigma\epsilon]
=G_{ii}(b_i-p_i)+\sum_{j\ne i}G_{ij}(b_j-p_j)
 +\sigma w_i^\top\epsilon.
\]

This is a matched-filter signal, cross-talk and Gaussian-noise decomposition. Overloaded multiuser detection studies such quantities with activity, power allocation and finite dimensional codes. [Viswanath, Anantharam and Tse, 1999](https://people.eecs.berkeley.edu/~ananth/1999-2001/Pramod/OptimalSeqsIT99.pdf) derives an optimized load/admissibility condition for linear-MMSE CDMA receivers.

Their receiver, objective and power constraints differ from ours; their theorem is not our theorem. The relevance is that replacing “users/signatures” with “concepts/feature directions” does not make the underlying interference calculation new. Our finite-state Gaussian risk is a useful exact evaluation tool. A contribution would need to explain a property of learned representations that this older detection framework does not already supply.

### 6. A supplied geometry and a learned geometry are different theorem targets

Our current conditional-risk formula answers: **given `W`, what error does this detector make?** The intended stronger result answers: **as frequency, load and importance change, what geometry does the training objective select, and where does its corrupted risk cross the fair comparator?**

Scherlis et al. already solve important capacity-allocation questions analytically in a different quadratic model. Gorton and Lewis already observe robustness differences between geometries at similar superposition levels. Consequently, neither “training geometry matters” nor “geometry can matter beyond a scalar amount of superposition” is by itself new. A predictive result for a clearly defined learned nonlinear family, with appropriate proof and tests, could still be distinct.

The expression `p n/m <= 1/tau^2 - 1` is not an established universal boundary for our task. Multiplying a static Gram overlap by activation probability changes the quantity being modeled; a bound on average activation interference is not automatically a worst-case margin law. It cannot serve as a novel theorem without a correctly specified model and proof.

## Wider evidence matrix

Reading-depth labels: **T** = relevant full-text methods/theorems/experiments inspected; **S** = abstract/introduction or selected contextual passages screened, with full text archived; **P** = primary preview or abstract only. These labels do not claim a cover-to-cover reading. Dates are original public dates unless a later relevant version is noted.

### Neural superposition, monosemanticity, geometry and robustness

| Primary source | Inspected evidence / depth | Relation to Project 1 and material difference |
|---|---|---|
| [Elhage et al. (2022), Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html) | T: toy setup, sparsity/importance phases, feature dimensionality, adversarial section | Same basic tied-ReLU substrate; capacity/interference and attacks already studied. Does not solve our complete fixed-energy noisy learned boundary. |
| [Scherlis et al. (2022; version through March 2025), Polysemanticity and Capacity](https://arxiv.org/abs/2210.01892) | T: Eq. 3, Sections 3.3–3.6, capacity allocation and phase diagrams | Exact equivalent of `M_i^2`; analytic importance/sparsity allocation. Quadratic computation model rather than our corrupted Bernoulli ReLU reconstruction task. |
| [Jermyn et al. (2022), Engineering Monosemanticity](https://arxiv.org/abs/2211.09169) | S: architecture/intervention setup | Monosemanticity can be changed in toy models. Not our corrupted-risk boundary. |
| [Lecomte et al. (2023), What Causes Polysemanticity?](https://arxiv.org/abs/2312.03096) | T: mechanisms involving noise and regularization | Polysemanticity need not mean exhausted representational capacity; definitions and causal controls matter. Different origin question. |
| [Marshall and Kirchner (2024), Coding Theory](https://arxiv.org/abs/2401.17975) | T: noise/dropout and redundancy discussion | Distributed redundant codes can tolerate corruption. Different coding and dropout model; prevents a universal “polysemanticity is bad for noise” framing. |
| [Hänni et al. (2024), Mathematical Models of Computation in Superposition](https://arxiv.org/abs/2408.05451) | T: superposition construction and interference bounds | Sparse computation, concentration and correction already have mathematical treatments. Not our exact risk crossing. |
| [Zhang et al. (2024 / ICLR 2025), Beyond Interpretability](https://arxiv.org/abs/2410.21331) | T: original and conference versions, experiments and Appendix B | Main motivation; clean/noisy two-feature comparison already exists. Different noise location, amplitudes and resource controls. |
| [Liu, Liu and Gore (2025), Superposition Yields Robust Neural Scaling](https://arxiv.org/abs/2505.10465) | T: strong/weak superposition, width scaling, importance distribution | Closely relevant geometry/load/importance theory. “Robust” refers to stability of scaling laws across frequency distributions, not attack or Gaussian-noise robustness. |
| [Gong et al. (2025; March 2026 version), Signal in the Noise](https://arxiv.org/abs/2505.11611) | T: interference measures and intervention/transfer experiments | Feature interference predicts cross-model effects. “Noise” does not denote our Gaussian corruption; no same phase theorem. |
| [Gorton and Lewis (2025), Adversarial Examples Are Not Bugs, They Are Superposition](https://arxiv.org/abs/2508.17456) | T: toy sparsity sweeps, attack construction, antipodal regime, ResNet/SAE experiment | Strong direct competition: toy plus real-model superposition/robustness link, and geometry-specific effects. No complete analytic boundary across our controls. |
| [Pertl et al. (2025; January 2026 version), Superposition in GNNs](https://arxiv.org/abs/2509.00928) | T: fixed-energy random/axis code noise comparison and pooling experiment | Relevant monosemantic/distributed noise comparison. Max-pooling corruption breaks rotational symmetry; it is not our additive isotropic code-noise detector. |
| [Stevinson et al. (2025; June 2026 version)](https://arxiv.org/abs/2510.11709) | T: Proposition 1, Corollary 1, toy correlations and ViT bottlenecks | Exact attack/interference directions and learned toy/real tests already exist. Different classification objective and threat model. |
| [Bereska et al. (2025), Superposition as Lossy Compression](https://arxiv.org/abs/2512.13568) | T: entropy measure, attack tests and abundance/scarcity regimes | Superposition and robustness can increase together; task capacity matters. Empirical/compression framework rather than our exact nonlinear trained-risk law. |
| [Garg and Peng (2026), How Many Features Can a Language Model Store?](https://arxiv.org/abs/2602.11246) | T: linear accessibility definition, upper/lower bounds, activation extension | Nearly matching width/sparsity bounds for uniformly accessible sparse representations. No same learned noisy reconstruction comparison. |
| [Prieto et al. (2026), From Data Statistics to Feature Geometry](https://arxiv.org/abs/2603.09972) | T: binary-concept setup and learned correlation geometry | Coactivation structure affects geometry and can make sharing constructive. Different focus; our independent-feature assumptions must be explicit. |
| [Mencattini et al. (2026), Rate-Distortion-Polysemanticity Tradeoff](https://arxiv.org/abs/2605.14694) | T: formal tradeoff and controlled construction | Analytic cost of monosemanticity is already a research topic. SAE distortion/information objectives differ from our noisy feature detection. |
| [Bağcı et al. (2026), Interpretability Without Tradeoffs](https://arxiv.org/abs/2605.31304) | S: abstract and introduction, functional-equivalence claim | Disentangles units while preserving model outputs. Measured neuron monosemanticity need not change predictive behavior; differs from limited-resource feature storage. |
| [Lu et al. (2026), Adversarial Concept Search](https://arxiv.org/abs/2606.13934) | T: geometry/error prediction and compositional experiments | Geometry-based prediction of model failures already studied. Compositional/task errors rather than our Gaussian code-noise threshold risk. |
| [Elimadi (2026), Why Does Robustness Reduce Superposition?](https://arxiv.org/abs/2608.22155) | T: toy setup and robust-training explanation | Direct empirical/thematic overlap; feature dropping explains reduced superposition. Does not provide our full boundary; notation inconsistencies mean its Gram claims should not be adopted without checking. |
| [Vompa (September 2026), High-Probability Linear Accessibility](https://arxiv.org/abs/2609.09556) | T: Lemmas 1–2, Theorem 1, Corollary 1, assumptions | Direct recent theory competition on sparse interference, width, noise and thresholds. Random supplied directions and fixed support, rather than our clean-trained nonlinear geometry. |
| [Shi et al. (September 2026), Feature Superposition: Theory to Practice](https://arxiv.org/abs/2609.06862) | T: geometry, capacity, robustness sections and reference tracing | Broad discovery/check source, not independent proof of novelty. Selected sections of this 96-page survey were inspected, not every cited paper. |
| [A unifying framework from neural superposition to sparse interpretable codes (2026)](https://www.nature.com/articles/s42256-026-01259-z) | P: publisher abstract, preview and references | Related broad framework. Full article was inaccessible here; cannot be ruled out as an exact competitor from its abstract alone. |

### Sparse recovery, coding and frame geometry

| Primary source | Inspected evidence / depth | Relation and difference |
|---|---|---|
| [Viswanath, Anantharam and Tse (1999), Optimal CDMA Sequences](https://people.eecs.berkeley.edu/~ananth/1999-2001/Pramod/OptimalSeqsIT99.pdf) | T: signal/interference model, admissibility and optimized sequence/power results | Load, code overlap, noise and optimized linear detection long predate neural-superposition terminology. Linear-MMSE/SIR objective differs from our ReLU training and binary risk. |
| [Candès, Romberg and Tao (2005/2006), Stable Signal Recovery](https://arxiv.org/abs/math/0503066) | T: measurement/noise assumptions and stable recovery statement | Sparse noisy recovery established through RIP and nonlinear decoding. Different recovery algorithm and no learned mono comparator. |
| [Donoho, Elad and Temlyakov (2006), Stable Sparse Overcomplete Recovery](https://elad.cs.technion.ac.il/wp-content/uploads/2018/02/23_Stability_IEEE_TIT.pdf) | T: sparse/coherence stability statements | Strong historical interference/noise precedent. Bounded-noise sparse optimization rather than our thresholded noisy code. |
| [Wainwright (2007), Noisy Sparsity Recovery Limits](https://arxiv.org/abs/math/0702301) | T: information-theoretic recovery setting and sufficient/necessary regimes | Noise/sparsity/width limits already studied; support success and optimal decoding differ from mean feature error. |
| [Fletcher, Rangan and Goyal (2008), Sparsity Pattern Recovery](https://arxiv.org/abs/0804.1839) | T: random model, SNR/amplitude effects, maximum-correlation recovery | Direct matched-recovery phase/scaling precedent. Full support recovery and random measurements, not our trained representation. |
| [Ben-Haim, Eldar and Elad (2009), Coherence-Based Random-Noise Guarantees](https://arxiv.org/abs/0903.4579) | T: thresholding Theorem 4 and Gaussian assumptions | Sparse interference plus feature amplitude plus noise guarantee already exists. Different fixed dictionary/support setting. |
| [Ambrus (2014), Tight Frames](https://arxiv.org/abs/1403.7382) | T: frame-potential characterization | The rank/energy overlap bound is standard; new training consequences would need separate proof. |
| [Barbier and Krzakala (2014), Superposition Codes](https://arxiv.org/abs/1403.8024) | T: Gaussian channel and decoding thresholds | Phase thresholds for superposed codes already studied. Block-one-hot messages and AMP, not independent concepts and our decoder. |
| [Papyan, Romano and Elad (2016), CNNs via Sparse Coding](https://arxiv.org/abs/1607.08194) | T: thresholding/CNN connection and stability assumptions | Already connects neural computation to sparse interference/recovery. Different multilayer convolutional model. |
| [Romano et al. (2018/2019), Adversarial Noise Attacks](https://arxiv.org/abs/1805.11596) | T: Theorems 7, 12–13, fixed-dictionary limitation | Classifier margin, coherence and sparsity yield neural robustness theorems plus real-data tests. Explicitly does not analyze learning. |
| [Thomas, Dasgupta and Rosing (2020/2021), Hyperdimensional Computing](https://arxiv.org/abs/2010.07426) | T: Theorems 2, 7, 10 and Lemma 11 | Very close sum-of-feature-vectors plus threshold model; handles Gaussian and adversarial corruption. Designed/random codes rather than trained nonlinear allocation. |
| [Sulam, Muthukumar and Arora (2020), Supervised Sparse Coding Robustness](https://arxiv.org/abs/2010.12088) | T: Theorems 4.1/5.1, encoder gap, margin and stability | Learned representation + theory + real certified robustness already exists. Lasso encoder, encoder-gap/RIP assumptions and adversarial risk differ from our setting. |
| [Orhan and Ma (2015), Neural Population Coding of Multiple Stimuli](https://pubmed.ncbi.nlm.nih.gov/25740513/) | P: primary abstract and publisher excerpts | Mixed stimulus coding and decoding precision under noise are older questions. Different population tuning model; full article not inspected. |

### General robustness and primary informal disclosures

| Primary source | Inspected evidence / depth | Relation and difference |
|---|---|---|
| [Tsipras et al. (2018/2019), Robustness May Be at Odds with Accuracy](https://arxiv.org/abs/1805.12152) | S: setup and central tradeoff | General clean/robust tradeoff is known; not the feature-packing theorem. |
| [Schmidt et al. (2018), Robust Generalization Requires More Data](https://arxiv.org/abs/1804.11285) | S: model and sample-complexity claim | A separate data-size confound for robustness, not our interference law. |
| [Ilyas et al. (2019), Adversarial Examples Are Features](https://arxiv.org/abs/1905.02175) | S: robust/nonrobust feature distinction | Predictive features and robust features need not coincide. Not a monosemanticity equivalence. |
| [Zhang et al. (2019), TRADES](https://arxiv.org/abs/1901.08573) | S: clean/robust objective and decomposition | General accuracy/robustness tradeoff machinery; no same capacity geometry result. |
| [Etmann et al. (2019), Robustness and Saliency Interpretability](https://arxiv.org/abs/1905.04172) | S: geometric margin connection | Interpretability/robustness and gradient alignment are older themes, not new solely by association. |
| [Vaintrob (January 2026), Denoising and Superposition](https://www.lesswrong.com/posts/siu22scEfuKxpSgfK/a-tale-of-three-theories-sparsity-frustration-and) | T: author's binary denoising model and code disclosure | Gaussian-corrupted bottleneck experiments already disclosed. Different untied/nonlinear architecture and frustration question; informal evidence, not a verified peer-reviewed theorem. |
| [SONI (2026), Selective Orthogonalisation via Noise Injection](https://www.lesswrong.com/posts/ihbn9wwdYP9pKT3ds/soni-selective-orthogonalisation-via-noise-injection) | T: stated intervention, toy setup and limitations | Latent noise as a tool to change superposition already proposed. Its downstream robustness and proof claims were not independently validated by this audit. |

## What the present experiment establishes, and what it does not

The saved run is valuable because it tests exact predictions without adjusting the outcomes to fit a desired narrative. In this restricted setting, representations that do better on clean reconstruction can lose under stronger Gaussian corruption. Decoder choice can change the ranking. These are sound reasons to specify resources, threshold and task explicitly.

They are not yet new general laws. Related phenomena appear in the literature above. The current bound was often loose, some runs did not meet the fixed convergence diagnostic, and neither global optimality nor a load/importance sweep was established. Those limitations matter when deciding whether an observed crossing is a training-selected phase boundary.

Likewise, a real-model demonstration would test transfer, but adding a diffusion model would not by itself make an established toy theorem novel. Conversely, a strong new theoretical result can be valuable even before a broad application campaign. Novelty and empirical scope must be assessed separately.

## The contribution still worth testing within the existing direction

A defensible target remains:

> A predictive result for the robustness boundary of the representation selected by a specified nonlinear training objective, with fixed resources and specified concept frequencies/importances, distinguishing which capacity-saving geometries help and which hurt under a defined corruption.

This is a tightening of the original Project 1 question, not a new project. To count as an advance, the result must add something nonroutine to the closest theory: for example, a solved learned-geometry family, matching bounds that locate an actual crossing, or a demonstrably new prediction about trained geometry that existing capacity/coherence bounds do not supply. Merely calculating risk after measuring `W` is weaker.

The theorem must distinguish:

1. Two supplied code families from optimized representation classes.
2. Clean-training-selected geometry from robustness-optimized geometry.
3. A sufficient low-error region from a boundary where one family outperforms another.
4. Average Gaussian corruption from a worst-case perturbation guarantee.
5. Fixed total energy, fixed per-feature amplitude and fixed model width.

Under the time constraint, the review supports a narrowly defined, nonroutine claim in the current direction. It does not support adding uncontrolled model families or starting a large exploratory sweep to compensate for an unclear contribution. This audit does not modify the experiment plan or authorize a pivot.

## Confidence of the conclusions

- **High:** `M_i^2` has an exact predecessor; the basic superposition/noise tradeoff is established; standard overlap and concentration bounds have substantial prior coverage.
- **High:** several papers already combine superposition/robustness theory or controlled experiments with real neural models.
- **Moderate:** the current pair calculation and experiment, on their own, are insufficiently distinct for a strong main-track novelty claim. This is a research judgment, not an acceptance prediction.
- **Uncertain:** whether the full nonlinear learned boundary can be solved within eight weeks, and whether a narrowly specified new result survives additional exact-theorem comparison once derived.
- **Not established:** that this project is a guaranteed conference paper, that an exact absence of prior work has been proved, or that every paper using different notation has been ruled out.

The honest current status is therefore: **a viable research direction with significant prior coverage and an unfinished novelty-bearing theorem, rather than a completed novel Project 1 paper.**
