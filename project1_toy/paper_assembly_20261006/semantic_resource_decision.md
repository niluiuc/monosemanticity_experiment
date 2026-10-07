# Semantic resource gate: FAIL for the proposed follow-up

6 October 2026. A resource eligibility decision, not a negative scientific risk result.

## Checked resource

[Pach et al., Sparse Autoencoders Learn Monosemantic Features in Vision-Language Models](https://proceedings.neurips.cc/paper_files/paper/2025/file/89e83382abeee53b932a6df62edbf9cc-Paper-Conference.pdf), NeurIPS 2025, and its [official repository](https://github.com/ExplainableML/sae-for-vlm), fixed commit `39dff5bd6dea67fc3ef350bc7b2312e5fcfc1493`. See Appendix C, p.24, and Appendix D, p.29. The paper and raw archive stay in an external cache; source URLs, sizes and SHA256 values are in `resource_gate_v1/resource_metadata.json`.

## What was actually inspected

The archive schema and non-activation metadata, the paper's definitions and user-study/benchmark description, and the official activation extraction and top-image-index source as text. No downloaded code was executed. No activation values were used for fitting, selecting a pair or evaluating risk. The first attempt failed on macOS filesystem metadata; the corrected attempt completed in 14.813 seconds. The separate console encoding failure during page display was corrected with UTF-8 output, without changing source data or analysis.

## Findings

- The released three CSV tables contain pairwise human preferences/monosemanticity scores, top-image integer indices and 50,000 activation-column names. There is no released concept-name column or feature-to-model/layer/SAE mapping in those schemas.
- Appendix C describes features drawn from four different sources (original CLIP, two CLIP SAE variants and a SigLIP SAE). The inspected files do not map each released opaque `k` to a particular model, layer and native feature identifier. Generic extraction scripts do not supply that mapping for this archive.
- Human annotators chose which of two top-image grids looked more similar and focused. They did not supply concept labels in the released preference table. That is useful independent interpretability evidence, but not a named concept association for a preselected pair.
- Top-image entries are integer dataset indices rather than supplied images or class/concept annotations. Obtaining ImageNet images or reconstructing missing mappings would exceed the fixed resource gate; guessing an association from index values would be invalid.
- The README says activation observations are shared ImageNet validation images. However, mapping opaque features to models and verifying the image-order convention remains insufficiently documented for the required semantic/provenance claim.

## Decision and smallest outstanding requirement

Do not run a risk experiment from this archive and call it semantic monosemanticity transfer. This candidate fails the specified semantic association and per-feature provenance requirements. No replacement pair or second resource search follows this failed gate within this task. The manuscript retains the existing honest ResNet mechanism pilot.

The required next input is one pre-existing feature export with **two fixed, independently described concept-associated nonnegative coordinates, their exact model/layer/feature mapping, and aligned per-image observations**. A suitable artifact would resolve this concrete blocker; training a new SAE, inventing labels or scanning robustness curves would not. The conditional protocol in `semantic_followup_protocol.md` specifies the numerical work once that prerequisite is satisfied. Until then no new empirical success is claimed.

This does not disprove the phase-boundary theorem or show that semantic transfer is impossible. It prevents an inadequately documented resource from being used to overstate the current paper.
