"""Presentation copy of saved risk curves; never changes scientific run outputs.

Makes the exactly-zero mono panel legible, and marks already-saved numerical
crossings. Every line uses the same archived CSV values without alteration.
"""
import csv
import hashlib
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RUN = HERE / 'toy' / 'run_v1'
OUT = HERE / 'report'


def main():
    with (RUN/'display_risk_curves.csv').open(newline='', encoding='utf-8') as f:
        curves = list(csv.DictReader(f))
    with (RUN/'primary_risks.csv').open(newline='', encoding='utf-8') as f:
        primary = list(csv.DictReader(f))
    roots = json.loads((RUN/'display_crossings.json').read_text())
    fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharex=True)
    for ax, p in zip(axes.ravel(), [.05, .20, .35, .375, .40]):
        rows = [r for r in curves if float(r['p']) == p]
        x = [float(r['sigma']) for r in rows]
        y = [float(r['difference']) for r in rows]
        ax.semilogx(x, y, color='#245b9a', label='selected code minus mono')
        ax.axhline(0, color='black', linewidth=.8)
        ax.fill_between(x, y, 0, where=[v < 0 for v in y], color='#4a9b62', alpha=.25,
                        label='numerically lower error')
        selected = [r for r in primary if float(r['p']) == p and r['label'] == 'clean_selected'
                    and r['detector'] == 'actual_decoder' and float(r['sigma']) > 0]
        control = {float(r['sigma']): float(r['weighted_sum_error']) for r in primary
                   if float(r['p']) == p and r['label'] == 'mono_retain_0'
                   and r['detector'] == 'actual_decoder'}
        ax.scatter([float(r['sigma']) for r in selected],
                   [float(r['weighted_sum_error'])-control[float(r['sigma'])] for r in selected],
                   color='#d37b00', s=24, zorder=3, label='prespecified noise settings')
        for root in roots:
            if root['p'] == p and root.get('converged'):
                ax.axvline(root['root_sigma'], color='gray', linestyle=':', linewidth=.8)
        if all(v == 0 for v in y):
            ax.set_ylim(-.001, .001)
            ax.text(.5, .73, 'Selected geometry is mono\nDifference is exactly zero',
                    transform=ax.transAxes, ha='center', fontsize=9)
        ax.set_title(f'p = {p:g}')
        ax.set_xlabel('Gaussian code-noise standard deviation')
        ax.set_ylabel('Weighted detection-error difference')
        ax.grid(alpha=.2)
    axes.ravel()[-1].axis('off')
    handles, labels = axes.ravel()[0].get_legend_handles_labels()
    axes.ravel()[-1].legend(handles, labels, loc='upper left', frameon=False, fontsize=9)
    axes.ravel()[-1].text(.03, .53,
        'Below zero: selected code helps\nAbove zero: mono helps\n\n'
        'Dotted lines: saved numerical crossings\n'
        'Each panel has its own vertical scale\n'
        'No claim of all roots or a monotone boundary', transform=axes.ravel()[-1].transAxes,
        fontsize=9, va='top')
    fig.suptitle('Actual decoder: sharing can help over an intermediate noise range', fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, .96])
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT/'actual_risk_difference.png', dpi=180)
    plt.close(fig)
    hashes = {name: hashlib.sha256((RUN/name).read_bytes()).hexdigest()
              for name in ['display_risk_curves.csv', 'primary_risks.csv', 'display_crossings.json']}
    (OUT/'plot_provenance.json').write_text(json.dumps({
        'source_hashes': hashes,
        'change': 'Presentation only: zero panel scale and label, saved crossing markers, negative-area shading. No numerical values changed; original run plots preserved.',
        'source_script': 'plot_report.py'}, indent=2))
    print('Saved presentation plot and provenance; raw archive unchanged.')


if __name__ == '__main__':
    main()
