# Broader controlled toy: prescribed clean training results

6 October 2026. Motivation, assumptions and stopping rule were saved before execution in `protocol.md`. This is the eight-feature/four-dimensional fixed-geometry support-bound deliverable from `../joint_phase_theory_2026-10-06/week_plan.md`, not a second model search. The noisy calibration stage has **not** run.

## Reproduce

Run `run_clean_training.py` using a Python environment with NumPy and SciPy. The default output directory must not already exist; use `--output` with a fresh path to preserve this run. The script copies the existing weighted projected-Adam code and its original dependency into the new run's source snapshot, saves settings/environment, verifies the gradient, then executes exactly the five seeds. No optimizer change or favorable checkpoint selection is performed.

## Settings and records

n=8, m=4, independent Bernoulli p=.2, encoder energy 4, importance `2^(-i/4)` for i=0,...,7. All 256 states are enumerated. The same tied-ReLU, free-bias training objective and projected-Adam settings are used: 5,000 steps, learning rate .01, beta1 .9, beta2 .999, epsilon 1e-8. Seeds 0,...,4 are all retained. Mono retains the four highest-importance concepts on orthogonal unit columns and predicts the prior mean for the omitted concepts.

`clean_run_v1` contains immutable source snapshots, settings/environment, exact population arrays, mono baseline, five final dictionaries and biases, every pre-update/final loss/gradient/energy record, 51 weight/bias checkpoints per seed, final optimizer moments, scalar clean-bias candidate ledgers, per-feature losses, P/Q constants and a SHA256 manifest. Each successful run has 5,001 history rows. The five-run training/evaluation stage took approximately four seconds on the recorded environment; this is observed timing, not a forecast of later calibration.

## Prechecks

Population normalization and the analytic mono loss agree to floating precision. A deterministic finite-difference check of all 32 encoder and 8 bias gradient coordinates passed: maximum absolute error `5.96745e-11`, with minimum distance to a ReLU kink `.000286175`. Mono energy is exactly 4 and its weighted clean MSE is `.2514085403153298`.

## Unmodified outcomes

| Seed | Final clean MSE | Fixed-W clean-bias-profiled MSE | Tangent gradient norm | Bias gradient norm | Loss-stability pass | Q/P |
|---:|---:|---:|---:|---:|:---:|---:|
| 0 | .24942832355389924 | .24942832355285616 | .10210466 | 1.3293e-6 | No | 461784.6031 |
| 1 | .35094816966186154 | .3508463837410253 | .13360591 | .007596406 | No | 15.49269636 |
| 2 | .29704022762926996 | .2970402276265881 | .12664724 | 2.3144e-6 | No | 11.29594939 |
| 3 | .3259853695246763 | .32598536933821376 | .22574444 | 1.5441e-5 | No | 11.90185316 |
| 4 | .29824421748567803 | .29824421684204316 | .14711704 | 2.5377e-5 | No | 11.33140388 |

Only seed 0's final iterate improves over mono in clean MSE, by `.00198021676143054`. The other four final iterates are worse. Every seed fails the existing `1e-5` difference-of-last-two-100-step-mean-loss diagnostic. The tangent gradients are materially nonzero. Small bias gradients for several seeds do not certify encoder stationarity. These final dictionaries must not be described as converged or globally optimal.

Some earlier recorded losses are lower than their final losses, particularly seed 1. Those values and all checkpoints remain available, but no earlier checkpoint is substituted for the prescribed final iterate. There are no nonfinite training failures and no retry or additional seed.

Fixed-geometry clean bias profiling gives very little improvement except seed 1's approximately `.000101786`; it does not repair the encoder or change the training result. Its finite enumeration is global for the scalar piecewise-quadratic clean bias objective, subject to floating precision. It is not global geometry optimization.

## Support bound and its limitations

All five final dictionaries have eight mathematically nonzero columns; no column was thresholded to zero. Their full-support penalty relative to mono is `P=.06285213507883247`.

Q values for seeds 0,...,4 are respectively `29024.148253332703`, `.9737490443682156`, `.7099745368111018`, `.7480568827122501`, `.7122029273791234`. The previously derived support theorem yields a sufficient noisy-MSE ordering at `sigma>Q/P`, under symmetric global bias calibration and its stated fixed-geometry decoder class. This is an asymptotic sufficient bound, not a prediction of a tight empirical crossing.

Seed 0's last two column norms are only `2.59703e-6` and `2.17516e-6`; both reconstruct almost constant prior means on clean data. They remain nonzero in the support theorem, and the inverse column norm in Q makes `Q/P` approximately `461785`. That large scale is part of the result. It cannot be removed by retrospectively treating small columns as exactly omitted features. The other four bound scales are also large relative to the encoder's unit-scale coordinates.

The clean test therefore does not validate robust general clean-training selection. It produces the requested fixed trained dictionaries for a possible direct test of the support bound, while exposing an optimizer-stability and bound-tightness limitation. The exact two-feature global-selection and critical-law results do not inherit these limitations, but they also do not prove that the eight-feature runs are optimal.

## Next decision

Stop this clean stage now, as prescribed. No optimizer schedule adjustment, checkpoint selection, longer training, extra seed, frequency or feature distribution has been launched. Root must review calibration method and runtime budget before the already prescribed noisy evaluations at `0`, `Q/P`, and `2Q/P` on these same dictionaries. Any failed calibration gap or extremely loose bound remains reportable. The nonbinary scope check and eventual real-model transfer are separate, unexecuted stages.

## Bounded repair and independent audits

See repair_protocol.md (saved before execution), repair_outcomes.md and repair_run_v1. All five seeds are retained; none passes the selected-gradient threshold. Independent original and repaired final-output audits are in independent_clean_review_v1 and independent_repair_review_v2. The parsing failure in the first repair audit is documented in independent_repair_review_v1/checker_failure.md. Full loss/trial traces, periodic weight checkpoints and final weights are saved; weights at every step are not saved. The optimizer arm is closed.
