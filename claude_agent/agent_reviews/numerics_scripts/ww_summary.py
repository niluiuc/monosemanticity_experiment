"""Summarise well-width results (numerics_results/ww/*.json)."""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(os.path.dirname(HERE), "numerics_results", "ww")
rows = []
for f in sorted(glob.glob(os.path.join(D, "*.json"))):
    rows += json.load(open(f))["rows"]
print("n rows", len(rows))
combos = sorted(set((r["sigma"], r["c"]) for r in rows))
allg = []
worst_v2 = max(rows, key=lambda r: r["v2_minus_mine"])
print("max (v2 - mine) over all rows: %.3e at p=%.10f c=%g s=%g" % (worst_v2["v2_minus_mine"], worst_v2["p"], worst_v2["c"], worst_v2["sigma"]))
for s, c in combos:
    R = sorted([r for r in rows if r["sigma"] == s and r["c"] == c], key=lambda r: r["p"])
    print("\n== sigma=%g c=%g  (%d p-values)" % (s, c, len(R)))
    for r in R:
        ws = [w for w in r["wells"] if abs(w["t"]) < 0.6]      # small/moderate-angle wells
        desc = []
        for w in ws:
            desc.append("t*=%+.5f gain=%+.2e oneside=%.3f basin=%.2f curv=%s belowF0=%s nv2=%d" % (
                w["t"], w["gain_vs_mono"], w["rel_onesided"], min(w["rel_basin"], 99),
                "%.3f" % w["rel_curv"] if w["rel_curv"] else "-", "%.4f" % w["rel_below_F0"] if w["rel_below_F0"] else "-",
                w["n_v2_gridpts_in_basin"]))
            if w["gain_vs_mono"] > 0 and w["t"] == r["best_t"]:
                allg.append((w["rel_onesided"], w["rel_curv"] or np.nan, w["rel_below_F0"] or np.nan, s, c, r["p"], w["t"], w["gain_vs_mono"]))
        print("p=%.5f best_t=%+.5f v2-mine=%+.1e | %s" % (r["p"], r["best_t"], r["v2_minus_mine"], " || ".join(desc)))
print("\nGLOBAL sharing wells (best and below mono): n =", len(allg))
if allg:
    A = np.array([a[:3] for a in allg], float)
    for j, nm in enumerate(["one-sided basin / |t*|", "curvature width / |t*|", "{F<F0} width / |t*|"]):
        k = np.nanargmin(A[:, j]); g = allg[k]
        print("min %-24s = %.4f  at sigma=%g c=%g p=%.5f t*=%+.5f gain=%.2e" % (nm, A[k, j], g[3], g[4], g[5], g[6], g[7]))
