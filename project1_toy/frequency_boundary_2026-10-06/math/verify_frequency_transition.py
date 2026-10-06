"""Exact symbolic identity checks for the Stage A frequency theorem.

No training or numerical parameter/angle sweep. SymPy checks derivations;
the global inequalities and branch coverage are proved in derivation.md.
"""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
p,k,c,r=s.symbols('p k c r',real=True)
q=1-p; D=1-p+p*p
a=1-c
checks={}

S3=p*q*c*c+p*p*(c+r)**2-p*p*(c+p*r)**2/D
Scompact=p*q*c*(p+(1-2*p)*c+2*p*q*r)/D
checks['opposite_strong_loss']=s.factor(s.expand(S3-Scompact).subs(r*r,a*c))==0
# substitute exact rational rank-one geometry to avoid formal sqrt assumptions
A=1/(1+k*k); C=k*k*A; R=k*A
S=Scompact.subs({c:C,r:R})
W3=p*q*A*A+p*p*(A+R)**2-p*p*(A+p*R)**2/D
Wall=p*q*A
checks['weak_three_active_gain']=s.factor(W3-(Wall-p*q*(q*R-p*A)**2/D))==0
delta_all=S+Wall/2-p*q/2
expected_delta=p*q*C*(p-D/2+(1-2*p)*C+2*p*q*R)/D
checks['all_active_loss_difference']=s.factor(delta_all-expected_delta)==0
H=s.expand(D*k*k*(1+k*k)-2*(q*k-p*k*k)**2-(q*k-p)**2)
checks['three_active_H']=s.factor(S+W3/2-p*q/2-p*q*H/(2*D*(1+k*k)**2))==0
coeff_A=1-p-p*p
coeff_B=-2+5*p-2*p*p
Hexpanded=coeff_A*k**4+4*p*q*k**3+coeff_B*k*k+2*p*q*k-p*p
checks['H_polynomial']=s.factor(H-Hexpanded)==0
checks['H_derivative_bound_identity']=s.factor(s.diff(H,k)-(
    4*coeff_A*k**3+2*p*k*(6*q*k-1)+2*p*q+2*(coeff_B+p)*k))==0
checks['B_lower_bound_identity']=s.factor(coeff_B+p+2*(p*p-3*p+1))==0
checks['weak_branch_boundary_matching']=s.factor((S+W3/2-S-Wall/2).subs(k,p/q))==0
checks['orientation_order_three_active']=s.factor(W3-S-p*q*(A-C)*(q+2*p*q*R)/D)==0
Lplus=p*q*(c*c+r*r)+p*p*(c-r)**2-p*(c-r)**2/(2-p)
Splus=p*q*c*(1+2*q*r)/(2-p)
checks['same_sign_strong_loss']=s.factor(s.expand(Lplus-Splus).subs(r*r,a*c))==0
checks['same_sign_mono_difference']=s.factor(Splus+p*q*a/2-p*q/2-
    p*q*c*(p/2+2*q*r)/(2-p))==0
local=s.limit(delta_all/k**2,k,0,dir='+')
checks['mono_local_coefficient']=s.factor(local-p*q*(p/D-s.Rational(1,2)))==0
pc=(3-s.sqrt(5))/2
checks['critical_probability_root']=s.simplify((p*p-3*p+1).subs(p,pc))==0
checks['threshold_above_quarter']=bool(pc>s.Rational(1,4))
checks['threshold_below_half']=bool(pc<s.Rational(1,2))
result={'stage':'A symbolic checks only','checks':checks,'all_checks_pass':all(checks.values()),
        'critical_probability_exact':str(pc),'critical_probability_decimal':str(s.N(pc,20)),
        'critical_sparsity_exact':str(1-pc),'sympy_version':s.__version__,
        'global_proof_location':'derivation.md; identities alone do not prove inequalities/coverage'}
HERE.mkdir(parents=True,exist_ok=True)
(HERE/'verification_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))

if not result['all_checks_pass']:
    raise AssertionError('At least one identity check failed; inspect before interpreting theorem.')
