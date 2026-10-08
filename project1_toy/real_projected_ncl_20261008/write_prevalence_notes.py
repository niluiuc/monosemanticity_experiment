import json,shutil
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).parent; root=base.resolve().parents[1]; out=base/'outputs/prevalence_check_v1'
d=json.loads((out/'results.json').read_text())
fig,ax=plt.subplots(figsize=(6.5,3.6)); x=np.arange(2)
for j,m in enumerate(('CL','NCL')):
    ax.bar(x+(j-.5)*.30,[d['methods'][m]['original_purity'],d['methods'][m]['matched_purity']],width=.30,label=m)
ax.set_xticks(x,['Original activity proxy','Matched 7% rank-selection budget'])
ax.set_ylabel('Mean majority-class fraction'); ax.set_title('Class-purity contrast under one prevalence control'); ax.legend()
fig.text(.5,.01,'NCL has 127 zero cutoffs; rank selection is not equal positive firing rates.',ha='center',fontsize=8)
fig.tight_layout(rect=(0,.045,1,1)); fig.savefig(out/'prevalence_control.png',dpi=160); plt.close(fig)
shutil.copy2(out/'prevalence_control.png',root/'research_notes/figures/native_prevalence_control_20261008.png')
section=r'''
\section{One prevalence control for the consistency proxy}
\paragraph{Question and fixed measurement.}
The original class-consistency proxy depends on activation frequency as well as class selectivity. Use cached features from the same 5,000 validation images to test one rank-based prevalence control; no TEST images, new training or corruption forwards are involved. For each model, normalize each image's projected feature vector as in the original score, take absolute coordinate values, and exclude coordinates inactive on every validation image. Compute NCL's original mean activity fraction with threshold $10^{-5}$ across its nondead coordinates, without labels: 0.07004655. Fix $k=350$, and select the top $k$ values for every nondead coordinate of both models. Break ties by the same seeded label-independent image permutation, avoiding the validation array's class-sorted order.

\paragraph{Definition and limits.}
For selected sets $A_j$, the score is
\[
S=\frac1J\sum_{j=1}^J\frac{\max_c\sum_{i\in A_j}\mathbf1\{y_i=c\}}{|A_j|},\qquad |A_j|=350.
\]
This is a majority-class purity proxy, not a definition of a semantic concept. Match selected counts rather than presume both models have equal positive firing rates. In fact 127 of NCL's 232 nondead coordinates have zero cutoffs, requiring selection of some tied zeros; CL's 256 coordinates have no cutoff ties. Report this rather than calling the procedure perfect activation matching.

\paragraph{Observed outcome and stopping decision.}
Original scores are 0.01000119 (CL) and 0.11470436 (NCL). Rank-controlled scores are 0.06608259 and 0.08959360, with difference 0.02351101. A paired within-class bootstrap with 200 fixed draws gives conditional interval $[0.02009444,0.02587170]$. This bootstrap conditions on the selected ranks and $k$; it does not include uncertainty from their selection. Independent counting reproduces the scores, all draws, intervals and equal selected counts. A smaller positive contrast survives this one control. Do not interpret its reduction as a causal percentage explained by sparsity, claim ground-truth monosemanticity, or replace the registered original metric. Stop at this one selection budget.

\begin{figure}[htbp]\centering
\includegraphics[width=.95\textwidth]{figures/native_prevalence_control_20261008.png}
\caption{Original and rank-controlled majority-class proxies. Equal rank-selection counts retain a smaller NCL advantage. Tied zero cutoffs prevent interpreting this as equal actual firing rates. It is a post-outcome measurement sensitivity check, not a causal intervention.}
\end{figure}
'''
(base/'prevalence_notes.tex').write_text(section,encoding='utf-8')
p=root/'research_notes/volume2.tex'; t=p.read_text(encoding='utf-8')
start='% BEGIN NATIVE PREVALENCE CONTROL'; end='% END NATIVE PREVALENCE CONTROL'; block=start+'\n'+section+'\n'+end+'\n'
if start in t:
    a=t.index(start); b=t.index(end,a)+len(end); t=t[:a]+block.rstrip()+t[b:]
else:
    a=t.index('\\chapter{Project 2'); t=t[:a]+block+'\n'+t[a:]
common=r'''
\paragraph{Common class-shift prerequisite and stop.}
Before extending to a global class-bias calibration control, decompose the saved centered residual into its mean across images and directions plus its remaining part. A common class-only shift accounts for 0.120951 of CL residual energy and 0.039828 of NCL residual energy at $\sigma=0.04$. Neither exceeds the predeclared 0.25 screening threshold; the proposed calibration experiment is therefore not run. This is a heuristic stopping decision for this specific control, not proof that class-bias calibration cannot affect error. The much larger per-image direction-mean fractions do not establish a common shift removable by one global class bias.
'''
marker='% END NATIVE GATE DIAGNOSTIC'
if '\\paragraph{Common class-shift prerequisite and stop.}' not in t: t=t.replace(marker,common+'\n'+marker)
p.write_text(t,encoding='utf-8')
record='''

## Matched-rank prevalence control and class-bias prerequisite

- Physics CPU job 11212722 completed. At one declared 7% selection budget, CL/NCL purity is .06608259/.08959360. Difference .02351101, conditional interval [.02009444,.02587170]. Independent selection/count/bootstrap verification passes.
- NCL has 127 zero cutoffs among 232 nondead coordinates. This is equal rank-selection count, not equal positive firing rates. It is a sensitivity control on a class proxy, not ground-truth monosemanticity or causal attribution. Stop at one budget.
- Saved-record common-drift check finds 12.095%/3.983% of affine residual energy in a common class-only shift for CL/NCL, below the declared 25% criterion. No global-bias calibration experiment is run. This does not prove calibration irrelevant.
- Outcomes and measurement definition are integrated in Section 8.40; the class-bias stopping decision is in Section 8.37. No new novelty claim or successful native boundary prediction.
'''
for p in (base/'RUN_STATUS.md',root/'project1_toy/plan.md'):
    t=p.read_text(encoding='utf-8')
    if '## Matched-rank prevalence control and class-bias prerequisite' not in t: p.write_text(t+record,encoding='utf-8')
print('Integrated bounded prevalence control and stopped class-bias path.')
