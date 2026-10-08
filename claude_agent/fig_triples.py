"""fig12: real triples. Fraction storing feature 2 (uncorrelated), feature 3 (correlated with 1), and all three, per c13 bin."""
import json, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
S = json.load(open("results/real_triples/solutions.json"))
B = [[-0.2, -0.05], [-0.05, -0.01], [-0.01, 0.01], [0.01, 0.05], [0.05, 0.15], [0.15, 0.6]]
st = lambda w, j: abs(w[j]) / max(abs(x) for x in w) > 0.05
f2, f3, f23 = [], [], []
for b in B:
    rr = [s for s in S if s["bin"] == b]
    f2.append(np.mean([st(s["w"], 1) for s in rr])); f3.append(np.mean([st(s["w"], 2) for s in rr]))
    f23.append(np.mean([st(s["w"], 1) and st(s["w"], 2) for s in rr]))
x = np.arange(len(B)); lab = [f"[{a},{b})" for a, b in B]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ax.bar(x - 0.27, f2, 0.27, label="feature 2 stored (uncorrelated; always opposite-sign)")
ax.bar(x, f3, 0.27, label="feature 3 stored (sign = sign of c13 in 60/60 strong cases)")
ax.bar(x + 0.27, f23, 0.27, label="all three stored")
ax.set_xticks(x); ax.set_xticklabels(lab, fontsize=8); ax.set(xlabel="c13 = corr(channel 1, channel 3)", ylabel="fraction of 20 triples",
    title="ResNet18 layer4 triples: correlation decides packing")
ax.legend(fontsize=7); fig.tight_layout(); fig.savefig("figures/fig12_real_triples.png"); print("ok")
