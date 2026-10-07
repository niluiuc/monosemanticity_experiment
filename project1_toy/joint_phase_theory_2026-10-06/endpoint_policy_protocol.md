# Fixed check of the endpoint decoder-policy contrast

6 October 2026. Prospective protocol; no endpoint noise comparisons have run at the time this file is created.

- Question: at importance eta=2/3 and the clean storage endpoint pc=1/2, can the identical clean-selected geometry favor sharing with frozen biases but favor mono when both decoders' biases are calibrated?
- Link: the derived frozen leading coefficient B vanishes at this endpoint, while the calibrated coefficient 3/4-v(1/2) is strictly positive. This tests Project 1's risk-ordering mechanism, not an attack or a generic safety guarantee.
- Smallest test: epsilon=.005 and .001 only, p=1/2-epsilon, same Bernoulli/tied-ReLU/energy-one model. At each, use exactly sigma=2*sqrt((16/81)/(3/4-v(1/2)))*epsilon^(3/2). Compare frozen and symmetrically calibrated risk differences at this identical sigma. No scan or fitted exponent.
- Global clean branch selection and the endpoint asymptotic derivation require professor review before execution. Use exact rational cubic root brackets with 200 bisections.
- Calibration reuses reviewed 70-digit scalar branch-and-bound, slack 1e-40, at most 100,000 expansions per feature, total weighted gap min(1e-10,(16/81)*epsilon^3/100). Four feature ledgers per geometry. Preserve every ledger and all source/input hashes.
- Stop after two geometries and their two policy comparisons. If a sign is unresolved or opposite to prediction, retain it; no new epsilon, noise multiplier, tolerance or optimizer. Do not claim all-noise ordering, exact root count, arbitrary-load theory or publication novelty from this test.
