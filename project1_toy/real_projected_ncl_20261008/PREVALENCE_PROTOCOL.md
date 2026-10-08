# One matched-prevalence measurement check

Question: does NCL's larger class-consistency proxy persist when both representations have the same per-coordinate activation count?

Connection: the native experiment establishes a risk reversal for two methods, not monosemanticity as the cause. A sparsity-dependent purity score cannot by itself distinguish more selective concepts from simply fewer activations. Resolve this specific measurement confound before constructing a representation-based explanation.

Smallest test: cached projected features for the original 5,000 validation images only. Normalize each image feature vector as in the original consistency score. Compute the mean original activation prevalence (absolute normalized feature value > 1e-5) across NCL nondead coordinates, without labels. Freeze one k = round(prevalence * 5000), clipped to [1,5000]. Select the top k absolute normalized activations for every nondead coordinate of each model. Break ties by the same seeded label-independent random image ordering, not class-sorted validation order. Score majority-class fraction per coordinate, then average, as before.

Report original and matched scores, prevalence, k, nondead dimensions and ties at the cutoff. Bootstrap paired images within classes with 200 fixed draws, conditional on the already selected activations. This interval does not include uncertainty of choosing k or reselecting top-k activations and must be labeled conditional/descriptive.

Stopping decision: if the matched-score difference is positive with a positive conditional interval, say this specific contrast survives the prevalence control. Otherwise say it is unresolved or fails. In neither case call it a causal monosemanticity effect or replace the original experiment's registered metric/gates. No threshold, rank-fraction or layer search follows this one check. No TEST images, new training or new noise runs.
