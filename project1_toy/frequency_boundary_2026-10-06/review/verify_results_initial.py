"""Independent checks of the fixed frequency experiment; no new scientific cases.

Different nonempty-active-subset certificate construction and scalar-latent
risk calculation. Exact root-isolation helpers share the reviewed backend.
"""
import csv
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import sys
import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
RUN = HERE / 'toy' / 'run_v1'
OLDER = HERE.parent / 'focused_bridge_2026-10-06'
sys.path.insert(0, str(OLDER / 'review'))
from verify_toy import scalar_bias_mask_minimum, latent_risk, quadrature_mse

spec = importlib.util.spec_from_file_location('exact_backend', OLDER / 'math' / 'certify_low_p.py')
backend = importlib.util.module_from_spec(spec)
spec.loader.exec_module(backend)
t = backend.t
states = np.array(list(itertools.product([0., 1.], repeat=2)))


def read_csv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def independent_global_certificate(p):
    """225 subset branches instead of four ordered regions with kink biases."""
    P = [(1-p)**2, p*(1-p), p*(1-p), p*p]
    binary = list(itertools.product([0, 1], repeat=2))
    den = 1+t*t
    collections = []
    for i in range(2):
        row = [1/den, t/den] if i == 0 else [t/den, t*t/den]
        z = [sum(row[j]*b[j] for j in range(2)) for b in binary]
        y = [b[i] for b in binary]
        branches = []
        for mask in itertools.product([False, True], repeat=4):
            if not any(mask):
                continue
            A = sum(P[j] for j in range(4) if mask[j])
            B = sum(P[j]*(y[j]-z[j]) for j in range(4) if mask[j])
            C = sum(P[j]*((y[j]-z[j])**2 if mask[j] else y[j]**2) for j in range(4))
            beta = s.cancel(B/A)
            constraints = [backend.positive_numerator((z[j]+beta)*(1 if mask[j] else -1)) for j in range(4)]
            branches.append((beta, s.cancel(C-B*B/A), constraints))
        collections.append(branches)
    candidates = {}
    for one, two in itertools.product(*collections):
        objective = s.cancel(one[1]+two[1]/2)
        constraints = one[2]+two[2]
        roots = {}
        for poly in constraints+[backend.positive_numerator(s.diff(objective, t)), s.Poly(t, t)]:
            for root in backend.roots_of_expression(poly.as_expr()):
                roots[root['key']] = root
        for root in roots.values():
            if any(backend.sign_at(poly, root) < 0 for poly in constraints):
                continue
            key = (str(objective), root['key'])
            candidates.setdefault(key, {'objective': objective, 'root': root,
                                       'bounds': backend.value_interval(objective, root)})
    values = list(candidates.values())
    best = min(values, key=lambda c: c['bounds'][1])
    assert all(c['bounds'][0] > best['bounds'][1] for c in values if c is not best)
    assert best['bounds'][1] < p*(1-p)/2  # best mono; infinity is larger
    assert best['bounds'][1] < p/2       # excludes either all-off plateau
    # Target-one kinks cannot be local minima (downward derivative jump).
    # Target-zero kinks have continuous derivatives, captured by subsets.
    return best, len(values)


def main():
    checks = []
    manifest = json.loads((RUN/'sha256_manifest.json').read_text())
    for name, expected in manifest.items():
        assert hashlib.sha256((RUN/name).read_bytes()).hexdigest() == expected, name
    settings = json.loads((RUN/'settings.json').read_text())
    assert settings['frequencies'] == ['1/20', '1/5', '7/20', '3/8', '2/5']
    assert settings['primary_sigmas'] == [0., .05, .15, .30, .60]
    pc = (3-s.sqrt(5))/2
    models = {}
    for frequency in settings['frequencies']:
        p = s.Rational(frequency); case = RUN/f'p_{float(p):.3f}'
        for model in json.loads((case/'selected_models.json').read_text()):
            models[(float(p), model['label'])] = (np.array(model['W']), np.array(model['bias']))
        w, bias = models[(float(p), 'clean_selected')]
        if p < pc:
            best, count = independent_global_certificate(p)
            original = json.loads((case/'certificate_summary.json').read_text())
            assert s.cancel(s.sympify(original['winner']['objective'], locals={'t': t})-best['objective']) == 0
            assert s.Poly(s.sympify(original['winner']['root']['polynomial'], locals={'t': t}), t).monic() == best['root']['poly']
            root_bounds = [s.Rational(v) for v in original['winner']['root']['isolating_interval']]
            assert max(root_bounds[0], best['root']['ab'][0]) <= min(root_bounds[1], best['root']['ab'][1])
            checks.append({'p': frequency, 'independent_subset_branches': 225,
                           'distinct_candidates': count, 'same_exact_optimum': True,
                           'root_polynomial': str(best['root']['poly'].as_expr())})
        else:
            assert np.array_equal(w, np.array([[1., 0.]]))
            assert np.array_equal(bias, np.array([0., float(p)]))
            checks.append({'p': frequency, 'mono_theorem_selection': 'verified'})
        print('Independent selection check passed:', frequency, flush=True)
    max_bias = max_risk = max_mse = max_energy = max_curve = max_root = 0.
    for (pf, label), (w, bias) in models.items():
        P = np.prod(np.where(states == 1, pf, 1-pf), axis=1)
        z = states @ (w.T@w)
        per_loss = np.sum(P[:, None]*(np.maximum(z+bias, 0)-states)**2, axis=0)
        for i in range(2):
            max_bias = max(max_bias, abs(per_loss[i]-scalar_bias_mask_minimum(z[:, i], states[:, i], P)))
        max_energy = max(max_energy, abs(float(np.sum(w*w))-1))
    rows = read_csv(RUN/'primary_risks.csv')
    assert len(rows) == 150
    mse_cache = {}
    for row in rows:
        pf = float(row['p']); sigma = float(row['sigma']); label = row['label']
        w, bias = models[(pf, label)]
        P = np.prod(np.where(states == 1, pf, 1-pf), axis=1)
        err, fp, fn = latent_risk(w, bias, states, P, sigma, row['detector'])
        for i in range(2):
            for prefix, actual in [('error', err[i]), ('fp', fp[i]), ('fn', fn[i])]:
                max_risk = max(max_risk, abs(float(row[f'{prefix}_{i}'])-actual))
        cachekey = (pf, label, sigma)
        if cachekey not in mse_cache:
            mse_cache[cachekey] = quadrature_mse(w, bias, states, P, sigma)
        for i in range(2):
            max_mse = max(max_mse, abs(float(row[f'mse_{i}'])-mse_cache[cachekey][i]))
    curves = read_csv(RUN/'display_risk_curves.csv')
    assert len(curves) == 1200
    def difference(pf, sigma):
        P = np.prod(np.where(states == 1, pf, 1-pf), axis=1)
        one = latent_risk(*models[(pf, 'clean_selected')], states, P, sigma, 'actual_decoder')[0]
        two = latent_risk(*models[(pf, 'mono_retain_0')], states, P, sigma, 'actual_decoder')[0]
        return float(np.array([1., .5])@(one-two))
    for row in curves:
        val = difference(float(row['p']), float(row['sigma']))
        max_curve = max(max_curve, abs(val-float(row['difference'])))
    crossing_rows = json.loads((RUN/'display_crossings.json').read_text())
    for row in crossing_rows:
        assert 'failure' not in row and row['converged']
        pf = row['p']; left = difference(pf, row['lower_sigma']); right = difference(pf, row['upper_sigma'])
        assert left*right < 0 and min(abs(left), abs(right)) > 1e-12
        max_root = max(max_root, abs(difference(pf, row['root_sigma'])))
    assert max_bias < 1e-12 and max_risk < 1e-12 and max_curve < 1e-12
    assert max_mse < 1e-9 and max_energy < 1e-12 and max_root < 1e-9
    result = {'hashes_checked': len(manifest), 'global_selection_checks': checks,
              'primary_risk_rows': len(rows), 'display_formula_values': len(curves),
              'numerical_crossings_checked': len(crossing_rows),
              'max_bias_loss_difference': max_bias, 'max_risk_difference': max_risk,
              'max_mse_quadrature_difference': max_mse, 'max_energy_difference': max_energy,
              'max_display_difference': max_curve, 'max_crossing_residual': max_root,
              'all_checks_passed': True,
              'limits': 'Different branch construction and scalar risk evaluation share the reviewed exact root backend and SciPy CDF library. Checks do not establish all noise crossings, novelty or variable-load transfer.'}
    (HERE/'review').mkdir(exist_ok=True)
    (HERE/'review'/'verification_results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
