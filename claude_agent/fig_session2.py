"""fig10: session-2 theory checks. (a) mono curvature kappa_0(p) vs finite differences;
(b) noise-trained transition: eps_train / prediction vs sigma at 4 eta; (c) endpoint |c_e| vs sigma."""
import json, glob, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from spinodal import kappa0
fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
pp = np.linspace(0.15, 0.40, 200)
ax[0].plot(pp, [kappa0(p, 0.5) for p in pp], "k-", label="kappa_0(p) = pq[p+qPhi(z_p)-eta]")
for f, mk in [("results/resultB/stiff_s0.001.json", "o"), ("results/resultB/stiff_s0.01.json", "s"), ("results/resultB/stiff_s0.03.json", "^")]:
    r = json.load(open(f)); k = [x for x in r[0] if x.startswith("kappa_minus")][0]
    ax[0].plot([x["p"] for x in r], [x[k] for x in r], mk, label=f"finite diff., sigma={r[0]['sigma']}")
ax[0].axhline(0, color="gray", lw=0.5); ax[0].axvline(0.27911, color="r", ls=":", lw=0.8, label="spinodal p_sp=0.279")
ax[0].axvline(0.38197, color="b", ls=":", lw=0.8, label="p_c")
ax[0].set(xlabel="p", ylabel="curvature at mono", title="(a) mono is metastable on [p_sp, p_c) for any small sigma"); ax[0].legend(fontsize=6)
for f in sorted(glob.glob("results/resultB/bisect_*.json")):
    r = json.load(open(f)); mt = np.mean(r["eps_trained_bracket"]); mf = np.mean(r["eps_fixed_bracket"])
    ax[1].plot(r["sigma"], mt / r["eps_pred"], "o", color={0.48: "C0", 0.5: "C1", 0.52: "C2"}.get(round(r["eta"], 2), "C3"))
    ax[1].plot(r["sigma"], mf / r["eps_pred"], "x", color={0.48: "C0", 0.5: "C1", 0.52: "C2"}.get(round(r["eta"], 2), "C3"))
for e, cc in [(0.48, "C0"), (0.5, "C1"), (0.52, "C2"), (2 / 3, "C3")]:
    ax[1].plot([], [], "o", color=cc, label=f"eta={e:.3g}")
ax[1].plot([], [], "kx", label="fixed clean encoder (existing calibrated policy)"); ax[1].plot([], [], "ko", label="noise-trained (theta re-optimised)")
ax[1].axhline(1, color="k", lw=0.7); ax[1].set(xscale="log", xlabel="training noise sigma", ylabel="eps* / (B_cal/C)^(1/3) sigma^(2/3)",
                                                title="(b) transition location vs zero-fit prediction"); ax[1].legend(fontsize=6)
s = json.load(open("results/endpoint_refined/summary.json"))
ax[2].loglog(s["sigma"], s["abs_c_e"], "o-", label="|c_e| (refined, +-5%)")
ss = np.logspace(-3, -1.4, 20)
ax[2].loglog(ss, 0.19 * ss, "k--", lw=0.8, label="0.19 sigma (small-sigma trend)")
ax[2].loglog(ss, 0.163 * ss, "r-", lw=1.0, label="theory: sigma*maxPhi'/(2 eta p q) = 0.16 sigma (sigma->0)")
ax[2].set(xlabel="training noise sigma", ylabel="|c_e|", title="(c) critical endpoint on the c<0 side"); ax[2].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig10_session2_theory_checks.png"); print("ok")
