"""R1 — signed critical coefficients (corrects analytic_A.py, which used A = -d kappa_-/dp).
With eps = p_c - p:  kappa_-(p_c - eps) = -A eps + O(eps^2),  A = +d kappa_-/dp |_{p_c}.
Opposite branch near p_c (k = |theta|):  F - F0 = h k - A eps k^2 + B k^3,  h = 2 eta c p q.
  c = 0:   k* = K eps,  K = 2A/(3B);  gain = C eps^3,  C = 4A^3/(27 B^2)
  c < 0 at p_c (h < 0):  k* = sqrt(-h/(3B))
  c > 0, same-sign side:  theta* = h/(2 kappa_+)
Run from claude_agent/:  python repair_v1/analytic_A_signed.py"""
import json, sys, os
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fra2 import K_C_theory

p, eta, c = sp.symbols("p eta c", positive=True)
q = 1 - p; D = 1 - p + p**2
kappa_minus = p*q*(p - eta*D)/D            # c = 0, from results/analytic_A_series.txt
kappa_plus = p*q*(1 - eta*(2 - p))/(2 - p)
B = 2*p**2*q**2/D
E = sp.Rational(1, 2); pc = (3 - sp.sqrt(5))/2
A = sp.diff(kappa_minus, p).subs({eta: E}).subs(p, pc)
Bv = B.subs(p, pc)
A_f, B_f = float(A), float(Bv)
K_pred, C_pred = 2*A_f/(3*B_f), 4*A_f**3/(27*B_f**2)
K_th, C_th = K_C_theory(0.5)
q0 = 1 - float(pc)
resp_neg = (2*0.5*float(pc)*q0/(3*B_f))**0.5            # k* = sqrt(-h/(3B)) = coef * sqrt(|c|)
kp = float(kappa_plus.subs({eta: E, p: pc}))
resp_pos = 0.5*float(pc)*q0/kp                           # theta* = h/(2 kappa_+) = coef * c
cstar = (A_f**2/(4*B_f))/(2*0.5*float(pc)*q0)
out = dict(A=A_f, A_symbolic=str(sp.nsimplify(sp.simplify(A))), B=B_f, K_pred=K_pred, K_theorem=float(K_th),
           C_pred=C_pred, C_theorem=float(C_th), signs_ok=bool(A_f > 0 and K_pred > 0 and C_pred > 0),
           K_rel_err=abs(K_pred/K_th - 1), C_rel_err=abs(C_pred/C_th - 1),
           neg_c_response="k* = sqrt(-h/(3B)) = %.10f*sqrt(|c|)" % resp_neg,
           pos_c_response="theta* = h/(2 kappa_+) = %.10f*c" % resp_pos,
           first_order_line="c* = A^2 eps^2/(8 eta p q B) = %.10f*eps^2" % cstar)
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "analytic_A_signed.json"), "w"), indent=1)
