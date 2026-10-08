# GO design: one controlled learned-vision phase comparison

7 October 2026 UTC. Prospective mathematical design, before any image generation, model training, score extraction or new risk evaluation. This is an AI mathematical review collaborating with the experiment reviewer. It does not report a completed experiment or promise a favorable result.

## One central next step

**GO, subject to root's prospective implementation review:** recover two independent planted visual factors using a learned image model, clean-train the original energy-one scalar tied-ReLU compression on its soft scores, and test the pre-existing finite mono-versus-sharing reversal at p=.5, equal importance, and Gaussian code standard deviations 0 and .30.

This is a controlled visual instantiation of the learned-perception/compression pipeline. It is not native ResNet transfer, semantic discovery in arbitrary hidden channels, diffusion or a test of the 3/2 critical exponent. Controlled factors are deliberate: they provide the assumptions and independent ground truth that the previous continuous correlated pairs lacked. Scores must remain soft outputs of the image model; inserting labels or hard-thresholding scores into the compressor is prohibited.

The pre-existing dense global theorem gives L*=.246425565098879 for the ideal independent bits, versus mono loss .25. Archived oracle-calibrated comparisons give ideal Delta(0)=-.003574434901 and Delta(.30)=+.005425102707. These finite margins make approximate learned recovery testable; tiny near-critical O(epsilon^3) margins would require implausibly exact image recovery under the short runtime budget.

## Fixed-target coupling bound, with derivation

Let X in {0,1}^2 be the planted independent fair bits. Let r(I) in [0,1]^2 be soft learned scores from the corresponding generated image I. Their joint law is a coupling of the ideal factors and recovered factors, not an assumption that the scores themselves are independent or binary. Use squared encoder energy one, G=w w^T, positive importance matrix D=diag(I1,I2), and the same scalar standard Gaussian Z for both compared evaluations. The target remains the planted X in both worlds:

F_r=D^(1/2)[ReLU(G r+b+sigma w Z)-X],

F_X=D^(1/2)[ReLU(G X+b+sigma w Z)-X].

Coordinatewise ReLU is 1-Lipschitz, so pointwise

||F_r-F_X|| <= sqrt(Imax) ||G(r-X)||.

Define d_w^2=Imax E||G(r-X)||^2 and delta^2=E||r-X||^2. Since ||G||op=||w||^2=1, d_w<=sqrt(Imax)*delta. Minkowski and the reverse triangle inequality in L2 yield

|sqrt(R_r(w,b,sigma))-sqrt(R_X(w,b,sigma))| <= d_w <= sqrt(Imax)*delta.

This holds uniformly in biases and noise level, for each fixed encoder. It does not use an independence assumption about recovered scores and does not compare against scores as their own targets. Equal importance makes Imax=1.

The corresponding fixed-model risk enclosure is

max(0,sqrt(R_X)-d_w)^2 <= R_r <= (sqrt(R_X)+d_w)^2.

For sharing and mono, denote the two ideal risk square roots by a_s,a_m, and their coupling radii by d_s,d_m. Then the real-image factor-reconstruction difference belongs to

[max(0,a_s-d_s)^2-(a_m+d_m)^2,
 (a_s+d_s)^2-max(0,a_m-d_m)^2].

A negative upper endpoint certifies sharing's advantage on the declared coupled distribution; a positive lower endpoint certifies mono's advantage. Numerical global calibration gaps and moment-evaluation tolerances must additionally be propagated through these enclosures. These are ordinary coupling inequalities used to check applicability, not advertised as the novel phase theorem.

If each world separately optimizes its biases, the root-risk inequality remains valid after taking infima over biases in both directions, because its bound is uniform in b. For actual finite-calibration fitted biases, use the exact four-state ideal risk evaluated at those realized biases; do not substitute an oracle bias or infer held-out guarantees from calibration accuracy alone.

## Actual clean training, including an optimization-error bound

The compressor must actually be fitted on TRAIN soft image scores r against their true planted X, with the original energy and decoder restrictions. Applying canonical theoretical weights and calling them learned is prohibited. Keep soft-score preprocessing fixed; do not normalize away reconstruction error with labels.

On state-balanced TRAIN groups, define L_r(w,b) as their four-state weighted clean empirical risk. The ideal comparison law has precisely p=.5, so its global clean optimum is the already proved L*. If delta_train is the measured TRAIN recovery L2 error, the uniform bound gives

inf_(w,b) sqrt(L_r(w,b)) >= max(0,sqrt(L*)-delta_train).

Therefore, for any actually fitted candidate (w_hat,b_hat),

0 <= L_r(w_hat,b_hat)-inf L_r
 <= L_r(w_hat,b_hat)-max(0,sqrt(L*)-delta_train)^2.

This is an explicit upper bound on empirical clean optimization excess, derived from the known ideal global theorem and observed recovery error. It does not assert that a finite angular optimizer is globally exact. It does not imply native image-population optimality.

In addition to the unchanged finite angular resolution/bias-profiling checks, gate this bound at 1.5e-3. Gate delta_train and delta_calibration at 5e-4. A bound that is negative beyond declared arithmetic slack indicates a code/math inconsistency and stops the run; it cannot be silently clipped into a success.

The mono class includes both coordinate orientations. Select its orientation on clean TRAIN loss with a predetermined deterministic tie rule, then freeze that orientation for noisy comparisons. Both comparators receive the same scalar noise and may independently calibrate their biases on CALIBRATION at each prescribed sigma. Do not choose the mono orientation using held-out outcomes.

## Realized-parameter predictions before test outcomes

After TRAIN compression and CALIBRATION bias fits, evaluate the existing exact Gaussian four-state risk formula at the ACTUAL fitted encoders and biases. This avoids assuming that small training loss alone gives canonical weights or a canonical gate pattern. Preserve these parameters, numerical gaps, hashes and ideal sign predictions in a prediction artifact before evaluating TEST model scores or risks.

Using d_s=d_m=5e-4 as the predeclared recovery allowance, require the transported predicted interval to be strictly negative at sigma0 and strictly positive at sigma.30, with each sign separated from its numerical gap. Stop if either enclosure is unresolved or has the wrong sign; do not add noise, change p, select another sign branch by outcomes, alter the feature generator or repair the training seed. Canonical margins motivate the protocol, but the realized parameters and propagated bounds determine its eligibility.

Only then evaluate TEST images once. Use four equally weighted planted-state strata and independent nuisance draws. Compute the actual soft-score recovery delta_test, realized-parameter per-state coupling radii, Gaussian conditional risks and comparison enclosures. Require delta_test<=5e-4; otherwise report failed recovery/applicability. Held-out coupling bounds describe the specified finite TEST distribution. They do not prove a uniform bound over all nuisance images or the entire unknown generated population.

## Why perception is substantive, and the ceiling of the claim

The image model must learn to recover factors despite independent background, contrast, texture and small-position nuisance. Compression receives only its soft scores, with recovery errors measured and propagated. Thus a result is not obtained by substituting perfect factor labels into a Bernoulli script. Failure of feature recovery, numerical clean selection, sign prediction or held-out verification is a real possible outcome and must remain in the record.

If all gates pass, the strongest claim is: **the pre-existing finite clean-versus-noisy comparison predicts a reversal in an actually learned, controlled visual-factor reconstruction pipeline within quantified perception and optimization errors.** This supports controlled applicability of the phase mechanism. It is not evidence of the near-transition 3/2 exponent, spontaneous monosemanticity discovery, native large-model robustness, or general adversarial safety. It is supporting evidence for the existing theoretical contribution, not a new main mathematical result or a guaranteed strong conference paper.

## Scope and stopping

Use exactly one generator, one image architecture, one seed, one training run, two code-noise levels and no postfailure substitutions. The experiment reviewer supplies concrete image/model sizes, seed, optimizer and runtime limits; root must review their prospective protocol before execution. Recommended overall wall-clock cap is 600 seconds, including a 300-second maximum image-training budget. If any prerequisite fails, save its failure and stop this experiment. Do not reopen either old real pair, add a high-noise forced crossing, or start diffusion/LLM/SAE work in parallel.

This full supporting derivation must be integrated into the existing derivation PDF by root before it is presented as delivered mathematics. No scientific result is claimed by this design file alone.
