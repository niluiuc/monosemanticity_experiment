"""Independent active-subset certificate for the existing p=1/5 case.

Different branch construction from the student's score-ordered regions.
Uses the reviewed exact rational interval/root helpers for the common
algebraic-number backend. No training or new research settings.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import sympy as s

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('reviewed_root_backend',HERE/'certify_low_p.py')
backend=importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)
t=backend.t
den=1+t*t
states=list(itertools.product([0,1],repeat=2))
P=[s.Rational(16,25),s.Rational(4,25),s.Rational(4,25),s.Rational(1,25)]


def active_subset_candidates(feature):
    row=[1/den,t/den] if feature==0 else [t/den,t*t/den]
    offsets=[sum(row[i]*state[i] for i in range(2)) for state in states]
    labels=[state[feature] for state in states]
    out=[]
    for mask in itertools.product([False,True],repeat=4):
        if not any(mask):
            continue
        A=sum(P[j] for j in range(4) if mask[j])
        B=sum(P[j]*(labels[j]-offsets[j]) for j in range(4) if mask[j])
        C=sum(P[j]*((labels[j]-offsets[j])**2 if mask[j] else labels[j]**2) for j in range(4))
        beta=s.cancel(B/A)
        constraints=[backend.positive_numerator((offsets[j]+beta)*(1 if mask[j] else -1)) for j in range(4)]
        out.append((mask,beta,s.cancel(C-B*B/A),constraints))
    return out


def main():
    checked=[]
    branches=0
    for first,second in itertools.product(active_subset_candidates(0),active_subset_candidates(1)):
        branches+=1
        expression=s.cancel(first[2]+second[2]/2)
        constraints=first[3]+second[3]
        roots={}
        # t=0 also ensures a sample for a constant branch feasible everywhere.
        for polynomial in constraints+[backend.positive_numerator(s.diff(expression,t)),s.Poly(t,t)]:
            for root in backend.roots_of_expression(polynomial.as_expr()):
                roots[root['key']]=root
        for root in roots.values():
            if any(backend.sign_at(poly,root)<0 for poly in constraints):
                continue
            bounds=backend.value_interval(expression,root)
            checked.append({'expression':expression,'root':root,'bounds':bounds,
                            'active_subsets':[first[0],second[0]],'bias':[first[1],second[1]]})
    unique={}
    for candidate in checked:
        unique.setdefault((str(candidate['expression']),candidate['root']['key']),candidate)
    checked=list(unique.values())
    best=min(checked,key=lambda c:c['bounds'][1])
    others=[candidate for candidate in checked if candidate is not best]
    overlap=[candidate for candidate in others if candidate['bounds'][0]<=best['bounds'][1]]
    expected=s.Poly(20*t**3+175*t**2-60*t-59,t).monic()
    assert best['root']['poly']==expected
    assert best['root']['ab'][0]<s.Rational(-442,1000)
    assert best['root']['ab'][1]>s.Rational(-443,1000)
    assert not overlap
    assert best['bounds'][1]<s.Rational(2,25)
    # Any all-off feature already costs at least .1, exceeding this candidate.
    assert best['bounds'][1]<s.Rational(1,10)
    # Both ±infinity represent the mono code retaining feature 2: loss .16.
    assert best['bounds'][1]<s.Rational(4,25)
    expected_expression=(905*t**4-320*t**3+410*t*t+441)/(5250*den**2)
    assert s.cancel(best['expression']-expected_expression)==0
    expected_bias=[t*(5*t-1)/(21*den),1/(5*den)]
    assert all(s.cancel(found-required)==0 for found,required in zip(best['bias'],expected_bias))
    expected_derivative=8*t*(20*t**3+175*t*t-60*t-59)/(2625*den**3)
    assert s.cancel(s.diff(expected_expression,t)-expected_derivative)==0
    # Clean weaker reconstruction maximum is (t^2+1/5)/(1+t^2).
    half_minus_maximum=s.Rational(1,2)-(t*t+s.Rational(1,5))/den
    assert backend.sign_at(backend.positive_numerator(half_minus_maximum),best['root'])>0
    strong_gap_signs=[]
    for state in states:
        gap=(state[0]+t*state[1])/den+expected_bias[0]-s.Rational(1,2)
        sign=backend.sign_at(backend.positive_numerator(gap),best['root'])
        strong_gap_signs.append(sign)
        assert sign==(1 if state[0] else -1)
    result={'method':'Independent nonempty active-subset branch construction; reviewed shared exact root-isolation backend.',
        'joint_subset_branches':branches,
        'distinct_feasible_candidate_points':len(checked),
        'nonseparated_other_candidates':len(overlap),
        'certified_root_polynomial':str(best['root']['poly'].as_expr()),
        'root_interval':[str(x) for x in best['root']['ab']],
        'loss_interval':[str(x) for x in best['bounds']],
        'loss_approx':str(s.N(sum(best['bounds'])/2,20)),
        'active_subsets':best['active_subsets'],
        'all_off_lower_bound':'1/10',
        'infinity_optimal_loss':'4/25',
        'weaker_feature_max_reconstruction_strictly_below_half':True,
        'strong_feature_threshold_gap_signs':strong_gap_signs,
        'clean_weighted_detection_error':'1/10',
        'clean_selected_mono_weighted_detection_error':'1/10',
        'symbolic_derivative_and_bias_formula_checks':'passed'}
    (HERE/'teacher_low_p_check_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':
    main()
