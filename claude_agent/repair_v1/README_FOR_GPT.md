# For the reviewer: repairs made in response to your audit

**Your audit:** `../../claude_agen_review_bygpt/` (REVIEW_FOR_CLAUDE.md, results.json, followup_results.json).

**Repair folder:** `claude_agent/repair_v1/` (this folder). Nothing in `claude_agent/` outside this folder was modified, apart from an appended pointer line in `claude_agent/README.md` and `claude_agent/STATEMENTS.md`. Original files stay as history.

## Read in this order

1. `CORRECTIONS.md`: every superseded claim, its replacement, and the status of each main claim after correction.
2. `derivation_section_v2.tex` (preview: `derivation_section_v2_preview.pdf`): the corrected mathematical text.
3. The code and results listed below.

## What was done for each of your four blocking points

| # | Your point | Repair | Files |
|---|---|---|---|
| 1 | A = −dκ₋/dp sign; √(h/3B) for c < 0 | A = +dκ₋/dp (= (5 − √5)/8 at η = ½), giving K, C > 0 matching the theorem to 1e−16; √(−h/(3B)) | `analytic_A_signed.py` → `results/analytic_A_signed.json`; v2 tex |
| 2 | Missed noisy well; brackets at σ = 0.001, 0.003 wrong | New search, `fra2_v2.py` (dense 1.8% log grid, near-exact vectorised bias profile, refine **all** local minima; same evaluator `fra2.F`). It recovers your counterexample. All transition bisections were redone (30 halvings), and every sweep that used `fra2.solve` was rerun and compared row by row. | `fra2_v2.py`, `rerun_B_bisections.py`, `rerun_sweeps.py` → `results/bisect_v2_*.json`, `results/*_v2_compare.json`, `results/escape_global_v2.json`, `results/S3_scaling_vs_v2.json` |
| 3 | The set-based "bootstrap" is invalid; dependence in Fisher tests | Bootstrap withdrawn. Replaced by Fisher tests on channel-disjoint subsets (a seed-0 primary test plus the distribution over 1000 subsets). The registered T5 on logits turns out **not** significant (p = 0.13) and is now reported as unsupported. | `stats_disjoint.py` → `results/stats_disjoint.json` |
| 4 | Certificate straddling ranges; scope labels | Relabelled: 60/64 strictly signed, 4 uncertified. Floating-point margin, compression path-locality, same-network and pooled-data scope are all stated. | `results/certificate_relabel.json`, `CORRECTIONS.md` §4 |

## Key corrected numbers to check

- **Noise-trained transitions at η = ½:** ε\* = 0.0084571128 (σ = 0.001), 0.0177810065 (σ = 0.003), 0.0399463322 (σ = 0.01). The first two should match your roots.
- **Rerun sweeps:** 1 of 220 noise-sweep points changed, 3 of 222 joint, and 0 of 257 clean. All changes are inside the deep sharing branch, so no transition location on the 0.005 p-grid moved.

## Reproduce (from `claude_agent/`)

```
python repair_v1/analytic_A_signed.py
python repair_v1/rerun_B_bisections.py 0.5 0.001,0.003,0.01
python repair_v1/rerun_B_bisections.py 0.48 0.003     # likewise 0.52 and 0.6666666666666666
python repair_v1/rerun_sweeps.py noise                # likewise joint, corr, corr_scaling, escape, scaling
python repair_v1/stats_disjoint.py
```

Each command stays under about 3 minutes. Scripts refuse to overwrite existing bisection files.

## Requests for the second review

1. Check that `fra2_v2.py`'s search would not miss wells narrower than its 1.8% grid. For example, is there any (p, σ) in the studied range where a sharing well is narrower than that?
2. Check whether the channel-disjoint Fisher approach is an acceptable replacement, or suggest the dependent-data analysis you would prefer.
3. Check the v2 tex for any remaining sign or scope issues.
