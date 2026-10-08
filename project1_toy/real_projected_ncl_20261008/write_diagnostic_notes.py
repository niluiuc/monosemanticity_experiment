import json,shutil
from pathlib import Path
base=Path(__file__).parent; root=base.resolve().parents[1]
section=r'''
\section{Finite-noise applicability diagnostic}
\paragraph{Question, status and stopping criterion.}
After the native outcome was observed, conduct one validation-only diagnostic at the previously failed $\sigma=0.04$. It is not a new prospective prediction. Use the same 500 validation images and 32 Gaussian directions per image, with unchanged seed. Compare the actual classifier, its full affine approximation, and an affine approximation to only the CNN backbone followed by the exact trained nonlinear projector and fixed probe. This last approximation permits projector gates to switch while keeping the upstream backbone affine. The existing applicability thresholds must both hold for both networks: classification-error discrepancy at most 0.02 and relative centered-logit RMS residual at most 0.25. Failure stops projection-only repairs; no extra heads, noise levels or TEST images are searched.

\paragraph{Observed failure and independent verification.}
For CL, allowing projector gates to switch gives error discrepancy 0.0599375 and relative RMS residual 1.145880. For NCL, the corresponding quantities are 0.0830000 and 0.960406. Both fail. The full affine approximation reproduces the previous discrepancies 0.0605000 and 0.0754375. Independent recomputation from saved actual and approximate logits verifies every reported error and residual ratio. Thus this proposed repair is insufficient: an adequate approximation must also treat the upstream CNN's finite-noise nonlinearity. This diagnostic does not establish which upstream layers cause the effect or whether their nonlinearity explains the CL--NCL reversal.

\paragraph{Exact finite-sample residual decomposition.}
For image $i$, direction $d$ and class-logit vector $s$, let $P=I-\mathbf{1}\mathbf{1}^{\mathsf T}/100$ remove the irrelevant common-logit offset. Define
\[
r_{id}=P\{s(x_i+\sigma z_{id})-s_{\mathrm{approx}}(x_i,z_{id},\sigma)\},
\qquad \bar r_i=D^{-1}\sum_{d=1}^D r_{id},\quad D=32.
\]
Write $r_{id}=\bar r_i+(r_{id}-\bar r_i)$. Squaring and summing eliminates the cross-term because $\sum_d(r_{id}-\bar r_i)=0$. Hence the identity
\[
\frac1{ND}\sum_{i,d}\|r_{id}\|^2
=\frac1N\sum_i\|\bar r_i\|^2
+\frac1{ND}\sum_{i,d}\|r_{id}-\bar r_i\|^2
\]
holds exactly for the saved finite sample. This is a standard decomposition, not a novel theorem. For the full affine approximation, the first component accounts for 0.716019 of CL residual energy and 0.678497 of NCL residual energy. With nonlinear projection after an affine backbone, the fractions are 0.715752 and 0.599003. The empirical direction average includes finite-sample variability; these fractions are not unbiased estimates of population drift energy. They nevertheless show that the observed approximation error contains a substantial coherent component across sampled directions, rather than only direction-centered fluctuation. They do not provide a crossing prediction or causal monosemanticity conclusion.

\begin{figure}[htbp]
\centering\includegraphics[width=.95\textwidth]{figures/native_residual_decomposition_20261008.png}
\caption{Decomposition of centered logit residual energy at $\sigma=0.04$ on saved validation records. The vertical axis is an energy fraction. Blue is the empirical direction mean; orange is the direction-centered component. The two bars for each network compare the full affine approximation with affine CNN plus exact nonlinear projector. This post-outcome descriptive calculation identifies a deficiency of the attempted predictor; it is not new TEST evidence.}
\end{figure}

\paragraph{Decision for the paper.}
Preserve the real native ordering reversal and the rejected affine forecast. Stop the projection-only repair path. The next research contribution must explain finite-noise native behavior beyond a locally affine encoder, and be evaluated prospectively on data or model instances not used to construct it. Replication is also required before interpreting the released-checkpoint comparison as a broad monosemanticity tradeoff. Adding more special cases to the previous toy theorem would not resolve these gaps.
'''
(base/'diagnostic_notes.tex').write_text(section,encoding='utf-8')
shutil.copy2(base/'outputs/gate_diagnostic_v1/residual_decomposition.png',root/'research_notes/figures/native_residual_decomposition_20261008.png')
source=root/'research_notes/volume2.tex'; text=source.read_text(encoding="utf-8")
start='% BEGIN NATIVE GATE DIAGNOSTIC'; end='% END NATIVE GATE DIAGNOSTIC'
block=start+'\n'+section+'\n'+end+'\n'
if start in text:
    a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+block.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2'); text=text[:a]+block+'\n'+text[a:]
source.write_text(text,encoding='utf-8')
record='''

## Bounded gate diagnostic completed

- Physics CPU job 11212585 completed. This is explicitly post-outcome validation analysis, not a revised successful prediction.
- At sigma .04, affine CNN plus exact nonlinear projector fails both networks: error discrepancies .0599375/.0830000 and relative centered-logit RMS residuals 1.145880/.960406 for CL/NCL. Stop projection-only repairs.
- All actual/approximate logits are saved, unlike the first prediction run's aggregate residual record. Independent NumPy recomputation reproduces errors and residuals. No TEST images were loaded.
- The exact saved-record energy decomposition attributes .716019/.678497 of full-affine residual energy to the empirical direction mean for CL/NCL. This mean includes sampling variation. It is descriptive evidence of a substantial coherent component, not causal attribution or a crossing law.
- Full assumptions, derivation of the standard residual identity, outcomes and plot are integrated in Section 8.37 of the existing derivation volume and editable source. No new novelty claim is made.
'''
for path in (base/'RUN_STATUS.md',root/'project1_toy/plan.md'):
    old=path.read_text(encoding="utf-8")
    if '## Bounded gate diagnostic completed' not in old: path.write_text(old+record,encoding='utf-8')
print('Integrated completed diagnostic and exact standard residual identity.')
