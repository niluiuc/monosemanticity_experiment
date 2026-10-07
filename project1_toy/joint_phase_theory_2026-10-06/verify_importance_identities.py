"""Independent symbolic checks of the new branch and endpoint identities."""
from pathlib import Path
import argparse,hashlib,json
import sympy as s

H=Path(__file__).resolve().parent
p,k,eta=s.symbols('p k eta',real=True)
q=1-p;D=1-p+p*p;a=1/(1+k*k);c=k*k/(1+k*k);r=k/(1+k*k)
S=p*q*c-p*q/D*(q*r-p*c)**2
W4=p*q*a
W3=p*q*a-p*q/D*(q*r-p*a)**2
A=p-eta*D;E=1-p-eta*D
delta=p*q/D*k*k*(A+2*p*q*k+E*k*k)/(1+k*k)**2
J=A+3*p*q*k+(2*E-A)*k*k-p*q*k**3
N=(q-eta*D)*k**4+2*p*q*k**3+(p*(1+eta)-2*eta*D)*k*k+2*eta*p*q*k-eta*p*p
checks={
 'profiled_all_active_difference':s.factor(S+eta*W4-eta*p*q-delta)==0,
 'profiled_three_active_difference':s.factor(S+eta*W3-eta*p*q-p*q/D*N/(1+k*k)**2)==0,
 'stationarity_cubic':s.factor(s.diff(delta,k)-2*p*q/D*k*J/(1+k*k)**3)==0,
 'critical_slope_discriminant':s.rem((1+eta-2*eta*p)**2-(1+2*eta-3*eta**2),eta*p*p-(1+eta)*p+eta,p)==0,
}
end=delta.subs({eta:s.Rational(2,3),p:s.Rational(1,2)})
checks['endpoint_opposite_clean_identity']=s.factor(end-k**3/(6*(1+k*k)**2))==0
plus=p*q*c*((1+2*q*r)/(2-p)-eta)
ep=s.symbols('epsilon',positive=True)
op_gain=s.limit(delta.subs({eta:s.Rational(2,3),p:s.Rational(1,2)-ep,k:s.Rational(4,3)*ep})/ep**3,ep,0)
plus_gain=s.limit(plus.subs({eta:s.Rational(2,3),p:s.Rational(1,2)-ep,k:s.Rational(4,9)*ep})/ep**3,ep,0)
checks['endpoint_opposite_gain']=op_gain==-s.Rational(16,81)
checks['endpoint_same_sign_gain']=plus_gain==-s.Rational(16,2187)
checks['opposite_gain_factor_27']=s.simplify(op_gain/plus_gain)==27
checks['endpoint_frozen_coefficient_zero']=((q*(1-2*p)/2).subs(p,s.Rational(1,2))==0)
assert all(checks.values()),checks
ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=H/'importance_symbolic_review_v1')
out=ap.parse_args().output;out.mkdir(parents=True,exist_ok=False)
(out/'results.json').write_text(json.dumps(dict(all_passed=True,checks=checks,
 endpoint_clean_gain=str(op_gain),same_sign_gain=str(plus_gain),
 scope='Symbolic branch identities and endpoint leading terms only; not an independent global proof or novelty audit.'),indent=2))
(out/'source_sha256.json').write_text(json.dumps({Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
print(json.dumps(checks,indent=2))
