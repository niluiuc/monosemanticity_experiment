# real_v1: checkpoint feasibility for the bounded real-network test

Date: 2026-10-08. Written before any experiment. Nothing has been run.

## Answer: yes, existing checkpoints make this feasible without retraining

- **The anchor repo** (PKU-ML/Beyond_Interpretability → PKU-ML/Monosemanticity-Robustness) releases code only. It has no checkpoints.
- **The predecessor NCL repo** (PKU-ML/non_neg, ICLR 2024, same group, same solo-learn codebase, same ResNet-18 SimCLR/NCL setup) **releases pretrained CL and NCL checkpoints**:
  - CIFAR-10: https://drive.google.com/drive/folders/1z57D9WOZk5N5nsqVixkUza9ZX6NiH6Wx
  - CIFAR-100: https://drive.google.com/drive/folders/1EbF9oKFu9rjsfRj_hv-Q-GVYKUSVxIkP
  - ImageNet-100: https://drive.google.com/drive/folders/1iIqn2hklptrlG3bLmjULw_rfKKO-JC5s
- The README states that CIFAR uses `non_neg=rep_relu` and ImageNet-100 uses `non_neg=relu`.
- **The repo includes `main_eval.py`,** which computes class consistency (semantic consistency), sparsity and retrieval mAP. That covers GPT's step 2 directly.
- **Caveat:**
  - I could not list the Drive folder contents from my sandbox (the page is JS-rendered).
  - Whether each folder holds the final epoch, both methods and linear heads must be checked on download.
  - The sandbox also has no torch and no Drive download access. The run must happen on GPT's runtime or the user's machine.

## Why this fits GPT's bounded design

| GPT step | Concrete choice |
|---|---|
| 1. One task, one architecture, two conditions | CIFAR-100, ResNet-18, released CL (poly) vs NCL (mono) checkpoints. The anchor's Table 1 reports exactly this pair. |
| 2. Do they differ in semantic consistency? Record capacity and clean accuracy | `main_eval.py` class consistency + sparsity (active dims / 512) on both. Linear probe on frozen features for clean accuracy. **Stop if consistency does not differ.** |
| 3. One predetermined corruption family | Additive Gaussian input noise at test time (the anchor's Fig. 2 family), on a fixed σ grid declared in advance, with the probe trained on clean data. |
| 4. Does the clean advantage reverse? Do measured properties explain it? | Report error(σ) for both models, the crossing σ\* with a bootstrap band, and whether a pre-declared prediction from the measured features (see below) gets the sign and location right. |
| 5. Stop rules | Stop if (a) consistency is not different, (b) CL has no clean advantage (band includes 0), or (c) the crossing is unresolved on the declared grid. No sweeps over width, sparsity, corruption type or label noise. |

## CPU cost estimate (ResNet-18, 32×32)

- Feature extraction for 50k train + 10k test images: about 0.6 GFLOP per image, roughly 10–20 minutes per model on a laptop CPU.
- Test features under corruption: 10k × about 8 σ values × 2 models, roughly 30–60 minutes total.
- Linear probes on cached 512-d features: minutes.
- **Total:** about 1–2 hours. This fits the few-hour limit.

## Important facts before we start (from the anchor's own Table 1)

- **CIFAR-100 label noise:** CL 54.5 vs NCL 52.8 clean, so mono is 1.7 points worse clean. NCL is ahead from 10% label noise onward.
- **The anchor already contains the crossover phenomenon** our question targets. What it lacks is any *prediction of where the crossover happens*. That is the contribution space, as GPT says.
- **Input noise:** Fig. 2 is ImageNet-100 only. Whether CIFAR-100 CL vs NCL crosses under Gaussian input noise is **not yet known**. That is what the run measures.

## Prediction the maths must make (to be frozen before test corruption)

The measured mechanism, stated as quantities computed on clean training features only:
1. **Clean gap** Δ₀ = err_NCL(0) − err_CL(0).
2. **Noise sensitivity of each model's probe logits:** the mean squared change in margin per unit σ², estimated from a small held-out *validation* subset at one small σ. This is the real-network analogue of the toy's B coefficient: the growth rate of risk with noise.
3. **Predicted crossing** σ̂\* from Δ₀ and the two growth rates (the leading-order law σ\* ≈ √(Δ₀/ΔB)). It is checked against the observed σ\* on the test set.

Whether the representation properties (consistency, sparsity) explain ΔB is a secondary pre-declared regression across the 2 models × classes. It is reported as association, not causation, per GPT's caveat that NCL does not isolate monosemanticity.

## Proposed next action

GPT (or the user) downloads the CIFAR-100 folder and reports its file list. I then write `PROTOCOL_FROZEN.md` here with the σ grid, splits, seeds and stop rules, before any corrupted test image is scored.
