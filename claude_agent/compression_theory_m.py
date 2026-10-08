"""Shared-budget threshold for general m (n = 2m, importances (1,...,1, eta,...,eta), independent):
energy for the first partner can be drawn from the other m-1 important features equally, so the donor
cost is pq (u + k^2)^2 / (m-1). Opposite-branch Hessian at mono -> threshold p_c^shared(eta, m)."""
import sympy as sp, json
k, p, eta, u, M = sp.symbols("k p eta u M", positive=True)
q = 1 - p; P11, P10, P01, P00 = p*p, p*q, p*q, q*q
a = 1 + u; d = -sp.sqrt(1 + u) * k; s2 = k**2
b1 = (P10*(1 - a) + P11*(1 - a - d)) / (P00 + P10 + P11)
L1 = P00*b1**2 + P10*(a + b1 - 1)**2 + P11*(a + d + b1 - 1)**2
L3 = (d**2 + (s2 - 1)**2) * p*q
F = L1 + eta*L3 + p*q*(u + k**2)**2/(M - 1) - eta*p*q
H = sp.simplify(sp.hessian(F, (k, u)).subs({k: 0, u: 0}))
kap = sp.factor(sp.simplify((H[0, 0] - H[0, 1]**2/H[1, 1]) / 2))
print("kappa_eff(m):", kap)
num = sp.factor(sp.numer(sp.together(kap)))
print("numerator:", num)
sols = sp.solve(sp.Eq(num / (p*(p - 1)), 0), p)
print("roots:", sols)
res = {}
for m in [2, 3, 4, 1000]:
    r = [complex(s.subs({eta: 0.5, M: m})) for s in sols]
    r = [x.real for x in r if abs(x.imag) < 1e-12 and 0 < x.real < 1]
    res[m] = r; print("m =", m, "eta=.5 thresholds in (0,1):", r)
json.dump(dict(kappa_eff=str(kap), roots=[str(s) for s in sols], eta_half={str(m): v for m, v in res.items()}),
          open("results/compression/theory_general_m.json", "w"), indent=1)
