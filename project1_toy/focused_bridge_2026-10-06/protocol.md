# Focused derivation–training bridge

Recorded before new training: 6 October 2026, America/Chicago.

## Question and connection to Project 1

Can a tractable population calculation predict the representation selected by clean training, and then its feature-detection risk under Gaussian code noise? This addresses the missing link between the existing conditional-risk formulas and the intended learned-geometry robustness boundary. It is not a new model family or a completed general phase diagram.

The first eight-feature experiment descriptively found nearly antipodal pairs at lower activation rates. The present two-feature test examines whether assuming an equal-amplitude antipodal pair and a prescribed threshold is justified by training. It also checks the role of importance in training, not only in the evaluation weight.

## Smallest useful setting

- Independent binary concepts, `n=2`, `m=1`.
- Both concepts have the same activation probability, with `p` in `[0.05, 0.20, 0.50]`.
- Importance vectors `[1,1]` and `[1,0.5]`: six cases total.
- Tied encoder/decoder, `h=Wb`, reconstruction `ReLU(W^T W b + bias)`.
- Encoder energy `||W||_F^2=1`. Decoder biases are free as in the existing infrastructure.
- Clean training minimizes the **sum** of importance-weighted population squared reconstruction errors, exactly enumerating all four binary states.
- Actual decoder decisions use strict `reconstruction > 0.5`, equivalently `preactivation > 0.5`.
- Diagnostic centered matched decisions use the previously derived midpoint threshold. They are reported separately and cannot replace an unfavorable actual-decoder result.
- Test corruption is `h + sigma*epsilon`, `epsilon ~ N(0,1)`. Sigma values `[0,0.05,0.15,0.30,0.60]` are fixed before training. Exact Gaussian integration over enumerated binary states is the primary evaluation; numerical simulation may verify it without redefining the result.
- Compare with both one-feature retention codes, each at energy one with its optimal clean bias. Clearly identify which retained feature minimizes the clean training objective. Report both comparisons, without retrospectively picking a noise-specific baseline as the main result.
- Include the fixed equal-amplitude antipodal code `W=[1/sqrt(2),-1/sqrt(2)]` with clean-optimal biases, rather than assuming zero biases.

## Mathematical work

1. Derive the globally optimal bias for **fixed** `W` by the finite ReLU activation-interval decomposition. Include interval boundaries and stationary points; do not assume the whole bias objective is convex.
2. At energy one, use `W=(cos(theta),sin(theta))` up to the irrelevant global sign. Reduce the clean learned-geometry problem to a one-dimensional objective after bias minimization.
3. Prove only the optimality statements actually supported by analysis. A numerical angular grid is a diagnostic, not a global proof. Any unresolved geometry optimality remains explicitly unresolved.
4. Connect the analytically characterized family to exact noisy detection risk. Do not infer a universal load boundary from `n/m=2`.

## Controlled numerical work

- Reuse existing population construction and exact-risk functions; save a snapshot of any reused source. Weighted gradients may be added in the new working directory, with an independent finite-difference check.
- Seeds `0..5` for each of the six cases; retain every final iterate and failure.
- Projected Adam, 4,000 fixed steps, learning rate `0.01`, beta values `0.9,0.999`, epsilon `1e-8`, following the existing solver. No favorable checkpoint selection and no unlogged retry with different settings.
- Save full loss/gradient/energy traces, final weights/biases, settings and environment.
- Loss-stability diagnostic: difference between the last two 100-step mean losses at most `1e-5`. Report this and tangent/bias gradients; passing it is not proof of global convergence.
- Separate angular landscape diagnostic: 361 equally spaced angles from `-pi/2` through `pi/2`, with globally minimized fixed-geometry biases. Include endpoints and the two exact equal-amplitude pair angles as explicit candidates. The grid does not certify the best possible geometry.
- Compare trained loss to this diagnostic and compare trained bias loss to the fixed-geometry analytical optimum. Save all discrepancies.

## Stop / extend criteria

Stop this first test after the six cases, 36 fixed-step trainings, stated landscape diagnostic and independent mathematical/code review. Do not extend to new loads, correlations, pretrained models, optimizer searches or extra seeds in this protocol.

Extension is warranted only if the reviewers establish a correct prediction and the experiment supports the training-to-geometry link, with a clearly identified remaining claim. If biases, geometries or convergence disagree, report the discrepancy and propose the smallest correction rather than widening the sweep. Failure to prove global optimality is a result limitation, not permission to relabel a numerical optimum as a theorem.

## Student–teacher review and records

Two coordinators each supervise a student and an independent teacher. Students derive or implement; teachers acknowledge correct work, criticize specific errors or unsupported claims, and give a bounded direction when necessary. Reviews must cite the checked equations/files/results. Revision is driven by material errors, not obligatory criticism. Concurrent execution is staggered to respect four slots.

**Execution-topology correction (before the student experiments):** the tool actually enforces four total agent threads, including completed threads, and supplies no thread-close operation. It therefore cannot instantiate the requested seven-thread tree. The existing math coordinator thread performs the math student role; the idle toy coordinator later independently reviews that mathematics as teacher. The toy child performs the toy student role; root independently reviews its code/results as teacher. The two student workstreams remain parallel and neither signs off on its own work. This changes the allocation of review roles, not the scientific settings or stopping rule.

New mathematical artifacts belong in `math/`; numerical artifacts in `toy/`. Existing saved runs and research notes are preserved. Root alone appends outcomes to `project1_toy/plan.md`, separating preregistered settings, results, post-run interpretation and unresolved questions. All outputs, including unfavorable ones, are retained. No acceptance or novelty guarantee is attached to this test.
