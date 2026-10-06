"""Verify archived results without modifying their files.

Replays predictions from raw records and optionally reruns the fixed optimizer.
This is an arithmetic/provenance audit, not an independent proof of the research claim.
"""
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[variable] = '1'
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
from toy_math import geometry, exact_detection, interference_bound, train_population, pair_closed_risks


def read_csv(path):
    with path.open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def unpack(data, name):
    shape = tuple(data['shape'])
    return np.unpackbits(data[name], count=int(np.prod(shape))).reshape(shape).astype(bool)


def verify(run, retrain=False):
    run = Path(run).resolve()
    config = json.loads((run / 'config.json').read_text())
    manifest = json.loads((run / 'manifest.json').read_text())
    for record in manifest['files']:
        path = run / record['path']
        if path.stat().st_size != record['bytes'] or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise AssertionError(f'Artifact changed or corrupted: {record["path"]}')
    checked_predictions = 0
    checked_feature_rows = 0
    max_exact_difference = 0.0
    max_retrain_difference = 0.0
    audited_training_runs = 0
    for pi, p in enumerate(config['trained']['probabilities']):
        for seed in config['trained']['seeds']:
            folder = run / 'trained' / f'p{p:.2f}_seed{seed}'
            with np.load(folder / 'test_inputs.npz') as data:
                inputs, epsilon = data['inputs'].astype(float), data['epsilon']
                states, weights = data['population_states'].astype(float), data['population_probabilities']
            features = read_csv(folder / 'feature_metrics.csv')
            with np.load(folder / 'test_predictions.npz') as packed:
                for model in ['learned', 'mono']:
                    with np.load(folder / f'{model}_model.npz') as data:
                        W, bias, saved_G = data['W'], data['bias'], data['G']
                    if not np.allclose(W.T @ W, saved_G, rtol=0, atol=1e-12):
                        raise AssertionError('Saved Gram matrix inconsistent with weights')
                    for si, sigma in enumerate(config['trained']['sigmas']):
                        score = (inputs @ W.T + sigma * epsilon) @ W
                        for detector in ['matched', 'decoder']:
                            threshold = geometry(W, p)[-1] if detector == 'matched' else .5 - bias
                            replayed = score > threshold
                            archived = unpack(packed, f'{model}_{detector}_s{si}')
                            if not np.array_equal(replayed, archived):
                                raise AssertionError(f'Prediction mismatch: {folder.name}/{model}/{detector}/{sigma}')
                            checked_predictions += replayed.size
                            exact = exact_detection(W, states, weights, threshold, sigma)[0]
                            rows = sorted([r for r in features if r['model'] == model and r['detector'] == detector
                                           and float(r['sigma']) == sigma], key=lambda r: int(r['feature']))
                            counts = (replayed != inputs).sum(axis=0)
                            bound = interference_bound(W, p, sigma)
                            for i, row in enumerate(rows):
                                if int(row['error_count']) != counts[i]:
                                    raise AssertionError('CSV error count does not match raw predictions')
                                if abs(float(row['measured_error']) - counts[i] / len(inputs)) > 1e-12:
                                    raise AssertionError('CSV measured rate incorrect')
                                difference = abs(float(row['exact_error']) - exact[i])
                                max_exact_difference = max(max_exact_difference, difference)
                                if difference > 1e-12:
                                    raise AssertionError('Exact risk inconsistent with saved dictionary')
                                if detector == 'matched' and abs(float(row['matched_bound']) - bound[i]) > 1e-12:
                                    raise AssertionError('Saved bound incorrect')
                                checked_feature_rows += 1
                if retrain:
                    W, bias, history, _, _ = train_population(config['trained'], p, seed)
                    with np.load(folder / 'learned_model.npz') as data:
                        difference = max(float(np.max(np.abs(W - data['W']))), float(np.max(np.abs(bias - data['bias']))))
                    saved_history = np.loadtxt(folder / 'training_history.csv', delimiter=',', skiprows=1)
                    difference = max(difference, float(np.max(np.abs(history - saved_history))))
                    max_retrain_difference = max(max_retrain_difference, difference)
                    if difference > 1e-9:
                        raise AssertionError(f'Retraining mismatch: {folder.name}, difference {difference}')
                    audited_training_runs += 1

    pair_rows = read_csv(run / 'pair_totals.csv')
    for p in config['pair']['probabilities']:
        with np.load(run / 'pair' / f'p{p:.2f}_inputs.npz') as data:
            inputs, epsilon = data['inputs'].astype(float), data['epsilon']
        with np.load(run / 'pair' / f'p{p:.2f}_predictions.npz') as packed:
            for ai, a in enumerate(config['pair']['amplitudes']):
                for si, sigma in enumerate(config['pair']['sigmas']):
                    closed = pair_closed_risks(p, sigma, a)
                    for model, W, truth in [('pair', np.array([[a, -a]]), closed[0]),
                                            ('mono', np.array([[1., 0.]]), closed[1])]:
                        predicted = (inputs @ W.T + sigma * epsilon) @ W > np.diag(W.T @ W) / 2
                        if not np.array_equal(predicted, unpack(packed, f'a{ai}_{model}_s{si}')):
                            raise AssertionError('Pair raw prediction replay failed')
                        checked_predictions += predicted.size
                        row = next(r for r in pair_rows if float(r['p']) == p and float(r['sigma']) == sigma
                                   and float(r['pair_amplitude']) == a and r['model'] == model)
                        if abs(float(row['measured_total_error']) - np.sum(predicted != inputs, axis=1).mean()) > 1e-12:
                            raise AssertionError('Pair measured error incorrect')
                        if abs(float(row['closed_total_error']) - truth) > 1e-12:
                            raise AssertionError('Pair closed risk incorrect')
    return {
        'status': 'passed', 'run_directory': str(run),
        'hashed_files_checked': len(manifest['files']),
        'raw_binary_predictions_replayed': checked_predictions,
        'trained_feature_rows_checked': checked_feature_rows,
        'maximum_exact_risk_recompute_difference': max_exact_difference,
        'training_runs_repeated': audited_training_runs,
        'maximum_retraining_parameter_or_trace_difference': max_retrain_difference,
        'scope': 'integrity, arithmetic replay and optional optimizer reproduction; not novelty or real-model validation',
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory')
    parser.add_argument('--retrain', action='store_true')
    parser.add_argument('--report', help='Optional audit JSON outside the archived run directory')
    args = parser.parse_args()
    result = verify(args.run_directory, args.retrain)
    if args.report:
        report = Path(args.report).resolve()
        run = Path(args.run_directory).resolve()
        if report == run or run in report.parents:
            raise ValueError('Audit report must be outside the immutable run directory')
        report.parent.mkdir(parents=True, exist_ok=True)
        if report.exists():
            raise FileExistsError('Refusing to overwrite an existing audit report')
        report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))
