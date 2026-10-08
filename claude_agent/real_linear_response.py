"""Quantitative real-data test of the field picture (S1/S2 transferred to continuous features).
For each saved real pair (both datasets), measure at mono (theta=0, sigma=0.005):
   h      = -(F(+d) - F(-d)) / (2d)              (the field; compare with 2*eta*Cov(X1,X2) from the bridge proof)
   kappa+ = (F(+d) - F(0) - (-h) d) / d^2       (same-sign stiffness)
and predict the same-sign weight by linear response theta_pred = h / (2 kappa+).
Compare with the globally selected theta* (saved, sigma=0.005) for pairs that selected the same-sign branch.
This is a test of local -> global: the prediction uses only derivatives at mono.
Usage: REAL_DATASET=layer4|logits python real_linear_response.py"""
import json, os
import numpy as np
import real_pairs as R

d = 2e-3
X, zf, el = R.load(); Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
P = {(p["i"], p["j"]): p for p in json.load(open(R.OUT + "/pairs.json"))["pairs"]}
L = json.load(open(R.OUT + "/landscapes.json"))
rows = []
for r in L:
    X1, X2 = Xn[:, r["i"]], Xn[:, r["j"]]
    Fm, F0, Fp = R.landscape(X1, X2, 0.005, np.array([-d, 0.0, d]))
    h = -(Fp - Fm) / (2 * d)
    kap = (Fp - F0 + h * d) / d ** 2
    cov = float(np.mean((X1 - X1.mean()) * (X2 - X2.mean())))
    th = [x for x in r["rows"] if x["sigma"] == 0.005][0]["theta_star"]
    rows.append(dict(i=r["i"], j=r["j"], corr=P[(r["i"], r["j"])]["corr"], h=float(h), h_bridge=2 * R.ETA * cov,
                     kappa_plus=float(kap), theta_pred=float(h / (2 * kap)) if kap > 0 else None, theta_star=th))
same = [x for x in rows if x["theta_star"] > 0 and x["theta_pred"] is not None and x["h"] > 0]
err = np.array([x["theta_pred"] - x["theta_star"] for x in same])
rel = np.array([abs(x["theta_pred"] - x["theta_star"]) / x["theta_star"] for x in same])
hb = np.array([[x["h"], x["h_bridge"]] for x in rows])
out = dict(dataset=os.environ.get("REAL_DATASET", "layer4"), n_pairs=len(rows), n_same_sign=len(same),
           field_vs_bridge_max_abs_diff=float(np.max(np.abs(hb[:, 0] - hb[:, 1]))),
           field_vs_bridge_corr=float(np.corrcoef(hb.T)[0, 1]),
           median_rel_err_same_sign=float(np.median(rel)), frac_within_20pct=float(np.mean(rel < 0.2)),
           corr_pred_vs_star=float(np.corrcoef([x["theta_pred"] for x in same], [x["theta_star"] for x in same])[0, 1]),
           rows=rows)
json.dump(out, open(R.OUT + "/linear_response.json", "w"), indent=1)
print({k: v for k, v in out.items() if k != "rows"})
