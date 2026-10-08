"""Refined critical-endpoint search c_e(sigma) < 0 (Result C).
For a given (sigma, c): scan p in [p*(sigma), p*(sigma)+0.035] (36 points, 2 processes) and test
whether the exact profiled landscape on theta in [-0.5, 0] (300 log-spaced points down to 1e-5)
has >= 2 local minima. Each call tests ONE c and appends to results/endpoint_refined/s<sigma>.json;
bisection is done across calls (the sandbox caps a call at ~3 min).
Usage: python endpoint_refine.py <sigma> <c>        |   python endpoint_refine.py summary"""
import json, sys, os, glob
import numpy as np
from multiprocessing import Pool
from fra2 import F, pc_theory

ETA = 0.5; PC = pc_theory(ETA)
TH = -np.concatenate([[0.0], np.logspace(-5, np.log10(0.5), 300)])[::-1]
os.makedirs("results/endpoint_refined", exist_ok=True)


def nmin(args):
    p, c, sigma = args
    v = np.array([F(t, p, c, sigma, ETA)[0] for t in TH])
    idx = [k for k in range(len(v)) if (k == 0 or v[k] < v[k - 1] - 1e-15) and (k == len(v) - 1 or v[k] < v[k + 1] - 1e-15)]
    return p, len(idx), [float(TH[k]) for k in idx]


if __name__ == "__main__":
    if sys.argv[1] == "summary":
        for f in sorted(glob.glob("results/endpoint_refined/s*.json")):
            if "firstpass" in f: continue
            r = json.load(open(f)); ins = [t["c"] for t in r["tests"] if t["bistable"]]; outs = [t["c"] for t in r["tests"] if not t["bistable"]]
            lo = min(ins) if ins else None; hi = max([o for o in outs if lo is None or o < lo], default=None)
            print(r["sigma"], "most negative bistable c:", lo, " nearest non-bistable below:", hi)
        raise SystemExit
    sigma, c = float(sys.argv[1]), float(sys.argv[2])
    pstar = PC - 0.8315564147061506 * sigma ** (2 / 3)
    PS = np.linspace(pstar, pstar + 0.035, 36)
    with Pool(2) as pool:
        res = pool.map(nmin, [(p, c, sigma) for p in PS])
    hit = [r for r in res if r[1] >= 2]
    fn = f"results/endpoint_refined/s{sigma}.json"
    rec = json.load(open(fn)) if os.path.exists(fn) else dict(sigma=sigma, p_window=[float(PS[0]), float(PS[-1])], tests=[])
    rec["tests"].append(dict(c=c, bistable=bool(hit), bistable_p=[float(h[0]) for h in hit],
                             example_minima=hit[0][2] if hit else None))
    json.dump(rec, open(fn, "w"), indent=1)
    print(sigma, c, "bistable" if hit else "not bistable", [round(h[0], 4) for h in hit])
