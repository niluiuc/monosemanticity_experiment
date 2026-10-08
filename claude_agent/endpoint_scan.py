"""Locate the critical endpoint c_e(sigma) < 0 of the noise-induced first-order line.
For each (sigma, c) scan p and record the bistable window (p values whose opposite-sign
landscape has two local minima).  Usage: python endpoint_scan.py <sigma> <m1,m2,...>
where c = -m * sigma**(4/3) (the scaling predicted in README §4)."""
import json, sys, os, time
import numpy as np
from landscape import landscape, local_minima, TH
from fra2 import pc_theory, K_C_theory

ETA = 0.5
sigma = float(sys.argv[1])
ms = [float(x) for x in sys.argv[2].split(",")]
pc = pc_theory(ETA)
pstar = pc - 0.8315564147061506 * sigma ** (2 / 3)
ps = np.linspace(pstar - 0.03, pstar + 0.06, 46)
order = np.argsort(TH)
os.makedirs("results/endpoint", exist_ok=True)
for m in ms:
    c = -m * sigma ** (4 / 3)
    fn = f"results/endpoint/s{sigma}_m{m}.json"
    if os.path.exists(fn):
        continue
    t0 = time.time(); rows = []
    for p in ps:
        v = landscape(p, c, sigma)[order]
        mins = local_minima(v)
        rows.append(dict(p=float(p), n_min=len(mins), minima_theta=[float(TH[order][i]) for i in mins]))
    bist = [r["p"] for r in rows if r["n_min"] >= 2]
    out = dict(sigma=sigma, m=m, c=c, p_grid=ps.tolist(), rows=rows,
               bistable_p=[min(bist), max(bist)] if bist else None, secs=time.time() - t0)
    json.dump(out, open(fn, "w"), indent=1)
    print(sigma, m, round(c, 6), "bistable window:", out["bistable_p"], round(out["secs"], 1), "s", flush=True)
