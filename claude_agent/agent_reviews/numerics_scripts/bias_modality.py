"""Task 1: how often is the per-output bias loss multimodal, and does the globally best bias basin ever
jump between adjacent angles (a bias 'tie' where a coarse-grid argmin can pick the wrong basin)?
python bias_modality.py <seed> <n>"""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie, fra2, fra2_v2
rng = np.random.default_rng(int(sys.argv[1])); B = np.linspace(-3, 3.5, 6501)
for trial in range(int(sys.argv[2])):
    p = rng.uniform(.15, .45); c = rng.uniform(-.05, .05); s = float(rng.choice([0.0, .001, .003, .01, .03, .1]))
    X, P = ie.joint(p, c)
    ts = np.concatenate([-np.geomspace(1e-5, np.pi / 2, 3000)[::-1], np.geomspace(1e-5, np.pi / 2, 3000)])
    msg = []
    for i in range(2):
        w = np.cos(ts) if i == 0 else np.sin(ts)
        m = np.cos(ts)[:, None] * X[None, :, 0] + np.sin(ts)[:, None] * X[None, :, 1]; o = w[:, None] * m
        G = np.concatenate([(ie.G_noisy(o[k:k+300], np.broadcast_to(B, (len(o[k:k+300]), len(B))), X[:, i], P, np.abs(w[k:k+300]) * s)
                             if s > 0 else ie.G_clean(o[k:k+300], np.broadcast_to(B, (len(o[k:k+300]), len(B))), X[:, i], P)) for k in range(0, len(o), 300)])
        isl = np.zeros_like(G, bool); isl[:, 1:-1] = (G[:, 1:-1] < G[:, :-2]) & (G[:, 1:-1] <= G[:, 2:])
        nmin = isl.sum(1); bstar = B[G.argmin(1)]
        jumps = np.where(np.abs(np.diff(bstar)) > 0.05)[0]
        worst = 0.0
        for j in jumps[:20]:                       # bisect the jump in t, then compare evaluators at the tie
            a, b = ts[j], ts[j + 1]
            for tt in np.linspace(a, b, 41):
                d1 = fra2.F(tt, p, c, s, .5)[0] - ie.F1(tt, p, c, s, .5)
                d2 = fra2_v2.profile(np.array([tt]), p, c, s, .5)[0] - ie.F1(tt, p, c, s, .5)
                worst = max(worst, d1, d2)
        msg.append("out%d: multimodal at %d/%d angles, best-basin jumps=%d, max excess at jumps=%.1e" % (i + 1, (nmin > 1).sum(), len(ts), len(jumps), worst))
    print("p=%.4f c=%+.4f s=%.3f | %s" % (p, c, s, " | ".join(msg)), flush=True)
