"""Task 1 (adversarial): fra2.F / fra2_v2.profile pick the bias basin by the argmin of a coarse bias grid
(spacing 0.005 / 0.01) and then polish locally. Where the per-output bias loss has two local minima with
nearly equal values, the wrong basin can be chosen. Locate such angles with the independent evaluator and
compare fra2.F and fra2_v2.profile against it there.  python bias_ties.py <seed> <n_params>"""
import os, sys, json, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie
import fra2, fra2_v2
from scipy.optimize import brentq

rng = np.random.default_rng(int(sys.argv[1])); n = int(sys.argv[2])
B = np.linspace(-3, 3.5, 6501)
worst = []
for trial in range(n):
    p = rng.uniform(.15, .45); c = rng.uniform(-.05, .05); s = float(rng.choice([.001, .003, .01, .03, .1]))
    X, P = ie.joint(p, c)
    ts = np.concatenate([-np.geomspace(1e-4, np.pi / 2, 1500)[::-1], np.geomspace(1e-4, np.pi / 2, 1500)])
    gaps = {0: [], 1: []}
    for i in range(2):
        w1, w2 = np.cos(ts), np.sin(ts)
        m = w1[:, None] * X[None, :, 0] + w2[:, None] * X[None, :, 1]
        wi = (w1 if i == 0 else w2)
        o = wi[:, None] * m
        Gv = np.concatenate([ie.G_noisy(o[k:k + 200], np.broadcast_to(B, (len(o[k:k + 200]), len(B))), X[:, i], P, np.abs(wi[k:k + 200]) * s) for k in range(0, len(o), 200)])
        isl = np.zeros_like(Gv, bool); isl[:, 1:-1] = (Gv[:, 1:-1] < Gv[:, :-2]) & (Gv[:, 1:-1] <= Gv[:, 2:])
        sc = np.sort(np.where(isl, Gv, np.inf), axis=1)
        gaps[i] = sc[:, 1] - sc[:, 0]                  # inf when unimodal
    g = np.minimum(gaps[0], gaps[1])
    # signed gap difference changes sign at a tie: find tie points by sign change of (basin A - basin B) -> use small gaps
    cand = np.where(g < 1e-5)[0]
    dmax = 0.0; tw = None
    for k in cand[:200]:
        t = ts[k]
        for tt in np.linspace(t - 1e-3 * abs(t), t + 1e-3 * abs(t), 9):
            a = fra2.F(tt, p, c, s, .5)[0]; b = ie.F1(tt, p, c, s, .5); v2 = fra2_v2.profile(np.array([tt]), p, c, s, .5)[0]
            d = max(a - b, v2 - b)
            if d > dmax: dmax, tw = d, (float(tt), float(a - b), float(v2 - b))
    worst.append(dict(p=p, c=c, sigma=s, n_near_tie=int(len(cand)), max_excess=dmax, at=tw))
    print("p=%.4f c=%+.4f s=%.3f  near-tie angles=%d  max(fra2.F|v2.profile - indep)=%.2e at %s" % (p, c, s, len(cand), dmax, tw), flush=True)
json.dump(worst, open(os.path.join(os.path.dirname(HERE), "numerics_results", f"bias_ties_seed{sys.argv[1]}.json"), "w"), indent=1)
