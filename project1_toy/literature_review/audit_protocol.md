# Project 1 novelty audit protocol

Audit requested and protocol recorded: 2026-10-05 (America/Chicago).
No additional toy-model training is authorized by this literature audit.

## Target to audit

Project 1 seeks a mathematical boundary or tight bound for when compressed feature
representations in superposition help versus hurt robustness, depending on feature
activation sparsity, feature-to-dimension ratio, importance distribution and specified
corruption. The intended evidence is derivation, known-ground-truth toy models and
a small real-model demonstration. The empirical starting point is monosemanticity
and robustness (Zhang et al., ICLR 2025).

The implemented first experiment is narrower: independent Bernoulli concepts,
tied ReLU autoencoder, fixed encoder energy, clean population reconstruction
training, test-time Gaussian noise in code space, matched and decoder thresholds,
fixed n=8/m=4 and a restricted monosemantic baseline. The derivations also include
an exact two-feature comparison, general finite-state risk, an alignment metric
and a Bernstein-style error upper bound. These are audited separately from the
uncompleted general learned-geometry boundary.

## Screening breadth

Search the relevant literature across (1) superposition/monosemanticity theories,
(2) robustness, interpretability and capacity tradeoffs, (3) sparse coding,
compressed sensing and dictionary/frame design, (4) overloaded multiuser and
Gaussian-channel detection, and (5) feature-load/importance neural scaling theory.
Use title/abstract searches, equation and terminology searches, and references
from full-text relevant works. Include old work and recent preprints rather than
restricting to the nearest named papers. Exclude quantum superposition unless
there is a concrete mathematical match to this statistical model.

Primary sources only for conclusions. Secondary results may aid discovery but
are not evidence of a paper's mathematical or experimental claims. Check arXiv
submission/version dates and restrict novelty judgments to work available by
2026-10-05. Archive retrieval URLs, versions and content hashes where possible.
Do not infer venue acceptance from a submission PDF alone.

## Evidence categories

- Established directly or equivalent after a variable transformation.
- Substantive prior coverage of the question, but not identical assumptions/result.
- Routine specialization/application of known tools; not sufficient novelty by itself.
- A potentially open contribution not established in this project or this search.
- Unknown because the full source could not be inspected or coverage is incomplete.

An absence of a search hit is not proof of novelty. Do not treat binary rather than
continuous amplitudes, a different noise location, a different seed count or a new
plot as automatically a publishable scientific contribution. Conversely, do not
declare an unproved general boundary already solved merely because a related paper
studies a narrower case. Record the exact overlap and difference.

## Deliverables

1. Dated search ledger and source inventory.
2. Claim-by-claim comparison of current formulas and experiments.
3. Wider survey matrix with source links and reading depth.
4. A direct verdict separating the broad question, existing calculations and the
   still-uncompleted stronger result, with explicit uncertainty.
5. Save the audit separately and report findings in chat. Per the user's explicit
   instruction, do not write anything to plan.md during this audit.

## Coverage constraint

The requested breadth is the relevant existing literature, including terminology
outside mechanistic interpretability. No finite search can certify that every
publication, private project, unindexed manuscript or future submission was checked.
The final report must state actual search coverage rather than claiming omniscience.
