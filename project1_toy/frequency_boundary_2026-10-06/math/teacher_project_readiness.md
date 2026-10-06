# Teacher assessment: Project 1 readiness and the next decision

6 October 2026. This is a substantive research assessment, separate from
algebraic verification. It reads the existing `research_notes/volume2.tex`,
the focused-bridge derivations and numerical records, the frequency
transition proof and independent reviews, and the certified noise-sign
result. No new experiment, search or scope extension is performed here.

## Main judgment

**The bounded two-feature mathematics has made a real advance and is
ready to be taught and integrated. Project 1 as originally proposed is
not mathematically or empirically complete, and publication novelty has
not been established.**

The correct response to the deadline is to use the strongest established
claim and stop discretionary toy elaboration. It is not to describe this
restricted theorem as the general load/importance robustness phase diagram,
or to launch a large model as a substitute for a missing claim.

The original question remains: when does storing additional concepts
through superposition outweigh interference, as sparsity, capacity/load,
importance and corruption change? The new theorem addresses one exact,
nonlinear, resource-controlled slice of that question. It should remain
visibly connected to the broader target, without implying that every axis
has now been solved.

## What the work actually establishes

| Established result | Why it helps Project 1 | Limit that must accompany it |
|---|---|---|
| Global optimal bias at a supplied finite-state geometry | Replaces an arbitrary zero bias by the decoder selected by the stated clean objective | Elementary optimization, not a novelty claim by itself |
| Importance-unequal balanced pair is locally nonstationary | Predicts a geometry change from the training objective rather than fitting a risk after training | Local statement unless strengthened by a separate certificate |
| Dense-case global clean optima | Demonstrates that even equal importance need not select balanced norms, and that the tested unequal importance can select mono | Only the specified dense cases |
| Exact global `p=.20`, weights `[1,.5]` sharing optimum | Provides a complete clean training-to-geometry example, independently certified | One parameter case; does not establish general optimizer convergence |
| Continuous clean frequency transition `pc=(3-sqrt(5))/2` | Predicts the global sharing-versus-mono storage label throughout a frequency interval from the actual nonlinear objective | Fixed two features, one dimension, energy one and importance ratio two |
| Four below-transition global geometry certificates | Supplies selected geometries for prespecified validation points, rather than assumed equal pairs | Discrete selections do not give an explicit selected geometry curve at every p |
| Exact state-conditioned noisy decoder risk | Makes the corruption comparison operational and checkable | Standard conditional calculation; fixed decoder and code-noise model |
| Rigorous at-least-two noise roots at `p=.05` | Shows a selected representation's comparison with mono can be nonmonotone; a single simplistic boundary is inadequate | One frequency, not an exact root count or a universal shape theorem |

The central new mathematical chain inside the declared setting is:

**clean population objective → globally selected geometry/storage label
→ specified decoder → operational Gaussian corruption risk.**

This is stronger than a result conditional on an arbitrarily supplied
dictionary. It resolves the particular learned-geometry blocker identified
in the literature audit. Whether these exact results are new to the
literature remains a different question.

## Material distinctions and issues

### 1. Two objectives are involved

Clean geometry is selected by importance-weighted continuous reconstruction
MSE. The displayed corruption comparison uses thresholded binary detection
error. These are different loss functions.

This is not a mathematical error: classification of reconstructed features
is a legitimate downstream test. It becomes an error if a summary claims
that the representation necessarily improves the same clean task whose
noisy performance is then being compared. At `p=.05`, the selected sharing
code has **worse clean detection**, `11/400` versus mono's `1/40`, despite
better clean MSE. It improves detection only in an intermediate noise
region in the certified example. At `p=.20`, its clean detection ties mono
and its positive primary-noise detection measurements are worse.

Necessary wording: the representation is **clean reconstruction-selected**;
its downstream detection ordering under corruption is assessed separately.
The noise benefit must not be sold as universal.

### 2. The decoder is part of the claim

The actual rule is strict reconstructed amplitude greater than `1/2`.
It is not the Bayes-optimal noise-aware classifier for every rare prior.
The existing centered-midpoint diagnostic produces materially different
rankings. Noisy risk therefore belongs to the **geometry-and-decoder
system**, not a universal scalar measure of monosemanticity.

A different threshold cannot replace an adverse result after evaluation.
To keep the current bounded claim, state this decoder explicitly and retain
the already saved diagnostic. It is not necessary to open a whole new
noise-aware decoder optimization project now. A stronger claim of
decoder-independent intrinsic robustness would require additional work
and is not authorized by the present proof.

### 3. Population selection is not guaranteed practical training

The fixed projected-Adam campaign ran all 36 settings and preserved nine
loss-stability failures. Several stability-passing iterates retained
substantial tangent gradients and missed better encoders. The different
angular solver reached the certified optima at two existing cases.

This establishes that the stated objective has the selected solution and
that the bounded angular procedure can reach it. It does **not** establish
that the original projected-Adam solver, all seeds, or a natural neural
model learns the theorem's geometry. The optimization failures are useful
evidence and must remain visible. Calling all these codes identically
"trained optima" would misstate the record.

### 4. The fixed load and importance are genuine restrictions

Every new global theorem fixes `n/m=2` and weights `[1,.5]` (with separate
dense equal-importance checks). It does not derive a variable-load law or
an importance-decay boundary. The original eight-feature run also fixed
load and uniform importance. Those missing axes cannot be filled by wording.

Merely tiling independent pair/mono blocks would make their risk differences
add. It would not by itself create a new load-dependent location of the
boundary or prove optimality among unrestricted multi-dimensional codes.
Such an extension can be a consistency check, but must not be counted as
a solved general capacity phase diagram.

### 5. Relation to the starting paper needs exact attribution

Zhang et al.'s motivating monosemanticity paper studies different objectives,
continuous toy feature amplitudes and noise locations in its analyses.
The present binary, fixed-energy, code-noise theorem is a controlled
mechanistic extension of that motivation. It is not automatically a
strict generalization of every robustness experiment in that paper.

Our alignment metric also has the exact capacity/dimensionality predecessor
identified in the audit. The new claim must be about learned selection
and its consequences, not about introducing that metric.

## Was the extension disciplined?

**Yes, within its logged bounds.** The sequence addressed concrete blockers:

1. The initial trained dictionary raised the question of equal-pair
   optimality. Six existing frequency/importance cases and a fixed angular
   diagnostic tested that assumption.
2. Nonstationary projected-Adam outputs warranted a two-case angular
   diagnostic, not a broad optimizer campaign.
3. A local numerical optimum required a one-case global branch certificate.
4. The two endpoint storage optima motivated the fixed-importance frequency
   theorem; all sign and bias branches were checked.
5. Five preregistered frequency validations tested that prediction.
6. A nonmonotone plotted comparison motivated one rigorous sign certificate
   at an already tested frequency and noise strength.

Failures, very small advantages, negative comparisons and numerical checker
repairs were preserved. No evidence was changed to obtain preferred signs.
The display curve is a fixed supplied-formula visualization, not a dense
training/geometry search. Its sampled roots were explicitly labeled
incomplete, and the rigorous follow-up proves only the necessary existence
claim.

The stopping warning is now substantive: this successful bounded sequence
must not turn into endless exact-root location/count proofs, precision
tightening, decoder variants, distributions or additional toy families.
Those are optional unless a paper claim specifically requires them.

## Necessary versus optional next work

### Necessary before claiming a paper result

- **Integrate and independently check the complete derivations.** The
  document must distinguish fixed supplied-code boundaries from globally
  selected geometry, clean storage labels from noisy detection regions,
  numerical diagnostics from proofs, and solver iterates from certified
  optima. Raw experimental outcomes remain linked and unchanged.
- **Complete a focused exact-claim novelty comparison.** Use the already
  archived literature and compare this objective, its global frequency
  selection theorem, and the nonmonotone selected-code corruption result
  with explicit equations and assumptions in the direct prior sources.
  This is a targeted remaining blocker, not a repeat of the broad survey.
  Correctness and verification do not establish publication novelty.
- **Choose an honest manuscript scope.** Either the paper presents a
  rigorous fixed-load/fixed-importance mechanism with a meaningful real
  demonstration, or it claims the broader capacity law and obtains the
  additional theory/evidence needed for that claim. Do not silently label
  the first as the completed second. The research direction stays the same.
- **Specify one prospective real-model test before allocating substantial
  compute.** It needs a concrete feature measurement, corruption location,
  decoder/outcome, comparator and falsifiable prediction. A natural-model
  SAE Gram matrix is not automatically this tied reconstruction map. The
  transfer may test a qualitative mechanism rather than an unjustified
  exact CDF identity. The team should choose the already planned modality
  based on available compute and expertise, not add new applications.

These tasks can proceed with the existing mathematics and infrastructure;
they do not require a fresh project. The deadline argues for deciding the
precise contribution now and using the remaining research time for its
most informative transfer, instead of indefinitely improving toy plots.

### Optional at present

- Exact locations or total counts of all Gaussian risk roots.
- Extra frequencies, seeds, angle grids or optimizer configurations.
- A full general-importance-ratio theorem merely because it is algebraically
  tempting.
- New correlations, amplitudes, noise types or recursive-training loops.
- Multiple pretrained architectures or modalities.
- A readout-optimization study that is not part of the selected claim.

If a broader variable-load claim remains the manuscript's central target,
some capacity-dependent result is necessary eventually. That is a scope
decision, not permission to run an unguided multi-axis sweep now.

## Minimal go/no-go recommendation

**GO:** finalize the derivation integration, retain the restricted global
theorem as established work, complete its exact-claim novelty check, and
prepare one bounded real-model transfer protocol in parallel. Stop further
toy exploration under the completed protocols.

**HOLD:** launching an expensive diffusion retraining/self-consumption
pipeline before the Project 1 transfer claim and compute budget are fixed.
That would reintroduce Project 2 and a separate training-loop problem
without resolving the present manuscript's evidence needs.

**NO-GO for current wording:** claiming that the full sparsity/load/
importance-decay robustness phase diagram is solved, that verification
guarantees ICML novelty or acceptance, or that this geometry has been
validated in a real model. Those claims are unsupported by current files.

If the exact-claim literature comparison finds this theorem routine or
already covered, do not hide it behind a large-model demonstration. Identify
the smallest nonroutine extension inside the original direction, with a
new explicit question and stop condition, before committing remaining
compute. If a distinct claim survives, the current correct proofs and
reproducible toy evidence are a useful foundation for the next stage.

## Required integration checks for Volume II

The current volume already labels much mathematics conditional, which is
good. The new material must also:

- Keep the supplied equal-pair crossing near `0.279938913` tied to its
  original fixed detector and equal-energy assumptions; it is not the
  trained-decoder crossing of the new global geometry.
- Include every activation-interval argument used to prove a global
  optimum, including the hidden weak-bias competitor and all sign/order
  sectors. An equation list is not a substitute for these proofs.
- Explain rational root/candidate completeness and interval signs in
  the one-case certificates; a program's `certified=True` is not an
  explanatory derivation.
- Explain the Machin quadrant argument, integrated Taylor bounds and
  strict clean margins behind the two-root existence result.
- State which original training runs failed and which solver/certificate
  results are later bounded corrections, without suggesting raw data
  were overwritten.
- Present the known literature identity `M_i^2=C_i` with attribution.
- Remove context-dependent headings such as "Recovering the old expression"
  from team-facing notes; readers need the mathematical definition rather
  than a reference to an unseen chat.
- Mark historical eight-week dates and original broad-grid suggestions
  as an earlier plan. They must not be interpreted as an automatically
  renewed eight-week budget or authorization for broad experiments now.

The existing Project 2 material is background to the original integrated
program. No new Project 2 experiment or general monosemanticity-collapse
theorem was completed in this work. The updated volume must preserve that
boundary as clearly as it preserves the new Project 1 results.
