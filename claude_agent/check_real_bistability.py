"""Robustness check of P2: recompute the landscape at the first bistable sigma with a finer bias
profile (121-point grid, 30 Newton steps) and report minima, their theta, depth difference and
barrier height. Spurious minima from profiling error would vanish or have ~1e-9 barriers."""
import json, numpy as np
import real_pairs as R
R_bg_fine = np.linspace(-1.5, 1.5, 121)
def profiled_fine(theta, X1, X2, sigma, out):
    w1, w2 = np.cos(theta)[:, None], np.sin(theta)[:, None]
    wi = w1 if out == 0 else w2; x = (X1 if out == 0 else X2)[None, :]
    m = wi * (w1 * X1[None, :] + w2 * X2[None, :]); s = np.maximum(np.abs(wi) * sigma, 1e-12)
    best = np.full(theta.shape, np.inf); bb = np.zeros(theta.shape)
    for b in R_bg_fine:
        L = R.out_loss_and_derivs(m + b, s, x)[0].mean(1); u = L < best; best[u] = L[u]; bb[u] = b
    for _ in range(30):
        L, d1, d2 = R.out_loss_and_derivs(m + bb[:, None], s, x); g, h = d1.mean(1), d2.mean(1)
        cand = bb + np.clip(np.where(h > 1e-8, -g / np.maximum(h, 1e-8), -0.05 * np.sign(g)), -0.1, 0.1)
        Lc = R.out_loss_and_derivs(m + cand[:, None], s, x)[0].mean(1); bb = np.where(Lc <= L.mean(1), cand, bb)
    return R.out_loss_and_derivs(m + bb[:, None], s, x)[0].mean(1)
X, zf, el = R.load(); Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
P = {(p["i"], p["j"]): p for p in json.load(open(R.OUT + "/pairs.json"))["pairs"]}
L = json.load(open(R.OUT + "/landscapes.json"))
th = np.linspace(-np.pi / 4, np.pi / 4, 361)
out = []
cands = [r for r in L if any(len(x["sector_minima_theta"]) >= 2 for x in r["rows"])]
cands = sorted(cands, key=lambda r: abs(P[(r["i"], r["j"])]["corr"]))[:8] + sorted(cands, key=lambda r: -abs(P[(r["i"], r["j"])]["corr"]))[:3]
for r in cands:
    s = [x["sigma"] for x in r["rows"] if len(x["sector_minima_theta"]) >= 2][0]
    X1, X2 = Xn[:, r["i"]], Xn[:, r["j"]]
    Fv = profiled_fine(th, X1, X2, s, 0) + 0.5 * profiled_fine(th, X1, X2, s, 1)
    mins = [k for k in range(1, len(th) - 1) if Fv[k] < Fv[k - 1] and Fv[k] < Fv[k + 1]]
    rec = dict(i=r["i"], j=r["j"], corr=P[(r["i"], r["j"])]["corr"], sigma=s, n_min_fine=len(mins),
               minima_theta=[float(th[k]) for k in mins])
    if len(mins) >= 2:
        a, b = mins[0], mins[-1]
        rec["depth_diff"] = float(abs(Fv[a] - Fv[b])); rec["barrier"] = float(Fv[a:b + 1].max() - max(Fv[a], Fv[b]))
    out.append(rec); print(rec, flush=True)
json.dump(out, open(R.OUT + "/bistability_check.json", "w"), indent=1)
