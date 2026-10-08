# Independent verification findings

This is an audit of the October 7 `claude_agent` work, not a new exploration. The original scripts and saved results were preserved. See `plan.md` for the questions and stopping rules. Audit outputs are unedited raw JSON.

## Reproduce

From the repository root, with NumPy, SciPy, SymPy, mpmath and Matplotlib installed:

```text
python claude_agen_review_bygpt/verify.py
python claude_agen_review_bygpt/resolve_noise_and_real.py
python claude_agen_review_bygpt/plot_checks.py
```

`verify.py` does not import the original research scripts. The follow-up imports the original side-effect-free `fra2` evaluator only to compare the two objective implementations at the same geometry. It uses cached activations; it does not rerun ResNet forward inference. The original optimizer counterexample is preserved in `original_solver_countercheck.json`.

## Findings

- Clean field, branch stiffness and cubic: independently differentiated and confirmed. The original `A_slope=-dc2_dp` is wrong for epsilon=pc-p; consequently its saved `K_pred` and `C_pred` are negative, contrary to its claimed successful signed check. Correct A=.3454915028, K=1.5786893258, C=.2870182162.
- The printed sqrt(h/(3B)) at negative correlation has the wrong sign; the correct radicand is -h/(3B). The saved positive response coefficient itself is correct.
- All 100 sampled local gate cases passed. All 20 archived losses reproduced with maximum discrepancy 4.17e-17. Four independently selected critical responses agree with their leading expressions within .054-.375 percent.
- All 14 high-precision shared-budget path checks passed their gate conditions; maximum finite-k curvature discrepancy 1.36e-8. These are local one-partner instability checks, not full global n-by-m certification.
- **Noise search failure reproduced.** Independent competing-well equality gives epsilon=.0084571128 at sigma=.001 and .0177810065 at sigma=.003. Neither lies inside the original saved bracket; the first miss is small, the second is clear. At p=.3641344889933496, sigma=.003, the original solver selects mono despite an independently exhibited sharing geometry that lowers its own loss by 1.27e-8. Thus a search missed a well; the Gaussian-moment evaluator agrees at the same geometry.
- Four independent noisy curvature checks agree with the stated first-order approximation to at worst 9.74e-6. Uniform tail/remainder proofs and the global noise law are not thereby established.
- Complete saved pair/triple counts reproduce, including the failed pooled displacement result. Sixteen fresh empirical bias fits at saved pair/triple encoders reproduce losses to 1.12e-16. These are compressor calculations on concatenated train/calibration/test arrays, not held-out native-network robustness.
- The 'channel bootstrap' discards resampled multiplicities via a set. Its coverage claim is unsupported. Shared channels also invalidate taking independence in Fisher tests for granted. Two representations are from the same ResNet, not separate model replications.
- Four independently optimized clean encoder cases land inside the archived branch-certificate ranges. There are 60 strictly signed ranges and four zero-straddling ranges. Agreement is not a floating-point enclosure proof or a proof that zero is the exact optimum.
- The minibatch tied-network noisy gradient agrees with finite differences to 9.57e-9. Saved training-seed convergence was not independently rerun.

## Decisions

Keep the corrected clean local mathematics and checked local compression thresholds. Keep real empirical counts with their scope and failed predictions explicit. Do not use the archived noise-transition brackets as verified precision, the set-based resampling intervals as justified 95% confidence intervals, or these real-compressor tests as evidence of native ResNet robustness. No publication novelty claim was verified here.

Complete derivations, corrections and evidence are added to the existing `Superposition_Recursive_Training_Derivations.pdf` and editable source. Original inaccurate files remain as historical evidence; use this audit to identify corrections before manuscript reuse.

## Follow-up justification

The initial numerical check failed to reproduce the sigma=.003 bracket. That specific contradiction triggered two local competing-well root searches, six 55-digit Gaussian-loss evaluations, and one original-solver call at a constructive counterexample. The discrepancy was isolated to encoder search. No other noise levels or toy families were added.

The real checks refitted biases at six correlation-extreme/near-zero pair geometries and four extreme triples. Two neighboring encoder directions per pair were evaluated. This limited rerun confirms objective values; it does not certify a global minimum across all empirical encoder directions.

An initial audit invocation also selected a nonexistent certificate-grid point (.35,.005). The checker stopped with StopIteration. The selection was corrected to the existing (.34,.005) point and the audit rerun; this was an audit-selection error, not evidence about the research model.
