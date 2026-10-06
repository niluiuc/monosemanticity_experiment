"""Prespecified bounded training-to-geometry bridge. Run with Python from here.

All outputs written to a fresh directory. No overwriting of an existing run.
"""
import argparse
import csv
import hashlib
import json
import platform
import shutil
import sys
import time
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import minimize_scalar
from scipy.integrate import quad
from scipy.special import ndtr
from bridge_math import weighted_loss_gradient, optimal_biases, scalar_bias_optimum, train_weighted
from toy_math_snapshot import binary_population, exact_detection, exact_decoder_mse, geometry

SETTINGS = {
    'n': 2, 'm': 1, 'encoder_energy': 1., 'activation_rates': [.05, .2, .5],
    'importance_vectors': [[1., 1.], [1., .5]], 'seeds': list(range(6)),
    'steps': 4000, 'learning_rate': .01, 'adam_beta1': .9, 'adam_beta2': .999,
    'adam_epsilon': 1e-8, 'convergence_window': 100,
    'convergence_absolute_tolerance': 1e-5, 'sigmas': [0., .05, .15, .30, .60],
    'angle_grid_count': 361, 'angle_grid_lower': -np.pi/2, 'angle_grid_upper': np.pi/2,
    'extra_exact_angles': [-np.pi/4, np.pi/4],
    'objective': 'sum of importance-weighted population reconstruction MSE',
    'noise': 'Gaussian code noise h + sigma*epsilon, epsilon N(0,1)',
    'decoder_decision': 'strict reconstructed >0.5, equivalent preactivation >0.5',
    'midpoint_decision': 'strict G_i b > sum_{j!=i} G_ij*p + G_ii/2',
    'bias_tie_policy': 'retain all candidates within 1e-12 absolute-scaled loss; choose smallest finite tied candidate',
    'seed_selection': 'all prescribed final iterates; no selected checkpoint or retry',
    'scope': 'numerical grid diagnostic, not globally proved geometry optimum',
}


def write_json(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=True), encoding='utf-8')


def angle_encoder(theta):
    a = np.sqrt(.5)
    if theta == -np.pi/4:
        return np.array([[a, -a]])
    if theta == np.pi/4:
        return np.array([[a, a]])
    W = np.array([[np.cos(theta), np.sin(theta)]])
    W[abs(W) < 1e-15] = 0.
    return W


def prechecks():
    rng = np.random.default_rng(20261006)
    gradient_errors = []
    bias_errors = []
    for p in SETTINGS['activation_rates']:
        states, probabilities = binary_population(2, p)
        for importance in SETTINGS['importance_vectors']:
            for trial in range(8):
                W = rng.normal(size=(1,2))
                bias = rng.normal(size=2)
                if np.min(abs(states @ (W.T @ W) + bias)) < 1e-4:
                    raise AssertionError('Prespecified gradient check too near a kink')
                _, gW, gb = weighted_loss_gradient(W, bias, states, probabilities, importance)
                packed = np.r_[W.ravel(), bias]
                analytic = np.r_[gW.ravel(), gb]
                h = 1e-6
                numeric = []
                for i in range(4):
                    plus, minus = packed.copy(), packed.copy()
                    plus[i] += h; minus[i] -= h
                    lp = weighted_loss_gradient(plus[:2].reshape(1,2), plus[2:], states, probabilities, importance)[0]
                    lm = weighted_loss_gradient(minus[:2].reshape(1,2), minus[2:], states, probabilities, importance)[0]
                    numeric.append((lp-lm)/(2*h))
                gradient_errors.append(float(np.max(abs(analytic-numeric))))
            for theta in np.linspace(-np.pi/2, np.pi/2, 9):
                W = angle_encoder(theta)
                offsets = states @ (W.T @ W)
                for feature in range(2):
                    c, y = offsets[:,feature], states[:,feature]
                    beta, best, details = scalar_bias_optimum(c, y, probabilities)
                    objective = lambda b: float(np.sum(probabilities * (np.maximum(c+b, 0)-y)**2))
                    breaks = np.unique(-c)
                    edges = np.r_[breaks[0]-2., breaks, breaks[-1]+2.]
                    independent = [objective(b) for b in breaks]
                    for lo, hi in zip(edges[:-1], edges[1:]):
                        if hi > lo:
                            independent.append(minimize_scalar(objective, bounds=(lo,hi), method='bounded',
                                                              options={'xatol': 1e-12}).fun)
                    bias_errors.append(float(abs(best-min(independent))))
                    if objective(beta) > best+1e-12:
                        raise AssertionError('Chosen beta does not attain recorded optimum')
    # Independent normal quadrature over each half-line of the one-dimensional
    # code. This checks the source routine without calling its CDF implementation.
    states, probabilities = binary_population(2,.2)
    W = np.array([[.8,-.6]])
    threshold = np.array([.31,.23]); sigma = .30
    risk, fp, fn, state_errors = exact_detection(W,states,probabilities,threshold,sigma)
    quadrature_errors = np.zeros_like(state_errors)
    for s, state in enumerate(states):
        mean_h = float(state @ W[0])
        for i, wi in enumerate(W[0]):
            crossing = (threshold[i]/wi - mean_h)/sigma
            predicted_one_is_right_tail = wi > 0
            error_is_right_tail = predicted_one_is_right_tail != bool(state[i])
            lo, hi = (crossing,np.inf) if error_is_right_tail else (-np.inf,crossing)
            quadrature_errors[s,i] = quad(lambda z: np.exp(-z*z/2)/np.sqrt(2*np.pi),lo,hi,epsabs=1e-12)[0]
    risk_error = float(np.max(abs(quadrature_errors-state_errors)))
    max_gradient = max(gradient_errors); max_bias = max(bias_errors)
    passed = max_gradient < 1e-6 and max_bias < 1e-10 and risk_error < 1e-10
    result = {'passed': bool(passed), 'gradient_checks': len(gradient_errors),
              'max_gradient_absolute_error': max_gradient,
              'scalar_bias_checks': len(bias_errors), 'max_bias_minimum_loss_error': max_bias,
              'independent_normal_quadrature_max_state_error': risk_error,
              'gradient_check_errors': gradient_errors, 'bias_check_errors': bias_errors}
    if not passed:
        raise AssertionError(json.dumps(result))
    return result


def write_csv(path, rows):
    if rows:
        with path.open('w',newline='',encoding='utf-8') as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='run_v1')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    output = Path(args.output).resolve()
    output.mkdir(exist_ok=False,parents=True)
    sources = output/'source_snapshot'; sources.mkdir()
    for name in ['run_bridge.py','bridge_math.py','toy_math_snapshot.py','protocol_snapshot.md']:
        shutil.copy2(root/name,sources/name)
    write_json(output/'settings.json',SETTINGS)
    write_json(output/'environment.json',{'python':sys.version,'executable':sys.executable,
               'platform':platform.platform(),'numpy':np.__version__,'scipy':scipy.__version__,
               'training_preregistered_before_run': True})
    start = time.perf_counter()
    try:
        checks = prechecks()
    except Exception as exc:
        write_json(output/'prechecks_failure.json',{'error':str(exc)})
        raise
    checks['seconds'] = time.perf_counter()-start
    write_json(output/'prechecks.json',checks)
    print('Pretraining checks passed',flush=True)
    training_rows, risk_rows, geometry_rows, comparison_rows = [],[],[],[]
    landscape_rows = []
    training_seconds = 0.
    for p in SETTINGS['activation_rates']:
        states, probabilities = binary_population(2,p)
        for importance in SETTINGS['importance_vectors']:
            case = f'p_{p:.2f}_importance_{importance[1]:.2f}'
            folder = output/case; folder.mkdir()
            write_json(folder/'case_settings.json',{'p':p,'importance':importance,
                                                    'states':states.tolist(),'probabilities':probabilities.tolist()})
            # Angles are exactly the prescribed grid plus explicit exact pair candidates.
            angles = np.r_[np.linspace(-np.pi/2,np.pi/2,361), -np.pi/4,np.pi/4]
            losses, biases, encoder_grid, bias_details = [],[],[],[]
            for j, theta in enumerate(angles):
                W = angle_encoder(theta)
                bias, loss, details = optimal_biases(W,states,probabilities,importance)
                losses.append(loss); biases.append(bias); encoder_grid.append(W)
                bias_details.append(details)
                landscape_rows.append({'case':case,'p':p,'importance_0':importance[0],
                                       'importance_1':importance[1],'candidate_index':j,
                                       'theta':float(theta),'weight_0':float(W[0,0]),
                                       'weight_1':float(W[0,1]),'bias_0':float(bias[0]),
                                       'bias_1':float(bias[1]),'weighted_loss':loss,
                                       'explicit_extra_candidate':j>=361})
            losses = np.asarray(losses)
            grid_min = float(losses.min())
            grid_tied = np.flatnonzero(abs(losses-grid_min)<=1e-12)
            index = int(grid_tied[0])
            np.savez_compressed(folder/'landscape.npz',angles=angles,losses=losses,
                                W=np.stack(encoder_grid),bias=np.stack(biases),
                                tied_best_indices=grid_tied)
            write_json(folder/'landscape_bias_candidates.json',bias_details)
            models = [('grid_diagnostic_best',None,encoder_grid[index],biases[index])]
            for label, W in [('fixed_antipodal',np.array([[np.sqrt(.5),-np.sqrt(.5)]])),
                             ('mono_retain_0',np.array([[1.,0.]])),
                             ('mono_retain_1',np.array([[0.,1.]]))]:
                beta, loss, details = optimal_biases(W,states,probabilities,importance)
                models.append((label,None,W,beta))
                write_json(folder/f'{label}_bias_candidates.json',details)
            mono_losses = [weighted_loss_gradient(W,b,states,probabilities,importance)[0]
                           for label,seed,W,b in models if label.startswith('mono')]
            preferred_mono = int(np.argmin(mono_losses))
            for seed in SETTINGS['seeds']:
                before=time.perf_counter()
                W,bias,history,checkpoints,diagnostics = train_weighted(SETTINGS,p,importance,seed)
                seconds=time.perf_counter()-before; training_seconds += seconds
                optimal_beta, best_bias_loss, details = optimal_biases(W,states,probabilities,importance)
                diagnostics.update({'seconds':seconds,'bias_optimal_loss':best_bias_loss,
                                    'bias_optimization_gap':diagnostics['final_loss']-best_bias_loss,
                                    'loss_minus_grid_diagnostic_best':diagnostics['final_loss']-grid_min,
                                    'bias_reoptimized_minus_grid_best':best_bias_loss-grid_min})
                checkpoint_arrays = {'checkpoint_'+name: value for name,value in checkpoints.items()}
                np.savez_compressed(folder/f'seed_{seed}.npz',W=W,bias=bias,history=history,
                                    bias_reoptimized=optimal_beta, **checkpoint_arrays)
                write_json(folder/f'seed_{seed}_diagnostics.json',diagnostics)
                write_json(folder/f'seed_{seed}_bias_candidates.json',details)
                training_rows.append({'case':case,'p':p,'importance_0':importance[0],
                                     'importance_1':importance[1],'seed':seed,**diagnostics})
                models.append(('trained_final',seed,W,bias))
                models.append(('trained_bias_reoptimized',seed,W,optimal_beta))
            comparison_rows.append({'case':case,'grid_minimum_loss':grid_min,
                                    'grid_tied_indices':json.dumps(grid_tied.tolist()),
                                    'mono_0_loss':mono_losses[0],'mono_1_loss':mono_losses[1],
                                    'clean_preferred_mono_retains':preferred_mono,
                                    'clean_mono_tied':abs(mono_losses[0]-mono_losses[1])<=1e-12})
            saved_models=[]
            for label,seed,W,bias in models:
                G,d,V,B,M,midpoint = geometry(W,p)
                actual_threshold = .5-bias
                clean_loss,gW,gb = weighted_loss_gradient(W,bias,states,probabilities,importance)
                tangent=gW-np.sum(gW*W)*W
                theta=float(np.arctan2(W[0,1],W[0,0]))
                saved_models.append({'label':label,'seed':seed,'W':W.tolist(),'bias':bias.tolist(),
                                     'actual_threshold':actual_threshold.tolist(),'midpoint':midpoint.tolist()})
                geometry_rows.append({'case':case,'label':label,'seed':seed,'theta_raw':theta,
                                      'W_0':float(W[0,0]),'W_1':float(W[0,1]),
                                      'bias_0':float(bias[0]),'bias_1':float(bias[1]),
                                      'energy':float(np.sum(W**2)),'G_00':float(d[0]),
                                      'G_11':float(d[1]),'G_01':float(G[0,1]),
                                      'M_0':float(M[0]),'M_1':float(M[1]),
                                      'clean_weighted_mse':clean_loss,
                                      'tangent_gradient_norm':float(np.linalg.norm(tangent)),
                                      'bias_gradient_norm':float(np.linalg.norm(gb)),
                                      'actual_min_abs_state_gap':float(np.min(abs(states@G.T-actual_threshold))),
                                      'midpoint_min_abs_state_gap':float(np.min(abs(states@G.T-midpoint)))})
                for sigma in SETTINGS['sigmas']:
                    per_mse=exact_decoder_mse(W,bias,states,probabilities,sigma)
                    for detector, threshold in [('actual_decoder',actual_threshold),('centered_midpoint',midpoint)]:
                        risk,fp,fn,error = exact_detection(W,states,probabilities,threshold,sigma)
                        row={'case':case,'p':p,'importance_0':importance[0],'importance_1':importance[1],
                             'label':label,'seed':seed,'sigma':sigma,'detector':detector,
                             'weighted_sum_error':float(np.asarray(importance)@risk),
                             'unweighted_sum_error':float(risk.sum()),
                             'weighted_sum_decoder_mse':float(np.asarray(importance)@per_mse),
                             'unweighted_sum_decoder_mse':float(per_mse.sum())}
                        for i in range(2):
                            row.update({f'error_{i}':float(risk[i]),f'fp_{i}':float(fp[i]),
                                        f'fn_{i}':float(fn[i]),f'decoder_mse_{i}':float(per_mse[i])})
                        risk_rows.append(row)
            write_json(folder/'evaluated_models.json',saved_models)
            print(case,'completed, grid diagnostic loss',grid_min,flush=True)
    write_csv(output/'training_summary.csv',training_rows)
    write_csv(output/'geometry.csv',geometry_rows)
    write_csv(output/'risks.csv',risk_rows)
    write_csv(output/'landscape.csv',landscape_rows)
    write_csv(output/'comparisons.csv',comparison_rows)
    write_json(output/'timings.json',{'total_seconds':time.perf_counter()-start,
                                    'training_seconds':training_seconds})
    # Hashes include source and all raw results, not themselves.
    manifest = {str(path.relative_to(output)):hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(output.rglob('*')) if path.is_file()}
    write_json(output/'sha256_manifest.json',manifest)
    print('Completed all prespecified cases:',output,flush=True)


if __name__=='__main__':
    main()
