"""Plot archived pilot outputs only; never fit or execute a model."""
from pathlib import Path
import argparse,json,textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--contrast',action='store_true',help='Also render saved paired policy contrast, without new evaluation.')
    args=ap.parse_args()
    assert args.run.is_dir()
    args.output.mkdir(parents=True,exist_ok=False)
    settings_path=args.run/'settings.json'
    settings=json.loads(settings_path.read_text()) if settings_path.exists() else {}
    results_path=args.run/'results.json'
    channels=settings.get('channels',[])
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    if results_path.exists():
        rows=json.loads(results_path.read_text())['cases'];sigma=np.array([r['sigma'] for r in rows])
        fig,ax=plt.subplots(figsize=(8,5))
        unresolved=[]
        for key,label,color,marker in [('delta_frozen','Frozen zero-noise calibration biases','#1f77b4','o'),
                                       ('delta_calibrated','Biases calibrated at each noise','#d95f02','s')]:
            estimates=np.array([r['comparisons'][key]['mean'] for r in rows])
            intervals=np.array([r['comparisons'][key]['interval95'] for r in rows])
            # Percentile intervals need not contain the original point estimate.
            ax.vlines(sigma,intervals[:,0],intervals[:,1],color=color,alpha=.8,lw=1.5)
            ax.plot(sigma,estimates,marker=marker,color=color,label=label,lw=1.4)
            for j,row in enumerate(rows):
                good=all(p['resolved'] for p in row['profiles'].values())
                if not good:
                    ax.plot(sigma[j],estimates[j],marker='x',markersize=11,mew=2,color='black')
                    if j not in unresolved:unresolved.append(j)
        ax.axhline(0,color='black',lw=1,ls='--')
        ax.set_xlabel(r'Absolute scalar code-noise standard deviation $\sigma$')
        ax.set_ylabel(r'Test weighted MSE: $R_{\rm sharing}-R_{\rm mono}$')
        ax.set_title('Fixed learned-activation pair: decoder-policy comparison')
        ax.legend(loc='best',fontsize=9);ax.grid(alpha=.2)
        caption=(f'Operational ResNet18 layer4 central-cell channels {channels}; not semantic labels. '
                 'Bars: paired-image 95% percentile bootstrap, conditional on fitted models.\n'
                 'Negative favors sharing; positive favors mono. Code noise is not image-input corruption. '
                 +('Black × marks unresolved calibration.' if unresolved else 'All saved calibration gaps resolved.'))
        if len(rows)!=5:caption+=' Saved run is incomplete; missing points are not inferred.'
        fig.text(.08,.025,'\n'.join(textwrap.wrap(caption.replace('\n',' '),110)),fontsize=8,ha='left',va='bottom')
        fig.subplots_adjust(left=.12,right=.97,top=.89,bottom=.23)
        filename='vision_policy_risk.png'
        metadata=dict(kind='saved_noisy_risk_comparison',channels=channels,
                      unresolved_case_indices=unresolved,
                      evidence='Held-out conditional Gaussian MSE, paired bootstrap over test images only; not a population proof.')
    else:
        clean_path=args.run/'clean_selection.json'
        if not clean_path.exists():
            (args.output/'plot_status.json').write_text(json.dumps(dict(
                status='No clean or noisy results available; no scientific plot generated.'),indent=2));return
        clean=json.loads(clean_path.read_text());fig,ax=plt.subplots(figsize=(8,5))
        colors=['#7189ad','#154c79']
        for color,hist in zip(colors,clean['histories']):
            grid=hist['grid'];angles=np.array([r['angle'] for r in grid]);loss=np.array([r['loss'] for r in grid])
            ax.plot(angles,loss,color=color,lw=1,label=f"Angle grid {hist['size']}",alpha=.9)
            trace=hist['refinement_trace']
            if trace:
                ax.scatter([r['angle'] for r in trace],[r['loss'] for r in trace],s=16,color=color,
                           marker='.',label=f"Best-cell refinement {hist['size']}")
        mono=clean['mono']['loss'];ax.axhline(mono,color='#d95f02',ls='--',label='Train-selected mono baseline')
        selected=clean['sharing'];angle=float(np.arctan2(selected['weights'][1],selected['weights'][0])%np.pi)
        ax.scatter([angle],[selected['loss']],s=65,marker='*',color='black',label='Final numerical candidate')
        ax.set_xlabel(r'Encoder angle $\theta$ (radians, modulo $\pi$)')
        ax.set_ylabel('Clean training weighted reconstruction MSE')
        ax.set_title('Fixed pair clean selection: eligibility check')
        ax.legend(fontsize=8);ax.grid(alpha=.2)
        caption=(f'Operational channels {channels}; full predeclared angle grids and bounded best-cell traces.\n'
                 'A stopped clean gate permits no noisy-transfer claim. Finite-grid/refinement agreement is not a global certificate.')
        fig.text(.08,.025,'\n'.join(textwrap.wrap(caption.replace('\n',' '),110)),fontsize=8,ha='left',va='bottom')
        fig.subplots_adjust(left=.12,right=.97,top=.89,bottom=.21)
        filename='vision_clean_gate.png'
        metadata=dict(kind='saved_clean_selection',channels=channels,clean_gates=clean['gates'],
                      evidence='Numerical empirical clean selection only; no noisy curve invented after a stopped gate.')
    path=args.output/filename;fig.savefig(path,dpi=180);plt.close(fig)
    metadata.update(plot=filename,source_run=str(args.run.resolve()))
    if args.contrast and results_path.exists():
        fig,ax=plt.subplots(figsize=(8,4.8))
        estimates=np.array([r['comparisons']['policy_contrast']['mean'] for r in rows])
        intervals=np.array([r['comparisons']['policy_contrast']['interval95'] for r in rows])
        ax.vlines(sigma,intervals[:,0],intervals[:,1],color='#6a3d9a',lw=1.6)
        ax.plot(sigma,estimates,'o-',color='#6a3d9a',label='Paired policy contrast')
        for j in unresolved:ax.plot(sigma[j],estimates[j],'kx',markersize=11,mew=2)
        ax.axhline(0,color='black',ls='--',lw=1)
        ax.set_xlabel(r'Absolute scalar code-noise standard deviation $\sigma$')
        ax.set_ylabel(r'$\Delta_{\rm calibrated}-\Delta_{\rm frozen}$ (weighted MSE)')
        ax.set_title('Relative-risk policy effect on the fixed learned-activation pair')
        ax.grid(alpha=.2)
        caption=(f'Operational channels {channels}; pointwise paired-image 95% percentile bootstrap conditional on fitted models. '
                 'Positive contrast shifts the relative comparison toward mono. '
                 'A resolved contrast does not resolve either individual risk ordering or establish a reversal.')
        if unresolved:caption+=' Black × marks unresolved calibration.'
        if len(rows)!=5:caption+=' Saved run is incomplete.'
        fig.text(.08,.025,'\n'.join(textwrap.wrap(caption,110)),fontsize=8,ha='left',va='bottom')
        fig.subplots_adjust(left=.12,right=.97,top=.89,bottom=.23)
        contrast_path=args.output/'vision_policy_contrast.png';fig.savefig(contrast_path,dpi=180);plt.close(fig)
        metadata['contrast_plot']=contrast_path.name
        print(str(contrast_path.resolve()))
    (args.output/'plot_status.json').write_text(json.dumps(metadata,indent=2))
    print(str(path.resolve()))

if __name__=='__main__':main()
