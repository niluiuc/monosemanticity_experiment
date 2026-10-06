# Critical calibration: precision and bound implementation

Question: does the predicted critical boundary survive symmetric global bias calibration at the same six supplied geometries? This is the second prescribed policy, not another representation search.

Smallest useful test: the 12 previously prescribed comparisons, sigma = .5 and2 times1.3187498488288778 epsilon^(3/2). Both comparators receive oracle population bias calibration. n2/m1, energy1, independent Bernoulli(pc-epsilon) features and weights(1,.5). No training. Preserve numerical global-loss intervals; certify a sign only if the difference interval excludes zero.

Implementation: existing midpoint Taylor branch-and-bound logic, ported entirely to70 decimal digits with1e-40 slack. Per-feature gap tolerance is total target/(1+.5), where total target=min(1e-10,C epsilon^3/100). Maximum100,000 interval expansions per output. Keep all generated nodes and final active heap. Compare outside half-lines using the existing bounds. Bias domain is [-max(offsets)-12sd-1,1-min(offsets)]. Zero-column mono is exact prior prediction.

Focused efficiency specialization: the existing curvature identity is f''=2 sum P[Phi(mu/sd)-y phi(mu/sd)/sd]. On a bias interval, bound absolute curvature by H=2[1+sum P*y*phi(distance(0,offset+[lo,hi])/sd)/sd]. This is bounded above by the earlier global H and is valid because phi decreases with absolute argument and Phi is between0 and1. This bound changes no risk objective; it avoids needlessly pessimistic bounds far from target-one gate crossings. Its derivation must be added to the companion PDF, and independently reviewed before execution.

Stop at12 comparisons. Only successfully certified critical brackets may be bisected afterward; failed gaps stay unresolved. No recalibration map outside those brackets, no extra epsilon values, no favorable threshold adjustment. High-precision arithmetic with declared slack is a numerical bound check, not rigorous directed-rounding interval arithmetic.
