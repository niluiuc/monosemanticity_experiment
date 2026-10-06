"""Run the fixed Project 1 protocol and retain every result in a new folder.

Usage: python run_experiments.py [--output runs/my_independent_run]
Paths for --output are relative to this script's directory, unless absolute.
"""
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'
os.environ['MPLBACKEND'] = 'Agg'

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
import logging
from pathlib import Path
import platform
import shutil
import sys
import time
import traceback
import contextlib
import numpy as np
import scipy
import matplotlib
from scipy.optimize import brentq
from toy_math import (binary_population, geometry, exact_detection,
                      interference_bound, exact_decoder_mse, pair_closed_risks,
                      wilson_interval, train_population, mono_baseline)
from checks import run_checks

ROOT = Path(__file__).resolve().parent


def write_json(path, content):
    path.write_text(json.dumps(content, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def write_csv(path, records):
    if not records:
        return
    with path.open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def pack_predictions(path, predictions):
    names = list(predictions)
    shape = predictions[names[0]].shape
    np.savez_compressed(path, shape=np.array(shape), names=np.array(names),
                        **{name: np.packbits(value, axis=None) for name, value in predictions.items()})


def feature_measurements(W, bias, states, weights, inputs, epsilon, sigmas,
                         model, metadata, alpha, comparison_cap):
    G, d, V, B, alignment, midpoint = geometry(W, metadata['p'])
    records, totals, predictions = [], [], {}
    sample_n = len(inputs)
    hoeffding = np.sqrt(np.log(2 * comparison_cap / alpha) / (2 * sample_n))
    for si, sigma in enumerate(sigmas):
        hidden = inputs @ W.T + sigma * epsilon
        scores = hidden @ W
        decoded = np.maximum(scores + bias, 0)
        exact_mse = exact_decoder_mse(W, bias, states, weights, sigma)
        measured_mse = np.mean((decoded - inputs)**2, axis=0)
        bound = interference_bound(W, metadata['p'], sigma)
        for detector, threshold in [('matched', midpoint), ('decoder', .5 - bias)]:
            exact, exact_fp, exact_fn, _ = exact_detection(W, states, weights, threshold, sigma)
            predicted = scores > threshold
            predictions[f'{model}_{detector}_s{si}'] = predicted
            wrong = predicted != inputs
            count = wrong.sum(axis=0)
            measured = count / sample_n
            low, high = wilson_interval(count, sample_n)
            total_per_sample = wrong.sum(axis=1)
            total_se = np.std(total_per_sample, ddof=1) / np.sqrt(sample_n)
            for i in range(W.shape[1]):
                active = inputs[:, i] == 1
                count1, count0 = int(active.sum()), int((~active).sum())
                standard_error = np.sqrt(exact[i] * (1 - exact[i]) / sample_n)
                residual = float(measured[i] - exact[i])
                z_score = residual / standard_error if standard_error > 0 else None
                records.append({
                    **metadata, 'model': model, 'detector': detector, 'sigma': sigma,
                    'feature': i, 'test_samples': sample_n, 'active_samples': count1,
                    'inactive_samples': count0, 'error_count': int(count[i]),
                    'exact_error': float(exact[i]), 'measured_error': float(measured[i]),
                    'mc_minus_exact': residual, 'wilson95_low': float(low[i]),
                    'wilson95_high': float(high[i]), 'mc_standardized_residual': z_score,
                    'familywise_hoeffding_tolerance': float(hoeffding),
                    'within_familywise_tolerance': bool(abs(residual) <= hoeffding),
                    'exact_false_positive_rate': float(exact_fp[i]),
                    'measured_false_positive_rate': float(wrong[~active, i].mean()) if count0 else None,
                    'exact_false_negative_rate': float(exact_fn[i]),
                    'measured_false_negative_rate': float(wrong[active, i].mean()) if count1 else None,
                    'gram_diagonal': float(d[i]), 'interference_variance': float(V[i]),
                    'largest_overlap': float(B[i]),
                    'alignment_M': float(alignment[i]) if np.isfinite(alignment[i]) else None,
                    'threshold': float(threshold[i]), 'decoder_bias': float(bias[i]),
                    'matched_bound': float(bound[i]) if detector == 'matched' else None,
                    'exact_reconstruction_mse': float(exact_mse[i]),
                    'measured_reconstruction_mse': float(measured_mse[i]),
                })
            totals.append({
                **metadata, 'model': model, 'detector': detector, 'sigma': sigma,
                'exact_total_error': float(exact.sum()),
                'measured_total_error': float(measured.sum()),
                'measured_total_error_standard_error': float(total_se),
                'exact_mean_feature_error': float(exact.mean()),
                'exact_total_reconstruction_mse': float(exact_mse.sum()),
                'measured_total_reconstruction_mse': float(measured_mse.sum()),
                'matched_total_bound': float(bound.sum()) if detector == 'matched' else None,
            })
    return records, totals, predictions


def run_pairs(config, out):
    settings = config['pair']
    directory = out / 'pair'
    directory.mkdir()
    totals, features = [], []
    for pi, p in enumerate(settings['probabilities']):
        seed = settings['seed_base'] + pi
        rng = np.random.default_rng(seed)
        inputs = (rng.random((settings['samples'], 2)) < p).astype(float)
        noise = rng.normal(size=(settings['samples'], 1))
        np.savez_compressed(directory / f'p{p:.2f}_inputs.npz',
                            inputs=inputs.astype(np.uint8), epsilon=noise, seed=seed)
        states, weights = binary_population(2, p)
        predictions = {}
        for ai, a in enumerate(settings['amplitudes']):
            code_pair = np.array([[a, -a]])
            mono = np.array([[1., 0.]])
            for si, sigma in enumerate(settings['sigmas']):
                closed_pair, closed_mono = pair_closed_risks(p, sigma, a)
                for model, W, closed in [('pair', code_pair, closed_pair), ('mono', mono, closed_mono)]:
                    threshold = np.diag(W.T @ W) / 2
                    exact = exact_detection(W, states, weights, threshold, sigma)[0]
                    scores = (inputs @ W.T + sigma * noise) @ W
                    predicted = scores > threshold
                    key = f'a{ai}_{model}_s{si}'
                    predictions[key] = predicted
                    wrong = predicted != inputs
                    per_sample = wrong.sum(axis=1)
                    measured = wrong.mean(axis=0)
                    tol = np.sqrt(np.log(2 * config['checks']['comparison_cap'] /
                                         config['checks']['familywise_alpha']) / (2 * len(inputs)))
                    totals.append({
                        'p': p, 'sigma': sigma, 'pair_amplitude': a, 'model': model,
                        'encoder_energy': float(np.sum(W**2)), 'test_seed': seed,
                        'test_samples': len(inputs), 'closed_total_error': float(closed),
                        'enumerated_total_error': float(exact.sum()),
                        'measured_total_error': float(per_sample.mean()),
                        'measured_total_error_standard_error': float(per_sample.std(ddof=1) / np.sqrt(len(inputs))),
                    })
                    for i in range(2):
                        features.append({
                            'p': p, 'sigma': sigma, 'pair_amplitude': a, 'model': model,
                            'feature': i, 'exact_error': float(exact[i]),
                            'measured_error': float(measured[i]),
                            'absolute_mc_minus_exact': float(abs(measured[i] - exact[i])),
                            'familywise_hoeffding_tolerance': float(tol),
                            'within_familywise_tolerance': bool(abs(measured[i] - exact[i]) <= tol),
                        })
        pack_predictions(directory / f'p{p:.2f}_predictions.npz', predictions)
    crossings = []
    for a in settings['amplitudes']:
        root = brentq(lambda sigma: np.subtract(*pair_closed_risks(.2, sigma, a)), .05, 1.5)
        crossings.append({'p': .2, 'pair_amplitude': a, 'crossing_sigma': float(root),
                          'method': 'root of exact risks, not a fitted boundary'})
    write_csv(out / 'pair_totals.csv', totals)
    write_csv(out / 'pair_features.csv', features)
    write_json(out / 'pair_crossings.json', crossings)
    return totals, features, crossings


def run_trained(config, out):
    settings = config['trained']
    directory = out / 'trained'
    directory.mkdir()
    all_features, all_totals, comparisons, training = [], [], [], []
    for pi, p in enumerate(settings['probabilities']):
        for seed in settings['seeds']:
            tag = f'p{p:.2f}_seed{seed}'
            run = directory / tag
            run.mkdir()
            logging.info('Training %s: %d fixed steps', tag, settings['steps'])
            W, bias, history, checkpoints, diagnostics = train_population(settings, p, seed)
            if abs(np.sum(W**2) - settings['encoder_energy']) > 1e-10:
                raise AssertionError('Encoder energy constraint violated')
            np.savez_compressed(run / 'training_checkpoints.npz', **checkpoints)
            np.savetxt(run / 'training_history.csv', history, delimiter=',', comments='',
                       header='step,population_reconstruction_mse,encoder_energy,tangent_gradient_norm,bias_gradient_norm')
            mono_W, mono_bias = mono_baseline(settings['n'], settings['m'], p, settings['encoder_energy'])
            states, weights = binary_population(settings['n'], p)
            test_seed = settings['test_seed_base'] + 1000 * pi + seed
            rng = np.random.default_rng(test_seed)
            inputs = (rng.random((settings['samples'], settings['n'])) < p).astype(float)
            epsilon = rng.normal(size=(settings['samples'], settings['m']))
            np.savez_compressed(run / 'test_inputs.npz', inputs=inputs.astype(np.uint8),
                                epsilon=epsilon, test_seed=test_seed,
                                population_states=states.astype(np.uint8), population_probabilities=weights)
            metadata = {'p': p, 'initialization_seed': seed, 'test_seed': test_seed}
            predictions, run_features, run_totals = {}, [], []
            for model, model_W, model_bias in [('learned', W, bias), ('mono', mono_W, mono_bias)]:
                G, d, V, B, alignment, midpoint = geometry(model_W, p)
                np.savez_compressed(run / f'{model}_model.npz', W=model_W, bias=model_bias, G=G,
                                    gram_diagonal=d, interference_variance=V, largest_overlap=B,
                                    alignment_M=alignment, matched_threshold=midpoint)
                features, totals, predicted = feature_measurements(
                    model_W, model_bias, states, weights, inputs, epsilon, settings['sigmas'],
                    model, metadata, config['checks']['familywise_alpha'], config['checks']['comparison_cap'])
                run_features.extend(features)
                run_totals.extend(totals)
                predictions.update(predicted)
            pack_predictions(run / 'test_predictions.npz', predictions)
            write_csv(run / 'feature_metrics.csv', run_features)
            write_csv(run / 'total_metrics.csv', run_totals)
            for si, sigma in enumerate(settings['sigmas']):
                for detector in ['matched', 'decoder']:
                    learned_errors = (predictions[f'learned_{detector}_s{si}'] != inputs).sum(axis=1)
                    mono_errors = (predictions[f'mono_{detector}_s{si}'] != inputs).sum(axis=1)
                    difference = learned_errors.astype(float) - mono_errors.astype(float)
                    selected = [r for r in run_totals if r['sigma'] == sigma and r['detector'] == detector]
                    exacts = {r['model']: r['exact_total_error'] for r in selected}
                    se = difference.std(ddof=1) / np.sqrt(len(difference))
                    comparisons.append({
                        **metadata, 'sigma': sigma, 'detector': detector,
                        'exact_learned_minus_mono': exacts['learned'] - exacts['mono'],
                        'measured_learned_minus_mono': float(difference.mean()),
                        'paired_standard_error': float(se),
                        'paired_normal95_low': float(difference.mean() - 1.959963984540054 * se),
                        'paired_normal95_high': float(difference.mean() + 1.959963984540054 * se),
                    })
            d = np.diag(W.T @ W)
            training_record = {**metadata, **diagnostics,
                               'encoder_energy': float(np.sum(W**2)),
                               'weak_columns': int(np.sum(d < settings['weak_column_relative_cutoff'] * settings['encoder_energy'] / settings['n'])),
                               'exact_zero_columns': int(np.sum(d == 0)),
                               'mono_clean_reconstruction_mse': float((settings['n'] - settings['m']) * p * (1 - p))}
            write_json(run / 'training_summary.json', training_record)
            training.append(training_record)
            all_features.extend(run_features)
            all_totals.extend(run_totals)
            logging.info('%s: final reconstruction %.6f; mono %.6f; convergence diagnostic %s',
                         tag, diagnostics['final_loss'], training_record['mono_clean_reconstruction_mse'],
                         diagnostics['convergence_diagnostic_pass'])
    write_csv(out / 'trained_feature_metrics.csv', all_features)
    write_csv(out / 'trained_total_metrics.csv', all_totals)
    write_csv(out / 'paired_comparisons.csv', comparisons)
    write_csv(out / 'training_summary.csv', training)
    return all_features, all_totals, comparisons, training


def summary_statistics(config, pair_features, crossings, features, totals, comparisons, training):
    matched = [r for r in features if r['detector'] == 'matched']
    bound_violations = [r for r in matched if r['exact_error'] > r['matched_bound'] + config['checks']['bound_tolerance']]
    simultaneous_failures = [r for r in features if not r['within_familywise_tolerance']]
    pair_failures = [r for r in pair_features if not r['within_familywise_tolerance']]
    groups = []
    for p in config['trained']['probabilities']:
        for detector in ['matched', 'decoder']:
            for sigma in config['trained']['sigmas']:
                values = [r['exact_learned_minus_mono'] for r in comparisons
                          if r['p'] == p and r['detector'] == detector and r['sigma'] == sigma]
                groups.append({'p': p, 'detector': detector, 'sigma': sigma,
                               'mean_exact_learned_minus_mono': float(np.mean(values)),
                               'min_exact_learned_minus_mono': float(np.min(values)),
                               'max_exact_learned_minus_mono': float(np.max(values)),
                               'seeds_learned_better': int(np.sum(np.array(values) < 0)),
                               'seed_count': len(values)})
    slack = np.array([r['matched_bound'] - r['exact_error'] for r in matched if r['model'] == 'learned'])
    return {
        'trained_settings': len(training), 'pair_feature_comparisons': len(pair_features),
        'trained_feature_comparisons': len(features),
        'max_trained_absolute_mc_minus_exact': max(abs(r['mc_minus_exact']) for r in features),
        'max_pair_absolute_mc_minus_exact': max(r['absolute_mc_minus_exact'] for r in pair_features),
        'trained_familywise_tolerance_failures': len(simultaneous_failures),
        'pair_familywise_tolerance_failures': len(pair_failures),
        'matched_bound_violations': len(bound_violations),
        'learned_bound_slack_min': float(slack.min()),
        'learned_bound_slack_median': float(np.median(slack)),
        'learned_bound_slack_max': float(slack.max()),
        'convergence_diagnostic_failures': [
            {'p': r['p'], 'seed': r['initialization_seed'], 'change': r['window_mean_loss_change']}
            for r in training if not r['convergence_diagnostic_pass']],
        'training': training, 'pair_crossings': crossings, 'risk_comparison_groups': groups,
    }


def manifest(out):
    entries = []
    for path in sorted(out.rglob('*')):
        if path.is_file() and path.name != 'manifest.json':
            entries.append({'path': path.relative_to(out).as_posix(), 'bytes': path.stat().st_size,
                            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    write_json(out / 'manifest.json', {'hash_algorithm': 'SHA-256', 'files': entries})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', help='New output directory; existing directories are refused')
    args = parser.parse_args()
    config = json.loads((ROOT / 'config.json').read_text())
    start = datetime.now(timezone.utc)
    relative = args.output or 'runs/' + start.strftime('run_%Y%m%dT%H%M%SZ')
    out = Path(relative)
    if not out.is_absolute():
        out = ROOT / out
    out.mkdir(parents=True, exist_ok=False)
    source = out / 'source'
    source.mkdir()
    for name in ['run_experiments.py', 'toy_math.py', 'checks.py', 'plot_results.py',
                 'verify_results.py', 'config.json', 'requirements.txt', 'README.md']:
        shutil.copy2(ROOT / name, source / name)
    shutil.copy2(ROOT / 'plan.md', out / 'plan_before_run.md')
    write_json(out / 'config.json', config)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[logging.FileHandler(out / 'run.log', encoding='utf-8'), logging.StreamHandler()])
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        np.show_config()
    write_json(out / 'environment.json', {
        'python': sys.version, 'python_executable': sys.executable, 'platform': platform.platform(),
        'numpy': np.__version__, 'scipy': scipy.__version__, 'matplotlib': matplotlib.__version__,
        'blas_configuration': buffer.getvalue(),
        'thread_settings': {key: os.environ[key] for key in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS')},
        'start_utc': start.isoformat(), 'command': sys.argv,
    })
    timer = time.perf_counter()
    status = {'status': 'running', 'start_utc': start.isoformat()}
    try:
        logging.info('Output directory: %s', out)
        checks = run_checks(config)
        write_json(out / 'checks.json', checks)
        logging.info('Pre-run mathematical checks passed')
        _, pair_features, crossings = run_pairs(config, out)
        logging.info('Solved-pair simulations complete')
        features, totals, comparisons, training = run_trained(config, out)
        summary = summary_statistics(config, pair_features, crossings, features, totals, comparisons, training)
        write_json(out / 'summary.json', summary)
        from plot_results import make_plots, write_report
        make_plots(out)
        write_report(out)
        status['status'] = 'completed'
        if (summary['matched_bound_violations'] or summary['trained_familywise_tolerance_failures']
                or summary['pair_familywise_tolerance_failures']):
            status['status'] = 'completed_with_check_failures'
        logging.info('Finished all prespecified settings. Status: %s', status['status'])
    except Exception:
        status['status'] = 'failed'
        status['exception'] = traceback.format_exc()
        logging.exception('Run failed; retained existing output for diagnosis')
        raise
    finally:
        status['end_utc'] = datetime.now(timezone.utc).isoformat()
        status['elapsed_seconds'] = time.perf_counter() - timer
        write_json(out / 'run_status.json', status)
        # Flush and close file handlers before hashing the unmodified log.
        logging.shutdown()
        manifest(out)
        print(f'Saved run: {out}')


if __name__ == '__main__':
    main()
