"""Independent bounded Gaussian quadrature and immutable-record verification.

Does not import the experiment's moment or calibration implementations.
Does not change run_v1 or optimize another geometry.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.special import ndtr

BASE = Path(__file__).resolve().parent
RAW = BASE / 'run_v1'


def check():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=BASE/'independent_review_reproduction',
                        help='Fresh review directory; an existing path is refused.')
    OUT = parser.parse_args().output.resolve()
    OUT.mkdir(exist_ok=False)
    hashes = json.loads((RAW / 'sha256_manifest.json').read_text())
    for name, expected in hashes.items():
        assert hashlib.sha256((RAW / name).read_bytes()).hexdigest() == expected, name
    settings = json.loads((RAW / 'settings.json').read_text())
    assert settings['sigmas'] == [0., .3, .6]
    assert settings['p'] == .5 and settings['importance'] == [1., 1.]
    assert settings['fixed_W'] and settings['no_new_training']
    states = np.array([[0., 0.], [0., 1.], [1., 0.], [1., 1.]])
    phi = lambda x: math.exp(-x*x/2) / math.sqrt(2*math.pi)
    records = []
    all_rows = list(csv.DictReader((RAW / 'outcomes.csv').open()))
    for row in all_rows:
        label = row['label']; sigma = float(row['sigma'])
        data = np.load(RAW / label / f'sigma_{sigma:.2f}' / 'outputs.npz')
        W = data['W']; G = W.T @ W
        assert abs(np.sum(W*W)-1) < 1e-14
        for kind, biases, expected in [('frozen', data['clean_bias'], data['frozen_mse']),
                                      ('calibrated', data['calibrated_bias'], data['calibrated_mse'])]:
            for i in range(2):
                total = error = tail = 0.
                sd = sigma * abs(W[0, i])
                for b in states:
                    mu = float((G @ b)[i]+biases[i]); y = b[i]
                    if sd == 0:
                        val = (max(mu, 0)-y)**2; qerror = bound = 0.
                    else:
                        cuts = sorted(set([-12., 0., 12.] + ([-mu/sd] if -12 < -mu/sd < 12 else [])))
                        integrand = lambda z: (max(mu+sd*z, 0)-y)**2*phi(z)
                        integrals = [quad(integrand, lo, hi, epsabs=1e-13, epsrel=1e-13)
                                     for lo, hi in zip(cuts[:-1], cuts[1:])]
                        val = sum(x[0] for x in integrals); qerror = sum(x[1] for x in integrals)
                        Q = ndtr(-12.)
                        bound = 4*(abs(mu)+1)**2*Q + 4*sd**2*(12*phi(12)+Q)
                    total += val/4; error += qerror/4; tail += bound/4
                discrepancy = abs(total-float(expected[i]))
                assert discrepancy <= 1e-11, (label, sigma, kind, i, discrepancy)
                records.append(dict(label=label, sigma=sigma, decoder=kind, feature=i,
                                    quadrature=total, saved=float(expected[i]),
                                    discrepancy=discrepancy, quadrature_error_estimate=error,
                                    omitted_tail_bound=tail))
        if sigma:
            for i in range(2):
                result = json.loads((RAW / label / f'sigma_{sigma:.2f}' / f'feature_{i}' / 'result.json').read_text())
                assert result['resolved'] and result['global_gap'] <= 1e-8
                if abs(W[0, i]) == 0:
                    assert result['objective'] == .25 and result['beta'] == .5
                    continue
                folder = RAW / label / f'sigma_{sigma:.2f}' / f'feature_{i}'
                boundary = json.loads((folder / 'boundary_checks.json').read_text())
                assert boundary['lower_halfline_cannot_beat_feasible_upper']
                assert boundary['upper_halfline_cannot_beat_feasible_upper']
                H = 2*(1+1/(sigma*abs(W[0, i])*math.sqrt(2*math.pi)))
                assert abs(H-boundary['curvature_bound']) < 1e-13
                nodes = list(csv.DictReader((folder / 'interval_ledger.csv').open()))
                for node in nodes:
                    f = float(node['midpoint_loss']); g = float(node['midpoint_gradient'])
                    h = float(node['radius'])
                    lower = max(0., f-abs(g)*h-H*h*h/2-1e-12)
                    assert abs(lower-float(node['lower_bound'])) < 1e-13
                active = json.loads((folder / 'remaining_intervals.json').read_text())
                lower = min([result['global_upper'], boundary['excluded_lower_halfline_loss_bound'],
                             boundary['upper_halfline_loss_lower_bound']] + [x['lower'] for x in active])
                assert abs(lower-result['global_lower']) < 1e-13
    differences = []
    for sigma in [0., .3, .6]:
        by_label = {r['label']:r for r in all_rows if float(r['sigma']) == sigma}
        same = by_label['shared_same_sign']; opp = by_label['shared_opposite_sign']; mono = by_label['mono_retain_0']
        assert abs(float(same['calibrated_sum_mse'])-float(opp['calibrated_sum_mse'])) < 1e-13
        delta = float(same['calibrated_sum_mse'])-float(mono['calibrated_sum_mse'])
        lower = float(same['calibrated_global_lower'])-float(mono['calibrated_global_upper'])
        upper = float(same['calibrated_global_upper'])-float(mono['calibrated_global_lower'])
        assert upper < 0 if sigma == 0 else lower > 0
        differences.append(dict(sigma=sigma, calibrated_sharing_minus_mono=delta,
                                numerical_gap_lower=lower, numerical_gap_upper=upper))
    report = dict(status='passed', raw_hashes_verified=len(hashes), checked_feature_risks=len(records),
                  max_mse_discrepancy=max(x['discrepancy'] for x in records),
                  max_omitted_tail_bound=max(x['omitted_tail_bound'] for x in records),
                  interpretation='Same-MSE reversal survives symmetric oracle bias calibration in this fixed dense toy. Numerical global gaps are floating checks, not exact interval certificates.',
                  risk_checks=records, differences=differences)
    (OUT / 'results.json').write_text(json.dumps(report, indent=2))
    print(json.dumps({k:v for k,v in report.items() if k != 'risk_checks'}, indent=2))


if __name__ == '__main__':
    check()
