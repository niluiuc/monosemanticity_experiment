# Real-activation test of correlation-decided packing (triples). Protocol written before running.

**Question.** In real ReLU activations, does a third channel's correlation with a dominant channel decide (a) the sign it is stored with and (b) whether it displaces an uncorrelated partner? This is the toy's three-feature map (fig 11).

**Data.** The same saved ResNet18 layer4 activations as `real_protocol.md`: 1024 images, RMS-normalised, the same eligibility rule, read-only.

## Triples (seed 20261008)

- **Roles.** Channel i is feature 1 (importance 1). Channel j is feature 2 (importance 0.5), required to satisfy |corr(i, j)| < 0.02 and |corr(j, k)| < 0.05. Channel k is feature 3 (importance 0.45), with c13 = corr(i, k) in one of six bins: [−0.20, −0.05), [−0.05, −0.01), [−0.01, 0.01), [0.01, 0.05), [0.05, 0.15), [0.15, 0.60].
- **Sampling.** 20 triples per bin, 120 in total.

## Model

The same scalar tied-ReLU code with free biases, w on the unit sphere, clean training (σ = 0.005, as before).

- **Global search:** a 40 × 48 direction grid, then Nelder–Mead from the 3 best grid points. Biases are profiled exactly, as in `real_pairs.py`.
- **Storage rule:** feature j counts as stored if |w_j| / max|w| > 0.05.

## Directional predictions, fixed before running

- **T1 (sign rule for the third feature).** For |c13| ≥ 0.05, the relative sign sign(w1·w3) equals sign(c13) in at least 90% of the triples where feature 3 is stored.
- **T2 (displacement).** The fraction of triples that store the uncorrelated feature 2 is lower in the two strongest-|c13| bins combined than in the [−0.01, 0.01) bin.
- **T3 (field: correlation pulls feature 3 in).** The fraction that store feature 3 is higher for |c13| ≥ 0.05 than in the [−0.01, 0.01) bin.

## Limits, stated in advance

- Features are continuous and dense, with median activity of about 0.55 (above the Bernoulli p_c), so the toy's displacement line is not expected to transfer quantitatively.
- Triples share channels, so they are not independent.

**Stopping rule.** Run once and report everything.

## Replication on class logits (added before running)

The identical code runs with `REAL_DATASET=logits`: the rectified ImageNet-class logits of the first 1024 saved images, the same selection rules and seed, 20 triples per bin.

- **Registered: T1, T2 and T3 unchanged.**
- **Also registered now (it was post hoc on layer 4):**
  - **T4.** Among triples with |c13| ≥ 0.05, three-feature storage is more frequent for c13 > 0 than for c13 < 0.
  - **T5.** The uncorrelated partner is stored less often in the strongly negative bin [−0.20, −0.05) than in the strongly positive bin [0.15, 0.60].
