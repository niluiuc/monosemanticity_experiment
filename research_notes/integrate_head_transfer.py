"""Integrate saved fixed head results without any fitting or altered outcomes."""
from pathlib import Path
import json, shutil

ROOT=Path(__file__).resolve().parent.parent
HERE=ROOT/'research_notes'
RUN=ROOT/'project1_toy/head_transfer_20261007/evaluation_run_v1'

def main():
    rows=json.loads((RUN/'results.json').read_text())['cases']
    audit=json.loads((ROOT/'project1_toy/head_transfer_20261007/independent_audit_v1/results.json').read_text())
    assert audit['passed'] and len(rows)==5
    table=[]
    for r in rows:
        a=r['comparisons']['delta_frozen'];b=r['comparisons']['delta_calibrated']
        table.append(f"{r['multiplier']:.2f} & {a['mean']:.8f} & {b['mean']:.8f} & [{b['interval95'][0]:.8f}, {b['interval95'][1]:.8f}]\\\\")
    content=r'''\section{Class-mapped evidence transfer: a resolved sharing advantage}
\label{sec:head-evidence-transfer}
This is a fixed operational transfer check, not a new theorem or a claim
that hidden ResNet features are monosemantic. Its question is whether
clean-trained scalar sharing of two independently named model-evidence
coordinates retains an advantage over coordinate retention under the
same Gaussian code corruption and decoder policies as the preceding pilot.
The rejected external SAE export did not provide the required concept and
model mapping; it was not used for this run.

\subsection{Prospective feature definition and controls}
The official frozen ImageNet ResNet18 \texttt{IMAGENET1K\_V1} head has
category 281 \texttt{tabby} and category 207 \texttt{golden retriever}.
These exact identifiers and names were verified before score inference.
The two targets are $\ReLU(\ell_{281})$ and $\ReLU(\ell_{207})$, where
$\ell$ is the genuine full classifier-head logit vector, not the previous
single-spatial-cell hidden activation. Raw logits for all 1,000 categories
are preserved. The zero threshold was fixed before outcomes and never changed.

Class supervision supplies a documented evidence association, not a faithful
causal concept decomposition. Raw logits have an additive softmax gauge:
shifting every logit leaves classification probabilities unchanged but
changes these rectified coordinates. The fixed checkpoint gives a
reproducible coordinate system; zeros do not certify concept absence.
CIFAR cat/dog labels do not certify the tabby or golden-retriever subclasses.
This test does not intervene on image inputs or measure full-network
adversarial robustness.

One seeded permutation (NumPy seed 20261007) of CIFAR10 training indices
provided disjoint 256 training, 256 calibration and 4,096 test images.
Official preprocessing and the previously verified checkpoint were reused;
no new model or SAE was trained. The complete forward pass took 304.453
seconds. A prespecified training-only association gate required AUROC
greater than .65 for both named scores against the respective coarse
cat/dog labels. The values .9049523 and .8081940 passed. Held-out
descriptive values were .8700349 and .8172911; test labels did not select
or fit any reconstruction.

Each nonnegative target was divided by its training RMS without centering.
Importances were $(1,2/3)$; scalar encoder squared energy was one;
decoding was tied ReLU with free biases. Mono could retain either
coordinate and its omitted coordinate's best constant error was included.
The existing exact empirical bias-interval profiler and 256/512 angle
grids, with one best-cell refinement per grid, selected the clean geometry.
This finite search is not a global-optimum certificate. Zero fractions
were .17578125 and .22265625, and coactivation was .640625.

Sharing's weights were approximately $(.83541738,.54961605)$; mono retained
the first coordinate. Training risks were .300735002 and .371810660,
respectively: sharing gain .071075658. Both refined losses agreed, both
refinements succeeded, and the original positive-gain/mixed-energy gates
passed. The selected same-sign geometry differs from the theorem's
opposite-sign Bernoulli critical branch.

\subsection{Held-out risks and the unfavorable transfer limit}
Encoders were frozen. Both models' zero-noise biases were fitted on the
calibration split and used for the frozen policy; the calibrated policy
refitted biases on that same split at each noise. Noise standard deviation
was the fixed multiplier times .7308510286, the square root of the mean
training variance of the two RMS-normalized targets. Both models received
the same independent scalar Gaussian code corruption. Conditional Gaussian moments,
scalar bias localization and their assumptions are those already derived
in this volume. No fitted scaling expression was introduced.

At zero noise, held-out risks were .333790049 (sharing) and .404845579
(mono). Their difference was $-.071055530$ with paired 95\% bootstrap
interval $[-.08898894,-.05201580]$. Thus the clean training advantage
transferred in this operational test. Every prescribed noisy difference
also favored sharing. The table reports total importance-weighted test MSE
for sharing minus mono; positive values would favor mono. The prespecified
primary outcome was the calibrated difference at multiplier .4; the frozen
difference and policy contrast at .4 were secondary, with other levels
retained as the fixed descriptive curve:
\begin{center}\small
\begin{tabular}{rrrr}
\toprule
Multiplier & Frozen difference & Calibrated difference & Calibrated 95\% interval\\
\midrule
TABLE_ROWS
\bottomrule
\end{tabular}\end{center}
All ten model/noise calibration comparisons met the unchanged numerical
gap target $10^{-7}$ with arithmetic slack $10^{-12}$. These are audited
floating-arithmetic bounds, not directed-rounding proof certificates.
Bootstrap intervals use 2,000 paired image resamples and are pointwise,
conditional on fitted models; they omit training/calibration uncertainty.

At multiplier .4, calibrated risks were .398223291 and .471492166,
respectively. There was \emph{no ordering reversal} on the fixed grid;
sharing's point advantage was slightly larger than at zero noise.
This does not reproduce a fragile sharing phase or the critical exponent.
It is evidence that clean benefits of packing named evidence coordinates
can persist under this declared corruption, preventing a universal
interpretation that monosemantic retention must win whenever noise is added.
\begin{figure}[htbp]\centering
\includegraphics[width=.96\linewidth]{figures/project1_head_risk.png}
\caption{Fixed class-evidence reconstruction comparison. Negative risk
differences favor sharing. Pointwise conditional intervals remain below
zero; this is a one-pair operational result, not a real-model phase boundary.}
\end{figure}

\subsection{Calibration contrast, independent audit and stop}
The contrast $\Delta_{\rm calibrated}-\Delta_{\rm frozen}$ was negative
at multipliers .05 and .10 with intervals below zero, unresolved at .20,
and positive at .40: .000617314 with interval
$[.000346820,.000899737]$. Calibration therefore helped sharing relatively
more at the lowest positive levels and mono relatively more at the largest
level. It never changed the winner. At .40, both models' held-out risks
improved under calibration; improvements were .002236486 for sharing
and .002853800 for mono.
\begin{figure}[htbp]\centering
\includegraphics[width=.96\linewidth]{figures/project1_head_policy_contrast.png}
\caption{Saved decoder-policy contrast. The .20 interval includes zero.
A positive contrast favors mono relative to frozen evaluation, but does
not imply that mono's total reconstruction risk is lower.}
\end{figure}

Independent checks verified 9 extraction and 38 evaluation manifest files,
fixed image/label/category mapping, raw-logit rectification, RMS scaling,
training AUROC by pairwise tie-aware counting, clean grid losses, all
896 calibration nodes, conditional per-image losses and paired bootstrap
records. Maximum independently recomputed risk discrepancy was
$4.44\times10^{-15}$. No additional forward pass was performed by this
saved-record audit. Original data, source snapshots, settings, failures and
results remain unchanged under \path{project1_toy/head_transfer_20261007}.

Stop this pair and grid. Do not change class IDs, raw-logit threshold,
noise range or decoder after seeing no reversal. The result is stronger
than the earlier unresolved channel pilot as evidence of a held-out
sharing benefit, yet it is not hidden-feature monosemanticity, critical
branch validation, arbitrary-load theory or a full-model robustness result.
'''.replace('TABLE_ROWS','\n'.join(table))
    (HERE/'project1_head_results_20261007.tex').write_text(content,encoding='utf-8')
    volume=HERE/'volume2.tex';text=volume.read_text(encoding='utf-8')
    start='% BEGIN FIXED HEAD TRANSFER\n';end='% END FIXED HEAD TRANSFER\n'
    if start in text:
        before,rest=text.split(start,1);_,after=rest.split(end,1);text=before+after
    anchor='\\chapter{Project 2: the correct meaning of the covariance recursion}'
    assert anchor in text
    text=text.replace(anchor,start+content+'\n'+end+'\n'+anchor,1)
    volume.write_text(text,encoding='utf-8')
    for name in ['head_risk','head_policy_contrast']:
        shutil.copy2(ROOT/f'project1_toy/head_transfer_20261007/plots_v2/{name}.png',HERE/f'figures/project1_{name}.png')
    print('Integrated saved head results; no new mathematical derivation or numerical case.')

if __name__=='__main__':main()
