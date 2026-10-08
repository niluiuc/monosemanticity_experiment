"""Same-sign branch version of compression_theory.py (needed when eta > 1/2: the fixed-norm
same-sign stiffness kappa_+ = pq(1 - eta(2-p))/(2-p) vanishes at p = 2 - 1/eta)."""
import sympy as sp, json
k, p, eta, u = sp.symbols("k p eta u", real=True)
q = 1 - p
P11, P10, P01, P00 = p*p, p*q, p*q, q*q
a = 1 + u; d = sp.sqrt(1 + u) * k; s2 = k**2
b1 = -(P01*d + P10*(a - 1) + P11*(a + d - 1)) / (P01 + P10 + P11)
L1 = P01*(d + b1)**2 + P10*(a + b1 - 1)**2 + P11*(a + d + b1 - 1)**2
L3 = (d**2 + (s2 - 1)**2) * p*q
donor = p*q*(u + k**2)**2
F = L1 + eta*L3 + donor - eta*p*q
H = sp.simplify(sp.hessian(F, (k, u)).subs({k: 0, u: 0}))
kap_fixed = sp.factor(sp.simplify(H[0, 0] / 2)); kap_eff = sp.factor(sp.simplify((H[0, 0] - H[0, 1]**2 / H[1, 1]) / 2))
print("kappa+_fixed:", kap_fixed); print("kappa+_eff:", kap_eff)
out = {}
for e in [0.7]:
    pf = sp.nsolve(kap_fixed.subs(eta, e), p, 0.57); pe = sp.nsolve(kap_eff.subs(eta, e), p, 0.62)
    out[str(e)] = dict(fixed=float(pf), shared=float(pe)); print(e, float(pf), float(pe))
sol = sp.solve(sp.numer(sp.together(kap_eff)) / (p*(p-1)), p)
print("closed-form roots:", sol)
json.dump(dict(kappa_plus_fixed=str(kap_fixed), kappa_plus_eff=str(kap_eff), roots=out, closed=[str(s) for s in sol]),
          open("results/compression/theory_same_sign.json", "w"), indent=1)
