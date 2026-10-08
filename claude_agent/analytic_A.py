"""Task 6 — exact (symbolic) clean profiled loss near mono, with correlation c.

For sigma = 0 and small |theta| the optimal biases sit on a fixed gate pattern, where the loss is
quadratic in the bias, so the profiled loss on each branch has an exact closed form:

 opposite branch (theta<0, d = sin cos < 0, a = cos^2, s = sin):
   output 1: gates  (0,0) on with value b1, (1,0) on, (0,1) OFF (d+b1<=0), (1,1) on
             b1* = [P10(1-a) + P11(1-a-d)] / (P00+P10+P11)          valid while 0 <= b1* <= |d|
   output 2: all gates open -> loss2 = Var(d X1 + (s^2-1) X2)          valid while d + b2* > 0
 same-sign branch (theta>0):
   output 1: (0,0) OFF (b1<=0), others on;  b1* = -[P01 d + P10(a-1) + P11(a+d-1)]/(P01+P10+P11)
             valid while -d <= b1* <= 0
   output 2: all gates open.

We expand both in theta to O(theta^4) with general (p, c, eta), check against the numerical
solver, derive the cubic coefficient INDEPENDENTLY of the existing (K, C), and re-derive the
first-order line c*(eps) and the critical response exactly at leading order.
Writes results/analytic_A.json and results/analytic_A_series.txt."""
import json
import sympy as sp
import numpy as np

th, p, c, eta = sp.symbols("theta p c eta", real=True)
q = 1 - p
cov = c * p * q
P11, P10, P01, P00 = p**2 + cov, p*q - cov, p*q - cov, q**2 + cov
a, d, s = sp.cos(th)**2, sp.sin(th)*sp.cos(th), sp.sin(th)
EX1 = EX2 = p
VarX = p*q


def var_lin(u, v):  # Var(u X1 + v X2)
    return u**2*VarX + v**2*VarX + 2*u*v*cov


loss2 = var_lin(d, s**2 - 1)
# opposite branch
b1n = (P10*(1 - a) + P11*(1 - a - d)) / (P00 + P10 + P11)
L1n = P00*b1n**2 + P10*(a + b1n - 1)**2 + P11*(a + d + b1n - 1)**2
# same-sign branch
b1p = -(P01*d + P10*(a - 1) + P11*(a + d - 1)) / (P01 + P10 + P11)
L1p = P01*(d + b1p)**2 + P10*(a + b1p - 1)**2 + P11*(a + d + b1p - 1)**2
# mono value
F0 = P10*0 + eta*VarX           # output1 exact (b1=0) + output2 prior-mean loss

Fn = sp.simplify(L1n + eta*loss2 - F0)
Fp = sp.simplify(L1p + eta*loss2 - F0)
ORDER = 5
sn = sp.series(Fn, th, 0, ORDER).removeO()
spos = sp.series(Fp, th, 0, ORDER).removeO()
coef_n = [sp.factor(sp.simplify(sn.coeff(th, k))) for k in range(ORDER)]
coef_p = [sp.factor(sp.simplify(spos.coeff(th, k))) for k in range(ORDER)]

with open("results/analytic_A_series.txt", "w") as fh:
    fh.write("F(theta)-F(mono) on each branch, exact Taylor coefficients (theta^k), general p,c,eta\n")
    for k in range(ORDER):
        fh.write(f"opposite  theta^{k}: {coef_n[k]}\n")
    for k in range(ORDER):
        fh.write(f"same-sign theta^{k}: {coef_p[k]}\n")
print(open("results/analytic_A_series.txt").read())

# ---- numerical check against the solver ----------------------------------------
from fra2 import F as Fnum, pc_theory, K_C_theory
fn_l = sp.lambdify((th, p, c, eta), Fn, "mpmath")
fp_l = sp.lambdify((th, p, c, eta), Fp, "mpmath")
checks = []
for (pp, cc) in [(0.38, 0.0), (0.36, 0.0), (0.42, 0.01), (0.33, -0.02), (0.30, 0.005)]:
    for t in [-0.02, -0.005, 0.005, 0.02]:
        ex = float((fn_l if t < 0 else fp_l)(t, pp, cc, 0.5))
        nu = Fnum(t, pp, cc, 0.0, 0.5)[0] - Fnum(0.0, pp, cc, 0.0, 0.5)[0]
        checks.append(dict(p=pp, c=cc, theta=t, closed_form=ex, solver=nu, diff=ex - nu))
mx = max(abs(r["diff"]) for r in checks)
print("max |closed form - solver| =", mx)

# ---- independent cubic coefficient at c = 0, p = p_c --------------------------------
E = sp.Rational(1, 2)
pcv = sp.nsimplify(pc_theory(0.5)) if False else (3 - sp.sqrt(5)) / 2   # p_c(1/2) = (3-sqrt5)/2
k = sp.symbols("k", positive=True)   # k = |theta| on the opposite branch -> theta = -k
c2 = coef_n[2].subs({c: 0, eta: E})
c3 = coef_n[3].subs({c: 0, eta: E})
c2_at_pc = sp.nsimplify(sp.simplify(c2.subs(p, pcv)))
dc2_dp = sp.simplify(sp.diff(c2, p).subs(p, pcv))
B_indep = sp.simplify(-c3.subs(p, pcv))           # F = kappa k^2 + B k^3 with theta=-k  -> B = -coef3
K, C = K_C_theory(0.5)
A_slope = float(-dc2_dp)                          # kappa_- = -A eps + O(eps^2), eps = pc - p
res = dict(kappa_minus_at_pc=float(c2_at_pc), A=A_slope, B_independent=float(B_indep),
           B_from_K_C=2*C/K**3, K_pred=2*A_slope/(3*float(B_indep)), K_theorem=K,
           C_pred=4*A_slope**3/(27*float(B_indep)**2), C_theorem=C)
print(res)

# ---- leading-order field results with the independent coefficients ----------------
h1 = coef_n[1].subs({eta: E})          # linear coefficient: F = coef1*theta + ...
res["linear_coeff_general"] = str(sp.factor(coef_n[1]))
q0 = 1 - float(pcv)
Bv = float(B_indep)
h_of_c = lambda cc: 2*0.5*cc*float(pcv)*q0
res["critical_response_coeff_c<0"] = float(np.sqrt(2*0.5*float(pcv)*q0/(3*Bv)))
kap_plus = float(coef_p[2].subs({c: 0, eta: E, p: pcv}))
res["kappa_plus_at_pc"] = kap_plus
res["same_sign_response_coeff"] = 0.5*float(pcv)*q0/kap_plus
res["c_star_coeff_eps2"] = (A_slope**2/(4*Bv))/(2*0.5*float(pcv)*q0)
print({k_: v for k_, v in res.items() if not isinstance(v, str)})
json.dump(dict(series_file="results/analytic_A_series.txt", solver_checks=checks, max_abs_diff=mx, **res),
          open("results/analytic_A.json", "w"), indent=1)
