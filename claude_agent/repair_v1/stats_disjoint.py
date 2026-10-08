"""R3 — replaces real_stats.py's invalid 'channel bootstrap' (set(rng.choice(...)) dropped
multiplicities). Inference here uses CHANNEL-DISJOINT subsets: within a subset no channel occurs in
two units (pairs or triples), so units share no channel and Fisher's exact test is applied to units
that do not overlap. A maximal disjoint subset is built greedily in a random order; this is repeated
for 1000 seeded orders. Every individual test is a valid test on its subset; the distribution of
p-values over orders is reported descriptively (median, 90th percentile, fraction < .05), together
with the FIRST order (seed 0), which is the pre-specified primary test.
Remaining caveat (not fixed by disjointness): all channels come from one network, so different
channels are not independent draws from a population of networks.
Run from claude_agent/:  python repair_v1/stats_disjoint.py"""
import os, sys, json
import numpy as np
from scipy.stats import fisher_exact
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def greedy_disjoint(units, rng):
    order = rng.permutation(len(units)); used = set(); keep = []
    for k in order:
        ch = units[k]
        if not (set(ch) & used):
            keep.append(k); used |= set(ch)
    return np.array(sorted(keep))


def fisher(a1, n1, a2, n2, alt):
    return float(fisher_exact([[a1, n1 - a1], [a2, n2 - a2]], alternative=alt)[1])


def summarize(ps, first):
    ps = np.array(ps)
    return dict(primary_seed0=first, median=float(np.median(ps)), p90=float(np.quantile(ps, 0.9)),
                frac_below_0p05=float(np.mean(ps < 0.05)), n_orders=len(ps))


out = {}
for name, d in [("layer4", "real"), ("logits", "real_logits")]:
    P = {(p["i"], p["j"]): p for p in json.load(open(os.path.join(ROOT, "results", d, "pairs.json")))["pairs"]}
    L = json.load(open(os.path.join(ROOT, "results", d, "landscapes.json")))
    units = [(r["i"], r["j"]) for r in L]
    corr = np.array([P[u]["corr"] for u in units])
    bist = np.array([any(len(x["sector_minima_theta"]) >= 2 for x in r["rows"]) for r in L])
    co = np.array([any(any(t < -0.1 for t in x["sector_minima_theta"]) and any(t > -0.05 for t in x["sector_minima_theta"])
                       for x in r["rows"]) for r in L])
    th0 = np.array([[x for x in r["rows"] if x["sigma"] == 0.005][0]["theta_star"] for r in L])
    ac = np.abs(corr); t1, t2 = np.quantile(ac, [1 / 3, 2 / 3])   # terciles fixed on the full set
    lo, hi = ac <= t1, ac > t2
    weak = ac < 0.1
    P2, AS, sizes = [], [], []
    sign_neg, sign_pos = [], []
    for seed in range(1000):
        k = greedy_disjoint(units, np.random.default_rng(seed)); m = np.zeros(len(units), bool); m[k] = True
        sizes.append(int(m.sum()))
        a1, n1 = int(bist[m & lo].sum()), int((m & lo).sum()); a2, n2 = int(bist[m & hi].sum()), int((m & hi).sum())
        P2.append(fisher(a1, n1, a2, n2, "greater"))
        b1, m1 = int(co[m & weak & (corr > 0)].sum()), int((m & weak & (corr > 0)).sum())
        b2, m2 = int(co[m & weak & (corr < 0)].sum()), int((m & weak & (corr < 0)).sum())
        AS.append(fisher(b1, m1, b2, m2, "greater"))
        neg = m & (corr < -0.05); pos = m & (corr > 0.15)
        sign_neg.append((int((th0[neg] < 0).sum()), int(neg.sum()))); sign_pos.append((int((th0[pos] > 0).sum()), int(pos.sum())))
        if seed == 0:
            first = dict(P2=(a1, n1, a2, n2), asym=(b1, m1, b2, m2))
    out[name] = dict(n_pairs=len(units), disjoint_subset_size=dict(min=min(sizes), median=float(np.median(sizes)), max=max(sizes)),
                     P2_bistability_low_vs_high=summarize(P2, P2[0]), P2_counts_seed0=first["P2"],
                     posthoc_asymmetry_weakcorr=summarize(AS, AS[0]), asym_counts_seed0=first["asym"],
                     sign_rule_all_orders_exact=bool(all(a == n for a, n in sign_neg) and all(a == n for a, n in sign_pos)))

for name, d in [("layer4", "real_triples"), ("logits", "real_triples_logits")]:
    S = json.load(open(os.path.join(ROOT, "results", d, "solutions.json")))
    units = [(s["i"], s["j"], s["k"]) for s in S]
    st = lambda w, j: abs(w[j]) / max(abs(x) for x in w) > 0.05
    c13 = np.array([s["c13"] for s in S]); bins = [tuple(s["bin"]) for s in S]
    s2 = np.array([st(s["w"], 1) for s in S]); s3 = np.array([st(s["w"], 2) for s in S]); s23 = s2 & s3
    strong = np.abs(c13) >= 0.05; zero = np.array([b == (-0.01, 0.01) for b in bins])
    T3, T4, T5, sizes = [], [], [], []
    for seed in range(1000):
        k = greedy_disjoint(units, np.random.default_rng(seed)); m = np.zeros(len(units), bool); m[k] = True; sizes.append(int(m.sum()))
        T3.append(fisher(int(s3[m & strong].sum()), int((m & strong).sum()), int(s3[m & zero].sum()), int((m & zero).sum()), "greater"))
        pos, neg = m & (c13 >= 0.05), m & (c13 <= -0.05)
        T4.append(fisher(int(s23[pos].sum()), int(pos.sum()), int(s23[neg].sum()), int(neg.sum()), "greater"))
        bn = m & np.array([b == (-0.2, -0.05) for b in bins]); bp = m & np.array([b == (0.15, 0.6) for b in bins])
        T5.append(fisher(int(s2[bp].sum()), int(bp.sum()), int(s2[bn].sum()), int(bn.sum()), "greater"))
    out["triples_" + name] = dict(n=len(units), disjoint_subset_size=dict(min=min(sizes), median=float(np.median(sizes)), max=max(sizes)),
                                  T3=summarize(T3, T3[0]), T4=summarize(T4, T4[0]), T5=summarize(T5, T5[0]),
                                  note="T4/T5 were registered in advance only for logits; for layer4 they are post hoc")
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "results", "stats_disjoint.json"), "w"), indent=1)
