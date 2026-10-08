"""Task 2: well-width study near the noise-induced transition (eta = 0.5).
For each (sigma, c) and p in p0 + [-0.01, 0.01], p0 = p_c - 0.8316 sigma^(2/3):
  * independent F(t) on a log grid (relative spacing REL) on [1e-6, 0.6] both signs + linear to pi/2,
  * every discrete local min / max refined by golden section (independent evaluator),
  * per non-mono local minimum: t*, gain F0-F*, flanking barriers, basin width, one-sided distances,
    width of {F < F0} component, curvature width, number of fra2_v2 grid points inside the basin,
  * fra2_v2.solve on the same parameters: does it find the same global optimum?
Usage: python well_width.py <sigma> <c> [np=21] [rel=2e-3]  -> ../numerics_results/ww_s<sigma>_c<c>.json"""
import os, sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie
import fra2_v2
from scipy.optimize import brentq

ie.NB = 261
ETA = 0.5
PC = (3 - np.sqrt(5)) / 2
GR = ie.GR


def golden(f, a, b, it=80):
    return ie.golden_t(f, a, b, it)


def analyse(p, c, s, rel):
    lg = np.geomspace(1e-6, 0.6, int(np.log(0.6 / 1e-6) / np.log1p(rel)) + 1)
    pos = np.concatenate([lg, np.linspace(0.6, np.pi / 2, 301)[1:]])
    ts = np.concatenate([-pos[::-1], [0.0], pos])
    v = ie.Fvec(ts, p, c, s, ETA)
    F0 = v[len(pos)]
    f = lambda x: ie.F1(x, p, c, s, ETA)
    k = np.arange(1, len(ts) - 1)
    mins = k[(v[k] <= v[k - 1]) & (v[k] <= v[k + 1])]
    maxs = k[(v[k] >= v[k - 1]) & (v[k] >= v[k + 1])]
    # refine
    rmax = []
    for j in maxs:
        x, fx = golden(lambda t: -f(t), ts[j - 1], ts[j + 1]); rmax.append((x, -fx))
    rmax = [(-np.pi / 2, v[0])] + rmax + [(np.pi / 2, v[-1])]
    tmx = np.array([a for a, _ in rmax]); fmx = np.array([b for _, b in rmax])
    wells = []
    for j in mins:
        if ts[j] == 0.0:
            continue
        x, fx = golden(f, ts[j - 1], ts[j + 1])
        if v[j] < fx: x, fx = ts[j], v[j]
        L = np.where(tmx < x)[0]; R = np.where(tmx > x)[0]
        tL, fL = tmx[L[-1]], fmx[L[-1]]; tR, fR = tmx[R[0]], fmx[R[0]]
        # barrier toward 0 (a max between t* and 0) - if t=0 is in the basin, mono and well are same basin
        h = 1e-4 * max(abs(x), 1e-6)
        curv = (f(x + h) - 2 * fx + f(x - h)) / h ** 2
        depth = min(fL, fR) - fx
        w_curv = 2 * np.sqrt(2 * depth / curv) if curv > 0 and depth > 0 else None
        # {F<F0} component containing x
        wlt = None
        if fx < F0:
            g = lambda t: f(t) - F0
            # walk outward on the grid to find sign changes
            idx = np.searchsorted(ts, x)
            lo = idx - 1
            while lo > 0 and v[lo] < F0: lo -= 1
            hi = idx
            while hi < len(ts) - 1 and v[hi] < F0: hi += 1
            try:
                aL = brentq(g, ts[lo], x, xtol=1e-15) if g(ts[lo]) > 0 else ts[lo]
                aR = brentq(g, x, ts[hi], xtol=1e-15) if g(ts[hi]) > 0 else ts[hi]
                wlt = aR - aL
            except Exception as e:
                wlt = None
        G = np.concatenate([-fra2_v2.GRID[::-1], fra2_v2.GRID[1:]])
        n_v2 = int(((G > tL) & (G < tR)).sum())
        wells.append(dict(t=float(x), F=float(fx), gain_vs_mono=float(F0 - fx), tL=float(tL), tR=float(tR),
                          barrier_depth=float(depth), basin_width=float(tR - tL),
                          rel_basin=float((tR - tL) / abs(x)),
                          rel_onesided=float(min(abs(x - tL), abs(tR - x)) / abs(x)),
                          rel_curv=(float(w_curv / abs(x)) if w_curv else None),
                          width_below_F0=(float(wlt) if wlt is not None else None),
                          rel_below_F0=(float(wlt / abs(x)) if wlt is not None else None),
                          n_v2_gridpts_in_basin=n_v2))
    best = min([(0.0, F0)] + [(w["t"], w["F"]) for w in wells], key=lambda z: z[1])
    r2 = fra2_v2.solve(p, c, s, ETA)
    return dict(p=p, c=c, sigma=s, F0=float(F0), best_t=float(best[0]), best_F=float(best[1]), wells=wells,
                v2_t=r2["t_star"], v2_F=r2["F_star"], v2_minus_mine=float(r2["F_star"] - best[1]),
                n_grid=len(ts))


T_START = time.time()
if __name__ == "__main__":
    s = float(sys.argv[1]); c = float(sys.argv[2])
    npnt = int(sys.argv[3]) if len(sys.argv) > 3 else 21
    rel = float(sys.argv[4]) if len(sys.argv) > 4 else 2e-3
    idx = [int(x) for x in sys.argv[5].split(",")] if len(sys.argv) > 5 else list(range(npnt))
    p0 = PC - 0.8316 * s ** (2 / 3)
    out_dir = os.path.join(os.path.dirname(HERE), "numerics_results", "ww"); os.makedirs(out_dir, exist_ok=True)
    pl = p0 + np.linspace(-0.01, 0.01, npnt)
    for i in idx:
        p = pl[i]
        fn = os.path.join(out_dir, f"ww_s{s}_c{c}_n{npnt}_i{i:03d}.json")
        if os.path.exists(fn): continue
        t0 = time.time()
        r = analyse(float(p), c, s, rel); r["secs"] = time.time() - t0
        rows = [r]
        print("p=%.5f best_t=%+.5f gain=%.3e v2-mine=%+.2e wells=%s" % (
            p, r["best_t"], r["F0"] - r["best_F"], r["v2_minus_mine"],
            [(round(w["t"], 5), round(w["rel_basin"], 3), round(w["rel_onesided"], 3), w["rel_below_F0"] and round(w["rel_below_F0"], 4)) for w in r["wells"]]), flush=True)
        json.dump(dict(sigma=s, c=c, eta=ETA, rel=rel, rows=rows), open(fn, "w"), indent=1)
        if time.time() - T_START > float(os.environ.get("BUDGET", "140")):
            break
