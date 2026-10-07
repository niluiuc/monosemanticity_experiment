# Professor review: head-results derivation-volume section

Reviewed `research_notes/project1_head_results_20261007.tex` against saved extraction/evaluation records, the independent audit and `professor_head_result_decision.md`. No section/source/result was edited and no experiment or mathematics was added.

## Verdict

The section reports the completed test accurately. All displayed risks, intervals, class association values, clean weights/gain, zero/coactivation fractions, extraction duration, audit counts and maximum discrepancy agree with the saved records at their displayed precision. There is no unsupported ordering reversal or critical-law transfer claim.

Two compact method clarifications should be included before delivery so the strongest reported number is interpretable without hunting through the protocol:

1. **Label the primary endpoint.** Explicitly state that calibrated sharing-minus-mono weighted MSE at multiplier.4 was the prespecified primary outcome, fixed before inference, with frozen difference/policy contrast secondary and all five curves retained. The current section contains its actual number but does not identify that prospective status.
2. **Define the noise reference and sign at this table.** State that .7308510286 is `sqrt((Var_train(x1)+Var_train(x2))/2)` after train-RMS normalization, that independent scalar Gaussian noise of this standard deviation is added to the code identically for both models, and that table differences are sharing-minus-mono total weighted reconstruction MSE. Earlier sections derive these conventions, so a short cross-reference plus definitions is sufficient; no new derivation is required.

These are reporting clarifications, not numerical or mathematical errors. No other necessary correction is identified.

## Verified interpretation and limits

- Full classifier-head logits are distinguished from the earlier spatial activation proxy; fixed IDs and rectification threshold precede outcomes. Additive logit gauge and lack of concept-absence meaning are explained correctly.
- Broad CIFAR cat/dog association is not mistaken for tabby/breed ground truth, causal concepts or validated monosemantic hidden features.
- Width/energy/tied decoder, free biases, both mono orientations and omitted-feature loss are stated; numerical clean selection is not called globally certified.
- Primary frozen biases come from zero-noise calibration on the same split used for noisy calibration. Encoders remain frozen and test data do not select or fit.
- Every sampled risk difference favors sharing with intervals belowzero; absolute risks rise and no winner reversal occurs. Relative sharing advantage is not interpreted as noise improving absolute reconstruction.
- Calibration contrast is correctly negative/resolved at.05/.1, unresolved at.2, and positive/resolved at.4. It is not presented as a universal mono calibration advantage.
- Bootstrap is conditional/pointwise, calibration arithmetic is not directed rounding, and forward inference was not independently duplicated. Audit9/38 manifest files,896 nodes and4.44e-15 maximum discrepancy match the saved audit.
- The stop decision forbids extra pairs, threshold/noise/decoder changes after no crossing. The result strengthens labeled operational sharing evidence while leaving the original real critical-boundary and hidden-monosemanticity gaps explicit.

With the two concise clarifications, this is faithful full-method/results delivery for the completed bounded experiment. It does not convert the auxiliary evidence-score reconstruction result into a full-model robustness theorem.
