"""Independently check saved applicability moments and grid lookups; no fitting."""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Use a fresh audit output path.')
    source = Path(__file__).with_name('covariance_diagnostic.json')
    diagnostic = json.loads(source.read_text())
    findings = {}
    for name, case in diagnostic['cases'].items():
        paths = [ROOT / rel.replace('\\', '/') for rel in case['input_sha256']]
        for path, expected in zip(paths, case['input_sha256'].values()):
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected
        target = next(p for p in paths if p.name == 'normalized_targets.npz')
        grid_path = next(p for p in paths if p.name == 'clean_selection.json')
        settings_path = next(p for p in paths if p.name == 'settings.json')
        settings = json.loads(settings_path.read_text())
        with np.load(target) as arrays:
            for split, record in case['splits'].items():
                key = split if split in arrays.files else 'cal'
                x = arrays[key]
                assert np.all(x >= 0) and np.all(np.isfinite(x))
                means = np.sum(x, axis=0) / len(x)
                moments = np.sum(x * x, axis=0) / len(x)
                variances = moments - means * means
                covariance = float(np.dot(x[:, 0], x[:, 1]) / len(x) - means.prod())
                assert len(x) == record['n']
                assert np.allclose(means, record['means'], rtol=0, atol=1e-12)
                assert np.allclose(variances, record['variances'], rtol=0, atol=1e-12)
                assert abs(covariance-record['covariance']) < 1e-12
                assert abs(covariance / np.sqrt(variances.prod()) - record['correlation']) < 1e-12
                slopes = [-2 * settings['importance'][1] * covariance,
                          -2 * settings['importance'][0] * covariance]
                assert np.allclose(slopes, record['empirical_mono_directional_slopes'], rtol=0, atol=1e-12)
        selection = json.loads(grid_path.read_text())
        for row in case['saved_grid_neighbours']:
            grid = next(h['grid'] for h in selection['histories'] if h['size'] == row['grid_size'])
            centre = next(r for r in grid if r['angle'] == row['endpoint_angle'])
            neighbour = next(r for r in grid if r['angle'] == row['neighbour_angle'])
            assert centre['loss'] == row['endpoint_loss']
            assert neighbour['loss'] == row['neighbour_loss']
            assert abs((neighbour['loss']-centre['loss']) / row['signed_angular_step'] - row['angular_secant']) < 1e-12
        findings[name] = {'splits_checked': len(case['splits']),
                          'saved_neighbours_checked': len(case['saved_grid_neighbours']),
                          'train_covariance': case['splits']['train']['covariance']}
    report = {'passed': True, 'cases': findings,
              'diagnostic_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
              'scope': 'Independent moment formula and exact archived-grid lookup only; no new inference, fitting, corruption, population inference or mathematical proof certification.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
