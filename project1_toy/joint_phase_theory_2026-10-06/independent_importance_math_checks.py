"""Independent finite algebra/root-record audit; no new validation cases."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json
import sympy as s
import mpmath as mp

HERE=Path(__file__).resolve().parent
p,k,e=s.symbols('p k eta',real=True)
q=1-p;D=q+p*p;a=1/(1+k*k);c=k*k/(1+k*k);r=k/(1+k*k)
states=[(0,0),(0,1),(1,0),(1,1)]
probs=[q*q,p*q,p*q,p*p]
def scalar_loss(row,bias,target,mask):
 return s.factor(sum(P*((row[0]*x[0]+row[1]*x[1]+bias-x[target])**2 if on else x[target]**2)
                     for x,P,on in zip(states,probs,mask)))
S=scalar_loss([a,-r],p*(c+p*r)/D,0,[1,0,1,1])
W4=scalar_loss([-r,c],p*(a+r),1,[1,1,1,1])
W3=scalar_loss([-r,c],p*(a+p*r)/D,1,[1,1,0,1])
Sp=scalar_loss([a,r],(c-r)/(2-p),0,[0,1,1,1])
Wp=scalar_loss([r,c],p*(a-r),1,[1,1,1,1])
A=p-e*D;E=q-e*D
delta=p*q/D*k*k*(A+2*p*q*k+E*k*k)/(1+k*k)**2
J=A+3*p*q*k+(2*E-A)*k*k-p*q*k**3
N=E*k**4+2*p*q*k**3+(p*(1+e)-2*e*D)*k*k+2*e*p*q*k-e*p*p
checks={
 'independent_strong_state_loss':s.factor(S-(p*q*c-p*q*(q*r-p*c)**2/D))==0,
 'independent_weak_all_state_loss':s.factor(W4-p*q*a)==0,
 'independent_weak_three_state_loss':s.factor(W3-(p*q*a-p*q*(q*r-p*a)**2/D))==0,
 'independent_same_sign_state_losses':s.factor(Sp-p*q*c*(1+2*q*r)/(2-p))==0 and s.factor(Wp-p*q*a)==0,
 'all_active_weighted_excess':s.factor(S+e*W4-e*p*q-delta)==0,
 'three_active_weighted_excess':s.factor(S+e*W3-e*p*q-p*q*N/(D*(1+k*k)**2))==0,
 'stationarity_from_state_losses':s.factor(s.diff(S+e*W4,k)-2*p*q*k*J/(D*(1+k*k)**3))==0,
 'three_branch_derivative_regroup':s.factor(s.diff(N,k)-(4*E*k**3+2*p*k*(3*q*k-(1-e))+4*A*k+2*e*p*q))==0,
 'pointwise_sign_sector_comparison':s.factor(Sp-S-p*q*(1-2*p)*k*k*(q+2*q*q*k-k*k)/((2-p)*D*(1+k*k)**2))==0,
 'endpoint_both_sign_excess':s.factor(delta.subs({p:s.Rational(1,2),e:s.Rational(2,3)})-k**3/(6*(1+k*k)**2))==0 and s.factor((Sp+e*Wp-e*p*q).subs({p:s.Rational(1,2),e:s.Rational(2,3)})-k**3/(6*(1+k*k)**2))==0,
}
assert all(checks.values()),checks

def sqrt_bracket(rad):
 lo=F(0);hi=F(2)
 for _ in range(300):
  mid=(lo+hi)/2
  if mid*mid<rad:lo=mid
  else:hi=mid
 assert lo*lo<rad<hi*hi
 return lo,hi
def pair_interval(pair,root_bounds):
 u,v=map(F,pair);lo,hi=root_bounds
 return (u+v*lo,u+v*hi) if v>=0 else (u+v*hi,u+v*lo)
def as_mp(v):return mp.mpf(v.numerator)/v.denominator

ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
args.output.mkdir(parents=True,exist_ok=False)
mp.mp.dps=100
saved=json.loads((HERE/'importance_run_v1/results.json').read_text())
casechecks=[]
for case in saved['cases']:
 eta=F(case['eta']);eps=F(case['epsilon']);ex=case['exact'];rad=F(ex['radicand'])
 assert rad==1+2*eta-3*eta*eta
 R=s.sqrt(s.Rational(rad.numerator,rad.denominator))
 pexpr=(1+s.Rational(eta))/(2*s.Rational(eta))-R/(2*s.Rational(eta))-s.Rational(eps)
 p_pair=ex['p_pair']
 assert s.simplify(s.Rational(p_pair[0])+s.Rational(p_pair[1])*R-pexpr)==0
 independent_J=s.Poly(J.subs({p:pexpr,e:s.Rational(eta)}),k)
 for actual,expected in zip(ex['cubic_pairs'],independent_J.all_coeffs()):
  assert s.simplify(s.Rational(actual[0])+s.Rational(actual[1])*R-expected)==0
 lo=F(ex['root_lower']);hi=F(ex['root_upper'])
 assert hi-lo==F(1,8)/2**200 and 0<lo<hi<F(1,8)
 for endpoint,stored_pair,want in [(lo,ex['lower_value'],-1),(hi,ex['upper_value'],1)]:
  expected=independent_J.eval(s.Rational(endpoint))
  assert s.simplify(s.Rational(stored_pair[0])+s.Rational(stored_pair[1])*R-expected)==0
  lower,upper=pair_interval(stored_pair,sqrt_bracket(rad))
  assert upper<0 if want<0 else lower>0
 plo,phi=pair_interval(p_pair,sqrt_bracket(rad))
 assert F(7,20)<plo<phi<F(21,50)
 assert F(12,25)<=eta<=F(13,25)
 ksaved=mp.mpf(case['k']);psaved=mp.mpf(case['p'])
 assert as_mp(lo)<ksaved<as_mp(hi)
 pexact=mp.mpf(str(s.N(pexpr,100)))
 assert abs(psaved-pexact)<mp.mpf('1e-68')
 assert abs(ksaved-(as_mp(lo)+as_mp(hi))/2)<mp.mpf('1e-68')
 casechecks.append(dict(eta=str(eta),epsilon=str(eps),all_exact_coefficients_and_bracket_signs=True,
                        numeric_p_error=str(abs(psaved-pexact)),numeric_k_midpoint_error=str(abs(ksaved-(as_mp(lo)+as_mp(hi))/2))))
assert len(casechecks)==4
result=dict(symbolic_checks=checks,four_saved_case_root_checks=casechecks,
 scope='Independent four-state algebra plus exact rational root-enclosure audit of the four already executed cases; no new experiments or global-proof substitute.')
(args.output/'results.json').write_text(json.dumps(result,indent=2))
(args.output/'source_sha256.json').write_text(json.dumps({Path(__file__).name:hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},indent=2))
print(json.dumps(result,indent=2))
