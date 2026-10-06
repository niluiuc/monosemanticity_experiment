"""Plot saved values only. No estimation, simulation or fitted exponents."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
d=Path(__file__).resolve().parent
r=json.loads((d/'verification_results.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(9,3.5))
e=[float(v['epsilon']) for v in r['rows']]
for axis,key,limit,label in [
    (ax[0],'k_over_epsilon','K','k / epsilon'),
    (ax[1],'clean_gain_over_epsilon_cubed','C','Clean gain / epsilon cubed')]:
    axis.plot(e,[float(v[key]) for v in r['rows']],'o-',label='Exact local stationary solution')
    axis.axhline(float(r[limit]),ls='--',color='black',label='Derived limit')
    axis.set(xlabel='Distance below storage transition',ylabel=label)
ax[0].legend(fontsize=8)
fig.tight_layout()
fig.savefig(d/'critical_constants_reproduced.png',dpi=180)
