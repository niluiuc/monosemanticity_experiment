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
