"""Plot saved fixed-pair results only; no inference, fitting or new noise levels."""
from pathlib import Path
import json, argparse, textwrap
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=HERE/'plots_v1')
    args=parser.parse_args()
    run=HERE/'evaluation_run_v1';out=args.output;out.mkdir(exist_ok=False)
    if not (run/'results.json').exists():
        if not (run/'clean_selection.json').exists():
            (out/'status.json').write_text(json.dumps({'status':'Stopped before geometry fitting; no risk figure'}));return
        clean=json.loads((run/'clean_selection.json').read_text());fig,ax=plt.subplots(figsize=(8,4.8))
        for history in clean['histories']:
            ax.plot([r['angle'] for r in history['grid']],[r['loss'] for r in history['grid']],label=str(history['size'])+'-point grid')
        ax.axhline(clean['mono']['loss'],color='black',ls='--',label='Best coordinate-retaining mono')
        ax.set(xlabel='Encoder angle (radians)',ylabel='Training weighted reconstruction MSE',title='Fixed class-evidence pair: clean-selection gate')
        ax.legend();fig.tight_layout();fig.savefig(out/'head_clean_gate.png',dpi=170);return
    rows=json.loads((run/'results.json').read_text())['cases']
    sigma=[r['sigma'] for r in rows]
    for stem,keys,ylabel in [('head_risk',['delta_frozen','delta_calibrated'],'Test MSE: sharing minus mono'),('head_policy_contrast',['policy_contrast'],'Calibrated minus frozen risk difference')]:
        fig,ax=plt.subplots(figsize=(8,5))
        for key in keys:
            means=[r['comparisons'][key]['mean'] for r in rows]
            ci=np.array([r['comparisons'][key]['interval95'] for r in rows])
            line,=ax.plot(sigma,means,'o-',label=key.replace('_',' '));ax.vlines(sigma,ci[:,0],ci[:,1],colors=line.get_color())
        ax.axhline(0,color='black',ls='--',lw=1);ax.grid(alpha=.2);ax.legend()
        ax.set(xlabel='Absolute Gaussian scalar-code noise SD',ylabel=ylabel,title='Fixed tabby / golden-retriever evidence coordinates')
        text=('Rectified class logits, not validated monosemantic hidden features. '
              'Bars: pointwise paired-image 95% bootstrap, conditional on fitted models.\n'
              'Code noise is not image-input corruption; no full-network robustness claim.')
        fig.text(.08,.025,'\n'.join(textwrap.wrap(text.replace('\n',' '),108)),fontsize=8)
        fig.subplots_adjust(left=.15,right=.97,bottom=.22,top=.88)
        fig.savefig(out/(stem+'.png'),dpi=170);plt.close(fig)
    (out/'status.json').write_text(json.dumps({'source':'evaluation_run_v1/results.json','new_evaluations':0},indent=2))

if __name__=='__main__':main()
