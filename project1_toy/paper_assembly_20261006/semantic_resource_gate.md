# Prospective resource eligibility gate

6 October 2026. Written before downloading or inspecting the candidate's activation archive and before any new risk evaluation.

## Question and connection to Project 1

Can a published vision-feature resource provide independently documented concept associations and aligned activation observations for one preselected pair? This resolves the semantic gap in the existing ResNet channel pilot, not a new toy-model question. The downstream question remains the mono-versus-sharing corrupted reconstruction risk difference, with clean training selection and both fixed decoder policies.

## Smallest useful check

Inspect only ExplainableML/sae-for-vlm (Pach et al., NeurIPS 2025): its paper's feature-evaluation appendix, official archive schema and model/feature/sample provenance. Repository commit is fixed to `39dff5bd6dea67fc3ef350bc7b2312e5fcfc1493`. The published archive is 21,980,821 bytes. Download at most this archive and the conference paper; inspect archive members, first metadata rows, feature identifiers and sample order. Do not fit a bottleneck, compute corrupted risk, or search feature pairs during this gate.

## Eligibility requirements

1. Two nonnegative operational features have documented model/layer/SAE provenance.
2. A concept association or independently interpretable feature evidence exists before risk evaluation. A human preference that feature A is more interpretable than B alone does not identify their concepts.
3. Observations for both features align to the same images, with provenance adequate for disjoint training/calibration/test splits. Published top-activation images must be separable from held-out risk images.
4. A deterministic pair-selection rule can be fixed using only external semantic evidence, without consulting noisy outcomes or choosing the most favorable clean gain.
5. Files can be read without executing downloaded source or untrusted serialized objects; no new SAE/backbone training, ImageNet acquisition or dataset construction is needed.

## Budget and stopping rule

One resource, at most 10 minutes of acquisition/schema examination, 60 MB total downloaded compressed/paper bytes, 250 MB decompressed CSV reading. Reject unsafe archive paths or links. Stop on missing semantic labels/identifier mapping/sample alignment. Document a failed gate; do not quietly substitute another pair/resource or label neurons after observing favorable risk. If eligible, write and review a separate complete numerical protocol before running it. Human interpretability evidence is not causal concept validation, which remains an explicit limit even if the gate passes.

## Initial metadata observation

Official GitHub tree reports `metric_benchmark.tar.gz` as 21,980,821 bytes, blob `01e77226eb42271eb727977d059f172825979f00`. The README describes pairwise human interpretability preferences, top-16 ImageNet training images, and validation activations. Those descriptions do not yet establish feature-to-model mapping or semantic labels. Eligibility is pending.
