"""Computer-assisted global certificate (sigma = 0) for correlated features: on which branch does the
GLOBAL optimum lie?  F(theta) = sum_i eta_i min_b G_i(theta, b) is evaluated EXACTLY (all pieces and
breakpoints of the piecewise-quadratic bias problem, vectorised). A rigorous Lipschitz constant
    |dF/dtheta| <= L = 2 * 3.5 * 2*sqrt(2) * (1 + eta)
(v1 used 3.5, which is too small; v2: an optimal b can always be chosen in [-sqrt2, 1+sqrt2], since G is constant
 below -max o and increasing above 1 - min o, so |ReLU(o+b)-t| <= 1+2*sqrt2; |d o_x/d theta| <= 2 sqrt2)
lets us discard every theta-interval I with F(mid) - L|I|/2 > F_best. Intervals are bisected until
discarded or shorter than h_min. Output per (p, c): the surviving set, whether it lies entirely in
theta<0 / theta>0 / contains 0, and the best value. Floating point is double precision with a
1e-12 safety margin (not directed rounding).
Usage: python certify_global.py <p-list> <c-list>  -> results/certificate/*.json"""
import json, sys, os, time
import numpy as np

ETA = 0.5
LIP = 2 * (1 + 2 * np.sqrt(2)) * 2 * np.sqrt(2) * (1 + ETA)   # v2: |relu(o+b)-t| <= 1+2*sqrt2 for b in [-sqrt2, 1+sqrt2]
SAFE = 1e-12


def joint(p, c):
    q = 1 - p; cov = c * p * q
    X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], float)
    P = np.array([q * q + cov, p * q - cov, p * q - cov, p * p + cov])
    return X, P


def out_min_vec(o, t, P):
    """o: (N,4) offsets, t: (4,) targets, P: (4,) probs -> exact min_b sum P (relu(o+b)-t)^2, shape (N,)."""
    N = o.shape[0]
    cands = [-o]                                             # breakpoints (N,4)
    order = np.argsort(-o, axis=1)                           # states by decreasing offset
    os_ = np.take_along_axis(o, order, 1); Ps = P[order]; ts = t[order]
    for k in range(1, 5):                                    # piece where exactly the top-k states are on
        W = Ps[:, :k].sum(1)
        b = (Ps[:, :k] * (ts[:, :k] - os_[:, :k])).sum(1) / np.maximum(W, 1e-300)
        lo = -os_[:, k - 1]
        hi = -os_[:, k] if k < 4 else np.full(N, np.inf)
        valid = (b >= lo) & (b <= hi) & (W > 0)
        cands.append(np.where(valid, b, -o[:, 0])[:, None])   # invalid -> harmless duplicate breakpoint
    B = np.concatenate(cands, 1)                              # (N, 8)
    val = (P[None, None, :] * (np.maximum(o[:, None, :] + B[:, :, None], 0) - t[None, None, :]) ** 2).sum(2)
    return val.min(1)


def Fvec(th, p, c):
    X, P = joint(p, c)
    w1, w2 = np.cos(th)[:, None], np.sin(th)[:, None]
    m = w1 * X[None, :, 0] + w2 * X[None, :, 1]               # (N,4)
    return out_min_vec(w1 * m, X[:, 0], P) + ETA * out_min_vec(w2 * m, X[:, 1], P)


def certify(p, c, h_min=1e-7, max_iter=60):
    ivs = np.linspace(-np.pi / 2, np.pi / 2, 20001)
    lo, hi = ivs[:-1], ivs[1:]
    best = Fvec(np.linspace(-np.pi / 2, np.pi / 2, 200001), p, c).min()
    for it in range(max_iter):
        mid = 0.5 * (lo + hi); fm = Fvec(mid, p, c); best = min(best, fm.min())
        keep = fm - LIP * (hi - lo) / 2 > best + SAFE
        lo, hi = lo[~keep], hi[~keep]
        if len(lo) == 0: break
        small = (hi - lo) < h_min
        if small.all(): break
        # bisect the not-yet-small survivors
        L1, H1 = lo[~small], hi[~small]; M1 = 0.5 * (L1 + H1)
        lo = np.concatenate([lo[small], L1, M1]); hi = np.concatenate([hi[small], M1, H1])
        if len(lo) > 4_000_000: break
    surv_lo, surv_hi = lo.min() if len(lo) else None, hi.max() if len(hi) else None
    side = None
    if len(lo):
        if hi.max() < 0: side = "opposite (theta<0)"
        elif lo.min() > 0: side = "same-sign (theta>0)"
        else: side = "contains/straddles 0"
    return dict(p=p, c=c, best=float(best), n_surviving=int(len(lo)), surviving_range=[float(surv_lo), float(surv_hi)] if len(lo) else None,
                certified_side=side, iterations=it + 1)


if __name__ == "__main__":
    ps = [float(x) for x in sys.argv[1].split(",")]; cs = [float(x) for x in sys.argv[2].split(",")]
    os.makedirs("results/certificate_v2", exist_ok=True)
    for c in cs:
        for p in ps:
            fn = f"results/certificate_v2/p{p}_c{c}.json"
            if os.path.exists(fn): continue
            X, P = joint(p, c)
            if P.min() <= 0: continue
            t0 = time.time(); r = certify(p, c); r["secs"] = time.time() - t0
            json.dump(r, open(fn, "w"), indent=1)
            print(p, c, r["certified_side"], r["surviving_range"], r["n_surviving"], round(r["secs"], 1), flush=True)
