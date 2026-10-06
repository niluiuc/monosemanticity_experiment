"""Independent teacher audit of the fixed six-case toy run, without rewriting it.

Questions: do saved risks implement the protocol, do supplied biases attain the
fixed-geometry optimum, and do training artifacts reproduce? This is verification
of existing cases, not a parameter search or an added training experiment.
Biases are checked through all 16 active masks, independently of the student's
interval implementation. Gaussian probabilities use latent scalar thresholds.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
import sys
import time
import numpy as np
from scipy.special import ndtr
from scipy.integrate import quad


def scalar_bias_mask_minimum(c, y, weights):
    candidates = []
    for bits in itertools.product([False, True], repeat=4):
        active = np.asarray(bits)
        low = max(-c[active], default=-np.inf)
        high = min(-c[~active], default=np.inf)
        if low > high:
            continue
        A = weights[active].sum()
        if A == 0:
            beta = high
        else:
            vertex = np.sum(weights[active] * (y[active] - c[active])) / A
            beta = max(low, min(high, vertex))
        loss = np.sum(weights * (np.maximum(c + beta, 0) - y)**2)
        candidates.append((float(loss), float(beta)))
    return min(candidates)[0]


def latent_risk(W, bias, states, probability, sigma, detector):
    w = W.ravel()
    gram = np.outer(w, w)
    p = probability @ states
    threshold = (0.5 - bias if detector == 'actual_decoder' else
                 (gram - np.diag(np.diag(gram))) @ p + np.diag(gram)/2)
    code = states @ w
    errors = np.empty_like(states)
    for i, wi in enumerate(w):
        if sigma == 0 or wi == 0:
            predicts = code * wi > threshold[i]
            errors[:, i] = predicts != states[:, i]
        else:
            z = (code - threshold[i] / wi) / sigma
            one_prob = ndtr(z if wi > 0 else -z)
            errors[:, i] = np.where(states[:, i] == 1, 1 - one_prob, one_prob)
    risk = probability @ errors
    fp = np.sum(probability[:, None] * errors * (1-states), axis=0)/(1-p)
    fn = np.sum(probability[:, None] * errors * states, axis=0)/p
    return risk, fp, fn


def quadrature_mse(W, bias, states, probability, sigma):
    result = np.zeros(2)
    w = W.ravel()
    for s, row in enumerate(states):
        mu_h = row @ w
        for i, wi in enumerate(w):
            if sigma == 0 or wi == 0:
                integral = (max(wi*mu_h + bias[i], 0)-row[i])**2
            else:
                cut = -(wi*mu_h+bias[i])/(wi*sigma)
                def integrand(z):
                    pred = max(wi*(mu_h+sigma*z)+bias[i], 0)
                    return (pred-row[i])**2*np.exp(-z*z/2)/np.sqrt(2*np.pi)
                integral = (quad(integrand,-np.inf,cut,epsabs=1e-11)[0] +
                            quad(integrand,cut,np.inf,epsabs=1e-11)[0])
            result[i] += probability[s]*integral
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run',type=Path,default=Path(__file__).resolve().parents[1]/'toy/run_v1')
    ap.add_argument('--report',type=Path,default=Path(__file__).resolve().parent/'toy_verification.json')
    ap.add_argument('--retrain',action='store_true')
    args = ap.parse_args()
    start = time.perf_counter()
    run = args.run.resolve()
    failures = []
    manifest = json.loads((run/'sha256_manifest.json').read_text(encoding='utf-8'))
    for name, expected in manifest.items():
        actual = hashlib.sha256((run/name).read_bytes()).hexdigest()
        if actual != expected: failures.append('Hash mismatch: '+name)
    settings = json.loads((run/'settings.json').read_text(encoding='utf-8'))
    with (run/'risks.csv').open(newline='',encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    with (run/'training_summary.csv').open(newline='',encoding='utf-8') as f:
        training = list(csv.DictReader(f))
    with (run/'geometry.csv').open(newline='',encoding='utf-8') as f:
        geometries = list(csv.DictReader(f))
    if len(training) != 36: failures.append('Expected 36 trainings')
    if len(rows) != 960: failures.append('Expected 960 detector/model/sigma rows')
    lookup = {(r['case'],r['label'],r['seed'],float(r['sigma']),r['detector']):r for r in rows}
    max_risk = max_bias_loss = max_quadrature = max_clean_loss = max_energy = 0.
    zero_disagreements = []
    direct_decoder_disagreements = []
    case_count = model_count = 0
    for folder in sorted(run.glob('p_*')):
        case_count += 1
        case = folder.name
        config = json.loads((folder/'case_settings.json').read_text(encoding='utf-8'))
        states = np.asarray(config['states']); probability = np.asarray(config['probabilities'])
        importance = np.asarray(config['importance'])
        models = json.loads((folder/'evaluated_models.json').read_text(encoding='utf-8'))
        for model in models:
            model_count += 1
            W = np.asarray(model['W']); bias = np.asarray(model['bias'])
            seed = '' if model['seed'] is None else str(model['seed'])
            clean = importance @ (probability @ (np.maximum(states @ W.T @ W+bias,0)-states)**2)
            record = next(r for r in geometries if (r['case'],r['label'],r['seed']) == (case,model['label'],seed))
            max_clean_loss = max(max_clean_loss,abs(clean-float(record['clean_weighted_mse'])))
            max_energy = max(max_energy,abs(np.sum(W**2)-1))
            if model['label'] != 'trained_final':
                offsets = states @ W.T @ W
                minimum = sum(importance[i]*scalar_bias_mask_minimum(offsets[:,i],states[:,i],probability) for i in range(2))
                max_bias_loss = max(max_bias_loss,abs(clean-minimum))
            for sigma in settings['sigmas']:
                for detector in ['actual_decoder','centered_midpoint']:
                    row = lookup[(case,model['label'],seed,sigma,detector)]
                    risk,fp,fn = latent_risk(W,bias,states,probability,sigma,detector)
                    if sigma == 0 and detector == 'actual_decoder':
                        direct_prediction = np.maximum(states @ W.T @ W + bias,0)>0.5
                        direct_error = probability @ (direct_prediction != states)
                        saved_error = np.asarray([float(row[f'error_{i}']) for i in range(2)])
                        direct_difference = float(np.max(abs(direct_error-saved_error)))
                        if direct_difference > 1e-10:
                            direct_decoder_disagreements.append({'case':case,'model':model['label'],
                                'seed':seed,'max_feature_error_difference':direct_difference,
                                'saved_weighted_error':float(row['weighted_sum_error']),
                                'direct_float64_weighted_error':float(importance @ direct_error)})
                    errors = [abs(risk[i]-float(row[f'error_{i}'])) for i in range(2)]
                    errors += [abs(fp[i]-float(row[f'fp_{i}'])) for i in range(2)]
                    errors += [abs(fn[i]-float(row[f'fn_{i}'])) for i in range(2)]
                    errors += [abs(importance @ risk-float(row['weighted_sum_error']))]
                    difference = max(errors)
                    if sigma == 0 and difference > 1e-10:
                        zero_disagreements.append({'case':case,'model':model['label'],'seed':seed,'detector':detector,'max_difference':float(difference)})
                    elif sigma > 0:
                        max_risk = max(max_risk,difference)
            if model['label'] == 'fixed_antipodal':
                mse = quadrature_mse(W,bias,states,probability,.3)
                row = lookup[(case,model['label'],seed,.3,'actual_decoder')]
                max_quadrature = max(max_quadrature,max(abs(mse[i]-float(row[f'decoder_mse_{i}'])) for i in range(2)))
    if max_risk > 1e-10: failures.append('Positive-noise risk mismatch')
    if max_bias_loss > 1e-10: failures.append('Bias optimum mismatch')
    if max_clean_loss > 1e-10: failures.append('Clean objective mismatch')
    if max_energy > 1e-12: failures.append('Encoder energy mismatch')
    if max_quadrature > 1e-9: failures.append('Independent MSE quadrature mismatch')
    replay_max = None
    if args.retrain:
        source = run/'source_snapshot'
        sys.path.insert(0,str(source))
        spec = importlib.util.spec_from_file_location('audit_bridge_math',source/'bridge_math.py')
        module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        replay_max = 0.
        for row in training:
            W,bias,trace,checkpoints,diagnostic = module.train_weighted(settings,float(row['p']),[float(row['importance_0']),float(row['importance_1'])],int(row['seed']))
            with np.load(run/row['case']/f"seed_{row['seed']}.npz") as saved:
                for name, value in [('W',W),('bias',bias),('history',trace)]:
                    replay_max = max(replay_max,float(np.max(abs(value-saved[name]))))
        if replay_max > 1e-12: failures.append('Training replay mismatch')
    result = {'hashes_checked':len(manifest),'cases':case_count,'models':model_count,
              'training_records':len(training),'risk_records':len(rows),
              'max_positive_noise_risk_discrepancy':max_risk,
              'max_fixed_geometry_bias_loss_discrepancy':max_bias_loss,
              'max_clean_loss_discrepancy':max_clean_loss,'max_energy_discrepancy':max_energy,
              'max_independent_decoder_mse_quadrature_discrepancy':max_quadrature,
              'zero_noise_arithmetic_disagreements':zero_disagreements,
              'direct_float64_decoder_zero_noise_disagreements':direct_decoder_disagreements,
              'training_replay_max_difference':replay_max,
              'loss_stability_failures':sum(r['convergence_diagnostic_pass']!='True' for r in training),
              'numerical_training_failures':sum(bool(r['failure']) for r in training),
              'errors':failures,'seconds':time.perf_counter()-start,
              'interpretation':'Zero-noise disagreements are reported, not repaired by changing raw predictions. This audit does not prove global geometry optimality.'}
    args.report.parent.mkdir(parents=True,exist_ok=True)
    args.report.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    if failures: raise SystemExit(1)


if __name__ == '__main__':
    main()
