"""Read saved map and numerical brackets; never generate or smooth results."""
from pathlib import Path
import csv,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'frozen_run_v1/results.json').read_text())
with (HERE/'frozen_run_v1/population_map.csv').open() as f:rows=list(csv.DictReader(f))
fig,axes=plt.subplots(2,3,figsize=(11,6))
for axis,case in zip(axes.flat,data['cases']):
    points=[r for r in rows if r['epsilon']==case['epsilon'] and float(r['sigma'])>0]
    eps=float(case['epsilon'])
    axis.plot([float(r['sigma'])/eps**1.5 for r in points],[float(r['delta'])/eps**3 for r in points],lw=1)
    axis.axhline(0,color='black',lw=.6)
    axis.axvline(float(data['constants']['frozen_coefficient']),color='orange',ls='--',label='Asymptotic first crossing')
    axis.set(xscale='log',xlim=(.2,60),ylim=(-2,2),title=f"epsilon={case['epsilon']}; detected brackets={len(case['detected_crossings'])}",
             xlabel='sigma / epsilon^(3/2)',ylabel='Risk difference / epsilon^3')
fig.suptitle('Frozen clean biases: sharing minus mono population MSE (positive favors mono)')
fig.tight_layout()
fig.savefig(HERE/'frozen_phase_map.png',dpi=180)
fig,ax=plt.subplots(figsize=(6,4))
cases=[c for c in data['cases'] if c['detected_crossings']]
ax.plot([float(c['epsilon']) for c in cases],[float(c['detected_crossings'][0]['sigma_over_epsilon_3_2']) for c in cases],'o-',label='First detected numerical crossing')
ax.axhline(float(data['constants']['frozen_coefficient']),ls='--',color='black',label='Derived asymptotic coefficient')
ax.set(xlabel='Distance below clean storage transition',ylabel='sigma crossing / epsilon^(3/2)')
ax.legend(fontsize=8);fig.tight_layout();fig.savefig(HERE/'frozen_boundary_scaling.png',dpi=180)
