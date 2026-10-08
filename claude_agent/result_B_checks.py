"""Task 7 — the two open steps of Result B.
(1) bisect: precise noise-trained transition eps_train(sigma) [global optimum switches mono<->sharing]
    vs the fixed-encoder calibrated crossing eps_fix(sigma) [encoder frozen at its CLEAN optimum,
    biases re-optimised under noise; = existing calibrated policy]. If re-optimising theta only
    matters at higher order, (eps_train - eps_fix)/eps_fix -> 0 as sigma -> 0.
(2) stiff: curvature of the noisy profiled loss at mono, both signs, F(+-delta) with delta << sigma.
Usage: python result_B_checks.py bisect <eta> <sigma> | stiff <sigma> <p-list>"""
import json, sys, os
import numpy as np
from fra2 import solve, F, pc_theory, K_C_theory
from scipy.special import ndtr
from scipy.optimize import minimize_scalar

os.makedirs("results/resultB", exist_ok=True)


def Bcal(eta):
    p0 = pc_theory(eta); D0 = 1 - p0 + p0**2
    phi = lambda z: np.exp(-z*z/2)/np.sqrt(2*np.pi)
    H = lambda z: (z*z+1)*ndtr(z) + z*phi(z)
    v = minimize_scalar(lambda z: p0*(1+z*z)+(1-p0)*H(z), bounds=(-5, 5), method="bounded",
                        options={"xatol": 1e-12}).fun
    return D0 - v


def sharing_wins_trained(p, s, eta):
    r = solve(p, 0.0, s, eta)
    return r["F_neg"] < r["F_mono"] - 1e-15, r


def sharing_wins_fixed(p, s, eta):
    rc = solve(p, 0.0, 0.0, eta)                      # clean-selected encoder
    t = rc["t_star"]
    if abs(t) < 1e-9:
        return False, dict(theta_clean=t)
    Fs = F(t, p, 0.0, s, eta)[0]; Fm = F(0.0, p, 0.0, s, eta)[0]
    return Fs < Fm, dict(theta_clean=t, F_share=Fs, F_mono=Fm)


def bisect(fun, s, eta, lo_eps, hi_eps, n=11):
    pc = pc_theory(eta)
    lo, hi = lo_eps, hi_eps          # sharing wins at eps=hi (deeper), mono at eps=lo
    for _ in range(n):
        mid = 0.5*(lo+hi)
        win, _ = fun(pc - mid, s, eta)
        if win: hi = mid
        else: lo = mid
    return [lo, hi]


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "bisect":
        eta, s = float(sys.argv[2]), float(sys.argv[3])
        fn = f"results/resultB/bisect_eta{eta:.4f}_s{s}.json"
        if os.path.exists(fn): raise SystemExit("exists")
        K, C = K_C_theory(eta); bc = Bcal(eta); pred = (bc/C)**(1/3)*s**(2/3)
        which = sys.argv[4] if len(sys.argv) > 4 else "both"
        out = dict(eta=eta, sigma=s, pc=pc_theory(eta), C=C, B_cal=bc, eps_pred=pred)
        if which in ("both", "fixed"):
            out["eps_fixed_bracket"] = bisect(sharing_wins_fixed, s, eta, 0.3*pred, 2.0*pred, 9)
        if which in ("both", "trained"):
            out["eps_trained_bracket"] = bisect(sharing_wins_trained, s, eta, 0.3*pred, 2.0*pred, 9)
        json.dump(out, open(fn, "w"), indent=1); print(out)
    elif mode == "stiff":
        s = float(sys.argv[2]); ps = [float(x) for x in sys.argv[3].split(",")]
        rows = []
        for p in ps:
            F0 = F(0.0, p, 0.0, s, 0.5)[0]
            row = dict(p=p, sigma=s)
            for dl in [s*1e-2, s*3e-2]:
                row[f"kappa_minus_d{dl:.1e}"] = (F(-dl, p, 0.0, s, 0.5)[0]-F0)/dl**2
                row[f"kappa_plus_d{dl:.1e}"] = (F(dl, p, 0.0, s, 0.5)[0]-F0)/dl**2
            rows.append(row); print(row, flush=True)
        json.dump(rows, open(f"results/resultB/stiff_s{s}.json", "w"), indent=1)
