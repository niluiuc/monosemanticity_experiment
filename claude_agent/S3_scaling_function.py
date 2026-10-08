"""S3: explain the measured fixed-encoder crossing eps_fix(sigma) with a scaling function.
At geometry theta(p) (clean-selected, opposite branch) put b1 = sigma*y. For output 1 the gates of states
x1=1 are far from the kink, so to leading order
   L1_noisy/sigma^2 = P00 H(y) + P01 H(y - r) + P10 (y^2 + 1) + P11 ((y - r)^2 + 1),   r = |d|/sigma,
with d = sin(theta)cos(theta) and H(z) = E[ReLU(z+Z)^2] = (z^2+1)Phi(z) + z phi(z).
Calibrated sharing penalty: Pi(r) = min_y [...] - (clean output-1 loss)/sigma^2, mono: v(p) = min_y [p(1+y^2) + q H(y)].
Crossing condition (all else exact): G_clean(p) = sigma^2 [Pi(r) - v(p)] + output-2 noise term eta*sin^2(theta)*sigma^2.
As r -> infinity, Pi -> D and this reduces to the leading law. Compare with the bisection eps_fix."""
import json, glob, numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar, brentq
from fra2 import solve, F, pc_theory

phi = lambda z: np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
H = lambda z: (z * z + 1) * ndtr(z) + z * phi(z)
ETA = 0.5; PC = pc_theory(ETA)


def Pi(r, p):
    q = 1 - p; P11, P10, P01, P00 = p * p, p * q, p * q, q * q
    f = lambda y: P00 * H(y) + P01 * H(y - r) + P10 * (y * y + 1) + P11 * ((y - r) ** 2 + 1)
    noisy = minimize_scalar(f, bounds=(-10, r + 10), method="bounded", options={"xatol": 1e-12}).fun
    clean = r * r * P11 * (P00 + P10) / (P00 + P10 + P11)
    return noisy - clean


def v(p):
    q = 1 - p
    return minimize_scalar(lambda y: p * (1 + y * y) + q * H(y), bounds=(-5, 5), method="bounded", options={"xatol": 1e-12}).fun


def crossing(sigma):
    def g(eps):
        p = PC - eps
        r = solve(p, 0.0, 0.0, ETA); th = r["t_star"]; gain = r["F_mono"] - r["F_star"]
        d = abs(np.sin(th) * np.cos(th))
        pen = sigma ** 2 * (Pi(d / sigma, p) - v(p) + ETA * np.sin(th) ** 2)
        return gain - pen
    return brentq(g, 0.5 * 0.83 * sigma ** (2 / 3), 2.0 * 0.83 * sigma ** (2 / 3), xtol=1e-7)


if __name__ == "__main__":
    out = []
    for f in sorted(glob.glob("results/resultB/bisect_eta0.5000_s*.json")):
        r = json.load(open(f)); s = r["sigma"]
        e_sf = crossing(s); e_fix = float(np.mean(r["eps_fixed_bracket"]))
        out.append(dict(sigma=s, eps_leading=r["eps_pred"], eps_scaling_function=e_sf, eps_fixed_measured=e_fix,
                        eps_fixed_bracket=r["eps_fixed_bracket"], rel_err_leading=e_fix / r["eps_pred"] - 1,
                        rel_err_scaling=e_fix / e_sf - 1))
        print(s, "leading %.5f  scaling-fn %.5f  measured %.5f %s  rel.err leading %+.3f  scaling %+.4f" %
              (r["eps_pred"], e_sf, e_fix, np.round(r["eps_fixed_bracket"], 5), out[-1]["rel_err_leading"], out[-1]["rel_err_scaling"]), flush=True)
    json.dump(out, open("results/resultB/S3_scaling_function.json", "w"), indent=1)
