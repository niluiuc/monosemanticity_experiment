# Bounded follow-up after independent v1 reviews

Recorded before the follow-up solver runs, 6 October 2026.

## Evidence and question

The mathematics teacher verified a nonzero importance-dependent derivative at
the equal antipodal geometry for p<.5. In v1, projected coordinatewise Adam stays
near that geometry for the unequal-importance cases despite large tangent
gradients. A flat loss trace is therefore not enough to validate geometry
selection. The question is whether a direct solver of the exact profiled angular
objective follows the proven descent direction and reaches a stationary point.

## Smallest solver diagnostic

- Only p=.05 and .20, weights [1,.5], n=2,m=1, encoder energy one.
- One deterministic start per case: theta=-pi/4, W=(cos theta,sin theta), with
  globally minimized fixed-W biases.
- Optimize the clean, weighted population objective after exact bias minimization.
- Compute the angle derivative from the weighted tied gradient and
  dW/dtheta=(-sin theta,cos theta). This is an envelope derivative where the
  minimizing bias branch is differentiable; disclose any encountered ambiguity.
- Armijo descent: initial trial step .1 at every iteration, halve up to 30 times,
  sufficient decrease coefficient 1e-4. No search over optimizer configurations.
- Stop at absolute angle gradient <=1e-8 or at 4,000 iterations. Stop and record
  a failure if no trial step passes. Keep the final stopping iterate, not a
  retrospectively selected checkpoint.
- Save every angle/loss/gradient/bias, accepted step, branch/tie information,
  settings, source snapshot, environment and hash manifest.
- Report both actual-decoder and centered-midpoint exact detection risks and
  decoder MSE at the SAME five noise levels as v1, with both mono controls.
- Compare with the existing prescribed angular grid as a diagnostic; do not add
  angles or treat local stationarity as global optimality. A lower off-grid loss
  is not a new phase theorem.

Stop after these two cases and independent review. Do not launch a full optimizer
campaign, extra seeds, new loads or real models in this follow-up.

## Bounded mathematical certificate

Separately, attempt a global clean-geometry certificate only for the already
tested case p=.20, weights [1,.5], energy one. Use the fixed-bias active-interval
method and finite algebraic branch comparison. Symbolic algebra is permitted as
a checking tool; symbolic-regression fitting is not used. Exact algebraic roots
or proved isolating intervals are acceptable. Numerical scans alone are not a
certificate. If a complete certificate is not tractable, stop with the proven
branch result and explicit missing comparison rather than widening scope.

Mathematics student and independent teacher use separate files under math/.
Toy student and root teacher preserve v1 and write separate solver-diagnostic
artifacts under toy/. Root alone updates plan.md. Both streams remain in the
existing Project 1 direction; neither correctness nor this follow-up establishes
publication novelty.
