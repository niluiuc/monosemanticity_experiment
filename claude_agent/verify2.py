"""Session-2 independent checks: (a) real-pair per-sample Gaussian loss + derivatives vs Monte
Carlo / finite differences; (b) real-pair global optimum vs a brute (theta, b1, b2) grid for 3 pairs
at sigma=0.1; (c) B2 curvature formula vs finite differences at a 4th sigma. -> results/verify2.json"""
import json, numpy as np
import real_pairs as R
from spinodal import kappa0
from fra2 import F
rng = np.random.default_rng(7); out = {}
mu = rng.normal(0, 1, 6); s = 0.3; x = rng.integers(0, 2, 6).astype(float)
L, d1, d2 = R.out_loss_and_derivs(mu, s, x)
Z = rng.standard_normal((2_000_000, 1))
mc = ((np.maximum(mu[None, :] + s * Z, 0) - x[None, :]) ** 2).mean(0)
h = 1e-5
fd1 = (R.out_loss_and_derivs(mu + h, s, x)[0] - R.out_loss_and_derivs(mu - h, s, x)[0]) / (2 * h)
fd2 = (R.out_loss_and_derivs(mu + h, s, x)[1] - R.out_loss_and_derivs(mu - h, s, x)[1]) / (2 * h)
out["loss_mc_max_abs_err"] = float(np.max(np.abs(mc - L))); out["d1_fd_max_err"] = float(np.max(np.abs(fd1 - d1)))
out["d2_fd_max_err"] = float(np.max(np.abs(fd2 - d2)))
X, zf, el = R.load(); Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
P = json.load(open("results/real/pairs.json"))["pairs"]; Ld = {(r["i"], r["j"]): r for r in json.load(open("results/real/landscapes.json"))}
bb = []
for pr in [P[3], P[100], P[180]]:
    X1, X2 = Xn[:, pr["i"]], Xn[:, pr["j"]]
    th = np.linspace(-np.pi / 2, np.pi / 2, 721)[:-1]; bgrid = np.linspace(-1.5, 1.5, 121)
    best = np.inf
    for out_i in (0, 1):
        pass
    w1, w2 = np.cos(th)[:, None], np.sin(th)[:, None]
    tot = 0
    for oi, wi, xi, wt in [(0, w1, X1, 1.0), (1, w2, X2, 0.5)]:
        m = wi * (w1 * X1[None, :] + w2 * X2[None, :]); sd = np.maximum(np.abs(wi) * 0.1, 1e-12)
        Lb = np.stack([R.out_loss_and_derivs(m + b, sd, xi[None, :])[0].mean(1) for b in bgrid], 1).min(1)
        tot = tot + wt * Lb
    k = int(np.argmin(tot)); rec = Ld[(pr["i"], pr["j"])]["rows"]; s01 = [r for r in rec if r["sigma"] == 0.1][0]
    bb.append(dict(i=pr["i"], j=pr["j"], brute_theta=float(th[k]), brute_F=float(tot[k]), solver_theta=s01["theta_star"],
                   solver_F=s01["F_star"], solver_minus_brute=s01["F_star"] - float(tot[k])))
out["real_brute_force"] = bb
fd = []
for p in [0.36, 0.30]:
    s_ = 0.002; F0 = F(0.0, p, 0.0, s_, 0.5)[0]; dl = s_ * 1e-2
    fd.append(dict(p=p, sigma=s_, numeric=(F(-dl, p, 0.0, s_, 0.5)[0] - F0) / dl ** 2, kappa0=float(kappa0(p, 0.5))))
out["B2_check_sigma_0.002"] = fd
json.dump(out, open("results/verify2.json", "w"), indent=1); print(json.dumps(out, indent=1))
