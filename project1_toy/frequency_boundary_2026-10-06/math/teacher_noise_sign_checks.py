"""One-case independent mapping/series checks, without new settings.

Exact interval construction is reviewed in teacher_noise_sign_review.md.
100-digit CDF references are implementation crosschecks, not sign proofs.
"""
import importlib.util
import itertools
import json
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp
import sympy as s

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('noise_student',HERE/'certify_noise_sign.py')
student=importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)


def mp_fraction(x):
    return mp.mpf(x.numerator)/mp.mpf(x.denominator)


def independent_atan_bounds(x):
    term=x
    partial=term
    for j in range(1,31):
        term=-term*x*x*F(2*j-1,2*j+1)
        partial+=term
    next_term=-term*x*x*F(61,63)
    return partial+next_term,partial


def main():
    mp.mp.dps=100
    original=json.loads((HERE/'noise_sign_certificate_results.json').read_text())
    reproduction=json.loads((HERE/'teacher_noise_sign_reproduction/noise_sign_certificate_results.json').read_text())
    assert {k:v for k,v in original.items() if k!='seconds'}=={k:v for k,v in reproduction.items() if k!='seconds'}
    saved=json.loads(student.CERTIFICATE.read_text())
    symbol=s.symbols('t')
    claimed_poly=s.Poly(380*symbol**3+14800*symbol**2-1140*symbol-6839,symbol)
    assert s.Poly(s.sympify(saved['winner']['root']['polynomial'],locals={'t':symbol}),symbol).monic()==claimed_poly.monic()
    expressions=[(20*symbol*symbol-symbol)/(381*(1+symbol*symbol)),1/(20*(1+symbol*symbol))]
    assert all(s.cancel(s.sympify(found,locals={'t':symbol})-required)==0 for found,required in zip(saved['winner']['bias_formulas'],expressions))
    for x in [F(1,5),F(1,239)]:
        assert independent_atan_bounds(x)==student.atan_bounds(x)
    x=F(1,5);y=F(1,239)
    twice=2*x/(1-x*x)
    fourth=2*twice/(1-twice*twice)
    assert (fourth-y)/(1+fourth*y)==1
    assert 4*x/(1+x*x)-y>0
    PI=tuple(F(z) for z in original['pi_interval'])
    assert mp_fraction(PI[0])<mp.pi<mp_fraction(PI[1])
    root=tuple(F(z) for z in original['root_interval'])
    t=mp_fraction(sum(root)/2)
    denominator=1+t*t
    G=[[1/denominator,t/denominator],[t/denominator,t*t/denominator]]
    beta=[(20*t*t-t)/(381*denominator),1/(20*denominator)]
    norm=[1/mp.sqrt(denominator),-t/mp.sqrt(denominator)]
    sigma=mp.mpf(3)/10
    p=F(1,20);q=1-p
    references=[]
    clean=F(0)
    total=mp.mpf(0)
    for detail in original['details']:
        bits=detail['bits'];i=detail['feature']
        z=sum(G[i][j]*bits[j] for j in range(2))+beta[i]
        argument=(1-2*bits[i])*(z-mp.mpf(1)/2)/(sigma*norm[i])
        cdf=(1+mp.erf(argument/mp.sqrt(2)))/2
        ai=tuple(F(z) for z in detail['argument_interval'])
        ci=tuple(F(z) for z in detail['error_probability_interval'])
        assert mp_fraction(ai[0])<=argument<=mp_fraction(ai[1])
        assert mp_fraction(ci[0])<=cdf<=mp_fraction(ci[1])
        # Different recurrence for the integrated Taylor polynomial coefficients.
        positive=student.outward_decimal(ai)
        for endpoint in positive:
            xx=abs(endpoint)
            term=xx
            upper=term
            for j in range(1,81):
                term=-term*xx*xx*F(2*j-1,2*j*(2*j+1))
                upper+=term
            lower=upper-term*xx*xx*F(161,162*163)
            assert lower>=0
            reconstructed=student.add(student.point(F(1,2)),student.mul(student.C,(lower,upper)))
            reconstructed=max(F(0),reconstructed[0]),min(F(1),reconstructed[1])
            if endpoint<0:
                reconstructed=student.sub(student.point(1),reconstructed)
            assert reconstructed==student.phi_point(endpoint)
        prob=F(detail['probability'])
        weight=F(1) if i==0 else F(1,2)
        clean+=weight*prob*int((z>mp.mpf(1)/2)!=bool(bits[i]))
        total+=mp_fraction(weight*prob)*cdf
        references.append({'bits':bits,'feature':i,'CDF_reference':str(mp.nstr(cdf,30))})
    mono=(1+mp.erf(-mp.mpf(5)/(3*mp.sqrt(2))))/2+mp.mpf(1)/40
    difference=total-mono
    enclosure=tuple(F(z) for z in original['difference_interval'])
    assert mp_fraction(enclosure[0])<difference<mp_fraction(enclosure[1])
    assert enclosure[1]<0
    assert clean==F(11,400)
    assert clean-F(1,40)==F(1,400)
    assert F(3,4)-(F(1,2)+F(1,40))==F(9,40)
    result={'source_mapping_checks':'passed','fresh_reproduction_except_runtime':'identical',
            'independent_series_recurrence_checks':'passed',
            'CDF_state_reference_checks':references,
            'reference_precision_digits':100,
            'difference_reference':str(mp.nstr(difference,30)),
            'clean_super_error':'11/400','clean_difference':'1/400',
            'infinite_noise_difference':'9/40',
            'all_checks_pass':True,
            'scope':'Exactly the already declared p=1/20, sigma=3/10, selected geometry; no root searches or new settings.'}
    (HERE/'teacher_noise_sign_check_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='CDF_state_reference_checks'},indent=2))


if __name__=='__main__':
    main()
