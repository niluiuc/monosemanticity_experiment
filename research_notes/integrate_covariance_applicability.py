"""Integrate reviewed applicability proof and unchanged saved-record diagnostic."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
HERE = ROOT / 'research_notes'
REVIEW = ROOT / 'project1_toy/professor_bridge_review_20261007'


def main():
    diagnostic = json.loads((REVIEW / 'covariance_diagnostic.json').read_text())
    table = []
    for key, label in [('hidden_channels', 'Hidden channels'), ('class_evidence', 'Class evidence')]:
        case = diagnostic['cases'][key]
        train = case['splits']['train']
        neighbour = next(r for r in case['saved_grid_neighbours']
                         if r['grid_size'] == 512 and r['endpoint_angle'] == 0
                         and r['signed_angular_step'] > 0)
        table.append(f"{label} & {train['covariance']:.8f} & {train['correlation']:.8f} & "
                     f"{train['empirical_mono_directional_slopes'][0]:.8f} & "
                     f"{neighbour['angular_secant']:.8f}\\\\")
    content = r'''\section{Applicability audit: correlation obstructs exact clean retention}
\label{sec:covariance-applicability}
The preceding real-feature comparisons did not demonstrate the
training-transition-linked risk boundary. Before another importance
sweep, check whether their empirical clean objectives can even contain
the exact retention optimum used by the independent-Bernoulli law.
The following constructive proof resolves this prerequisite.

\subsection{Assumptions and a constructive exclusion}
Let $X_1,X_2\geq0$ have finite second moments, let
$\mu_2=\E X_2>0$, and fix $\eta>0$. Use exactly the scalar,
energy-one encoder, tied ReLU decoder and free biases of Project 1:
\begin{align}
L(w,b)&=\E\bigl[(\ReLU(w_1(w_1X_1+w_2X_2)+b_1)-X_1)^2\bigr]
\nonumber\\
&\quad+\eta\E\bigl[(\ReLU(w_2(w_1X_1+w_2X_2)+b_2)-X_2)^2\bigr],
\qquad w_1^2+w_2^2=1.
\end{align}
Retention of the first coordinate, $w=(1,0)$ with
$b=(0,\mu_2)$, has risk $\eta\operatorname{Var}(X_2)$.
These biases attain its minimum: the first coordinate is reconstructed
exactly and the omitted coordinate has its best constant prediction.
If $\operatorname{Cov}(X_1,X_2)\ne0$, this geometry is not a local
minimum of the jointly optimized clean objective.

For $|\theta|<1$ take the explicit feasible path
\begin{equation}
w(\theta)=(\sqrt{1-\theta^2},\theta),\qquad
b(\theta)=(0,\mu_2).
\label{eq:cov-feasible-path}
\end{equation}
It preserves the energy and tied decoder exactly. Write
$s=\sqrt{1-\theta^2}$. The two preactivations are
\begin{equation}
u_1=(1-\theta^2)X_1+\theta sX_2,
\qquad u_2=\mu_2+\theta sX_1+\theta^2X_2.
\end{equation}
Since ReLU is one-Lipschitz and $\ReLU(X_1)=X_1$,
\begin{equation}
\|\ReLU(u_1)-X_1\|_{L^2}
\leq\theta^2\|X_1\|_{L^2}+|\theta|\|X_2\|_{L^2}.
\end{equation}
Thus the retained-coordinate squared error is $O(\theta^2)$,
including its atom at zero and either perturbation sign.

Put $v_\theta=\theta sX_1+\theta^2X_2$ and
$d_\theta=\ReLU(\mu_2+v_\theta)-(\mu_2+v_\theta)$.
The dropped output's baseline bias is strictly positive. Its clipping
residual satisfies
\begin{equation}
|d_\theta|\leq|v_\theta|\,
\ind\{\mu_2+v_\theta<0\}.
\end{equation}
For $|\theta|\leq1/2$,
$|v_\theta/\theta|\leq X_1+X_2/2$, which has finite second
moment. For each finite realization the displayed indicator tends to
zero as $\theta\to0$. Dominated convergence therefore gives
$\|d_\theta\|_{L^2}=o(|\theta|)$.
Also $v_\theta/\theta\to X_1$ in $L^2$. Consequently
\begin{equation}
\ReLU(u_2)=\mu_2+\theta X_1+r_\theta,
\qquad\|r_\theta\|_{L^2}=o(|\theta|).
\end{equation}
Expand the squared error. Cauchy--Schwarz controls the terms containing
$r_\theta$, yielding
\begin{align}
\E[(\ReLU(u_2)-X_2)^2]
&=\operatorname{Var}(X_2)
+2\theta\E[(\mu_2-X_2)X_1]+o(|\theta|)\nonumber\\
&=\operatorname{Var}(X_2)
-2\theta\operatorname{Cov}(X_1,X_2)+o(|\theta|).
\end{align}
Combining both outputs proves the feasible-path expansion
\begin{equation}
L(w(\theta),(0,\mu_2))
=\eta\operatorname{Var}(X_2)
-2\eta\operatorname{Cov}(X_1,X_2)\theta+o(|\theta|).
\label{eq:covariance-retention-obstruction}
\end{equation}
Choose $\theta$ with the same sign as the nonzero covariance. The
negative linear term dominates the remainder for sufficiently small
$|\theta|$, giving strict improvement arbitrarily close to retention.
Bias optimization can only improve on this explicit feasible path;
no assertion about differentiability of the profiled minimum is needed.
Interchanging coordinates gives the same exclusion for retaining $X_2$
when $\E X_1>0$. Thus with both means positive and nonzero covariance,
neither exact coordinate-retaining geometry is a clean local or global
optimum for any strictly positive pair of importance weights in this class.
The simultaneous sign reversal of an encoder leaves its tied decoder
unchanged, so negative coordinate-retention orientations add no exception.

\subsection{What the exclusion does and does not establish}
For a finite empirical distribution, bounded observations and positive
$\mu_2$ make the dropped gate remain active sufficiently close to zero;
the argument is an elementary finite-sum expansion. Applying it to a
training array is an exact statement about that array's empirical
objective, not a claim about unknown population covariance.

The omitted coordinate can be predicted to first order using the
retained coordinate's correlated deviations. This is the familiar
covariance/regression mechanism, not a claimed major novelty or a
theorem about all monosemantic neural representations. A richer untied
decoder changes the comparator and requires a different analysis.
Making importance small makes the advantage small; it does not create
an exact retention optimum at a positive importance. A finite optimizer
tolerance can conceal a small benefit and imitate a transition.

Zero covariance is necessary for a retention optimum under these
conditions, but is not sufficient for a transition, independence or
the critical exponent. The established critical law also uses binary
support, a globally selected opposite-sign branch, cubic clean gain and
particular gate separations. Merely observing some transition in
continuous data cannot validate those assumptions or the $3/2$ law.
The exclusion concerns clean selection. It does not exclude a noisy
winner crossing elsewhere and does not explain every noisy outcome.

\subsection{Bounded saved-record check and actual findings}
The diagnostic question was fixed before recomputation: do the two
saved training distributions have the covariance obstruction, and do
their already recorded closest angular neighbours corroborate local
improvement? The minimum test reads saved train, calibration and test
arrays plus the existing 256/512 angular grids. It performs no fitting,
new noise evaluation, model inference or feature selection. Stop after
these two pairs regardless of the signs. Inputs and outputs are hashed
in \texttt{project1\_toy/professor\_bridge\_review\_20261007/}.

Both training arrays have positive coordinate means. Their recorded
moments and nearest positive-sharing neighbour at the first retention
endpoint are:
\begin{center}
\small
\begin{tabular}{lrrrr}
\toprule
Pair & Covariance & Correlation & Path derivative & Grid secant\\
\midrule
__ROWS__
\bottomrule
\end{tabular}
\end{center}
The path derivative is $-2\eta\operatorname{Cov}(X_1,X_2)$ with
$\eta=2/3$. The grid secant is a finite-angle change in the
\emph{bias-profiled} empirical loss, not an exact profiled derivative.
Their close values are corroboration, not proof of derivative equality.
Both saved resolutions also improve toward positive sharing from the
other retention endpoint. There, increasing the weak first-coordinate
parameter moves the usual angular coordinate downward, so angular and
weak-parameter slopes have opposite sign.

For the hidden pair, training means are approximately $(.52040617,
.65005986)$; for the class-evidence pair they are $(.69959241,.66504437)$.
The saved calibration and test covariances are also positive, but are
reported descriptively without population inference or selection use.
Two independent proof reviews found no required mathematical correction.

\subsection{Why an eventual high-noise crossing is not a rescue}
The earlier section ``An arbitrary-load bound for fixed geometries under
bias calibration'' already proves, for dependent nonnegative targets with
finite third moments,
\[
\lim_{\sigma\to\infty} R_{\rm cal}(W,\sigma)
=\sum_i I_i\operatorname{Var}(X_i)
+\sum_{i:w_i\ne0}I_i(\E X_i)^2.
\]
Its uniform density bound, continuity argument and sufficient
mono-favored region $\Delta_{\rm cal}\ge P-Q/\sigma$ are already
derived in this volume. For full-support sharing versus retention of
the first coordinate, the population-optimal difference therefore tends
to $\eta(\E X_2)^2>0$. This is a support/noise-exposure effect: both
mixed outputs are noisy and eventually approach zero prediction, while
mono's omitted constant remains uncorrupted. Full-support orthogonal
geometries have the same limit. It does not independently validate the
clean storage transition, critical exponent or semantic interpretation.

For comparison, hold the finite biases fixed and keep $w$ fixed.
For each nonzero output, ReLU homogeneity and its Lipschitz inequality give
\[
\frac{g_i}{\sigma}
=\ReLU\!\left(w_iZ+\frac{w_i(w\cdot X)+b_i}{\sigma}\right)
\longrightarrow (w_i Z)_+
\quad\hbox{in }L^2.
\]
Finite second moments justify this convergence. Thus
$\E g_i^2/\sigma^2\to w_i^2/2$; Cauchy--Schwarz makes
$\E X_i g_i/\sigma^2\to0$ and $\E X_i^2/\sigma^2\to0$.
A zero output weight yields a finite constant with zero scaled limit.
For energy-one two-feature sharing and retention of the first coordinate,
\[
\frac{\Delta_{\rm frozen}(\sigma)}{\sigma^2}
\longrightarrow
\frac{w_1^2+\eta w_2^2-1}{2}
=-\frac{(1-\eta)w_2^2}{2}.
\]
This ordinary Gaussian scaling is not advertised as a new critical law.
With $\eta<1$, it reflects redistribution of importance-weighted output
noise rather than matching every sensitivity resource.

The two reviewers rejected a widened noise search as a replacement
central result. An eventual calibrated crossing could verify the existing
support bound, but would not resolve the missing transition-linked
real-feature validation. Population-optimal bias statements also cannot
be silently substituted for finite calibration/test-split guarantees.
No additional noise values were evaluated for this audit.

\subsection{Stopping decision and unresolved research claim}
Neither unchanged empirical pair can have the exact positive-importance
retention onset required for the current independent-feature critical
mechanism. Therefore an importance sweep on these pairs is not a
justified validation experiment. Do not add noise levels or replace
features merely to obtain a desired reversal. Preserve both real
tests and their actual outcomes.

This excludes an unsuitable experiment; native real-feature validation
remains unresolved. Binarizing or independently permuting scores would
be a controlled or semi-synthetic experiment, not natural transfer.
A correlated-feature extension requires a narrow proof target and
stopping condition before fitting; its success is not established here.
'''.replace('__ROWS__', '\n'.join(table))
    (HERE / 'project1_covariance_applicability_20261007.tex').write_text(content, encoding='utf-8')
    path = HERE / 'volume2.tex'
    source = path.read_text(encoding='utf-8')
    start = '% BEGIN COVARIANCE APPLICABILITY'
    end = '% END COVARIANCE APPLICABILITY'
    if start in source:
        before, remainder = source.split(start, 1)
        _, after = remainder.split(end, 1)
        source = before.rstrip() + '\n\n' + after.lstrip()
    anchor = r'\chapter{Project 2: the correct meaning of the covariance recursion}'
    assert source.count(anchor) == 1
    source = source.replace(anchor, start + '\n' + content + '\n' + end + '\n\n' + anchor, 1)
    path.write_text(source, encoding='utf-8')
    print('Integrated full covariance applicability derivation and saved diagnostics into existing Volume II.')


if __name__ == '__main__':
    main()
