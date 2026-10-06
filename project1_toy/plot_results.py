"""Plots and factual report from saved values; no fitting, filtering or seed selection."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from toy_math import pair_closed_risks


def read_csv(path):
    with Path(path).open(newline='', encoding='utf-8') as stream:
        return list(csv.DictReader(stream))


def make_plots(out, plot_directory=None):
    out = Path(out)
    plots = Path(plot_directory) if plot_directory is not None else out / 'plots'
    plots.mkdir(parents=True, exist_ok=True)
    config = json.loads((out / 'config.json').read_text())
    totals = read_csv(out / 'trained_total_metrics.csv')
    features = read_csv(out / 'trained_feature_metrics.csv')
    probabilities = config['trained']['probabilities']
    seeds = config['trained']['seeds']
    sigmas = config['trained']['sigmas']

    fig, axes = plt.subplots(len(probabilities), 2, figsize=(10, 11), sharex=True, sharey=True,
                             constrained_layout=True)
    colors = ['tab:blue', 'tab:orange', 'tab:green']
    for pi, p in enumerate(probabilities):
        for di, detector in enumerate(['matched', 'decoder']):
            ax = axes[pi, di]
            for si, seed in enumerate(seeds):
                rows = sorted([r for r in totals if float(r['p']) == p and r['detector'] == detector
                               and r['model'] == 'learned' and int(r['initialization_seed']) == seed],
                              key=lambda r: float(r['sigma']))
                exact = [float(r['exact_mean_feature_error']) for r in rows]
                measured = [float(r['measured_total_error']) / config['trained']['n'] for r in rows]
                errors = [1.96 * float(r['measured_total_error_standard_error']) / config['trained']['n'] for r in rows]
                ax.plot(sigmas, exact, color=colors[si], label=f'Learned seed {seed}: exact')
                ax.errorbar(sigmas, measured, yerr=errors, fmt='.', color=colors[si], capsize=2)
            baseline = sorted([r for r in totals if float(r['p']) == p and r['detector'] == detector
                               and r['model'] == 'mono' and int(r['initialization_seed']) == seeds[0]],
                              key=lambda r: float(r['sigma']))
            ax.plot(sigmas, [float(r['exact_mean_feature_error']) for r in baseline],
                    'k--', label='Restricted mono: exact')
            ax.set_title(f'p={p:.2f}; {detector} detector')
            ax.set_ylabel('Mean feature error')
            ax.set_ylim(bottom=0)
            ax.grid(alpha=.2)
    for ax in axes[-1]:
        ax.set_xlabel('Code-noise standard deviation sigma')
    # Fix the global upper limit after plotting every panel. With shared y axes,
    # setting only bottom=0 inside the loop can freeze a previous upper limit.
    # Include exact values AND the displayed MC confidence limits, without clipping.
    n = config['trained']['n']
    upper = max(max(float(r['exact_mean_feature_error']),
                    (float(r['measured_total_error'])
                     + 1.96 * float(r['measured_total_error_standard_error'])) / n)
                for r in totals)
    for ax in axes.flat:
        ax.set_ylim(0, min(1.0, 1.05 * upper))
    axes[0, 0].legend(fontsize=8)
    fig.suptitle('All initialization seeds; points show simulation with marginal 95% MC intervals')
    fig.savefig(plots / 'learned_vs_mono_risk.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for di, detector in enumerate(['matched', 'decoder']):
        ax = axes[di]
        for p in probabilities:
            rows = [r for r in features if r['model'] == 'learned' and r['detector'] == detector and float(r['p']) == p]
            ax.scatter([float(r['exact_error']) for r in rows], [float(r['measured_error']) for r in rows],
                       s=9, alpha=.45, label=f'p={p}')
        ax.plot([0, 1], [0, 1], 'k--', lw=1)
        ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='Exact state-mixture error',
               ylabel='Measured error', title=f'{detector}: all features, seeds and sigma')
        ax.legend(fontsize=8)
    fig.savefig(plots / 'exact_vs_measured.png', dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5), constrained_layout=True)
    for p in probabilities:
        rows = [r for r in features if r['model'] == 'learned' and r['detector'] == 'matched' and float(r['p']) == p]
        ax.scatter([float(r['exact_error']) for r in rows], [float(r['matched_bound']) for r in rows],
                   s=12, alpha=.5, label=f'p={p}')
    ax.plot([0, 1], [0, 1], 'k--', lw=1)
    ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='Exact feature error', ylabel='Interference upper bound',
           title='Above the diagonal is valid; large distance means a loose bound')
    ax.legend()
    fig.savefig(plots / 'bound_vs_exact.png', dpi=180)
    plt.close(fig)

    matrices = []
    for p in probabilities:
        for seed in seeds:
            with np.load(out / 'trained' / f'p{p:.2f}_seed{seed}' / 'learned_model.npz') as data:
                matrices.append(data['G'].copy())
    limit = max(np.max(np.abs(G)) for G in matrices)
    fig, axes = plt.subplots(len(probabilities), len(seeds), figsize=(10, 12), constrained_layout=True)
    for ax, G, (p, seed) in zip(axes.flat, matrices, [(p, s) for p in probabilities for s in seeds]):
        image = ax.imshow(G, cmap='RdBu_r', vmin=-limit, vmax=limit)
        ax.set_title(f'p={p:.2f}, seed={seed}')
        ax.set(xlabel='Concept j', ylabel='Concept i')
    fig.colorbar(image, ax=axes.ravel().tolist(), label='G_ij (one common, unclipped scale)')
    fig.savefig(plots / 'all_learned_gram_matrices.png', dpi=180)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)
    for ax, p in zip(axes.flat, probabilities):
        for seed in seeds:
            trace = np.loadtxt(out / 'trained' / f'p{p:.2f}_seed{seed}' / 'training_history.csv', delimiter=',', skiprows=1)
            ax.plot(trace[:, 0], trace[:, 1], label=f'seed {seed}')
        mono = (config['trained']['n'] - config['trained']['m']) * p * (1 - p)
        ax.axhline(mono, color='k', ls='--', label='Restricted mono clean MSE')
        ax.set(title=f'p={p}', xlabel='Training step', ylabel='Population sum-of-feature MSE')
        ax.set_ylim(bottom=0)
        ax.legend(fontsize=8)
    fig.savefig(plots / 'training_losses.png', dpi=180)
    plt.close(fig)

    p_axis = np.linspace(.01, .8, 160)
    noise_axis = np.linspace(.01, 1.5, 180)
    pp, ss = np.meshgrid(p_axis, noise_axis)
    gaps = []
    for a in config['pair']['amplitudes']:
        # Vectorize the closed formula; no simulated values or fitted expression.
        from scipy.special import ndtr
        q, q3, qm = ndtr(-a / (2 * ss)), ndtr(-3 * a / (2 * ss)), ndtr(-1 / (2 * ss))
        gaps.append(2 * (1 - pp)**2 * q + 2 * pp * (1 - pp) * (q + q3)
                    + 2 * pp**2 * (1 - q) - pp - qm)
    limit = max(np.max(np.abs(gap)) for gap in gaps)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for ax, gap, a in zip(axes, gaps, config['pair']['amplitudes']):
        im = ax.pcolormesh(pp, ss, gap, cmap='RdBu_r', vmin=-limit, vmax=limit, shading='auto')
        ax.contour(pp, ss, gap, levels=[0], colors='black')
        energy = 2 * a**2
        ax.set(title=f'Pair energy={energy:.1f}; mono energy=1',
               xlabel='Activation probability p', ylabel='Code-noise sigma')
    fig.colorbar(im, ax=axes, label='Exact pair risk minus mono risk; no color clipping')
    fig.savefig(plots / 'fixed_pair_phase_diagram.png', dpi=180)
    plt.close(fig)


def write_report(out):
    out = Path(out)
    summary = json.loads((out / 'summary.json').read_text())
    checks = json.loads((out / 'checks.json').read_text())
    config = json.loads((out / 'config.json').read_text())
    lines = [
        '# Generated results: Project 1 toy protocol v1', '',
        'This report is generated from saved measurements. The complete protocol is',
        '`plan_before_run.md`; exact per-feature values are in the CSVs. No seeds are excluded.', '',
        '## Mathematical and simulation checks', '',
        f"- Pre-run checks: {checks['status']}.",
        f"- Gradient relative difference: {checks['gradient_relative_difference']:.12g}.",
        f"- Pair closed versus state-enumerated risk maximum difference: {checks['pair_closed_vs_enumerated_max_difference']:.12g}.",
        f"- Trained feature comparisons: {summary['trained_feature_comparisons']}.",
        f"- Maximum trained absolute simulation-minus-exact difference: {summary['max_trained_absolute_mc_minus_exact']:.9g}.",
        f"- Maximum pair absolute simulation-minus-exact difference: {summary['max_pair_absolute_mc_minus_exact']:.9g}.",
        f"- Familywise-tolerance failures: trained {summary['trained_familywise_tolerance_failures']}, pair {summary['pair_familywise_tolerance_failures']}.",
        f"- Matched-bound violations: {summary['matched_bound_violations']}.",
        f"- Learned bound minus exact risk: min {summary['learned_bound_slack_min']:.6g}, median {summary['learned_bound_slack_median']:.6g}, max {summary['learned_bound_slack_max']:.6g}.",
        '', 'The upper bound is not a fitted prediction. A valid but loose bound does not',
        'locate a sharp boundary. Exact risk agreement verifies the specified probability',
        'calculation and implementation, not novelty or generalization to other models.', '',
        '## Fixed-code crossings', '',
        '| Pair amplitude | Pair energy | Mono energy | p | Exact crossing sigma |',
        '|---|---|---|---|---|',
    ]
    for crossing in summary['pair_crossings']:
        a = crossing['pair_amplitude']
        lines.append(f"| {a:.9f} | {2*a*a:.6f} | 1 | {crossing['p']} | {crossing['crossing_sigma']:.9f} |")
    lines.extend(['', 'These crossings compare specified fixed codes, not optimized trained networks.', '',
                  '## Training: every final iterate', '',
                  '| p | Seed | Final clean reconstruction MSE | Restricted mono MSE | Loss-window change | Diagnostic passed | Weak columns |',
                  '|---|---|---|---|---|---|---|'])
    for r in summary['training']:
        lines.append(f"| {r['p']:.2f} | {r['initialization_seed']} | {r['final_loss']:.9f} | {r['mono_clean_reconstruction_mse']:.9f} | {r['window_mean_loss_change']:.6g} | {r['convergence_diagnostic_pass']} | {r['weak_columns']} |")
    lines.extend(['', 'This convergence diagnostic measures recent loss stability. It is not a proof',
                  'of stationarity, global optimality, or agreement between initialization seeds.', '',
                  '## Learned versus restricted mono detection risk', '',
                  'Negative differences favor the learned code. Values below are **total errors',
                  'summed over all eight concepts**, averaged across the three retained seeds.',
                  'Min/max show initialization variation, not confidence intervals. See',
                  '`paired_comparisons.csv` for individual-seed simulation estimates and paired SEs.', '',
                  '| p | Detector | sigma | Mean exact learned-minus-mono | Seed min | Seed max | Seeds learned better |',
                  '|---|---|---|---|---|---|---|'])
    for r in summary['risk_comparison_groups']:
        lines.append(f"| {r['p']:.2f} | {r['detector']} | {r['sigma']:.2f} | {r['mean_exact_learned_minus_mono']:+.8f} | {r['min_exact_learned_minus_mono']:+.8f} | {r['max_exact_learned_minus_mono']:+.8f} | {r['seeds_learned_better']}/{r['seed_count']} |")
    lines.extend(['', '## Limits on interpretation', '',
                  '- Binary independent concepts, uniform importance, one feature load (8/4).',
                  '- Training uses the exact population, not finite noisy training samples.',
                  '- The mono baseline uses known concepts; it is a restricted, idealized control.',
                  '- Noise is isotropic Gaussian in code space. No input-space or adversarial claim.',
                  '- The matched detector knows p and differs from the learned decoder.',
                  '- A low detection error for rare features can hide frequent missed presences;',
                  '  false positive and false negative rates are reported separately in the CSV.',
                  '- Geometric overlap is not by itself a semantic assessment of natural-model features.',
                  '- This run contains no load sweep, importance sweep, recursive loop or real model.', '',
                  '## Next decision', '',
                  'Stop here and review these results. The next experiment requires a new dated',
                  'entry in the living plan. Do not retrospectively select a detector, seed or',
                  'noise range that makes the preferred story look stronger.', '',
                  '## Plots', '',
                  '- `plots/training_losses.png`: all training traces, including unsuccessful cases.',
                  '- `plots/learned_vs_mono_risk.png`: both detectors, every initialization seed.',
                  '- `plots/exact_vs_measured.png`: all learned-feature prediction checks.',
                  '- `plots/bound_vs_exact.png`: bound looseness as well as validity.',
                  '- `plots/all_learned_gram_matrices.png`: every learned interference matrix.',
                  '- `plots/fixed_pair_phase_diagram.png`: exact fixed-code risk comparison.', ''])
    (out / 'results.md').write_text('\n'.join(lines), encoding='utf-8')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('run_directory')
    parser.add_argument('--plots-only-to', help='Write corrected views outside an immutable run; do not rewrite its report')
    args = parser.parse_args()
    make_plots(args.run_directory, args.plots_only_to)
    if args.plots_only_to is None:
        write_report(args.run_directory)
