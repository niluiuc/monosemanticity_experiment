# At least two noisy-detection crossings for one clean-selected geometry

6 October 2026. This uses only the already globally certified p=1/20, importance [1,1/2], two-feature / one-dimension, energy-one toy model and the already tested sigma=3/10. No new frequency, noise setting or training is introduced.

Status: calculation and [independent teacher review](teacher_noise_sign_review.md) completed and approved. The student's turn was interrupted by a tool usage limit after source/results were saved. Root completed the exposition from those files; no certificate result was replaced. The teacher reproduced the certificate into a separate directory and independently checked all eight state calculations.

## The statement

Let R_shared(sigma) be the importance-weighted actual-decoder detection error of the globally clean-selected sharing solution, and let R_mono(sigma) be that of the clean-preferred mono control. Set Delta=R_shared-R_mono. The certificate establishes

\[
\Delta(0)=\frac1{400}>0,\qquad
\Delta(3/10)<0,\qquad
\lim_{\sigma\to\infty}\Delta(\sigma)=\frac9{40}>0.
\]

Every clean state has a strict threshold gap for the selected code, so the positive-noise Gaussian risk tends continuously to its clean error as sigma decreases to zero. The error is continuous for sigma>0. The intermediate value theorem therefore gives at least one root in (0,3/10) and at least one in (3/10,infinity): **at least two distinct positive noise crossings**.

This proves a nonmonotone comparison with mono. It does not prove there are exactly two roots, nor certify the numerical root locations .207955... and .625275.... It also does not prove the same result at other frequencies.

## Geometry and biases

The globally selected root t* is the certified negative root of

\[
380t^3+14800t^2-1140t-6839=0
\]

in the rational isolating interval saved in `../toy/run_v1/p_0.050/certificate_summary.json`. The encoder is (1,t*)/sqrt(1+t*²), with clean-optimal biases

\[
\beta_1=\frac{20t^{*2}-t^*}{381(1+t^{*2})},\qquad
\beta_2=\frac1{20(1+t^{*2})}.
\]

The strong concept misses the coactivation state, of probability p²=1/400. The weak concept is never detected and contributes weighted error p/2=1/40. Thus the clean sharing error is 11/400, versus mono's 1/40, proving the displayed clean difference exactly. The general infinite-noise argument in `../noise_limits.md` gives 1/4-p/2=9/40.

## Exact finite-noise sign certificate

`certify_noise_sign.py` propagates rational intervals for t*, Gram entries, biases, encoder norms and all eight state/feature Gaussian arguments. Square roots are enclosed by integer arithmetic: floor(sqrt(x)*10^d)/10^d and the next rational grid point enclose sqrt(x).

The Gaussian CDF is monotone, so an argument interval can be rounded outward and evaluated at its endpoints. For x>=0,

\[
\Phi(x)=\tfrac12+\frac1{\sqrt{2\pi}}\int_0^x e^{-u^2/2}\,du.
\]

Taylor's theorem gives an upper bound on exp(-v) with an even-degree polynomial and a lower bound with the following odd-degree polynomial, for v>=0. Integrating those two polynomials gives rational bounds on the integral. The script uses degrees 80 and 81. Negative arguments use Phi(-x)=1-Phi(x).

The normalizing constant is enclosed from Machin's identity

\[
\pi=16\arctan(1/5)-4\arctan(1/239).
\]

For 0<x<1, the arctangent alternating series has decreasing terms; even partial sums and the following odd partial sums bound it. The tangent addition formula gives tan(4 arctan(1/5)-arctan(1/239))=1. This angle is positive and below .8, while pi/2>1, so it equals pi/4, establishing the identity in the correct quadrant.

All sign decisions use rational arithmetic. Decimal values are display approximations only. Full per-state probability and margin/CDF bounds, the geometry-source hash, risk bounds and the strictly negative difference bound are preserved in `noise_sign_certificate_results.json`.

The saved rational enclosure for Delta(3/10), displayed approximately, is

\[
[-0.014474506712828471,\;-0.014474506712749220].
\]

The whole interval is negative. The independent 100-digit reference value, approximately -0.0144745067127706407821, lies inside it. That reference is a crosscheck; the proof of the sign uses the rational enclosure. The independent checks and reproduction records are saved in `teacher_noise_sign_check_results.json` and `teacher_noise_sign_reproduction/`.

## Reproduce and limits

The script writes beside itself. To preserve the original result, reproduce through an import with HERE redirected to a fresh folder while leaving CERTIFICATE pointing to the saved source geometry, or use the teacher's separate reproduction procedure. Python standard-library rational/integer arithmetic and SymPy are sufficient.

The finite noise-risk sign is computer-assisted. Its argument relies on the previously reviewed global clean-geometry certificate. Publication novelty, higher feature load and real-model behavior remain separate research questions.
