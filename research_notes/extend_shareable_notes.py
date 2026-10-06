"""Extend the existing shareable article through the sixth derivation chapter."""
from pathlib import Path
import re, shutil, json

ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'output/overleaf/monosemanticity_notes'
TARGET=DEST/'main.tex'
text=TARGET.read_text(encoding='utf-8')
if '% BEGIN PROJECT 1 EXTENSION' in text:
    text=text.split('% BEGIN PROJECT 1 EXTENSION')[0]+text.split('% END PROJECT 1 EXTENSION')[1]
original_appendix=text.split(r'\appendix',1)[1]
initial=text.split(r'\appendix',1)[0]
original_appendix=original_appendix.replace(r'\end{document}','')
source=(ROOT/'research_notes/volume2.tex').read_text(encoding='utf-8')
extension=source.split(r'\chapter{Fix the question before manipulating the symbols}',1)[1]
extension=r'\chapter{Research setup: features, tasks and corruption}'+extension.split(r'\chapter{Project 2:',1)[0]

replacements={
 'The commitments that remain fixed':'Research objectives and the operational task',
 "The source anchor is Zhang et al.'s monosemanticity-and-robustness paper, taught in Volume I.":"The source anchor is Zhang et al.'s monosemanticity-and-robustness paper analyzed in Sections 1--12.",
 'The mathematical choices below instantiate this direction; they do not exhaust it.':'The following mathematical model specifies a controlled instance of these research questions.',
 'What the original margin formula really means':'Linear readouts, geometric alignment and perturbation radii',
 'Retain the valid geometric identity while making its adversarial interpretation exact.':'Distinguish a geometric alignment score from a task-dependent perturbation radius.',
 'Recovering the old expression':'Alignment of a tied readout with a feature axis',
 'Calling $Ge_i$ ``the optimal readout\'\' without these qualifications was unjustified.':'The matched direction $Ge_i$ therefore need not be the least-squares-optimal effective readout.',
 'Answers to the earlier conceptual questions':'Interpretation: perturbations, sign, frequency and scale',
 'They repair the operational meaning of the earlier margin; they are not, by themselves, a novel conference contribution.':'Their assumptions determine the interpretation of the margin. These identities alone do not establish a new learned-representation result.',
 'Linear reconstruction: the useful calculation and its limit':'Linear reconstruction risk and an isotropic comparison',
 'This is not evidence against the project. It shows that':'This calculation shows that',
 'A controlled way forward':'Why nonlinear decoding is needed for the tradeoff',
 'Project 1: an exact risk for arbitrary fixed geometry':'Project 1: feature-detection risk for fixed geometry',
 'What the formula buys us':'Frequency, importance and capacity in the risk',
 'Why this differs from the earlier proposed boundary':'Statistical risk and worst-case geometry are different quantities',
 'The earlier expression $p(n/m)\\le\\tau^{-2}-1$ inserted an average active-feature count into a worst-case alignment formula. An unrestricted attacker can perturb inactive coordinates too; that substitution is not valid.':'A state-averaged interference load cannot be substituted into an unrestricted worst-case alignment formula. An unrestricted attacker can perturb inactive coordinates as well as active ones. Activation frequency must enter through the stated input distribution or an explicitly restricted perturbation set.',
 'The project remains a phase-diagram project. Its phase variable is now a defined error comparison rather than an arbitrary cutoff on a scale-dependent proxy.':'The phase variable is a defined comparison of prediction errors under specified resources and corruptions.',
 'Project 1: a closed tradeoff for a superposed pair':'Project 1: the superposed-pair tradeoff and phase diagram',
 'What is solved and what is still research':'Scope of the solved pair and the learned-geometry question',
 'not an inferred slogan that rare concepts are always safe':'with no assumption that rare concepts automatically receive isolated directions',
 'Unlike $M_i$, this expression has activation probabilities in a legitimate statistical role.':'Activation probabilities enter this variance because the nuisance activations are random; the fixed-geometry alignment score $M_i$ has a different definition.',
 'Chernoff optimization gives either one-sided tail bound':'The exponential-moment calculation below gives either one-sided tail bound',
 'Equations in this chapter':'Equations in this section',
 'This chapter solves':'This section solves',
 '$S_i$':'$T_i$',
 'S_i=':'T_i=',
 'S_i+':'T_i+',
 'S_i +':'T_i +',
 'S_i+':'T_i+',
 'S_i)':'T_i)',
 '\\pm(S_i':'\\pm(T_i',
}
for a,b in replacements.items():extension=extension.replace(a,b)

setup=r'''
\subsection{Binary presence, continuous amplitude and a named concept}
A binary feature $b_i$ records whether a concept is present. It is not a class label for the entire input and is not a neuron index. An input can contain several concepts simultaneously. If $b_i\sim\operatorname{Bernoulli}(p_i)$, then
\begin{equation}\Prb(b_i=1)=p_i,\qquad \Prb(b_i=0)=s_i=1-p_i,\qquad \E b_i=p_i,\qquad \Var(b_i)=p_i(1-p_i).\end{equation}
The identity $b_i^2=b_i$ gives $\E b_i^2=p_i$ and hence the variance. For a continuous sparse feature $x_i=b_iU_i$, with $U_i\sim\operatorname{Unif}[0,1]$ independent of $b_i$,
\begin{equation}\E x_i^k=p_i\int_0^1u^k\,du=\frac{p_i}{k+1},\qquad \E x_i=\frac{p_i}{2},\qquad \Var(x_i)=\frac{p_i}{3}-\frac{p_i^2}{4}.\end{equation}
Recovering presence and reconstructing amplitude are different tasks, even when the same encoder is used. Their phase boundaries need not coincide.

For example, $b=(1,0,1)$ may mean that an image contains a circle and a red object, but no square. The encoder maps this combination to $h=w_1+w_3$. The columns $w_i$ identify storage directions; the scalar coefficient $b_i$ identifies whether each direction contributes on this input. A neuron coordinate is a component of $h$, which may mix several such contributions.

\subsection{Why the Gram matrix is positive semidefinite and rank limited}
The Gram entry is $G_{ij}=w_i^\top w_j$. Symmetry follows from the symmetry of the inner product. For every $v\in\R^n$,
\begin{equation}v^\top Gv=v^\top W^\top Wv=(Wv)^\top(Wv)=\norm{Wv}_2^2\ge0.\end{equation}
This proves positive semidefiniteness. It does not assert that every entry of $G$ is positive: an antipodal pair has a negative off-diagonal entry. Diagonal entries satisfy $G_{ii}=\norm{w_i}_2^2\ge0$.

Rank counts linearly independent directions in the image of a linear map. Because $Wv\in\R^m$, its image has dimension at most $m$. Its $n$ columns also span at most $n$ independent directions. Thus $\rank W\le\min(m,n)$. Moreover,
\begin{equation}\ker(W^\top W)=\ker W,\qquad \rank G=\rank W\le m.\end{equation}
For the kernel equality, $Gv=0$ implies $0=v^\top Gv=\norm{Wv}_2^2$, hence $Wv=0$; the converse follows immediately. If $n>m$, $G$ cannot equal $I_n$. A fully noninterfering comparator with the same bottleneck must therefore omit features or use another explicitly stated resource convention.

\subsection{Signed concepts and destructive interference}
If temperature is a single signed variable $t$, positive and negative values describe its two poles. With one stored direction, the readout reports the signed temperature; moving toward the negative pole is a change in the target signal. This is different from two separately specified nonnegative concepts $x_1,x_2$ represented by
\begin{equation}W=(1,-1),\qquad h=x_1-x_2,\qquad \hat x=(\ReLU(h),\ReLU(-h)).\end{equation}
When $x_1>0,x_2=0$, the first concept is recovered exactly; when $x_1=0,x_2>0$, the second is recovered exactly. When both are positive, their common amplitude is lost. In particular, $x_1=x_2>0$ gives $h=0$, indistinguishable from simultaneous absence. Deciding whether two names denote one signed variable or two independently meaningful concepts is part of specifying ground truth, not something a Gram matrix determines by itself.

\subsection{Three distinct roles for importance}
An importance weight $I_i$ determines the cost of an error, while $p_i$ determines how often an activation occurs. A rare concept can have a large penalty when missed. In a fixed model, changing $I_i$ changes the reported weighted risk without changing $G$. In a trained model, changing the weights in the training loss can also change the learned geometry. Neither operation proves that the optimizer must allocate an isolated direction to that concept. Those effects must be separated in the analysis and experiments.
'''

margin_detail=r'''
\subsection{The perturbation budget and equality in the norm bound}
The constraint $\norm\delta_q\le\varepsilon$ specifies a set of allowed perturbations. Writing $\delta=\varepsilon u$ reduces the maximization to $\norm u_q\le1$; the factor $\varepsilon$ remains outside the inner product. For $q=2$, Cauchy--Schwarz is tight at
\begin{equation}\delta_{\rm worst}=-\varepsilon y\frac{\beta}{\norm\beta_2},\qquad yf(x+\delta_{\rm worst})=yf(x)-\varepsilon\norm\beta_2.\end{equation}
The smallest budget reaching the boundary is therefore $r_2=yf(x)/\norm\beta_2$. Equality reaches score zero; crossing requires a larger budget or a stated tie rule. For $q=\infty$, choosing $\delta_j=-\varepsilon y\operatorname{sign}(\beta_j)$ gives a swing $\varepsilon\norm\beta_1$. For $q=1$, concentrate the budget on a coordinate of largest $|\beta_j|$, giving a swing $\varepsilon\norm\beta_\infty$. These are different operational quantities for the same readout.

\subsection{Deriving the alignment ratio and its allowed values}
Let $e_i$ be the standard basis vector, with a one in coordinate $i$. Then $\beta=Ge_i$ is column $i$ of $G$, and $\beta^\top e_i=G_{ii}$. Because $G$ is symmetric,
\begin{align}
\norm{Ge_i}_2^2&=\sum_jG_{ji}^2=G_{ii}^2+\sum_{j\ne i}G_{ij}^2,\\
M_i&=\frac{G_{ii}}{\sqrt{G_{ii}^2+\sum_{j\ne i}G_{ij}^2}}
=\frac1{\sqrt{1+\sum_{j\ne i}(G_{ij}/G_{ii})^2}}.
\end{align}
Dividing the sum of squares by $G_{ii}^2$ is the same as dividing every summand before adding: $\sum_jG_{ij}^2/G_{ii}^2=\sum_j(G_{ij}/G_{ii})^2$. This is not the square of a sum of overlaps.

If $w_i\ne0$, the diagonal is positive and the denominator is finite and at least $G_{ii}$. Hence $0<M_i\le1$. Negative values, including $-1$, cannot occur for this Gram-matrix alignment. A generic cosine can be negative, but this particular cosine involves a vector whose coordinate on $e_i$ is positive. Equality $M_i=1$ holds precisely when every $G_{ij}=0$ for $j\ne i$. If $w_i=0$, all entries in the corresponding row vanish, so the formula is undefined, not zero.

For $G=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$, both scores equal $1/\sqrt2$. The negative overlap lowers this sign-blind alignment exactly as a positive overlap of the same magnitude would. Yet the ReLU decoder can recover either concept perfectly when they never co-occur. This illustrates why statistical reliability depends on the input law and decoder as well as a squared-overlap score.

For the same fixed geometry, replacing $x=e_i$ by $x=a_i e_i$ with $a_i>0$ changes the zero-threshold radius to $a_iM_i$. Replacing the threshold by $c$ changes it to $(a_iG_{ii}-c)/\norm{Ge_i}_2$, provided this example is correctly classified. Thus $M_i$ is not a universal input-independent attack budget.

A common scaling $W\mapsto tW$ cancels in $M_i$. In contrast, scaling only column $w_i$ by $t>0$ gives
\begin{equation}M_i(t)=\frac{tG_{ii}}{\sqrt{t^2G_{ii}^2+\sum_{j\ne i}G_{ij}^2}}.\end{equation}
Individual feature norm, relative overlap and the overall norm budget must therefore be distinguished.
'''

ls_detail=r'''
\subsection{Derivation of the least-squares readout}
For centered $x$ with covariance $C$, let $h=Wx+\xi$, where independent centered noise has covariance $N$. The scalar estimate is $a^\top h$. Expanding its mean squared error for target $x_i=e_i^\top x$ gives
\begin{align}
J_i(a)&=\E(x_i-a^\top h)^2\\
&=C_{ii}-2a^\top WC e_i+a^\top(WCW^\top+N)a,\\
\nabla_aJ_i(a)&=-2WC e_i+2(WCW^\top+N)a.
\end{align}
Thus the normal equations are $(WCW^\top+N)a=WC e_i$. For a nonsingular covariance matrix, invert it. For a singular covariance matrix, the pseudoinverse gives the minimum-Euclidean-norm solution. Solutions differing by a vector in the covariance nullspace make the same prediction almost surely. For uncentered data, add an intercept $\mu_i-a^\top W\mu$ rather than silently dropping the means.

As a concrete example, take $W=(1,1)$, $C=\diag(4,1)$ and scalar code-noise variance $N=1/2$. The least-squares coefficient for $x_1$ is $a_1^*=4/(4+1+1/2)=8/11$. The tied matched coefficient is $w_1=1$. The former compensates for nuisance variance; the latter directly uses the storage direction. The least-squares optimum is an optimum for this squared-error task, not automatically for classification, adversarial robustness or a nonlinear decoder.

\subsection{Computing a Moore--Penrose pseudoinverse}
For a matrix $A\in\R^{r\times c}$, take an SVD $A=U\Sigma V^\top$. Replace each positive singular value $s_k$ by $1/s_k$ and leave zero singular values at zero, forming a $c\times r$ matrix $\Sigma^\dagger$. Then
\begin{equation}A^\dagger=V\Sigma^\dagger U^\top.\end{equation}
Zero singular values encode directions with no information; there is no finite inverse in those directions. In numerical work, values below a stated tolerance are treated as zero.

For the rank-one square matrix $A=\begin{pmatrix}1&1\\1&1\end{pmatrix}$, the nonzero unit singular vector is $(1,1)^\top/\sqrt2$ and the singular value is 2. Therefore
\begin{equation}A^\dagger=\frac14\begin{pmatrix}1&1\\1&1\end{pmatrix}.\end{equation}
For the full-row-rank rectangular matrix
\begin{equation}A=\begin{pmatrix}1&0&1\\0&1&0\end{pmatrix},\qquad AA^\top=\diag(2,1),\qquad A^\dagger=A^\top(AA^\top)^{-1}=\begin{pmatrix}1/2&0\\0&1\\1/2&0\end{pmatrix},\end{equation}
one has $AA^\dagger=I_2$, while $A^\dagger A$ is the orthogonal projector onto the row space, not $I_3$. The four defining identities are $AA^\dagger A=A$, $A^\dagger AA^\dagger=A^\dagger$, $(AA^\dagger)^\top=AA^\dagger$ and $(A^\dagger A)^\top=A^\dagger A$. These examples show both a singular square case and a genuinely rectangular case.
'''

recon_detail=r'''
\subsection{From a squared error to a trace: every term}
Set $z=(I-G)(x-\mu)-G\epsilon$ and $d=(I-G)\mu$. Then $x-\hat x=z+d$, with $\E z=0$. Expanding gives
\begin{equation}\E(z+d)^\top D(z+d)=\E z^\top Dz+d^\top Dd,\end{equation}
because both cross terms contain $\E z$. The scalar quadratic satisfies $z^\top Dz=\tr(Dzz^\top)$, so
\begin{equation}\E z^\top Dz=\tr(D\E zz^\top)=\tr(D\Cov z).\end{equation}
Independence and centering give
\begin{equation}\Cov z=(I-G)C(I-G)^\top+GNG^\top.\end{equation}
There is a plus sign on the noise term because the two minus signs multiply. The mean term is $d^\top Dd=\norm{D^{1/2}(I-G)\mu}_2^2$. This proves the reconstruction formula and identifies the information lost when a nonzero mean is omitted.

For independent random variables $A,B$, $\Var(A+B)=\Var A+\Var B$, but independence is a condition, not a consequence of their having identical marginal Gaussian distributions. In general,
\begin{equation}\Var(A\pm B)=\Var A+\Var B\pm2\Cov(A,B).\end{equation}
This follows by expanding $((A-\E A)\pm(B-\E B))^2$ and taking expectations. It is also the scalar form of the covariance transformation used above.
'''

frame_detail=r'''
\subsection{What a unit-column tight frame is}
A unit-column dictionary has $\norm{w_i}_2=1$ for every feature. It is tight when
\begin{equation}WW^\top=\frac nm I_m.\end{equation}
This says that, taken together, the columns supply equal total squared projection in every latent direction. It does not say the columns are mutually orthogonal. Multiplying by $W^\top$ and $W$ gives $F^2=(n/m)F$ for $F=W^\top W$.

An explicit example has three columns in two dimensions:
\begin{equation}W=\begin{pmatrix}1&-1/2&-1/2\\0&\sqrt3/2&-\sqrt3/2\end{pmatrix},\quad WW^\top=\frac32I_2,\quad F=\begin{pmatrix}1&-1/2&-1/2\\-1/2&1&-1/2\\-1/2&-1/2&1\end{pmatrix}.\end{equation}
The columns have 120-degree separation. Each row has off-diagonal squared overlap $1/4+1/4=1/2=n/m-1$. More generally,
\begin{equation}\sum_jF_{ij}^2=(F^2)_{ii}=\frac nmF_{ii}=\frac nm,\qquad \sum_{j\ne i}F_{ij}^2=\frac nm-1.\end{equation}
The diagonal contributes one, which must be subtracted before calling the remainder interference.

\subsection{Why the two optimized linear risks agree}
Let $E=n/m-1$. Expanding the distributed risk gives
\begin{equation}\ell(g)=v-2vg+(v+\sigma_x^2)(1+E)g^2.\end{equation}
Its derivative is $-2v+2(v+\sigma_x^2)(1+E)g$, and its second derivative is positive. Substitution of $g_*$ therefore gives a global minimum within this one-parameter family:
\begin{equation}\ell(g_*)=v-\frac{v^2}{(v+\sigma_x^2)(1+E)},\qquad n\ell(g_*)=nv-\frac{mv^2}{v+\sigma_x^2}.\end{equation}
For an isolated retained feature, the risk at coefficient $a$ is $v(1-a)^2+\sigma_x^2a^2$. The optimum is $a_*=v/(v+\sigma_x^2)$ and its risk is $v\sigma_x^2/(v+\sigma_x^2)$. Each omitted coordinate has risk $v$. Consequently,
\begin{align}L_{\rm mono}&=m\frac{v\sigma_x^2}{v+\sigma_x^2}+(n-m)v\\&=nv-\frac{mv^2}{v+\sigma_x^2}=L_{\rm distributed}.\end{align}
The equality compares the full set of $n$ targets, including omitted ones. If the dropped coordinates were excluded from evaluation, it would be a different comparison. For $n=3,m=2,v=0.2,\sigma_x^2=0.1$, both risks equal $1/3$.
'''

detector_detail=r'''
\subsection{Deriving the conditional Gaussian error}
For a fixed state $b$, write $u_i=(Gb)_i$ and $s_{z,i}=\sigma\sqrt{G_{ii}}$. The score is $z_i=u_i+\zeta_i$, where $\zeta_i/s_{z,i}\sim\mathcal N(0,1)$. If $b_i=1$, an error is a false negative:
\begin{equation}\Prb(z_i\le\theta_i\mid b)=\Phi\!\left(\frac{\theta_i-u_i}{s_{z,i}}\right).\end{equation}
If $b_i=0$, an error is a false positive:
\begin{equation}\Prb(z_i>\theta_i\mid b)=1-\Phi\!\left(\frac{\theta_i-u_i}{s_{z,i}}\right)=\Phi\!\left(\frac{u_i-\theta_i}{s_{z,i}}\right).\end{equation}
The identity $1-\Phi(t)=\Phi(-t)$ combines them using $2b_i-1$. Correlations between different $\zeta_i$ do not affect these marginal probabilities. They do matter when computing the joint law of several detector outputs.

The unconditional error is $e_i=(1-p_i)e_{i,0}+p_ie_{i,1}$, where $e_{i,0}$ is the false-positive probability conditional on absence and $e_{i,1}$ is the false-negative probability conditional on presence. For $p_i=0.001$, false-positive rate 0.01 and false-negative rate 0.1, the total error is $0.999(0.01)+0.001(0.1)=0.01009$, whereas recall is only $0.9$ and precision is
\begin{equation}\frac{p_i(1-e_{i,1})}{p_i(1-e_{i,1})+(1-p_i)e_{i,0}}\simeq0.0826.\end{equation}
Thus low aggregate error does not establish a useful rare-concept detector. Frequency, recall, precision and the importance-weighted contribution answer distinct questions.
'''

bayes_detail=r'''
\subsection{Deriving the prior-dependent threshold}
For $h=ab+\xi$ with $a>0$, the class-conditional densities are Gaussians centered at 0 and $a$. Bayes' rule gives
\begin{align}
\log\frac{\Prb(b=1\mid h)}{\Prb(b=0\mid h)}
&=\log\frac{p}{1-p}+\log\frac{\exp(-(h-a)^2/(2\sigma^2))}{\exp(-h^2/(2\sigma^2))}\\
&=\log\frac{p}{1-p}+\frac{h^2-(h-a)^2}{2\sigma^2}\\
&=\log\frac{p}{1-p}+\frac{ah}{\sigma^2}-\frac{a^2}{2\sigma^2}.
\end{align}
Declaring presence when the log ratio exceeds zero and dividing by $a/\sigma^2$ gives the stated threshold. The logarithmic term vanishes at $p=1/2$; it is positive for a rare feature and negative for a common one. If the readout is the matched score $z=ah$, its threshold is $a\theta_{\rm Bayes}$, not the same numerical threshold as for $h$. Equal error costs are assumed; asymmetric false-positive and false-negative costs would supply an additional log cost ratio.
'''

pair_detail=r'''
\subsection{How each Gaussian tail enters the four-state table}
For state 00, $h=\xi$. A false activation of concept 1 requires $\xi>a/2$, while a false activation of concept 2 requires $\xi<-a/2$; each probability is $q$. For state 10, $h=a+\xi$. Missing concept 1 requires $\xi\le-a/2$, with probability $q$, while falsely detecting concept 2 requires $\xi<-3a/2$, with probability $q_3$. The state 01 has the reversed roles.

For state 11, the noiseless contributions cancel and $h=\xi$. Concept 1 is missed unless $\xi>a/2$, hence its miss probability is $1-q$. Concept 2 is missed unless $\xi<-a/2$, also with probability $1-q$. The two errors need not be independent: linearity of expectation permits summing their weighted marginal probabilities. The weighted count may exceed one because it counts errors on two targets, not the probability of a single binary failure event.

The four input probabilities sum to one. Multiplying each conditional weighted error by its state probability and adding is the law of total expectation, which proves the pair-risk formula without assuming independent decoder outputs.
'''

clean_detail=r'''
\subsection{Comparing against the better monosemantic allocation}
For $p_1,p_2>0$ in the noiseless detector, beating the comparator retaining feature 1 requires $p_1<I_2/(I_1+I_2)$; beating the comparator retaining feature 2 requires $p_2<I_1/(I_1+I_2)$. Therefore
\begin{equation}R_p<\min(R_{m1},R_{m2})\quad\Longleftrightarrow\quad p_1<\frac{I_2}{I_1+I_2}\ \text{and}\ p_2<\frac{I_1}{I_1+I_2}).\end{equation}
The closing parenthesis on the right is omitted in the mathematical interpretation: the condition is the conjunction of the two strict inequalities. For equal frequencies $p$ and arbitrary weights, this becomes $p<\min(I_1,I_2)/(I_1+I_2)$. Equal weights yield $p<1/2$. If one feature is much more important, a mono code protecting it becomes preferable over a larger part of the frequency range. At $p_i=0$, the cancellation used in deriving the strict conditions is not available; direct risks determine ties and preferences.
'''
# Keep the equation itself clean: no commentary about a typesetting correction.
clean_detail=clean_detail.replace(r'\frac{I_1}{I_1+I_2}).',r'\frac{I_1}{I_1+I_2}.')
clean_detail=clean_detail.replace('The closing parenthesis on the right is omitted in the mathematical interpretation: the condition is the conjunction of the two strict inequalities. ','')

phase_code='''"""Exact pair-risk phase diagram; run with NumPy, SciPy and Matplotlib."""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ndtr
from scipy.optimize import brentq


def pair_risks(p1, p2, I1, I2, sigma, a, c=1.0):
    # sigma is positive here. At sigma=0 use the clean formulas.
    q = ndtr(-a / (2.0 * sigma))
    q3 = ndtr(-3.0 * a / (2.0 * sigma))
    qm = ndtr(-c / (2.0 * sigma))
    P00 = (1.0 - p1) * (1.0 - p2)
    P10 = p1 * (1.0 - p2)
    P01 = (1.0 - p1) * p2
    P11 = p1 * p2
    superposed = (
        (I1 + I2) * P00 * q
        + P10 * (I1 * q + I2 * q3)
        + P01 * (I1 * q3 + I2 * q)
        + P11 * (I1 + I2) * (1.0 - q)
    )
    mono1 = I1 * qm + I2 * p2
    mono2 = I2 * qm + I1 * p1
    return superposed, np.minimum(mono1, mono2)


def risk_gap(p, sigma, a):
    # Equal frequencies and equal importance in this figure.
    superposed, mono = pair_risks(p, p, 1.0, 1.0, sigma, a)
    return superposed - mono


def main():
    output = Path(__file__).resolve().parents[1] / "figures"
    output.mkdir(parents=True, exist_ok=True)
    probabilities = np.linspace(0.01, 0.80, 180)
    noise_levels = np.linspace(0.01, 1.50, 200)
    P, SIGMA = np.meshgrid(probabilities, noise_levels)
    controls = [
        ("Equal stored-feature amplitude", 1.0),
        ("Equal total encoder energy", 1.0 / np.sqrt(2.0)),
    ]
    fig, axes = plt.subplots(
        1, 2, figsize=(10.4, 4.1), constrained_layout=True
    )
    for ax, (title, amplitude) in zip(axes, controls):
        gap = risk_gap(P, SIGMA, amplitude)
        image = ax.pcolormesh(
            P, SIGMA, gap, cmap="RdBu_r", shading="auto",
            vmin=-0.30, vmax=0.30,
        )
        ax.contour(
            P, SIGMA, gap, levels=[0.0], colors="black",
            linewidths=1.6,
        )
        ax.set(
            xlabel="Activation probability p = 1 - s",
            ylabel="Code-noise standard deviation sigma",
            title=title,
        )
        crossing = brentq(
            lambda noise: float(risk_gap(0.20, noise, amplitude)),
            0.05, 1.50,
        )
        ax.plot(0.20, crossing, "ko", markersize=4)
        print(f"{title}: p=0.20 crossing sigma={crossing:.9f}")
    fig.colorbar(
        image, ax=axes,
        label="Risk(superposed) - risk(best mono); blue < 0",
    )
    fig.savefig(output / "pair_phase_controls.png", dpi=220)
    plt.close(fig)


if __name__ == "__main__":
    main()
'''
(DEST/'supplement/phase_diagram.py').write_text(phase_code,encoding='utf-8')

plot_text=r'''
\subsection{Reproducing and reading the phase diagram}
The following complete Python program evaluates the proved risk functions directly. It does not train a network, fit a curve to experimental outcomes or perform symbolic regression. Install NumPy, SciPy and Matplotlib in a Python environment and run \texttt{python supplement/phase\_diagram.py} from the source project. The program saves \path{figures/pair_phase_controls.png}.

\lstinputlisting[language=Python,caption={Exact evaluation of the two-feature risk and its zero-gap contour.},label={lst:pairphase}]{supplement/phase_diagram.py}

\paragraph{Inputs and outputs of \texttt{pair\_risks}.}
The inputs $p_1,p_2$ are presence probabilities; $I_1,I_2$ are penalties; $\sigma$ is Gaussian code-noise standard deviation; and $a,c$ are the pair and mono encoder amplitudes. \texttt{ndtr} is the standard normal CDF $\Phi$. The variables \texttt{q}, \texttt{q3} and \texttt{qm} implement the three tail probabilities. The next four variables implement the state probabilities. \texttt{superposed} is their weighted sum. \texttt{np.minimum(mono1, mono2)} selects the better of the two mono allocations rather than choosing one after seeing a preferred result.

\paragraph{Constructing the grid.}
\texttt{np.meshgrid} creates arrays containing every activation-probability/noise pair on the specified grid. Broadcasting evaluates the same closed-form risk at all points. All noise levels are positive; the clean limit is derived analytically rather than dividing by zero. The plot fixes $n=2,m=1$, equal frequencies and equal weights. It is a slice of the research tradeoff, not a solved phase diagram for arbitrary feature load or arbitrary learned networks.

\paragraph{Resource controls.}
In the left panel, $a=c=1$: every stored concept has the same amplitude, but the pair encoder has energy $\norm W_F^2=2$, compared with mono energy 1. In the right panel, $a=1/\sqrt2,c=1$: both encoder energies equal 1. The pair still represents two potential concepts, but each uses a weaker direction. The difference between panels shows how strongly the conclusion depends on a stated norm budget.

\paragraph{Colors and contour.}
The color is $\Delta R=R_p-\min(R_{m1},R_{m2})$. Blue means the superposed pair makes fewer importance-weighted feature errors; red means the specified mono family makes fewer. The black curve is $\Delta R=0$. Saturated colors show values clipped by the chosen color scale, not clipped risks. The white transition is equality of two risks, not a boundary between zero error and nonzero error. Both representations can fail on either side.

\paragraph{A reproducible numerical slice.}
The dot at $p=0.2$ marks a root found by \texttt{brentq}, which solves the already-derived equality rather than fitting an empirical law. The crossings are $\sigma\simeq0.658349502$ under equal amplitude and $\sigma\simeq0.279938913$ under equal total energy. Below the relevant crossing, retaining both concepts outweighs collision and noise costs for this slice; above it, protecting one direction has lower weighted risk. The horizontal coordinate is activation probability $p=1-s$, so moving right makes concepts more frequent, not sparser.

\fig{pair_phase_controls.png}{0.99}{Exact two-feature phase diagrams under equal stored-feature amplitude and equal total encoder energy. Gaussian code noise is ordinary statistical corruption; the figure is not an adversarial-attack guarantee. The black equality contour is evaluated from the analytic risks for fixed codes and thresholds.}

\subsection{Which phase diagram is established by this calculation?}
The pair calculation establishes a boundary for two specified codes and detector rules. A learned-geometry diagram asks a stronger question: which geometry is selected by the training objective as $p$, $n/m$ and importance decay vary, and whether its held-out risk crosses a capacity-controlled comparator. That question requires the geometry analysis and learned-toy experiments; the analytic plot gives a precise mechanism to test rather than a universal conclusion.
'''

relu_detail=r'''
\subsection{Derivation of the continuous-amplitude collision cost}
If both amplitudes are positive and $x_1\ge x_2$, the reconstruction is $(x_1-x_2,0)$, so both coordinate errors have magnitude $x_2$. For $x_2>x_1$, both have magnitude $x_1$. The weighted squared error is therefore $(I_1+I_2)\min(x_1,x_2)^2$ only on simultaneous activation. Conditional on that event, the amplitudes are independent uniform variables. Their minimum has survival probability $(1-t)^2$ for $0\le t\le1$, hence
\begin{align}\E\min(U_1,U_2)^2&=\int_0^1 2t(1-t)^2\,dt\\&=2\left(\frac12-\frac23+\frac14\right)=\frac16.\end{align}
The mono reconstruction of a dropped feature has squared error $x_2^2$ and expectation $p_2/3$. This gives the distinct reconstruction boundary. For equal frequencies and weights it favors the pair for every $0<p<1$ in the noiseless setting, whereas binary detection has crossing $p=1/2$. The difference is caused by the target and loss, not by a contradiction in the geometry.
'''

centering_detail=r'''
\subsection{The conditional means and the fluctuation variance}
Let $d_i=G_{ii}>0$ and $u_i=\sum_{j\ne i}G_{ij}p_j$. Independence of the input features gives
\begin{equation}\E(z_i\mid b_i=0)=u_i,\qquad \E(z_i\mid b_i=1)=u_i+d_i.\end{equation}
The midpoint threshold is $u_i+d_i/2$. Subtracting it from the score yields
\begin{equation}z_i-\theta_i=d_i(b_i-1/2)+\underbrace{\sum_{j\ne i}G_{ij}(b_j-p_j)}_{T_i}+\zeta_i.\end{equation}
For $b_i=0$, the detector fails when $T_i+\zeta_i>d_i/2$; for $b_i=1$, it fails when $T_i+\zeta_i\le-d_i/2$. This explicitly identifies the two one-sided tail events.

Every summand $X_j=G_{ij}(b_j-p_j)$ has mean zero, variance $G_{ij}^2p_j(1-p_j)$ and absolute value at most $|G_{ij}|\le B_i$. Since the summands are independent,
\begin{equation}\Var(T_i)=\sum_{j\ne i}G_{ij}^2p_j(1-p_j)=V_i.\end{equation}
The projected noise has variance $\Var(\zeta_i)=\sigma^2d_i$. Thus the total variance is $v_i=V_i+\sigma^2d_i$. The target's own frequency $p_i$ controls the mixture of class-conditional errors; the other frequencies control this nuisance variance.

\subsection{Bernstein's exponential-moment bound: the origin of $B_i/3$}
For a centered scalar $X$ with $|X|\le B$ and variance $v$, expand the moment-generating function:
\begin{equation}\E e^{\lambda X}=1+\sum_{k=2}^{\infty}\frac{\lambda^k\E X^k}{k!}.\end{equation}
The first-order term vanishes because $\E X=0$. For $k\ge2$, $\E|X|^k\le B^{k-2}\E X^2=B^{k-2}v$. The factorial inequality
\begin{equation}k!\ge2\,3^{k-2}\end{equation}
holds at $k=2$ and remains true by induction because the next multiplier is $k+1\ge3$. Therefore, when $|\lambda|B<3$,
\begin{align}\E e^{\lambda X}
&\le1+\frac{v\lambda^2}{2}\sum_{k=2}^{\infty}\left(\frac{|\lambda|B}{3}\right)^{k-2}\\
&=1+\frac{v\lambda^2}{2(1-|\lambda|B/3)}\\
&\le\exp\!\left(\frac{v\lambda^2}{2(1-|\lambda|B/3)}\right).
\end{align}
The denominator comes from an ordinary geometric series; the constant $1/3$ comes from the factorial bound. Multiplying the MGFs of the independent summands, or adding their logarithms, gives
\begin{equation}\log\E e^{\lambda T_i}\le\frac{\lambda^2V_i}{2(1-|\lambda|B_i/3)}.\end{equation}
The same calculation works for $-T_i$ because it uses an absolute bound.

\subsection{Adding the Gaussian MGF without losing the inequality direction}
A centered Gaussian with variance $\sigma^2d_i$ has MGF $\E e^{\lambda\zeta_i}=\exp(\lambda^2\sigma^2d_i/2)$, obtained by completing the square in its density. Independence gives
\begin{align}\log\E e^{\lambda(T_i+\zeta_i)}
&\le\frac{\lambda^2V_i}{2(1-|\lambda|B_i/3)}+\frac{\lambda^2\sigma^2d_i}{2}\\
&\le\frac{\lambda^2(V_i+\sigma^2d_i)}{2(1-|\lambda|B_i/3)}.
\end{align}
The second inequality is valid because $0<1-|\lambda|B_i/3\le1$: putting the Gaussian term over this smaller positive denominator makes the upper bound larger. It does not change the actual variance $v_i$. The denominator tends to one as $\lambda\to0$, so the bound retains the correct small-$\lambda$ variance scale rather than replacing it by an infinite or arbitrary constant.

\subsection{Chernoff's inequality and a specific admissible choice}
For $t>0$ and $\lambda>0$, Markov's inequality applied to $e^{\lambda(T_i+\zeta_i)}$ gives
\begin{equation}\Prb(T_i+\zeta_i\ge t)\le\exp\!\left(-\lambda t+\frac{v_i\lambda^2}{2(1-c_i\lambda)}\right),\qquad c_i=B_i/3,\quad c_i\lambda<1.\end{equation}
Choose $\lambda=t/(v_i+c_it)$ when $v_i>0$. This is admissible because $c_i\lambda=c_it/(v_i+c_it)<1$. Also $1-c_i\lambda=v_i/(v_i+c_it)$, so substitution gives
\begin{align}-\lambda t+\frac{v_i\lambda^2}{2(1-c_i\lambda)}
&=-\frac{t^2}{v_i+c_it}+\frac{t^2}{2(v_i+c_it)}\\
&=-\frac{t^2}{2(v_i+c_it)}.
\end{align}
The same upper bound holds for the negative tail. This proves the rational Bernstein tail expression by an explicit feasible choice; it need not be the exact minimizing $\lambda$.

\subsection{The exact optimizer of this MGF upper bound}
For $c_i>0,v_i>0$, differentiating the displayed exponent gives the stationary condition
\begin{equation}t=\frac{v_i\lambda(2-c_i\lambda)}{2(1-c_i\lambda)^2}.\end{equation}
Writing $u=1-c_i\lambda$ solves it as
\begin{equation}\lambda_* =\frac1{c_i}\left(1-\sqrt{\frac{v_i}{v_i+2c_it}}\right).\end{equation}
The resulting bound is
\begin{equation}\Prb(T_i+\zeta_i\ge t)\le\exp\!\left[-\frac{v_i}{c_i^2}\left(1+\frac{c_it}{v_i}-\sqrt{1+\frac{2c_it}{v_i}}\right)\right].\end{equation}
It is at least as sharp as the feasible-choice bound because it minimizes the same upper-bound exponent. Neither bound is the exact tail probability. For $v_i=c_i=t=1$, the exponents are $-(2-\sqrt3)$ and $-1/4$; their difference is about 0.01795. Its size depends on the parameters and is not universally negligible. The rational expression is useful because its feature-error condition can be rearranged transparently.

\subsection{From the tail bound to feature error: why $B_i/6$ appears}
Set $t=d_i/2$. The tail denominator contains $B_it/3=B_id_i/6$. The squared numerator is $t^2=d_i^2/4$, giving
\begin{equation}U_i=\exp\!\left[-\frac{d_i^2}{8(V_i+\sigma^2d_i+B_id_i/6)}\right].\end{equation}
Each conditional error is bounded by $U_i$. Therefore
\begin{equation}e_i=(1-p_i)e_{i,0}+p_ie_{i,1}\le(1-p_i)U_i+p_iU_i=U_i.\end{equation}
There is no factor two: this is a weighted average of two class-conditional errors, not a union of both tails for the same class. If $v_i=0$, then the fluctuation is zero almost surely, and the deterministic positive-margin detector has no error.

\subsection{Meaning and usefulness of a sufficient region}
For $0<\delta<1$, demanding $U_i\le\delta$, taking logarithms and rearranging yields
\begin{equation}V_i+\sigma^2d_i+B_id_i/6\le\frac{d_i^2}{8\log(1/\delta)}.\end{equation}
When this inequality holds, $e_i\le\delta$ follows under the stated assumptions. When it fails, the bound has not certified the target; the true detector may still meet it. For an isolated unit-norm feature with $\sigma=0.2$, the exact midpoint error is $\Phi(-2.5)\simeq0.00621$, whereas the Gaussian Chernoff bound is $\exp(-3.125)\simeq0.04394$. The bound certifies a 5-percent target but not a 1-percent target, even though the exact error meets both. This example shows both finite usefulness and conservatism.
'''

random_detail=r'''
\subsection{Deriving the random-dictionary expectation}
Condition on a unit direction $w_i$ and rotate coordinates so that it is the first basis vector. An independent uniformly random unit direction $w_j$ then has $w_i^\top w_j=(w_j)_1$. Rotational symmetry makes every coordinate have the same second moment. Since $\sum_{k=1}^m(w_j)_k^2=1$,
\begin{equation}m\E(w_j)_1^2=1,\qquad \E G_{ij}^2=\frac1m.\end{equation}
Linearity of expectation gives $\E_W V_i=m^{-1}\sum_{j\ne i}p_j(1-p_j)$ without requiring squared overlaps within a row to be independent. The expectation is over dictionaries, not over the already-fixed test geometry. In particular, substituting $\E_WV_i$ into an exponential error bound does not produce a guarantee for each dictionary; expectation and a nonlinear function cannot generally be interchanged.

For a deliberately conservative random-dictionary statement, Markov's inequality gives $\Prb_W\{V_i>\E_WV_i/\delta_G\}\le\delta_G$. A sharper concentration analysis may improve this, and a trained dictionary requires analysis of its training-induced geometry. Directly measuring $V_i$ uses the conditional bound without that additional random-dictionary step.

\subsection{Deriving the capacity constraint from the spectrum}
Let the $r$ nonzero eigenvalues of $G$ be $\lambda_1,\ldots,\lambda_r$. Unit columns imply $\tr G=n$, and $r\le m$. Cauchy--Schwarz gives
\begin{equation}n^2=\left(\sum_{k=1}^r\lambda_k\right)^2\le r\sum_{k=1}^r\lambda_k^2=r\tr(G^2)\le m\tr(G^2).\end{equation}
Because $G$ is symmetric, $\tr(G^2)=\sum_{i,j}G_{ij}^2$. The $n$ diagonal entries each contribute one, so subtracting them gives the average off-diagonal bound. Equality at $r=m$ requires equal nonzero eigenvalues $n/m$, the tight-frame case. A lower bound on average squared overlap is not an upper bound on any row's error or a rule fixing which concepts interfere.

\subsection{Squared overlap and the largest interference term}
The sum $\sum_{j\ne i}G_{ij}^2$ measures total squared overlap; it is not itself a maximum or a tail probability. For equal nuisance activation rates, one overlap $a$ and four overlaps $a/2$ give the same $V_i$ but different $B_i$. Their interference distributions differ because one permits a larger individual jump. The Bernstein expression keeps both quantities: the variance controls aggregate fluctuations and $B_i$ controls a bound on individual jumps. Actual rare-event probabilities also depend on the joint activation law.
'''

geometry_detail=r'''
\subsection{Correlated concepts: use conditional means and covariances}
For correlated input features, let $p_{j\mid c}=\Prb(b_j=1\mid b_i=c)$ and let $C_{-i\mid c}$ be the covariance matrix of the remaining features conditional on $b_i=c$. Then
\begin{align}m_{i,c}&=\E(z_i\mid b_i=c)=G_{ii}c+\sum_{j\ne i}G_{ij}p_{j\mid c},\\
v_{i,c}&=G_{i,-i}C_{-i\mid c}G_{i,-i}^\top+\sigma^2G_{ii}.\end{align}
The covariance term contains both diagonal conditional variances and off-diagonal conditional covariances. Using unconditional variances in the first term and conditional covariances in the second would mix two different distributions. The separation of the class means is
\begin{equation}m_{i,1}-m_{i,0}=G_{ii}+\sum_{j\ne i}G_{ij}(p_{j\mid1}-p_{j\mid0}).\end{equation}
It need not equal $G_{ii}$. Conditional nuisance distributions need not be Gaussian, so these first two moments alone do not determine the exact error. The finite-state risk remains available for a specified joint law, while an independence-based Bernstein argument needs replacement or additional assumptions.

\subsection{A tractable family for feature load between one and two}
Use $m$ mutually orthogonal latent coordinates. Let $k$ coordinates each store an antipodal pair, and let the other $m-k$ coordinates store an isolated feature. The total number of features is $n=(m-k)+2k=m+k$, so $n/m=1+k/m\in[1,2]$. The Gram matrix is block diagonal. Weighted detection risk adds the isolated-feature risks and the pair risks:
\begin{equation}R=\sum_{\ell\in\mathcal S}I_\ell\Phi\!\left(-\frac{c_\ell}{2\sigma}\right)+\sum_{(i,j)\in\mathcal P}R_p(p_i,p_j,I_i,I_j,\sigma;a_{ij}),\end{equation}
where $\mathcal S$ is the isolated set and $\mathcal P$ is the paired set. A total-energy constraint takes the explicit form $\sum_{\ell\in\mathcal S}c_\ell^2+2\sum_{(i,j)\in\mathcal P}a_{ij}^2=E_{\rm enc}$. Changing the number of pairs without controlling this energy would confound feature load with signal amplitude. This block family gives exact load-dependent comparisons, but it does not cover loads greater than two or prove global optimality among all dictionaries.

\subsection{What must be solved to obtain a learned phase diagram}
For a tied nonlinear autoencoder, one possible population objective is
\begin{equation}\mathcal L(W,d;P,I)=\E_{b\sim P}\sum_i I_i\left[b_i-\ReLU((W^\top Wb)_i+d_i)\right]^2,\end{equation}
subject to stated norm and capacity constraints. Here $d_i$ is a decoder bias, distinct from the diagonal notation used in the fluctuation calculation. The bias can instead be denoted $\beta_{\rm dec,i}$ when both calculations are used together. A smooth-point derivative is
\begin{equation}\frac{\partial\mathcal L}{\partial\omega}=-2\sum_iI_i\E\left[(b_i-\hat b_i)\frac{\partial\hat b_i}{\partial\omega}\right],\end{equation}
for an encoder or decoder parameter $\omega$. Importance changes the optimization force, not merely the final evaluation weight. Frequency changes the sampling law inside the expectation. A closed-form boundary expressed only in $(p,n/m,\gamma)$ requires a characterization of the selected geometry, its optimization assumptions and its decoder, rather than substituting an average load for the measured overlaps.

The immediate test is conditional: given a trained $W$, does the exact risk or bound predict held-out feature errors under a specified corruption? The stronger test is structural: do changes in sparsity, load and importance select geometries with the predicted risk tradeoff? These retain the monosemanticity motivation of the source paper while making the mathematical contribution and empirical requirements explicit.
'''

# Insert the detailed discussion at the point where its definitions are used.
extension=extension.replace(r'\section{Three noise locations}',setup+'\n'+r'\section{Three noise locations}')
extension=extension.replace(r'\section{Alignment of a tied readout with a feature axis}',margin_detail.split(r'\subsection{Deriving the alignment ratio')[0]+'\n'+r'\section{Alignment of a tied readout with a feature axis}')
extension=extension.replace(r'\section{It is a matched readout, not always the optimal readout}',r'\subsection{Deriving the alignment ratio'+margin_detail.split(r'\subsection{Deriving the alignment ratio',1)[1]+'\n'+r'\section{It is a matched readout, not always the optimal readout}')
extension=extension.replace(r'\section{Interpretation: perturbations, sign, frequency and scale}',ls_detail+'\n'+r'\section{Interpretation: perturbations, sign, frequency and scale}')
extension=extension.replace(r'\section{An isotropic example with no distributional advantage}',recon_detail+'\n'+r'\section{An isotropic example with no distributional advantage}')
extension=extension.replace(r'\section{Why nonlinear decoding is needed for the tradeoff}',frame_detail+'\n'+r'\section{Why nonlinear decoding is needed for the tradeoff}')
extension=extension.replace(r'\section{Frequency, importance and capacity in the risk}',detector_detail+'\n'+r'\section{Frequency, importance and capacity in the risk}')
extension=extension.replace(r'\section{Defining the phase boundary}',bayes_detail+'\n'+r'\section{Defining the phase boundary}')
extension=extension.replace(r'\section{The clean boundary in closed form}',pair_detail+'\n'+r'\section{The clean boundary in closed form}')
extension=extension.replace(r'\section{Noise moves the boundary}',clean_detail+'\n'+r'\section{Noise moves the boundary}')
extension=re.sub(r'\\fig\{pair_phase_equal_energy.png\}[^\n]*',lambda m:plot_text,extension)
extension=extension.replace(r'\section{Scope of the solved pair and the learned-geometry question}',relu_detail+'\n'+r'\section{Scope of the solved pair and the learned-geometry question}')
extension=extension.replace(r'\section{A robust region with an operational threshold}',centering_detail+'\n'+r'\section{A robust region with an operational threshold}')
extension=extension.replace(r'\section{Importance, correlations and learned geometry}',random_detail+'\n'+r'\section{Importance, correlations and learned geometry}')
extension=extension+geometry_detail

# Conversion keeps the article's original section numbers and appends six sections.
extension=extension.replace(r'\subsection{',r'\subsubsection{').replace(r'\section{',r'\subsection{').replace(r'\chapter{',r'\section{')
extension=extension.replace('Chapter 4','Section 16').replace('Chapter 5','Section 17').replace('next chapters','following sections')
extension=extension.replace('this chapter','this section').replace('This chapter','This section')
extension=extension.replace(r'\lesson{',r'\extensionfocus{')
extension=extension.replace('The next experiments should','Experiments should').replace('The next chapters do this.','The feature-detection sections retain this nonlinear mechanism.')

initial=initial.replace('Reading Notes on Zhang et al. (ICLR 2025)','Reading Notes and Project 1 Derivations')
initial=initial.replace('September 2026','October 2026')
initial=initial.replace('Both arXiv:2410.21331v1 and the ICLR 2025 proceedings version are considered.','Both arXiv:2410.21331v1 and the ICLR 2025 proceedings version are considered. The continuation develops feature-detection risk, a resource-controlled superposition phase diagram, and a general interference bound, with detailed proofs and executable Python code.')
initial=initial.replace('The companion research notes develop this approach for a small feature-detection model.','Sections 13--18 develop this approach for a small feature-detection model.')
initial=initial.replace('The companion research notes develop this connection with exact toy formulas, a transition operator and a coupling bound. It then explains what needs to be checked in a diffusion model.','The feature-detection derivations in Sections 13--18 establish the immediate-risk side of this program. A recursive-training operator and a validated diffusion connection require a separate extension; they are not inferred from the fixed-geometry formulas.')
initial=initial.replace(r'\newcommand{\lesson}',r'\newcommand{\lesson}')
initial=initial.replace(r'\begin{document}',r'\newcommand{\extensionfocus}[1]{\par\noindent\textit{Objective: #1}\par}'+'\n'+r'\begin{document}')
initial=initial.replace('The notes do not reproduce every bibliography entry or every plotted individual data point; it covers','The notes do not reproduce every bibliography entry or every plotted individual data point; they cover')
extension=extension.replace('sparsity-dependent tradeoff.\n\\checkpoint','sparsity-dependent tradeoff.\n\\checkpoint')

# Avoid symbol reuse between a Gram diagonal and a learned decoder bias.
extension=extension.replace(r'\mathcal L(W,d;P,I)',r'\mathcal L(W,\beta_{\rm dec};P,I)')
extension=extension.replace(r'(W^\top Wb)_i+d_i',r'(W^\top Wb)_i+\beta_{\rm dec,i}')
extension=extension.replace('Here $d_i$ is a decoder bias, distinct from the diagonal notation used in the fluctuation calculation. The bias can instead be denoted $\\beta_{\\rm dec,i}$ when both calculations are used together.','Here $\\beta_{\\rm dec,i}$ is a learned decoder bias, distinct from the Gram diagonal $d_i=G_{ii}$.')

original_appendix=original_appendix.replace('The paper\'s main argument is covered in Sections 1--6.','The paper\'s main argument is covered in Sections 1--6. The research extension occupies Sections 13--18.')
original_appendix=original_appendix.replace('it covers every substantive','they cover every substantive')
original_appendix=original_appendix.replace('References and provenance','References')
original_appendix=original_appendix.replace(r'$T$ & Contrastive temperature; unrelated to recursive generations.\\',r'''$T$ & Contrastive temperature; unrelated to recursive generations.\\
$b_i,p_i,s_i$ & Binary concept presence, its activation probability, and $1-p_i$.\\
$\theta_i$ & Feature-detection threshold in the matched score.\\
$\Phi,\phi$ & Standard Gaussian CDF and density.\\
$M_i$ & Gram-row alignment, defined for $G_{ii}>0$.\\
$\beta,c$ & Effective linear readout and scalar decision threshold.\\
$N,N_x$ & Noise covariances in the specified code or feature space.\\
$a,c$ in the pair model & Superposed and mono encoder amplitudes.\\
$q,q_3,q_m$ & Gaussian error tails for the pair and mono codes.\\
$T_i,V_i,B_i$ & Centered nuisance interference, its variance and a largest-term bound.\\
$d_i,v_i,c_i$ in the tail proof & $G_{ii}$, $V_i+\sigma^2G_{ii}$ and $B_i/3$.\\
$\delta,\delta_G$ & Desired error upper bound and random-geometry failure probability.\\
$\beta_{\rm dec,i}$ & Learned decoder bias, distinct from a Gram diagonal.\\''')
insert=r'''
% BEGIN PROJECT 1 EXTENSION
\clearpage
The continuation develops the first research question under an explicit feature-detection model. It connects the paper's representation-level motivation to operational prediction errors, then derives a two-feature phase diagram and an interference bound for larger dictionaries. The six sections retain the progression from definitions to exact toy calculations to the learned-geometry question.
'''+extension+'\n% END PROJECT 1 EXTENSION\n'
result=initial+insert+r'\appendix'+'\n'+original_appendix+r'\end{document}'+'\n'
for phrase in ['Recovering the old expression','earlier proposed boundary','earlier margin','Volume I','Volume II','Project 2: the correct meaning']:
    assert phrase not in result,phrase
assert result.count(r'\section{')==20, result.count(r'\section{') # 18 main, 2 appendices
assert '\\section{Project 1: load, interference and a general bound}' in result
TARGET.write_text(result,encoding='utf-8')
(DEST/'README.md').write_text('''# Monosemanticity and Robustness: Research Notes

Compile main.tex with pdfLaTeX (two or three passes). This is the continued article:
Sections 1--12 analyze Zhang et al.; Sections 13--18 cover the first six research
derivation chapters through Project 1's load, interference and general bound.
Project 2 derivations are not appended.

The exact phase-diagram Python program appears in the document and in
supplement/phase_diagram.py. It requires NumPy, SciPy and Matplotlib and writes
figures/pair_phase_controls.png. All figures required for compilation are included.
The plotted boundary is an equality of proved fixed-code risks, not a fitted law or
a universal learned-network guarantee. Source-material clarification questions are
incorporated as self-contained definitions, proofs and worked examples.
''',encoding='utf-8')
print(json.dumps({'tex':str(TARGET),'characters':len(result),'main_sections':18,'appendix_sections':2}))
