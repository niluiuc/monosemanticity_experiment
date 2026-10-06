# Project 1 toy experiments: living research record

## Purpose and scope

This file is the shared record of why an experiment is run, what is fixed before it,
what was actually observed, and what follows from those observations. Append dated
entries instead of rewriting inconvenient results. Preserve every run and all seeds.
An analysis change must be identified as a change, with its reason, and must not
replace the original output. The present experiment tests Project 1 only.

**Workflow rule:** no unguided exploration. An extension needs a specific question,
the smallest useful test, and a stopping criterion. No language model, diffusion
model, recursive training, symbolic regression, or large parameter search in this run.

## Broader organizing research question — explicitly adopted 6 October 2026

**Can we derive a joint feature-storage and robustness phase diagram that
recovers compatible known clean-storage phases at zero noise and extends them
to monosemantic-versus-superposed reconstruction-risk boundaries as feature
frequency, importance, compression and noise vary?**

This is the broader Project 1 question and organizing goal. It couples two
predictions within a declared model: what geometry clean training selects,
and where that selected geometry has lower corrupted reconstruction risk than
the matched mono comparator. The focused boundary question below is the
tractable route into this broader goal, not a replacement for it.

The comparison remains `R_super - R_mono`, with one declared reconstruction
outcome, matched width/energy, all discarded-concept losses included, and
separately specified frozen-bias and symmetric-calibration policies. A joint
diagram must distinguish a change in which concepts are stored from a change
in which representation has lower risk.

### Additional mathematics required for the broader goal

1. **Training-selected geometry:** Extend the restricted clean-selection
   results to the parameter family whose phase diagram we actually claim.
   Existing fixed-geometry formulas and selected two-feature optima do not
   solve arbitrary importance ratios or feature-to-dimension ratios.
2. **Robustness boundary:** Compose the selected geometry with the declared
   corrupted reconstruction risk and characterize its zero-difference boundary
   against mono, analytically or through an informative proved bound. Two noisy
   comparison points establish a reversal in one case, not a general boundary.
   The detection-error crossing theorem must not be substituted for this MSE
   boundary.
3. **Recovery of prior special cases:** Identify compatible earlier results,
   match their assumptions/objectives, and show how the broader result reduces
   to them. Our current model does not automatically contain all results of
   Elhage, Zhang or Scherlis; calling the outcome a generalization requires
   the corresponding mathematical reduction.

**Execution rule:** Reuse the existing clean-selection and Gaussian-risk
derivations. First resolve the frequency/noise boundary in the analytically
controlled family; add importance or load only when needed for a specific
claimed extension. Larger-toy and real-model validation can proceed with
prespecified tests, but cannot replace the missing mathematics. General
arbitrary-load theory remains a stretch target until tractability is shown.
This scope statement adds no new theorem or experiment; every subsequent
derivation must also enter the existing companion derivation PDF.

## Current Project 1 question and contribution target — 6 October 2026

This section states the current paper-level target. The protocols and dated
entries below remain historical records; their outputs and unfavorable findings
are not replaced by this clarification. No new experiment or derivation was
performed for this scope update.

- **Our project question:** For representations selected by clean training,
  where is the boundary between monosemanticity and superposition giving lower
  corrupted reconstruction error, and how does it depend on feature frequency,
  importance, compression and noise? The central deliverable is a predictive
  phase diagram of `R_super - R_mono`: positive favors mono, negative favors
  sharing, and zero marks their risk-equality boundary. Feature-storage
  transitions and risk-equality boundaries must be distinguished.
- **Comparison definition:** Use the same declared weighted reconstruction
  MSE for both representations, with matched code width and encoder energy.
  Include the reconstruction loss of concepts omitted by the mono comparator.
  Specify whether decoder biases remain clean-trained or receive symmetric
  noisy-distribution calibration; these are separate risk diagrams, not
  interchangeable measurements. Gaussian code corruption is the current
  controlled setting, not an adversarial or AI-safety guarantee.
- **Related prior results:** Elhage studies clean sparsity/importance-dependent
  storage and superposition phases. Scherlis derives capacity-allocation
  phases in a different solvable model. Zhang's motivating ICLR paper studies
  clean/noisy performance tradeoffs empirically and compares specified mono/poly
  representations theoretically. Later work connects interference, adversarial
  vulnerability and feature retention. The existence of phases or a clean/noisy
  reversal is therefore not our claimed discovery. Exact assumptions and
  reading limits are in `paper_decision_2026-10-06/exact_claim_comparison.md`.
- **Our targeted addition:** Link clean training's selected geometry to the
  same operational corrupted risk and a predicted boundary, with equal-resource
  and decoder-calibration controls. The controls support the phase diagram;
  a single calibrated reversal does not replace it or establish novelty.
- **Completed evidence:** Exact global clean-selection results in restricted
  two-feature settings, a fixed-importance clean storage transition, corrupted
  risk calculations and a dense clean/noisy MSE reversal that survives symmetric
  oracle bias calibration. The separate at-least-two-crossing detection result
  is valid for its specified decoder but is not the same reconstruction-MSE
  diagram. Independent checks and adverse training outcomes are retained.
- **Still required:** A boundary or informative bound across meaningful
  parameter changes, verification of its predictions in a controlled larger
  toy, and one bounded real-representation mechanism test. The full arbitrary-
  load/importance boundary and a strong main-track contribution are not complete.

### Focused contribution versus a genuine generalization

- **Why a sharp dagger:** The immediate missing link is specific: a predictive
  robustness boundary grounded in the geometry actually selected by training,
  rather than another observation that mono helps under noise. This is a
  focused contribution target, not a statement that existing results were weak
  or that our contribution has already been established.
- **Why the current result is not a superset:** Our Bernoulli features, fixed
  energy, tied-ReLU reconstruction and Gaussian code-noise outcome do not
  automatically contain Zhang's classification/separability theory or Scherlis's
  quadratic model. Different assumptions plus additional experiments do not
  prove a mathematical generalization of those results.
- **Broader question we can target:** Can a common, explicitly specified model
  yield a joint feature-storage and robustness phase diagram, recovering
  compatible published clean-storage results in the zero-noise limit and
  extending them to predicted mono-versus-sharing risk boundaries under noise,
  as feature frequency, importance and compression vary?
- **What would justify calling it a superset:** Identify the particular prior
  results being generalized; match their assumptions, objectives and outcomes;
  demonstrate their recovery as special cases; and derive a new regime or
  boundary from the broader result. This can generalize selected compatible
  results, not all existing architectures, tasks or robustness notions.
- **Time-bounded execution:** Keep the joint diagram as the organizing question.
  Start with the existing analytically controlled frequency/noise family at
  fixed load and declared importance. Each necessary extension must resolve a
  missing boundary prediction, with a prespecified minimal test and stopping
  rule. Arbitrary-load or architecture generalization remains a stretch target;
  do not restart the project or launch unrelated toy families to claim breadth.

## Background and motivation

The research direction starts from *Beyond Interpretability: The Gains of Feature
Monosemanticity on Model Robustness* (arXiv:2410.21331; ICLR 2025). That paper motivates
asking whether more interpretable representations can also improve robustness. Its
different experiments use different robustness definitions; it does not establish
a universal adversarial guarantee or the general phase diagram we seek.

Our Project 1 question is more specific: when does representing additional concepts
in a limited space help prediction, and when do interference and corruption make it
costly? The research notes derive exact risks for specified small geometries and a
general upper bound conditional on a dictionary. They do **not** yet characterize
the geometry selected by nonlinear training for arbitrary sparsity and load.

The references for this implementation are Sections 13–18 of
`../output/overleaf/monosemanticity_notes/main.tex`, especially the exact pair risks,
the finite-state detection risk, and the independent-feature interference bound.
Existing independent numerical checks are in `../research_notes/verify_additional.py`.
Those checks verify identities; the new experiment additionally trains an encoder.

## Concepts, model and measurement

Each input b has n independently generated binary concepts, b_i ~ Bernoulli(p).
The concepts are known variables rather than labels inferred from natural data.
For example, a variable could mean wheel present, but no image renderer is used.
All concept importances I_i are 1 in this first experiment. Sparsity s = 1-p.

The encoder stores h = W b in m dimensions. Its tied decoder returns
ReLU(W^T h + beta). We minimize the exact population weighted reconstruction MSE
over all 2^n binary states, with each state's actual Bernoulli probability. We
constrain sum(W^2) = m by projecting the encoder after each Adam update. This is
projected Adam, not a proof of optimality. Decoder biases are unconstrained.

At evaluation time only, h_noisy = W b + sigma*epsilon, epsilon ~ N(0,I_m).
This is **ordinary Gaussian corruption in the code**, not a pixel perturbation,
worst-case attack, training-label noise, safety evaluation, or recursive training.

Let G=W^T W, d_i=G_ii, and z_i=w_i^T h_noisy. We evaluate two distinct detectors:

1. **Matched midpoint detector (the mathematical object):** predict presence when
   z_i > theta_i, theta_i=sum(j!=i)G_ij*p + d_i/2. The true p is supplied, making
   this an oracle-calibrated toy detector, not a learned real-world threshold.
2. **Trained decoder:** predict presence when ReLU(z_i+beta_i) > 0.5, equivalently
   z_i > 0.5-beta_i. Reconstruction MSE also uses the decoder's continuous output.

For either fixed threshold, exact detection error is computed by summing all states
and integrating the one-dimensional projected Gaussian analytically. For sigma>0
and d_i>0, e_i=sum_b P(b)*Phi(-(2b_i-1)*(G_i b-theta_i)/(sigma*sqrt(d_i))).
At sigma=0 we use the stated strict > decision rule directly. At exactly zero
encoder columns the score is deterministic, so use its actual constant decision,
never divide by zero. The matched detector returns absent for a zero column here
(all tested p<=0.5). No column is dropped merely because its norm is small.

For the matched detector only, V_i=sum(j!=i)G_ij^2*p*(1-p) and
B_i=max(j!=i)|G_ij| give the bound
e_i <= exp(-d_i^2 / (8*(V_i + sigma^2*d_i + B_i*d_i/6))).
This is a sufficient upper bound; it may be loose or uninformative. For zero columns
we record the trivial bound 1 and flag the degeneracy. A Gaussian-CDF calculation
can be exact even when a bound is loose. Agreement of the exact risk with simulation
does not alone establish a novel explanation of learned geometry.

## Questions and hypotheses fixed before the run

**Q1: solved pair check.** Do independently generated Gaussian-corruption samples
match the closed-form risks of the two-concept/one-dimension codes? Does the
equal-energy comparison reproduce the analytic risk crossing? A failed formula
check is an implementation or derivation problem, not evidence for the mechanism.

**Q2: learned dictionary check.** Given a trained eight-concept/four-dimension W,
does the exact state-mixture calculation predict observed matched-detector errors?
Does the interference bound upper-bound the exact errors? The same exact mixture
also predicts the trained decoder, using its different threshold.

**Q3: robustness tradeoff in the learned toy.** Can the trained unrestricted code
beat a restricted mono code on clean reconstruction/detection, and lose that
advantage under corruption? This is a hypothesis, not an expected success condition.
We report both detectors even if they disagree. Sparse inputs may favor superposition,
but no seed or activation frequency is guaranteed to do so.

The restricted baseline explicitly stores the first four concepts on orthogonal
unit directions and omits the other four (symmetry makes the choice arbitrary for
equal p and I). It has the same dimensions and total encoder energy as the learned
code. Its decoder reconstructs stored concepts exactly and omitted concepts by
their population mean p. Its clean reconstruction risk is (n-m)*p*(1-p).
Presence decisions for omitted concepts are absent at the fixed 0.5 threshold.
This is an ideal, known-concept baseline within a specified family; it is not an
optimality claim among all encoders or a model trained with identical optimization.

## Prespecified settings (2026-10-05, before executing experiments)

| Item | Setting |
|---|---|
| Pair codes | W=[a,-a] versus [1,0] or [0,1]; equal frequencies and importance |
| Pair detector | Uncentered threshold d_i/2, as in the solved pair; distinct from the centered matched detector used for the trained toy |
| Pair amplitude controls | a=1/sqrt(2), equal total encoder energy; a=1, unequal-energy diagnostic |
| Pair activation rates | 0.05, 0.20, 0.50 |
| Pair noise levels | 0, 0.05, 0.30, 0.80 |
| Pair simulation size | 100,000 inputs per activation rate, shared across codes/noise levels |
| Trained toy | n=8 concepts, m=4 dimensions; total encoder energy 4 |
| Trained activation rates | 0.05, 0.15, 0.30, 0.50 |
| Training initialization seeds | 0, 1, 2, all retained |
| Training objective | Exact population sum over 256 states; unit importance |
| Initialization | Normal encoder rescaled to prescribed energy; zero decoder biases |
| Optimizer | Projected Adam, learning rate 0.01, betas 0.9/0.999, epsilon 1e-8 |
| Training duration | Exactly 4,000 steps; final iterate, no best-checkpoint selection |
| Training precision/runtime | float64, CPU NumPy; one BLAS thread when supported |
| Trained-test noise levels | 0, 0.05, 0.15, 0.30, 0.60 |
| Test simulation size | 50,000 inputs per (activation rate, initialization seed) |
| Evaluation seeds | Separate from initialization; saved explicitly in each run |
| Reuse of test samples | Same inputs and standard Gaussian noise for both models and all sigma at a setting |
| Convergence diagnostic | Last-100-step mean loss versus preceding-100-step mean; abs difference <=1e-5 |
| Weak-column descriptive cutoff | d_i < 0.01*(encoder energy/n); not a drop rule |
| Primary comparison | Learned minus restricted-mono risk, with both detector thresholds reported |

Monte Carlo errors are binary per feature. Save exact and measured errors, false
positive and false negative rates, Wilson 95% intervals, standardized residuals,
and paired differences using common samples. Wilson intervals are marginal, not
simultaneous. A separate familywise Hoeffding tolerance uses alpha=0.001 and a
conservative cap of 5,000 feature comparisons. No independence across features or
noise settings is assumed for the union bound. Error plots retain all seeds.

## Checks required before training

- Analytic reconstruction gradient agrees with finite differences away from ReLU kinks.
- Pair closed forms agree with independent state enumeration, including clean inputs.
- Encoder energy projection is correct and zero-column evaluation is defined.
- General bound is checked against exact risk for independent binary states.
- All finite calculations are saved; failure messages and exit status are retained.

## Artifacts and reproducibility policy

`run_experiments.py` reads `config.json` and writes to a **new** timestamped run folder
under `runs/`. It refuses to overwrite a run. Each run records its configuration,
pre-run plan snapshot, code copies, environment, start/end time, checks, checkpoints,
training traces, per-feature CSVs, paired comparisons, and plot files. Raw test inputs,
standard noise, and binary predictions are saved as compressed NumPy archives (binary
predictions packed without changing the values). No failed seed may be silently removed.
The final manifest stores SHA-256 hashes. Results come from code, not hand-edited tables.

The code uses NumPy/SciPy/Matplotlib, which are already available here; it does not
require PyTorch. Exact population training isolates representation optimization from
finite training-sample variability. It is consequently not a realistic finite-data
training experiment; that limitation is intentional and must remain explicit.

## Stopping criteria and next decision

Run only the pair check and the 12 trained settings. Stop after saving and reviewing
them. If a required check fails, diagnose that specific failure before interpreting
results. If optimization fails the convergence diagnostic, mark that run as such;
do not select a nicer seed or extend training without a new logged protocol.

If exact risks agree with simulation but the bound is loose, report that rather than
claiming a sharp empirical phase boundary. If trained codes do not show the proposed
tradeoff, report the negative result and inspect loss, geometry, and detector thresholds
before proposing any extension. If the first learned test works, the next focused
experiment is changing concept load with the same code and energy controls. Importance
decay and a single real-model transfer are later decisions. Project 2 is not run here.

## Execution log

- 2026-10-05: Protocol written before execution. No experiment outcomes available yet.

## Observations and interpretation

Pending execution. Append measured outcomes and limitations here after reading the
generated artifacts; do not replace the protocol above with retrospective hypotheses.

### 2026-10-05 — Protocol v1 completed and audited

The text above was recorded before execution and is retained as the protocol.
This entry was appended after examining the saved outputs. Full measurements:

- [Generated results](runs/protocol_v1_2026-10-05/results.md).
- [Post-run review and corrected plots](reviews/protocol_v1_2026-10-05/review.md).
- [Training settings and outcomes](runs/protocol_v1_2026-10-05/training_summary.csv).
- [Every feature, model, detector and noise level](runs/protocol_v1_2026-10-05/trained_feature_metrics.csv).
- [Paired comparisons](runs/protocol_v1_2026-10-05/paired_comparisons.csv).
- [Full reproduction audit](audits/protocol_v1_2026-10-05.json).

**Executed:** the 24 pair settings (3 activation rates x 2 amplitudes x 4 noise
levels, each comparing two codes), and all 12 learned settings (4 activation rates
x 3 initialization seeds). No training seed was omitted or replaced. The primary
runner completed in about 17.6 seconds in the recorded CPU environment, excluding
the subsequent reproduction audit and post-run review.

**Checks and reproducibility:** the tied gradient's finite-difference relative
difference was 1.36e-10. Pair closed forms and independently enumerated risks agreed
to 1.11e-16. Across 1,920 trained-model/baseline feature comparisons the largest
absolute Monte Carlo-minus-exact error was 0.00599949; the analogous pair maximum
was 0.00233758. Both were within the prespecified familywise Hoeffding tolerance,
with zero failures. There were no observed violations of the matched-detector
bound. The audit verified 143 artifact hashes, replayed 105,600,000 binary predictions,
and repeated all 12 trainings. Saved weights, biases and training traces reproduced
exactly in this environment (maximum difference 0). This is reproducibility of the
implementation, not independent confirmation of novelty or a real-model result.

**Clean reconstruction:** every learned final iterate had lower clean population
reconstruction MSE than the restricted mono baseline. Example ranges across all
three seeds are 0.109217–0.109264 versus 0.190000 at p=0.05, and 0.979962–0.981213
versus 1.000000 at p=0.50. The advantage is small in the latter regime. These are
sum-of-feature squared errors, distinct from presence-detection errors.

**Detection tradeoff:** at p=0.05, 0.15 and 0.30, all seeds favor the learned code
on clean detection and favor the restricted mono baseline at sigma=0.60, for both
detectors. At sigma=0.30 the two detectors disagree: the matched detector favors
mono while the trained decoder favors the learned code at those activation rates.
Thus the decoder and its threshold materially affect the apparent boundary.
At p=0.50, every tested noise level favors the learned code for every seed and both
detectors. We did not observe a reversal in this dense-input regime within the
tested range; the result cannot be summarized as superposition always hurting
robustness. Nor did we measure a continuous learned-code crossing by sweeping
additional noise values: this run only contains the five specified noise levels.

**Exact fixed-pair crossing:** at p=0.20 the equal-energy crossing is sigma=0.279938913.
The unequal-energy diagnostic (pair energy 2 versus mono energy 1) crosses at
sigma=0.658349502. These roots are from exact specified-code risks and are not
boundaries for an arbitrary trained model. The energy control changes the comparison
substantially and must remain explicit.

**Rare-concept caution:** small unconditional error does not mean the concept is
reliably detected when present. For the learned decoder at p=0.05 and sigma=0.30,
the mean exact false-positive rate is 0.01232832 and false-negative rate is
0.47521680 (averaged over all concepts and seeds). Its favorable total error against
mono at that setting does not mean it retains high recall. The matched detector's
rates at the same setting are 0.13722551 and 0.13534086. Both are reported; neither
is designated the preferred detector retrospectively.

**Bound limitation:** the learned-feature bound-minus-exact-risk slack is between
0.354057 and 0.638304, with median 0.588103 probability units. The bound is valid
in these tests but too loose to locate the observed tradeoff sharply. We should
not claim that this numerical run confirms a tight bound or the original broad
phase-diagram objective.

**Optimization limitation:** 6/12 runs failed the fixed loss-stability diagnostic:
p=0.15 seed 0; p=0.30 seeds 0 and 2; p=0.50 seeds 0, 1 and 2. Some failures are
small and all outcomes are retained, but none should be called proven converged
or globally optimal. Both recent loss changes and final gradient norms are saved.

**Descriptive geometry inspection (post-run, not a preregistered hypothesis test):**
the three lower activation rates show approximately four mutual antipodal pairs,
while the p=0.50 geometry is less pair-specific. Actual cosine summaries for all
seeds are in `reviews/protocol_v1_2026-10-05/geometry_review.json`. This connects the
trained toy to the solved pair family descriptively; it does not prove that the
pair family is globally optimal or that natural-model concepts have this geometry.

**Presentation error and correction:** visual review found that the original
shared-axis risk plot clipped some high-noise curves above approximately 0.30.
The cause was setting only the lower y limit repeatedly before all panels were
plotted. The original plot, code snapshot and numerical outputs remain unchanged.
The corrected view sets a global upper limit after considering every exact and
displayed Monte Carlo value. Use
[the corrected risk plot](reviews/protocol_v1_2026-10-05/plots/learned_vs_mono_risk.png).
The separate review records the repair, including the first failed plotting attempt
caused by a missing parent directory. No measurement was altered for this correction.
An optional NumPy environment-report warning about missing PyYAML did not affect
training or evaluations; no package was installed to silence it.
The current reproduction README specifies Python 3.12 or later after checking the
installed packages' metadata (the pinned SciPy version requires Python >=3.12).
The archived pre-run README's Python 3.11 statement was too broad; this is a
documentation correction, and the actual run used Python 3.12.14 as recorded.

**Conclusion:** the initial toy implementation works, and some regimes show a
noise-dependent tradeoff against the specified mono control. This is not yet the
full sparsity/load/importance phase diagram, a novel theorem on trained geometry,
a real-model validation, or a guarantee of conference acceptance. Detector-dependent
results, the dense-input outcome, loose bounds, and optimization limitations are
part of the result, not material to suppress.

### Next focused plan — proposed, not executed

1. Inspect and resolve optimizer stability with a separately logged, fixed protocol
   applied to all original settings. A smaller or scheduled learning rate is a
   candidate numerical repair; it must be chosen before that run and evaluated by
   reconstruction/convergence diagnostics rather than a preferred robustness result.
   Preserve protocol v1 and compare all seeds. No automatic additional sweep now.
2. Once that check is adequate, vary feature load using this same model family.
   Specify which capacity and energy quantities are held fixed before executing.
   This directly tests a missing axis of Project 1; no new model family is needed.
3. Use the resulting mechanism to select one small real-model demonstration.
   Diffusion, LLMs and recursive training remain unexecuted in this initial stage.

### 2026-10-05 — Direct related-work check: Toy Models of Superposition

Read [Elhage et al. (2022), Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html).
This is the source of the tied encoder/ReLU-decoder family already used in the
research notes and this experiment. It studies sparse inputs, importance, feature
packing, geometric arrangements (including antipodal pairs), and phase changes.
It also contains actual toy adversarial experiments and analytically constructed
feature attacks. Neither antipodal geometry nor a generic superposition/robustness
connection should be presented as a new discovery in protocol v1.

There is a direct metric identity for every stored feature: their feature
dimensionality D_i = ||w_i||^2 / sum_j (normalized(w_i)^T w_j)^2 equals
G_ii^2 / sum_j G_ij^2 = M_i^2. Thus our alignment M is the square root of an
existing feature-dimensionality measure, not a newly invented geometric statistic.
At exactly zero columns our ratio is undefined; a separate convention for absent
features must not be confused with this stored-feature identity.

The protocols are not identical: their active feature amplitudes are continuous
uniform values on [0,1], while protocol v1 uses binary amplitudes; v1 enforces a
fixed total encoder energy and evaluates isotropic Gaussian noise in code space.
Their adversarial experiment perturbs feature inputs. Therefore protocol v1 is an
adaptation, not a full replication or a validation of their adversarial results.

This reading narrows the novelty claim without changing the project direction:
a contribution must establish a specific new quantitative result, such as a
resource-controlled corruption-risk boundary with stated decoder and distribution
assumptions, and show more than known feature packing. Such novelty remains
unverified. The reading does not justify new training runs or rebuilding the model;
the next focused task remains checking optimizer stability before extending load.

### 2026-10-06 — Broader novelty audit and focused derivation–training bridge

The user authorized updates to this living record after the literature audit.
The separate audit is [novelty_audit.md](literature_review/novelty_audit.md), with
[search coverage](literature_review/search_ledger.md) and an
[archived source index](literature_review/source_index.md). It finds substantial
prior coverage of the superposition/noise tradeoff, capacity phases, the squared
alignment metric, and generic sparse-interference/noise bounds. The complete
nonlinear learned-geometry boundary has neither been identified as solved in the
inspected literature nor established by this project. Its novelty remains to be
demonstrated, rather than presumed.

This does not change the Project 1 direction: mathematics -> controlled toy
validation -> eventual real-model transfer, building from monosemanticity.
It sharpens the next question to the missing link from the clean training
objective to geometry and then to corrupted detection risk. The earlier proposed
eight-feature optimizer repair and load sweep remain unexecuted; the smaller
two-feature check takes precedence because it can directly test the derivation
without widening the experiment.

**Pre-run protocol:** [focused_bridge_2026-10-06/protocol.md](focused_bridge_2026-10-06/protocol.md).
The smallest setting is two independent Bernoulli concepts in one code dimension,
encoder energy one, probabilities 0.05/0.20/0.50 and importance vectors [1,1] and
[1,0.5]. The mathematics derives optimal decoder biases for fixed geometry and
reduces clean geometry selection to an angular objective. The experiment runs
36 fixed-step trainings (all six cases, seeds 0..5), checks a separately identified
361-angle landscape diagnostic, and computes exact Gaussian code-noise detection
risks. Both actual decoder and centered matched rules are reported separately.
The optimal-bias supplied antipodal and both mono retention codes are controls.

**Stopping rule:** finish these prespecified cases and independent student/teacher
reviews. Extend only when a correct mathematical prediction survives review and
the trained results support the geometry link. Numerical grids and convergence
diagnostics are not global-optimality proofs. Record failures and unfavorable
outcomes; do not automatically search optimizer settings, add loads or introduce
real models. At this point this entry records the protocol, not a result.

### 2026-10-06 — Focused bridge outcomes and independent reviews

The two student streams completed the fixed protocol. The available tools limited
the team to four total agent threads, so review roles were reused: the math stream
performed its student derivation and an independent agent checked it; the toy
student ran the experiment and root independently checked it. The scientific
settings were unchanged. No student signed off on its own work.

**Mathematics:** [student_derivation.md](focused_bridge_2026-10-06/math/student_derivation.md)
and [teacher_review.md](focused_bridge_2026-10-06/math/teacher_review.md).
Fixed-geometry global bias minimization is proved. Clean-trained equal-pair bias
is p(1+p)/(2(1-p+p^2)) for p<=.5; the actual threshold is .5 minus this bias.
For p=.5 and equal importance, all energy-one rank-one geometries are covered by
the proof: optimal squared column norms are (1+1/sqrt(2))/2 and
(1-1/sqrt(2))/2, with loss (9+2sqrt(2))/48=.2464255651. Both sign sectors attain
it; the equal pair and mono loss .25 are worse. For p=.5 and weights [1,.5],
retaining the important feature alone is globally optimal, with loss .125.
For p<.5 unequal importance, the equal antipodal pair is locally nonstationary.
Global low-p geometry and the full robustness boundary remain unproved.
Correctness has been independently reviewed; novelty has not been established.

**Toy run:** [results.md](focused_bridge_2026-10-06/toy/report_v1/results.md).
All 36 trainings completed in 68.06 seconds total, with all seeds retained.
Twenty-seven pass the loss-stability diagnostic and nine fail; no nonfinite
training failure occurred. Passing loss stability does not imply stationarity.
At low p with unequal importance, every projected-Adam outcome stays near an
equal pair despite substantial tangent gradients and lower grid losses.
Reoptimizing only the final biases closes at most 4.95e-7 loss, so this is chiefly
an encoder-optimization issue. Seed dependence remains at equal importance.
The two detector rules change the apparent noise tradeoff; clean reconstruction
improvement also need not improve binary feature detection.

Root's [independent toy review](focused_bridge_2026-10-06/review/toy_teacher_review.md)
verified 163 hashes, 96 evaluated models and 960 detector/noise rows. All 36
training trajectories reproduced exactly in this environment. Positive-noise
risks agreed with an independent scalar-noise calculation to 6.66e-16.
The review also confirmed strict-threshold rounding instability at p=.5,
weights [1,.5], final seeds 1 and 4: raw algebraic clean weighted detection error
.125 versus direct float64 ReLU error .25. These values are preserved and must
not be claimed as meaningful recovery of the nearly dropped feature.

**Justified bounded follow-up, protocol recorded before execution:**
[followup_protocol.md](focused_bridge_2026-10-06/followup_protocol.md).
This addresses the reviewed optimizer blocker with only two deterministic
one-angle solver diagnostics (p=.05/.20, weights [1,.5]), and attempts an active-
branch mathematical certificate for only the existing p=.20 unequal-importance
case. The model/objective/energy/noise values remain fixed. No broad solver search,
load sweep or pretrained model is authorized by this follow-up. At this entry's
creation, its follow-up outcomes are not yet known.

### 2026-10-06 — Bounded solver follow-up completed and independently checked

The prespecified two-case angle diagnostic is complete. Its
[report](focused_bridge_2026-10-06/toy/angle_diagnostic_results.md),
[raw run](focused_bridge_2026-10-06/toy/run_angle_diagnostic_v1/),
[independent teacher review](focused_bridge_2026-10-06/review/angle_teacher_review.md)
and [verification JSON](focused_bridge_2026-10-06/review/angle_verification.json)
are saved separately from the original projected-Adam run. No original seed,
failure, threshold discrepancy or source snapshot has been changed.

Both cases use importance [1,.5], encoder energy one, the same exact population
reconstruction objective and globally optimized biases at each angle. From the
single prescribed starting angle -pi/4, p=.05 reaches angle -.5745808452382377
after 1,279 accepted updates, loss .017742880541346515 and absolute angle gradient
9.978e-9. The p=.20 case reaches angle -.41625677289385893 after 678 updates,
loss .07775208251629454 and gradient 9.792e-9. Every accepted step is .1;
no halving, extra initialization or new solver configuration is used.
These results resolve the bounded optimizer blocker; a small gradient alone
does not establish global geometry optimality.

Independent checks verified all 21 archived hashes, all 1,959 saved iterates
and all 60 model/detector/noise rows. The reviewer independently enumerated
all sixteen activation subsets for scalar bias minima, evaluated the direct
angle derivative, checked Armijo decrease and energy, and integrated scalar
Gaussian detection probabilities. Maximum discrepancies were 6.94e-18 for
bias minima, 4.17e-17 for angle gradients and 2.78e-16 for detection probabilities.
No numerical correction to the scientific run was needed.

**Unfavorable and mixed results:** lower clean reconstruction loss does not
automatically improve concept detection. At p=.20, the improved mixed code
has lower clean weighted MSE (.07775208) than the mono control (.08), but the
actual trained decoder ties its clean weighted detection error (.10) and is
worse at every positive tested noise level. At sigma .30, the errors are
.159442 versus mono .147790. At p=.05, the code is worse at low noise, but
better at sigma .30 (.058316 versus .072790) and .60 (.223667 versus .227328).
These are only the prescribed noise points, not a proved continuous boundary.
All unrounded values, both mono controls, per-feature errors and the separate
midpoint detector remain in the CSVs. Reconstruction and detection are distinct
tasks, and favorable midpoint results cannot replace the actual decoder.

**Reproduction-only edit:** the working angle runner gained a --output option
after the run so a teammate can use a fresh directory. Its default and refusal
to overwrite existing directories remain unchanged. The original archived
runner and raw hashes were preserved. The --help interface was checked; no
scientific rerun was performed for this CLI edit.

The integrated [focused experiment README](focused_bridge_2026-10-06/README.md)
explains the motivation, formulas, settings, results, evidence and reproduction
commands. The mathematical certificate has its own independent review and
status; it must not be inferred from this numerical solver outcome alone.

### 2026-10-06 — One-case global geometry certificate passed independent review

The bounded mathematical follow-up is complete:
[certificate and derivation](focused_bridge_2026-10-06/math/low_p_certificate.md),
[independent teacher review](focused_bridge_2026-10-06/math/teacher_low_p_review.md),
[independent checks](focused_bridge_2026-10-06/math/teacher_low_p_check_results.json).
This strengthens only the existing p=1/5, importance [1,1/2], two-feature /
one-dimension, energy-one, free-bias tied-ReLU case. It does not retroactively
turn the earlier numerical grid or local solver into a proof.

Up to global sign, the globally selected encoder is
W=(1,t)/sqrt(1+t^2), where the attaining root satisfies
20t^3+175t^2-60t-59=0 and
-.442090239023400245 < t < -.442090239023400243.
The decoder biases are t(5t-1)/(21(1+t^2)) and 1/(5(1+t^2)).
The optimum objective is
(905t^4-320t^3+410t^2+441)/(5250(1+t^2)^2),
with value .077752082516294294514, strictly below either mono retention
control (.08 and .16). The angle diagnostic agrees numerically with this
separately established global population optimum.

The certificate covers all sign/retention sectors, feasible bias vertices,
ReLU kinks, geometry-region endpoints and the omitted infinity mono point.
It compares 256 finite joint bias branches using exact rational root isolation
and objective bounds. The student candidate ledger has 265 distinct feasible
points; the winning upper bound is strictly below every competing lower bound.
No numerical grid is used to establish global optimality.

The independent teacher reproduced the certificate in a fresh directory and
reviewed its completeness and exact-sign arithmetic. A separate construction
enumerated all 225 joint nonempty active-state subsets, obtaining the same
algebraic optimum from 30 distinct feasible candidates. This construction
shares the reviewed SymPy root-isolation/interval backend; it is not represented
as an independent computer-algebra implementation. The original student result
JSON and candidate ledger remained unchanged. No material mathematical repair
was required. The first execution's output-serialization failure and successful
repair remain disclosed in the certificate report.

**Exact detection consequence:** the important concept is correctly detected
in all four clean states, while the weaker concept's maximum clean decoder
reconstruction is strictly below .5. Thus its nonzero stored direction does
not imply detection under the actual decoder rule. The clean weighted detection
error is exactly .10, equal to mono, despite the strictly better reconstruction
objective. The unfavorable positive-noise results in the numerical follow-up
remain observations at the five prescribed noise points; no theorem about every
positive sigma or a continuous crossing is claimed.

**Current status and stopping:** the two-feature training-to-geometry link now
has independently reviewed exact examples and checked noisy-risk calculations.
The general sparsity/load/importance boundary is not complete, publication
novelty is not established, and no real-model transfer or recursive-training
result has been obtained. The next bounded mathematical question is to extend
the certified active branch over a stated range of frequency and importance,
compare competing branches, and derive the specified noise-risk tradeoff.
Do not begin a new optimizer search, load sweep or pretrained-model run merely
because the current tests are complete. Preserve the intended mathematics ->
controlled toy -> real-model research structure and the time constraint.

### 2026-10-06 — Frequency extension authorized and protocol recorded

After the teacher recommendation, the user asked to keep working. The next
bounded question holds importance [1,.5], load two concepts / one dimension,
encoder energy one and the existing objective fixed, and varies only activation
frequency p. The [Stage A protocol](frequency_boundary_2026-10-06/protocol.md)
was saved before the new analysis. It asks for the clean sharing-versus-retention
transition and its connection to the already specified noise risk.

The student derives a candidate local transition pc=(3-sqrt(5))/2; the global
branch comparison and independent teacher review are separate required steps.
The [finite verification protocol](frequency_boundary_2026-10-06/verification_protocol.md)
was saved after this prediction and before executing new numerical cases.
It fixes five p values (.05,.20,.35,.375,.40), existing noise settings and
exact population geometry comparison. No new training campaign is included.
Its execution is gated on the independent mathematical review. At this entry's
creation, the new numerical outcomes are not known.

The user also requested that plots be displayed directly in chat. The standing
workflow now requires inline plots, explanations and bullet-point reports of
what was done and found, including uncertainty and unfavorable outcomes.

### 2026-10-06 — Global clean frequency transition proved and reviewed

Stage A is complete: [derivation](frequency_boundary_2026-10-06/math/derivation.md)
and [independent review](frequency_boundary_2026-10-06/math/teacher_review.md).
For the fixed binary two-feature, one-dimension, energy-one tied-ReLU model
with free biases and importance [1,.5], the global clean transition is
pc=(3-sqrt(5))/2=.3819660112501051518.

For 0<p<pc, an opposite-sign mixed code strictly improves on the best mono
clean reconstruction loss, so every global minimizer stores both concepts.
For pc<=p<=.5, retaining only the important concept is uniquely optimal in
geometry up to global sign; the loss is p(1-p)/2. Equality belongs to the
mono regime. The proof covers both signs, both norm/importance orderings,
competing nonconvex weak-bias minima and zero-column endpoints. It does not
assert a unique explicit sharing geometry at every p below pc.

The student verified 15 symbolic identities and inequalities, and the teacher
independently checked 25 identities including active-subset loss construction.
No algebra repair was required by the review. An initial student checker failure
caused by substituting r^2=ac before expanding squared expressions is preserved;
expanding first fixed the checker without changing assumptions or formulas.
These checks support the algebra; the global theorem follows from the documented
branch-coverage and inequality proof, not a frequency scan.

The separately reviewed [noise endpoint derivation](frequency_boundary_2026-10-06/noise_limits.md)
shows that any fixed genuinely shared code has weighted detection error tending
to .75 at infinite Gaussian code noise, while mono tends to .5+p/2. Their
difference tends to .25-p/2>0 for p<.5. A finite-noise advantage therefore need
not be permanent; multiple crossings are possible. This does not establish a
negative difference at any specific p or count all roots.

The clean storage transition is not automatically the noisy robustness boundary.
The independent review passed before the fixed Stage B numerical execution was
dispatched. At this entry's creation, those new numerical results are not known.

### 2026-10-06 — Finite frequency verification and independent review completed

The fixed [five-case report](frequency_boundary_2026-10-06/toy/results.md)
and [raw archive](frequency_boundary_2026-10-06/toy/run_v1/) are complete.
No new training, frequency/angle sweep or optimizer configuration was introduced.
All four below-transition sharing optima have strictly separated rational value
intervals from every competing distinct candidate and both mono endpoints;
the p=.40 mono selection follows the independently reviewed theorem.

| p | Weak concept encoder energy | Selected clean weighted MSE | Mono MSE |
|---|---:|---:|---:|
| .05 | .295373681287 | .017742880541 | .023750000000 |
| .20 | .163490565429 | .077752082516 | .080000000000 |
| .35 | .002595127216 | .113740582191 | .113750000000 |
| .375 | .000121567823 | .117187402718 | .117187500000 |
| .40 | 0 | .120000000000 | .120000000000 |

These certify selected geometry at five stated points; the continuous clean
transition comes from the separate proof. The advantages near pc are small
(9.42e-6 and 9.73e-8 in MSE) and must not be portrayed as large practical gains.

The same actual-decoder Gaussian-noise rule gives mixed outcomes. At p=.20,
sharing remains worse at every positive primary noise setting despite better
reconstruction. At p=.05, it is worse at low noise and better at .30/.60.
The .35 and .375 cases show small intermediate-noise advantages. At .40,
selected geometry is mono, so all comparisons are identically zero. Both
detectors, both mono controls and all per-feature errors/MSE remain in the CSVs.

The predefined display formula evaluations and Brent brackets identify numerical
crossings at (.2079551941,.6252753374) for p=.05,
(.2698862926,1.0932765901) for p=.35, and
(.1277396994,3.3971473354) for p=.375. No crossing was found for .20 in the
display interval. This does not establish a complete root count or exact signs
at very small positive noise, where Gaussian probabilities can saturate.
The result supports a nonmonotone comparison, rather than assuming one permanent
robust phase after a single crossing.

Root's [independent numerical review](frequency_boundary_2026-10-06/review/teacher_review.md)
passed. It verified all 48 raw hashes, 150 primary risk rows, 1,200 plotted values
and six crossing brackets. An alternative 225-active-subset branch construction
per sharing case recovered the same exact optimum. Maximum detection and plotted
risk discrepancies are 5.56e-17 and 1.39e-16; crossing residuals are below 2.32e-14.
The shared reviewed rational-root backend and SciPy CDF library are disclosed.

**Independent-checker failure, preserved:** the first review failed an MSE
assertion because old unbounded quadrature missed central Gaussian mass at
very distant weak-feature ReLU cutoffs. For p=.375,sigma=.05 it returned zero
instead of the saved .2343468115. The failing source and six mismatches are
retained in the review folder. A diagnostic-script parenthesis typo was repaired
before that script calculated results. Replacing only the independent integrator
with a [-12,12] central-body integral and a Gaussian tail bound yielded agreement
to 1.39e-16, with omitted-tail bound below 3.90e-31. Acceptance thresholds and
experimental outputs were unchanged. The full independent review then passed.

Both original plots were visually inspected. The original exactly-zero .40 panel
has an unhelpful automatic 1e-17 axis scale. A separate [presentation plot](frequency_boundary_2026-10-06/report/actual_risk_difference.png)
labels equality, marks saved crossings and shades negative differences. No
numerical values or original archive files changed; plot provenance is recorded.
Plots are also displayed in chat, as requested.

The bounded one-case exact noise-sign calculation at p=.05,sigma=.30 uses only
an already evaluated setting. Its source and rational bounds are saved; its
independent review is separate. A student tool-usage interruption occurred after
those files were saved; root resumed the exposition and review rather than
discarding the records. At this entry's creation, that certificate's review
is still pending. It must not be inferred from the numerical root plot alone.

### 6 October 2026: exact noise-crossing certificate independently approved

The bounded [noise-sign proof](frequency_boundary_2026-10-06/math/noise_crossings.md)
and [teacher review](frequency_boundary_2026-10-06/math/teacher_noise_sign_review.md)
are now complete. This supersedes the pending review status in the preceding
historical entry. No new training, frequency or noise setting was introduced.

For the globally clean-selected p=1/20 code, the actual-decoder weighted
detection-risk difference from the clean-preferred mono control satisfies:

- Exact clean difference: Delta(0)=1/400>0, with all eight clean threshold gaps strict.
- At the already tested sigma=3/10, exact rational interval arithmetic gives a
  wholly negative enclosure, displayed approximately as
  [-.014474506712828471,-.014474506712749220].
- Exact infinite-noise difference: Delta(infinity)=9/40>0.

Continuity therefore proves **at least two distinct positive noise crossings**,
one in (0,.30) and one in (.30,infinity). This is an existence result for one
fixed selected geometry, not an exact root count, a certificate of the plotted
root locations, or a result for every frequency. It concerns average Gaussian
code-noise detection, not worst-case input attacks or AI safety.

The teacher reproduced the certificate into a fresh directory, independently
checked the geometry/bias mapping and interval/series calculations, and checked
all eight state probabilities at 100-digit precision. All checks passed; the
high-precision reference is a crosscheck and the rational enclosure supplies
the sign proof. Original results remain unchanged. This protocol is complete;
higher load and real-model transfer require their own focused protocol.

### 6 October 2026: verified frequency-milestone delivery

Created `output/Project1_Frequency_Transition_Code_and_Results_2026-10-06.zip`
with 317 files plus its internal delivery manifest (7,217,560 bytes). Before
packaging, all 48 current raw-run hashes and all 184 preceding focused-run
hashes matched their frozen manifests. ZIP integrity and every delivered file
hash passed. The independent-checker failure and corrected verification are
included, as are both mathematics reviews and the exact noise-sign certificate.

Archive SHA-256:
`b9de092c866757ed151f13d244890b2c33e996598c2c13c9bdd9429a0a542bcd`.
The `.sha256.json` sidecar contains every file hash. The earlier delivery ZIP
was not overwritten. The new archive includes a plan snapshot through the
approved crossing proof; this delivery confirmation was appended afterward.
The prior focused-bridge folder is included because the new verifier imports
its reviewed backend. Literature review text/index are included; literature
PDFs remain in the workspace. This packaging run adds no scientific case.

### 6 October 2026: derivation-document and teacher-review requirements

The user requires every new mathematical result to appear with full derivations
in the existing `Superposition_Recursive_Training_Derivations.pdf` and its
editable LaTeX source. Working Markdown proofs alone are insufficient. The
current integration therefore includes the clean-training/bias profiles,
dense-case optima, exact low-frequency selection certificate, global frequency
transition, actual-decoder noise formula, endpoint limits, two-crossing sign
certificate, and verification/tail-bound reasoning. Existing Project 2 content
is preserved; no new Project 2 mathematics or experiment is being introduced.

No further scientific experiment is authorized by this integration step.
The teacher is auditing both proof completeness and whether the results address
the intended Project 1 claim. The necessary remaining gap must be distinguished
from optional exact special cases, and population selection must remain distinct
from optimizer convergence. A project-readiness assessment and document review
will determine the next bounded action.

### 6 October 2026: full derivation volume updated and reviewed

Updated the existing
`output/pdf/Superposition_Recursive_Training_Derivations.pdf` in place.
The 62-page volume now integrates the complete new Project 1 mathematics
in Chapters 7--8: finite bias profiling, trained pair, importance derivative,
dense global optima, exact low-frequency geometry certificate, global clean
frequency transition, actual-decoder Gaussian risks, endpoint and noncommuting
limits, and the rational two-crossing existence proof. Full branch/feasibility
arguments and the computer-assisted certificate method are explained, not
replaced by equation lists or program success flags. Both saved plots are
included with their limits. Existing Project 2 content remains background.

The substantive teacher reviewed global coverage, all sign/norm/importance
orientations, competing weak bias minima, threshold equality, compactness,
certificate completeness, CDF/Taylor/Machin bounds, strict clean gaps, and
continuity. The requested explicit noncommuting-limit derivation was added.
Five further exact substitution checks confirmed the p=1/20 objective,
derivative, biases and branch feasibility. The teacher approved both chapters
and identified the remaining paper-critical scope/novelty/transfer decisions:

- [Document review](frequency_boundary_2026-10-06/math/teacher_document_review.md).
- [Project-readiness assessment](frequency_boundary_2026-10-06/math/teacher_project_readiness.md).

The updated volume preserves all 36 projected-Adam outcomes and their 27/9
loss-stability split, distinguishes stability from stationarity and population
certificates from practical learning, attributes M_i squared to existing
capacity theory, and distinguishes supplied midpoint-pair results from the
trained decoder's noise comparison. The historical eight-week schedule is
labeled as background, not a renewed budget or permission for broad grids.

Compilation passed with no overfull/reference warnings or page-boundary issues.
All-page contact sheets and full-size new mathematical pages/figures were
visually inspected. The portable single-source Overleaf project also compiled;
its normalized typeset text agrees with the updated PDF page by page. Source
ZIP integrity and every archived source-file hash passed. The pre-update PDF
and source are preserved in `tmp/pdfs/derivations_before_20261006/`.

Editable source: `research_notes/volume2.tex`; portable source:
`output/overleaf/research_derivations/main.tex`, with the `figures/` folder
included in `output/overleaf/Superposition_Recursive_Training_Derivations_Source.zip`.
Verification record:
`output/pdf/Superposition_Recursive_Training_Derivations.verification.json`.
PDF SHA-256:
`97c107a2b2d4d43f80245d6699a83dca29566bbdb18d1b1741886dfb1773c9aa`.

No new scientific experiment ran. The completed protocols remain stopped.
Do not accumulate extra toy root counts, precision levels or axes. The next
decision should resolve the exact established claim's novelty and one bounded
real-model transfer within Project 1; the full arbitrary-load/importance
robustness law is not established by this document update.

### 6 October 2026: same-outcome decoder-calibration control

After the retrospective evidence audit and prospective
`paper_decision_2026-10-06/calibration_protocol.md`, the senior reviewer approved
one bounded control at the existing globally solved dense case: p=.5, equal
importance, n=2,m=1, energy one, two relative-sign sharing optima and mono.
Geometry remained frozen; EVERY code received oracle population bias
calibration at sigma .30 and .60, with sigma zero as the clean anchor. No new
training, load/frequency campaign, detection metric or linear experimental arm
was added. Raw sources/settings/protocol/approval are frozen in that run.

The same reconstruction-MSE reversal survives calibration. Sharing MSE is
.3179305136707885 versus mono .31250541096332785 at sigma .30, and
.49113473370400085 versus .4670928069991759 at .60. Positive differences are
.00542510270746065 and .02404192670482495. The clean shared advantage remains
.24642556509887897 versus mono .25. Both relative signs agree to floating
precision. All ten nonzero-column calibrations passed the prescribed numerical
global gap <=1e-8 per feature, with 47--58 expansions; zero columns are exact.
No budget, exclusion or gradient-check failure occurred. Twenty derivative
checks differ by at most 9.1433e-11; all 85 archived hashes match.

This is a floating-point global-gap diagnostic, not an outward-rounded exact
certificate. Independent root Gaussian-quadrature/tail and ledger verification
is required before treating the comparison as a final research claim. Oracle
calibration is not a finite-data transfer result. Larger loads, novel explanatory
scope and real-model validity remain unresolved. The control stops at these
three supplied geometries and three stated noise settings.

Records: `paper_decision_2026-10-06/run_v1/`, `README.md`,
`calibration_results.md`, and the three-setting-only `calibration_control.png`.
The calibration-method TeX fragment is prepared separately for professor review
and integration into the existing derivation volume; that source is not modified
by this numerical step. The next action is independent review and the senior
claim/transfer decision, not another exploratory toy sweep.

### 6 October 2026: completed independent check and paper decision

The calibration control's independent review is complete. All 85 frozen raw
hashes matched. Direct bounded Gaussian integration checked all 36 saved
per-feature frozen/calibrated MSE values; maximum discrepancy was
1.943e-16, with maximum omitted-tail bound 3.913e-31. The checker imports
neither the experiment's Gaussian-moment routine nor its calibration solver.
Its report is paper_decision_2026-10-06/independent_review/results.json.
Curvature constants, interval bounds, excluded tails and active global lower
bounds also passed. No scientific run was repeated or altered.

The reportable result is: under equal latent width and encoder energy,
globally clean-optimal nonlinear sharing improves clean reconstruction, but
its noisy reconstruction disadvantage survives symmetric oracle population
bias calibration in the tied-ReLU decoder class. Sharing-minus-mono MSE is
-.003574434901 clean, +.005425102707 at sigma .30, and +.024041926705 at .60.
These are not adversarial guarantees or a full load-dependent phase diagram.
The qualitative clean/noisy tradeoff is established prior knowledge; exact
clean selection and this readout control strengthen our specific mechanism
claim but do not establish main-track publication novelty.

Senior decision: stop optional toy extensions. Specify ONE bounded real-model
mechanism test with a runnable fixed representation layer, justified feature
basis, matched width/energy, coverage-aware isolation comparator, same held-out
reconstruction outcome, one declared corruption and separate symmetric bias
calibration. No second model or changed metric is automatically authorized
to recover a preferred result. See professor_decision.md for the complete
GO/NO-GO criteria and one-day protocol planning ceiling.

The full Gaussian moments, scalar calibration derivatives, curvature and
infinite-tail bounds, numerical branch-and-bound procedure, sign symmetry,
linear reference derivation and result table are integrated into the existing
Superposition_Recursive_Training_Derivations.pdf, Section 8.11. The volume is
66 pages, compiled and visually checked, with no overfull or unresolved
reference warnings. Its final SHA-256 is
c80ceee2916d4d09599f4e0ecebf5f3f93a6b8c6dceabb5b6dfe38a980aa35dd.
Editable sources remain local. Plot-reproduction code uses only saved rows;
no additional noise evaluations were introduced.
