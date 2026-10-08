# Pre-execution controlled image implementation review

7 October 2026 UTC. AI mathematical reviewer independently read the full prospective protocol and `controlled_image_extract.py` before training. No training, extraction, test inference or new risk evaluation was run by this reviewer.

## GO: one bounded TRAIN stage, with the declared stopping rules

Reviewed source SHA256: `41e3e048f790e455053e31b0a0a43e34caa48a9c02770f2d35a958cfe9355687`.

Reviewed protocol SHA256: `3c8e00ce2757762fa3ebcaa7367b80215582a3ff5befde1cfdf137f9ec8604d4`.

- Seeded disjoint CIFAR background IDs are used only for nuisance pixels. Original dataset class labels do not enter supervision. Each background is rendered in all four equally weighted planted states with the same nuisance, giving the exact independent-fair-bit reference law.
- Disk and bar overlays remain spatially disjoint under the specified translations; contrast bounds and independent split-specific nuisance generators are implemented. The classifier receives actual image pixels, not state IDs or labels as inputs.
- The fixed CPU CNN, optimizer, batch/epoch/runtime limits, deterministic initialization/shuffle and BCE supervision agree with the protocol. A timeout fails eligibility rather than silently qualifying the last iterate as completed.
- Float64 sigmoid is evaluated stably on saved learned logits. No hard threshold, label substitution, post-hoc temperature, score normalization or sample exclusion occurs.
- TRAIN contains 1024 images and CALIBRATION 256. The separate TEST stage does not render or infer its 1024 images until a passed recovery gate and approved, model-hash-bound prediction are present. Test images use disjoint backgrounds and fresh nuisance.
- Provenance, pixel arrays, labels, logits, soft scores, final checkpoint, epoch history and source/config hashes are retained. Failure logs are preserved.

The pre-existing dense comparison is an appropriate finite fixture for the uniform coupling bound; it is not a 3/2 exponent test. The compressor must next be actually fitted on the first64 TRAIN background quartets, exactly256 rows, with scores as inputs and true planted bits as targets. Its near-optimality lower bound must use **recovery delta on that subset**, not recovery averaged over all1024 image-model training examples. The unchanged angular/bias resolution and all prescribed optimizer/solver failures remain visible.

This GO authorizes the one bounded TRAIN stage only. It does not authorize TEST until both fixed realized-parameter sign predictions pass an independent review. Root should preserve the reviewed extraction source hash across both stages and bind the prediction to the final checkpoint/source/config. Recovery failure stops this model without repair or substitution. No success or conference-level novelty is inferred from this implementation review.
