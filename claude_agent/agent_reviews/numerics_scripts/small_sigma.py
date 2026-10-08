"""Task 2 (sigma -> 0): locate the noise-induced transition (c = 0, eta = .5) with the independent evaluator
for very small sigma, then measure the sharing well's basin at the transition and check fra2_v2 there.
python small_sigma.py <sigma>"""
import os, sys, json, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import indep_eval as ie, well_width as ww, fra2_v2
ie.NB = 261
s = float(sys.argv[1]); pc = ww.PC


def best_share(p):
    g = np.geomspace(1e-7, 0.3, 2500); ts = -g
    v = ie.Fvec(ts, p, 0.0, s, .5); j = int(np.argmin(v))
    t, f = ie.golden_t(lambda x: ie.F1(x, p, 0.0, s, .5), ts[min(j + 1, len(ts) - 1)], ts[max(j - 1, 0)], it=70)
    return (t, f) if f < v[j] else (ts[j], v[j])


pred = 0.8316 * s ** (2 / 3)
lo, hi = 0.8 * pred, 1.3 * pred
sh = lambda e: best_share(pc - e)[1] < ie.F1(0.0, pc - e, 0.0, s, .5) - 1e-18
assert (not sh(lo)) and sh(hi)
for _ in range(22):
    m = 0.5 * (lo + hi)
    if sh(m): hi = m
    else: lo = m
pT = pc - hi
r = ww.analyse(float(pT), 0.0, s, 2e-3)
w = [x for x in r["wells"] if x["t"] < 0 and abs(x["t"]) < 0.3]
v2 = fra2_v2.solve(float(pT), 0.0, s, .5)
out = dict(sigma=s, eps_T=hi, eps_rel_to_pred=hi / pred - 1, p=pT, wells=w, v2_t=v2["t_star"], v2_minus_indep=v2["F_star"] - r["best_F"],
           indep_best_t=r["best_t"], gain=r["F0"] - r["best_F"])
json.dump(out, open(os.path.join(os.path.dirname(HERE), "numerics_results", f"small_sigma_{s}.json"), "w"), indent=1)
print("sigma=%g eps_T=%.6e (%.3f%% vs 0.8316 s^2/3) p_T=%.10f  best t=%+.4e gain=%.2e  v2 t=%+.4e  v2-indep=%+.1e" % (
    s, hi, 100 * (hi / pred - 1), pT, r["best_t"], out["gain"], v2["t_star"], out["v2_minus_indep"]))
for x in w:
    print("  well t*=%+.4e gain=%+.2e one-sided/|t*|=%.3f curv/|t*|=%s barrier at %s  nv2=%d" % (
        x["t"], x["gain_vs_mono"], x["rel_onesided"], x["rel_curv"], (x["tL"], x["tR"]), x["n_v2_gridpts_in_basin"]))
