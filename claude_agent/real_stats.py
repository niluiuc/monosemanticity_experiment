"""Significance of the registered real-data contrasts, with dependence between pairs handled by a
channel-cluster bootstrap (resample channels, keep pairs whose both channels are drawn).
P2 (bistability low vs high |corr| tercile) and post-hoc branch-coexistence asymmetry (pos vs neg corr),
for both datasets; triples T3. Also Fisher exact tests (which ignore the dependence)."""
import json, numpy as np
from scipy.stats import fisher_exact
rng = np.random.default_rng(1)
out = {}
for name, d in [("layer4", "results/real"), ("logits", "results/real_logits")]:
    P = {(p["i"], p["j"]): p for p in json.load(open(d + "/pairs.json"))["pairs"]}
    L = json.load(open(d + "/landscapes.json"))
    corr = np.array([P[(r["i"], r["j"])]["corr"] for r in L]); ij = np.array([(r["i"], r["j"]) for r in L])
    bist = np.array([any(len(x["sector_minima_theta"]) >= 2 for x in r["rows"]) for r in L])
    co = np.array([any(any(t < -0.1 for t in x["sector_minima_theta"]) and any(t > -0.05 for t in x["sector_minima_theta"]) for x in r["rows"]) for r in L])
    ac = np.abs(corr); t1, t2 = np.quantile(ac, [1/3, 2/3]); lo, hi = ac <= t1, ac > t2
    diff = bist[lo].mean() - bist[hi].mean()
    # coexistence asymmetry among weakly correlated pairs |corr|<0.1: rate for corr>0 minus corr<0
    w = ac < 0.1; asym = co[w & (corr > 0)].mean() - co[w & (corr < 0)].mean()
    chans = np.unique(ij)
    bs_d, bs_a = [], []
    for _ in range(2000):
        draw = set(rng.choice(chans, len(chans), replace=True))
        keep = np.array([(a in draw) and (b in draw) for a, b in ij])
        if keep.sum() < 20: continue
        l, h = lo & keep, hi & keep
        if l.sum() and h.sum(): bs_d.append(bist[l].mean() - bist[h].mean())
        wp, wn = w & keep & (corr > 0), w & keep & (corr < 0)
        if wp.sum() and wn.sum(): bs_a.append(co[wp].mean() - co[wn].mean())
    out[name] = dict(
        P2_diff=float(diff), P2_cluster_bootstrap_CI95=np.percentile(bs_d, [2.5, 97.5]).tolist(),
        P2_fisher_p=float(fisher_exact([[bist[lo].sum(), (~bist[lo]).sum()], [bist[hi].sum(), (~bist[hi]).sum()]])[1]),
        coexist_asym_weakcorr=float(asym), coexist_asym_cluster_bootstrap_CI95=np.percentile(bs_a, [2.5, 97.5]).tolist(),
        n_boot=[len(bs_d), len(bs_a)])
S = json.load(open("results/real_triples/solutions.json"))
st = lambda w, j: abs(w[j]) / max(abs(x) for x in w) > 0.05
strong = [s for s in S if abs(s["c13"]) >= 0.05]; zero = [s for s in S if s["bin"] == [-0.01, 0.01]]
a = sum(st(s["w"], 2) for s in strong); b = sum(st(s["w"], 2) for s in zero)
out["triples_T3_fisher_p"] = float(fisher_exact([[a, len(strong) - a], [b, len(zero) - b]])[1])
print(json.dumps(out, indent=1)); json.dump(out, open("results/real_stats.json", "w"), indent=1)
