"""fig11: storage phase map for three features in one dimension vs (p, c13)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
R = json.load(open("results/three_feature/packing_map.json"))
cs = sorted(set(r["c13"] for r in R)); ps = sorted(set(r["p"] for r in R))
lab = {"mono": 0, "{1,2-}": 1, "{1,3+}": 2, "{1,3-}": 3, "{1,2-,3+}": 4, "{1,2-,3-}": 5}
def phase(w):
    s2 = "2-" if w[1] < -1e-3 else ("2+" if w[1] > 1e-3 else None)
    s3 = "3-" if w[2] < -1e-3 else ("3+" if w[2] > 1e-3 else None)
    k = "{" + ",".join(["1"] + [x for x in (s2, s3) if x]) + "}"
    return lab.get(k if (s2 or s3) else "mono", -1)
M = np.full((len(ps), len(cs)), np.nan); W3 = np.full_like(M, np.nan)
for r in R:
    i, j = ps.index(r["p"]), cs.index(r["c13"]); M[i, j] = phase(r["w"]); W3[i, j] = r["w"][2]
cmap = ListedColormap(["#dddddd", "#9ecae1", "#fdae6b", "#a1d99b", "#e6550d", "#31a354"])
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
im = ax[0].imshow(M, origin="lower", aspect="auto", cmap=cmap, vmin=-0.5, vmax=5.5)
ax[0].set_xticks(range(len(cs))); ax[0].set_xticklabels([str(c) for c in cs], fontsize=7)
ax[0].set_yticks(range(len(ps))); ax[0].set_yticklabels([f"{p:.3f}" for p in ps], fontsize=7)
ax[0].set(xlabel="corr(feature1, feature3) = c13", ylabel="p", title="stored set (signs relative to feature 1)")
cb = plt.colorbar(im, ax=ax[0], ticks=range(6)); cb.ax.set_yticklabels(list(lab), fontsize=7)
for p_, mk in [(0.1, "o-"), (0.2, "s-"), (0.3, "^-")]:
    rr = sorted([r for r in R if abs(r["p"] - p_) < 1e-9], key=lambda r: r["c13"])
    ax[1].plot([r["c13"] for r in rr], [r["w"][2] for r in rr], mk, label=f"w3, p={p_}")
    ax[1].plot([r["c13"] for r in rr], [r["w"][1] for r in rr], mk, alpha=0.35, label=f"w2, p={p_}")
ax[1].axhline(0, color="k", lw=0.5); ax[1].axvline(0, color="k", lw=0.5)
ax[1].set(xlabel="c13", ylabel="weight", title="feature 3 enters with the sign of c13;\nstrong |c13| displaces feature 2"); ax[1].legend(fontsize=6, ncol=2)
fig.tight_layout(); fig.savefig("figures/fig11_three_feature_packing.png"); print("ok")
