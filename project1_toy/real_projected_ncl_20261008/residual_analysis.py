"""Fixed saved-record decomposition; no new forwards or outcome fitting."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

base=Path(__file__).parent; out=base/'outputs/gate_diagnostic_v1'
rows=[]
for method in ('CL','NCL'):
    with np.load(out/(method+'_logits.npz')) as a:
        actual=a['actual_logits'].astype(float); clean=a['clean_logits'].astype(float)
        labels=a['labels']; increment=actual-clean
        increment-=increment.mean(-1,keepdims=True)
        for key in ('full_affine_logits','backbone_affine_logits'):
            approx=a[key].astype(float); r=actual-approx; r-=r.mean(-1,keepdims=True)
            drift=r.mean(1,keepdims=True); centered=r-drift
            total=float(np.mean(r*r)); drift_energy=float(np.mean(drift*drift)); fluctuation=float(np.mean(centered*centered))
            assert abs(total-drift_energy-fluctuation)<1e-10*max(total,1)
            # The empirical direction average is descriptive, not a population expectation.
            rows.append(dict(method=method,approximation=key,total_residual_energy=total,
                empirical_direction_mean_energy=drift_energy,centered_residual_energy=fluctuation,
                empirical_mean_energy_fraction=drift_energy/total,
                relative_rms=float(np.sqrt(total/np.mean(increment*increment)))))
result=dict(rows=rows,directions_per_image=32,sigma=.04,
    status='Post-outcome descriptive decomposition of saved validation logits',
    identity='mean ||r||^2 = mean ||direction_mean(r)||^2 + mean ||r-direction_mean(r)||^2',
    limitations='Exact finite-sample identity. The direction mean contains sampling variation; it is not an unbiased estimate of population drift energy. No causal attribution or crossing prediction follows.')
(out/'residual_decomposition.json').write_text(json.dumps(result,indent=2))
fig,ax=plt.subplots(figsize=(7,4)); x=np.arange(len(rows)); fractions=[r['empirical_mean_energy_fraction'] for r in rows]
ax.bar(x,fractions,label='Empirical direction mean',color='#4679a7')
ax.bar(x,1-np.array(fractions),bottom=fractions,label='Direction-centered residual',color='#d08b4b')
ax.set_xticks(x,['CL\nFull affine','CL\nAffine CNN +\nnonlinear projector','NCL\nFull affine','NCL\nAffine CNN +\nnonlinear projector'])
ax.set_ylabel('Fraction of squared logit residual'); ax.set_ylim(0,1)
ax.set_title('Why the local approximation fails at pixel noise σ = 0.04')
ax.legend(loc='upper center',bbox_to_anchor=(.5,-.23),ncol=2,frameon=False)
fig.text(.5,.01,'Saved validation records, 32 directions/image; empirical decomposition, not causal inference.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.10,1,1)); fig.savefig(out/'residual_decomposition.png',dpi=160); plt.close(fig)
print(json.dumps(result,indent=2))
