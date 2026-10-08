import json,shutil
from pathlib import Path
base=Path(__file__).parent; root=base.resolve().parents[1]
data=json.loads((base/'outputs/test_run_v1/results.json').read_text())
rows=[]
for s,cl,ncl,d,lo,hi in zip(data['sigma_grid'],data['CL_error'],data['NCL_error'],data['delta_NCL_minus_CL'],data['simultaneous_lower'],data['simultaneous_upper']):
    rows.append(f'{s:.2f} & {100*cl:.3f} & {100*ncl:.3f} & {100*d:+.3f} & $[{100*lo:+.3f},{100*hi:+.3f}]$\\\\')
section=r'''
\section{Native projected-feature corruption reversal}
\label{sec:native-projected-reversal}

\paragraph{Source-justified representation and separate registration.}
The preceding backbone experiment remains a failed prerequisite check. Inspection of the anchor's released evaluation code at commit \texttt{d8519e994d8e0ccc98ad6d55978c58d70c72421e} establishes that its linear classifier receives the backbone output after the native projector, followed by ReLU for NCL. This differs from the predecessor's default backbone-only probing path. A separate follow-up therefore uses the strictly loaded projector from each released checkpoint, with signed CL outputs and nonnegative NCL outputs. The released projectors have 2048 hidden units and 256 outputs; they are not the anchor's larger-projector runs. This layer choice was source-justified after seeing the backbone failure and registered before projected features were computed. It is not retrospectively the original experiment. No further head, checkpoint or noise-grid search was conducted.

\paragraph{Clean starting contrast.}
Use the same fitting and validation indices and the same fixed 50-epoch clean-probe procedure. Reuse the verified clean backbone cache, applying the actual frozen projector. The projected-feature validation error is 0.443000 for CL and 0.464800 for NCL: the NCL-minus-CL difference is 0.021800, with conditional paired-image 95\% interval $[0.011000,0.033400]$. Class consistency is 0.010001187 for CL and 0.114704363 for NCL, with difference 0.104703176 and interval $[0.101658631,0.108490251]$. Both prerequisites pass. Raw sparsity below 0.01 is 0.025153 for CL and 0.937743 for NCL; nondead coordinate counts are 256 and 232 respectively. This establishes the specified proxy contrast and clean advantage for this fitted pair, not a causal isolation of monosemanticity.

\paragraph{The prospective affine prediction failed.}
On the prescribed 500 validation images and 32 shared noise directions each, the affine classifier approximation predicts no crossing on the fixed grid. Its error discrepancy at raw-pixel noise $\sigma=0.04$ is 0.060500 for CL and 0.0754375 for NCL, exceeding the allowed 0.02. The relative centered-logit RMS residuals are 1.142834 and 1.105300, exceeding the allowed 0.25. At $\sigma=0.01$, error discrepancies are much smaller, 0.0000625 and 0.0026875; small-noise agreement does not justify finite-noise extrapolation. The failed prediction was frozen and hashed before TEST scoring. Its predictive claim is rejected. Under the previously documented pre-outcome design, the independently specified native phenomenon test still runs.

\paragraph{Actual native test and uncertainty.}
Evaluate both complete frozen image networks, including their trained projectors and fitted clean probes, on the official 10,000-image TEST split. Add unclipped Gaussian noise to raw pixels on the fixed eight-level grid, using three shared seeded directions per image. Neither network nor head adapts to corruption. Define the reported difference as NCL classification error minus CL classification error: positive favors CL; negative favors NCL. Bootstrap paired images within classes, keeping replicates grouped, with 2,000 draws. The table's intervals use Bonferroni tail quantiles over the eight levels, conditional on this checkpoint/probe pair and the specified sampling procedure. They do not provide training-seed uncertainty or confidence over every intermediate noise strength.

\begin{center}\small
\begin{tabular}{rrrrl}
\hline
$\sigma$ & CL error (\%) & NCL error (\%) & Difference (points) & Simultaneous interval\\
\hline
TABLE_ROWS
\hline
\end{tabular}
\end{center}

\begin{figure}[htbp]
\centering
\includegraphics[width=\textwidth]{figures/native_projected_curve_20261008.png}
\caption{Actual native classification-error curves and NCL-minus-CL differences on the fixed grid. The dashed curve is the failed frozen affine prediction, retained for comparison. Negative differences favor NCL. The result exhibits a resolved intermediate-noise advantage for NCL; it is not a monotone advantage for all corruption levels. Connecting lines guide the eye and do not certify behavior between evaluated levels.}
\end{figure}

\paragraph{What is established.}
CL wins clean with a positive simultaneous lower endpoint. NCL wins at $\sigma=0.12$, with error advantage 1.2233 percentage points and interval $[0.6075,1.8684]$ points, and at $\sigma=0.20$, with advantage 0.6500 points and interval $[0.2116,1.0850]$. Thus this complete native-network comparison establishes the targeted ordering reversal at evaluated noise levels. The point curve first changes sign between 0.04 and 0.08; linear interpolation gives 0.07835294. That value is descriptive, not a successfully predicted boundary or a confidence interval: the difference at 0.08 is unresolved, while the positive difference at 0.04 and negative difference at 0.12 are resolved. CL regains a small resolved advantage at 0.30. Both models then have accuracy below 3\%, close to the 1\% chance level, so this late advantage has limited practical meaning. There is no evidence here for a unique, permanent crossing.

\paragraph{Verification, limitations and connection to the theory.}
Independent NumPy recomputation reproduces all saved test error differences, simultaneous intervals and the reversal decision; it also checks the failed prediction curve and frozen hash. Cached-feature consistency is independently checked. The native reversal is an observed risk-ordering result. The affine mathematical approximation did not predict it. The earlier toy reconstruction theorem uses a different loss, noise location and representation model, so its numerical boundary and critical exponent are not validated by this classification experiment. These results must not be presented as quantitative confirmation of the toy law. The remaining paper-critical gap is an explanation and predictive boundary that survives the native nonlinear model, with appropriate independent replication. Existing monosemanticity papers already demonstrate robustness gains; this single comparison alone does not establish publication novelty or a completed main-track paper.

\paragraph{Reproducible record.}
Protocols, source justification, registration, code, immutable failed and successful gate outputs, final probes, split indices, validation direction errors, frozen prediction, per-image/per-replicate test errors and losses, bootstrap draws, logs and independent checks are retained under \texttt{project1\_toy/real\_projected\_ncl\_20261008/}. Full feature caches and verified dependencies remain in the documented cluster scratch directory. The conditional native run completed successfully in approximately 12 minutes 45 seconds on the Physics CPU allocation. Completion of computation is distinct from success of the predictive claim.
'''.replace('TABLE_ROWS','\n'.join(rows))
(base/'native_outcome.tex').write_text(section,encoding='utf-8')
shutil.copy2(base/'outputs/figures/native_corruption_curve.png',root/'research_notes/figures/native_projected_curve_20261008.png')
source=root/'research_notes/volume2.tex'; text=source.read_text(encoding='utf-8')
start='% BEGIN NATIVE PROJECTED OUTCOME'; end='% END NATIVE PROJECTED OUTCOME'
block=start+'\n'+section+'\n'+end+'\n\n'
if start in text:
    a=text.index(start); b=text.index(end,a)+len(end); text=text[:a]+block.rstrip()+text[b:]
else:
    a=text.index('\\chapter{Project 2'); text=text[:a]+block+text[a:]
source.write_text(text,encoding='utf-8'); print('Integrated native reversal and failed prediction, with limits.')
