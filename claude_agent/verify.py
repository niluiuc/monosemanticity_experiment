"""Task 5 — independent checks of the new solver (none of these reuse solve()'s search logic).
(a) Monte Carlo vs the closed-form noisy loss at random parameters (incl. correlation).
(b) Brute-force 3-D grid over (theta, b1, b2) vs solve() at representative points.
(c) Small-angle stiffness formulas of README §2 vs exact profiled loss.
Writes results/verify.json."""
import json, time
import numpy as np
from fra2 import output_loss, states, solve, F, pc_theory

rng = np.random.default_rng(20261007)
out = {}

# (a) Monte Carlo ------------------------------------------------------------
mc = []
for k in range(8):
    p = rng.uniform(0.15, 0.5); c = rng.uniform(-0.1, 0.1); s = rng.choice([0.0, 0.03, 0.1, 0.3])
    t = rng.uniform(-np.pi / 2, np.pi / 2); b = rng.uniform(-0.5, 0.5, 2); eta = 0.5
    exact = float(output_loss(np.cos(t), b[0], t, 0, p, c, s) + eta * output_loss(np.sin(t), b[1], t, 1, p, c, s))
    X, pr = states(p, c)
    N = 4_000_000
    idx = rng.choice(4, size=N, p=pr); x = X[idx]
    w = np.array([np.cos(t), np.sin(t)]); h = x @ w + s * rng.standard_normal(N)
    y = np.maximum(w[None, :] * h[:, None] + b[None, :], 0)
    per = (y[:, 0] - x[:, 0]) ** 2 + eta * (y[:, 1] - x[:, 1]) ** 2
    est, se = per.mean(), per.std() / np.sqrt(N)
    mc.append(dict(p=p, c=c, sigma=float(s), theta=t, b=b.tolist(), exact=exact, mc=float(est), mc_se=float(se),
                   z=float((est - exact) / se)))
out["monte_carlo"] = mc
print("MC max |z| =", max(abs(r["z"]) for r in mc))

# (b) brute force -------------------------------------------------------------
bf = []
pts = [(pc_theory(0.5) - 0.02, 0.0, 0.0), (0.30, 0.0, 0.03), (0.33, -0.005, 0.03), (0.30, 0.005, 0.0)]
for (p, c, s) in pts:
    r = solve(p, c, s, 0.5)
    tt = np.linspace(-np.pi / 2, np.pi / 2, 1441)
    # refine the brute grid around BOTH the solver optimum and mono, so the comparison is fair
    tt = np.unique(np.concatenate([tt, r["t_star"] + np.linspace(-0.01, 0.01, 81), np.linspace(-0.01, 0.01, 81)]))
    bb = np.linspace(-1.0, 1.5, 1251)
    T = tt[:, None]
    l1 = output_loss(np.cos(T), bb[None, :], T, 0, p, c, s).min(axis=1)
    l2 = output_loss(np.sin(T), bb[None, :], T, 1, p, c, s).min(axis=1)
    tot = l1 + 0.5 * l2
    j = int(np.argmin(tot))
    bf.append(dict(p=p, c=c, sigma=s, solver_theta=r["t_star"], solver_F=r["F_star"], brute_theta=float(tt[j]),
                   brute_F=float(tot[j]), solver_minus_brute=float(r["F_star"] - tot[j])))
    print(bf[-1])
out["brute_force"] = bf

# (c) stiffness formulas (clean, small theta) ---------------------------------
st = []
for (p, c) in [(0.42, 0.0), (0.45, 0.02), (0.45, -0.02), (0.40, 0.0)]:
    q = 1 - p; cov = c * p * q
    P11 = p * p + cov; P10 = p * q - cov; P01 = P10; P00 = q * q + cov
    A_pos = (P01 + P11) * P10 / (P01 + P11 + P10)
    A_neg = P11 * (P10 + P00) / (P11 + P10 + P00)
    h = 2 * 0.5 * cov
    F0 = F(0.0, p, c, 0.0, 0.5)[0]
    for th in [1e-3, -1e-3, 3e-3, -3e-3]:
        kap = (A_pos if th > 0 else A_neg) - 0.5 * p * q
        pred = -h * th + kap * th ** 2
        ex = F(th, p, c, 0.0, 0.5)[0] - F0
        st.append(dict(p=p, c=c, theta=th, exact=ex, predicted_2nd_order=pred, rel_err=abs(ex - pred) / abs(ex)))
out["stiffness"] = st
print("stiffness max rel err", max(r["rel_err"] for r in st))
json.dump(out, open("results/verify.json", "w"), indent=1)
