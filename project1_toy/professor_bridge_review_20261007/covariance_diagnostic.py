"""Read-only applicability diagnostic; no training, risk evaluation, or new noise."""
import hashlib
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent / 'covariance_diagnostic.json'
if OUT.exists():
    raise FileExistsError('Do not overwrite original diagnostic evidence')
cases = {
    'hidden_channels': ROOT / 'project1_toy/vision_transfer_20261006/vision_run_v1',
    'class_evidence': ROOT / 'project1_toy/head_transfer_20261007/evaluation_run_v1',
}
report = {'scope': 'Saved targets and saved clean grids only; no new fitting or noise.', 'cases': {}}
for name, folder in cases.items():
    target_file = folder / 'normalized_targets.npz'
    grid_file = folder / 'clean_selection.json'
    settings_file = folder / 'settings.json'
    arrays = np.load(target_file)
    selection = json.loads(grid_file.read_text())
    settings = json.loads(settings_file.read_text())
    result = {'input_sha256': {
        str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in [target_file, grid_file, settings_file]
    }, 'splits': {}, 'saved_grid_neighbours': []}
    for split in ['train', 'calibration', 'test']:
        key = split if split in arrays.files else 'cal'
        x = arrays[key]
        cov = float(np.mean((x[:, 0] - x[:, 0].mean()) * (x[:, 1] - x[:, 1].mean())))
        var = np.var(x, axis=0)
        result['splits'][split] = dict(
            n=len(x), means=x.mean(axis=0).tolist(), variances=var.tolist(),
            covariance=cov, correlation=float(cov / np.sqrt(var.prod())),
            empirical_mono_directional_slopes=[-2 * settings['importance'][1] * cov,
                                               -2 * settings['importance'][0] * cov],
        )
    for history in selection['histories']:
        grid = history['grid']
        for endpoint in [0.0, np.pi / 2]:
            index = min(range(len(grid)), key=lambda j: abs(grid[j]['angle'] - endpoint))
            centre = grid[index]
            for neighbour in [(index - 1) % len(grid), (index + 1) % len(grid)]:
                row = grid[neighbour]
                # Signed angular difference modulo pi, oriented locally.
                step = (row['angle'] - centre['angle'] + np.pi / 2) % np.pi - np.pi / 2
                result['saved_grid_neighbours'].append(dict(
                    grid_size=history['size'], endpoint_angle=endpoint,
                    neighbour_angle=row['angle'], signed_angular_step=float(step),
                    endpoint_loss=centre['loss'], neighbour_loss=row['loss'],
                    loss_change=row['loss'] - centre['loss'],
                    angular_secant=(row['loss'] - centre['loss']) / step,
                ))
    report['cases'][name] = result
OUT.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
