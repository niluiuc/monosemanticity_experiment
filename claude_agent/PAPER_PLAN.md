# A possible paper built on the existing manuscript plus the claude_agent additions

This proposes structure only. It is additive and does not replace `project1_toy/paper_assembly_20261006/manuscript.md`; the existing theorem stays the core. Status labels follow `STATEMENTS.md`.

**Working title:** *When does superposition pay? Storage phases, correlation fields and noise in a solvable bottleneck.*

**One-sentence thesis.** In the solvable tied-ReLU bottleneck, the existing critical storage boundary is the critical point of a larger phase diagram.

- Feature correlation acts as a field.
- Training noise makes storage first order, with a metastable window.
- The resource convention (fixed versus shared energy) moves the boundaries and fixes the compression phases.
- The same selection rules appear in real ResNet18 activations.

## Sections

1. **Introduction and question.** The question is unchanged from the manuscript: for clean- or noise-trained representations, when is monosemantic retention better than sharing?
2. **Model and comparator.** Unchanged (manuscript §3), plus correlation c, the training-noise protocol, and the two resource conventions (per-dimension and shared Frobenius).
3. **Clean storage transition and risk boundary.** Existing: global selection, ε³ gain, ε^{3/2} boundary, frozen and calibrated coefficients. *Existing theorems.*
4. **Correlation as a field.**
   - Lemma A′, the exact local expansion. *Theorem (local).*
   - Exponents 1/2 and 1, and the first-order line c\* ∝ ε². *Leading order.*
   - Endpoint under noise. *Numerical.*
   - Figs 2, 5.
5. **Training noise.**
   - First-order transition at ε\* = (B_cal/C)^{1/3}σ^{2/3}, which reuses the existing coefficients. *Leading order, plus precise numerics at four η.*
   - Mono spinodal κ₀ and the O(1) metastable window. *Leading order.*
   - Gradient-flow and Adam behaviour. *Numerical.*
   - Figs 3, 4, 6, 10.
6. **Resource convention and compression.**
   - Shared-budget thresholds 1 − √((1−η)/(1+η)) and (3η−1)/(η+1). *Local plus numerical.*
   - Symmetry-broken one-partner phase, and the first-order 1 → 2 partner switch. *Numerical.*
   - Trained networks agree. *Numerical.*
   - The bicritical identity B_frozen = κ₊·D(2−p)/(2pq), which explains the manuscript's special endpoint. *Exact identity.*
   - Fig 13.
7. **Correlation decides packing.** Three features in one dimension: correlation adds or competes for slots (fig 11). *Numerical.*
8. **Real representations.**
   - Pre-registered pair tests on two ResNet18 representations, and triple tests.
   - All registered failures are reported (noise shrinkage on layer 4, pooled displacement).
   - The field equals 2ηCov exactly, but the quadratic stiffness does not transfer.
   - Figs 7–9, 12; main figure panels (c) and (d).
   - The earlier ResNet pilots (manuscript §6) are re-read through the field picture.
9. **Related work.** As in the manuscript, plus TMS's correlated-feature observations, which give the qualitative sign rule; Elimadi (2026); and denoising.
10. **Limitations.**
    - Small n and m.
    - Several statements are leading order rather than proved.
    - Global selection is open for c ≠ 0.
    - Real tests are directional, on one network.

## Main figure

`figures/fig_main.pdf`. A compression panel (fig 13a) could be added as a fifth panel or a second figure.

## Status after session 3 (additive update)

- **S2 global branch selection:** certified on a 64-point grid (63 resolved).
- **S3 location:** explained to < 1% by an explicit scaling function.
- **S4:** has its first-order term.
- **S5 endpoint:** has a mechanism and a linear law.
- **Compression:** generalised to any m and confirmed with trained networks, including under training noise.
- **Real-data asymmetry:** confirmed prospectively on a second representation.

## Remaining work that most raises acceptance odds (my ranking)

1. **Rigorous versions of S3 and S4**, using the existing calibrated-coefficient machinery. This turns the noise story into theorems.
2. **Global selection at c ≠ 0.** Now certified on a grid; a continuum or interval-arithmetic version would turn S2 into a theorem.
3. **A second real network**, for example a small language model's SAE features, for the pair sign rule and the triples. This answers "one ResNet only".
4. **Theory for the c_e(σ) endpoint and the 1 → 2 partner switch.**

No timeline is implied here; ordering is by value only.
