"""Identity on the critical line eta = p/D (kappa_- = 0): the existing frozen noise coefficient
B_frozen = q(1-2p)/2 is proportional to the same-sign stiffness kappa_+ = pq(1-eta(2-p))/(2-p):
    B_frozen = kappa_+ * D (2-p) / (2 p q).
Hence B_frozen vanishes exactly where the same-sign direction becomes soft (eta=2/3, p=1/2)."""
import sympy as sp, json
p = sp.symbols("p", positive=True); q = 1 - p; D = 1 - p + p**2; eta = p / D
kplus = p*q*(1 - eta*(2 - p))/(2 - p)
Bfro = q*(1 - 2*p)/2
ratio = sp.simplify(Bfro / kplus)
print("B_frozen / kappa_+ on critical line =", sp.factor(ratio))
print("check equals D(2-p)/(2pq):", sp.simplify(ratio - D*(2 - p)/(2*p*q)) == 0)
json.dump(dict(identity="B_frozen = kappa_plus * D (2-p) / (2 p q) on eta = p/D", ratio=str(sp.factor(ratio)),
               verified=bool(sp.simplify(ratio - D*(2 - p)/(2*p*q)) == 0)), open("results/bicritical_identity.json", "w"), indent=1)
