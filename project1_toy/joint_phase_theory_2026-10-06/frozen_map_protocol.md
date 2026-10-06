# Frozen reconstruction map: execution protocol

Recorded before execution. Question: at clean-selected near-transition geometries, does the predicted critical boundary appear in exact population reconstruction MSE, and how many sign changes does the fixed display grid resolve?

Connection: sections 8.12–8.15 of the derivation PDF predict a crossing proportional to epsilon^(3/2), and at least two frozen-bias crossings sufficiently near the storage transition. The latter is asymptotic, not a claim that every finite case must show two.

Settings: six fixed epsilon values .02,.01,.005,.0025,.001,.0005; p=(3-sqrt(5))/2-epsilon. Importance (1,.5), energy1, n2/m1, independent binary features, tied ReLU, opposite-sign branch, clean biases. Gaussian code noise. Use 70-digit arithmetic; no training or fitting. Evaluate zero and 121 logarithmic sigma points from1e-7 to2. Preserve all732 rows and all720 adjacent positive-grid intervals. Bisect detected sign brackets to relative width1e-5, at most100 iterations. Also evaluate the prescribed critical brackets at .5 and2 times the derived coefficient and gate-scale samples x=.05,10.

Clean geometry: solve the reviewed branch stationarity equation locally; require 70-digit residual <1e-55 and stated branch feasibility. Global clean selection is a separate proof/certificate requirement: this local residual must NOT be labeled a finite global certificate. The existing exact-rational backend cannot be silently applied to irrational p. Independent reviewer is assessing the smallest exact route; pending it, results are conditional on the supplied branch geometry.

Stop after these six cases. Do not add noise points or epsilon values to obtain desirable crossings. A grid interval with same-sign endpoints is explicitly 'no detected bracket', not 'no root'. Preserve prior failed brackets. No calibrated or larger toy is part of this execution.
