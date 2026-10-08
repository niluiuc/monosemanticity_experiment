"""Same as S3_scaling_function.py but keeping the amplitude offsets a-1 = -sin^2(theta) of the x1=1
states (still treating their gates as fully open): tests whether those terms explain the remaining gap."""
import json, glob, numpy as np
from scipy.optimize import minimize_scalar, brentq
from fra2 import solve, pc_theory
from S3_scaling_function import H, v
ETA = 0.5; PC = pc_theory(ETA)

def Pi2(th, p, s):
    q = 1 - p; P11, P10, P01, P00 = p*p, p*q, p*q, q*q
    d = abs(np.sin(th) * np.cos(th)); s2 = np.sin(th) ** 2
    r, al = d / s, s2 / s
    f = lambda y: P00*H(y) + P01*H(y - r) + P10*((y - al)**2 + 1) + P11*((y - al - r)**2 + 1)
    noisy = minimize_scalar(f, bounds=(-10, r + al + 10), method="bounded", options={"xatol": 1e-12}).fun
    g = lambda b: P00*b*b + P10*(b - s2)**2 + P11*(b - s2 - d)**2
    clean = minimize_scalar(g, bounds=(0, d), method="bounded", options={"xatol": 1e-14}).fun / s**2
    return noisy - clean

def crossing(sigma):
    def g(eps):
        p = PC - eps; r = solve(p, 0.0, 0.0, ETA); th = r["t_star"]
        return (r["F_mono"] - r["F_star"]) - sigma**2 * (Pi2(th, p, sigma) - v(p) + ETA*np.sin(th)**2)
    return brentq(g, 0.4*sigma**(2/3), 1.7*sigma**(2/3), xtol=1e-7)

out = []
for f in sorted(glob.glob("results/resultB/bisect_eta0.5000_s*.json")):
    r = json.load(open(f)); s = r["sigma"]; e2 = crossing(s); m = float(np.mean(r["eps_fixed_bracket"]))
    out.append(dict(sigma=s, eps_scaling_with_amplitude=e2, eps_fixed_measured=m, rel_err=m/e2 - 1))
    print(s, "with amplitude terms %.5f  measured %.5f  rel.err %+.4f" % (e2, m, m/e2 - 1), flush=True)
json.dump(out, open("results/resultB/S3_scaling_function2.json", "w"), indent=1)
