"""Core routines for the bounded held-out robustness test (repair_v3). See PROTOCOL_FROZEN.md.

Model: energy-one scalar code h = w.x + sigma*Z, tied decoder xhat_i = ReLU(w_i h + b_i), importances eta.
Per-image risk is the exact expectation over Z (Gaussian ReLU moments). Biases are fitted per output
and per sigma on a declared fitting split; encoders are fitted on TRAIN only at sigma = 0.
"""
import json, os, hashlib
import numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar

HERE = os.path.dirname(os.path.abspath(__file__))
ALGO = os.path.dirname(os.path.dirname(HERE))
LOGITS = os.path.join(ALGO, "project1_toy", "head_transfer_20261007", "extraction_run_v1", "raw_logits.npy")
SQ2PI = np.sqrt(2 * np.pi)
SPLIT_SEED = 20261008
TRAIN_ROWS = np.arange(0, 256)
CAL_ROWS = np.arange(256, 512)
EXCLUDED_ROWS = np.arange(512, 1024)          # used by earlier pooled analyses: never evaluated here
POOL_ROWS = np.arange(1024, 4608)              # 3584 images for the new allocation


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def make_split():
    rng = np.random.default_rng(SPLIT_SEED)
    perm = rng.permutation(POOL_ROWS)
    return dict(S=np.sort(perm[:896]), P=np.sort(perm[896:1792]), E=np.sort(perm[1792:]))


def load_rows(rows, cols):
    L = np.load(LOGITS, mmap_mode="r")
    return np.maximum(np.asarray(L[np.asarray(rows)][:, list(cols)], dtype=float), 0.0)


# ---------------------------------------------------------------- per-image loss
def out_loss(mu, s, t):
    """E[(ReLU(mu + s Z) - t)^2], elementwise; s scalar >= 0."""
    if s <= 0:
        return (np.maximum(mu, 0.0) - t) ** 2
    z = mu / s
    Phi = ndtr(z); phi = np.exp(-0.5 * z * z) / SQ2PI
    m1 = mu * Phi + s * phi
    m2 = (mu * mu + s * s) * Phi + mu * s * phi
    return m2 - 2 * t * m1 + t * t


def fit_bias(o, t, s):
    """argmin_b mean_n out_loss(o_n + b, s, t_n). Exact piecewise enumeration if s == 0."""
    o = np.asarray(o, float); t = np.asarray(t, float); n = len(o)
    if s <= 0:
        idx = np.argsort(-o); os_ = o[idx]; ts = t[idx]
        r = os_ - ts
        S1 = np.concatenate([[0.0], np.cumsum(r)]); S2 = np.concatenate([[0.0], np.cumsum(r * r)])
        Tt = np.concatenate([[0.0], np.cumsum(ts * ts)]); Ttot = Tt[-1]
        cands = list(-os_)
        for k in range(1, n + 1):
            b = -S1[k] / k
            lo = -os_[k - 1]; hi = -os_[k] if k < n else np.inf
            if lo <= b <= hi:
                cands.append(b)
        cands = np.array(cands)
        vals = np.array([np.mean(out_loss(o + b, 0.0, t)) for b in cands])
        j = int(np.argmin(vals)); return float(cands[j]), float(vals[j])
    grid = np.linspace(-3.0, 3.0, 601)
    vals = np.array([np.mean(out_loss(o + b, s, t)) for b in grid])
    locs = [k for k in range(len(grid)) if (k == 0 or vals[k] <= vals[k - 1]) and (k == len(grid) - 1 or vals[k] <= vals[k + 1])]
    best = (np.inf, None)
    for k in locs:
        a, c = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
        rr = minimize_scalar(lambda b: np.mean(out_loss(o + b, s, t)), bounds=(a, c), method="bounded", options={"xatol": 1e-10})
        v, b = (rr.fun, rr.x) if rr.fun < vals[k] else (vals[k], grid[k])
        if v < best[0]: best = (v, b)
    return float(best[1]), float(best[0])


def offsets(w, X):
    h = X @ w
    return [w[0] * h, w[1] * h]


def fit_biases(w, X, sigma, eta):
    """biases (b1, b2) fitted on X at noise sigma; returns biases and weighted mean loss."""
    o = offsets(w, X); bs = []; tot = 0.0
    for i in range(2):
        b, v = fit_bias(o[i], X[:, i], abs(w[i]) * sigma); bs.append(b); tot += eta[i] * v
    return np.array(bs), tot


def per_image_loss(w, b, X, sigma, eta):
    o = offsets(w, X)
    return sum(eta[i] * out_loss(o[i] + b[i], abs(w[i]) * sigma, X[:, i]) for i in range(2))


# ---------------------------------------------------------------- encoders (train, sigma = 0)
def clean_profile(theta, X, eta):
    w = np.array([np.cos(theta), np.sin(theta)])
    return fit_biases(w, X, 0.0, eta)[1]


def fit_sharing_encoder(X, eta, n_grid=1440):
    th = np.linspace(-np.pi / 2, np.pi / 2, n_grid, endpoint=False)
    v = np.array([clean_profile(t, X, eta) for t in th])
    n = len(th); minima = []
    for k in range(n):
        if v[k] <= v[k - 1] and v[k] <= v[(k + 1) % n]:
            a, c = th[k] - (th[1] - th[0]), th[k] + (th[1] - th[0])
            rr = minimize_scalar(lambda t: clean_profile(t, X, eta), bounds=(a, c), method="bounded", options={"xatol": 1e-9})
            tt, vv = (rr.x, rr.fun) if rr.fun < v[k] else (th[k], v[k])
            minima.append((float(vv), float(tt)))
    minima.sort()
    best_v, best_t = minima[0]
    competing = [m for m in minima[1:] if m[0] - best_v < 1e-6]
    return dict(theta=best_t, train_loss=best_v, n_local_minima=len(minima), competing_within_1e6=competing)


def fit_mono(X, eta):
    out = {}
    for r in (0, 1):
        w = np.zeros(2); w[r] = 1.0
        out[r] = fit_biases(w, X, 0.0, eta)[1]
    r = int(min(out, key=out.get))
    return dict(retained=r, train_loss=out[r], other_orientation_train_loss=out[1 - r])


# ---------------------------------------------------------------- theory coefficient (PREDICTION_STATEMENT.md section 2)
def v_coeff(p):
    H = lambda z: (z * z + 1) * ndtr(z) + z * np.exp(-z * z / 2) / SQ2PI
    return minimize_scalar(lambda z: p * (1 + z * z) + (1 - p) * H(z), bounds=(-8, 8), method="bounded", options={"xatol": 1e-12}).fun


def theory_B(w_share, b_share0, r, X, eta):
    """B = sum_i eta_i w_i^2 f_i(open) - eta_r v(p_r), evaluated on the images X."""
    o = offsets(w_share, X)
    f = [float(np.mean(o[i] + b_share0[i] > 0)) for i in range(2)]
    p_r = float(np.mean(X[:, r] > 0))
    B = sum(eta[i] * w_share[i] ** 2 * f[i] for i in range(2)) - eta[r] * v_coeff(p_r)
    return B, f, p_r


def first_crossing(sig, d):
    """first sigma where d goes from < 0 to >= 0 (linear interpolation); np.inf if none; nan if d[0] >= 0."""
    if d[0] >= 0: return np.nan
    for k in range(1, len(sig)):
        if d[k] >= 0:
            return float(sig[k - 1] + (sig[k] - sig[k - 1]) * (-d[k - 1]) / (d[k] - d[k - 1]))
    return np.inf
