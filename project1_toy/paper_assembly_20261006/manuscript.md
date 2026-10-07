# When does feature sharing stop paying? Training-selected robustness boundaries in a nonlinear bottleneck

Working manuscript skeleton, 6 October 2026. This assembles existing reviewed results; it does not report a new experiment or extend any theorem. Numbers below refer to immutable archived runs. The full derivations remain in `output/pdf/Superposition_Recursive_Training_Derivations.pdf` (104 pages). Submission length, author list and venue formatting are intentionally undecided.

## Abstract — working draft

Packing features into a low-dimensional representation can improve clean reconstruction while changing its sensitivity to corruption. We ask where a clean-trained sharing representation ceases to outperform coordinate-retaining monosemantic reconstruction. In an energy-constrained, two-feature tied-ReLU bottleneck, we globally characterize clean storage selection on a declared importance-frequency domain. Near its storage transition, the selected weak feature has quadratic energy and the clean sharing advantage vanishes cubically in distance to the transition. Combining this selection result with exact Gaussian code-corruption risk yields a local noise boundary proportional to that distance raised to the power three halves. Symmetric population bias calibration changes the derived coefficient; at a singular importance endpoint, the same encoders have opposite frozen and calibrated risk orderings. Prespecified finite population checks and independent numerical audits validate the scoped predictions. A frozen ResNet hidden-channel pilot has unresolved representation orderings; a separate prespecified class-mapped evidence test resolves a sharing advantage across its entire fixed noise grid, without a reversal. These operational tests do not validate hidden-feature monosemanticity or the real-model critical law. The results characterize a specific reconstruction tradeoff, not universal monosemantic robustness or adversarial safety.

## 1. Introduction: the project question

**For representations selected by clean training, where does monosemantic retention have lower corrupted reconstruction risk than feature sharing, and how does that boundary depend on feature frequency, importance, compression and noise?**

The organizing question is broader than the theorem proved here. The current exact contribution fixes two features and one code dimension, specifies encoder energy and decoder class, and derives frequency/importance/noise boundaries. Arbitrary compression ratios and a real-model phase law remain unproved. Recursive self-training is a separate Project 2 objective and is not part of this manuscript's evidence.

The important distinction is between a **storage transition** and a **risk boundary**. Clean training first selects whether the model retains only the important feature or shares its scalar code between both features. We then freeze that selected encoder and compare corrupted reconstruction risks against the clean-selected coordinate-retaining comparator. We do not handpick a sharing geometry after seeing noisy performance. Above the storage transition, the unrestricted clean optimum itself becomes mono; equality there reflects coincident models, not a nontrivial corruption-induced crossing.

Proposed contributions, subject to the precise prior-work comparison:

1. A global clean-selection result, including competing signs, feature assignments and bias activation regions, on an explicit two-feature parameter domain.
2. A derived near-transition mono-versus-sharing risk law, including its importance-dependent coefficients under two symmetric decoder policies.
3. A singular endpoint showing opposite risk orderings under those policies with encoder, task and noise held fixed.
4. Prespecified population validation and two transparently limited real-activation tests: the earlier unresolved hidden-channel pilot and the completed fixed class-evidence follow-up. A stronger hidden-semantic-feature phase demonstration remains unestablished.

Do not claim “the first robustness phase diagram,” a general literature superset, or a universal critical exponent. Broad clean/noisy tradeoffs are already established.

## 2. Related work and precise increment

- **Elhage et al. (2022):** the biased tied-ReLU reconstruction architecture, importance/sparsity storage phases and superposition motivation are inherited. Their input law and candidate energy constraints differ; our theorem is not a strict superset.
- **Jermyn et al. (2022):** biases can suppress interference and steer monosemantic training basins. Bias relevance itself is not our discovery.
- **Zhang et al. (ICLR 2025):** clean polysemantic benefit and noisy monosemantic benefit, including a small analytic comparison, are already demonstrated. Our candidate increment is the global clean selector composed with its resource-matched reconstruction-risk boundary and symmetric calibration, rather than another qualitative reversal.
- **Scherlis et al.:** importance-dependent capacity phases and the earlier Gram-based alignment score have antecedents. We do not claim the old alignment formula as original.
- **Gorton and Lewis; Elimadi et al.; Stevinson et al.:** geometry-dependent adversarial vulnerability, robustness-induced feature dropping and predictive interference-based attack theory already exist. Our scalar Gaussian code corruption is a different threat model; we do not claim stronger full-image or adversarial empirical coverage.
- **Hänni et al.:** superposition can support computation with interference correction. Our constrained reconstruction result does not imply that superposition universally harms robustness.

The claim-level comparison, primary-source passages and text hashes are in `claim_novelty_review.md` and `notebook_overlap_addendum.md`. The linked Wattenberg exact-loss notebook and official framework notebook were also inspected as source text without execution. Exact clean candidate risks, mean biases for discarded features and clean risk-difference phase plots already appear there. McGrath's primary comment additionally reports continuous clean minima, so continuity of a clean storage transition is not itself our originality claim. No exact matching conjunction for our selected critical Gaussian-code/calibration boundary was identified in these inspected sources. This supports a narrow candidate contribution, not proof that no earlier paper or notebook contains it. McGrath's comment provides no separate notebook link; its undisclosed full derivation remains unavailable for equation-by-equation comparison.

## 3. Model, outcome and comparator

Let X=(X1,X2), with independent Bernoulli(p) coordinates and importance weights (1,eta). A scalar code h=wX uses squared encoder norm one. Reconstruction is coordinatewise ReLU(w_i h+b_i), with tied decoder weights and free biases. Clean selection minimizes weighted population reconstruction MSE over the declared encoder and bias classes.

At evaluation, add independent scalar Gaussian code noise Z with standard deviation sigma: h=wX+Z. Risk is the expectation of weighted squared reconstruction error. Define Delta_j=R_sharing,j−R_mono,j. Negative Delta favors sharing; positive Delta favors mono. This is stochastic reconstruction robustness, not input-image corruption, worst-case norm-bounded attack or a general safety score.

Both representations receive the same scalar code width, squared encoder energy, tied-decoder rule and absolute code-noise budget. Tying also fixes total decoder squared norm, but redistributing w redistributes per-output noise sensitivity. Equal width and energy do not mean every possible architectural resource is matched.

The mono comparator can retain either coordinate, chosen by clean loss. Its omitted coordinate uses the best constant bias; its error is included in total risk. It is not a model that reconstructs both concepts for free. For Bernoulli targets, the omitted-feature contribution is its importance times p(1−p). An untied decoder or richer readout could exploit correlations in real features; current comparisons do not cover those alternatives.

Two policies hold the encoder fixed:

- **Frozen:** use clean-optimal biases unchanged under corruption.
- **Calibrated:** both models may optimize their biases for the noisy population distribution. Toy analysis uses population optimization. The vision pilot instead fits biases on a disjoint calibration sample, with held-out test risk.

## 4. Clean training selects sharing: theorem structure

On eta in [0.48,0.52] and p in [0.35,0.42], the reviewed global proof establishes the storage threshold

`pc(eta) = (1+eta−sqrt(1+2eta−3eta^2))/(2 eta)`.

At and above pc, important-coordinate retention is optimal. Below pc, the globally selected branch uses opposite signs. Put q=1−p, D=1−p+p^2 and A=p−eta D. Its weak-to-strong amplitude ratio k is the relevant root in (0,1) of

`A + 3 p q k + (2−3p−eta D) k^2 − p q k^3 = 0`.

This root is selected only after all competitor branches are excluded. The appendix must retain that coverage; finding a stationary point alone would be insufficient.

For epsilon=pc−p approaching zero from above, define p0=pc, q0=1−p0, D0=1−p0+p0^2 and s_eta=sqrt(1+2eta−3eta^2). The proved expansion gives k=K_eta epsilon+O(epsilon^2), where

`K_eta = s_eta / (3 p0 q0)`,

`C_eta = s_eta^3 / (27 D0 p0 q0)`.

Thus weak-feature energy is K_eta^2 epsilon^2+O(epsilon^3), while the total clean sharing advantage is C_eta epsilon^3+O(epsilon^4). These are restatements of the reviewed importance-family derivation in the companion volume, not new mathematical claims.

Interpretation: clean training buys a small additional feature near the storage threshold, but the gain shrinks rapidly. The subsequent corruption comparison evaluates that selected purchase, rather than imposing arbitrary overlap.

## 5. The mono-versus-sharing risk boundary

For sigma=t epsilon^(3/2), the reviewed family theorem gives

`Delta_j / epsilon^3 -> −C_eta + B_j(eta) t^2`.

On the declared importance interval, B_j is positive for each policy. Consequently a local crossing scale approaches sqrt(C_eta/B_j). State an asymptotic crossing and sign brackets; do not assert a unique all-noise crossing count. The exponent arises from the proved cubic clean gain balanced against the quadratic corruption penalty. The numerical exponent alone is not an independent discovery or a universal law.

The explicit coefficients are

`B_frozen = D0−(1+p0)/2 = q0(1−2p0)/2`,

`B_calibrated = D0−v(p0)`,

where `v(p)=min_z [p(1+z^2)+(1−p) H(z)]` and `H(z)=(z^2+1) Phi(z)+z phi(z)` is the second moment of ReLU(z+Z) for standard normal Z. Phi and phi are the standard normal CDF and density. On the proved importance interval, B_calibrated>B_frozen>0. The minimizer satisfies `p z+(1−p)[z Phi(z)+phi(z)]=0`. These explicit quantities make the prediction testable without fitting its coefficient.

Symmetric calibration changes B_j. At eta=2/3, where pc=1/2, a separate global proof covers 0.495<=p<0.5. There C=16/81, B_frozen=0 and B_calibrated=3/4−v(1/2), approximately .05436870643. The calibrated threshold sqrt(C/B_calibrated) is approximately 1.90608815. On this same critical scale, the frozen leading noise coefficient vanishes while the calibrated coefficient remains positive. For fixed t above that threshold and sufficiently small epsilon, sharing wins frozen and mono wins calibrated. This endpoint is a special cancellation; disclose it as such, alongside the ordinary importance-family result.

### Existing quantitative validation

| Prespecified case | Frozen Delta | Calibrated Delta enclosure |
|---|---:|---:|
| eta=2/3, epsilon=.005, sigma=.001347807858 | −2.760446858084e−8 | [7.342184481747e−8, 7.352032194179e−8] |
| eta=2/3, epsilon=.001, sigma=.000120551600 | −1.906926819009e−10 | [6.020884856940e−10, 6.040952718804e−10] |

These finite checks match the opposite-ordering prediction. They do not establish behavior away from the theorem domain. The displayed calibrated enclosures are numerical global-loss bounds computed at 70-digit precision with declared arithmetic slack and independently checked at 90 digits; they are not directed-rounding computer-assisted proof certificates. Independent audits recomputed eight endpoint bias ledgers and 666 nodes. The importance-family run checked 32 ledgers and 2,684 nodes; all fixed calibrated endpoint signs resolved. The earlier frozen population map contains 732 risk evaluations. Some calibrated bisections stopped at ambiguous midpoints; those failures and brackets remain archived rather than replaced with guessed roots.

## 6. Real-activation pilot: what transferred and what did not

An official frozen ImageNet ResNet18 was evaluated on 1,024 predetermined CIFAR10 images. The first two eligible center-cell post-ReLU layer4 channels were selected by a fixed index rule. Disjoint 256/256/512 training/calibration/test splits, training-RMS feature normalization, importance (1,2/3), five fixed scalar code-noise levels, and matched one-dimensional reconstruction models were specified before extraction. Geometry selection is numerical and lacks a global certificate for these continuous features.

The learned sharing geometry passed the training gate, with clean training gain 0.0178830. It had same-sign weights, unlike the opposite-sign Bernoulli branch. For the primary comparison, zero-noise biases were fitted on the calibration split, rather than taken from the training fit; both policies therefore coincide at zero noise. Clean-training-bias test measurements are separate archived secondary records. Under the primary zero-noise baseline, the held-out clean point estimate reversed the training advantage: sharing risk 0.3792952 versus mono 0.3702662. Every individual frozen/calibrated sharing-minus-mono 95% paired bootstrap interval included zero. **No resolved held-out representation winner, real-model phase boundary or critical exponent was obtained.**

The paired contrast between calibrated and frozen risk differences was positive at every positive noise level. At the largest fixed noise, it was 0.00594655 with conditional paired-bootstrap interval [0.00355361,0.00824315]. This supports differential calibration benefit for this operational pair, conditional on fitted models and the fixed test distribution. Intervals are pointwise, not simultaneous, and do not include training uncertainty.

A saved-record decomposition found that images with target0 equal to zero contributed 68.7% of the largest contrast. Mono's gate was exactly at zero there, while sharing gate distances varied. Calibration harmed held-out positive-target images in both models. These observations support a gate association, not causal identification or subgroup significance. The two channels have no independently established concept labels; calling this semantic monosemanticity transfer would be unsupported.

The checked Pach et al. SAE resource failed the necessary concept/provenance mapping gate, as recorded in `semantic_resource_decision.md`; no risk experiment was run from that archive. Rather than guessing names for its opaque features, a separately reviewed narrower follow-up used two officially class-mapped outputs of the cached ResNet. This closes an operational labeling gap, not the stronger requirement for validated hidden monosemantic features.

### Fixed class-evidence follow-up: a resolved sharing-favored slice

Before scores were inspected, official indices281(tabby)/207(golden retriever), zero-threshold logit rectification, seed20261007 splits256/256/4096, and the same five noise multipliers were fixed. No SAE was trained or class/threshold scanned. Class supervision supplies an intended evidence association, not ground-truth concept identity; raw-logit zero is checkpoint-gauge dependent. CIFAR cat/dog labels do not certify those subclasses. Training-only association gates passed (AUROC .904952/.808194), and the clean sharing gate passed with training gain .071075658. Same-sign weights(.83541738,.54961605) differ from the Bernoulli critical branch.

Held-out sharing-minus-mono clean risk was −.071055530 with interval[−.08898894,−.05201580]. Every frozen and calibrated difference interval remained belowzero at the five prescribed noise levels. The primary calibrated difference at multiplier .4 was −.073268875, interval[−.09160315,−.05388520]; calibrated risks were .398223291 sharing and .471492166 mono. **No ordering reversal or real critical boundary was observed.** Both absolute risks rose with noise while the sharing advantage slightly grew. Total encoder/decoder energy is matched, but importance-weighted output sensitivity need not match; this redistribution belongs to the specified decoder/noise model rather than being isolated as semantic geometry alone.

Calibration favored sharing relatively at .05/.10, was unresolved at .20, and favored mono relatively at .40: policy contrast .000617314, interval[.000346820,.000899737]. Neither policy changed the winner. All numerical calibration gaps resolved. Independent audit verified provenance, fixed association/gates,896 calibration nodes, Gaussian losses and all paired bootstrap summaries; maximum risk discrepancy4.44e−15. Raw outputs and all settings remain in `../head_transfer_20261007/`.

This supplies a resolved sharing-favored operational slice, supporting a conditional tradeoff rather than an assertion that mono always wins under noise. It does not refute Zhang et al., whose task and noise model differ, reproduce the Bernoulli critical exponent, validate hidden-feature monosemanticity or show a full-model robustness intervention. Stop this fixed pair/grid rather than extending noise to hunt for a reversal.

### Applicability diagnosis: why an importance scan would not test the critical law

Two independent mathematical and empirical AI reviewers checked the missing prerequisite before any further fitting. For nonnegative square-integrable coordinates with positive means in the declared energy-one tied-ReLU class, the feasible path `w(theta)=(sqrt(1-theta^2),theta)`, `b=(0,E X2)` has clean risk `eta Var(X2) - 2 eta Cov(X1,X2) theta + o(abs(theta))`. The retained-coordinate error is only quadratic. Nonzero covariance permits strict improvement by a sign-matched weak column arbitrarily close to mono; profiling biases can only improve that feasible candidate. Exchanging coordinates excludes both mono orientations. This is a standard covariance-prediction mechanism, not a proposed major originality claim.

The saved hidden/head TRAIN covariances are .0933814261/.1633140130. Their existing clean angular neighbors corroborate local same-sign improvement. Neither unchanged empirical training pair can possess the exact positive-importance retention onset required by the Bernoulli critical law. This is an empirical-objective statement, not population inference or proof that a noisy crossing is impossible. An importance sweep on these arrays cannot resolve the missing mechanism; numerical snapping of a weak column to zero would not establish a true transition. The full proof, saved-data script and independent six-split/sixteen-neighbor check are in `../professor_bridge_review_20261007/` and the companion volume, Section 8.29.

The reviewers also rejected widening noise to obtain an eventual calibrated crossing as central validation: the existing arbitrary-load support bound predicts that crossing because mono's omitted constant bypasses code noise. Even full-support orthogonal codes have that limit. It would not validate the selected critical geometry, exponent or semantic mechanism. A full correlated-Bernoulli extension needs new competing-branch/global-selection work and does not itself bridge the continuous real pairs. No new fitting, extraction or noise case was run during this audit.

## 7. Figure and evidence plan

1. Storage transition and local corrupted-risk boundary: distinguish geometry selection from Delta=0 and label the proved domain. Use existing saved population data and asymptotic predictions, with ambiguous brackets visible.
2. Importance-family boundary: `importance_policy_phase.png`; label analytic limits versus finite frozen points. Do not imply a complete finite calibrated map.
3. Endpoint policy contrast: `endpoint_policy_contrast.png`; same encoder/task/noise, two decoder policies, finite enclosures and asymptotic interpretation.
4. Vision pilot: `vision_policy_risk.png` and `vision_policy_contrast.png`; display unresolved representation-ordering intervals alongside the positive paired contrast.
5. Class-evidence transfer: `head_transfer_20261007/plots_v2/head_risk.png` and `head_policy_contrast.png`; display all sharing-favored intervals and the changing calibration contrast, without implying a real phase crossing.

Full derivations, Gaussian-moment calculations, bias profiling and calibration localization go in the mathematical appendix. Reproduction scripts, exact settings, ledgers, bootstrap seeds, hashes and all failed checks remain available in the repository. Standard Gaussian identities and optimization machinery are supporting methods, not separate originality claims.

## 8. Limitations and submission decision

The theory solves a declared two-feature class, not arbitrary load, unknown semantic bases, adaptive representation learning under noise or recursive training. The broader eight-feature arm failed its prescribed stationarity gate after one bounded repair; it supplies no global learned phase evidence and should be reported as unresolved supplementary work. Further optional toy repairs are stopped.

The strongest current paper material is the globally selected local boundary plus policy-dependent coefficients and endpoint contrast. Its exact novelty is plausible within inspected sources; its general significance remains a reviewer question. The earlier real pilot remains limited and unresolved; the completed class-evidence follow-up resolves a held-out sharing advantage, but lacks a phase crossing and validated hidden-feature semantics. These outcomes are complementary scoped evidence, not validation of a universal critical law. Do not imply that proof correctness, a positive toy reversal or combining two directions guarantees ICML main-track or spotlight acceptance.

## Assembly checklist

- [x] Preserve original mono-versus-sharing boundary question.
- [x] Separate broad organizing scope from actually proved theorem domain.
- [x] Identify contribution hierarchy and standard/inherited components.
- [x] Retain failed larger-toy and unresolved real-pilot outcomes.
- [x] Cross-check theorem hierarchy with professor review and claim-level literature audit.
- [x] Resolve the first semantic resource eligibility gate: failed; missing concept/provenance mapping recorded.
- [ ] Obtain one eligible externally documented semantic feature artifact; do not replace this prerequisite with unlabeled-channel scanning.
- [ ] If eligible, freeze and review one numerical protocol before fitting or noisy risk.
- [ ] Complete that one test and make a claim-strength decision from its actual evidence.
- [x] Complete and independently audit the separate professor-approved class-evidence operational follow-up; sharing wins all fixed levels, no reversal. Preserve the stronger hidden-feature requirement as unmet rather than checking it off.
- [ ] Convert the assembled manuscript to the chosen venue format after claims and evidence are fixed.
