"""Exact Q(sqrt5) root brackets for six prescribed clean global optima.

The strip theorem excludes other geometry/bias sectors. This script verifies
symbolic identities and brackets its unique cubic root without rationalizing p.
No noise experiment or additional parameter settings.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
import sympy as s
import mpmath as mp

HERE=Path(__file__).resolve().parent
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def neg(a):return (-a[0],-a[1])
def mul(a,b):return (a[0]*b[0]+5*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,z):return (a[0]*z,a[1]*z)
def const(z):return (F(z),F(0))
def sign(a):
    u,v=a
    if v==0:return (u>0)-(u<0)
    if u==0:return (v>0)-(v<0)
    if u>0 and v>0:return 1
    if u<0 and v<0:return -1
    compare=(u*u>5*v*v)-(u*u<5*v*v)
    return compare if u>0 else -compare
def evaluate(coefficients,k):
    value=const(0)
    for a in coefficients:value=add(scale(value,k),a)
    return value
def strings(pair):return [str(v) for v in pair]

def main():
    out=HERE/'clean_global_certificate_v1';out.mkdir(exist_ok=False)
    p,k=s.symbols('p k');q=1-p;D=1-p+p*p;A=p-D/2
    delta=p*q/D*k*k*(A+2*p*q*k+(1-p-p*p)*k*k/2)/(1+k*k)**2
    J=A+3*p*q*k+(3-5*p-p*p)*k*k/2-p*q*k**3
    identities={'stationarity_cubic':s.factor(s.diff(delta,k)-2*p*q/D*k*J/(1+k*k)**3)==0,
                'cubic_monotonicity':s.expand(s.diff(J,k)-3*p*q*(1-k*k)-(3-5*p-p*p)*k)==0,
                'strip_H_boundary_lower':s.Rational(-31,1250)+2*s.Rational(144,625)*s.Rational(144,337)==s.Rational(72497,421250),
                'strip_J_endpoint_lower':s.Rational(-31,1250)+s.Rational(3,8)*s.Rational(144,625)-s.Rational(1,512)*s.Rational(1,4)==s.Rational(78223,1280000)}
    assert all(identities.values())
    saved=json.loads((HERE/'frozen_run_v1/results.json').read_text());cases=[];mp.mp.dps=70
    for case in saved['cases']:
        eps=F(case['epsilon']);P=(F(3,2)-eps,F(-1,2));Q=add(const(1),neg(P));PQ=mul(P,Q);P2=mul(P,P)
        AP=add(P,scale(add(add(const(1),neg(P)),P2),F(-1,2)))
        JP=scale(add(add(const(3),scale(P,-5)),neg(P2)),F(1,2))
        coefficients=[neg(PQ),JP,scale(PQ,3),AP]
        lo=F(0);hi=F(1,8)
        assert sign(evaluate(coefficients,lo))==-1 and sign(evaluate(coefficients,hi))==1
        for _ in range(200):
            mid=(lo+hi)/2
            if sign(evaluate(coefficients,mid))<0:lo=mid
            else:hi=mid
        def number(x):return mp.mpf(x.numerator)/x.denominator
        numeric=mp.mpf(case['k'])
        assert number(lo)<numeric<number(hi)
        assert sign(add(P,const(-F(9,25))))>=0
        cases.append(dict(epsilon=case['epsilon'],p_field=strings(P),cubic_coefficients_descending=[strings(a) for a in coefficients],
                          exact_root_lower=str(lo),exact_root_upper=str(hi),exact_width=str(hi-lo),
                          lower_field_value=strings(evaluate(coefficients,lo)),upper_field_value=strings(evaluate(coefficients,hi)),
                          lower_sign=-1,upper_sign=1,saved_numeric_root_inside=True,global_selection_basis='global_strip_certificate.tex'))
    result=dict(method='Exact rational-pair arithmetic in Q(sqrt5); monotone cubic bisection200 iterations; global strip theorem',
                identities=identities,cases=cases,all_passed=True,scope='Exact clean root brackets and global analytical branch proof; corrupted risk remains high-precision numerical evaluation.')
    (out/'results.json').write_text(json.dumps(result,indent=2))
    (out/'source_sha256.json').write_text(json.dumps({str(p.relative_to(HERE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'global_strip_certificate.tex']},indent=2))
    print(json.dumps(dict(all_passed=True,exact_brackets=len(cases),identities=identities),indent=2))

if __name__=='__main__':main()
