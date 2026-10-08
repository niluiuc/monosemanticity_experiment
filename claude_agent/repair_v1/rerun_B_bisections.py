"""R2a — recompute the noise-trained transition eps_train(sigma) and the fixed-encoder crossing
eps_fix(sigma) with the repaired search (fra2_v2). Replaces results/resultB/bisect_*.json
(kept as history). Bisection: 30 halvings of [0.3, 2] x leading prediction.
Run from claude_agent/:  python repair_v1/rerun_B_bisections.py <eta> <sigma-list>"""
import os, sys, json, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from fra2_v2 import solve
from fra2 import F, pc_theory, K_C_theory
from result_B_checks import Bcal


def trained_shares(p, s, eta):
    r = solve(p, 0.0, s, eta); return r["F_star"] < r["F_mono"] - 1e-16


def fixed_shares(p, s, eta):
    rc = solve(p, 0.0, 0.0, eta); t = rc["t_star"]
    if abs(t) < 1e-12: return False
    return F(t, p, 0.0, s, eta)[0] < F(0.0, p, 0.0, s, eta)[0] - 1e-16


def bisect(fun, s, eta, pred, n=30):
    pc = pc_theory(eta); lo, hi = 0.3 * pred, 2.0 * pred        # eps: mono at lo, sharing at hi
    assert not fun(pc - lo, s, eta) and fun(pc - hi, s, eta), "initial bracket invalid"
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if fun(pc - mid, s, eta): hi = mid
        else: lo = mid
    return [lo, hi]


if __name__ == "__main__":
    eta = float(sys.argv[1]); sigmas = [float(x) for x in sys.argv[2].split(",")]
    K, C = K_C_theory(eta); bc = Bcal(eta)
    for s in sigmas:
        fn = os.path.join(HERE, "results", f"bisect_v2_eta{eta:.4f}_s{s}.json")
        if os.path.exists(fn): print("exists", fn); continue
        pred = (bc / C) ** (1 / 3) * s ** (2 / 3)
        bt = bisect(trained_shares, s, eta, pred); bf = bisect(fixed_shares, s, eta, pred)
        out = dict(eta=eta, sigma=s, eps_pred=pred, eps_trained_bracket=bt, eps_fixed_bracket=bf,
                   rel_dev_trained=np.mean(bt) / pred - 1, rel_dev_fixed=np.mean(bf) / pred - 1,
                   trained_minus_fixed_rel=np.mean(bt) / np.mean(bf) - 1)
        json.dump(out, open(fn, "w"), indent=1)
        print(json.dumps(out), flush=True)
