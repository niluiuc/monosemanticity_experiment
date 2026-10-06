# Independent toy teacher review: bounded angle diagnostic

6 October 2026. The student ran the two deterministic cases specified in
`../followup_protocol.md`. This review independently checks the result rather
than selecting a favorable seed or repeating a parameter search.

## Verdict and credit

The student correctly addressed the reviewed coordinatewise projected-Adam
blocker using the same objective and energy, exact fixed-geometry bias minima
and a profiled angle step. Both cases followed the proven importance descent
direction and met the prespecified angle-gradient threshold. The implementation
and saved numerical claims pass the independent checks. No material numerical
repair is required.

In particular, the student did not turn the improved reconstruction into an
unsupported claim of better detection. The p=.20 result is unfavorable to such
a claim and was reported as such. This is good scientific reporting, not a
failure to obtain the preferred narrative.

## Independent verification

`verify_angle.py` verified all 21 raw-run hashes, all 1,959 recorded iterates and
all 60 model/detector/noise risk rows. At every iterate, it recomputed the
population reconstruction loss, all sixteen possible active masks for each
feature's globally optimal bias, and the angle derivative directly from
`dz_i/dtheta = (b dot w') w_i + (b dot w) w_i'`.

It checked the angle updates, Armijo sufficient decrease, energy constraint,
stopping gradient and agreement with the independently reviewed initial
importance derivative. Scalar-latent Gaussian integration independently
recomputed every reported feature error, FP and FN probability.

Maximum discrepancies: bias-minimum loss 6.94e-18; angle gradient 4.17e-17;
objective 2.78e-17; detection probabilities 2.78e-16; encoder energy 2.23e-16.
No Armijo violation or other error was observed. Results are saved in
`angle_verification.json`.

## Recorded outcomes

| p | Accepted updates | Final angle | Clean weighted MSE | Absolute angle gradient |
|---|---:|---:|---:|---:|
| .05 | 1,279 | -.5745808452382377 | .0177428805413465 | 9.978e-9 |
| .20 | 678 | -.41625677289385893 | .0777520825162945 | 9.792e-9 |

Weights are [1,.5], and the encoder energy is one. The clean monosemantic MSEs
are .02375 and .08 respectively. The fixed starting pair, all original v1 seeds
and its unfavorable results remain archived separately.

The trajectories change their ReLU-active masks once each. The recorded
iterates/trials did not have sampled numerical bias ties or near-zero activation
kinks. This does not mean the mathematical objective is globally smooth or that
all alternative starts have been tested.

## Limits and bounded direction

Stationarity from one start is not global optimality. The low-p mathematical
certificate, if separately proved, can establish optimality of one case;
the numerical solver itself cannot. Neither this test nor its agreement with
the importance derivative solves the general load/frequency/importance phase
diagram or establishes publication novelty.

The p=.20 improved code ties the clean-selected mono detector at zero noise and
has higher actual-decoder detection error at every positive tested noise level.
Reconstruction is the training objective; detection is a separately defined
evaluation. Both must remain explicit in the paper's claim.

No further optimizer configurations, extra seeds or model families are needed
to validate this bounded solver diagnostic. Next work should be selected from
the remaining theorem requirements after integrating the mathematical review.
