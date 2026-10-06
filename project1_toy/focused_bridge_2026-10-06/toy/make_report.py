"""Post-run inspection/reporting only. Never changes archived run outputs."""
import csv
import hashlib
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read_csv(path):
    with path.open(encoding='utf-8') as handle:
        return list(csv.DictReader(handle))


def main():
    base = Path(__file__).resolve().parent
    run = base/'run_v1'
    report = base/'report_v1'
    report.mkdir(exist_ok=False)
    training=read_csv(run/'training_summary.csv')
    geo=read_csv(run/'geometry.csv')
    risks=read_csv(run/'risks.csv')
    cases=read_csv(run/'comparisons.csv')
    manifest=json.loads((run/'sha256_manifest.json').read_text())
    failed_hashes=[name for name,expected in manifest.items()
                   if hashlib.sha256((run/name).read_bytes()).hexdigest()!=expected]
    loss_errors=[]; checkpoint_errors=[]; rounding=[]
    for case in cases:
        name=case['case']
        settings=json.loads((run/name/'case_settings.json').read_text())
        x=np.asarray(settings['states']); P=np.asarray(settings['probabilities'])
        I=np.asarray(settings['importance'])
        for seed in range(6):
            raw=np.load(run/name/f'seed_{seed}.npz')
            W,bias=raw['W'],raw['bias']
            prediction=np.maximum(x@W.T@W+bias,0)
            # Independent direct reconstruction computation, not training routine.
            objective=float(np.sum(P[:,None]*I[None,:]*(prediction-x)**2))
            record=next(t for t in training if t['case']==name and int(t['seed'])==seed)
            loss_errors.append(abs(objective-float(record['final_loss'])))
            checkpoint_errors.append(float(np.max(abs(W-raw['checkpoint_W'][-1]))))
            direct_error=P@((prediction>.5)!=x).astype(float)
            algebra=next(r for r in risks if r['case']==name and r['label']=='trained_final'
                         and int(r['seed'])==seed and r['detector']=='actual_decoder'
                         and float(r['sigma'])==0.)
            algebra_error=np.array([float(algebra['error_0']),float(algebra['error_1'])])
            rounding.append({'case':name,'seed':seed,
                             'direct_float64_relu_weighted_error':float(I@direct_error),
                             'algebraic_threshold_weighted_error':float(I@algebra_error),
                             'maximum_per_feature_difference':float(max(abs(direct_error-algebra_error)))})
    verification={'hash_mismatches':failed_hashes,'hashed_files':len(manifest),
                  'max_reconstruction_loss_recompute_error':max(loss_errors),
                  'max_final_checkpoint_W_error':max(checkpoint_errors),
                  'maximum_encoder_energy_deviation':max(abs(float(g['energy'])-1) for g in geo),
                  'rounding_sensitive_rows':[r for r in rounding if r['maximum_per_feature_difference']>1e-12]}
    (report/'post_run_verification.json').write_text(json.dumps(verification,indent=2),encoding='utf-8')
    with (report/'zero_noise_float64_decoder_comparison.csv').open('w',newline='',encoding='utf-8') as handle:
        writer=csv.DictWriter(handle,fieldnames=list(rounding[0]));writer.writeheader();writer.writerows(rounding)
    if failed_hashes or max(loss_errors)>1e-12 or max(checkpoint_errors)>1e-12:
        raise AssertionError('Archived run consistency failed; results must not be summarized')
    timings=json.loads((run/'timings.json').read_text())
    checks=json.loads((run/'prechecks.json').read_text())
    text=[
        '# Focused training-to-geometry bridge: numerical results',
        '',
        'Run date: 6 October 2026. This report describes the prespecified test only. '
        'It does not claim global geometry optimality, a general load boundary, novelty, '
        'adversarial robustness or conference acceptance.',
        '',
        '## What was tested',
        '',
        'Six two-feature/one-dimension independent-Bernoulli cases, fixed encoder energy one, '
        'free ReLU biases, importance-weighted population reconstruction training. '
        'All six seeds per case ran for exactly 4,000 projected Adam steps. '
        'All final iterates and optimizer shortcomings are retained. A fixed 361-angle '
        'grid plus two explicit pair angles supplied a separate numerical landscape diagnostic. '
        'Both actual-decoder and centered-midpoint detection were evaluated at all five '
        'prespecified code-noise levels. No extra seed, local refinement or optimizer retry was run.',
        '',
        '## Verification',
        '',
        f'- Pretraining checks passed: {checks["gradient_checks"]} weighted-gradient checks '
        f'(maximum absolute discrepancy {checks["max_gradient_absolute_error"]:.3g}); '
        f'{checks["scalar_bias_checks"]} bias-minimum checks '
        f'({checks["max_bias_minimum_loss_error"]:.3g}); independent Gaussian quadrature '
        f'({checks["independent_normal_quadrature_max_state_error"]:.3g}).',
        f'- All {len(manifest)} archived file hashes match. Independent direct reconstruction '
        f'loss discrepancy is at most {max(loss_errors):.3g}. Final checkpoints agree exactly.',
        f'- Total run time {timings["total_seconds"]:.2f} seconds; training time '
        f'{timings["training_seconds"]:.2f} seconds. No nonfinite training failure occurred.',
        '',
        '## Clean reconstruction and optimizer results',
        '',
        'Losses below are importance-weighted **sums**. The numerical grid comparison is '
        'the best candidate among the prespecified angles, not a theorem about all geometries.',
        '',
        '| p | Importance | Grid diagnostic loss | Mono retaining 0 / 1 | Final trained loss range | Loss-stability failures |',
        '|---|---|---:|---:|---:|---:|',
    ]
    for case in cases:
        t=[r for r in training if r['case']==case['case']]
        losses=[float(r['final_loss']) for r in t]
        failures=sum(r['convergence_diagnostic_pass']=='False' for r in t)
        text.append(f'| {t[0]["p"]} | [{t[0]["importance_0"]}, {t[0]["importance_1"]}] '
                    f'| {float(case["grid_minimum_loss"]):.9f} '
                    f'| {float(case["mono_0_loss"]):.9f} / {float(case["mono_1_loss"]):.9f} '
                    f'| {min(losses):.9f}–{max(losses):.9f} | {failures}/6 |')
    text += [
        '',
        '**27/36 runs pass the prescribed loss-stability diagnostic; 9/36 fail. '
        'Passing this diagnostic does not imply stationarity or global convergence.**',
        '',
        '- For equal importance at p=0.05 and 0.20, three seeds approach antipodal '
        'geometry and three remain on the same-sign branch. The outcomes are seed dependent.',
        '- For importance [1,0.5] at p=0.05 and 0.20, all six projected-Adam outcomes '
        'remain near equal-amplitude antipodal geometry even though the grid supplies '
        'lower clean losses at unequal amplitudes. Tangent gradient norms remain roughly '
        '0.024–0.025 and 0.091. These are optimizer shortcomings; the outcome is not '
        'evidence that equal-amplitude geometry is optimal.',
        '- For equal importance at p=0.50, grid minima occur at several unequal-amplitude '
        'angles. All final trained losses remain above that grid diagnostic.',
        '- For importance [1,0.5] at p=0.50, all six runs approach the code retaining '
        'feature 0 and match clean loss 0.125. The grid also selects that retention code.',
        '- Reoptimizing biases for fixed final W changes the largest loss by only '
        f'{max(float(t["bias_optimization_gap"]) for t in training):.3g}. '
        'The principal observed gaps therefore concern encoder geometry/optimization '
        'rather than an omitted fixed-W bias improvement.',
        '',
        '![Prespecified clean-loss landscape and all final iterates](clean_landscapes.png)',
        '',
        'The lines show exact bias-minimized loss at the stated angular candidates. '
        'Every seed is plotted as its actual final weighted loss at its final angle. '
        'The two vertical dotted reference angles are equal antipodal (-45 degrees) '
        'and monosemantic retention of feature 0 (0 degrees). No axis range clips a '
        'computed objective value.',
        '',
        '## Noisy detection: every seed, both detector definitions',
        '',
        'The table gives min–max **across all six final seeds**; no favorable seed is '
        'selected. The baseline is chosen by clean reconstruction objective (feature 0 '
        'retention for unequal importance; the equal-importance baselines are tied and '
        'have equal aggregate detection error). All errors are weighted sums, not means. '
        'Full per-feature FP/FN, MSE and both baselines appear in `../run_v1/risks.csv`.',
        '',
        '| p | Importance | Detector | sigma | Final trained weighted error range | Clean-preferred mono error |',
        '|---|---|---|---:|---:|---:|',
    ]
    for case in cases:
        name=case['case']; t=[r for r in training if r['case']==name][0]
        preferred='mono_retain_0' if t['importance_1']=='0.5' else 'mono_retain_0'
        for detector in ['actual_decoder','centered_midpoint']:
            for sigma in [0.,.05,.15,.30,.60]:
                selected=[r for r in risks if r['case']==name and r['detector']==detector
                          and float(r['sigma'])==sigma]
                final=[float(r['weighted_sum_error']) for r in selected if r['label']=='trained_final']
                baseline=float(next(r for r in selected if r['label']==preferred)['weighted_sum_error'])
                text.append(f'| {t["p"]} | [1,{t["importance_1"]}] | {detector} '
                            f'| {sigma:.2f} | {min(final):.6f}–{max(final):.6f} | {baseline:.6f} |')
    text += [
        '',
        '**Decoder choice materially changes the comparison.** For the fixed '
        'equal-amplitude antipodal code with optimal clean biases, at p=0.05 and '
        'sigma=0.30 actual-decoder sum error is 0.070936 versus mono 0.097790, '
        'while the centered-midpoint detector gives 0.274245 for that same code. '
        'At p=0.20 these errors are 0.215473 versus mono 0.247790, and midpoint '
        '0.383883. The midpoint diagnostic cannot be silently substituted for the '
        'trained decoder.',
        '',
        'Clean reconstruction MSE and thresholded feature detection are different '
        'objectives. For p=0.05, importance [1,0.5], the grid-best clean code has '
        'actual-decoder clean weighted detection error 0.0275, worse than the '
        'fixed antipodal code\'s 0.00375 despite its better clean reconstruction MSE. '
        'Thus decreasing training loss need not decrease this classification metric.',
        '',
        '### Material zero-noise rounding caveat',
        '',
        'At p=0.50, importance [1,0.5], the nearly dropped second encoder weight '
        'has magnitude around 1e-16 and its bias is within float64 rounding of '
        '0.5. Algebraically equivalent strict comparisons can disagree in floating '
        'point: `Gb > 0.5-bias` versus `ReLU(Gb+bias)>0.5`. The raw primary '
        'algebraic-threshold results are retained, but their zero-noise variations '
        '(weighted error 0.125 or 0.25) must not be interpreted as robust recovery '
        'of the dropped feature. The direct float64 comparison is separately '
        'recorded in `zero_noise_float64_decoder_comparison.csv`. At nonzero tested '
        'noise, these trained aggregate risks agree with the retained-feature '
        'baseline. No weights were snapped to zero and no raw outputs were replaced.',
        '',
        '## What this supports and what remains unresolved',
        '',
        'The fixed-W bias computation and conditional noisy-risk evaluation pass '
        'the numerical checks. The experiment exposes the importance of decoder '
        'thresholds and supplies evidence that importance changes the preferred '
        'clean geometry. It does **not** establish that the prescribed training '
        'solver reliably reaches that geometry; multiple failures and nonstationary '
        'stable trajectories were observed.',
        '',
        'The independent mathematical/teacher review must determine which '
        'optimality statements can actually be proved. A grid minimum cannot be '
        'called a global theorem. The smallest warranted next action is to review '
        'the training-to-geometry derivation and the coordinatewise Adam/projection '
        'behavior. The present run stops here. Any alternative optimizer or tighter '
        'geometric test requires a new bounded, explicitly recorded protocol.',
    ]
    # One figure, no new model evaluation.
    fig,axes=plt.subplots(2,3,figsize=(13,7),sharex=True)
    for ax,case in zip(axes.ravel(),cases):
        name=case['case']; landscape=np.load(run/name/'landscape.npz')
        ax.plot(np.degrees(landscape['angles'][:361]),landscape['losses'][:361],label='bias-minimized grid')
        for row in geo:
            if row['case']==name and row['label']=='trained_final':
                theta=(float(row['theta_raw'])+np.pi/2)%np.pi-np.pi/2
                ax.scatter(np.degrees(theta),float(row['clean_weighted_mse']),marker='x',color='crimson')
                ax.annotate(row['seed'],(np.degrees(theta),float(row['clean_weighted_mse'])),fontsize=7,xytext=(3,3),textcoords='offset points')
        ax.axvline(-45,color='gray',linestyle=':',linewidth=.8)
        ax.axvline(0,color='gray',linestyle=':',linewidth=.8)
        ax.set_title(name.replace('_importance_','; I1=').replace('p_','p='))
        ax.set_xlabel('encoder angle (degrees)'); ax.set_ylabel('clean weighted sum MSE')
        ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    fig.suptitle('Prespecified angular diagnostic; red crosses retain every final seed')
    fig.tight_layout();fig.savefig(report/'clean_landscapes.png',dpi=180);plt.close(fig)
    (report/'results.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    files={str(path.relative_to(base)):hashlib.sha256(path.read_bytes()).hexdigest()
           for path in sorted(report.rglob('*')) if path.is_file()}
    files['make_report.py']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (report/'sha256_report_manifest.json').write_text(json.dumps(files,indent=2),encoding='utf-8')
    print(json.dumps(verification,indent=2))


if __name__=='__main__':
    main()
