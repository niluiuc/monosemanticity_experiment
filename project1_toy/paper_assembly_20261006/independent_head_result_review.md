# Independent saved-record review: fixed class-evidence transfer

6 October 2026. **Audit PASS.** No inference, fitting, new noise levels or replacement pair were run. Immutable extraction/evaluation outputs were not edited. Audit source, full machine-readable output and its SHA-256 manifest are preserved in `head_transfer_20261007/independent_audit_v1/`.

## What was checked

The independent auditor verified all 9 extraction-manifest files and 38 evaluation-manifest files; actual cached checkpoint/data hashes; official category mapping 281/207; declared preprocessing; seed-20261007 permutation and 256/256/4,096 split indices; cached CIFAR labels; all 1,000 raw logits and exact fixed-pair rectification; training RMS, zeros and noise reference; AUROC by positive-negative pair counts with half credit for ties; all saved clean grid losses and selection gates; zero-noise calibration candidates; all conditional Gaussian per-image risks and risk differences; 896 calibration ledger nodes, partition coverage and exterior bounds; and the default-integer bootstrap draw followed by uint16 cast plus all saved bootstrap means/intervals. All five calibration cases resolved. Maximum independently recomputed per-image risk discrepancy was `4.440892098500626e-15`.

Forward inference was not duplicated. The audit checks the saved outputs against the archived approved implementation and provenance; it does not independently rerun the entire ResNet. Angular clean selection remains a numerical search, not a global proof for this empirical distribution.

## Actual observations

- Training AUROCs were `.9049522541` (tabby evidence versus cat) and `.8081939799` (golden-retriever evidence versus dog), passing the prespecified `.65` gate. Descriptive test AUROCs were `.8700349377` and `.8172911158`; they selected nothing.
- Training RMS values were `2.3272077353` and `2.5516058232`; zero fractions `.17578125` and `.22265625`. Gaussian standard deviations use the fixed training noise reference `.7308510286`.
- Numerical clean selection chose same-sign sharing weights `(0.8354173789, 0.5496160505)` versus mono `(1,0)`. Training sharing gain was `.0710756583`. The 256/512 refinements agreed in loss and all declared clean gates passed.
- Held-out zero-noise sharing-minus-mono risk was `-.0710555300`, interval `[-.0889889429,-.0520158043]`. Sharing also remained better, with negative pointwise intervals, at every positive fixed noise level under both policies.

| Noise multiplier | Frozen sharing-minus-mono | Calibrated sharing-minus-mono | Policy contrast |
|---:|---:|---:|---:|
| 0 | -.0710555300 | -.0710555300 | 0 |
| .05 | -.0711332655 | -.0711548026 | -.0000215370 |
| .1 | -.0713038655 | -.0713725079 | -.0000686424 |
| .2 | -.0718532322 | -.0719331061 | -.0000798739 |
| .4 | -.0738861898 | -.0732688755 | +.0006173143 |

The primary calibrated delta at `.4` was `-.0732688754671862`, 95% pointwise paired interval `[-.09160314565598802,-.05388519686819121]`. Individual calibrated risks there were `.3982232908` (sharing) and `.4714921663` (mono). Both risks rose from their clean values, but mono's risk rose more: **the sharing advantage did not disappear or reverse** on this grid. Calibration narrowed the advantage relative to the frozen policy at `.4` by `.0006173143`, interval `[.0003468203,.0008997372]`; this is a resolved policy effect, not a winner reversal. Policy-contrast intervals were negative at `.05/.1` and included zero at `.2`.

## Interpretation and stopping

This is favorable evidence that clean-selected mixed storage can generalize and retain its advantage under the declared Gaussian code corruption for one externally class-mapped evidence pair. It is unfavorable to any empirical claim that this pair shows the predicted clean-to-noisy ordering reversal: **it does not**. The same-sign selected geometry also differs from the opposite-sign branch of the scoped Bernoulli critical theorem. Do not present this experiment as measuring that theorem's critical exponent or exact asymptotic branch.

The coordinates are checkpoint-dependent rectified class logits, not proven monosemantic hidden features. Coarse CIFAR labels are not breed/subclass annotations, logit zero is not concept absence, and the corruption acts on an auxiliary scalar compression rather than image inputs or the original ResNet. Bootstrap intervals are conditional on fitted models and pointwise; they omit training/calibration uncertainty. No universal monosemanticity, full-network robustness, safety or main-track sufficiency conclusion follows.

**Stopping decision:** the one fixed operational follow-up completed and its saved-record audit passed. Preserve these values and limitations; no additional pair/noise/model search or optimizer adjustment is justified by this run. The paper can report retained sharing advantage and decoder-policy sensitivity, while retaining the lack of a real-model reversal as a material limitation.
