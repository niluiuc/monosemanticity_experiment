"""EXPLORATORY (bounded): three independent Bernoulli(p) features in ONE code dimension,
importances (1, eta2, eta3), clean (sigma=0) or noise-trained. Question: is storage a cascade
of transitions, and does the first one sit at the two-feature p_c(eta2)?
w = (cos a, sin a cos b, sin a sin b); biases profiled per output (grid + bounded Brent);
global search: coarse (a,b) grid + Nelder-Mead polish from the best few grid points.
Usage: python fra3.py <eta2> <eta3> <sigma> <p-list>  -> results/three_feature/*.json"""
import json, sys, os, itertools
import numpy as np
from scipy.optimize import minimize_scalar, minimize
from fra2 import relu_moments

X = np.array(list(itertools.product([0, 1], repeat=3)), dtype=float)


C13 = float(os.environ.get("C13", "0"))   # optional correlation between features 1 and 3 (others independent)


def probs(p):
    q = 1 - p; cov = C13 * p * q
    P13 = {(0, 0): q * q + cov, (1, 0): p * q - cov, (0, 1): p * q - cov, (1, 1): p * p + cov}
    return np.array([P13[(int(x[0]), int(x[2]))] * (p if x[1] == 1 else q) for x in X])


def out_loss(wi, m, b, x, pr, sigma):
    mu = wi * m + b
    m1, m2 = relu_moments(mu, np.full_like(mu, abs(wi) * sigma))
    return float(np.sum(pr * (m2 - 2 * x * m1 + x * x)))


def F(ab, p, eta, sigma, bgrid=np.linspace(-2, 2, 401)):
    a, b = ab
    w = np.array([np.cos(a), np.sin(a) * np.cos(b), np.sin(a) * np.sin(b)])
    pr = probs(p); m = X @ w; tot = 0.0
    for i in range(3):
        x = X[:, i]
        mu = w[i] * m[None, :] + bgrid[:, None]
        m1, m2 = relu_moments(mu, np.full_like(mu, abs(w[i]) * sigma))
        L = (pr[None, :] * (m2 - 2 * x[None, :] * m1 + x[None, :] ** 2)).sum(1)
        j = int(np.argmin(L)); lo, hi = bgrid[max(j - 1, 0)], bgrid[min(j + 1, len(bgrid) - 1)]
        r = minimize_scalar(lambda bb: out_loss(w[i], m, bb, x, pr, sigma), bounds=(lo, hi), method="bounded",
                            options={"xatol": 1e-12})
        tot += eta[i] * min(r.fun, L[j])
    return tot


def solve(p, eta, sigma):
    A = np.concatenate([[0.0], np.logspace(-4, np.log10(np.pi / 2), 40)])
    B = np.linspace(-np.pi, np.pi, 49)[:-1]
    cand = []
    for a in A:
        for b in (B if a > 0 else [0.0]):
            cand.append((F((a, b), p, eta, sigma), a, b))
    cand.sort()
    best = cand[0]
    for v, a, b in cand[:4]:
        r = minimize(lambda z: F(z, p, eta, sigma), [a, b], method="Nelder-Mead",
                     options=dict(xatol=1e-9, fatol=1e-14, maxiter=600))
        if r.fun < best[0]:
            best = (r.fun, r.x[0], r.x[1])
    v, a, b = best
    w = [np.cos(a), np.sin(a) * np.cos(b), np.sin(a) * np.sin(b)]
    F_mono = F((0.0, 0.0), p, eta, sigma)
    return dict(p=p, eta=list(eta), sigma=sigma, w=[float(x) for x in w], F=float(v), F_mono=float(F_mono))


if __name__ == "__main__":
    e2, e3, s = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    ps = [float(x) for x in sys.argv[4].split(",")]
    os.makedirs("results/three_feature", exist_ok=True)
    fn = f"results/three_feature/eta{e2}_{e3}_s{s}" + (f"_c13_{C13}" if C13 else "") + ".json"
    rows = json.load(open(fn)) if os.path.exists(fn) else []
    for p in ps:
        if any(abs(r["p"] - p) < 1e-12 for r in rows): continue
        r = solve(p, (1.0, e2, e3), s); rows.append(r)
        json.dump(sorted(rows, key=lambda z: z["p"]), open(fn, "w"), indent=1)
        print(p, np.round(r["w"], 4), "%.3e" % (r["F_mono"] - r["F"]), flush=True)
