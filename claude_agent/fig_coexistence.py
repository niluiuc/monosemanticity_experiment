"""fig9: where in correlation do real pairs show opposite-sign / same-sign branch coexistence?
(post-hoc descriptive; compare with the toy phase diagram fig5: first-order line on the c>0 side,
only a short extension onto c<0 under noise)."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))
for a, (name, out) in zip(ax, [("ResNet18 layer4 channels", "results/real"), ("ResNet18 class logits (replication)", "results/real_logits")]):
    P = {(p["i"], p["j"]): p for p in json.load(open(out + "/pairs.json"))["pairs"]}
    L = json.load(open(out + "/landscapes.json"))
    corr = np.array([P[(r["i"], r["j"])]["corr"] for r in L])
    co = np.array([any(any(t < -0.1 for t in x["sector_minima_theta"]) and any(t > -0.05 for t in x["sector_minima_theta"]) for x in r["rows"]) for r in L])
    bins = np.linspace(-0.2, 0.25, 19)
    a.hist(np.clip(corr, -0.2, 0.25), bins=bins, color="lightgray", label="all sampled pairs")
    a.hist(np.clip(corr[co], -0.2, 0.25), bins=bins, color="C3", label="branch coexistence (some sigma)")
    a.axvline(0, color="k", lw=0.7); a.set(xlabel="pair correlation (clipped to [-0.2,0.25])", ylabel="pairs", title=name)
    a.legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig9_real_coexistence_vs_corr.png"); print("ok")
