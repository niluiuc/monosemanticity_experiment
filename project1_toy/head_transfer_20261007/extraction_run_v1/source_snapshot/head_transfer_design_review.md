# Professor review: fixed class-head evidence transfer

6 October2026. Prospective design review only. No class scores, features, fitting or risk comparisons were computed.

## Decision: GO for one bounded labeled operational check, with a strict claim ceiling

Official checkpoint category mapping provides independent, pre-existing semantic association for the two **class-evidence coordinates**. This is scientifically stronger than assigning names to arbitrary ResNet channels after viewing outcomes and directly repairs the missing feature-ID-to-label provenance of the rejected archive. Reusing the cached frozen checkpoint avoids new SAE/model training and a resource hunt.

It does **not** establish that the checkpoint's hidden features are monosemantic, that rectified logits are faithful causal concepts, or that the original phase theorem holds in a full vision model. It therefore satisfies a narrower semantic-linked operational requirement, not the strongest hidden-representation monosemanticity requirement. The contribution is a clean-trained compression/robustness check on externally labeled model evidence coordinates.

## Necessary design conditions

1. Verify the exact official `IMAGENET1K_V1` category strings and corresponding indices for `tabby` and `golden retriever` before reading scores. Record checkpoint hash, category metadata and IDs. Fix that pair even if sparse, nonconstant or clean-sharing gates fail; no second breed/class.
2. Declare targets exactly as `max(logit_category,0)` from the frozen official head and transforms, followed by training-only RMS scaling. The zero threshold is fixed before outcomes. Preserve raw logits as well as rectified targets. Do not move the threshold, substitute probabilities or select a relative-logit transform after a failed gate.
3. Raw logits have an additive softmax gauge: shifting all logits leaves classification probabilities unchanged but changes these rectified targets and their zeros. For a fixed checkpoint the scores are reproducibly defined, but the reconstruction result is **checkpoint-coordinate dependent**, not invariant classifier robustness. A zero target means nonpositive raw evidence in this declared gauge; it does not mean the concept is absent. The subsequent code noise is a corruption of the auxiliary compressed evidence, not an attack on the vision network.
4. CIFAR's broad cat/dog labels do not certify tabby/golden-retriever presence. Do not call class scores ground-truth concept activations or use CIFAR dog labels as breed annotations. They are outputs of a class-supervised model with independently documented intended association, subject to domain/model errors.
5. Reuse the fixed image indices/splits, numerical clean-selection gates, matched encoder energy/width, omitted-feature loss, calibration-zero baseline, fixed noise grid and held-out uncertainty protocol. No response-conditioned image selection. If switching to the already proposed larger held-out split, that split must be fixed independently before scores and recorded as a prospective design change, not described as the identical original pilot.
6. The existing hidden-channel activation file cannot supply head logits from its single spatial cell. A bounded frozen forward pass over the predefined images is necessary; using those central-cell values as if they were the official averaged head input would be an implementation error. Save genuine head scores/provenance and review the adapter before clean/noisy fitting.

## Interpretation and stopping

Positive resolved clean/noisy risk comparisons would show that a class-labeled evidence compression task exhibits the proposed tradeoff or policy sensitivity under the stated decoder/noise model. A resolved policy contrast alone remains distinct from a risk-ordering reversal. Negative, missing-zero or unresolved results must be retained and stop this pair; neither thresholds nor class IDs can change to manufacture a success.

Keep the two interpretations separate in the manuscript: the theorem concerns ground-truth Bernoulli features; this test concerns supervised class-evidence coordinates. A pair of labeled output logits is not a direct test of SAE monosemanticity or hidden-neuron semantics. This is a justified limited transfer check, not a claim that the empirical gap is completely solved or the paper now meets main-track significance.

If the intended paper claim requires validated hidden monosemantic features rather than labeled operational evidence, **STOP at that claim ceiling**: the smallest necessary alternative remains a fixed independently annotated hidden/SAE feature export with model mapping and aligned observations. Do not silently promote class logits into that missing resource. No new resource search, toy case or model training is recommended by this review.
