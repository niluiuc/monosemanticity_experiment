"""Finite exact-rational clean optimum certificate for one prescribed case.

Case p=1/5, importance (1,1/2), two concepts / one code dimension,
encoder energy one. Symbolic algebra and Sturm root isolation only; no
empirical fit, training campaign, or new parameter sweep.
"""
from pathlib import Path
from functools import lru_cache
import itertools
import json
import time
import sympy as s

HERE=Path(__file__).resolve().parent
t=s.symbols('t',real=True)
den=1+t*t
P=[s.Rational(16,25),s.Rational(4,25),s.Rational(4,25),s.Rational(1,25)]
states=list(itertools.product([0,1],repeat=2))
eps=s.Rational(1,10**35)


def interval_add(a,b): return (a[0]+b[0],a[1]+b[1])
def interval_mul(a,b):
    v=[a[i]*b[j] for i in [0,1] for j in [0,1]]
    return min(v),max(v)
def polynomial_interval(poly,ab):
    result=(s.Rational(0),s.Rational(0))
    for coefficient in poly.all_coeffs():
        result=interval_add(interval_mul(result,ab),(coefficient,coefficient))
    return result


def positive_numerator(expr):
    N,D=s.fraction(s.cancel(expr))
    # Every denominator is a nonzero constant times (1+t²), hence fixed sign.
    if D.subs(t,0)<0: N=-N
    return s.Poly(N,t,domain=s.QQ)


@lru_cache(None)
def roots_of_expression(expression):
    poly=s.Poly(expression,t,domain=s.QQ)
    if poly.is_zero or poly.degree()==0:return ()
    out=[]
    for factor,multiplicity in s.factor_list(poly)[1]:
        monic=factor.monic()
        for j,(ab,m) in enumerate(monic.intervals(eps=eps)):
            out.append({'poly':monic,'ab':ab,
                        'key':str(monic.as_expr())+'#'+str(j)})
    return tuple(out)


def sign_at(poly,root):
    if poly.is_zero:return 0
    a,b=root['ab']
    if a==b:
        value=poly.eval(a)
        return int(s.sign(value))
    value=polynomial_interval(poly,(a,b))
    if value[0]>0:return 1
    if value[1]<0:return -1
    gcd=s.gcd(poly,root['poly'])
    if gcd.degree()>0 and gcd.count_roots(a,b)>0:return 0
    for refinement in range(1,6):
        a,b=root['poly'].refine_root(a,b,eps=eps/s.Integer(10)**(10*refinement))
        value=polynomial_interval(poly,(a,b))
        if value[0]>0:return 1
        if value[1]<0:return -1
    raise RuntimeError('Cannot certify sign: '+str(poly.as_expr())+' at '+root['key'])


def value_interval(expr,root):
    N,D=s.fraction(s.cancel(expr))
    lo,hi=polynomial_interval(s.Poly(N,t),root['ab'])
    dlo,dhi=polynomial_interval(s.Poly(D,t),root['ab'])
    if dlo<=0:
        if dhi<0:
            lo,hi=-hi,-lo;dlo,dhi=-dhi,-dlo
        else:raise RuntimeError('Uncertified denominator')
    vals=[lo/dlo,lo/dhi,hi/dlo,hi/dhi]
    return min(vals),max(vals)


def feature_candidates(i,sample):
    row=[1/den,t/den] if i==0 else [t/den,t*t/den]
    offsets=[sum(row[j]*b[j] for j in [0,1]) for b in states]
    labels=[b[i] for b in states]
    breaks=sorted(set([-v for v in offsets]),key=lambda v:v.subs(t,sample))
    candidates=[]
    # Every kink is a valid bias; use the active set from the region interior.
    for j,beta in enumerate(breaks):
        active=[(offsets[k]+beta).subs(t,sample)>0 for k in range(4)]
        loss=sum(P[k]*((offsets[k]+beta-labels[k])**2 if active[k]
                      else labels[k]**2) for k in range(4))
        candidates.append({'name':f'f{i}_kink{j}','bias':s.cancel(beta),
                           'loss':s.cancel(loss),'constraints':[]})
    # Four nonempty active intervals; the far-left constant is included by kink0.
    edges=breaks+[None]
    for j,left in enumerate(breaks):
        right=edges[j+1]
        probe=left+1 if right is None else (left+right)/2
        active=[(offsets[k]+probe).subs(t,sample)>0 for k in range(4)]
        A=sum(P[k] for k in range(4) if active[k])
        B=sum(P[k]*(labels[k]-offsets[k]) for k in range(4) if active[k])
        C=sum(P[k]*((labels[k]-offsets[k])**2 if active[k]
                   else labels[k]**2) for k in range(4))
        beta=s.cancel(B/A)
        constraints=[positive_numerator(beta-left)]
        if right is not None:constraints.append(positive_numerator(right-beta))
        candidates.append({'name':f'f{i}_vertex{j}','bias':beta,
                           'loss':s.cancel(C-B*B/A),'constraints':constraints})
    return candidates


def main():
    start=time.time()
    regions=[(None,-1,s.Rational(-2)),(-1,0,s.Rational(-1,2)),
             (0,1,s.Rational(1,2)),(1,None,s.Rational(2))]
    checked=[]
    joint_branches=0
    raw_candidates=0
    for rid,(left,right,sample) in enumerate(regions):
        first=feature_candidates(0,sample)
        second=feature_candidates(1,sample)
        region_constraints=[]
        if left is not None:region_constraints.append(s.Poly(t-left,t))
        if right is not None:region_constraints.append(s.Poly(right-t,t))
        for c1,c2 in itertools.product(first,second):
            joint_branches+=1
            expr=s.cancel(c1['loss']+c2['loss']/2)
            constraints=region_constraints+c1['constraints']+c2['constraints']
            critical=positive_numerator(s.diff(expr,t))
            roots={}
            for poly in constraints+[critical]:
                for root in roots_of_expression(poly.as_expr()):
                    roots[root['key']]=root
            for root in roots.values():
                raw_candidates+=1
                if any(sign_at(poly,root)<0 for poly in constraints):continue
                bounds=value_interval(expr,root)
                checked.append({'region':rid,'branch':[c1['name'],c2['name']],
                                'expr':expr,'root':root,'bounds':bounds,
                                'bias':[c1['bias'],c2['bias']]})
        print('region',rid,'branches',joint_branches,'feasible points',len(checked),flush=True)
    if not checked:raise RuntimeError('No feasible candidates')
    # Duplicated candidate branches/functions have the same exact stationary root.
    unique={}
    for c in checked:
        key=(str(c['expr']),c['root']['key'])
        if key not in unique:unique[key]=c
    checked=list(unique.values())
    winner=min(checked,key=lambda c:c['bounds'][1])
    competing=[c for c in checked if c is not winner]
    overlap=[c for c in competing if c['bounds'][0]<=winner['bounds'][1]]
    # At t=±infinity the optimal mono loss is 4/25; retaining first at t=0 is 2/25.
    mono_first=s.Rational(2,25);mono_second=s.Rational(4,25)
    certified=bool(not overlap and winner['bounds'][1]<mono_first)
    summary={'case':{'p':'1/5','importance':['1','1/2'],'encoder_energy':'1'},
             'method':'finite bias candidates; rational stationary/feasibility roots; exact interval comparisons',
             'joint_branch_count':joint_branches,'raw_root_candidate_count':raw_candidates,
             'distinct_feasible_root_candidates':len(checked),
             'certified_global_minimum':certified,
             'winner':{'region':winner['region'],'branches':winner['branch'],
                       'objective':str(winner['expr']),
                       'stationary_polynomial':str(winner['root']['poly'].as_expr()),
                       'isolating_interval':[str(v) for v in winner['root']['ab']],
                       't_approx':str(s.N(sum(winner['root']['ab'])/2,20)),
                       'loss_interval':[str(v) for v in winner['bounds']],
                       'loss_approx':str(s.N(sum(winner['bounds'])/2,20)),
                       'bias_formulas':[str(v) for v in winner['bias']]},
             'nonseparated_candidate_count':len(overlap),
             'smallest_other_candidate_lower_bound':str(min(c['bounds'][0] for c in competing)),
             'mono_first_optimal_loss':str(mono_first),'mono_second_optimal_loss':str(mono_second),
             'runtime_seconds':time.time()-start,'sympy_version':s.__version__}
    serial=[]
    for c in checked:
        serial.append({'region':c['region'],'branches':c['branch'],
                       'objective':str(c['expr']),'root_polynomial':str(c['root']['poly'].as_expr()),
                       'root_interval':[str(v) for v in c['root']['ab']],
                       'objective_interval':[str(v) for v in c['bounds']]})
    (HERE/'low_p_certificate_results.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (HERE/'low_p_certificate_candidates.json').write_text(json.dumps(serial,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':main()
