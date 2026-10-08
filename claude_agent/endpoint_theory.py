"""Theory for the c<0 critical endpoint (S5). In the scaled variable x = |theta|/sigma at p near p_c,
F(-x sigma) - F(0) = sigma^2 Phi(x) + o(sigma^2): Phi grows like kappa_0 x^2, saturates at the calibrated
penalty B_cal (sharing gates fully linear), while the clean part -A eps theta^2 + B|theta|^3 is subleading.
A negative correlation adds -|h| sigma x with |h| = 2 eta |c| p q. The near-mono minimum disappears
(merges with the barrier) when |h|/sigma = max_x Phi'(x). Prediction:
     |c_e| = sigma * max Phi' / (2 eta p q)     (leading order, p ~ p_c)
Phi is computed from the exact solver at small sigma; prediction compared with endpoint_refined."""
import json, numpy as np
from fra2 import F, pc_theory
ETA = 0.5; PC = pc_theory(ETA); q = 1 - PC
res = {}
for s in [0.0005, 0.001, 0.002]:
    x = np.linspace(0.0, 12, 241)
    F0 = F(0.0, PC, 0.0, s, ETA)[0]
    Phi = np.array([(F(-xx * s, PC, 0.0, s, ETA)[0] - F0) / s ** 2 for xx in x])
    dPhi = np.gradient(Phi, x)
    k = int(np.argmax(dPhi))
    res[str(s)] = dict(x=x.tolist(), Phi=Phi.tolist(), max_dPhi=float(dPhi[k]), x_at_max=float(x[k]), Phi_at_12=float(Phi[-1]))
    print(s, "max Phi' =", round(dPhi[k], 5), "at x =", x[k], " Phi(12) =", round(Phi[-1], 5), " (B_cal = 0.16504)")
mp = np.mean([res[k]["max_dPhi"] for k in res])
coef = mp / (2 * ETA * PC * q)
summ = json.load(open("results/endpoint_refined/summary.json"))
print("predicted |c_e| / sigma =", round(coef, 4))
print("measured |c_e|/sigma:", dict(zip(summ["sigma"], np.round(summ["abs_c_e_over_sigma"], 4))))
json.dump(dict(phi_curves=res, predicted_coeff=coef, measured=summ), open("results/endpoint_theory.json", "w"), indent=1)
