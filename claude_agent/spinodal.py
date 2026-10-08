"""Mono spinodal under training noise (Result B2).
For |theta| << sigma -> 0 the noise smooths the ReLU kink; a second-order expansion of the profiled
loss in d = sin cos (with the output-1 bias re-optimised; Schur complement of the (d,b) Hessian)
gives the curvature at mono

    kappa_0(p) = p q [ p + q Phi(z_p) - eta ],    p z_p + q [z_p Phi(z_p) + phi(z_p)] = 0,

where z_p sigma is the noise-optimal mono bias (the minimiser in the existing v(p)).
Mono is locally stable iff kappa_0 > 0, i.e. for p > p_sp(eta), INDEPENDENT of sigma at leading
order -> the metastable window [p_sp, p_c) stays O(1) wide as sigma -> 0.
Compares with the finite-difference curvatures saved by result_B_checks.py stiff."""
import json, glob
import numpy as np
from scipy.special import ndtr
from scipy.optimize import brentq
from fra2 import pc_theory

phi = lambda z: np.exp(-z*z/2)/np.sqrt(2*np.pi)


def z_of(p):
    q = 1-p
    return brentq(lambda z: p*z + q*(z*ndtr(z)+phi(z)), -10, 10)


def kappa0(p, eta):
    q = 1-p
    return p*q*(p + q*ndtr(z_of(p)) - eta)


out = dict(formula="kappa_0(p) = p q [p + q Phi(z_p) - eta]", spinodal={}, comparison=[])
for eta in [0.48, 0.5, 0.52, 2/3]:
    psp = brentq(lambda p: kappa0(p, eta), 0.02, pc_theory(eta) - 1e-9)
    out["spinodal"][f"{eta:.4f}"] = dict(p_sp=psp, p_c=pc_theory(eta), window=pc_theory(eta)-psp)
    print(f"eta={eta:.4f}: p_sp={psp:.5f}, p_c={pc_theory(eta):.5f}, metastable width {pc_theory(eta)-psp:.4f}")
for f in sorted(glob.glob("results/resultB/stiff_s*.json")):
    for r in json.load(open(f)):
        key = [k for k in r if k.startswith("kappa_minus")][0]
        out["comparison"].append(dict(sigma=r["sigma"], p=r["p"], numeric=r[key], kappa0=kappa0(r["p"], 0.5)))
for r in out["comparison"]:
    print(r)
json.dump(out, open("results/resultB/spinodal.json", "w"), indent=1)
