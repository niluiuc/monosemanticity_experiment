"""Saved sign-certified numerical brackets; no fits or invented point precision."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
rows=json.loads((HERE/'calibrated_boundary_run_v1/results.json').read_text())
coefficient=float(json.loads((HERE/'calibrated_run_v1/settings.json').read_text())['coefficient'])
x=[float(r['epsilon']) for r in rows]
lo=[float(r['scaled_lower']) for r in rows];hi=[float(r['scaled_upper']) for r in rows]
mid=[(a+b)/2 for a,b in zip(lo,hi)]
fig,ax=plt.subplots(figsize=(7,4))
ax.errorbar(x,mid,yerr=[[m-a for m,a in zip(mid,lo)],[b-m for m,b in zip(mid,hi)]],fmt='o',capsize=4,label='Saved numerical crossing brackets')
ax.axhline(coefficient,ls='--',color='black',label='Derived calibrated coefficient')
ax.set(xlabel='Distance below clean storage transition',ylabel='sigma crossing / epsilon^(3/2)')
ax.legend(fontsize=9);fig.tight_layout();fig.savefig(HERE/'calibrated_boundary_scaling.png',dpi=180)
