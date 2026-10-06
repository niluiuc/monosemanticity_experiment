"""Rational CDF enclosure at ONE previously tested case/noise level.

No floating-point arithmetic is used for bound construction or sign tests.
Approximate decimals at the end are display labels, not the certificate.
"""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt, factorial
from decimal import Decimal, localcontext
import hashlib
import itertools
import json
import time
import sympy as s

HERE=Path(__file__).resolve().parent
CERTIFICATE=HERE.parent/'toy'/'run_v1'/'p_0.050'/'certificate_summary.json'
N=80  # even Taylor degree; the following odd degree supplies the lower bound
DIGITS=30
ARG_DIGITS=12


def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[1],-a[0]
def sub(a,b):return add(a,neg(b))
def mul(a,b):
    values=[x*y for x in a for y in b]
    return min(values),max(values)
def inverse(a):
    if a[0]<=0<=a[1]:raise ValueError('Denominator interval crosses zero')
    return 1/a[1],1/a[0]
def div(a,b):return mul(a,inverse(b))
def point(a):return F(a),F(a)
def sqrt_endpoint_bounds(x,digits=DIGITS):
    if x<0:raise ValueError('Negative square root')
    scale=10**digits
    n=isqrt(x.numerator*scale*scale//x.denominator)
    lo=F(n,scale)
    exact=(n*n*x.denominator==x.numerator*scale*scale)
    hi=lo if exact else F(n+1,scale)
    assert lo*lo<=x<=hi*hi
    return lo,hi
def sqrt_interval(a):
    return sqrt_endpoint_bounds(a[0])[0],sqrt_endpoint_bounds(a[1])[1]
def outward_decimal(a,digits=ARG_DIGITS):
    scale=10**digits
    lower=(a[0]*scale).__floor__()
    upper=(a[1]*scale).__ceil__()
    return F(lower,scale),F(upper,scale)


def atan_bounds(x,n=30):
    assert 0<x<1 and n%2==0
    upper=sum(((-1)**j*x**(2*j+1)/F(2*j+1)) for j in range(n+1))
    lower=upper-x**(2*n+3)/F(2*n+3)
    return lower,upper


def pi_bounds():
    x=F(1,5);y=F(1,239)
    tan2=2*x/(1-x*x)
    tan4=2*tan2/(1-tan2*tan2)
    assert (tan4-y)/(1+tan4*y)==1
    # Machin angle lies in (0,.8), and pi/2>1 from atan(1)>.5.
    assert 4*x/(1+x*x)-y>0
    return sub(mul(point(16),atan_bounds(x)),mul(point(4),atan_bounds(y)))


PI=pi_bounds()
C=inverse(sqrt_interval(mul(point(2),PI)))


def phi_point(x):
    if x<0:return sub(point(1),phi_point(-x))
    if x==0:return point(F(1,2))
    # Integrating even/odd exp(-u²/2) Taylor bounds on u in [0,x].
    upper=sum(((-1)**j*x**(2*j+1)/F(2**j*factorial(j)*(2*j+1)))
              for j in range(N+1))
    lower=upper-x**(2*N+3)/F(2**(N+1)*factorial(N+1)*(2*N+3))
    assert lower>=0
    result=add(point(F(1,2)),mul(C,(lower,upper)))
    assert result[0]<=result[1]
    return max(F(0),result[0]),min(F(1),result[1])


def phi_interval(a):
    # CDF monotonicity lets us round arguments outwards before exact series.
    rounded=outward_decimal(a)
    return phi_point(rounded[0])[0],phi_point(rounded[1])[1]


def as_json(a):return [str(a[0]),str(a[1])]
def approximate(x):
    with localcontext() as ctx:
        ctx.prec=24
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def main():
    start=time.time()
    saved=json.loads(CERTIFICATE.read_text())
    assert saved['strict_global_sharing_certificate']
    T=tuple(F(v) for v in saved['winner']['root']['isolating_interval'])
    symbol=s.symbols('t')
    poly=s.Poly(380*symbol**3+14800*symbol**2-1140*symbol-6839,symbol)
    assert poly.count_roots(s.Rational(T[0].numerator,T[0].denominator),
                            s.Rational(T[1].numerator,T[1].denominator))==1
    assert T[1]<0
    T2=mul(T,T)
    denominator=add(point(1),T2)
    a=inverse(denominator)
    c=div(T2,denominator)
    off=div(T,denominator)
    beta1=div(sub(mul(point(20),T2),T),mul(point(381),denominator))
    beta2=inverse(mul(point(20),denominator))
    norms=[inverse(sqrt_interval(denominator)),
           div(neg(T),sqrt_interval(denominator))]
    G=[[a,off],[off,c]]
    beta=[beta1,beta2]
    p=F(1,20);q=1-p;sigma=F(3,10)
    weights=[F(1),F(1,2)]
    risks=[point(0),point(0)]
    details=[]
    clean_weighted=F(0)
    for bits in itertools.product([0,1],repeat=2):
        prob=F(1)
        for bit in bits:prob*=p if bit else q
        for i in [0,1]:
            score=add(mul(G[i][0],point(bits[0])),mul(G[i][1],point(bits[1])))
            margin=sub(add(score,beta[i]),point(F(1,2)))
            assert margin[1]<0 or margin[0]>0
            predicted=int(margin[0]>0)
            clean_weighted+=weights[i]*prob*int(predicted!=bits[i])
            signed=mul(point(2*bits[i]-1),margin)
            argument=neg(div(signed,mul(point(sigma),norms[i])))
            cdf=phi_interval(argument)
            risks[i]=add(risks[i],mul(point(prob),cdf))
            details.append({'bits':list(bits),'feature':i,'probability':str(prob),
                            'margin_interval':as_json(margin),
                            'argument_interval':as_json(argument),
                            'error_probability_interval':as_json(cdf)})
    super_risk=add(risks[0],mul(point(F(1,2)),risks[1]))
    mono_retained=phi_point(-F(5,3)) # -.5/.3
    mono_risk=add(mono_retained,point(p/2))
    difference=sub(super_risk,mono_risk)
    clean_mono=p/2
    clean_difference=clean_weighted-clean_mono
    infinity_difference=sum(weights)/2-(F(1,2)+p/2)
    assert clean_difference==F(1,400)
    assert infinity_difference==F(9,40)
    assert difference[1]<0
    result={'case':{'p':'1/20','importance':['1','1/2'],'sigma':'3/10',
                    'decoder':'strict reconstruction>.5','encoder_energy':'1'},
            'method':'exact rational root enclosure, Machin pi, integer sqrt, integrated exponential Taylor bounds',
            'source_geometry_certificate_sha256':hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
            'root_interval':as_json(T),'pi_interval':as_json(PI),
            'normal_density_constant_interval':as_json(C),
            'super_risk_interval':as_json(super_risk),'mono_risk_interval':as_json(mono_risk),
            'difference_interval':as_json(difference),
            'difference_approximate_midpoint':approximate(sum(difference)/2),
            'difference_upper_bound_negative':True,
            'clean_super_risk':str(clean_weighted),'clean_mono_risk':str(clean_mono),
            'clean_difference':str(clean_difference),'infinite_noise_difference':str(infinity_difference),
            'CDF_even_Taylor_degree':N,'arctan_even_degree':30,
            'argument_outward_decimal_digits':ARG_DIGITS,'sqrt_decimal_digits':DIGITS,
            'details':details,'seconds':time.time()-start,
            'conclusion':'at least two positive noise crossings by continuity; not exact roots or total root count'}
    (HERE/'noise_sign_certificate_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({key:result[key] for key in [
        'difference_approximate_midpoint','difference_upper_bound_negative',
        'clean_difference','infinite_noise_difference','seconds','conclusion']},indent=2))


if __name__=='__main__':main()
