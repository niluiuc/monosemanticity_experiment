"""Task 5: empirical checks of certify_global.py: (a) max finite-difference slope of F vs LIP;
(b) optimal clean biases lie in [-sqrt2, 1+sqrt2]; (c) out_min_vec vs independent enumeration (see validate_eval.py)."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, CA); sys.path.insert(0, HERE)
import certify_global as cg, indep_eval as ie
rng = np.random.default_rng(7); mx = 0; bmin, bmax = 9, -9
th = np.linspace(-np.pi / 2, np.pi / 2, 400001)
for k in range(30):
    p = rng.uniform(.15, .45); c = rng.uniform(-.05, .05)
    F = cg.Fvec(th, p, c); sl = np.abs(np.diff(F)) / np.diff(th); mx = max(mx, sl.max())
    X, P = cg.joint(p, c)
    for i in range(2):                     # optimal bias by dense grid on a wide range
        t = rng.uniform(-np.pi / 2, np.pi / 2, 300); w = np.array([np.cos(t), np.sin(t)])
        m = (X @ w).T; o = w[i][:, None] * m; B = np.linspace(-4, 5, 9001)
        G = ie.G_clean(o, np.broadcast_to(B, (300, len(B))), X[:, i], P)
        # among (near-)optimal biases take the one closest to 0 (flat all-off region is degenerate)
        best = G.min(1, keepdims=True); ok = G <= best + 1e-14
        bb = np.where(ok, B, np.nan)
        lo = np.nanmax(np.where(ok, B, -np.inf), 1); hi = np.nanmin(np.where(ok, B, np.inf), 1)
        # the claim: SOME optimal b lies in the box -> check interval [hi(min), lo(max)] intersects box
        inter = (lo >= -np.sqrt(2) - 1e-3) & (hi <= 1 + np.sqrt(2) + 1e-3)
        assert inter.all(), (p, c, i)
        bmin = min(bmin, hi.min()); bmax = max(bmax, hi.max())
print("LIP used = %.3f ; max empirical |dF/dtheta| over 30 (p,c) x 400k angles = %.4f (ratio %.1f)" % (cg.LIP, mx, cg.LIP / mx))
print("optimal-bias box check passed; smallest-optimal-b range over samples: [%.3f, %.3f]" % (bmin, bmax))
