"""All two declared endpoint cases; no filtering or fitted trend."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent
cases=json.loads((H/'endpoint_policy_run_v1/results.json').read_text())['cases']
x=np.arange(len(cases));frozen=np.array([float(c['frozen_delta_over_epsilon_cubed']) for c in cases])
lower=np.array([float(c['calibrated_delta_lower'])/float(c['epsilon'])**3 for c in cases])
upper=np.array([float(c['calibrated_delta_upper'])/float(c['epsilon'])**3 for c in cases]);mid=(lower+upper)/2
fig,ax=plt.subplots(figsize=(7.6,4.8),layout='constrained')
ax.axhline(0,color='black',linewidth=1)
ax.axhline(-16/81,color='#174e87',linestyle='--',alpha=.65,label='Derived frozen limit: -16/81')
ax.axhline(16/27,color='#b94819',linestyle='--',alpha=.65,label='Derived calibrated limit: 16/27')
ax.scatter(x-.08,frozen,color='#174e87',s=65,label='Frozen clean biases')
ax.errorbar(x+.08,mid,yerr=[mid-lower,upper-mid],fmt='s',color='#b94819',capsize=5,
    label='Symmetric calibrated numerical brackets')
ax.set_xticks(x,[c['epsilon'] for c in cases]);ax.set(xlabel='Distance below the clean storage transition, epsilon',
    ylabel=r'$(R_{\rm share}-R_{\rm mono})/\epsilon^3$',title='Same clean-selected encoder and noise; opposite decoder-policy orderings')
ax.text(.02,.42,'Below zero: sharing wins\nAbove zero: mono wins',transform=ax.transAxes,fontsize=10)
ax.set_xlim(-.5,len(cases)-.5);ax.grid(axis='y',alpha=.18);ax.legend(fontsize=8.2,loc='center right')
fig.savefig(H/'endpoint_policy_contrast.png',dpi=180)
print('Saved both cases; error bars are numerical loss-gap bounds, not confidence intervals. No convergence trend is fitted.')
