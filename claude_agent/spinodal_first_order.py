"""S4 sharpened: curvature at mono under training noise, including the first-order correction
     kappa_sigma(p) = kappa_0(p) - 2 p z_p sigma + O(sigma^2)
from (i) the a = cos^2(theta) amplitude term: G_a * a''/2 with G_a = 2 p (z_p sigma) + exp-small, a'' = -2;
(ii) the cos(theta) factor on the code-noise scale, which only enters at O(sigma^2);
(iii) output 2 gate open up to exponentially small tails, contributing -eta p q + O(sigma^2).
Compared with every saved finite-difference curvature."""
import json, glob, numpy as np
from spinodal import kappa0, z_of
rows = []
for f in sorted(glob.glob("results/resultB/stiff_s*.json")):
    for r in json.load(open(f)):
        k = [x for x in r if x.startswith("kappa_minus")][0]
        p, s = r["p"], r["sigma"]
        pred1 = kappa0(p, 0.5) - 2 * p * z_of(p) * s
        rows.append(dict(sigma=s, p=p, numeric=r[k], kappa0=kappa0(p, 0.5), kappa0_plus_first_order=pred1,
                         err0=r[k] - kappa0(p, 0.5), err1=r[k] - pred1))
for r in rows:
    print(r["sigma"], r["p"], "num %.5f  k0 %.5f (err %.1e)  k0+1st %.5f (err %.1e)" % (r["numeric"], r["kappa0"], r["err0"], r["kappa0_plus_first_order"], r["err1"]))
e1 = {s: max(abs(r["err1"]) for r in rows if r["sigma"] == s) for s in sorted(set(r["sigma"] for r in rows))}
print("max |err| after first-order correction by sigma:", e1)
json.dump(dict(formula="kappa_sigma = kappa_0 - 2 p z_p sigma + O(sigma^2)", rows=rows, max_err_by_sigma=e1),
          open("results/resultB/spinodal_first_order.json", "w"), indent=1)
