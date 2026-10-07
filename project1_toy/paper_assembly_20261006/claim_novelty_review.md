# Claim-level originality review for the assembled Project 1 paper

6 October 2026. This is a focused comparison against eight archived primary fulltexts. Relevant model definitions, result statements and proof/experimental sections were re-read directly from their local `paper.txt` files; the earlier survey was used as an index, not as a substitute for those passages. No new literature search, scientific experiment, proof or central-source edit was performed. Section/equation references below identify the preserved versions, not an assumed latest version. Failure to identify an exact match is not a proof of absence from the literature.

## Verdict and the exact candidate

The inspected sources already establish clean sparsity/importance storage phases, importance-dependent capacity allocation, biased-ReLU interference suppression, and clean-performance/robustness tradeoffs. A paper claiming any of those broad phenomena as its invention would overlap directly.

The specific candidate addition is narrower and more defensible: **compose a globally proved clean storage transition with the same resource-matched decoder's corrupted reconstruction risk, derive its near-transition noise scale and coefficient, and show that symmetric bias calibration can change the leading coefficient and even the risk ordering of identical encoders.** I did not identify this complete conjunction in the inspected source statements and derivations.

The existing Project 1 theorems specify:

- Two independent Bernoulli(p) targets, one-dimensional linear code, encoder squared energy one, tied ReLU reconstruction and free clean biases. Risk is weighted population reconstruction MSE, with importance (1,eta). Code corruption is one independent scalar Gaussian of standard deviation sigma. It is not input-space noise or a worst-case attack.
- Global clean selection over both encoder sign sectors, both importance orientations and all bias activation intervals. The proved family rectangle eta in [.48,.52], p in [.35,.42] has the exact transition pc determined by p=eta(1-p+p^2). Below it, epsilon=pc-p gives weak-column energy of order epsilon^2 and clean sharing gain of order epsilon^3.
- Frozen and symmetrically population-calibrated policies have a local risk boundary sigma/epsilon^(3/2) approaching a derived positive policy-dependent coefficient. The theorem establishes an asymptotic crossing and sign brackets, not a unique all-noise crossing count.
- At eta=2/3 and pc=1/2, global clean selection is proved on p in [.495,.5). The frozen leading variance difference vanishes; calibrated mono still gains a positive leading variance advantage. At fixed t above the derived calibrated threshold, sigma=t epsilon^(3/2) favors sharing under frozen biases but mono under symmetric population bias calibration, for sufficiently small epsilon. Same encoders, noise and MSE; different allowed decoder adaptation.

These are the precise claims to compare. An exponent without its control variable, outcome, selection rule and calibration policy is not the same theorem.

## Direct source comparisons

### Elhage et al., *Toy Models of Superposition* (2022)

Primary [article](https://transformer-circuits.pub/2022/toy_model/index.html), [arXiv](https://arxiv.org/abs/2209.10652). Archive key `elhang2022` is misspelled. Direct local evidence: PDF pp.10–11 model/loss definition; pp.14–15 storage phase section (`paper.txt` lines 545–591 and 803–865); pp.29–30 adversarial section (lines 1417 onward).

The architecture is inherited: linear encoding, tied transpose decoding, free biases, ReLU output and importance-weighted reconstruction MSE. Inputs are spike-and-uniform continuous amplitudes. The clean phase study already uses two features and one code dimension, varies feature importance/sparsity, trains geometries and analytically compares the natural retain-1/retain-2/antipodal alternatives. The analytic candidates have W=[1,0], [0,1], [1,-1]; their encoder energies differ. It reports first-order switching among those candidates. The adversarial section already explains interference-driven vulnerability and tests input L2 attacks.

**Overlap:** the model family, two-to-one setting, bias suppression, clean storage phases and the capacity/robustness motivation are not new. **Distinction:** our energy-one constraint makes those particular candidate comparisons inapplicable without reoptimization; our free-bias global branch proof, continuous birth of the weak column under the specified Bernoulli distribution and selected-geometry Gaussian-code risk law are a constraint-specific extension. Do not claim their work only compared arbitrary supplied weights: their empirical geometry was clean-trained. Nor call our result a strict superset, since the input law, resource constraint and phase order differ. The local archived comments also disclose McGrath's bias-free full-loss-surface analysis; its linked notebook was not separately audited here, leaving a residual exact-equation comparison gap.

### Jermyn et al., *Engineering Monosemanticity in Toy Models* (2022)

[Primary paper](https://arxiv.org/abs/2211.09169). Direct evidence: Section 2.3, Eqs.(4)–(6), p.4; Sections 4.1.1–4.1.2, pp.7–12, Figures 5,7–9; Section 5.2 and discussion. Local lines 202–226, 395–409, 558–664 and 1607–1657.

Its learned architecture is L2*ReLU(L1*x+b), with a fixed projected input and untied learned matrices; the nonlinear width can vary independently of embedding width. It finds monosemantic and polysemantic loss basins, relates negative/positive biases to their neuron behavior and uses negative-bias initialization plus bias weight decay to steer training. Its displayed negative initial-bias scale is proportional to the square root of feature density, not our noise boundary as a power of distance to a globally selected storage transition.

**Overlap:** biases can change monosemanticity and suppress interference; calling bias/gate placement relevant is not a new scientific discovery. **Distinction:** training-path intervention and neuron-basin selection differ from holding globally clean-selected encoders fixed and comparing two population test-time calibration policies. The reviewed result is not the specified risk-gap/coefficient/endpoint theorem. Our work does not subsume their architectural/training claims.

### Zhang et al., *Beyond Interpretability* (ICLR 2025)

[Conference paper](https://proceedings.iclr.cc/paper_files/paper/2025/file/11822e84689e631615199db3b75cd0e4-Paper-Conference.pdf), [arXiv](https://arxiv.org/abs/2410.21331). Direct evidence: Section 4.2/Figure 5, p.9; Section 4.3/Theorems 4.1–4.2, pp.9–10; Appendix B.3/Theorems B.7–B.9, Eqs.(45)–(55), pp.24–25; Appendix B.4, pp.25–28. Local lines 827–921 and 1997–2117.

The 40-feature/20-dimensional toy is trained on reconstruction before a downstream linear classifier is tested on noisy labels or input Gaussian corruption. Its clean polysemantic advantage and noisy monosemantic advantage are already observed. Theory fixes nu_mono=x1 and nu_poly=x1-x2 under spike-and-uniform features, with argmax labels and conditional-moment separation J. Appendix B.3 gives added score variances lambda^2 and 2lambda^2 and a separation-order reversal. Appendix B.4 allows unequal positive mixing weights, but does not optimize them by our norm-one free-bias reconstruction objective.

**Overlap:** clean-trained superposition can help clean performance yet lose under corruption, including an analytic two-feature noise comparison. Therefore neither another reversal nor an elementary extra-variance calculation suffices as originality. **Distinction:** exact weighted reconstruction MSE after a proved global clean selector; common code-noise energy budget; asymptotic boundary tied to the selected weak-feature birth; symmetric globally localized decoder calibration; and the singular endpoint's frozen/calibrated opposite ordering. These are not a refutation of its conditional-separation theorem, because the tasks, noise locations and resource controls differ. The paper's main monosemanticity interventions and robustness experiments are broader than our theory.

### Scherlis et al., *Polysemanticity and Capacity in Neural Networks* (archived updated version)

[Primary paper](https://arxiv.org/abs/2210.01892). Direct evidence: Section 2.1 Eq.(3), p.5; Section 3.1 Eqs.(9)–(11), p.7; Section 3.4 Eqs.(15)–(18) and Section 3.5 phase boundaries, pp.8–9. Local lines 146–165, 260–289 and 392–455.

Its feature capacity is exactly the square of the earlier proposed Gram alignment score. Its solvable model predicts a scalar quadratic target sum(v_i*x_i^2), with quadratic neurons and centered independent inputs; it derives optimal ignored/partial/full capacity allocations depending on importance and kurtosis, across dimension budgets.

**Overlap:** analytical capacity allocation and importance/sparsity phases are established; the old M score cannot be claimed as new. **Distinction:** quadratic scalar regression differs from biased tied-ReLU vector reconstruction with Bernoulli targets and subsequent Gaussian code MSE. It supplies no directly applicable formula for our calibration-dependent critical risk law. Conversely, its arbitrary-dimensional capacity theory is not contained in our two-feature result; calling ours a generalization of all of it would be incorrect.

### Gorton and Lewis, *Adversarial Examples Are Not Bugs, They Are Superposition* (2025)

[Primary paper](https://arxiv.org/abs/2508.17456). Direct evidence: Sections 3.1.1–3.1.4, pp.3–4, including L2 reconstruction attack definition; Section 3.2/Figure 2, pp.4–5; Section 3.3 robust-training intervention. Local lines 153–250.

It clean-trains a tied-ReLU reconstruction toy with learned biases, n=100/m=20 and uniform importance; it varies sparsity, measures input-space worst-case MSE vulnerability and observes a dip near antipodal superposition. Learned negative biases suppress ordinary interference, while adversarial perturbations can overcome them.

**Overlap:** geometry matters beyond a coarse amount-of-superposition metric; antipodal geometry can have a nonmonotone robustness relation; clean-trained biased reconstruction plus a robustness test is established. **Distinction:** their empirical input-attack risk is not our exact Gaussian-code risk at a globally selected storage endpoint. Our policy coefficient and opposite calibrated/frozen ordering are not the same dip. Do not claim to explain that dip without evidence linking the noise/task/geometry differences.

### Elimadi et al., *Why Does Robustness Reduce Superposition?* (2026)

[Primary paper](https://arxiv.org/abs/2608.22155). Direct evidence: Section 3.6 Eq.(8), Section 3.7, p.3; Sections 5.1–5.3, pp.5–8. Local lines 153–175 and 244–363.

It trains on a mixture of clean and adversarial reconstruction loss, evaluates selected sparsities, and constructs amplitude-defined robust/nonrobust feature groups. Its explanation is that adversarial training preferentially drops costly nonrobust features, reducing superposition. Section 5.3 supplies a conceptual cost argument, not our global clean selector or Gaussian calibration boundary.

**Overlap:** robustness-induced feature abandonment is known. **Distinction:** robust retraining and input attacks differ from our clean global selection plus frozen-encoder test-time bias adaptation. A statement that dropping features improves robustness is not an adequate new central claim.

### Stevinson et al., *Adversarial Vulnerability from Interference Between Features in Superposition* (archived v2; ICML 2026)

[Primary paper](https://arxiv.org/abs/2510.11709). The archive key contains 2025, but the inspected title page explicitly identifies ICML 2026. Direct evidence: Sections 3.1–3.2, pp.3–4; Section 4.1/Proposition 1, p.5; Appendix B.1 pairwise-margin proposition, pp.13–14; Appendix C.2 nonlinear biased decoder variant, pp.15–16. Local lines 287–405, 418 onward and 1429–1581.

It trains a sparse continuous-input argmax classifier with a linear bottleneck and untied encoder/decoder, derives an optimal pairwise-margin adversarial perturbation and verifies attack geometry/transferability in synthetic tasks and image classifiers. Its ReLU/bias variant keeps the same attack mechanism. It already provides a representation-level predictive theory plus substantial real-vision experiments.

**Overlap:** interference-driven vulnerability with theoretically predicted geometry and real-model verification is taken; a generic Gram/coherence-versus-robustness framing would collide. **Distinction:** classification margin attacks and cross-entropy training differ from the storage-transition Gaussian-MSE critical law and decoder-policy reversal. The current two-channel frozen-ResNet pilot is substantially narrower than its full-model image experiments and cannot be presented as comparable empirical scope. The theoretical distinction, not a stronger real-model claim, must carry our manuscript.

### Hänni et al., *Mathematical Models of Computation in Superposition* (2024)

[Primary paper](https://arxiv.org/abs/2408.05451). Direct evidence: Section 3, Theorems 1–3, pp.4–5; Section 4, Theorems 6–8, pp.6–7; robustness discussion pp.8–9; Appendix D.4, Theorem 21, p.21. Local lines 313–459, 576–631, 737–749 and 1714 onward.

It constructs networks that compute sparse Boolean circuits in superposition and error-correction layers that reduce representation error. Theorem 21's error/interference bound depends on width d, sparsity s and representation error; dimension/circuit-width relations include powers such as 1.5. It is not a noisy population reconstruction-risk crossing with sigma scaling in pc-p.

**Overlap:** nonlinear gates can correct interference/noise and superposition can remain computationally useful; a universal claim that overlap necessarily causes fragility would contradict the scope of this constructive work. **Distinction:** constructive circuit emulation/error correction has no clean Bernoulli storage optimizer, matched two-feature retention comparator or symmetric population bias-calibration risk law. Identical numerical exponents occurring in unrelated bounds are not identical results.

## Known components versus the actual proposed increment

| Component | Assessment |
|---|---|
| Tied biased ReLU toy and sparse feature packing | Inherited from Elhage; not our contribution |
| Importance-dependent storage/capacity phases | Established; our global constraint-specific transition is a precise extension |
| Negative bias/gates suppress interference | Established by Elhage/Jermyn and later work |
| Mono can beat sharing under corruption | Already analytic/empirical in Zhang and related robustness work |
| Exact Gaussian ReLU moments, scalar interval profiling and Taylor bounds | Standard tools/correctness machinery; no independent originality established |
| Balancing a cubic clean gain with quadratic noise to obtain a 3/2 scale | The algebraic balance alone is elementary; original value would lie in proving those terms arise from global clean selection and remain under symmetric calibration |
| Full selected-geometry critical law with explicit calibrated/frozen coefficients | No exact matching conjunction identified in the inspected passages; plausible narrow original result |
| eta=2/3 singular endpoint: same encoder/MSE/noise, opposite ordering under the two decoder policies | Strongest specific candidate distinction identified here; no matching inspected theorem, but constrained and asymptotic rather than universal |
| Two arbitrary learned channels show differential calibration benefit | A narrow empirical mechanism check; not semantic monosemanticity or a transferred critical law |

## Paper-critical concerns and honest wording

1. **Fine tuning:** the eta=2/3 endpoint is a special cancellation. It is analytically interesting but not evidence of generic real-world reversal. Present the ordinary eta-interval law alongside it and disclose the endpoint's fixed assumptions.
2. **Generic scaling:** epsilon^3 versus sigma^2 balances routinely produce 3/2. Do not market the exponent's number as a universal new law; emphasize the proved training-selected mechanism, globality, policy coefficients and singular contrast.
3. **Decoder class:** calibration here means free reconstruction biases at fixed W. It is neither Bayes-optimal arbitrary readout nor full fine-tuning. A different decoder class can change the result.
4. **Semantic scope:** the mono comparator retains one declared ground-truth coordinate; in the vision pilot those coordinates are operational channels without semantic validation. The real pilot has a positive paired policy contrast but no resolved held-out clean sharing advantage or ordering reversal. Keep that unfavorable gap visible.
5. **Not a literature superset:** the original larger organizing question is legitimate, but this theorem does not subsume the different input, architectural, dimensional or adversarial regimes above.
6. **Remaining disclosure risk:** the Elhage analytical notebooks and McGrath linked full-surface notebook were not audited equation-by-equation here. The direct fulltexts support a plausible specific addition; notebook/private/unindexed overlap remains possible.

Suggested central wording: “For a resource-matched tied-ReLU bottleneck, we characterize how the globally clean-selected storage transition produces a calibration-dependent Gaussian reconstruction-risk boundary. A singular endpoint yields opposite frozen and calibrated risk orderings for the same representations.” Avoid “first phase diagram,” “monosemanticity guarantees robustness,” “universal critical exponent,” “generalizes all prior theory,” or a claim that the vision pilot reproduces the theorem.

## Preserved fulltext evidence hashes

All paths are under `project1_toy/literature_review/sources/<key>/paper.txt`; page markers in these text files correspond to their archived PDF versions. Source PDF hashes/URLs/version histories are separately preserved in `source_index.md` and each `provenance.json`.

| Key | SHA256 of text inspected |
|---|---|
| elhang2022 | `4028176a8b04fa8f27e74bc28ab7d107911f9deb6dbb48039400267b4071a46d` |
| jermyn2022 | `c26c73d4247e08ccb30b2fa73ee7ee6950252145453243d5da34fdcf6f74839b` |
| zhang_iclr2025 | `e3ade0a200c5c73db01db9f52a8234294abee58ca71249a992fc7bb1d52a715d` |
| scherlis2022 | `7de20614a0ab530098189fa8818e2d4fe819ae51384d6b25b0a875b8bb59beff` |
| gorton2025 | `53e24ce8fd0de38f77ddfbc82fa54c928ec720f6c3d79a2dcd0861835c180b9b` |
| elimadi2026 | `da22da19120f0784902f96e0ea010d6c4e752210b21dc5549a2e8c778f9d3b97` |
| stevinson2025 | `ff7b39dfac18a5eca65fb918c05a919a92e8835fb7639e515fca2da00aeb0bfb` |
| hanni2024 | `cae90d97cdd96f499b81c1ad51d546eb6213555de46f7e17f8836bcf1f1f05f4` |
