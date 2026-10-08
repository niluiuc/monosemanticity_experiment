"""POST-HOC descriptive refinement of P2 (labelled as such): count only 'branch coexistence',
i.e. a sector minimum on the opposite-sign branch (theta < -0.1) together with one at
near-mono / same-sign (theta > -0.05), at some sigma. This excludes multiple minima within one
branch caused by finite-sample roughness. Both datasets."""
import json, numpy as np
res = {}
for name, out in [("layer4", "results/real"), ("logits", "results/real_logits")]:
    P = {(p["i"], p["j"]): p for p in json.load(open(out + "/pairs.json"))["pairs"]}
    L = json.load(open(out + "/landscapes.json"))
    corr = np.array([P[(r["i"], r["j"])]["corr"] for r in L])
    co = np.array([any(any(t < -0.1 for t in x["sector_minima_theta"]) and any(t > -0.05 for t in x["sector_minima_theta"])
                       for x in r["rows"]) for r in L])
    ac = np.abs(corr); t1, t2 = np.quantile(ac, [1/3, 2/3])
    lo, hi = ac <= t1, ac > t2; mid = ~lo & ~hi
    res[name] = dict(low=[int(co[lo].sum()), int(lo.sum())], mid=[int(co[mid].sum()), int(mid.sum())],
                     high=[int(co[hi].sum()), int(hi.sum())],
                     corr_of_coexisting=sorted(np.round(corr[co], 3).tolist()))
    print(name, res[name])
json.dump(res, open("results/real_branch_coexistence_posthoc.json", "w"), indent=1)
