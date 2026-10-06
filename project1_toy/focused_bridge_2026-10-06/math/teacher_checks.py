"""Independent teacher checks; no model training or expanded experiment sweep.

The student uses ordered activation intervals. This checker enumerates all 16
active-state subsets instead, plus every kink and the all-off representative.
"""
import importlib.util
import itertools
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('student', HERE/'verify_derivation.py')
student = importlib.util.module_from_spec(spec)
spec.loader.exec_module(student)
states = np.array(list(itertools.product([0.,1.], repeat=2)))


def subset_bias(offsets, labels, probability):
    candidates = list(-offsets)
    candidates.append(float(-np.max(offsets)-1))
    for mask in itertools.product([False,True], repeat=4):
        active = np.array(mask)
        mass = probability[active].sum()
        if mass == 0:
            continue
        beta = np.dot(probability[active], labels[active]-offsets[active])/mass
        z = offsets+beta
        # Inclusion at a kink is harmless because ReLU's value is continuous.
        if np.all(z[active]>=-1e-12) and np.all(z[~active]<=1e-12):
            candidates.append(float(beta))
    loss = lambda beta: float(np.dot(probability,
        (np.maximum(offsets+beta,0)-labels)**2))
    losses = np.array([loss(b) for b in candidates])
    index = int(np.argmin(losses))
    return candidates[index],float(losses[index])


def main():
    max_discrepancy = 0.
    max_pair_bias_discrepancy = 0.
    max_pair_loss_discrepancy = 0.
    checked = 0
    angles = [-np.pi/2,-3*np.pi/8,-np.pi/4,-np.pi/8,0,np.pi/8,np.pi/4,np.pi/2]
    for p in [.05,.2,.5]:
        probability = np.prod(np.where(states==1,p,1-p),axis=1)
        for angle in angles:
            w = np.array([np.cos(angle),np.sin(angle)])
            G = np.outer(w,w)
            for feature in range(2):
                offsets = states@G[feature]
                b,L = subset_bias(offsets,states[:,feature],probability)
                bs,Ls,_ = student.optimum_bias(offsets,states[:,feature],probability)
                max_discrepancy = max(max_discrepancy,abs(L-Ls))
                checked += 1
        # Exactly opposite columns avoid introducing a spurious asymmetric tie.
        G = np.array([[.5,-.5],[-.5,.5]])
        b,L = subset_bias(states@G[0],states[:,0],probability)
        max_pair_bias_discrepancy = max(max_pair_bias_discrepancy,abs(b-student.pair_bias(p)))
        max_pair_loss_discrepancy = max(max_pair_loss_discrepancy,abs(L-student.pair_feature_loss(p)))

    t = 1/np.sqrt(2)
    w = np.array([np.sin(np.pi/8),-np.cos(np.pi/8)])
    G = np.outer(w,w)
    probability = np.full(4,.25)
    beta = np.array([(1+2*t)/4,(2-t)/6])
    numerical_losses = np.dot(probability,(np.maximum(states@G+beta,0)-states)**2)
    exact_losses = np.array([(1+t)/8,(3-2*t)/48])
    dense_formula_errors = []
    dense_bias_loss_errors = []
    for angle in np.linspace(-np.pi/2,np.pi/2,361):
        dense_w = np.array([np.cos(angle),np.sin(angle)])
        a = float(np.max(dense_w**2))
        c = 1-a
        r = float(np.sqrt(max(0,a*c)))
        opposite = dense_w[0]*dense_w[1]<0
        order = np.argsort(-dense_w**2)
        dense_G = np.outer(dense_w,dense_w)
        theoretical_bias = ([(2*c+r)/3,(a+r)/2] if opposite
                            else [2*(c-r)/3,(a-r)/2])
        observed = []
        for feature in order:
            _,Li = subset_bias(states@dense_G[feature],states[:,feature],probability)
            observed.append(Li)
        theoretical_loss = .25+c*(2*r-1)/12
        dense_formula_errors.append(abs(sum(observed)-theoretical_loss))
        for index,feature in enumerate(order):
            loss_at_formula = float(np.dot(probability,
                (np.maximum(states@dense_G[feature]+theoretical_bias[index],0)-states[:,feature])**2))
            dense_bias_loss_errors.append(abs(loss_at_formula-observed[index]))
    result = {
        'independent_active_subset_cases':checked,
        'maximum_bias_minimum_loss_discrepancy':max_discrepancy,
        'maximum_pair_bias_formula_discrepancy':max_pair_bias_discrepancy,
        'maximum_pair_feature_loss_discrepancy':max_pair_loss_discrepancy,
        'counterexample':{
            'W':w.tolist(),'bias':beta.tolist(),
            'feature_losses':numerical_losses.tolist(),
            'exact_total_expression':'(9 + 2*sqrt(2))/48',
            'exact_total_value':float((9+2*np.sqrt(2))/48),
            'direct_population_total':float(numerical_losses.sum()),
            'strict_gap_below_quarter':float((3-2*np.sqrt(2))/48),
            'maximum_expression_discrepancy':float(np.max(np.abs(numerical_losses-exact_losses))),
        },
        'dense_equalimportance_branch_check':{
            'angles_checked':361,
            'maximum_profiled_loss_formula_discrepancy':max(dense_formula_errors),
            'maximum_loss_at_analytic_bias_discrepancy':max(dense_bias_loss_errors),
            'analytic_global_claim':'p=0.5, importance=(1,1), energy=1 only; proof reviewed separately.'
        },
        'scope':'Independent finite-case checks, exact counterexample, and checks of the dense special-case proof; no general-p geometry claim.'
    }
    assert max_discrepancy<1e-12
    assert max_pair_bias_discrepancy<1e-12
    assert max_pair_loss_discrepancy<1e-12
    assert result['counterexample']['maximum_expression_discrepancy']<1e-12
    assert result['counterexample']['strict_gap_below_quarter']>0
    assert max(dense_formula_errors)<1e-12
    assert max(dense_bias_loss_errors)<1e-12
    (HERE/'teacher_check_results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
