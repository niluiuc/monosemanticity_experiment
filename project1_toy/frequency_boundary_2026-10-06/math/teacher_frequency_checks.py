"""Independent active-mask symbolic checks of Stage A; no numerical sweep."""
import itertools
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
p,k=s.symbols('p k',real=True)
q=1-p
D=1-p+p*p
a=1/(1+k*k)
c=k*k/(1+k*k)
r=k/(1+k*k)
states=list(itertools.product([0,1],repeat=2))
prob=[q*q,p*q,p*q,p*p]


def quadratic_from_mask(offsets,feature,mask):
    labels=[state[feature] for state in states]
    mass=sum(prob[j] for j in range(4) if mask[j])
    linear=sum(prob[j]*(labels[j]-offsets[j]) for j in range(4) if mask[j])
    constant=sum(prob[j]*((labels[j]-offsets[j])**2 if mask[j] else labels[j]**2) for j in range(4))
    return s.cancel(linear/mass),s.cancel(constant-linear*linear/mass)


def main():
    checks={}
    strong_minus=[0,-r,a,a-r]
    weak_minus=[0,c,-r,c-r]
    strong_plus=[0,r,a,a+r]
    weak_plus=[0,c,r,c+r]
    Bs,Sm=quadratic_from_mask(strong_minus,0,[1,0,1,1])
    Bw3,W3=quadratic_from_mask(weak_minus,1,[1,1,0,1])
    Bw2,W2=quadratic_from_mask(weak_minus,1,[1,1,0,0])
    Bwa,Wa=quadratic_from_mask(weak_minus,1,[1,1,1,1])
    Bsp,Sp=quadratic_from_mask(strong_plus,0,[0,1,1,1])
    Bwp,Wp=quadratic_from_mask(weak_plus,1,[1,1,1,1])
    same=lambda x,y:s.cancel(x-y)==0
    checks['opposite_strong_bias']=same(Bs,p*(c+p*r)/D)
    checks['opposite_strong_loss']=same(Sm,p*q*c-p*q*(q*r-p*c)**2/D)
    checks['opposite_weak_three_bias']=same(Bw3,p*(a+p*r)/D)
    checks['opposite_weak_three_loss']=same(W3,p*q*a-p*q*(q*r-p*a)**2/D)
    checks['opposite_weak_two_bias']=same(Bw2,p*a)
    checks['opposite_weak_two_loss']=same(W2,p*q*q*a*a+p*p)
    checks['opposite_weak_all_bias']=same(Bwa,p*(a+r))
    checks['opposite_weak_all_loss']=same(Wa,p*q*a)
    checks['same_strong_bias']=same(Bsp,(c-r)/(2-p))
    checks['same_strong_loss']=same(Sp,p*q*c*(1+2*q*r)/(2-p))
    checks['same_weak_bias']=same(Bwp,p*(a-r))
    checks['same_weak_loss']=same(Wp,p*q*a)
    checks['two_active_feasibility']=same(p*a-(r-c),(p-k+k*k)/(1+k*k))
    checks['three_active_lower_feasibility']=same(Bw3-(r-c),(p+D*k*k-q*k)/(D*(1+k*k)))
    checks['weak_three_orientation']=same(W3-Sm,p*q*(a-c)*(q+2*p*q*r)/D)
    delta_all=Sm+Wa/2-p*q/2
    checks['all_active_difference']=same(delta_all,p*q*c*(p-D/2+(1-2*p)*c+2*p*q*r)/D)
    H=s.cancel((Sm+W3/2-p*q/2)*2*D*(1+k*k)**2/(p*q))
    A=1-p-p*p
    B=-2+5*p-2*p*p
    checks['three_active_polynomial']=same(H,A*k**4+4*p*q*k**3+B*k*k+2*p*q*k-p*p)
    checks['H_derivative_decomposition']=same(s.diff(H,k),4*A*k**3+2*p*k*(6*q*k-1)+2*p*q+2*(B+p)*k)
    checks['B_positive_domain_identity']=same(B+p,-2*(p*p-3*p+1))
    checks['branch_boundary_agreement']=same((W3-Wa).subs(k,p/q),0)
    checks['mono_quadratic_coefficient']=same(s.limit(delta_all/(k*k),k,0),p*q*(p/D-s.Rational(1,2)))
    pc=(3-s.sqrt(5))/2
    checks['critical_polynomial']=s.simplify((p*p-3*p+1).subs(p,pc))==0
    checks['pc_above_quarter']=bool(pc>s.Rational(1,4))
    checks['pc_above_sixth']=bool(pc>s.Rational(1,6))
    checks['pc_below_half']=bool(pc<s.Rational(1,2))
    assert all(checks.values())
    result={'method':'Independent population quadratics from explicit active masks; exact symbolic identities only.',
            'checks':checks,'all_checks_pass':True,'check_count':len(checks),
            'pc_exact':str(pc),'pc_approx':str(s.N(pc,20)),
            'scope':'Global inequalities and interval coverage independently reviewed in teacher_review.md; no frequency/angle sweep.'}
    (HERE/'teacher_check_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
