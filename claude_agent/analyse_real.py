"""Analysis of the real-activation test exactly as pre-registered in real_protocol.md
(plus clearly labelled descriptive extras). Writes results/real/analysis.json and figures/fig7_real_pairs.png."""
import json, os
OUT = "results/real" if os.environ.get("REAL_DATASET", "layer4") == "layer4" else "results/real_logits"
FIG = "figures/fig7_real_pairs.png" if OUT == "results/real" else "figures/fig8_real_logits_replication.png"
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

P = {(p["i"], p["j"]): p for p in json.load(open(OUT + "/pairs.json"))["pairs"]}
L = json.load(open(OUT + "/landscapes.json"))
rows = []
for r in L:
    meta = P[(r["i"], r["j"])]
    byS = {x["sigma"]: x for x in r["rows"]}
    rows.append(dict(corr=meta["corr"], pbar=0.5 * (meta["p_i"] + meta["p_j"]), byS=byS))
corr = np.array([r["corr"] for r in rows]); pbar = np.array([r["pbar"] for r in rows])
S = sorted(rows[0]["byS"])
th0 = np.array([r["byS"][S[0]]["theta_star"] for r in rows])
out = {}

# P1 -----------------------------------------------------------------------------
neg = corr < -0.05; pos = corr > 0.15; mid = ~neg & ~pos
out["P1_opposite_sign_rate_corr_lt_-0.05"] = [int((th0[neg] < 0).sum()), int(neg.sum())]
out["P1_same_sign_rate_corr_gt_0.15"] = [int((th0[pos] > 0).sum()), int(pos.sum())]
med = np.median(pbar[mid])
sparse, dense = mid & (pbar < med), mid & (pbar >= med)
def logistic_mid(mask):
    # descriptive: correlation at which the same-sign fraction crosses 1/2 (binned)
    cs, ys = corr[mask], (th0[mask] > 0).astype(float)
    o = np.argsort(cs); cs, ys = cs[o], ys[o]
    k = max(3, len(cs) // 6)
    centers = [cs[i:i + k].mean() for i in range(0, len(cs) - k + 1, k)]
    fr = [ys[i:i + k].mean() for i in range(0, len(cs) - k + 1, k)]
    return centers, fr
out["P1_middle_sparse_vs_dense"] = dict(median_pbar=float(med),
    sparse_same_sign_rate=[int((th0[sparse] > 0).sum()), int(sparse.sum())],
    dense_same_sign_rate=[int((th0[dense] > 0).sum()), int(dense.sum())],
    sparse_mean_corr=float(corr[sparse].mean()), dense_mean_corr=float(corr[dense].mean()))
# a fairer comparison of the threshold: logistic fit sign ~ a + b*corr + g*pbar over the middle band
from scipy.optimize import minimize
def nll(beta, c_, p_, y_):
    z = beta[0] + beta[1] * c_ + beta[2] * (p_ - p_.mean())
    return np.sum(np.logaddexp(0, z) - y_ * z)
ymid = (th0[mid] > 0).astype(float)
fit = minimize(nll, np.zeros(3), args=(corr[mid], pbar[mid], ymid), method="BFGS")
cov_ = fit.hess_inv
out["P1_logistic_middle"] = dict(beta=fit.x.tolist(), se=np.sqrt(np.diag(cov_)).tolist(),
    note="same-sign ~ b0 + b1*corr + b2*(pbar-mean). Prediction: b2 > 0 (denser pairs switch at lower corr).")

# P2 -----------------------------------------------------------------------------
bist = np.array([any(len(r["byS"][s]["sector_minima_theta"]) >= 2 for s in S) for r in rows])
ac = np.abs(corr); t1, t2 = np.quantile(ac, [1 / 3, 2 / 3])
lo, hi = ac <= t1, ac > t2
out["P2_bistable_rate_low_absCorr_tercile"] = [int(bist[lo].sum()), int(lo.sum())]
out["P2_bistable_rate_high_absCorr_tercile"] = [int(bist[hi].sum()), int(hi.sum())]
out["P2_bistable_rate_mid_tercile"] = [int(bist[~lo & ~hi].sum()), int((~lo & ~hi).sum())]
# jump size along sigma (descriptive)
jumps = np.array([np.max(np.abs(np.diff([r["byS"][s]["theta_star"] for s in S]))) for r in rows])
out["descriptive_max_theta_jump_median_low_vs_high"] = [float(np.median(jumps[lo])), float(np.median(jumps[hi]))]

# P3 -----------------------------------------------------------------------------
def ratio(t):  # weak/strong column ratio (registered metric was |tan|; both reported)
    tt = np.abs(np.tan(t)); return np.minimum(tt, 1 / np.maximum(tt, 1e-300))
tanS = {s: np.array([abs(np.tan(r["byS"][s]["theta_star"])) for r in rows]) for s in S}
ratS = {s: np.array([ratio(r["byS"][s]["theta_star"]) for r in rows]) for s in S}
out["P3_median_abs_tan_by_sigma"] = {str(s): float(np.median(tanS[s])) for s in S}
out["P3_median_weak_strong_ratio_by_sigma"] = {str(s): float(np.median(ratS[s])) for s in S}
out["P3_fraction_pairs_ratio_decreased_0.005_to_0.6"] = float(np.mean(ratS[S[-1]] < ratS[S[0]]))
# exact zero (mono) never occurs with nonzero covariance: smallest selected ratio
out["descriptive_min_ratio_clean"] = float(ratS[S[0]].min())
json.dump(out, open(OUT + "/analysis.json", "w"), indent=1)
for k, v in out.items(): print(k, v)

# figure -------------------------------------------------------------------------
fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
sc = ax[0].scatter(corr, th0, c=pbar, cmap="viridis", s=14)
ax[0].axhline(0, color="k", lw=0.5); ax[0].axvline(0, color="k", lw=0.5)
ax[0].set(xlabel="channel-pair correlation", ylabel="clean selected theta* (sigma=0.005)",
          title="P1: sign of shared weight follows correlation")
plt.colorbar(sc, ax=ax[0], label="mean activity p")
for lab, m in [("low |corr| tercile", lo), ("middle", ~lo & ~hi), ("high |corr| tercile", hi)]:
    ax[1].bar(lab, bist[m].mean())
ax[1].set(ylabel="fraction with 2 minima at some sigma", title="P2: bistability vs |corr|")
ax[1].tick_params(axis="x", labelsize=7)
ax[2].plot(S, [np.median(ratS[s]) for s in S], "o-", label="median weak/strong ratio")
ax[2].plot(S, [np.median(tanS[s]) for s in S], "s--", label="median |tan theta*| (registered)")
ax[2].set(xlabel="training code noise sigma (RMS units)", ylabel="storage of weak feature",
          title="P3: noise shrinks shared storage"); ax[2].legend(fontsize=7)
fig.tight_layout(); fig.savefig(FIG)
