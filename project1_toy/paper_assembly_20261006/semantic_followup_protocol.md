# One semantic-linked follow-up: conditional numerical protocol

6 October 2026. **NOT executable yet:** the resource gate failed. This records the exact work to perform once a resource satisfies it. No new result, pair, numerical outcome or runnable-data claim is implied. Fix actual artifact hashes, feature IDs and semantic evidence, and obtain professor review before activation inspection or fitting.

## Question and relation to the theorem

For two independently concept-associated real-model features, does a clean-trained shared scalar representation retain its clean advantage under Gaussian code corruption, and does symmetric bias calibration change its risk relative to coordinate retention? This tests relevance of the Project 1 tradeoff to externally described concepts. It cannot reproduce a Bernoulli storage transition or establish its critical exponent from one empirical feature distribution. It is a controlled reconstruction model built on real learned features, not a full vision-network robustness intervention.

## Fixed inputs and selection

- One frozen published model/layer/SAE resource only. Require exact feature IDs, checkpoint or export hashes, preprocessing, nonnegative finite paired activations, and one observation per image.
- Require two distinct independently described concepts and their feature associations, established before looking at downstream risk. Do not infer labels from favorable loss curves. Record the strength and limitations of the external association; an SAE coordinate is not automatically ground truth.
- Fix the pair from that external evidence before reading activation outcomes. No fallback pair after a failed clean gate. If multiple externally eligible pairs exist, a deterministic ID-order rule must be declared before loading activation values; do not choose by training gain, frequency or crossing.
- Require at least 4,608 aligned images. Use one permutation with NumPy `default_rng(20261007)`: first 256 training, next 256 calibration, next 4,096 test; unused images are not a reserve for retries. Published images used to establish feature associations must be disjoint from these observations or identified and excluded by a fixed rule before permutation.
- Preserve raw arrays, image identifiers/order, labels used solely as external semantic evidence, resource provenance and exclusion list. Normalize each feature by training RMS without centering.

## Model and clean-selection gate

- Importance (1,2/3), one-dimensional encoder, squared encoder norm one, tied ReLU decoder, two free biases. Mono retains either feature, with orientation selected by clean training loss; omitted feature has its best constant prediction and contributes to total risk.
- Reuse existing continuous bias profiling and angular search implementation. Grids 256 then 512 on [0,pi), exactly one best-cell refinement each, no restarts or extra cells.
- Require positive means and variances, at least one feature with exact zero mass in training, refined-loss agreement within absolute 1e-6, mixed-column energies above 1e-8, successful refinements, and sharing clean gain above 1e-6. Save every candidate, not only the winner.
- Failure stops the fixed pair before noisy evaluation. It is not a universal negative theorem. Numerical search is not a global geometry certificate.

## Fixed corruption and symmetric decoder policies

- Freeze training-selected encoders. For each model, zero-noise biases are fitted on the calibration split and used for the frozen policy. Under the calibrated policy, optimize both models' biases on that same split at each noise. Test data never select or fit anything.
- Noise reference is `sqrt((Var_train(x1)+Var_train(x2))/2)` with ddof=0. The five standard deviations are that reference times {0,.05,.1,.2,.4}. Noise is independent scalar Gaussian code noise; no image-input or adversarial claim.
- Reuse exact conditional Gaussian ReLU moments and existing continuous-target scalar localization. Weighted calibration gap 1e-7 per model, arithmetic slack 1e-12, at most 20,000 expansions per output, 300 seconds shared calibration budget. Save unresolved cases and ledgers; do not loosen limits after seeing results.
- Primary outcome fixed in advance: calibrated sharing-minus-mono held-out risk at multiplier .4. Secondary outcomes: frozen risk difference and calibrated-minus-frozen policy contrast at .4; the complete five-level curves are descriptive. Do not select a primary level afterward.
- Save individual risks, per-feature and per-image losses, all bias values, calibration gaps, training/calibration losses and selected geometry. Preserve the sign convention: positive difference favors mono.

## Uncertainty and interpretation

- 2,000 paired image bootstrap resamples, NumPy seed 20261007, 95% percentile intervals, with indices and outputs retained. Intervals are conditional on the fitted models and pointwise; no simultaneous curve-level or training-uncertainty claim.
- An interval containing zero is unresolved. A sign-resolved noisy difference does not demonstrate a reversal unless the held-out clean ordering is also resolved in the opposite direction. A positive policy contrast alone does not establish a representation winner.
- Inspect the full fixed grid without extending it. A clean/noisy reversal is evidence for this pair/task/noise only; absence of reversal does not refute the scoped Bernoulli theorem. Report all unfavorable outcomes.

## Reuse, independent review and stopping

The existing `joint_phase_theory_2026-10-06/vision_transfer.py` contains the required numerical routines, but its command-line input preparation currently selects channels from train values. It must **not** be invoked unchanged for externally fixed semantic IDs. A small data adapter should package exactly the two predetermined columns and split indices, preserve provenance and call the existing routines without hidden feature reselection. Independently check the adapter, model orientation, resource identity, per-image loss recomputation and bootstrap pairing before reporting results.

Permit only resource loading plus this one fixed run. No new backbone/SAE training, parameter sweep, pair hunt, metric change, second model or optimizer repair. After the run, integrate actual results and any necessary new mathematics into the existing derivation volume, show plots in chat, update the plan and stop to decide the paper's claim strength. Until the external semantic/provenance prerequisite is met, this protocol stays pending; a larger sample alone would not repair that prerequisite.
