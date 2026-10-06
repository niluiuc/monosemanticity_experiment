# Independent numerical review of the fixed frequency verification

6 October 2026. The student ran the five frequencies in the pre-run verification protocol, after independent approval of the clean-storage theorem. Root checked the saved outputs independently. No additional scientific cases were introduced.

## Verdict and credit

The exact geometry selections, saved risks and plotted numerical crossing diagnostics pass the independent checks. The student correctly preserved all feasible/rejected algebraic candidate records, used the same resources and detector rules, and reported both adverse outcomes and very small effects. In particular, it did not replace the actual decoder with the midpoint detector to obtain a preferred ranking. No scientific output repair was required.

The four sharing selections were independently recovered using all 225 joint nonempty active-state subsets, rather than the student's four ordered regions with 256 joint kink/vertex candidates. The resulting candidate counts were 33, 30, 21 and 21; each construction recovered the same exact root polynomial and objective as the student. The reviewed rational root-isolation backend is shared and disclosed. The p=.40 mono selection agrees with the independently proved theorem.

## Numerical checks

`verify_results.py` verified all 48 raw hashes, all 150 primary detector/model/noise rows, all 1,200 plotted formula values, and the six saved Brent brackets/residuals. It independently computed scalar-latent noise probabilities, sixteen-subset fixed-bias minima, encoder energy, and decoder MSE by direct quadrature.

- Maximum bias-loss discrepancy: 5.56e-17.
- Maximum detection probability discrepancy: 5.56e-17.
- Maximum plotted risk-difference discrepancy: 1.39e-16.
- Maximum decoder-MSE quadrature discrepancy after checker repair: 1.39e-16.
- Maximum encoder-energy discrepancy: 2.23e-16.
- Maximum independently recomputed crossing residual: 2.32e-14.

All final assertions passed in `verification_results.json`.

## Failed checker and bounded repair

The first independent check failed its aggregate numerical assertion. All geometry, bias, detection and display-curve assertions had already passed. Diagnosis found six decoder-MSE checks with large disagreement: the old unbounded quadrature could miss central Gaussian mass when a weak-column ReLU cutoff lay tens or hundreds of standard deviations away. For example, at p=.375, sigma=.05 it returned zero for a feature with saved MSE .2343468115.

The failed verification source is preserved in `verify_results_initial.py`, and the discrepancies/cut locations are preserved in `verification_initial_failure.json`. `diagnose_quadrature.py` initially had a mismatched parenthesis in its diagnostic-only cutoff expression; this syntax error was corrected before that diagnostic calculated values. No experimental settings or outputs were changed.

The repaired independent checker integrates the Gaussian body over [-12,12], splitting at zero and any ReLU cutoff inside that interval. It bounds the omitted tail using

`|ReLU(mu+sd*z)-b|² <= 2(|mu|+1)²+2sd²*z²`,

the Mills bound `Q(12)<=phi(12)/12`, and the exact Gaussian tail second-moment identity. The largest omitted-tail bound is 3.90e-31, far below the numerical tolerance. This addresses the specific quadrature failure rather than weakening a tolerance or editing the measured values. The complete verification was rerun after this checker change and passed.

## Plots and interpretation

Both original plots were visually inspected. The storage figure shows certified discrete points and the independently proved critical probability; it does not interpolate a global geometry solution. The risk figure evaluates the saved CDF formula and uses separate vertical scales. The exactly-zero p=.40 panel has an unhelpful automatic 1e-17 axis range; a separate presentation copy fixes its axis/label and marks the already saved crossings. The original plot, source and raw hashes remain unchanged, and `../report/plot_provenance.json` records the presentation change.

The numerical display finds two crossings each for p=.05,.35,.375. No crossing was found for p=.20 within the fixed display interval, and p=.40 is identical to mono. Very-low-noise zeros can be finite-precision saturation, so neither strict positivity everywhere nor completeness of root counts is established by these curves. A separate one-case exact noise-sign certificate, if reviewed, can prove existence of multiple roots without certifying their total count.

The completed result is a fixed-load clean-selection theorem plus checked noisy-risk calculations. Full variable-load/importance theory, novelty and real-model transfer remain unresolved. The current finite verification stops here.
