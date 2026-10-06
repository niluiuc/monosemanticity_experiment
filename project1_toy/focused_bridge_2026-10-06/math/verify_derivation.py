"""Independent finite-interval checks of the bounded mathematical derivation.

No training runs or parameter extensions; 361-angle diagnostic prescribed in
protocol.md. A grid minimum is numerical evidence, never a global proof.
"""
import itertools
import json
from pathlib import Path
import numpy as np
from scipy.special import ndtr

HERE = Path(__file__).resolve().parent
STATES = np.array(list(itertools.product([0., 1.], repeat=2)))


def optimum_bias(offsets, labels, probabilities):
    """Global minimizer by all breakpoints and interval quadratic vertices."""
    breaks = np.unique(-np.asarray(offsets))
    candidates = list(breaks)
    edges = np.r_[-np.inf, breaks, np.inf]
    records = []
    for left, right in zip(edges[:-1], edges[1:]):
        probe = (right - 1 if np.isneginf(left) else
                 left + 1 if np.isposinf(right) else (left + right) / 2)
        active = offsets + probe > 0
        A = float(probabilities[active].sum())
        B = float(np.sum(probabilities[active] * (labels[active] - offsets[active])))
        C = float(np.sum(probabilities[active] * (labels[active] - offsets[active])**2)
                  + np.sum(probabilities[~active] * labels[~active]**2))
        if A > 0:
            vertex = float(np.clip(B / A, left, right))
            candidates.append(vertex)
        else:
            vertex = None
        records.append({'left': float(left), 'right': float(right),
                        'A': A, 'B': B, 'C': C, 'vertex': vertex})
    candidates = np.unique(candidates)
    losses = np.sum(probabilities[None, :] *
                    (np.maximum(offsets[None, :] + candidates[:, None], 0)
                     - labels[None, :])**2, axis=1)
    j = int(np.argmin(losses))
    return float(candidates[j]), float(losses[j]), records


def profile(theta, p, importance):
    w = np.array([np.cos(theta), np.sin(theta)])
    G = np.outer(w, w)
    probabilities = np.prod(np.where(STATES == 1, p, 1-p), axis=1)
    biases, losses = [], []
    for i in range(2):
        b, L, _ = optimum_bias(STATES @ G[i], STATES[:, i], probabilities)
        biases.append(b)
        losses.append(L)
    return float(np.dot(importance, losses)), np.array(biases), w


def pair_bias(p):
    return p*(1+p)/(2*(1-p+p*p)) if p <= .5 else p


def pair_feature_loss(p):
    if p <= .5:
        D = 1-p+p*p
        N = p*(1+p)/2
        return p*(1-p)/4 + p*p - N*N/D
    return p*(1-p)/2


def pair_feature_detection(p, sigma):
    threshold = .5-pair_bias(p)
    if sigma == 0:
        offsets = np.array([0, -.5, .5, 0])
        probs = np.array([(1-p)**2, p*(1-p), p*(1-p), p*p])
        return float(np.dot(probs, (offsets > threshold) != STATES[:, 0]))
    scale = sigma/np.sqrt(2)
    q = 1-p
    return float(q*q*ndtr(-threshold/scale)
                 + p*q*ndtr((threshold-.5)/scale)
                 + p*q*ndtr((-.5-threshold)/scale)
                 + p*p*ndtr(threshold/scale))


def actual_detection(w, biases, p, importance, sigma):
    """Independent state-integrated error for the clean-selected decoder."""
    G = np.outer(w,w)
    scores = STATES @ G.T
    thresholds = .5-np.asarray(biases)
    probabilities = np.prod(np.where(STATES == 1,p,1-p),axis=1)
    errors = ((scores>thresholds)!=STATES).astype(float)
    if sigma>0:
        stored = np.abs(w)>1e-14
        gaps=(2*STATES[:,stored]-1)*(scores[:,stored]-thresholds[stored])
        errors[:,stored]=ndtr(-gaps/(sigma*np.abs(w[stored])))
    per_feature=probabilities @ errors
    return float(np.dot(importance,per_feature)),per_feature.tolist()


def main():
    grid = np.linspace(-np.pi/2, np.pi/2, 361)
    angles = np.unique(np.r_[grid, -np.pi/4, np.pi/4])
    cases = []
    profile_rows = []
    max_bias_formula_error = 0.
    max_loss_formula_error = 0.
    for p in [.05, .2, .5]:
        for I in [np.array([1., 1.]), np.array([1., .5])]:
            values = [profile(theta, p, I) for theta in angles]
            losses = np.array([v[0] for v in values])
            j = int(np.argmin(losses))
            antipodal_L, antipodal_biases, _ = profile(-np.pi/4, p, I)
            max_bias_formula_error = max(max_bias_formula_error,
                float(np.max(np.abs(antipodal_biases-pair_bias(p)))))
            max_loss_formula_error = max(max_loss_formula_error,
                abs(antipodal_L-I.sum()*pair_feature_loss(p)))
            pair_risk = [float(I.sum()*pair_feature_detection(p,s))
                         for s in [0,.05,.15,.3,.6]]
            case = {'p': p, 'importance': I.tolist(),
                    'angle_grid_best': float(angles[j]),
                    'angle_grid_best_loss': float(losses[j]),
                    'angle_grid_best_biases': values[j][1].tolist(),
                    'angle_grid_best_w': values[j][2].tolist(),
                    'equal_antipodal_bias': pair_bias(p),
                    'equal_antipodal_loss': float(antipodal_L),
                    'equal_antipodal_actual_threshold': .5-pair_bias(p),
                    'equal_antipodal_detection_risk': pair_risk,
                    'mono_retain_1_loss': float(I[1]*p*(1-p)),
                    'mono_retain_2_loss': float(I[0]*p*(1-p)),
                    'grid_is_not_global_proof': True}
            case['angle_grid_best_actual_detection'] = [
                actual_detection(values[j][2],values[j][1],p,I,s)
                for s in [0,.05,.15,.3,.6]]
            cases.append(case)
            for theta, (loss,bias,w) in zip(angles, values):
                profile_rows.append([p,*I,theta,loss,*bias,*w])
    # Derivative check away from kinks, entirely deterministic.
    derivative_errors = []
    for p in [.05,.2,.5]:
        prob = np.prod(np.where(STATES == 1,p,1-p),axis=1)
        for theta in [-.71,.31]:
            w = np.array([np.cos(theta),np.sin(theta)])
            G = np.outer(w,w)
            for i in range(2):
                offsets = STATES @ G[i]
                beta = .1234567
                z = offsets+beta
                analytic = 2*np.sum(prob*(np.maximum(z,0)-STATES[:,i])*(z>0))
                h=1e-6
                f=lambda b: float(np.sum(prob*(np.maximum(offsets+b,0)-STATES[:,i])**2))
                derivative_errors.append(abs(analytic-(f(beta+h)-f(beta-h))/(2*h)))
    result={'numpy': np.__version__, 'cases':cases,
            'maximum_equal_pair_bias_formula_error':max_bias_formula_error,
            'maximum_equal_pair_loss_formula_error':max_loss_formula_error,
            'maximum_bias_derivative_finite_difference_error':max(derivative_errors),
            'scope':'Finite-interval bias proof; angle-grid diagnostic only.'}
    dense_errors=[]
    for theta in angles:
        loss, bias, w=profile(theta,.5,np.array([1.,1.]))
        a=float(np.max(w*w)); c=1-a; r=np.sqrt(a*c)
        dense_errors.append(abs(loss-(c*(1+r)/6+a/4)))
    result['maximum_dense_global_profile_formula_discrepancy']=max(dense_errors)
    result['dense_equal_importance_global_geometry_proved_separately']=True
    (HERE/'verification_results.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    np.savetxt(HERE/'angular_profile.csv',np.array(profile_rows),delimiter=',',
               header='p,I1,I2,theta,loss,bias1,bias2,w1,w2',comments='')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
