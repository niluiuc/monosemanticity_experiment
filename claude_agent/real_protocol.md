# Real-activation test of the field picture (protocol, written before running)

**Question.** Do real ReLU activations follow the qualitative selection rules of the toy phase diagram (README §2–§4)?

**Data.** We reuse the already-saved frozen ImageNet ResNet18 layer4 center-cell post-ReLU activations: `project1_toy/vision_transfer_20261006/extraction_run_v1/vision_activations.npz`, 1024 CIFAR10 images × 512 channels. There is no new extraction or download, and the archived files are only read.

## Fixed settings

- **Eligible channels:** zero fraction in (0.05, 0.95) on all 1024 images.
- **Which images are used:** all 1024 define the empirical distribution. This is a selection-mechanism test on a fixed empirical distribution, not held-out generalisation.
- **Normalisation:** each channel is divided by its RMS.
- **Pairs:** 200 pairs, seed 20261007. Pearson correlations are split into 8 equal-count bins over all eligible pairs, and 25 pairs are drawn per bin. Feature 1 is the lower channel index (importance 1); feature 2 has importance η = 0.5.
- **Model:** the same energy-one scalar code and tied ReLU decoder with free biases as the toy. Gaussian code noise σ ∈ {0.005, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6} (in RMS units). σ = 0.005 stands in for clean, and keeps the loss smooth.
- **Selection:** global over θ on a 240-point grid over [−π/2, π/2), plus refinement. For each θ the biases are profiled by grid initialisation (31 points) and 10 Newton steps on the exact per-sample Gaussian loss.
- **Recorded per (pair, σ):** θ\*, F(θ\*), F(mono), and the grid local minima inside the feature-1-dominant sector |θ| < π/4.

## Directional predictions, fixed before running

- **P1 (sign rule, clean).** Pairs with corr < −0.05 select θ\* < 0 (opposite sign) in at least 90% of cases. Pairs with corr > 0.15 select θ\* > 0 in at least 90%. Between those, the switch to same-sign storage needs larger positive correlation for *sparser* pairs. The toy line is c\* ∝ ε², with ε = p_c − p, so it grows with sparsity.
- **P2 (first order needs weak correlation).** Bistability, meaning two local minima in the sector at some σ, occurs more often in the lowest |corr| tercile than in the highest.
- **P3 (noise shrinks storage).** The median |tan θ\*| decreases from σ = 0.005 to σ = 0.6.

## Limits, stated in advance

- The features are continuous and not independent Bernoulli, so no toy coefficient is expected to transfer. Only directions are tested.
- With n = 1024 the correlation standard error is about 0.03.
- Pairs are not independent: channels repeat across pairs.

**Stopping rule.** Run once, report all outcomes, and do not re-select pairs or settings.

## Replication on a second representation (added after the primary run, before this run)

The same code is run with `REAL_DATASET=logits`.

- **Data.** The saved ResNet18 1000-class logits, rectified at zero: the first 1024 rows of `project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy`, read-only. These are class-evidence coordinates, a different representation from the hidden channels.
- **Pairs.** 120 pairs (8 correlation bins × 15), seed 20261007, chosen by the same eligibility rule.
- **Predictions.** P1–P3 exactly as above, with no changes. P3 is kept even though it failed on layer4, so the replication is not cherry-picked.
