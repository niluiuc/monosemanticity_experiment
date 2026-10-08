"""Adversarial test of the grid floor (fra2_v2 log grid starts at 1e-5): correlation-induced wells
with t* < 1e-5.  For each (p, sigma, sign c) we scan |c| on a log grid, locate t* with the independent
evaluator on a micro grid in [0, 1e-3], and report fra2_v2.solve's shortfall F_v2 - F_true."""
import os, sys, json, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie, fra2_v2
ie.NB = 261
PS = [0.30, 0.37] if len(sys.argv) < 3 else [float(x) for x in sys.argv[2].split(",")]
sigmas = [float(x) for x in sys.argv[1].split(",")]
rows = []
for s in sigmas:
    for p in PS:
        for sg in [-1, 1]:
            for c in sg * np.array([3e-7, 1e-6, 3e-6, 1e-5]):
                c = float(c)
                tt = sg * np.concatenate([[0], np.geomspace(1e-9, 1e-3, 400)])
                # sign convention: the correlation well sits at sign(c)*|t| (checked numerically below)
                v = np.concatenate([ie.Fvec(tt, p, c, s, .5), ie.Fvec(-tt[1:], p, c, s, .5)])
                T = np.concatenate([tt, -tt[1:]])
                j = int(np.argmin(v))
                if 0 < j < len(tt) - 1 or j > len(tt):
                    a, b = sorted([T[j - 1], T[j + 1]]) if j < len(tt) - 1 else sorted([T[j - 1], T[min(j + 1, len(T) - 1)]])
                    t_st, f_st = ie.golden_t(lambda x: ie.F1(x, p, c, s, .5), a, b)
                    if v[j] < f_st: t_st, f_st = T[j], v[j]
                else:
                    t_st, f_st = T[j], v[j]
                r = fra2_v2.solve(p, c, s, .5)
                F0 = v[0]
                rows.append(dict(p=p, c=c, sigma=s, t_true=float(t_st), gain_true=float(F0 - f_st), v2_t=r["t_star"],
                                 v2_shortfall=float(r["F_star"] - f_st)))
                print("s=%g p=%.2f c=%+.1e  t*=%+.3e gain=%.2e  v2 t=%+.3e  shortfall=%+.2e" % (
                    s, p, c, t_st, F0 - f_st, r["t_star"], r["F_star"] - f_st), flush=True)
out = os.path.join(os.path.dirname(HERE), "numerics_results", "tiny_angle_%s.json" % sys.argv[1].replace(",", "_"))
json.dump(rows, open(out, "w"), indent=1)
