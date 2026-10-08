"""
Exact population solver for the two-feature / one-dimension tied-ReLU bottleneck,
extended (additively) with
  * feature correlation  c  (Pearson correlation of the two Bernoulli(p) features)
  * TRAINING code noise  sigma  (the encoder AND biases are selected under noise,
    rather than selected clean and evaluated under noise as in project1_toy).

Model (same conventions as project1_toy/paper_assembly_20261006/manuscript.md §3):
  X = (X1, X2) in {0,1}^2, marginals Bernoulli(p), corr c.
  h = w . X + sigma Z,  w = (cos t, sin t)   (encoder energy one)
  yhat_i = ReLU(w_i h + b_i)                 (tied decoder, free biases)
  L(t, b) = E[(yhat_1 - X1)^2] + eta E[(yhat_2 - X2)^2]

t = 0      : mono, keep feature 1   (weak column exactly zero)
t < 0      : opposite-sign sharing  (the branch selected in the existing theorem)
t > 0      : same-sign sharing
t = pi/2   : mono, keep feature 2
w -> -w is a symmetry, so t in [-pi/2, pi/2] covers everything.

All expectations are exact (4 states x closed-form Gaussian ReLU moments).
"""
import numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar

SQ2PI = np.sqrt(2.0 * np.pi)


def states(p, c):
    """Joint law of two Bernoulli(p) with correlation c. Returns (X[4,2], prob[4])."""
    q = 1.0 - p
    cov = c * p * q
    P11 = p * p + cov
    P10 = p * q - cov
    P01 = p * q - cov
    P00 = q * q + cov
    pr = np.array([P00, P10, P01, P11])
    if np.any(pr < -1e-15):
        raise ValueError(f"infeasible (p,c)=({p},{c})")
    X = np.array([[0, 0], [1, 0], [0, 1], [1, 1]], dtype=float)
    return X, pr


def relu_moments(mu, s):
    """E[ReLU(Y)], E[ReLU(Y)^2] for Y ~ N(mu, s^2); s may be 0 (vectorised)."""
    mu = np.asarray(mu, dtype=float)
    s = np.asarray(s, dtype=float)
    s_safe = np.where(s > 0, s, 1.0)
    z = mu / s_safe
    Phi = ndtr(z)
    phi = np.exp(-0.5 * z * z) / SQ2PI
    m1 = mu * Phi + s_safe * phi
    m2 = (mu * mu + s_safe * s_safe) * Phi + mu * s_safe * phi
    det = s <= 0
    if np.any(det):
        r = np.maximum(mu, 0.0)
        m1 = np.where(det, r, m1)
        m2 = np.where(det, r * r, m2)
    return m1, m2


def output_loss(wi, b, t, i, p, c, sigma):
    """Exact E[(ReLU(w_i h + b) - X_i)^2]; broadcasting over arrays wi/t (shape A) and b (shape B)."""
    X, pr = states(p, c)
    w1, w2 = np.cos(t), np.sin(t)
    tot = 0.0
    for x, px in zip(X, pr):
        m = w1 * x[0] + w2 * x[1]
        mu = wi * m + b
        s = np.abs(wi) * sigma
        m1, m2 = relu_moments(mu, s * np.ones_like(mu))
        xi = x[i]
        tot = tot + px * (m2 - 2.0 * xi * m1 + xi * xi)
    return tot


def profile_bias(t, i, p, c, sigma, bgrid=np.linspace(-2.5, 2.5, 1001), xtol=1e-13):
    """Globally (grid + Brent) optimal bias for output i at fixed encoder angle t."""
    wi = np.cos(t) if i == 0 else np.sin(t)
    L = output_loss(np.array([wi]), bgrid, np.array([t]), i, p, c, sigma)
    j = int(np.argmin(L))
    lo, hi = bgrid[max(j - 1, 0)], bgrid[min(j + 1, len(bgrid) - 1)]
    f = lambda b: float(output_loss(np.array([wi]), np.array([b]), np.array([t]), i, p, c, sigma)[0])
    r = minimize_scalar(f, bounds=(lo, hi), method="bounded", options={"xatol": xtol})
    bb, val = (r.x, r.fun) if r.fun <= L[j] else (bgrid[j], L[j])
    return bb, val


def F(t, p, c, sigma, eta):
    """Bias-profiled population loss at angle t. Returns (loss, b1, b2)."""
    b1, l1 = profile_bias(t, 0, p, c, sigma)
    b2, l2 = profile_bias(t, 1, p, c, sigma)
    return l1 + eta * l2, b1, b2


def tgrid():
    """Angle grid dense near the mono point t=0 (and near +-pi/2)."""
    lin = np.linspace(0.0, np.pi / 2, 721)
    lg = np.logspace(-7, -1, 241)
    u = np.unique(np.concatenate([lin, lg, np.pi / 2 - lg]))
    u = u[(u >= 0) & (u <= np.pi / 2)]
    return u


TG = tgrid()


BCOARSE = np.linspace(-2.5, 2.5, 2001)
SMALL = np.logspace(-7, np.log10(0.3), 61)


def F_coarse(ts, p, c, sigma, eta):
    """Vectorised coarse profiled loss (bias minimised on BCOARSE). Locator only."""
    ts = np.asarray(ts)[:, None]
    l1 = output_loss(np.cos(ts), BCOARSE[None, :], ts, 0, p, c, sigma).min(axis=1)
    l2 = output_loss(np.sin(ts), BCOARSE[None, :], ts, 1, p, c, sigma).min(axis=1)
    return l1 + eta * l2


def _refine(ts, vals, j, p, c, sigma, eta):
    best_t, best_v = ts[j], F(ts[j], p, c, sigma, eta)[0]
    if 0 < j < len(ts) - 1:
        a, b = sorted([ts[j - 1], ts[j + 1]])
        r = minimize_scalar(lambda t: F(t, p, c, sigma, eta)[0], bounds=(a, b),
                            method="bounded", options={"xatol": 1e-13})
        if r.fun < best_v:
            best_t, best_v = r.x, r.fun
    return best_t, best_v


def branch_opt(p, c, sigma, eta, sign):
    """Best angle on one branch: sign=-1 -> t in [-pi/2,0], sign=+1 -> t in [0,pi/2].
    (1) coarse vectorised landscape over the whole branch, refined exactly at its argmin;
    (2) EXACT profiled loss on a log grid of small angles (where gains are ~1e-9 and the
        coarse locator is blind), refined exactly at its argmin. Best of both is returned."""
    ts = sign * TG
    vals = F_coarse(ts, p, c, sigma, eta)
    cand = [_refine(ts, vals, int(np.argmin(vals)), p, c, sigma, eta)]
    tsm = sign * np.concatenate([[0.0], SMALL])
    vsm = np.array([F(t, p, c, sigma, eta)[0] for t in tsm])
    cand.append(_refine(tsm, vsm, int(np.argmin(vsm)), p, c, sigma, eta))
    best_t, best_v = min(cand, key=lambda z: z[1])
    return best_t, best_v, ts, vals


def solve(p, c, sigma, eta, keep_landscape=False):
    """Global optimum over both branches. Returns dict."""
    tn, vn, tsn, valsn = branch_opt(p, c, sigma, eta, -1)
    tp, vp, tsp, valsp = branch_opt(p, c, sigma, eta, +1)
    Fm = F(0.0, p, c, sigma, eta)[0]
    t_star, v_star = (tn, vn) if vn <= vp else (tp, vp)
    out = dict(p=p, c=c, sigma=sigma, eta=eta, t_star=float(t_star), F_star=float(v_star),
               F_mono=float(Fm), t_neg=float(tn), F_neg=float(vn), t_pos=float(tp), F_pos=float(vp))
    if keep_landscape:
        ts = np.concatenate([tsn[::-1], tsp[1:]])
        vs = np.concatenate([valsn[::-1], valsp[1:]])
        out["landscape_t"] = ts
        out["landscape_F"] = vs
    return out


# ---------- existing closed forms (project1_toy manuscript §4) for validation ----------
def pc_theory(eta):
    return (1 + eta - np.sqrt(1 + 2 * eta - 3 * eta ** 2)) / (2 * eta)


def K_C_theory(eta):
    p0 = pc_theory(eta); q0 = 1 - p0; D0 = 1 - p0 + p0 ** 2
    s = np.sqrt(1 + 2 * eta - 3 * eta ** 2)
    return s / (3 * p0 * q0), s ** 3 / (27 * D0 * p0 * q0)
