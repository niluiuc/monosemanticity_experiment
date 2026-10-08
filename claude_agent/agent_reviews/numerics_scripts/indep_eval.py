"""Independent evaluator of the bias-profiled loss F(t) for the two-feature tied-ReLU toy model.
Written for the numerics audit; shares NO code with fra2.py / fra2_v2.py / certify_global.py.

F(t) = min_b1 G_1(t,b1) + eta * min_b2 G_2(t,b2),
G_i(t,b) = sum_x P_x E[(ReLU(w_i (w.x) + b + w_i sigma Z) - x_i)^2].

Bias minimisation per output:
  * s = |w_i| sigma == 0 : exact piecewise-quadratic enumeration (all breakpoint intervals, closed-form
    stationary point clipped to each interval, plus every breakpoint).
  * s > 0 : candidate grid = uniform grid on [BLO, BHI] + clusters of points around every breakpoint
    -o_x (offsets -o_x + s*k, k in KCL) + the clean optimal bias; take the K lowest discrete local minima
    of G on that grid and polish each with vectorised golden-section search (120 iterations) inside its
    two neighbouring grid points; return the smallest value.  The analytic s->0 limit is used for
    |z| > 40 to avoid overflow.
"""
import numpy as np
from scipy.special import ndtr

SQ2PI = np.sqrt(2 * np.pi)
BLO, BHI, NB = -3.0, 3.5, 1301
KCL = np.array([-12, -6, -3, -2, -1.5, -1, -0.6, -0.3, 0, 0.3, 0.6, 1, 1.5, 2, 3, 6, 12], float)
GR = (np.sqrt(5) - 1) / 2


def joint(p, c):
    q = 1 - p; cov = c * p * q
    X = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
    P = np.array([q * q + cov, p * q - cov, p * q - cov, p * p + cov])
    if P.min() < -1e-15:
        raise ValueError("infeasible")
    return X, np.maximum(P, 0)


def G_noisy(o, b, tg, P, s):
    """o:(N,4) offsets, b:(N,M) biases, tg:(4,), P:(4,), s:(N,) >0 -> (N,M)."""
    mu = o[:, None, :] + b[:, :, None]                 # (N,M,4)
    ss = s[:, None, None]
    z = mu / ss
    zc = np.clip(z, -40, 40)
    Phi = ndtr(zc); phi = np.exp(-0.5 * zc * zc) / SQ2PI
    m1 = mu * Phi + ss * phi
    m2 = (mu * mu + ss * ss) * Phi + mu * ss * phi
    big = z > 40; small = z < -40                      # analytic limits (errors < 1e-300 relative)
    m1 = np.where(big, mu, np.where(small, 0.0, m1))
    m2 = np.where(big, mu * mu + ss * ss, np.where(small, 0.0, m2))
    return (P * (m2 - 2 * tg * m1 + tg * tg)).sum(-1)


def G_clean(o, b, tg, P):
    r = np.maximum(o[:, None, :] + b[:, :, None], 0)
    return (P * (r - tg) ** 2).sum(-1)


def outmin_clean(o, tg, P):
    """exact min_b sum P (relu(o+b)-t)^2 by full interval enumeration. o:(N,4)."""
    N = o.shape[0]
    bps = np.sort(-o, axis=1)                          # breakpoints ascending (N,4)
    edges = np.concatenate([np.full((N, 1), -1e6), bps, np.full((N, 1), 1e6)], 1)   # 5 intervals
    cands = [bps]
    for k in range(5):
        lo, hi = edges[:, k], edges[:, k + 1]
        mid = 0.5 * (np.maximum(lo, -1e3) + np.minimum(hi, 1e3))
        on = (o + mid[:, None]) > 0                    # active set inside interval k
        W = (P * on).sum(1)
        bst = np.where(W > 0, (P * on * (tg - o)).sum(1) / np.where(W > 0, W, 1), mid)
        cands.append(np.clip(bst, np.maximum(lo, -1e3), np.minimum(hi, 1e3))[:, None])
    B = np.concatenate(cands, 1)
    return G_clean(o, B, tg, P).min(1)


def outmin(o, tg, P, s, K=3):
    """min over b of G for each row; s:(N,) (zeros allowed)."""
    N = o.shape[0]
    res = np.empty(N)
    z0 = s <= 0
    if z0.any():
        res[z0] = outmin_clean(o[z0], tg, P)
    nz = ~z0
    if not nz.any():
        return res
    o = o[nz]; s = s[nz]; n = o.shape[0]
    base = np.broadcast_to(np.linspace(BLO, BHI, NB), (n, NB))
    clus = (-o[:, :, None] + s[:, None, None] * KCL[None, None, :]).reshape(n, -1)
    bcl = np.empty((n, 0))
    B = np.sort(np.concatenate([base, clus], 1), axis=1)
    B = np.clip(B, BLO - 1, BHI + 1)
    Gv = G_noisy(o, B, tg, P, s)
    # discrete local minima (interior), keep K lowest
    M = B.shape[1]
    isl = np.zeros_like(Gv, bool)
    isl[:, 1:-1] = (Gv[:, 1:-1] <= Gv[:, :-2]) & (Gv[:, 1:-1] <= Gv[:, 2:])
    score = np.where(isl, Gv, np.inf)
    idx = np.argsort(score, axis=1)[:, :K]             # (n,K)
    valid = np.take_along_axis(score, idx, 1) < np.inf
    idx = np.clip(idx, 1, M - 2)
    a = np.take_along_axis(B, idx - 1, 1); c = np.take_along_axis(B, idx + 1, 1)
    best = Gv.min(1)
    # vectorised golden-section on all (row, k) brackets
    oo = np.repeat(o, K, 0); sv = np.repeat(s, K)
    a = a.reshape(-1); c = c.reshape(-1)
    x1 = c - GR * (c - a); x2 = a + GR * (c - a)
    f1 = G_noisy(oo, x1[:, None], tg, P, sv)[:, 0]; f2 = G_noisy(oo, x2[:, None], tg, P, sv)[:, 0]
    for _ in range(120):
        left = f1 < f2
        c = np.where(left, x2, c); a = np.where(left, a, x1)
        nx1 = np.where(left, c - GR * (c - a), x2); nx2 = np.where(left, x1, a + GR * (c - a))
        nf = G_noisy(oo, np.where(left, nx1, nx2)[:, None], tg, P, sv)[:, 0]
        f1, f2 = np.where(left, nf, f2), np.where(left, f1, nf)
        x1, x2 = nx1, nx2
    gm = np.minimum(f1, f2).reshape(n, K)
    gm = np.where(valid, gm, np.inf)
    res[nz] = np.minimum(best, gm.min(1))
    return res


def Fvec(th, p, c, sigma, eta, chunk=400):
    th = np.atleast_1d(np.asarray(th, float))
    X, P = joint(p, c)
    out = np.empty(len(th))
    for i0 in range(0, len(th), chunk):
        t = th[i0:i0 + chunk]
        w1, w2 = np.cos(t), np.sin(t)
        m = w1[:, None] * X[None, :, 0] + w2[:, None] * X[None, :, 1]
        g1 = outmin(w1[:, None] * m, X[:, 0], P, np.abs(w1) * sigma)
        g2 = outmin(w2[:, None] * m, X[:, 1], P, np.abs(w2) * sigma)
        out[i0:i0 + chunk] = g1 + eta * g2
    return out


def F1(t, p, c, sigma, eta):
    return float(Fvec(np.array([t]), p, c, sigma, eta)[0])


def golden_t(f, a, b, it=90):
    x1 = b - GR * (b - a); x2 = a + GR * (b - a); f1, f2 = f(x1), f(x2)
    for _ in range(it):
        if f1 < f2:
            b, x2, f2 = x2, x1, f1; x1 = b - GR * (b - a); f1 = f(x1)
        else:
            a, x1, f1 = x1, x2, f2; x2 = a + GR * (b - a); f2 = f(x2)
    return (x1, f1) if f1 < f2 else (x2, f2)


def dense_grid(rel=1e-3, tmin=1e-8, nlin=6001):
    n = int(np.log(np.pi / 2 / tmin) / np.log1p(rel)) + 1
    lg = np.geomspace(tmin, np.pi / 2, n)
    lin = np.linspace(0, np.pi / 2, nlin)
    pos = np.unique(np.concatenate([lg, lin]))
    return np.concatenate([-pos[::-1], [0.0], pos])


def global_search(p, c, sigma, eta, rel=1e-3, refine=True):
    """very dense search on [-pi/2, pi/2]; refines every discrete local minimum by golden section
    on the independent evaluator. Returns (t_best, F_best, F0, list of local minima)."""
    ts = dense_grid(rel)
    ts = ts[np.abs(ts) <= np.pi / 2]
    v = Fvec(ts, p, c, sigma, eta)
    F0 = F1(0.0, p, c, sigma, eta)
    k = np.arange(1, len(ts) - 1)
    loc = k[(v[k] <= v[k - 1]) & (v[k] <= v[k + 1])]
    # round-off plateaus near t=0 create thousands of 1e-17 'minima': refine the 20 lowest local minima plus
    # up to 20 local minima within 1e-12 of the best grid value
    order = loc[np.argsort(v[loc])]
    near = order[v[order] < v.min() + 1e-12][:20]
    loc = list(np.unique(np.concatenate([order[:20], near]))) + [0, len(ts) - 1]
    mins = []
    for j in loc:
        if refine and 0 < j < len(ts) - 1:
            tt, ff = golden_t(lambda x: F1(x, p, c, sigma, eta), ts[j - 1], ts[j + 1], it=70)
            if v[j] < ff: tt, ff = ts[j], v[j]
        else:
            tt, ff = ts[j], v[j]
        mins.append((float(tt), float(ff)))
    tb, fb = min(mins + [(0.0, F0)], key=lambda z: z[1])
    return tb, fb, F0, mins
