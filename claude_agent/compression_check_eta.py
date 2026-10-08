"""Bisection of the shared-budget transition for other eta; compare with 1 - sqrt((1-eta)/(1+eta))."""
import sys, json, os, numpy as np
from fra_nm import solve
from fra2 import pc_theory
e = float(sys.argv[1]); pred = 1 - np.sqrt((1 - e) / (1 + e)); fixed = pc_theory(e)
lo, hi = pred - 0.02, pred + 0.02; log = []
for _ in range(6):
    mid = (lo + hi) / 2; r = solve(4, 2, [1, 1, e, e], mid, 0.0, 6); g = r["loss_mono"] - r["loss"]
    log.append(dict(p=mid, gain=g)); print(e, mid, g, flush=True)
    if g > 1e-10: lo = mid
    else: hi = mid
os.makedirs("results/compression", exist_ok=True)
json.dump(dict(eta=e, bracket=[lo, hi], prediction_shared=pred, fixed_norm_pc=fixed, log=log),
          open(f"results/compression/bisection_eta{e}.json", "w"), indent=1)
print("eta", e, "bracket", lo, hi, "pred", pred, "fixed-norm", fixed)
