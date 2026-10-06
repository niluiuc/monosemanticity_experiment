# One-case rigorous noise-sign check: protocol before calculation

6 October 2026. Reuse the already globally certified clean geometry at
`p=1/20`, importance `(1,1/2)`, `n=2,m=1`, encoder energy one and its
clean-optimal biases. Reuse the actual strict decoder decision
`reconstruction>.5` and already tested code-noise level `sigma=3/10`.

Question: can exact rational enclosures prove its weighted detection-risk
difference from clean-selected mono is negative at this noise level, while
the exact clean and infinite-noise differences are positive? This would
establish at least two positive noise crossings, not their precise roots
or that there are exactly two.

Smallest calculation: bound the existing selected algebraic root, encoder
norms, decoder thresholds and eight Gaussian CDF values by rational interval
arithmetic. Obtain pi from Machin's arctangent identity and alternating-series
bounds; obtain square roots through exact integer arithmetic. Integrate
the exponential Taylor upper/lower polynomials to enclose each CDF. No
floating-point value is used to decide a sign.

Stop after this one sigma, the exact endpoint calculation and independent
teacher review. No new p, sigma, training, dense scan or root search. A
failed enclosure is reported as a gap; it is not permission to widen scope.
Source and all bounds/results are saved in this directory.
