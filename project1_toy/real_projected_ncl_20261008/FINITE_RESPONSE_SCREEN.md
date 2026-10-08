# One finite-response scaling screen

Question: does replacing the failed derivative at zero with the actual logit change at the already measured validation scale h=.04 qualitatively account for the native intermediate-noise ordering change?

Connection to the remaining Project 1 gap: the full nonlinear CNN has large finite-response shifts that the local derivative misses. This single candidate retains the entire measured nonlinear change, including its image-dependent mean and direction fluctuations, and tests whether simple scale transport suffices. It is not a derived superposition law or an intrinsically novel method.

Use only saved clean/actual logits for the original 500 validation images and 32 directions at .04. Define s_tilde(sigma) = s(0) + (sigma/.04)[s(.04)-s(0)]. Compute classification increments on the existing fixed eight-level grid, and add them to the original full-validation clean error baseline, exactly as for the original predictor. No fitting, new corruption level, new forward, checkpoint or threshold search.

This candidate is proposed after viewing the native TEST outcome. Its comparison with that outcome is a post-outcome screen, not a frozen prospective prediction. Screening criterion: it must show a positive-to-negative first ordering change between .04 and .12. Otherwise stop this simple finite-response scaling path. A screen pass would warrant a separately registered prospective applicability test; it would not establish the crossing formula or paper novelty.

Preserve all predicted points whether favorable or unfavorable, and leave the original frozen failed prediction unchanged.
