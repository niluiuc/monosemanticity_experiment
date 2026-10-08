"""Lemma for Result A (closing the 'fixed gate pattern' gap), sigma = 0.

For fixed theta the per-output clean loss is piecewise quadratic in its bias b, with breakpoints
where some state's pre-activation crosses zero. Its global minimum is attained either at the
interior minimiser of some piece (if inside that piece) or at a breakpoint. We enumerate every
piece and every breakpoint as a Taylor series in k = |theta| (k -> 0+), with symbolic (p, c), and
show that the gate pattern used in analytic_A.py is the unique global minimiser for small k:
every competitor's value minus the chosen value has a POSITIVE leading series coefficient on the
whole domain p in (0,1), feasible c. The sign of each leading coefficient (an explicit rational
function of p, c) is verified on a dense (p, c) grid and its factorisation is saved.
Output: results/gate_lemma.json"""
import json
import sympy as sp
import numpy as np

k, p, c, b = sp.symbols("k p c b", real=True)
q = 1 - p; cov = c * p * q
P = {(0, 0): q**2 + cov, (1, 0): p*q - cov, (0, 1): p*q - cov, (1, 1): p**2 + cov}
ORDER = 5


def ser(e):
    return sp.series(sp.simplify(e), k, 0, ORDER).removeO()


def lead(e):
    """leading (lowest-order) nonzero coefficient and its order of a polynomial-in-k series."""
    e = sp.expand(e)
    for n in range(ORDER):
        co = sp.simplify(e.coeff(k, n))
        if co != 0:
            return n, sp.factor(co)
    return None, sp.Integer(0)


def analyse(name, offsets, target_idx, chosen_on):
    """offsets[x]: pre-activation without bias for state x; target_idx: which coordinate is the target;
    chosen_on: set of states ON in the claimed optimal pattern."""
    states = list(P)
    kk = 1e-3
    num = {x: float(offsets[x].subs(k, kk)) for x in states}
    bps = sorted(set([-num[x] for x in states]))
    # map numeric breakpoints back to symbolic expressions
    bsym = []
    for v in bps:
        for x in states:
            if abs(-num[x] - v) < 1e-15:
                bsym.append(-offsets[x]); break
    edges = [-np.inf] + bps + [np.inf]
    cand = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        mid = 0.0 if not np.isfinite(lo) or not np.isfinite(hi) else 0.5 * (lo + hi)
        if not np.isfinite(lo): mid = hi - 1.0
        if not np.isfinite(hi): mid = lo + 1.0
        on = frozenset(x for x in states if num[x] + mid > 0)
        if not on:
            continue
        W = sum(P[x] for x in on)
        bstar = sum(P[x] * (x[target_idx] - offsets[x]) for x in on) / W
        Q = sum(P[x] * (offsets[x] + bstar - x[target_idx])**2 for x in on) + sum(P[x] * x[target_idx]**2 for x in states if x not in on)
        # is bstar inside (lo, hi)? check numerically at small k on a (p, c) grid later; record series
        cand.append(dict(kind="interior", on=sorted(on), bstar=bstar, value=Q, lo_idx=i - 1, hi_idx=i))
    # breakpoint candidates
    for j, bs in enumerate(bsym):
        val = sum(P[x] * (sp.Max(offsets[x] + bs, 0) - x[target_idx])**2 for x in states)
        cand.append(dict(kind="breakpoint", at=j, value=val))
    chosen = [cd for cd in cand if cd["kind"] == "interior" and set(cd["on"]) == set(chosen_on)]
    assert len(chosen) == 1, (name, [cd.get("on") for cd in cand])
    ch = chosen[0]
    chosen_val = ser(ch["value"])
    report = dict(name=name, chosen_on=[list(x) for x in sorted(chosen_on)], competitors=[])
    # numeric grid for sign checks
    pg = np.linspace(0.02, 0.98, 49)
    for cd in cand:
        if cd is ch:
            continue
        if cd["kind"] == "breakpoint":
            # breakpoint values: evaluate Max with small k numerically -> replace Max by piecewise for k->0+
            bs = bsym[cd["at"]]
            on_bp = [x for x in states if num[x] + float(bs.subs(k, kk)) > 1e-14]
            val = sum(P[x] * (offsets[x] + bs - x[target_idx])**2 for x in on_bp) + sum(P[x] * x[target_idx]**2 for x in states if x not in on_bp)
        else:
            val = cd["value"]
        diff = sp.expand(ser(val) - chosen_val)
        n, co = lead(diff)
        f = sp.lambdify((p, c), co, "numpy")
        # validity of an interior candidate: its minimiser must lie inside its own piece (for small k)
        vfun = []
        if cd["kind"] == "interior":
            if cd["lo_idx"] >= 0:
                nn, cc_ = lead(sp.expand(ser(cd["bstar"]) - ser(bsym[cd["lo_idx"]]))); vfun.append(sp.lambdify((p, c), cc_, "numpy"))
            if cd["hi_idx"] < len(bsym):
                nn, cc_ = lead(sp.expand(ser(bsym[cd["hi_idx"]]) - ser(cd["bstar"]))); vfun.append(sp.lambdify((p, c), cc_, "numpy"))
        mins = []; nvalid = 0; ntot = 0
        for pv in pg:
            cmax = min(1.0, (1 - pv) / pv, pv / (1 - pv)) * 0.999   # keeps all four probabilities positive
            for cv in np.linspace(-cmax, cmax, 41):
                ntot += 1
                if all(float(g(pv, cv)) > 0 for g in vfun):
                    nvalid += 1; mins.append(float(f(pv, cv)))
        report["competitors"].append(dict(kind=cd["kind"], on=[list(x) for x in cd.get("on", [])] if cd["kind"] == "interior" else None,
                                          leading_order=n, leading_coeff=str(co), valid_fraction=nvalid / ntot,
                                          min_on_grid=min(mins) if mins else None,
                                          positive_on_grid=bool((min(mins) > 0) if mins else True)))
    # the chosen interior minimiser must lie strictly inside its piece for small k
    lo_b = bsym[ch["lo_idx"]] if ch["lo_idx"] >= 0 else None
    hi_b = bsym[ch["hi_idx"]] if ch["hi_idx"] < len(bsym) else None
    inside = []
    for bnd, sgn in [(lo_b, 1), (hi_b, -1)]:
        if bnd is None: continue
        n, co = lead(sp.expand(sgn * (ser(ch["bstar"]) - ser(bnd))))
        f = sp.lambdify((p, c), co, "numpy")
        vals = [float(f(pv, cv)) for pv in pg for cv in np.linspace(-min(1, (1-pv)/pv, pv/(1-pv))*0.999, min(1, (1-pv)/pv, pv/(1-pv))*0.999, 41)]
        inside.append(dict(order=n, coeff=str(co), min_on_grid=min(vals), positive=bool(min(vals) > 0)))
    report["chosen_strictly_inside"] = inside
    return report


th = -k   # opposite-sign branch: theta = -k
a = sp.cos(k)**2
dn = -sp.sin(k) * sp.cos(k)
s2 = sp.sin(k)**2
off1_opp = {(0, 0): 0, (1, 0): a, (0, 1): dn, (1, 1): a + dn}
off2_opp = {(0, 0): 0, (1, 0): dn, (0, 1): s2, (1, 1): dn + s2}
dp = sp.sin(k) * sp.cos(k)
off1_same = {(0, 0): 0, (1, 0): a, (0, 1): dp, (1, 1): a + dp}
off2_same = {(0, 0): 0, (1, 0): dp, (0, 1): s2, (1, 1): dp + s2}
for D in (off1_opp, off2_opp, off1_same, off2_same):
    for x in D: D[x] = sp.sympify(D[x])

reports = [
    analyse("output1_opposite", off1_opp, 0, {(0, 0), (1, 0), (1, 1)}),
    analyse("output2_opposite", off2_opp, 1, {(0, 0), (1, 0), (0, 1), (1, 1)}),
    analyse("output1_same", off1_same, 0, {(1, 0), (0, 1), (1, 1)}),
    analyse("output2_same", off2_same, 1, {(0, 0), (1, 0), (0, 1), (1, 1)}),
]
ok = all(all(cp["positive_on_grid"] for cp in r["competitors"]) and all(i["positive"] for i in r["chosen_strictly_inside"]) for r in reports)
for r in reports:
    print("==", r["name"])
    for cp in r["competitors"]:
        print("  ", cp["kind"], cp["on"], "order", cp["leading_order"], "valid", round(cp["valid_fraction"], 3), "min", cp["min_on_grid"], cp["leading_coeff"][:70])
    for i in r["chosen_strictly_inside"]:
        print("   inside: order", i["order"], "min", "%.3e" % i["min_on_grid"], i["coeff"][:90])
print("ALL CHECKS POSITIVE:", ok)
json.dump(dict(all_positive=ok, reports=reports), open("results/gate_lemma.json", "w"), indent=1)
