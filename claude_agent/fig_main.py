"""fig_main: a single 2x2 paper figure assembled from saved results only.
(a) toy: selected angle vs p for several correlations c (field picture, sigma=0)
(b) toy: noise-trained selection becomes first order (sigma = 0, .003, .01, .03) with zero-fit prediction lines
(c) real: ResNet18 layer4 pairs, selected theta* vs correlation, coloured by activity (sign rule + two branches)
(d) real: ResNet18 layer4 triples, storage fractions per c13 bin."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fra2 import pc_theory, K_C_theory
PC = pc_theory(0.5); K, C = K_C_theory(0.5); A3 = 0.8315564147061506
fig, ax = plt.subplots(2, 2, figsize=(10, 7.4))
d = json.load(open("results/corr.json"))["rows"]; cs = sorted(set(r["c"] for r in d)); cm = plt.cm.coolwarm
for i, c in enumerate(cs):
    rr = sorted([r for r in d if r["c"] == c and "error" not in r], key=lambda r: r["p"])
    ax[0, 0].plot([r["p"] for r in rr], [r["t_star"] for r in rr], "-", color=cm(i / (len(cs) - 1)), lw=2.5 if c == 0 else 1.2, label=f"c={c:+g}")
ax[0, 0].axvline(PC, color="k", ls=":", lw=0.8); ax[0, 0].axhline(0, color="k", lw=0.4)
ax[0, 0].set(xlabel="feature frequency p", ylabel="selected angle θ* (0 = mono)", title="(a) correlation acts as a field (clean)")
ax[0, 0].legend(fontsize=6, ncol=2)
n = json.load(open("results/noise.json"))["rows"]
rr = sorted([r for r in d if r["c"] == 0.0], key=lambda r: r["p"])
ax[0, 1].plot([r["p"] for r in rr], [r["t_star"] for r in rr], "k-", lw=2, label="σ=0 (continuous)")
for s in [0.003, 0.01, 0.03]:
    q = sorted([r for r in n if r["sigma"] == s and r["p"] >= 0.25], key=lambda r: r["p"])
    l = ax[0, 1].plot([r["p"] for r in q], [r["t_star"] for r in q], "o-", ms=2.5, label=f"trained with σ={s}")[0]
    ax[0, 1].axvline(PC - A3 * s ** (2 / 3), color=l.get_color(), ls=":", lw=0.9)
ax[0, 1].set(xlim=(0.25, 0.42), ylim=(-0.2, 0.01), xlabel="p", ylabel="θ*",
             title="(b) training noise → first-order jump\n(dotted: p_c − (B_cal/C)^{1/3} σ^{2/3}, no fit)")
ax[0, 1].legend(fontsize=7)
P = {(p["i"], p["j"]): p for p in json.load(open("results/real/pairs.json"))["pairs"]}
L = json.load(open("results/real/landscapes.json"))
corr = np.array([P[(r["i"], r["j"])]["corr"] for r in L]); pbar = np.array([0.5 * (P[(r["i"], r["j"])]["p_i"] + P[(r["i"], r["j"])]["p_j"]) for r in L])
th = np.array([[x for x in r["rows"] if x["sigma"] == 0.005][0]["theta_star"] for r in L])
sc = ax[1, 0].scatter(corr, th, c=pbar, cmap="viridis", s=12)
ax[1, 0].axhline(0, color="k", lw=0.4); ax[1, 0].axvline(0, color="k", lw=0.4)
ax[1, 0].set(xlabel="channel-pair correlation", ylabel="selected θ*", title="(c) ResNet18 layer-4 pairs: sign rule 37/37, 17/17")
plt.colorbar(sc, ax=ax[1, 0], label="mean activity")
S = json.load(open("results/real_triples/solutions.json"))
B = [[-0.2, -0.05], [-0.05, -0.01], [-0.01, 0.01], [0.01, 0.05], [0.05, 0.15], [0.15, 0.6]]
st = lambda w, j: abs(w[j]) / max(abs(x) for x in w) > 0.05
f2 = [np.mean([st(s["w"], 1) for s in S if s["bin"] == b]) for b in B]
f3 = [np.mean([st(s["w"], 2) for s in S if s["bin"] == b]) for b in B]
f23 = [np.mean([st(s["w"], 1) and st(s["w"], 2) for s in S if s["bin"] == b]) for b in B]
x = np.arange(len(B))
ax[1, 1].bar(x - 0.27, f2, 0.27, label="uncorrelated partner stored")
ax[1, 1].bar(x, f3, 0.27, label="correlated channel stored")
ax[1, 1].bar(x + 0.27, f23, 0.27, label="all three stored")
ax[1, 1].set_xticks(x); ax[1, 1].set_xticklabels([f"[{a},{b})" for a, b in B], fontsize=7)
ax[1, 1].set(xlabel="correlation of third channel with dominant channel", ylabel="fraction of 20 triples",
             title="(d) layer-4 triples: correlation decides packing")
ax[1, 1].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig_main.png", dpi=160); fig.savefig("figures/fig_main.pdf"); print("ok")
