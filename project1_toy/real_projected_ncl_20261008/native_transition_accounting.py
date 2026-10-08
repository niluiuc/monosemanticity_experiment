"""Exact accounting of saved clean/noisy decisions; no new model evaluations."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).parent; out=base/'outputs/test_run_v1'
record=json.loads((out/'results.json').read_text()); grid=np.array(record['sigma_grid'])
errors={m:np.load(out/(m+'_test_scores.npz'))['errors'] for m in ('CL','NCL')}
rates={}; rows=[]
for m,e in errors.items():
    original=e[:,:,0]; assert np.all(original==original[:,:1])
    losses=np.mean((~original[:,:,None]) & e,axis=(0,1))
    recovery=np.mean(original[:,:,None] & (~e),axis=(0,1))
    rates[m]=dict(clean_error=float(original.mean()),new_error_probability=losses.tolist(),recovery_probability=recovery.tolist())
    assert np.max(np.abs(original.mean()+losses-recovery-e.mean((0,1))))<1e-12
clean_delta=rates['NCL']['clean_error']-rates['CL']['clean_error']
loss_delta=np.array(rates['NCL']['new_error_probability'])-rates['CL']['new_error_probability']
recovery_delta=np.array(rates['NCL']['recovery_probability'])-rates['CL']['recovery_probability']
delta=clean_delta+loss_delta-recovery_delta
assert np.max(np.abs(delta-record['delta_NCL_minus_CL']))<1e-12
cl0=errors['CL'][:,0,0]; ncl0=errors['NCL'][:,0,0]
groups={'both_correct':~cl0 & ~ncl0,'CL_only_correct':~cl0 & ncl0,
    'NCL_only_correct':cl0 & ~ncl0,'both_wrong':cl0 & ncl0}
group_records={}; summed=np.zeros(len(grid))
for name,mask in groups.items():
    difference=errors['NCL'][mask].astype(float)-errors['CL'][mask].astype(float)
    contribution=difference.sum((0,1))/(len(cl0)*3); summed+=contribution
    group_records[name]=dict(images=int(mask.sum()),fraction=float(mask.mean()),
        conditional_delta=difference.mean((0,1)).tolist(),unconditional_contribution=contribution.tolist())
assert np.max(np.abs(summed-delta))<1e-12
result=dict(sigma_grid=grid.tolist(),methods=rates,clean_delta=clean_delta,
    new_error_delta=loss_delta.tolist(),recovery_delta=recovery_delta.tolist(),
    delta_NCL_minus_CL=delta.tolist(),clean_groups=group_records,
    status='Exact accounting of saved post-outcome decisions; descriptive only',
    limitations='No geometry attribution or predictive boundary. Rates average the fixed three noise directions and reused TEST images. Group contributions are unconditional; group-conditional rates alone cannot be added.')
(out/'transition_accounting.json').write_text(json.dumps(result,indent=2))
fig,axes=plt.subplots(1,2,figsize=(10,4))
axes[0].plot(grid,np.full_like(grid,clean_delta)*100,label='Clean gap')
axes[0].plot(grid,loss_delta*100,label='Difference in new errors')
axes[0].plot(grid,-recovery_delta*100,label='Minus difference in recoveries')
axes[0].plot(grid,delta*100,'k-o',label='Total difference',ms=3)
for name,g in group_records.items(): axes[1].plot(grid,np.array(g['unconditional_contribution'])*100,label=name.replace('_',' '))
for ax in axes:
    ax.axhline(0,color='gray',lw=.7); ax.set_xlabel('Raw-pixel Gaussian noise standard deviation'); ax.legend(fontsize=7)
axes[0].set_ylabel('NCL − CL error difference (percentage points)')
axes[0].set_title('Loss and recovery accounting'); axes[1].set_title('Contributions by clean correctness group')
fig.suptitle('Which decisions produce the native ordering reversal?')
fig.text(.5,.01,'Saved TEST decisions; exact descriptive accounting, not a crossing forecast or causal monosemanticity test.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.055,1,.95)); fig.savefig(out/'transition_accounting.png',dpi=160); plt.close(fig)
print(json.dumps(result,indent=2))
