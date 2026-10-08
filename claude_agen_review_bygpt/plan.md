# Independent verification protocol - 7 October 2026

Question: do the central correlation, noise-trained storage and shared-budget compression claims follow from the actual tied-ReLU objective, and do the reported real-activation counts reproduce?

Connection: these are proposed extensions of Project 1's monosemantic-versus-shared storage/robustness phase diagram. A wrong gate pattern, sign or numerical optimizer can invalidate the claimed mechanism.

Smallest useful checks, specified before running:

- Independently differentiate the clean profiled branches with SymPy. Check field, stiffness, cubic and the sign of the critical slope against saved records.
- Enumerate all clean bias pieces independently; test 100 fixed-seed interior parameter cases and reproduce the 20 archived comparisons. Check four field-response cases and four global-branch certificate points.
- At 55 decimal digits, evaluate the actual piecewise-ReLU objective along the claimed energy-borrowing paths, above/below the stated thresholds for m=2,3,4. Check gate feasibility as well as curvature.
- Independently profile Gaussian-noise bias loss using derivative roots at kink-scaled intervals. Test the two sides of saved coexistence brackets at sigma=.001,.003; test four noisy mono curvatures.
- Recompute pair/triple headline counts from saved per-case results. Inspect dependence, data splits, and the claimed bootstrap rather than treating count agreement as experimental replication.
- Finite-difference the tied-network noisy training gradient on a fixed minibatch.

Stopping: agreement supports only the stated finite checks; it does not upgrade a local expansion to a global theorem or an asymptotic argument to a proof. A contradiction is recorded unchanged and isolated before any repair. No additional model training, scope extension or novelty claim is part of this audit.

Reproduction: run `python claude_agen_review_bygpt/verify.py`. Requires NumPy, SciPy, SymPy and mpmath. Original sources/results are not overwritten. Raw audit results are saved here as results.json.
