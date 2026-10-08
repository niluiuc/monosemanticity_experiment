"""Leading-order theory for the shared-energy (Frobenius) budget, n=4, m=2, independent features,
importances (1, 1, eta, eta). Near the decoupled mono point a partner k in dimension 1 can be
combined with an amplitude change r of feature 1, paid for by donor feature 2 (s^2 = 2 - r^2 - k^2).
Opposite-branch gate pattern (as in analytic_A / gate_lemma) with a -> r^2, d -> -r k, s^2 -> k^2.
Profile r at each k, expand in k: kappa_eff(p) = kappa_- (fixed-norm) - (cross term)^2 / (r-stiffness).
Find p where kappa_eff = 0 and compare with the numerical transition of fra_nm.py."""
import sympy as sp, json
k, p, eta, u = sp.symbols("k p eta u", real=True)   # r^2 = 1 + u
q = 1 - p
P11, P10, P01, P00 = p*p, p*q, p*q, q*q
a = 1 + u; d = -sp.sqrt(1 + u) * k; s2 = k**2
b1 = (P10*(1 - a) + P11*(1 - a - d)) / (P00 + P10 + P11)
L1 = P00*b1**2 + P10*(a + b1 - 1)**2 + P11*(a + d + b1 - 1)**2       # feature 1 output (target X1)
L3 = (d**2 + (s2 - 1)**2 - 2*0) * p*q                                  # feature 3 output: Var(d X1 + (s2-1) X3), indep.
donor = p*q*(u + k**2)**2                                              # feature 2: s^2 = 1 - u - k^2, loss pq(1-s^2)^2
Fm = eta * p*q                                                         # mono: feature-3 prior-mean loss (others exact)
F = L1 + eta*L3 + donor - Fm
# second-order expansion in (k, u)
Fk = sp.diff(F, k); 
H = sp.hessian(F, (k, u)).subs({k: 0, u: 0})
g = sp.Matrix([sp.diff(F, k), sp.diff(F, u)]).subs({k: 0, u: 0})
print("gradient at mono:", sp.simplify(g.T))
Hs = sp.simplify(H)
kap_fixed = sp.simplify(Hs[0, 0] / 2)
kap_eff = sp.simplify((Hs[0, 0] - Hs[0, 1]**2 / Hs[1, 1]) / 2)
print("kappa_fixed (u=0):", sp.factor(kap_fixed))
print("kappa_eff (u profiled):", sp.factor(kap_eff))
res = {}
for e in [0.5]:
    pf = sp.nsolve(kap_fixed.subs(eta, e), p, 0.38)
    pe = sp.nsolve(kap_eff.subs(eta, e), p, 0.42)
    res[str(e)] = dict(p_c_fixed_norm=float(pf), p_c_shared_energy=float(pe))
    print("eta", e, "fixed-norm p_c", float(pf), " shared-energy p_c", float(pe))
json.dump(dict(kappa_fixed=str(sp.factor(kap_fixed)), kappa_eff=str(sp.factor(kap_eff)), roots=res),
          open("results/compression/theory.json", "w"), indent=1)
