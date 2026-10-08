"""fig_main_v2 (3x2): adds (e) the certified global branch map with the first-order line and
(f) compression thresholds, to the four panels of fig_main. Saved results only."""
import json, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from fra2 import pc_theory, K_C_theory
exec(open("fig_main.py").read().split("fig, ax = plt.subplots")[0])   # reuse imports/constants
PC = pc_theory(0.5); K, C = K_C_theory(0.5)
fig = plt.figure(figsize=(14, 7.6))
# re-draw panels a-d by running fig_main's body on a 2x3 grid
src = open("fig_main.py").read().split("fig, ax = plt.subplots(2, 2, figsize=(10, 7.4))")[1].split("fig.tight_layout()")[0]
axs = [fig.add_subplot(2, 3, k) for k in (1, 2, 4, 5)]
ax = np.array([[axs[0], axs[1]], [axs[2], axs[3]]], dtype=object)
exec(src)
# (e) certificate map
ae = fig.add_subplot(2, 3, 3)
R = [json.load(open(f)) for f in glob.glob("results/certificate_v2/p*.json")]
col = {"opposite (theta<0)": "C0", "same-sign (theta>0)": "C3", "contains/straddles 0": "0.6"}
for side, cc in col.items():
    rr = [r for r in R if r["certified_side"] == side]
    ae.scatter([r["p"] for r in rr], [r["c"] for r in rr], c=cc, s=40, label=side.replace(" (theta<0)", " (θ<0)").replace(" (theta>0)", " (θ>0)").replace("contains/straddles 0", "mono / unresolved"))
pp = np.linspace(0.24, PC, 100); ee = PC - pp
ae.plot(pp, 9 * C * ee ** 2 / (16 * 0.5 * pp * (1 - pp) * K), "k--", lw=0.9, label="first-order line (leading order)")
co = json.load(open("results/coexistence_clean.json"))
ae.plot([r["p"] for r in co], [np.mean(r["c_star_bracket"]) for r in co], "k^", ms=5, label="bisection")
ae.set_yscale("symlog", linthresh=0.002); ae.axhline(0, color="k", lw=0.4)
ae.set(xlabel="p", ylabel="correlation c (symlog)", title="(e) certified global branch (Lipschitz B&B)"); ae.legend(fontsize=6)
# (f) compression thresholds
af = fig.add_subplot(2, 3, 6)
E = np.linspace(0.05, 0.95, 300)
af.plot(E, [pc_theory(e) for e in E], "C0-", label="fixed norm, opposite")
af.plot(E, 2 - 1 / E, "C0--", label="fixed norm, same-sign")
af.plot(E, 1 - np.sqrt((1 - E) / (1 + E)), "C3-", label="shared budget, opposite")
af.plot(E, (3 * E - 1) / (E + 1), "C3--", label="shared budget, same-sign")
for f in ["results/compression/transition_bisection.json", "results/compression/bisection_eta0.3.json", "results/compression/bisection_eta0.7_same_sign.json"]:
    r = json.load(open(f)); af.plot([r.get("eta", 0.5)], [np.mean(r["bracket"])], "ko", ms=6)
af.plot([2 / 3], [0.5], "k*", ms=11, label="bicritical = manuscript endpoint")
af.set(xlim=(0.05, 0.95), ylim=(0, 1), xlabel="η", ylabel="storage threshold p", title="(f) compression thresholds (n=4, m=2)")
af.legend(fontsize=6)
fig.tight_layout(); fig.savefig("figures/fig_main_v2.png", dpi=150); fig.savefig("figures/fig_main_v2.pdf"); print("ok")
