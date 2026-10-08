import shutil
from pathlib import Path
base=Path(__file__).parent; root=base.resolve().parents[1]
section=r'''
\section{Which decisions account for the native reversal?}
\paragraph{Question and exact identity.}
Use only the saved fixed native TEST decisions to separate new errors from recoveries. This is post-outcome descriptive analysis, not another model run or boundary forecast. For model $m$, let $e_m(0),e_m(\sigma)\in\{0,1\}$ indicate incorrect classification of the same labeled image before and after its sampled corruption. Pointwise,
\[
e_m(\sigma)=e_m(0)+(1-e_m(0))e_m(\sigma)-e_m(0)(1-e_m(\sigma)).
\]
Taking expectations over the specified images and noise directions gives
\[
R_m(\sigma)=R_m(0)+L_m(\sigma)-H_m(\sigma),
\]
where $L_m$ is the unconditional probability of a new error from an initially correct decision, and $H_m$ the unconditional probability of recovering an initially wrong decision. Subtracting CL from NCL yields
\[
\Delta(\sigma)=\Delta(0)+[L_{\rm NCL}-L_{\rm CL}]-[H_{\rm NCL}-H_{\rm CL}].
\]
Consequently, NCL wins exactly when the observed advantage in these transitions exceeds its clean deficit. This is standard event accounting, not a predictive law: the finite-noise transition probabilities on the right remain unknown before measurement.

\paragraph{Observed components at $\sigma=0.12$.}
The clean deficit is $+1.6500$ points. NCL has $2.2667$ points fewer new errors and $0.6067$ points more recoveries, giving $1.6500-2.2667-0.6067=-1.2233$ points overall. The unconditional new-error counts have different clean starting populations, so their difference alone does not establish greater conditional robustness.

\paragraph{Common clean-correct group.}
Partition images by the two clean decisions: both correct (4,502), CL only correct (985), NCL only correct (820), and both wrong (3,693). Each group's contribution equals its fraction times its conditional NCL-minus-CL error difference; these four contributions sum exactly to the total. On the common clean-correct group, the unconditional contribution at $0.04$ is $+1.6433$ points, favoring CL, whereas at $0.12$ it is $-0.7867$ points, favoring NCL. At $0.12$, CL-only, NCL-only and both-wrong groups contribute $0$, $-0.1867$ and $-0.2500$ points respectively. The reversal is therefore also present within a common clean-correct population; it is not merely an artifact of NCL starting with fewer correct examples. These subgroup numbers are descriptive sample averages, without a new subgroup confidence or causal claim.

\begin{figure}[htbp]\centering
\includegraphics[width=\textwidth]{figures/native_transition_accounting_20261008.png}
\caption{Left: exact clean-gap, new-error and recovery accounting. Right: unconditional contributions of the four clean correctness groups. The horizontal axis is pixel-noise standard deviation; the vertical axis is NCL-minus-CL error contribution in points. Connecting lines do not certify intermediate levels. No geometry attribution or successful crossing prediction follows from this accounting.}
\end{figure}
'''
(base/'transition_notes.tex').write_text(section,encoding='utf-8')
shutil.copy2(base/'outputs/test_run_v1/transition_accounting.png',root/'research_notes/figures/native_transition_accounting_20261008.png')
p=root/'research_notes/volume2.tex'; text=p.read_text(encoding='utf-8')
start='% BEGIN NATIVE TRANSITION ACCOUNTING'; end='% END NATIVE TRANSITION ACCOUNTING'; block=start+'\n'+section+'\n'+end+'\n'
if start in text:
    a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+block.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2'); text=text[:a]+block+'\n'+text[a:]
p.write_text(text,encoding='utf-8')
record='''

## Saved native decision accounting

- No new forwards or fitting. Exact clean-to-noisy error accounting reproduces the saved curve at every fixed level.
- At .12, clean deficit +1.6500 points, new-error difference -2.2667 and recovery contribution -0.6067 sum to -1.2233. Different clean populations make the unconditional loss difference insufficient by itself for conditional robustness.
- Among the same 4,502 images both classifiers get right clean, CL has lower sampled error at .04, but NCL has lower sampled error at .12. Their unconditional contributions are +1.6433 and -.7867 points. This is descriptive evidence that the native reversal also occurs within a common initially correct population, not a geometry attribution or boundary prediction.
- The standard exact identity and its derivation, numbers, limits and plot are integrated in Section 8.39. Stop this accounting at the saved fixed grid; no new subgroup search or significance claim.
'''
for p in (base/'RUN_STATUS.md',root/'project1_toy/plan.md'):
    t=p.read_text(encoding='utf-8')
    if '## Saved native decision accounting' not in t: p.write_text(t+record,encoding='utf-8')
print('Integrated exact decision accounting and limits.')
