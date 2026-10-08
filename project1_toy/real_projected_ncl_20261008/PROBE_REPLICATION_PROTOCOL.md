# Bounded probe-seed reliability check

Question: does the observed native clean/corrupted ordering persist when the clean linear probe's random initialization and training order change?

Connection to Project 1: a single fitted decision rule can create a fragile apparent tradeoff. Before developing a finite-noise mechanism, establish whether the native phenomenon survives this limited nuisance change.

This follow-up is selected after observing the original TEST curve. It is not independent confirmation on unseen images or unseen pretrained models. Sigma .12 is deliberately the previously observed reversal point. No predictive or monosemanticity-causal claim is permitted.

Smallest useful test: two additional probe seeds, 20261018 and 20261019; same frozen projected checkpoint representations, same FIT/VALIDATION split, same feature standardization, 50 epochs and optimizer settings. Evaluate both native networks on all original TEST images at sigma 0 and .12 only. Three paired Gaussian directions per image, new fixed noise seed 20261020, shared across methods and probe seeds.

Report clean validation errors and both TEST differences for each probe seed. Use 2,000 paired within-class image bootstrap draws, with Bonferroni simultaneous bands across the four seed-by-noise comparisons. These intervals are conditional on the pretrained networks and fitted probes; two probe seeds do not establish backbone training-seed uncertainty.

Stopping criterion: both probes must show resolved CL advantage clean and resolved NCL advantage at .12 for this limited stability check to pass. Retain failures or inconclusive comparisons, stop after these two seeds, and do not alter the training settings, choose another sigma or add seeds to obtain a pass.

Save all probe weights, histories, validation logits, TEST per-image errors/losses, bootstrap draws, source/protocol hashes and timestamps. Large cached training and noisy features remain in cluster scratch. Original predictions and TEST records remain unchanged.
