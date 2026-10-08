# Literature Scout: Novelty Check for Claims (a)-(d)

Date: 2026-10-07. Scope: web search (about 30 queries, standard plus extended modes) and targeted arXiv abstract fetches. Limits: several arXiv full-text fetches timed out, so some judgments below rest on abstracts and search-engine excerpts, not full papers. The "Hidden not Deleted" abstract and the Guo/Liu/Gore and Shi et al. abstracts were read in full. Nothing in this search proves absence; the confidence levels say how far each "appears new" judgment can be trusted.

## Summary table

| Claim | Verdict | Confidence | Closest prior work |
|---|---|---|---|
| (a) Correlation acts as a field conjugate to the weak-feature weight. Clean transition is a critical point. Response ~\|c\|^{1/2} for c<0 and linear for c>0. First-order line c* ~ eps^2 between opposite-sign and same-sign storage | **Partially known (qualitative); quantitative/critical-point framing appears new** | Medium | Elhage et al. 2022, Sec. "Correlated and Anticorrelated Features"; Prieto et al. ICLR 2026 (arXiv 2603.09972); Shi et al. 2026 survey (2-Bernoulli/1-dim worked example) |
| (b) Training with Gaussian code noise makes the storage transition first order, shifted by ~sigma^{2/3}, with a sigma-independent spinodal (metastable mono window) and gradient training stuck at mono | **Appears new** (the qualitative "noise suppresses superposition" part is known) | Medium | Pona 2023 (dropout suppresses superposition, LessWrong); Lecomte et al. ICLR 2024 (noise and incidental polysemanticity); Marshall & Kirchner 2024 (coding theory, dropout); Chen et al. 2023 (TMS phase transitions, SGD plateaus); Bereska et al. TMLR 2025; Elimadi 2026 |
| (c) Shared Frobenius energy budget shifts the threshold. p = 1 - sqrt((1-eta)/(1+eta)) for 4 features in 2 dims. Symmetry-broken single-partner phase. General-m formula | **Appears new** | Medium (low-medium for the general-m formula, because this kind of algebra can sit in appendices) | Elhage et al. 2022 (Thomson/sphere packing, "sticky" 1/2 dimensionality, antipodal pairs); Scherlis et al. 2022 (capacity budget); Guo/Liu/Gore 2026 (partial vs full representation, a continuous transition in width); Liu/Liu/Gore 2025 (weight decay and superposition) |
| (d) ResNet18: shared-weight sign follows correlation sign; bistability concentrates at weak correlation; positive correlation adds a same-sign slot while negative correlation competes for the opposite-sign slot | **Partially known (the sign rule is the TMS toy prediction); the real-data test and slot/bistability findings appear new** | Medium | Elhage et al. 2022 (anticorrelated features prefer negative interference, correlated ones positive); Prieto et al. 2026 (constructive interference among co-activating features, real-LM structures) |

**Scoop risk:** no 2025-2026 paper found that does this project (a 2x1 energy-constrained tied-ReLU model with correlation as a field, noise-induced first-order transition, a Frobenius-budget threshold, and a ResNet test). The closest recent "phase" paper, Guo/Liu/Gore (arXiv 2609.36455, 2026-09-29), works in the large-n, large-width regime with a continuous transition in width, so its axis is different. Prieto et al. (ICLR 2026) is the closest work on correlation. **Overall scoop risk: low-moderate.** The main exposure is that reviewers will expect the 2x1 correlated results to be positioned explicitly against TMS's correlated-features section and against Prieto et al.

---

## Per-claim analysis

### (a) Correlation as a conjugate field

**Prior work:**
- **Elhage et al. 2022, "Toy Models of Superposition"**, section "Correlated and Anticorrelated Features" (https://transformer-circuits.pub/2022/toy_model/index.html). Empirical finding: models prefer to put correlated features orthogonally; if they can't, they place them with *positive* interference and may collapse them to their principal component. *Anticorrelated* features are preferentially placed with *negative* interference (antipodal). This is the qualitative core of "the sign of storage follows the sign of correlation". It is numerical and phenomenological, with no exponents, no critical point and no field picture. The TMS "toy model of the toy model" (2 features in 1 dimension) compares hand-picked candidate solutions for independent features only.
- **Prieto, Stevinson, Barsbey, Birdal, Mediano, "From Data Statistics to Feature Geometry: How Correlations Shape Superposition", ICLR 2026, arXiv 2603.09972** (https://arxiv.org/abs/2603.09972). Introduces Bag-of-Words Superposition (BOWS). With correlated features, interference can be *constructive*: features arrange by co-activation, and ReLU suppresses false positives. The effect is stronger with weight decay and produces semantic clusters and cycles. Their example of 12 cyclically correlated features gives antipodal pairs in ReLU autoencoders. **Must-cite.** It is the main modern reference on correlation and geometry, but it is empirical/geometric with no critical scaling.
- **Shi, Li, Han, Hernández-Lobato, "Feature Superposition in Neural Networks: From Theory to Practice", arXiv 2609.06862 (Sep 2026)** (https://arxiv.org/abs/2609.06862). Has a worked 2-Bernoulli-feature/1-dimension example: the antipodal code [1,-1] with a ReLU decoder has total risk 2p² versus p for the dedicated code, plus R² comparisons. It also reportedly mentions an "exact expected-loss calculation" for the bias-free d=2, m=1 case attributed to a Tom McGrath comment accompanying TMS, which adds a "confused feature" regime. **Action: check that comment (TMS reviewer/comment section) and make sure the 2x1 baseline doesn't duplicate it. I could not retrieve it.**
- **Sign-Aware Gated SAEs, arXiv 2605.28149 (2026)**. Uses antipodal pairs with within-pair correlation rho in [-1, 0] as a test bed for SAEs. This is SAE methodology, not storage theory, so cite it at most as peripheral.
- **Chanin et al. "A is for Absorption" (arXiv 2409.14507)** and **"Sparse but Wrong" (arXiv 2508.16560)**. These cover correlated features as a cause of SAE pathologies (absorption, hedging, wrong L0). They are relevant context for "correlation matters" but are about SAEs, not storage transitions.

**Judgment: PARTIALLY KNOWN.** That positive and negative correlation select same-sign and opposite-sign (antipodal) interference is known from TMS and is consistent with Prieto et al. I found **no** prior treatment of: correlation as a symmetry-breaking field conjugate to the weak-feature weight, the critical-point interpretation of the clean transition, the asymmetric response exponents (|c|^{1/2} versus linear), or a first-order line c* ~ eps². These appear new (medium confidence; searches for Landau, mean-field, order-parameter and critical-exponent language around superposition returned nothing relevant). Frame it as "a quantitative, analytically solvable version of TMS's correlated-features observation".

### (b) Noise-induced first-order transition and metastability

**Prior work:**
- **Pona 2023, "Superposition and Dropout" (LessWrong)** (https://www.lesswrong.com/posts/znShPqe9RdtB6AeFr/superposition-and-dropout). Empirically, dropout generally *inhibits* superposition, except with varied importance and low sparsity. No transition order, no scaling.
- **Lecomte, Thaman, Schaeffer, Bashkansky, Chow, Koyejo, "What Causes Polysemanticity? An Alternative Origin Story of Mixed Selectivity from Incidental Causes", ICLR 2024** (https://iclr.cc/virtual/2024/23397). Noise added after the hidden layer, and L1 regularization, induce winner-take-all and sparsity dynamics, and incidental polysemanticity depends on initialization. This is relevant to "which basin gradient descent ends in", though their setting is different (no storage-transition analysis).
- **Marshall & Kirchner 2024, arXiv 2401.17975**. Coding-theory view: dropout corrupts monosemantic and superposition codes, while redundant polysemantic codes can recover.
- **Chen, Lau, Mendel, Wei, Murfet 2023, "Dynamical versus Bayesian Phase Transitions in a Toy Model of Superposition", arXiv 2310.06301**. Closed-form TMS loss, k-gon critical points, SGD plateaus and jumps between critical points. **Must-cite** for "phase transitions in TMS and SGD getting stuck at critical points", but it doesn't involve noise and doesn't give a first-order transition with a spinodal.
- **Zhang et al. ICLR 2025 (arXiv 2410.21331)**, **Gorton & Lewis 2025 / Stevinson et al. (arXiv 2508.17456)**, **Bereska et al. TMLR 2025 (arXiv 2512.13568)** and **Elimadi 2026 "Why Does Robustness Reduce Superposition?" (arXiv 2608.22155)**. These cover robustness/noise against superposition at the level of trends. Elimadi explains the trend by adversarial training *removing features*, not by a change in transition order. Bereska et al. report abundance versus scarcity regimes and that dropout acts as a capacity constraint.
- "Noise-driven escape from metastable phases explains grokking" (ICML 2026, arXiv 2606.17120). Describes first-order transitions and metastability in L2 strength for linear networks. This is an analogous mechanism in a different setting, so it is optional to cite.

**Judgment: APPEARS NEW (medium confidence).** "Noise or robustness pressure reduces superposition" is known qualitatively. I found nothing showing that training with code noise changes the *order* of the storage transition, a sigma^{2/3} shift, a sigma-independent spinodal, or gradient descent trapped in the mono branch inside a coexistence window. Searches for "first-order", "hysteresis", "metastable" or "spinodal" combined with superposition or toy models only returned unrelated physics or the grokking paper. Caveat: dropout and noise studies on LessWrong are numerous and partly unindexed, so an informal hysteresis observation could exist.

### (c) Shared Frobenius budget across dimensions

**Prior work:**
- **Elhage et al. 2022**. Covers the unit-norm feature regime (generalized Thomson problem), dimensionality "sticky points" at 1/2 (antipodal pairs), and pairing an "extra feature" with an existing one. There is no explicit global Frobenius constraint and no closed-form threshold.
- **Scherlis et al. 2022, "Polysemanticity and Capacity in Neural Networks", arXiv 2210.01892**. A per-feature capacity budget summing to the embedding dimension, all-or-nothing versus fractional allocation depending on kurtosis, and an equal-marginal-benefit condition. This is the conceptual ancestor of "a budget shifts the threshold", but it uses a quadratic-activation computation model and its budget is dimension, not energy.
- **Guo, Liu, Gore, "Emergent phases of superposition: from partial to full representation", arXiv 2609.36455 (2026-09-29)** (https://arxiv.org/abs/2609.36455). A *continuous* transition in width from partial representation (some feature norms vanish) to full representation. The critical width is linear in the number of active features (up to a log factor), and non-uniform firing probabilities delay the transition. This is a large-n random-projection approximation with no Frobenius constraint and no small-m closed forms. **Must-cite and position against it:** both papers study "which features get representation" phases, but on different axes (energy budget versus width).
- **Liu, Liu, Gore 2025, "Superposition Yields Robust Neural Scaling", arXiv 2505.10465**. Weight decay controls the degree of superposition, which is the closest "norm-penalty" knob.

**Judgment: APPEARS NEW (medium).** I found no closed form like p = 1 - sqrt((1-eta)/(1+eta)), no symmetry-broken single-partner phase, and no general-m budget formula. Searches for Frobenius, norm budget, sphere constraint, sqrt thresholds and partner features returned nothing matching. Low-medium for the general-m formula specifically, since small-case algebra can sit unindexed in appendices (for example in Shi et al. 2026 or Chen et al. 2023).

### (d) ResNet18 real-data observations

**Prior work:**
- **Elhage et al. 2022** predicts the sign rule in toy models (see (a)).
- **Prieto et al. ICLR 2026** reports correlation-driven geometry (clusters, cycles) in real LMs and BOWS. This is constructive interference for co-activating features, which partially anticipates "positive correlation → same-sign slot". It doesn't analyse bistability or slot competition.
- Empirical superposition work on CNNs exists (for example the LessWrong "Superposition through active learning lens" study on ResNet18 cosine similarities; Bereska et al. use SAE-based measures across vision models), but none tests the sign of the shared weight against correlation sign or seed bistability.

**Judgment: PARTIALLY KNOWN / mostly new as a real-data test (medium).** The sign rule is a known toy-model *prediction*, so present it as confirming that prediction in real activations, not as a discovery. The rest appears new: that bistability concentrates at weak |c|, consistent with the critical point in (a), and the asymmetric slot picture (a positive pair adds a same-sign slot, negative pairs compete for the one opposite-sign slot). Expect reviewer scrutiny on how "features" are defined in ResNet18 activations; that is a methodology risk, not a novelty risk.

---

## Must-cite list

1. Elhage et al. 2022, Toy Models of Superposition, especially the correlated/anticorrelated section and the 2-in-1 "toy model of the toy model": https://transformer-circuits.pub/2022/toy_model/index.html , arXiv 2209.10652
2. Prieto, Stevinson, Barsbey, Birdal, Mediano, ICLR 2026, "From Data Statistics to Feature Geometry: How Correlations Shape Superposition": https://arxiv.org/abs/2603.09972 (**not in the author's current list; the most important addition**)
3. Chen, Lau, Mendel, Wei, Murfet 2023, "Dynamical versus Bayesian Phase Transitions in a Toy Model of Superposition": https://arxiv.org/abs/2310.06301 (**likely missing; needed for (b)**)
4. Guo, Liu, Gore 2026, "Emergent phases of superposition: from partial to full representation": https://arxiv.org/abs/2609.36455 (already known to the author; the transition type differs: continuous, in width)
5. Shi, Li, Han, Hernández-Lobato 2026 survey: https://arxiv.org/abs/2609.06862 (has the 2-Bernoulli/1-dim antipodal risk example; also check the McGrath-comment exact-loss reference it cites)
6. Scherlis et al. 2022: https://arxiv.org/abs/2210.01892
7. Lecomte et al. ICLR 2024, incidental polysemanticity (noise and L1 with winner-take-all): https://iclr.cc/virtual/2024/23397 (**likely missing; relevant to (b) and basin selection**)
8. Pona 2023, Superposition and Dropout: https://www.lesswrong.com/posts/znShPqe9RdtB6AeFr/superposition-and-dropout
9. Marshall & Kirchner 2024, coding-theory view of polysemanticity and dropout: https://arxiv.org/abs/2401.17975
10. Zhang et al. ICLR 2025: https://arxiv.org/abs/2410.21331 ; Stevinson/Gorton "Adversarial Examples Are Not Bugs, They Are Superposition": https://arxiv.org/abs/2508.17456 ; Bereska et al. TMLR 2025: https://arxiv.org/abs/2512.13568 ; Elimadi 2026: https://arxiv.org/abs/2608.22155
11. Optional: Liu, Liu, Gore 2025, Superposition Yields Robust Neural Scaling, https://arxiv.org/abs/2505.10465 ; Chanin et al., feature absorption, https://arxiv.org/abs/2409.14507 ; Hänni et al. 2024, https://arxiv.org/abs/2408.05451 ; noise-driven metastability and grokking (ICML 2026, arXiv 2606.17120)

Checked and judged not close: "Hidden not Deleted: How Networks Suppress Entangled Features" (arXiv 2609.27593). It is about concept erasure in antipodal pairs and does map a bifurcation versus entanglement into "mirror/shadow" solutions; that is a bistability analogue, so cite it at most peripherally for (d). Also not close: Sign-Aware Gated SAEs (2605.28149), and the SAE audit (2607.12166), which mentions a "diffuse sharing regime" in the TMS phase diagram. Garg/Kleinberg/Peng COLT 2026 ("How Many Features Can a Language Model Store Under the LRH?") is a capacity-counting framework, not storage transitions. "Vompa 2026" could not be located.

## Search log (queries)

1. toy models of superposition correlated features phase transition first order
2. "Emergent phases of superposition" Guo Liu Gore 2026
3. superposition noise training first-order transition metastable toy model ReLU autoencoder
4. arXiv 2026 superposition phases Gore toy model statistical physics
5. "Why does robustness reduce superposition" Elimadi
6. feature correlation superposition geometry antipodal correlated features toy model 2025
7. Prieto ICLR 2026 superposition correlated features bag-of-words
8. superposition weight norm constraint Frobenius budget toy model polysemanticity capacity allocation
9. Elimadi "robustness" superposition arXiv 2608.22155 abstract
10. denoising autoencoder noise injection superposition toy model phase diagram monosemanticity
11. replica analysis sparse autoencoder superposition phase transition statistical mechanics 2025
12. "superposition" toy model mean-field theory phase diagram critical exponent 2026 arXiv (extended)
13. Garg Kleinberg Peng COLT 2026 superposition
14. Vompa 2026 superposition toy model
15. hidden layer Gaussian noise superposition toy model antipodal storage discontinuous transition (extended)
16. "Feature Superposition in Neural Networks: From Theory to Practice" survey correlation noise
17. two features one dimension tied ReLU autoencoder analytic phase boundary correlation bias (extended)
18. noise-induced first-order phase transition neural network training metastable gradient descent stuck spinodal
19. "Hidden, Not Deleted: How Networks Suppress Entangled Features"
20. Tom McGrath comment toy models of superposition two features one dimension exact loss "confused feature"
21. feature absorption sparse autoencoder correlated features hierarchy Chanin 2024
22. lesswrong correlated features toy model superposition sign of weight anticorrelated antipodal
23. superposition CNN ResNet activations feature correlation antipodal sign polysemantic neurons empirical
24. Gaussian noise robustness superposition toy model analytic threshold monosemantic bias calibration 2026
25. statistical mechanics of superposition polysemanticity order parameter Landau theory 2026 (extended)
26. "superposition and dropout" lesswrong toy model noise bottleneck
27. transformer-circuits "A Toy Model of Interference Weights" 2025 correlated features
28. "incidental polysemanticity" Lecomte winner-take-all noise L1
29. Marshall Kirchner coding theory polysemanticity noise robustness
30. superposition toy model "first-order" transition hysteresis noise training ICLR 2026 OR NeurIPS 2025 (extended)
31. superposition fixed weight norm sphere constraint threshold sqrt closed form antipodal partner (extended)
32. "Dynamical versus Bayesian Phase Transitions in a Toy Model of Superposition" first order SGD
33. two Bernoulli features antipodal code ReLU decoder risk 2p^2
34. Gorton Lewis 2025 adversarial superposition; Hänni computation in superposition
35. Bereska 2025 superposition lossy compression abundance scarcity
36. arXiv 2609.27593 abstract

Abstracts fetched directly: arXiv 2609.36455, 2609.06862, 2609.27593. Timed out: 2608.22155 (abstract page). Not directly verified: the McGrath comment, and the full text of Chen et al. 2023 and Prieto et al. 2026.
