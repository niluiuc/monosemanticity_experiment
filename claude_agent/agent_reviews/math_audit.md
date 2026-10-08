# Independent math audit of `repair_v2/derivation_section_v3.tex`

Auditor: independent re-derivation (own sympy / numpy code, written from scratch in a scratch directory; the project's code was used only to compare numbers and to inspect the gate-lemma logic). Date: 2026-10-07.

## Summary verdict

All the main formulas I was asked to check hold up under independent derivation:
- the small-angle expansion: linear term, kappa_plus and kappa_minus, and the c=0 cubic;
- the signed A', K, C;
- the two field-response laws and the c* line with its 9/16 coefficient;
- the bicritical identity;
- the shared-budget thresholds, including the general-m formula;
- B2 (kappa_0 and the -2 p z_p sigma term).

I found **no ERROR in any stated result**. The problems are about rigour and presentation:

1. **GAP (fixable): the Lemma A' proof sketch is incomplete as written.** The factor identities establish signs only for (a) breakpoint-versus-chosen value differences and (b) the claim that the chosen minimiser is strictly interior. The "competing interior minimiser lies outside its piece" conditions are checked **only on a numerical grid**. Some competitors have a *negative* value difference over part of the domain, so these validity conditions actually carry weight. The grid also omits c in (min(p/q,q/p), 1). The lemma is nevertheless **true**: a short convexity argument (Section 1.3) closes the gap completely and makes the enumeration unnecessary.
2. **Minor ERROR in the text of Prop. A:** "(up to O(theta^4))" for the per-state errors should read O(theta^3).
3. **OVERCLAIM (interpretive): the bicritical identity.** It is algebraically exact, but its only content is that two functions of p share the simple zero p=1/2 on the critical line. "Frozen penalty vanishes *when* the same-sign direction goes soft" suggests a mechanism the paper does not establish.
4. **Prop. C:**
   - The one-partner threshold derivation is correct, and its gate conditions hold along the profiled direction.
   - The donor cost is really one-sided (zero for s^2>1). This is harmless because u*>0, but it should be stated.
   - My own quadratic-order minimisation over the **full** 2x4 perturbation space finds no earlier instability at eta=0.3, 0.5, 0.7. This supports the restriction to the one-partner path numerically.
   - Two of the reported numerical brackets **exclude** the prediction (they lie just below it). The text presents them as agreement without comment.
5. **Labels.** Several paragraphs mix labels, contrary to the stated "one label per statement" policy:
   - Corollary A contains [P]/[I] content.
   - Prop C contains an [I] identity and [N] numerics.
   - "Three features" contains [E].
   - "Numerical observations (i)" is [N] in the tex but [L] for T10 in STATUS.

   Also, B2's "barrier O(sigma^2)" is asserted without derivation.

---

## 1. Lemma A' and Proposition A

### 1.1 Closed forms: CONFIRMED
I wrote my own exact branch losses:
- Output 2 with all gates open: Var(dX1+(s-1)X2), with a=cos^2, d=sin cos, s=sin^2.
- Output 1, opposite branch: states 00, 10, 11 on and 01 off; b1* = [P10(1-a)+P11(1-a-d)]/(P00+P10+P11).
- Output 1, same branch: states 10, 01, 11 on and 00 off.

I then expanded with sympy to O(theta^3), keeping p, c and eta symbolic:
- Linear coefficient on both branches: 2 c eta p(p-1) = **-2 eta c p q**, so h = 2 eta c p q.
- coeff(theta^2) - (A_minus - eta p q) = 0 and coeff(theta^2) - (A_plus - eta p q) = 0 exactly.
- c=0 cubic (opposite branch, in theta): -2p^2(p-1)^2/(p^2-p+1) = **-2p^2q^2/D**. With theta=-k this gives B = +2p^2q^2/D in k. At p_c (p=eta D) this equals 2 eta p q^2.
- c=0 cross-checks:
  - kappa_minus = pq(p - eta D)/D vanishes at p_c(eta) as stated.
  - kappa_plus = pq(1/(2-p) - eta) vanishes at p = 2 - 1/eta.
- At c=0, output 2's loss is exactly pq cos^2 theta, so the c=0 cubic comes entirely from output 1.
- For c != 0 the cubic coefficient depends on c and eta: (-2/3) p(p-1)(...)/(cp^2-cp-p^2+p-1). This is fine because only its c=0 value is used at leading order.

**Minor ERROR (text):** Prop. A says the per-state errors hold "up to O(theta^4)". This is wrong. For example, the (1,1) error on the same branch is (theta+b - sin^2 theta + O(theta^3))^2 = (theta+b)^2 - 2theta^2(theta+b) + ..., so the correction is O(theta^3). The quadratic coefficients are unaffected. Fix: "up to O(theta^3)".

### 1.2 What the gate-lemma code actually proves: GAP
I inspected `gate_lemma.py` and `results/gate_lemma.json`:
- **Breakpoint competitors:** the leading value differences are of fixed sign by the five factor identities. I confirmed the identities are exact. **OK.**
- **Chosen minimiser strictly inside its piece:** the leading coefficients are P11/(1-P01)-type ratios. **OK.**
- **Interior competitors:** the code computes the leading coefficient of (b*_competitor - piece boundary). It then evaluates its sign **only on a 49x41 (p,c) grid** and *skips* the value comparison where the competitor is invalid. Every interior competitor has `valid_fraction = 0.0`. These validity coefficients are never factored or proved.

This matters because some interior competitors have **negative** leading value difference. For example, output-2/opposite with only (0,1) on has difference -p(cp - c - 2p + 1) = P11 - pq, which is negative whenever P11 < pq, e.g. at c=0, p<1/2. So the argument genuinely depends on the ungridded-proved validity claim.

- **Grid coverage:** the grid uses c in [-min(1,q/p,p/q), +min(1,q/p,p/q)]. This **excludes** feasible c in (min(p/q,q/p), 1); for example, at p=0.3 it misses c > 0.43.
- **Text versus code:** the text says "every competing piece's unconstrained minimiser lies outside that piece at leading order ... all leading coefficients factor ... so the signs hold on the whole open feasible domain". That is stronger than what the code does.

### 1.3 A complete proof (recommended replacement): CONFIRMED that the lemma is true
Fix an output and a branch. Split the bias axis into two regions.

**Output 1.** The target-1 states have offsets 1+O(k).
- On the region b > -1/2, every target-1 state is on. The loss is a sum of convex terms: (o+b-1)^2 for the target-1 states and ReLU(o+b)^2 for the target-0 states. It is *strictly* convex, with second derivative at least 2p.
- The chosen stationary point lies strictly inside its piece (proved by the factor identities). It is therefore the **unique** minimiser on b > -1/2.
- On b <= -1/2 the target-1 errors alone are at least p(1/2 - O(k))^2 = Theta(1). The chosen value is O(k^2).

**Output 2.** The target-1 states have offsets O(k).
- On b >= p/2 all states are on. The loss is a strictly convex quadratic whose minimiser is b ~ p, inside the region.
- On b < p/2 the target-1 errors are at least p(1-p/2-O(k))^2 = pq + p^3/4 - O(k). That exceeds the chosen value pq + O(k) for small k.

This proves Lemma A' at every interior (p,c) with an explicit k_0. The k_0 degrades only as min P_x -> 0, which matches the "not uniform near the boundary" caveat. Ties and degenerate breakpoint orders cannot matter, because no enumeration is used. **Recommendation:** replace the enumeration sketch with this argument. Keep `gate_lemma.py` only as a cross-check.

Other checks:
- At theta=0 the bias optima are unique: b1=0 and b2=p.
- F is analytic on each side of theta=0 under the fixed pattern, so the O(|theta|^3) remainder in Prop. A is legitimate.

## 2. Signs, field response, c* line

- **A' = +d kappa_minus/dp at p_c: CONFIRMED.** d kappa_minus/dp at p_c = (pq/D)(1 - eta(2p-1)), which is 0.3454915 at eta=1/2. This equals (5-sqrt5)/8, and kappa_minus(p_c - eps) = -A' eps.
- **K and C: CONFIRMED.** Minimising -A' eps k^2 + B k^3 gives K = 2A'/(3B) = 1.578689 and C = 4A'^3/(27B^2) = 0.287018 (eta=1/2, B = 0.145898). Also 2C/K^3 = B identically.
- **c<0 field response: CONFIRMED.** For c<0 at p_c: |theta*| = sqrt(-h/(3B)) = 0.7344|c|^{1/2}. My exact clean solver gives 0.7361, 0.7379, 0.7399 at c = -1e-4, -4e-4, -1e-3.
- **c>0 field response: CONFIRMED.** For c>0 at p_c: theta* = h/(2 kappa_plus) = 4.236c. The solver gives 4.220 at c=1e-4 and 4.087 at c=1e-3. kappa_plus(p_c) > 0 for eta < 2/3, as required.
- **c* line: CONFIRMED, including the 9/16.** On the opposite branch g(k) = hk - A' eps k^2 + Bk^3. Its local minimum has zero depth when g has a double root, i.e. A'^2 eps^2 = 4Bh. With A'^2/B = 9C/(2K) this gives h = 9C eps^2/(8K), so c* = 9C eps^2/(16 eta p q K) = 0.86642 eps^2.
  - Comparing with zero rather than with the same-sign minimum is correct at leading order. The same-sign depth -h^2/(4 kappa_plus) = O(eps^4), and corrections to kappa_minus and B shift h only by O(eps^3).
  - A naive envelope (first-order) perturbation would give C eps^2/(2 eta p q K) = 0.770 eps^2, which is wrong because h k ~ eps^3 is the same order as the depth. The double-root condition the paper uses is the correct one.
  - Numerically, using bisection on the gap between the two exact local minima (own solver), c*/(0.86642 eps^2) = 0.9973, 0.9933, 0.9865, 0.9728 at eps = 0.002, 0.005, 0.01, 0.02. This converges to 1.
- **Lipschitz constant in [G]: CONFIRMED** (conservative):
  - |d o/d theta| <= sqrt2 < 2sqrt2.
  - The bias range [-sqrt2, 1+sqrt2] is justified.
  - The min-of-Lipschitz-family argument is valid without differentiability.
  - The double-precision caveat is correctly stated.
- **Claim B constant: CONFIRMED.** (B_cal/C)^{1/3} = 0.831556 (B_cal = 0.165038 at eta=1/2), and the inversion eps* = (B_cal/C)^{1/3} sigma^{2/3} is consistent.

## 3. Bicritical identity

- **The identity is exact: CONFIRMED.** On eta = p/D, 1 - eta(2-p) = (1-p)(1-2p)/D. So kappa_plus = pq(1-p)(1-2p)/(D(2-p)), and kappa_plus D(2-p)/(2pq) = q(1-2p)/2 = B_frozen. sympy simplifies the difference to 0. The point (eta,p) = (2/3,1/2) is where kappa_minus = kappa_plus = 0, so it is bicritical.
- **The interpretation is an OVERCLAIM.** B_frozen is defined only on the critical line, so it is a function of one variable. Any two functions with a common simple zero satisfy such an identity, with a smooth nonvanishing ratio (here D(2-p)/(2pq)). The identity therefore says no more than "B_frozen and kappa_plus both vanish at p=1/2".
  - A plausible common cause is the p=1/2 (c=0) symmetry: kappa_plus(1/2) = kappa_minus(1/2) for **all** eta, which I checked with sympy. That symmetry forces both branch zeros onto p=1/2 at eta=2/3, and it may also be why B_frozen is proportional to (1-2p).
  - Nothing in the text shows that the noise penalty vanishes *because* the same-sign direction softens.
  - **Fix:** "Both B_frozen and kappa_plus|_{eta=p/D} carry the factor (1-2p), so the frozen noise coefficient vanishes at the bicritical point; we do not claim a causal mechanism."
  - The identity is also embedded inside the [L] Prop. C paragraph, but STATUS gives it [I]. Move it to its own [I] paragraph.

## 4. Proposition C (shared-budget compression)

- **The thresholds are CONFIRMED.** I built my own sympy model (a -> 1+u, d -> -/+ sqrt(1+u)k, partner output Var with s2 -> k^2, donor pq(u+k^2)^2/(m-1)). The gradient vanishes at mono, and the Schur complements are:
  - opposite: k_eff proportional to 2p(p-1)(eta p^2 - 2eta p + 2eta + p^2 - 2p)/(p^2-2p+2), with roots **1 - sqrt((1-eta)/(1+eta))**;
  - same: proportional to (eta p - 3eta + p + 1), with root **(3eta-1)/(eta+1)**;
  - general m: roots exactly match the paper's formula (residual 0 at m = 2, 3, 4, 7). Values at eta=1/2 are 0.42265, 0.44174, 0.45308, and the m -> infinity limit is eta/2 - |1-eta|/2 + 1/2 = eta.
- **Donor cost model: CONFIRMED with a caveat.**
  - For a retained binary feature at squared amplitude s^2 with a free bias, the profiled loss is pq(1-s^2)^2 for s^2 <= 1, with b = p(1-s^2) >= 0 and both gates open. For s^2 > 1 it is **0** (b = 1 - s^2 gates the 0-state off).
  - So the true donor cost is pq·max(u+k^2, 0)^2, which is C^1 but not C^2 at mono. The code uses the two-sided form.
  - This is harmless here because the profiled direction has u*/k = pq/(1+q^2) > 0 (opposite) and q/(3-p) > 0 (same), so the donor really loses amplitude.
  - Feature 1's own loss is also one-sided in u, but it is captured by the closed form.
  - The text should state the one-sidedness.
- **Gate conditions along the profiled direction: CONFIRMED.**
  - Opposite: b1 = p^2 k/(1+q^2), which lies in (0, k), using 1 - q + q^2 = D.
  - Same: b1 = -(u+k)/(2-p), which lies in (-k, 0) because u* < qk.
  - For fixed k the true leading-order loss is convex in u (G1 is convex and the donor term is convex). So the pattern-valid stationary point is the global minimiser over u. The path computation is therefore an exact quadratic-order statement, not only "leading-order with numerical support".
- **Equal-donor split: JUSTIFIED** by convexity (Jensen): sum_j pq u_j^2 with sum_j u_j = u is minimised at equal shares.
- **One partner versus other perturbations: SUPPORTED numerically [N], not proved.**
  - I derived the full quadratic-order function for m=2, n=4: Q = G(u, g12, k13, k14) + G(-u, g12, k23, k24) - eta pq sum k^2. Here G is the exact leading-order profiled output-1 loss with ReLU gates over 16 states, and the gauge rotation is removed.
  - I minimised Q on the unit 5-sphere with 60 Nelder-Mead starts. The sign change of min Q is at:

    | eta | branch | sign change of min Q | prediction |
    |---|---|---|---|
    | 0.5 | opposite | in (0.4226, 0.4227) | 0.42265 |
    | 0.3 | opposite | in (0.2655, 0.2665) | 0.26620 |
    | 0.7 | same-sign | in (0.645, 0.6475) | 0.64706 |

  - In every case the minimiser is a single partner with u/k matching pq/(1+q^2) (0.183 at eta=0.5). The one-partner path is therefore the softest direction at quadratic order in the full space.
  - A direct Powell search on the exact 2x4 loss (12 random starts each) agreed: it found descent at p = 0.41 (eta=0.5) and p = 0.255 (eta=0.3), and none at p = 0.425 or 0.44 (eta=0.5) or p = 0.275 (eta=0.3).
  - For m >= 3, a separable argument shows j partners pay a donor cost per partner proportional to j/(m-j) >= 1/(m-1), so one partner is softest within that structure. Cross-dimension partner mixing for m >= 3 was not tested.
- **Numerics presentation: OVERCLAIM (minor).** The eta=0.5 bracket [0.4219, 0.4225] and the eta=0.7 gain-threshold bracket [0.6456, 0.6463] both **exclude** the prediction (0.42265, 0.64706). They lie just below it, which is consistent with a detection-threshold bias: sharing gain near threshold scales like (p_th - p)^2, so a 1e-10 gain cut misses roughly the last 1e-4 to 1e-3 in p. The text should say this instead of "vs".

## 5. Proposition B2

- **kappa_0: CONFIRMED by derivation.**
  - H'(z) = 2(zPhi + phi) and H'' = 2Phi. The stationarity condition is exactly p z + q(z Phi + phi) = 0.
  - The d-gradient is p(q g0' + p g1') = 0 at c=0.
  - Minimising the weighted quadratic over beta gives (P01 Phi + P11)(P00 Phi + P10)/(q Phi + p), which equals pq(p + q Phi) at c=0. Output 2 adds -eta pq + O(sigma^2).
  - The amplitude term G_a a''/2 with G_a = 2p z_p sigma gives -2p z_p sigma. Since z_p < 0, noise stiffens mono.
- **Spinodals: CONFIRMED.** p_sp = 0.26039, 0.27911, 0.29853, 0.46277 for eta = 0.48, 0.5, 0.52, 2/3.
- **Numerical check: CONFIRMED.** I wrote exact Gaussian moments for ReLU and ReLU^2, profiled both biases separately, and took a central finite difference with step sigma/40. Results for kappa_sigma - (kappa_0 - 2p z_p sigma):

  | (p, eta) | sigma = 0.003 | sigma = 0.01 | sigma = 0.03 |
  |---|---|---|---|
  | (0.30, 0.5) | -4.7e-7 | -2.3e-6 | -1.9e-5 |
  | (0.35, 0.48) | -1.2e-6 | -9.2e-6 | -8.1e-5 |
  | (0.25, 0.5) | 1.6e-7 | 3.1e-6 | 2.9e-5 |
  | (0.45, 2/3) | -2.6e-7 | 8.3e-7 | 9.5e-6 |

  The residual divided by sigma^2 is roughly constant (-0.09 to +0.03), which confirms that the remainder is **O(sigma^2)**. The paper reports a residual "<= 1.3e-4 independent of sigma (finite-difference step error)". Mine are smaller and scale as sigma^2, so their residual is indeed FD noise. Reporting a sigma^2-scaling residual would be the stronger evidence.
- **Validity domain: correctly scoped.** The derivation needs |theta| << sigma.
- **GAP:** "its barrier is O(sigma^2)" is not derived in B2. It is a statement about the landscape at |theta| ~ sigma (the Phi(x) scaling of the Numerical observations). Label it heuristic [L]/[N] or drop it.

## 6. Status labels, paragraph by paragraph

| Paragraph | Label | Verdict |
|---|---|---|
| Status labels / Setting | — | fine |
| Prop. A | [P] given A' | **Appropriate**; fix "O(theta^4)" -> "O(theta^3)" |
| Lemma A' | [P] | **Too strong for the written sketch** (interior-competitor validity is grid-only; the grid misses large positive c). **Appropriate** once the convexity proof in 1.3 is added |
| Corollary A | [L] | Appropriate, arguably conservative: the field responses and c* follow rigorously at leading order from [P] Prop. A plus the exact cubic. But the paragraph also contains [P]/[I] material (exact closed forms, B = 2p^2q^2/D, the A', K, C identities) and changelog prose ("session-2 script used the opposite sign"). Split it: [P] cubic/closed forms, [I] K, C at eta=1/2, [L] responses and c*; move the history to CORRECTIONS.md |
| Grid computation | [G] | Appropriate; the Lipschitz bound checks out; the 4 uncertified points are honestly flagged |
| Claim B | [L]+[N] | Appropriate. The "Check of the open step" and "Session-3 scaling function" sub-paragraphs are [N] (semi-analytic); label them explicitly |
| Prop. B2 | [L] | Appropriate for kappa_0 and the O(sigma) term (could become [P] up to exp-small terms with a written remainder). "Barrier O(sigma^2)" is **too strong** as stated, since it is underived |
| Real-activation tests | [E] | Appropriate (not mathematically auditable; the pre-registration claims were not verified here) |
| Three features | [N] | **Mislabelled/too weak a description**: half the paragraph is real-network triples, which is [E]. Label it [N]+[E] |
| Prop. C | [L] | Path thresholds: could be [P] at quadratic order along the path (gate validity and convexity in u verified). "Most unstable direction": [N]. Network checks: [N]. **The bicritical identity inside is [I] and should be separate**; its interpretive sentence is too strong. The bracket-versus-prediction wording is mildly overclaimed (two brackets exclude the prediction) |
| Numerical observations | [N] | Item (i) contains a semi-analytic endpoint law that STATUS T10 labels [L]. Make the two consistent (e.g. [N] for c_e, [L] for the law with Phi numerical) |
| STATUS.md T1–T11 | — | Consistent with the above except: T2 needs the proof upgrade; T10 vs tex mismatch; T11 interpretation |

## Recommended text fixes (concise)
1. Prop. A: replace "(up to O(theta^4))" with "(up to O(theta^3))".
2. Lemma A': replace the proof sketch with the convexity argument in Section 1.3. Alternatively, factor and prove the interior-competitor validity coefficients and extend the grid to c in (min(p/q,q/p), 1).
3. Corollary A: split by label. Add one line explaining the double-root condition, and note that a first-order (envelope) estimate would give 8/9 of the coefficient.
4. Prop. C:
   - state that the donor cost is pq·max(1-s^2, 0)^2 and that u* > 0 along the path;
   - state the gate conditions b1/k = p^2/(1+q^2) (opposite) and -(u+k)/((2-p)k) (same);
   - add "full quadratic-order 2x4 perturbation search finds no softer direction (eta = 0.3, 0.5, 0.7) [N]";
   - note that the brackets lie systematically just below the predictions;
   - move the bicritical identity to its own [I] paragraph and replace "Indeed ... vanishes exactly when ..." with the neutral wording in Section 3.
5. B2: drop "barrier O(sigma^2)" or label it heuristic. Report the residual as O(sigma^2) using a smaller FD step.
6. Three features: label [N]+[E]. Numerical observations (i): align the label with STATUS T10.
