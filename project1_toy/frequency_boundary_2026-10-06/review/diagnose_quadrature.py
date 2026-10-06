"""Locate the failed independent MSE check using only saved primary cases."""
from pathlib import Path
import csv
import json
import sys
import numpy as np

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE.parent/'focused_bridge_2026-10-06'/'review'))
from verify_toy import quadrature_mse

states = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
with (BASE/'toy'/'run_v1'/'primary_risks.csv').open(newline='') as f:
    rows = list(csv.DictReader(f))
findings = []
for row in rows:
    if row['detector'] != 'actual_decoder':
        continue
    p = float(row['p']); sigma = float(row['sigma'])
    models = json.loads((BASE/'toy'/'run_v1'/f'p_{p:.3f}'/'selected_models.json').read_text())
    model = next(m for m in models if m['label'] == row['label'])
    w = np.array(model['W']); bias = np.array(model['bias'])
    prob = np.prod(np.where(states == 1, p, 1-p), axis=1)
    check = quadrature_mse(w, bias, states, prob, sigma)
    raw = np.array([float(row[f'mse_{i}']) for i in range(2)])
    diff = np.max(abs(check-raw))
    if diff > 1e-9:
        cuts = [] if sigma == 0 else [((-(states@w.ravel())-bias[i]/w[0, i])/sigma).tolist()
                                     for i in range(2) if w[0, i] != 0]
        findings.append({'p': p, 'label': row['label'], 'sigma': sigma,
                         'saved_mse': raw.tolist(), 'checker_mse': check.tolist(),
                         'maximum_difference': float(diff), 'relu_cut_standard_normals': cuts})
result = {'initial_review': 'Global selection, bias, risk and curve assertions passed; aggregate MSE/energy/root assertion failed. The saved raw run is not modified.',
          'failing_mse_comparisons': findings,
          'hypothesis': 'Unbounded quadrature split at very distant ReLU cuts can miss central Gaussian mass. Must verify with an independent bounded-body integral.'}
(BASE/'review'/'verification_initial_failure.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
