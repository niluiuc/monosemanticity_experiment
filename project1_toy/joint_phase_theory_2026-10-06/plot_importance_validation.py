"""Plot derived critical coefficients and all saved finite frozen crossings."""
from pathlib import Path
import json
import mpmath as mp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

H=Path(__file__).resolve().parent;mp.mp.dps=40
phi=lambda z:mp.exp(-z*z/2)/mp.sqrt(2*mp.pi)
Phi=lambda z:mp.erfc(-z/mp.sqrt(2))/2
etas=np.linspace(.48,.52,81);frozen=[];calibrated=[]
for raw in etas:
    eta=mp.mpf(str(raw));s=mp.sqrt(1+2*eta-3*eta*eta)
    p=2*eta/(1+eta+s);q=1-p;D=1-p+p*p;C=s**3/(27*D*p*q)
    z=mp.findroot(lambda z:p*z+q*(z*Phi(z)+phi(z)),-.4)
    v=p*(1+z*z)+q*((1+z*z)*Phi(z)+z*phi(z))
    frozen.append(float(mp.sqrt(C/(q*(1-2*p)/2))))
    calibrated.append(float(mp.sqrt(C/(D-v))))
fig,ax=plt.subplots(figsize=(8.2,5.1),layout='constrained')
ax.plot(etas,frozen,color='#174e87',label='Derived frozen-bias limit')
ax.plot(etas,calibrated,color='#b94819',label='Derived calibrated limit')
ax.fill_between(etas,calibrated,frozen,color='#eecc8c',alpha=.32,
    label='Asymptotic policy-dependent ordering')
cases=json.loads((H/'importance_run_v1/results.json').read_text())['cases']
control=json.loads((H/'frozen_run_v1/results.json').read_text())['cases']
for epsilon,marker,color in [('.005','o','#1c83b5'),('.001','s','#264f6b')]:
    rows=[]
    for c in cases:
        if c['epsilon']==epsilon and 'crossing' in c['frozen']:
            cr=c['frozen']['crossing'];rows.append((float(c['eta']),float(cr['scaled_lower']),float(cr['scaled_upper'])))
    for c in control:
        if c['epsilon']==epsilon and c['detected_crossings']:
            cr=c['detected_crossings'][0];scale=float(epsilon)**1.5
            rows.append((.5,float(cr['lower'])/scale,float(cr['upper'])/scale))
    rows.sort()
    x=np.array([r[0] for r in rows]);lo=np.array([r[1] for r in rows]);hi=np.array([r[2] for r in rows]);mid=(lo+hi)/2
    ax.errorbar(x,mid,yerr=[mid-lo,hi-mid],fmt=marker,color=color,capsize=3,
        label=f'Saved frozen brackets, epsilon={epsilon}')
ax.set(xlabel='Relative feature importance eta',ylabel=r'Critical noise / $\epsilon^{3/2}$',
    title='Importance-dependent critical boundary in the proved two-feature family')
ax.grid(alpha=.18);ax.legend(fontsize=8.5,loc='upper left')
fig.savefig(H/'importance_policy_phase.png',dpi=180)
print('Saved importance_policy_phase.png; shaded region is an asymptotic prediction, not a finite-noise map.')
