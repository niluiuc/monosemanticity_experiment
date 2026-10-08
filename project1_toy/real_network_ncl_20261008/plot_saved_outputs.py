"""Plot saved results only; never run a model or select observations."""
import argparse,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

p=argparse.ArgumentParser(); p.add_argument('--root',type=Path,required=True); root=p.parse_args().root
clean=json.loads((root/'clean_run_v1/results.json').read_text())
out=root/'figures'; out.mkdir(exist_ok=True)
fig,axes=plt.subplots(1,2,figsize=(9,3.8))
fields=[('delta_error','error_difference_ci95','Classification error: NCL − CL'),
        ('delta_consistency','consistency_difference_ci95','Class consistency: NCL − CL')]
for ax,(field,interval,title) in zip(axes,fields):
    v=100*clean[field]; lo,hi=100*np.array(clean[interval])
    ax.plot([lo,hi],[0,0],color='#2563a6',linewidth=3); ax.scatter([v],[0],color='#2563a6',zorder=3)
    ax.axvline(0,color='black',linewidth=.8); ax.set_yticks([])
    ax.set_xlabel('Difference (percentage points)'); ax.set_title(title)
    ax.text(.5,.14,f'{v:.4f}; 95% interval [{lo:.4f}, {hi:.4f}]',transform=ax.transAxes,ha='center',fontsize=9)
fig.suptitle('Clean prerequisite decision: '+('PASS' if clean['clean_gates_passed'] else 'STOP'))
fig.text(.5,.01,'Paired image bootstrap, conditional on one fixed checkpoint/probe pair; class consistency is a proxy.',ha='center',fontsize=8)
fig.tight_layout(rect=[0,.04,1,.93]); fig.savefig(out/'clean_gates.png',dpi=170); plt.close(fig)
test=root/'test_run_v1/results.json'
if test.exists():
    data=json.loads(test.read_text()); pred=json.loads((root/'prediction_run_v1/prediction.json').read_text())
    x=np.array(data['sigma_grid']); fig,axes=plt.subplots(1,2,figsize=(10,4))
    for method in ('CL','NCL'): axes[0].plot(x,100*np.array(data[method+'_error']),'o-',label=method)
    axes[0].set_ylabel('Classification error (%)'); axes[0].legend()
    axes[1].fill_between(x,100*np.array(data['simultaneous_lower']),100*np.array(data['simultaneous_upper']),alpha=.2,label='Simultaneous test bands')
    axes[1].plot(x,100*np.array(data['delta_NCL_minus_CL']),'o-',label='Observed TEST')
    axes[1].plot(x,100*np.array(pred['delta_error_prediction']),'--',label='Frozen validation prediction')
    axes[1].axhline(0,color='black',linewidth=.8); axes[1].set_ylabel('Error difference: NCL − CL (points)'); axes[1].legend(fontsize=8)
    for ax in axes: ax.set_xlabel('Raw-pixel Gaussian noise standard deviation σ')
    fig.suptitle('Native classifier corruption test: '+('resolved reversal' if data['resolved_reversal'] else 'no resolved reversal'))
    fig.text(.5,.01,'One released checkpoint pair; unclipped input noise; no causal isolation of monosemanticity.',ha='center',fontsize=8)
    fig.tight_layout(rect=[0,.04,1,.93]); fig.savefig(out/'native_corruption_curve.png',dpi=170); plt.close(fig)
print('Plots generated only from saved results:',out)
