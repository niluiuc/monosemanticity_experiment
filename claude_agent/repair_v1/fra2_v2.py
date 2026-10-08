"""R2 — repaired encoder search for the two-feature model (same objective and evaluator as fra2.py).

Bug in fra2.solve (found by the GPT audit): the exact small-angle grid had ~28% relative spacing,
and the coarse locator's bias grid has ~1e-6 loss error. A narrow, shallow noisy sharing well
(width ~0.006 at theta ~ -0.028, depth ~1e-8, sigma = .003) fell between grid points, so mono was
returned. Repair:
  * every theta on a dense grid (700 log-spaced points per branch on [1e-5, 0.6] -> 1.8% relative
    spacing, plus 200 linear points to pi/2) is evaluated with a NEAR-EXACT vectorised bias profile
    (501-point grid then 40 safeguarded Newton steps on the exact Gaussian loss; sigma = 0 uses exact
    piecewise enumeration);
  * EVERY local minimum of that profile (not just the best grid point) is refined with bounded Brent
    on the original exact evaluator fra2.F, and the best refined value is returned.
The loss evaluator fra2.F is unchanged (the audit confirmed it)."""
import os, sys
import numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fra2 import F, states

SQ2PI = np.sqrt(2 * np.pi)
LOG = np.logspace(-5, np.log10(0.6), 700)
LIN = np.linspace(0.6, np.pi / 2, 201)[1:]
GRID = np.concatenate([[0.0], LOG, LIN])            # magnitudes; branch sign applied later
BGRID = np.linspace(-2.5, 2.5, 501)


def _moments(mu, s):
    s = np.maximum(s, 1e-300); z = mu / s
    Phi = ndtr(z); phi = np.exp(-0.5 * z * z) / SQ2PI
    m1 = mu * Phi + s * phi; m2 = (mu * mu + s * s) * Phi + mu * s * phi
    return m1, m2, Phi, phi


def _out_profile(th, i, p, c, sigma):
    """near-exact min_b of output i's loss, vectorised over theta array th (sigma > 0)."""
    X, P = states(p, c)
    w1, w2 = np.cos(th), np.sin(th)
    wi = (w1 if i == 0 else w2)[:, None]
    m = wi * (w1[:, None] * X[None, :, 0] + w2[:, None] * X[None, :, 1])      # (T,4)
    s = np.abs(wi) * sigma                                                    # (T,1)
    t = X[:, i][None, :]
    def loss(b):                                                              # b: (T,)
        mu = m + b[:, None]
        if sigma == 0:
            r = np.maximum(mu, 0); return (P * (r - t) ** 2).sum(1)
        m1, m2, _, _ = _moments(mu, s); return (P * (m2 - 2 * t * m1 + t * t)).sum(1)
    best = np.full(len(th), np.inf); bb = np.zeros(len(th))
    for b in BGRID:
        L = loss(np.full(len(th), b)); u = L < best; best[u] = L[u]; bb[u] = b
    if sigma > 0:
        for _ in range(40):
            mu = m + bb[:, None]; m1, m2, Phi, phi = _moments(mu, s)
            g = (P * (2 * m1 - 2 * t * Phi)).sum(1)
            h = (P * (2 * Phi - 2 * t * phi / np.maximum(s, 1e-300))).sum(1)
            step = np.where(h > 1e-12, -g / np.maximum(h, 1e-12), -1e-3 * np.sign(g))
            step = np.clip(step, -0.05, 0.05)
            cand = bb + step; Lc = loss(cand); ok = Lc <= best
            bb = np.where(ok, cand, bb); best = np.where(ok, Lc, best)
    else:   # exact piecewise enumeration (as in certify_global.py)
        from certify_global import out_min_vec
        best = out_min_vec(m, X[:, i], P)
    return best


def profile(th, p, c, sigma, eta):
    th = np.asarray(th, float)
    return _out_profile(th, 0, p, c, sigma) + eta * _out_profile(th, 1, p, c, sigma)


def branch_opt(p, c, sigma, eta, sign):
    ts = sign * GRID
    v = profile(ts, p, c, sigma, eta)
    cands = []
    for k in range(len(ts)):
        left = v[k - 1] if k > 0 else np.inf
        right = v[k + 1] if k < len(ts) - 1 else np.inf
        if v[k] <= left and v[k] <= right:
            cands.append(k)
    best = (np.inf, None)
    for k in cands:                                     # refine EVERY local minimum
        if 0 < k < len(ts) - 1:
            a, b = sorted([ts[k - 1], ts[k + 1]])
            r = minimize_scalar(lambda t: F(t, p, c, sigma, eta)[0], bounds=(a, b), method="bounded",
                                options={"xatol": 1e-12})
            val, t = (r.fun, r.x)
            v0 = F(ts[k], p, c, sigma, eta)[0]
            if v0 < val: val, t = v0, ts[k]
        else:
            t = ts[k]; val = F(t, p, c, sigma, eta)[0]
        if val < best[0]:
            best = (val, t)
    return best[1], best[0], len(cands)


def solve(p, c, sigma, eta):
    tn, vn, nn = branch_opt(p, c, sigma, eta, -1)
    tp, vp, npos = branch_opt(p, c, sigma, eta, +1)
    Fm = F(0.0, p, c, sigma, eta)[0]
    t_star, F_star = (tn, vn) if vn <= vp else (tp, vp)
    if Fm <= F_star: t_star, F_star = 0.0, Fm
    return dict(p=p, c=c, sigma=sigma, eta=eta, t_star=float(t_star), F_star=float(F_star), F_mono=float(Fm),
                t_neg=float(tn), F_neg=float(vn), t_pos=float(tp), F_pos=float(vp), n_local_minima=[nn, npos])
