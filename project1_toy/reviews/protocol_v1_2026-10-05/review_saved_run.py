"""Descriptive review of existing outputs only; no new training or simulations.

Writes a separate review, preserving the immutable original experiment directory.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import shutil
import numpy as np
from plot_results import make_plots


def review(run, output):
    run, output = Path(run), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    summary = json.loads((run / 'summary.json').read_text())
    config = json.loads((run / 'config.json').read_text())
    with (run / 'trained_feature_metrics.csv').open(newline='') as stream:
        features = list(csv.DictReader(stream))
    conditional = []
    for p in config['trained']['probabilities']:
        for detector in ['matched', 'decoder']:
            for sigma in config['trained']['sigmas']:
                rows = [r for r in features if r['model'] == 'learned' and float(r['p']) == p
                        and r['detector'] == detector and float(r['sigma']) == sigma]
                conditional.append({
                    'p': p, 'detector': detector, 'sigma': sigma,
                    'mean_exact_false_positive_rate': float(np.mean([float(r['exact_false_positive_rate']) for r in rows])),
                    'mean_exact_false_negative_rate': float(np.mean([float(r['exact_false_negative_rate']) for r in rows])),
                })
    with (output / 'conditional_error_summary.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(conditional[0]))
        writer.writeheader()
        writer.writerows(conditional)
    geometry = []
    for p in config['trained']['probabilities']:
        for seed in config['trained']['seeds']:
            with np.load(run / 'trained' / f'p{p:.2f}_seed{seed}' / 'learned_model.npz') as data:
                G = data['G']
                lengths = np.sqrt(np.diag(G))
                cosine = G / np.outer(lengths, lengths)
                np.fill_diagonal(cosine, np.inf)
                # Report actual row minima; no fitted pair threshold or selected seed.
                minima = cosine.min(axis=1)
                partners = cosine.argmin(axis=1)
                remainder = cosine.copy()
                remainder[np.arange(len(partners)), partners] = 0
                np.fill_diagonal(remainder, 0)
                geometry.append({
                    'p': p, 'initialization_seed': seed,
                    'mean_most_negative_cosine': float(minima.mean()),
                    'max_most_negative_cosine': float(minima.max()),
                    'max_absolute_nonpartner_cosine': float(np.abs(remainder).max()),
                    'partners': partners.tolist(),
                    'all_partners_mutual': bool(all(partners[partners[i]] == i for i in range(len(partners)))),
                })
    (output / 'geometry_review.json').write_text(json.dumps(geometry, indent=2) + '\n')
    make_plots(run, output / 'plots')
    lines = [
        '# Review of saved protocol v1 results', '',
        '**No additional training or simulation was performed for this review.**',
        'The original run remains unchanged. This file separates observations from interpretation.', '',
        '## Presentation correction', '',
        'The original `plots/learned_vs_mono_risk.png` has a plotting defect: successive',
        'bottom-only limits on shared y axes froze an upper limit of about 0.30, clipping',
        'some high-noise values. That original file and its code are preserved for audit.',
        'The corrected plot here sets one upper limit after considering **all** exact values',
        'and all displayed Monte Carlo confidence limits. It does not change any measurement.',
        'All six views are regenerated from the existing data in this review directory.',
        'An initial attempt to create the review plots failed because their parent directory',
        'did not exist; the plotting utility was repaired to create parent directories.', '',
        '## Observations', '',
        f"- All {summary['trained_settings']} trained settings have lower final clean reconstruction MSE than the specified restricted mono baseline.",
        f"- {len(summary['convergence_diagnostic_failures'])}/12 settings fail the prespecified loss-stability diagnostic. Their outcomes remain included.",
        '- At p=0.05, 0.15 and 0.30, both detectors favor the learned code without noise;',
        '  at sigma=0.60 both favor the restricted mono baseline for every seed.',
        '- Detector choice materially affects the intermediate-noise comparison: at sigma=0.30',
        '  the matched detector favors mono for those three activation rates, while the',
        '  trained decoder favors the learned code. Reporting only one would conceal this.',
        '- At p=0.50, both detectors favor the learned code at every tested noise level for',
        '  all seeds. There is no observed reversal within this noise range in that case.',
        '- The error bound has no observed violations, but its learned-feature median',
        f"  slack is {summary['learned_bound_slack_median']:.6f} probability units. It is too loose here to claim a sharp boundary.",
        '- Exact risk versus Monte Carlo agreement supports the calculation for a fixed',
        '  dictionary and detector. It does not establish a theorem selecting trained geometry.', '',
        '## Geometry: post-run descriptive inspection', '',
        'The saved Gram matrices suggest antipodal pair organization at the three lower',
        'activation rates and less pair-specific organization at p=0.50. The following',
        'quantities describe all seeds and were computed **after** inspecting the matrices;',
        'they were not preregistered hypothesis tests. See `geometry_review.json` for partners.', '',
        '| p | Seed | Mean most-negative cosine per feature | Maximum absolute nonpartner cosine | Partners all mutual |',
        '|---|---|---|---|---|',
    ]
    for r in geometry:
        lines.append(f"| {r['p']:.2f} | {r['initialization_seed']} | {r['mean_most_negative_cosine']:.9f} | {r['max_absolute_nonpartner_cosine']:.9f} | {r['all_partners_mutual']} |")
    lines.extend(['', 'These angles are descriptive, not a claim of global optimality, semantic',
                  'monosemanticity in natural models, or a causal intervention.', '',
                  '## Rare concepts: report conditional errors too', '',
                  'A detector that mostly predicts absence can look accurate when p is small.',
                  'The table below averages exact conditional rates across all features and seeds.',
                  'These are different quantities from unconditional error.', '',
                  '| p | Detector | sigma | False-positive rate | False-negative rate |',
                  '|---|---|---|---|---|'])
    for r in conditional:
        if r['sigma'] in [0, .3, .6]:
            lines.append(f"| {r['p']:.2f} | {r['detector']} | {r['sigma']:.2f} | {r['mean_exact_false_positive_rate']:.8f} | {r['mean_exact_false_negative_rate']:.8f} |")
    lines.extend(['', '## What this does and does not establish', '',
                  'The experiment is a successful initial implementation and a controlled example',
                  'of a noise-dependent tradeoff in some tested regimes. It is not the complete',
                  'phase diagram over sparsity, load and importance, and it does not establish',
                  'ICML novelty or transfer to a real model. The dense-case result and differing',
                  'detector comparisons prevent a universal "superposition hurts robustness" claim.', '',
                  '## Proposed next work; not executed', '',
                  '1. Resolve optimizer stability with a logged, fixed-duration follow-up using',
                  '   all original settings. Preserve this run and compare convergence diagnostics;',
                  '   do not pick a checkpoint based on robustness or discard a failed seed.',
                  '2. If the geometry and comparisons are stable, extend this same controlled',
                  '   setup to feature load. State the energy convention and baseline before running.',
                  '3. Only then choose the smallest real-model experiment testing the established',
                  '   mechanism. Do not add model downloads or recursive loops at this stage.', ''])
    (output / 'review.md').write_text('\n'.join(lines), encoding='utf-8')
    for name in ['review_saved_run.py', 'plot_results.py']:
        shutil.copy2(Path(__file__).parent / name, output / name)
    files = []
    for path in sorted(output.rglob('*')):
        if path.is_file() and path.name != 'manifest.json':
            files.append({'path': path.relative_to(output).as_posix(), 'bytes': path.stat().st_size,
                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    (output / 'manifest.json').write_text(json.dumps({'files': files}, indent=2) + '\n')
    print((output / 'review.md').resolve())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run_directory')
    parser.add_argument('review_directory')
    args = parser.parse_args()
    review(args.run_directory, args.review_directory)
