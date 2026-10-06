# Single bounded repair: outcomes and stopping decision

6 October 2026. The settings in `repair_protocol.md` were saved before execution. All five original final dictionaries and biases were used; no seed, checkpoint or restart was selected. The original run remains immutable.

## What ran

The exact existing population gradients drove tangent-projected descent, energy-sphere retraction and joint bias updates. Armijo coefficient was 1e-4, initial step .01, maximum twenty halvings, maximum 2,000 accepted updates per seed, and a hard two-minute total budget. The selected joint-gradient stop was 1e-5. No scientific assumptions or data changed.

All five runs reached **2,000 accepted updates**. Every proposal satisfied actual-loss Armijo decrease at the initial .01 step, so there were exactly **10,000** recorded trials and no rejected backtracking trials. No nonfinite failure or wall-time stop occurred. Each run saved 2,001 accepted-iterate history rows and 21 checkpoints. Full code/settings/input/source snapshots, states, trials and hashes are preserved in `repair_run_v1`. No noisy calibration was executed.

| Seed | Original final loss | Repair final loss | Mono loss | Joint gradient norm | Loss stability | Gradient stop |
|---:|---:|---:|---:|---:|:---:|:---:|
| 0 | .2494283236 | .2362549117 | .2514085403 | .001033501 | Pass | Fail |
| 1 | .3509481697 | .2819765217 | .2514085403 | .03570603 | Fail | Fail |
| 2 | .2970402276 | .2600155475 | .2514085403 | .01560052 | Fail | Fail |
| 3 | .3259853695 | .2505002456 | .2514085403 | .01755209 | Fail | Fail |
| 4 | .2982442175 | .2502017777 | .2514085403 | .01517120 | Fail | Fail |

## Blind interpretation

All losses improved under an actual objective-decrease check. Three of five repaired final dictionaries now beat mono on clean MSE, compared with one of five before repair. This demonstrates that the original unfavorable outcomes were not sufficient evidence of an architectural inability to improve on mono.

Nevertheless **none** reaches the predeclared gradient stopping threshold. Only seed 0 passes the scalar loss-stability check. No repaired dictionary should be labeled a converged or globally optimal trained representation. Finite-step improvement and passing loss stability are weaker claims. Final minimum absolute preactivations were approximately .03487,.00806,.00690,.00007435,.04817; the selected gradients are not explained by an exact zero-score kink at the final iterate. This does not resolve all possible nearby nonsmooth behavior.

Bias profiling at fixed repaired weights gives losses .2362547534,.2819301902,.2597942813,.2504932976,.2501990276. These are numerical global scalar-bias profiles, not new trained encoders or global geometry optima. Neither raw nor profiled outcomes have been substituted silently.

The support penalty P remains .06285213508 for all five. Q/P values are approximately **617.511,12.5307,12.3378,11.4811,13.0136**. Seed 0's weak columns grew from about 2e-6 to about .002 and .0017, but its sufficient bound remains very loose. No tiny column was thresholded away.

## Professor stopping decision

**NO-GO for further optimization in this toy family under the single-repair protocol.** Preserve both original and repaired results, including the unachieved gradient criterion. No second optimizer, longer training, alternative schedule, restart, checkpoint substitution or additional seed is justified here. Close the costly/loose Q/P calibration arm as recommended in `professor_decision.md`.

The exact two-feature global clean geometry and calibrated critical-boundary evidence remain separate and intact. These broader runs are optimization diagnostics and scope limitations, not a successful validation of arbitrary-load training selection. The next paper-critical work should return to the already defined controlled critical mechanism and its one matched-capacity real-model transfer, rather than prolong this supportive toy arm.
