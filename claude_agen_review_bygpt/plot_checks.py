"""Plot existing independent audit outputs; does not rerun experiments."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent
audit=json.loads((HERE/'results.json').read_text())
follow=json.loads((HERE/'followup_results.json').read_text())
fig,axs=plt.subplots(1,2,figsize=(10,3.8),layout='constrained')
for m in [2,3,4]:
    rows=[r for r in audit['compression_independent']['rows'] if r['m']==m and r['eta']==.5 and r['sign']==-1]
    x=[r['p']-r['threshold'] for r in rows]
    axs[0].plot(x,[r['curvature_pred'] for r in rows],'-',label=f'm={m}, local formula')
    axs[0].scatter(x,[r['curvature_exact'] for r in rows],marker='x',s=60)
axs[0].axhline(0,color='black',lw=.7)
axs[0].set(xlabel='p minus predicted local threshold',ylabel='One-partner profiled curvature',title='Local compression checks: formula vs exact loss')
axs[0].legend(fontsize=8)
rows=[r for r in follow['noise_resolution'] if r['sigma']==.003]
rows=sorted(rows,key=lambda r:r['eps'])
axs[1].plot([r['eps'] for r in rows],[float(r['gain_55digit']) for r in rows],'o-',label='Independent geometry, 55-digit loss')
saved=audit['noise_independent']['transition_checks'][1]['saved_bracket']
axs[1].axvspan(*saved,color='red',alpha=.2,label='Archived crossing bracket')
axs[1].axhline(0,color='black',lw=.7)
axs[1].set(xlabel='epsilon = clean threshold minus p',ylabel='Mono loss minus sharing loss',title='Noise sigma=0.003: archived bracket fails')
axs[1].ticklabel_format(axis='y',style='sci',scilimits=(0,0))
axs[1].legend(fontsize=8)
fig.savefig(HERE/'verification_checks.png',dpi=160)
print(HERE/'verification_checks.png')
