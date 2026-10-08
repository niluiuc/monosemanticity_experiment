import json,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).parent; root=base.resolve().parents[1]; out=base/'outputs/probe_replication_v1'
d=json.loads((out/'results.json').read_text()); points=np.array(d['delta_NCL_minus_CL'])*100
lo=np.array(d['simultaneous_lower'])*100; hi=np.array(d['simultaneous_upper'])*100
fig,ax=plt.subplots(figsize=(6.5,4)); x=np.arange(2)
for j,seed in enumerate(d['seeds']):
    xx=x+(j-.5)*.10; ax.errorbar(xx,points[j],yerr=[points[j]-lo[j],hi[j]-points[j]],fmt='o',capsize=4,label=str(seed))
ax.axhline(0,color='black',lw=.8); ax.set_xticks(x,['Clean','Gaussian pixel noise σ = 0.12'])
ax.set_ylabel('Error difference: NCL − CL (percentage points)'); ax.set_title('Native ordering reversal survives two additional probe seeds')
ax.legend(title='Probe seed'); fig.text(.5,.015,'Same checkpoint pair and reused images; conditional simultaneous intervals.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.05,1,1)); fig.savefig(out/'probe_stability.png',dpi=160); plt.close(fig)
shutil.copy2(out/'probe_stability.png',root/'research_notes/figures/native_probe_stability_20261008.png')
section=r'''
\section{Bounded probe-seed reliability check}
\paragraph{Motivation and declared scope.}
A native crossover from a single fitted probe might be sensitive to probe initialization and training order. After seeing the original TEST curve, predeclare two additional probe seeds, 20261018 and 20261019, and only two evaluation conditions: clean and the previously observed reversal point $\sigma=0.12$. Retain the same frozen backbone/projector checkpoints, training/validation split, training-only feature standardization, optimizer and 50 epochs. This is a bounded post-outcome reliability check, not independent confirmation on unseen models or unseen images. Do not search additional seeds, training settings or noise strengths if it fails.

\paragraph{Protocol and uncertainty.}
Evaluate all 10,000 original TEST images, with three Gaussian directions per image, new fixed noise seed 20261020 shared across both methods and both probe seeds. Save probe weights/histories, validation logits and per-image TEST errors/losses. Bootstrap paired images within classes with 2,000 draws, grouping noise replicates. Bonferroni intervals cover the four seed-by-condition comparisons. The stopping criterion requires resolved CL clean advantage and resolved NCL advantage at $0.12$ for each seed. These intervals remain conditional on the pretrained checkpoints and fitted probes; two probe seeds are not backbone-training replication.

\begin{center}\small
\begin{tabular}{rrrl}\hline
Probe seed & $\sigma$ & NCL minus CL (points) & Simultaneous interval\\\hline
20261018 & 0 & $+1.6200$ & $[+0.6500,+2.6700]$\\
20261018 & .12 & $-1.1933$ & $[-1.7867,-0.6683]$\\
20261019 & 0 & $+1.5100$ & $[+0.5099,+2.6151]$\\
20261019 & .12 & $-1.1567$ & $[-1.7534,-0.6131]$\\\hline
\end{tabular}\end{center}

\paragraph{Outcome and limits.}
Both new probe seeds pass. Independent recomputation verifies validation argmax decisions, TEST risk differences, every one of the 2,000 saved bootstrap draws, simultaneous intervals and stopping decision. The native ordering reversal is thus stable under these two specified probe-training variations. It remains a comparison of the same two pretrained checkpoints on the same image set. This result does not establish a new crossing formula, robustness across backbone training seeds, or monosemanticity as the isolated cause. Stop this seed check at the declared two probes.

\begin{figure}[htbp]\centering
\includegraphics[width=.95\textwidth]{figures/native_probe_stability_20261008.png}
\caption{NCL-minus-CL classification-error differences for two additional probes. Positive favors CL; negative favors NCL. Both clean and corrupted comparisons are resolved within the stated conditional uncertainty. This is post-outcome probe-seed reliability on reused images and fixed pretrained networks.}
\end{figure}
'''
(base/'probe_replication_notes.tex').write_text(section,encoding='utf-8')
p=root/'research_notes/volume2.tex'; text=p.read_text(encoding='utf-8')
start='% BEGIN NATIVE PROBE REPLICATION'; end='% END NATIVE PROBE REPLICATION'; block=start+'\n'+section+'\n'+end+'\n'
if start in text:
    a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+block.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2'); text=text[:a]+block+'\n'+text[a:]
p.write_text(text,encoding='utf-8')
record='''

## Two additional probe seeds completed and stopped

- Physics CPU job 11212673 completed. Fixed seeds 20261018/20261019 both reproduce resolved CL-clean/NCL-corrupted ordering on the same native networks. Clean differences +.0162/+.0151; sigma .12 differences -.0119333333/-.0115666667, with all four simultaneous conditional intervals excluding zero.
- Independent saved-record verification reproduces validation argmax/errors, TEST differences, all 2,000 bootstrap draws, intervals and decision. Protocol, weights, histories and raw outcomes are retained in outputs/probe_replication_v1.
- This is a post-outcome reliability check on reused TEST images and fixed backbone checkpoints, not a blinded boundary prediction or backbone-seed replication. Stop at two additional probes; do not search more seeds/noise points.
- Methods, outcomes, limits and plot are integrated in Section 8.38 of the derivations volume and its local editable source.
'''
for p in (base/'RUN_STATUS.md',root/'project1_toy/plan.md'):
    t=p.read_text(encoding='utf-8')
    if '## Two additional probe seeds completed and stopped' not in t: p.write_text(t+record,encoding='utf-8')
print('Integrated probe reliability results, with limits.')
