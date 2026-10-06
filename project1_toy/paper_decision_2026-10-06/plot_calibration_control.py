"""Reproduce the control figure using saved rows only; no new experiment.

The default output is separate from the original reviewed figure. Formatting
may differ; every plotted value comes from immutable run_v1/outcomes.csv.
"""
from pathlib import Path
import argparse
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=base/'calibration_control_reproduced.png')
    args = parser.parse_args()
    rows = list(csv.DictReader((base/'run_v1/outcomes.csv').open()))
    sigmas = sorted({float(row['sigma']) for row in rows})
    assert sigmas == [0., .3, .6]
    curves = {}
    for label in ['shared_same_sign', 'shared_opposite_sign', 'mono_retain_0']:
        selected = sorted((r for r in rows if r['label'] == label), key=lambda r:float(r['sigma']))
        curves[label] = {field: np.array([float(r[field]) for r in selected])
                         for field in ['frozen_sum_mse', 'calibrated_sum_mse']}
    for field in curves['shared_same_sign']:
        assert np.max(abs(curves['shared_same_sign'][field]-curves['shared_opposite_sign'][field])) < 1e-13
    fig, ax = plt.subplots(figsize=(12.3, 7.4))
    for label, title, color in [('shared_same_sign', 'Sharing (both signs agree)', '#ff7f0e'),
                                 ('mono_retain_0', 'Mono', '#1f77b4')]:
        ax.plot(sigmas, curves[label]['frozen_sum_mse'], 'o--', color=color,
                label=title+': frozen clean bias', markersize=8)
        ax.plot(sigmas, curves[label]['calibrated_sum_mse'], 's-', color=color,
                label=title+': oracle calibrated bias', markersize=8)
    ax.set(xlabel='Gaussian code-noise standard deviation',
           ylabel='Population sum reconstruction MSE',
           title='Same-outcome reversal survives symmetric bias calibration', xticks=sigmas)
    ax.grid(alpha=.25); ax.legend(loc='upper left')
    fig.text(.5, .015, 'Only the three prescribed settings are plotted; connecting lines are visual guides.',
             ha='center')
    fig.tight_layout(rect=[0,.045,1,1]); fig.savefig(args.output, dpi=150); plt.close(fig)
    print('Plotted only saved values:', args.output)


if __name__ == '__main__':
    main()
