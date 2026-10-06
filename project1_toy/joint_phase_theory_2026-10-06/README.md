# Joint phase theory and prescribed checks

The full derivations are in the existing Superposition_Recursive_Training_Derivations.pdf, sections 8.12–8.15. Local editable source: research_notes/joint_phase_derivations_20261006.tex (not uploaded by user instruction).

Read protocol.md first, then week_plan.md and novelty_assessment.md. verification_results.json is the complete four-case raw output. No calibrated critical simulation or larger toy was performed here. The professor's independent derivation review is ../paper_decision_2026-10-06/near_critical_professor_review.md.

Reproduce without overwriting evidence:

```powershell
python verify_critical_law.py --output verification_results_reproduced.json
python plot_saved_checks.py
```

Requires mpmath and matplotlib. Constants are analytically derived, not fitted. The numerical clean solution is local stationarity, not an independent global certificate. Failed finite brackets are described in week_plan.md and retained unchanged in JSON.
