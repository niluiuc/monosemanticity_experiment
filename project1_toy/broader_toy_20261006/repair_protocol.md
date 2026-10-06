# Single bounded optimizer-blocker repair

Recorded before execution, 6 October 2026. Root authorized this one follow-up after reviewing `professor_decision.md`. This changes an optimization implementation, not the scientific model, objective or data. Original fixed-step Adam outputs remain immutable.

## Question

Do the five existing final dictionaries still have unresolved training diagnostics under a direct tangent-gradient descent with an actual-loss decrease check? This resolves a specific blocker in using clean-trained higher-dimensional representations for Project 1. It does not test a new frequency or seek favorable seeds.

## Fixed implementation

- Start from ALL five final encoders and biases in `clean_run_v1/seed_0` through `seed_4`. Never select a checkpoint or rerandomize.
- Same n=8,m=4,p=.2, importances, energy4, exact256-state tied-ReLU objective; joint encoder/bias updates use the existing independently checked weighted gradients.
- Encoder tangent T=gW-<gW,W> W/4. Propose V=W-alpha*T, then normalize V to Frobenius energy4. Bias proposal beta-alpha*gb.
- Initial alpha=.01 at every iteration; Armijo coefficient1e-4. Accept only finite proposals with objective <= current_loss-1e-4*alpha*(||T||^2+||gb||^2).
- At most20 halvings of alpha, therefore at most21 trial evaluations per accepted update. Retain every attempted alpha, proposed loss, target loss, acceptance flag and failure.
- Stop if selected tangent-plus-bias gradient norm <=1e-5, at2000 accepted updates per seed, failed backtracking, nonfinite state, or the hard120-second total execution budget across ALL seeds. No second repair. A selected gradient near a ReLU kink is not a complete nonsmooth stationarity certificate; record minimum absolute preactivation and distinguish that limitation.
- Save initial/final states, all accepted-iterate loss/energy/gradient/kink-distance records,100-step checkpoints plus final state, and every backtracking trial. Report last-two100-step mean-loss change when available, but do not confuse it with gradient stationarity.

## Stopping decision and outputs

Stop after this single prescribed repair regardless of outcomes. Converged models worse than mono remain valid outcomes; positive comparison does not define convergence. A failed/stalled run remains unresolved. No noise calibration, second optimizer, alternative schedule, additional seeds or new toy family is authorized here. Root reviews outputs before any next stage.

Sources, exact input final files/settings and environment are snapshotted before execution into isolated `repair_run_v1`. The mathematical tangent/retraction/Armijo explanation and the Adam preconditioning caveat are saved in an accompanying TeX fragment for root to integrate into the existing derivations PDF.
