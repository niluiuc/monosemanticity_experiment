# Joint phase theory and prescribed checks

The full derivations are in the existing Superposition_Recursive_Training_Derivations.pdf, sections 8.12–8.15. Local editable source: research_notes/joint_phase_derivations_20261006.tex (not uploaded by user instruction).

Read protocol.md first, then week_plan.md and novelty_assessment.md. verification_results.json is the complete four-case raw output. No calibrated critical simulation or larger toy was performed here. The professor's independent derivation review is ../paper_decision_2026-10-06/near_critical_professor_review.md.

Reproduce without overwriting evidence:

```powershell
python verify_critical_law.py --output verification_results_reproduced.json
python plot_saved_checks.py
```

Requires mpmath and matplotlib. Constants are analytically derived, not fitted. The numerical clean solution is local stationarity, not an independent global certificate. Failed finite brackets are described in week_plan.md and retained unchanged in JSON.

## Subsequent fixed map and exact clean certificate

`frozen_run_v1/` contains all732 population risk rows and726 adjacent grid intervals. Five cases have two detected brackets; epsilon=.02 has none on this grid. This is not a complete positive-noise root count.

`clean_global_certificate_v1/` supplies exact Q(sqrt5) brackets for allsix roots, justified by the full global strip theorem in the companion PDF. This adds global selection evidence without changing the original run's pending-certificate label.

`frozen_independent_review_v1/` verifies archived hashes and three prescribed direct-quadrature comparisons for each model. Scripts refuse existing output folders to preserve evidence.

```powershell
python run_frozen_map.py --output frozen_run_reproduced
python certify_strip_roots.py --output clean_global_certificate_reproduced
python verify_frozen_map_independent.py --output frozen_independent_review_reproduced
python plot_frozen_map.py
```

The plotting script reads the original saved run. Its zoomed figure clips the displayed vertical range to[-2,2]; full values remain in population_map.csv. The certificate and independent checker target the original saved map and accept fresh output folders.

## Symmetric critical calibration

`calibrated_run_v1/` archives all12 prescribed endpoint comparisons,70-digit global-loss bounds and feature ledgers. All lower endpoints favor sharing and all upper endpoints favor mono. `calibrated_boundary_run_v1/` preserves every bisection; each stopped when its midpoint sign became unresolved under the unchanged gap target. The saved intervals must be shown as brackets, not exact crossing estimates.

`calibrated_results_professor_review.md`, `calibrated_professor_checks.py` and `calibrated_professor_check_results.json` provide the independent ledger audit. No additional calibrated noise-map or root-count claim is made.

```powershell
python run_critical_calibration.py --review critical_calibration_method_review.md --output calibrated_run_reproduced
python bisect_calibrated_boundaries.py --output calibrated_boundary_run_reproduced
python plot_calibrated_boundaries.py
```

The bisection and plot scripts target the original archived endpoint comparisons. Original run folders refuse overwrite. The full weekly schedule remains in week_plan.md; larger-toy and nonbinary tests are separate subsequent records.
