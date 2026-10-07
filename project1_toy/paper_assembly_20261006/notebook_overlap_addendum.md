# Targeted analytical-notebook overlap addendum

Date: 2026-10-06. Scope: close the linked-source gap in `claim_novelty_review.md`, without a new literature survey, experiment, or mathematical result. Both notebooks below were downloaded and inspected as JSON and indexed cell-source text. **No remote notebook cell was executed.** Cell numbers are zero-based in the downloaded JSON.

## Verdict

The directly linked exact-model notebook does **not** contain the present globally clean-selected, equal-energy biased Bernoulli selector or its Gaussian-code-noise/calibration boundary. However, it supplies substantially more relevant prior work than a generic reference to a clean phase diagram: explicit importance-dependent clean reconstruction losses, a model-selection phase diagram, mean bias on a discarded feature, and pairwise loss-difference plots are already there. The public McGrath comment also explicitly reports continuous motion of a two-feature clean-loss minimum with sparsity. None of those ingredients should be claimed as individually new.

The narrower candidate distinction survives this inspection: an exactly globally selected, energy-one biased Bernoulli encoder, its clean cubic gain and critical code-noise scale, followed by a comparison of frozen and **symmetrically bias-calibrated** risks, including the singular endpoint policy disagreement. This is a distinction from the inspected sources, not proof that the entire literature lacks it. The change from spike-uniform to Bernoulli inputs and from unconstrained to equal-energy weights must be stated openly; the result is not a generalization of every result in the 2022 paper.

## 1. Wattenberg's directly linked exact-model notebook

Primary article links: [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html), analytical phase-diagram discussion and reproducibility links. Exact linked notebook: [Exploring_Exact_Toy_Models.ipynb](https://github.com/wattenberg/superposition/blob/main/Exploring_Exact_Toy_Models.ipynb).

Evidence from the entire 15-cell source:

- Cells 0–1 explicitly announce analytical prototypes reproducing the learned clean sparsity/importance phase diagram.
- Cell 3 defines independent spike-uniform coordinates: nonzero with probability `s`, then Uniform[0,1]. Here `s` is activation probability, despite its label “sparsity”; it is not our inactivity-probability convention. The target is weighted squared reconstruction error with final-coordinate weight `r`.
- Cell 3 defines four **fixed** tied-ReLU maps: discard first/last (`D_first`, `D_last`) or antipodally superpose first/last pair (`S_first`, `S_last`). Discarded features receive the mean bias `s/2`; superposed prototypes have zero bias. Hence a mean-corrected discarded-feature baseline is prior work, not our invention.
- Cells 4–5 give the exact candidate risks `s/3 - s²/4`, `r(s/3 - s²/4)`, `s²/3`, and `(1+r)s²/6`. These are clean risks under the notebook's spike-uniform model, not our Bernoulli formulas.
- Cells 6–7 select the minimum among these four risks over sparsity and importance. Cells 10–14 plot their least-loss surfaces and pairwise log-loss ratios. Therefore “an analytic mono-versus-superposition phase diagram” or “a pairwise risk-difference diagram” by itself is not a fresh contribution.
- For input dimension two, a discard prototype has `trace(WᵀW)=1`; its superposed block `[[1,-1],[-1,1]]` has trace 2. More generally discard trace is `n-1`, superposed trace is `n`. The comparison is not equal encoder energy. This follows directly from the displayed matrices, not a claim about some uninspected training implementation.
- No cell optimizes a continuous encoder family subject to energy one, enumerates all biased ReLU activation intervals to certify a global selector, adds Gaussian noise to the scalar code, or recalibrates both decoders under that noise.

There are minor prose/code inconsistencies in the notebook (for example cell 11 refers to conditioning on nonzero vectors whereas cells 4–5 display unconditional population-risk formulas). Our comparison uses the actual stated input distribution and formulas/code, not that stray sentence. These inconsistencies do not remove the substantial clean-risk overlap.

## 2. Official training framework notebook

Exact primary-article link: [anthropics/toy-models-of-superposition/toy_models.ipynb](https://github.com/anthropics/toy-models-of-superposition/blob/main/toy_models.ipynb).

Evidence from all 22 cell sources:

- Cell 3 implements a learned tied linear encoder/decoder, learned output bias, and ReLU. `generate_batch` draws Uniform[0,1] amplitudes masked independently by activation probabilities. Cell 4 trains all weight and bias parameters with AdamW and importance-weighted squared reconstruction error.
- There is no hard `||W||_F²=1` constraint or global-optimality certificate. Initial Xavier normalization and AdamW regularization are not the present equality constraint.
- Cells 7–18 instantiate clean multi-feature sparsity/importance sweeps and geometric diagnostics. Cell 13 calculates pairwise interference and probability-weighted aggregate interference.
- Cell 19 `compute_dimensionality` divides squared feature-vector norms by summed squared overlaps with a unit feature direction. Algebraically this equals `G_ii² / sum_j G_ij²` for nonzero feature directions: the square of the historical `M_i` expression. That geometric quantity is explicitly present in the official notebook and must not be represented as newly discovered.
- Neither noisy population-risk comparison nor symmetric bias calibration is implemented in the inspected source cells. Notebook outputs were not regenerated.

## 3. McGrath comment: a corrected source boundary

Primary source: [McGrath comment on the 2022 article](https://transformer-circuits.pub/2022/toy_model/index.html#comment-deepmind). The HTML comment contains internal article links but **no externally linked analytical notebook**. Thus “the linked McGrath notebook remains unread” is an inaccurate description of the current source gap. There is no such link in this inspected comment.

The comment itself supplies relevant analytical evidence: exact expected loss in the two-feature/one-code ReLU model **ignoring bias terms**, obtained by integrating over activation regions; full loss surfaces and minima; an equal-sign “confused feature” regime; and a transition whose minimum moves continuously as sparsity changes. It distinguishes this continuous motion from a discontinuous transition to the confused-feature regime and notes local/global basins.

Consequently, continuous clean selection, unequal antipodal weights, and exact activation-region integration are known ideas. The comment does not provide a published detailed formula/proof or code for its full minima in the linked HTML; those unreproduced derivational details remain a residual source limitation. It does not state the energy-one biased Bernoulli critical Gaussian-code risk law or the symmetric calibration-policy reversal. We must not infer an unpublished absence from the lack of a linked notebook.

## 4. Claim-level comparison and paper wording

| Proposed ingredient | Actual overlap in inspected notebook/comment | Defensible treatment |
|---|---|---|
| Biased tied-ReLU sparse autoencoder and importance-weighted risk | Official notebook; mean discard bias also exact notebook | Adopt and cite as established model/background. |
| Analytic clean mono-versus-sharing phase/risk comparison | Exact notebook cells 3–14 | Not standalone novelty. |
| Continuous clean minimum as sparsity changes | McGrath comment | Not standalone novelty. |
| Interference alignment `M` and its square | Official notebook cell 19 dimensionality | Do not claim new geometric diagnostic. |
| Global energy-one biased Bernoulli selector, including sign/bias regions | Not present in these inspected sources | Candidate exact controlled-model contribution; state changed assumptions. |
| Cubic clean gain and `sigma_c ~ epsilon^(3/2)` for that selector | Not present in these inspected sources | Candidate consequence of proved selector and exact risk; exponent balancing alone is elementary, not the whole novelty claim. |
| Frozen versus symmetric noisy-bias calibration coefficients | Not present in these inspected sources | Candidate substantive risk-policy distinction. |
| `eta=2/3` endpoint disagreement between the two policies | Not present in these inspected sources | Candidate focused result; disclose tuned endpoint and scope. |

Suggested research-claim boundary: “Building on the established tied-ReLU model and its clean sparsity–importance phase structure, we certify the clean-selected representation in a matched-energy Bernoulli setting and determine how decoder calibration changes its critical Gaussian-code-noise risk boundary.” This wording claims the specific derivation and comparison, not the original model, existence of superposition phases, general robustness, or universal monosemanticity benefits.

**Stopping decision:** the two analytical/training notebooks actually linked by the primary article have been read in full source form and the McGrath comment/link status is resolved. No broader search is justified by this particular blocker. No downloaded notebook was run, and no scientific cases or outcomes were added.

## Archived provenance

Archive folder: `notebook_source_archive/` alongside this file. The article's direct download succeeded despite the web-reader size problem. The archive contains original bytes, indexed source text, extracted McGrath prose, and `notebook_provenance.json`. Raw GitHub `main` URLs are mutable; the hashes identify exactly the inspected byte snapshots on 2026-10-06.

| Snapshot | Source | Bytes / SHA-256 |
|---|---|---|
| `primary_article.html` | `https://transformer-circuits.pub/2022/toy_model/index.html` | 8,254,697 / `beebc71a46a601f5362760f648821e18c9b374bf0a1af5c8b3b0fabddc25e37f` |
| `exact.ipynb` | `https://raw.githubusercontent.com/wattenberg/superposition/main/Exploring_Exact_Toy_Models.ipynb` | 414,311 / `7ac47b3a332159732e53f691c66d55ba4a03b8a252f9599d61fe0372094af229` |
| `official.ipynb` | `https://raw.githubusercontent.com/anthropics/toy-models-of-superposition/main/toy_models.ipynb` | 4,448,596 / `9231576b82ada2e47fdc26de064674c1ab88cbf558569364f84fa483af2864e0` |
| `mcgrath_comment.txt` | primary HTML `#comment-deepmind`, plain text extraction | `d14d7ac84d56c883784758db014a911645b4a9c4a056cfc2eab81eb5d4ee976a` |

Retrieval failures in this bounded addendum: none for direct article/raw notebook downloads. Remaining limitation: the McGrath comment does not link a full derivation or notebook, so none could be checked beyond its disclosed prose/figures. No absence proof is implied.
