"""Validate indep_eval against (a) brute-force bias grids (1e6 pts), (b) fra2.F, (c) fra2_v2.profile,
(d) certify_global.out_min_vec at sigma=0."""
import os, sys, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie
import fra2, fra2_v2, certify_global as cg

rng = np.random.default_rng(1)
which = sys.argv[1] if len(sys.argv) > 1 else "all"

if which in ("brute", "all"):
    # (a) brute force: 2e6-point bias grid on [-3,3.5] + local golden from best point, few t
    worst = 0
    for trial in range(12):
        p = rng.uniform(0.15, 0.45); c = rng.uniform(-0.05, 0.05); s = rng.choice([0.001, 0.003, 0.01, 0.03, 0.1])
        t = rng.choice([-1, 1]) * 10 ** rng.uniform(-4, 0.1)
        X, P = ie.joint(p, c)
        w = np.array([np.cos(t), np.sin(t)]); m = X @ w
        for i in range(2):
            o = (w[i] * m)[None, :]; si = np.array([abs(w[i]) * s])
            mine = ie.outmin(o, X[:, i], P, si)[0]
            bb = np.linspace(-3, 3.5, 2_000_001)
            vals = np.concatenate([ie.G_noisy(o, bb[None, k:k + 200000], X[:, i], P, si)[0] for k in range(0, len(bb), 200000)])
            j = vals.argmin()
            _, gl = ie.golden_t(lambda b: ie.G_noisy(o, np.array([[b]]), X[:, i], P, si)[0, 0], bb[max(j - 1, 0)], bb[min(j + 1, len(bb) - 1)])
            brute = min(vals.min(), gl)
            worst = max(worst, mine - brute)
            print("p=%.4f c=%+.4f s=%.3f t=%+.3e i=%d  mine-brute=%+.2e" % (p, c, s, t, i, mine - brute))
    print("WORST mine-brute", worst)

if which in ("fra2", "all"):
    # (b)+(c): random parameters, random t (log-uniform small + uniform), compare
    dmax_F, dmax_P = 0, 0; rows = []
    for trial in range(30):
        p = rng.uniform(0.15, 0.45); c = rng.uniform(-0.05, 0.05); s = rng.choice([0, 0.001, 0.003, 0.01, 0.03, 0.1])
        ts = np.concatenate([rng.choice([-1, 1], 6) * 10 ** rng.uniform(-5, -0.5, 6), rng.uniform(-np.pi / 2, np.pi / 2, 4), [0.0]])
        mine = ie.Fvec(ts, p, c, s, 0.5)
        f2 = np.array([fra2.F(t, p, c, s, 0.5)[0] for t in ts])
        pv = fra2_v2.profile(ts, p, c, s, 0.5)
        dF = f2 - mine; dP = pv - mine
        dmax_F = max(dmax_F, np.abs(dF).max()); dmax_P = max(dmax_P, np.abs(dP).max())
        k = np.argmax(np.abs(dF))
        print("p=%.4f c=%+.4f s=%.3f  max|fra2.F-mine|=%.2e (t=%+.3e, signed %+.2e)  max|v2.profile-mine|=%.2e  min(fra2.F-mine)=%.2e"
              % (p, c, s, np.abs(dF).max(), ts[k], dF[k], np.abs(dP).max(), dF.min()))
    print("MAX |fra2.F - mine| =", dmax_F, " MAX |v2.profile - mine| =", dmax_P)

if which in ("cert", "all"):
    dm = 0
    for trial in range(20):
        p = rng.uniform(0.15, 0.45); c = rng.uniform(-0.05, 0.05)
        th = np.concatenate([rng.uniform(-np.pi / 2, np.pi / 2, 2000), rng.choice([-1, 1], 2000) * 10 ** rng.uniform(-7, 0, 2000)])
        a = cg.Fvec(th, p, c); b = ie.Fvec(th, p, c, 0.0, 0.5)
        dm = max(dm, np.abs(a - b).max())
    print("MAX |certify.Fvec - mine| (sigma=0, 80k angles) =", dm)
