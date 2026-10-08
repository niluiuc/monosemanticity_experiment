"""Real-activation test (see real_protocol.md). Usage:
   python real_pairs.py select                 -> results/real/pairs.json
   python real_pairs.py run <chunk> <nchunks>  -> results/real/part<chunk>.json
   python real_pairs.py merge <nchunks>"""
import json, sys, os, time
import numpy as np
from scipy.special import ndtr
from multiprocessing import Pool

SRC = "../project1_toy/vision_transfer_20261006/extraction_run_v1/vision_activations.npz"
SRC_LOGITS = "../project1_toy/head_transfer_20261007/extraction_run_v1/raw_logits.npy"
DATASET = os.environ.get("REAL_DATASET", "layer4")          # "layer4" (primary) or "logits" (replication)
OUT = "results/real" if DATASET == "layer4" else "results/real_logits"
PER_BIN = 25 if DATASET == "layer4" else 15
ETA = 0.5
SIGMAS = [0.005, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6]
TH = np.linspace(-np.pi / 2, np.pi / 2, 241)[:-1]
SQ2PI = np.sqrt(2 * np.pi)
os.makedirs(OUT, exist_ok=True)


def load():
    if DATASET == "layer4":
        d = np.load(SRC, allow_pickle=True)
        X = np.concatenate([d["train"], d["calibration"], d["test"]], 0).astype(float)
    else:   # replication: first 1024 saved images, 1000 ImageNet logits rectified at zero
        X = np.maximum(np.load(SRC_LOGITS, mmap_mode="r")[:1024].astype(float), 0.0)
    zf = (X <= 0).mean(0)
    elig = np.where((zf > 0.05) & (zf < 0.95))[0]
    return X, zf, elig


def out_loss_and_derivs(mu, s, x):
    """per-sample E[(ReLU(mu+sZ)-x)^2] and its first two derivatives in mu; s>0 scalar or array."""
    z = mu / s
    Phi = ndtr(z); phi = np.exp(-0.5 * z * z) / SQ2PI
    m1 = mu * Phi + s * phi
    m2 = (mu * mu + s * s) * Phi + mu * s * phi
    L = m2 - 2 * x * m1 + x * x
    d1 = 2 * m1 - 2 * x * Phi
    d2 = 2 * Phi - 2 * x * phi / s
    return L, d1, d2


def profiled(theta, X1, X2, sigma, out):
    """exact bias-profiled empirical loss of output `out` for each theta (vectorised)."""
    w1, w2 = np.cos(theta)[:, None], np.sin(theta)[:, None]
    wi = w1 if out == 0 else w2
    x = (X1 if out == 0 else X2)[None, :]
    m = wi * (w1 * X1[None, :] + w2 * X2[None, :])           # (T, n)
    s = np.maximum(np.abs(wi) * sigma, 1e-12)
    bg = np.linspace(-1.5, 1.5, 31)
    best = np.full(theta.shape, np.inf); bb = np.zeros(theta.shape)
    for b in bg:                                              # grid initialisation
        L = out_loss_and_derivs(m + b, s, x)[0].mean(1)
        upd = L < best; best[upd] = L[upd]; bb[upd] = b
    for _ in range(10):                                       # safeguarded Newton
        L, d1, d2 = out_loss_and_derivs(m + bb[:, None], s, x)
        g, h = d1.mean(1), d2.mean(1)
        step = np.where(h > 1e-8, -g / np.maximum(h, 1e-8), -0.05 * np.sign(g))
        step = np.clip(step, -0.1, 0.1)
        cand = bb + step
        Lc = out_loss_and_derivs(m + cand[:, None], s, x)[0].mean(1)
        ok = Lc <= L.mean(1)
        bb = np.where(ok, cand, bb)
    return out_loss_and_derivs(m + bb[:, None], s, x)[0].mean(1), bb


def landscape(X1, X2, sigma, theta=TH):
    l1, b1 = profiled(theta, X1, X2, sigma, 0)
    l2, b2 = profiled(theta, X1, X2, sigma, 1)
    return l1 + ETA * l2


def analyse_pair(args):
    i, j, X1, X2 = args
    rows = []
    for s in SIGMAS:
        Fv = landscape(X1, X2, s)
        k = int(np.argmin(Fv))
        # refine around the global grid minimum (golden section on theta)
        a, b = TH[(k - 1) % len(TH)], TH[(k + 1) % len(TH)]
        if b < a: a, b = TH[k] - (TH[1] - TH[0]), TH[k] + (TH[1] - TH[0])
        gr = (np.sqrt(5) - 1) / 2
        for _ in range(30):
            c1, c2 = b - gr * (b - a), a + gr * (b - a)
            f1, f2 = landscape(X1, X2, s, np.array([c1, c2]))
            if f1 < f2: b = c2
            else: a = c1
        t_star = 0.5 * (a + b); F_star = float(landscape(X1, X2, s, np.array([t_star]))[0])
        if F_star > Fv[k]: t_star, F_star = float(TH[k]), float(Fv[k])
        sector = np.abs(TH) < np.pi / 4
        idx = np.where(sector)[0]
        mins = [int(t) for t in idx if Fv[t] < Fv[t - 1] and Fv[t] < Fv[(t + 1) % len(TH)]]
        F_mono = float(landscape(X1, X2, s, np.array([0.0]))[0])
        rows.append(dict(sigma=s, theta_star=float(t_star), F_star=F_star, F_mono=F_mono,
                         sector_minima_theta=[float(TH[t]) for t in mins],
                         sector_minima_F=[float(Fv[t]) for t in mins]))
    return dict(i=int(i), j=int(j), rows=rows)


if __name__ == "__main__":
    mode = sys.argv[1]
    X, zf, elig = load()
    Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
    if mode == "select":
        C = np.corrcoef(Xn[:, elig].T)
        iu = np.triu_indices(len(elig), 1)
        cc = C[iu]
        edges = np.quantile(cc, np.linspace(0, 1, 9))
        rng = np.random.default_rng(20261007)
        pairs = []
        for b in range(8):
            sel = np.where((cc >= edges[b]) & (cc <= edges[b + 1]))[0]
            for t in rng.choice(sel, PER_BIN, replace=False):
                a_, b_ = elig[iu[0][t]], elig[iu[1][t]]
                pairs.append(dict(i=int(a_), j=int(b_), corr=float(cc[t]),
                                  p_i=float(1 - zf[a_]), p_j=float(1 - zf[b_])))
        json.dump(dict(edges=edges.tolist(), n_images=int(X.shape[0]), n_eligible=int(len(elig)), pairs=pairs),
                  open(OUT + "/pairs.json", "w"), indent=1)
        print("selected", len(pairs), "edges", np.round(edges, 3))
    elif mode == "run":
        ch, n = int(sys.argv[2]), int(sys.argv[3])
        fn = f"{OUT}/part{ch}.json"
        if os.path.exists(fn): raise SystemExit("exists")
        P = json.load(open(OUT + "/pairs.json"))["pairs"][ch::n]
        t0 = time.time()
        with Pool(2) as pool:
            out = pool.map(analyse_pair, [(p["i"], p["j"], Xn[:, p["i"]], Xn[:, p["j"]]) for p in P])
        json.dump(out, open(fn, "w"), indent=1)
        print("chunk", ch, len(out), round(time.time() - t0, 1), "s")
    elif mode == "merge":
        n = int(sys.argv[2]); allr = []
        for ch in range(n): allr += json.load(open(f"{OUT}/part{ch}.json"))
        json.dump(allr, open(OUT + "/landscapes.json", "w"), indent=1); print("merged", len(allr))
