"""fig13: compression axis. (a) storage-instability thresholds vs eta for fixed-norm vs shared budget,
both branches, with bisection brackets. (b) n=4,m=2, eta=.5: partner weights vs p."""
import json, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fra2 import pc_theory
E = np.linspace(0.05, 0.95, 300)
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
ax[0].plot(E, [pc_theory(e) for e in E], "C0-", label="fixed norm, opposite-sign: p_c(η) (existing)")
ax[0].plot(E, 2 - 1 / E, "C0--", label="fixed norm, same-sign: 2 − 1/η")
ax[0].plot(E, 1 - np.sqrt((1 - E) / (1 + E)), "C3-", label="shared budget, opposite: 1 − √((1−η)/(1+η))")
ax[0].plot(E, (3 * E - 1) / (E + 1), "C3--", label="shared budget, same-sign: (3η−1)/(η+1)")
for f in ["results/compression/transition_bisection.json", "results/compression/bisection_eta0.3.json", "results/compression/bisection_eta0.7_same_sign.json"]:
    r = json.load(open(f)); e = r.get("eta", 0.5)
    ax[0].plot([e], [np.mean(r["bracket"])], "ko", ms=7)
ax[0].plot([], [], "ko", label="numerical bisection, n=4, m=2 (bracket < 1e-3)")
ax[0].plot([2 / 3], [0.5], "k*", ms=12, label="bicritical (2/3, 1/2) = manuscript endpoint")
ax[0].set(xlim=(0.05, 0.95), ylim=(0, 1), xlabel="importance η of the weak features", ylabel="frequency p below which a partner is stored",
          title="(a) storage thresholds: resource convention moves them")
ax[0].legend(fontsize=6.5)
R = json.load(open("results/compression/n4_m2_eta1.0-1.0-0.5-0.5_c0.0.json"))
ps = [r["p"] for r in R]
def partner_norms(W):
    W = np.array(W); return sorted([np.linalg.norm(W[:, 2]), np.linalg.norm(W[:, 3])], reverse=True)
pn = np.array([partner_norms(r["W"]) for r in R])
ax[1].plot(ps, pn[:, 0], "o-", label="larger partner norm")
ax[1].plot(ps, pn[:, 1], "s-", label="smaller partner norm")
ax[1].axvline(pc_theory(0.5), color="C0", ls=":", label="fixed-norm p_c = 0.382")
ax[1].axvline(1 - np.sqrt(1 / 3), color="C3", ls=":", label="shared p_c = 0.4226")
ax[1].set(xlabel="p", ylabel="weak-feature column norm", title="(b) n=4, m=2, η=½: mono → one partner → two partners")
ax[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig13_compression.png"); print("ok")
