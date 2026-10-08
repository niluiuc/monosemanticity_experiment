# Review of the learned four-concept comparison

The run follows the lecture's detection-risk comparison: same dimension and encoder energy, known independent binary concepts, midpoint matched detectors, Gaussian code noise, and dropped-concept errors included. It does not substitute class purity or compare different real-network training methods.

Reconstruction training and detection evaluation are different operations. The clean tied-ReLU reconstruction objective chooses the encoder; the lecture's fixed detector evaluates it. The learned reconstruction biases are not its detection thresholds. All settings were stated before execution. This tests whether a geometry selected by that clean objective also exhibits the detection tradeoff, not whether it globally optimizes detection.

At p=.10 and .20, seeds 0 and 1 approach two orthogonal antipodal pairs. Their numerical risk crossings closely match the fixed-pair control. This verifies that the pictured mechanism can arise from clean learning in this four-concept model. It is not a new arbitrary-load law: two independent identical pairs add two copies of the existing risk, so the zero stays at the same noise value.

Seven of fifteen runs pass the saved loss-stability diagnostic; the remaining eight are kept and labelled unstable under that diagnostic. Even a stable loss is not a stationarity certificate. Numerical final encoders and their conditional risks remain valid objects to inspect, but unstable runs do not establish optimal storage selection. Seed 2 at p=.20 has no strict clean advantage. The p=.50 cases show different branches and at p=.70 no root is detected on the prescribed grid.

For p>.50, the zero-output omitted-concept rule is intentionally the lecture's baseline, but is worse than predicting presence using the known prior. The high-frequency plots must not be presented as an optimal Bayes comparison. Comparisons including all dropped concepts are necessary; this particular output rule remains a modelling choice.

Risk verification recomputes all 2265 learned-geometry grid values by an explicit conditional-state loop, mono values from a scalar normal tail, and fixed pair values from the four-state formula. Maximum discrepancy is 1.55e-15. Fresh state/noise simulation agrees in all three fixed checks. These checks verify risk computation, not global encoder optimality or novelty.

Stop here without fixing bad seeds by more training or searching more settings. This is a completed learned extension at n=4,m=2. The next load experiment, if undertaken, should retain the same detection outcome and evaluate n=3 or n=5 at m=2. No real-image transfer claim follows from this run alone.
