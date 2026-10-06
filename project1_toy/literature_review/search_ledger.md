# Literature-audit search ledger

Audit date and cutoff: 5 October 2026, America/Chicago. Retrieval continued into 6 October UTC, still 5 October locally. No sources first disclosed after the cutoff are used to establish prior art.

## Method

1. Separate the full Project 1 question from its current fixed-geometry calculations and fixed-load toy experiment.
2. Search the relevant question under both neural and older mathematical terminology.
3. Inspect primary papers' actual assumptions, equations and experiments when judging direct overlap. Search results and secondary explanations are discovery aids only.
4. Follow references from direct sources and the September 2026 superposition survey. Verify titles, dates and claims against primary sources; do not inherit a survey's possible attribution errors.
5. Check paper versions and avoid inferring acceptance from a submission-format header.
6. Classify exact equivalence, substantial but different prior coverage, routine specialization, potentially open contribution, and unresolved access limitations separately.

This ledger records the search families and important trails, not a fabricated complete transcript of every search-engine request. Query phrases below describe the searched subject unless explicitly marked as exact preserved queries.

## Search families and trails

| Family | Searched subjects and reference trails | Representative primary sources located |
|---|---|---|
| Monosemanticity and robustness | Starting ICLR paper; nonnegative learning, SAE interventions, noisy toy theory and conference appendix | Zhang et al., original arXiv and ICLR 2025 versions |
| Superposition and adversarial vulnerability | Superposition attacks, sparsity sweeps, feature interference, Gram geometry, learned bottlenecks | Elhage et al.; Gorton and Lewis; Stevinson et al.; Elimadi |
| Capacity and phases | Feature dimensionality/capacity, ignored vs mono vs poly features, sparsity, importance and phase boundaries | Scherlis et al.; Liu et al.; Jermyn et al. |
| Competing geometry interpretations | Correlation structure, constructive interference, compositional failure, code redundancy, same-capacity robustness | Prieto et al.; Lu et al.; Marshall and Kirchner; Bereska et al.; Pertl et al. |
| Recent feature-recovery theory | Linear accessibility, sparse support, random spherical codes, observation noise, width bounds | Garg and Peng; Vompa |
| Sparse coding and recovery | Coherence, noisy thresholding, support recovery, signal amplitude, RIP, lower/upper bounds | Ben-Haim et al.; Fletcher et al.; Wainwright; Donoho et al.; Candès et al. |
| Neural sparse-model robustness | Forward thresholding/CNN interpretation; classifier margin, dictionary coherence, encoder stability | Papyan et al.; Romano et al.; Sulam et al. |
| Frame geometry | Rank/trace bound, total squared overlap, tight frames and frame-potential minimization | Ambrus and its classical references |
| Communication theory | Overloaded linear detection, matched filters, cross-talk, Gaussian channels, spreading codes, optimal sequences and user capacity | Viswanath et al.; Barbier and Krzakala |
| Hyperdimensional representations | Sum encodings, membership thresholding, capacity, cross-talk, random and adversarial corruption | Thomas et al. |
| Neural population coding | Mixed stimulus encoding, overlap, noise and decoding precision | Orhan and Ma, primary abstract/publisher excerpts |
| Broader robustness context | Accuracy/robustness tradeoff, nonrobust predictive features, sample complexity, margin and saliency | Tsipras et al.; Ilyas et al.; Schmidt et al.; TRADES; Etmann et al. |
| Broad field cross-check | September 2026 survey's geometry, capacity, robustness and reference sections; 2026 publisher framework preview | Shi et al.; Nature Machine Intelligence framework article |
| Primary informal disclosures | Denoising, noise injection, orthogonalization and supplied toy code | Vaintrob's January 2026 post; SONI post |
| Functional-equivalence caution | Disentangling neurons while preserving predictions | ELUDe arXiv paper |

## Exact preserved final-pass queries

- `"Adversarial Noise Attacks" "Sparse" Romano Elad`
- `"Adversarial Robustness of Supervised Sparse Coding"`
- `"Interpretability Without Tradeoffs" "ELUDe"`

These final queries resolved an initially failed ELUDe publisher download through arXiv and added two direct sparse-model robustness papers. They were not the whole search.

## High-value checks beyond abstracts

- Scherlis Eq. (3): direct algebraic identity with our squared alignment metric; capacity allocation and analytic phase sections inspected.
- Elhage: feature dimensionality and the actual adversarial-robustness experiment, rather than treating the source as a purely qualitative motivation.
- Zhang conference Appendix B.3: Gaussian-noise comparison, separating it from noisy-label and language-model safety experiments.
- Stevinson Proposition 1/Corollary 1: attack direction determined by interference, with toy/real-model experiment distinctions.
- Gorton: geometry-specific sparsity effects, not merely a monotone scalar-superposition story.
- Vompa: random-direction/fixed-support assumptions, dimension/noise bounds and threshold corollary.
- Ben-Haim Theorem 4: threshold support recovery under Gaussian noise, with sparsity/coherence/amplitude dependence.
- Thomas Theorems 2/7/10 and Lemma 11: closely related sum code and threshold recovery with Gaussian and adversarial corruption.
- Romano Theorem 7 and layered results: fixed-dictionary classifier stability; its explicit exclusion of learning.
- Sulam Theorems 4.1/5.1: robust risk and certificates for learned sparse encoders, with encoder-gap assumptions.
- CDMA: optimized sequence/power admissibility uses a different receiver and objective; its load theorem is not interchangeable with our risk boundary.

## Access and extraction limitations

- The Nature Machine Intelligence framework article was screened from its publisher preview. Full text was not available here.
- Orhan and Ma was screened from the primary abstract and publisher excerpts; full text was not inspected.
- The initial ELUDe publisher request failed; arXiv 2605.31304 was subsequently retrieved successfully. The failed record is retained rather than silently erased.
- Some mathematical PDFs have imperfect text extraction. Conclusions were checked against primary displayed equations or surrounding statements where necessary; extracted text should not be treated as an error-free mathematical transcription.
- The PDF archive includes many background papers screened at a lower reading depth than the direct competitors. `novelty_audit.md` labels that difference.
- The September 2026 survey was used for targeted section/reference tracing; this is not a claim to have read every page or checked every reference in its bibliography.

## Stopping rule

The search was stopped after covering direct neural competitors and the older mathematical equivalents that affect the actual formulas, with repeated overlap across sparse recovery, frame theory and code detection. Additional indiscriminate searches would not resolve the main remaining issue: our novelty-bearing learned-geometry boundary has not yet been derived. A precise new theorem, if obtained, will need a further targeted comparison against these archived sources.

No `plan.md` edits and no additional training runs were performed during the audit.
