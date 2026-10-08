"""EXPLORATORY compression axis: n Bernoulli(p) features in m dims, clean, tied ReLU, free biases,
total encoder energy ||W||_F^2 = m (one unit per code dimension, matching the two-feature model).
Optional pairwise correlations via a Gaussian-copula-free construction for n=4: feature pairs (1,3)
and (2,4) may carry correlation c (others independent).
Biases are profiled EXACTLY (piecewise-quadratic enumeration over 2^n states).
Global search: structured starts + random starts, each polished by Powell, best kept.
Usage: python fra_nm.py <n> <m> <eta-list> <c13> <p-list> [n_random]"""
import json, sys, os, itertools
import numpy as np
from scipy.optimize import minimize


def joint(n, p, c13=0.0, c24=0.0):
    X = np.array(list(itertools.product([0, 1], repeat=n)), dtype=float)
    q = 1 - p
    def pair(a, b, c):
        cov = c * p * q
        return {(0, 0): q*q + cov, (1, 0): p*q - cov, (0, 1): p*q - cov, (1, 1): p*p + cov}[(a, b)]
    pr = []
    for x in X.astype(int):
        if n == 4:
            pr.append(pair(x[0], x[2], c13) * pair(x[1], x[3], c24))
        else:
            pr.append(np.prod([p if v else q for v in x]))
    return X, np.array(pr)


def out_min(o, t, pr):
    """min_b sum_x pr_x (ReLU(o_x+b) - t_x)^2 exactly (piecewise quadratic)."""
    bps = np.unique(-o)
    cand = list(bps)
    edges = np.concatenate([[-np.inf], bps, [np.inf]])
    for lo, hi in zip(edges[:-1], edges[1:]):
        mid = (lo + hi) / 2 if np.isfinite(lo) and np.isfinite(hi) else (hi - 1 if np.isfinite(hi) else lo + 1)
        on = o + mid > 0
        W = pr[on].sum()
        if W <= 0: continue
        b = (pr[on] * (t[on] - o[on])).sum() / W
        if lo <= b <= hi: cand.append(b)
    vals = [(pr * (np.maximum(o + b, 0) - t) ** 2).sum() for b in cand]
    k = int(np.argmin(vals)); return vals[k], cand[k]


def loss(Wflat, n, m, eta, X, pr):
    W = Wflat.reshape(m, n); W = W * np.sqrt(m) / (np.linalg.norm(W) + 1e-300)
    H = X @ W.T                     # (S, m)
    tot = 0.0
    for i in range(n):
        o = H @ W[:, i]
        tot += eta[i] * out_min(o, X[:, i], pr)[0]
    return tot


def solve(n, m, eta, p, c13=0.0, n_random=12, seed=0):
    X, pr = joint(n, p, c13, c13)
    rng = np.random.default_rng(seed)
    starts = []
    E = np.zeros((m, n)); E[np.arange(m), np.arange(m)] = 1.0; starts.append(E.copy())   # mono (keep first m)
    for k in (0.05, 0.2, 0.4):
        for sgn in (-1, 1):
            S = E.copy()
            for j in range(m, n): S[(j - m) % m, j] = sgn * k                              # decomposed partner start
            starts.append(S)
    for _ in range(n_random): starts.append(rng.normal(size=(m, n)))
    best = None
    for S in starts:
        r = minimize(loss, S.ravel(), args=(n, m, eta, X, pr), method="Powell",
                     options=dict(xtol=1e-9, ftol=1e-13, maxiter=20000, maxfev=40000))
        if best is None or r.fun < best[0]:
            best = (r.fun, r.x)
    W = best[1].reshape(m, n); W = W * np.sqrt(m) / np.linalg.norm(W)
    return dict(n=n, m=m, eta=list(eta), p=p, c13=c13, loss=float(best[0]), W=W.tolist(),
                loss_mono=float(loss(E.ravel(), n, m, eta, X, pr)))


if __name__ == "__main__":
    n, m = int(sys.argv[1]), int(sys.argv[2]); eta = [float(x) for x in sys.argv[3].split(",")]
    c13 = float(sys.argv[4]); ps = [float(x) for x in sys.argv[5].split(",")]
    nr = int(sys.argv[6]) if len(sys.argv) > 6 else 12
    os.makedirs("results/compression", exist_ok=True)
    fn = f"results/compression/n{n}_m{m}_eta{'-'.join(map(str, eta))}_c{c13}.json"
    rows = json.load(open(fn)) if os.path.exists(fn) else []
    for p in ps:
        if any(abs(r["p"] - p) < 1e-12 for r in rows): continue
        r = solve(n, m, eta, p, c13, nr); rows.append(r)
        json.dump(sorted(rows, key=lambda z: z["p"]), open(fn, "w"), indent=1)
        print(p, np.round(np.array(r["W"]), 4).tolist(), "gain %.3e" % (r["loss_mono"] - r["loss"]), flush=True)
