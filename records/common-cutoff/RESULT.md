# Einstein optimality at a common cutoff with positive $\mu^*$: certified counterexamples

## Question

Flat density of states, infinite electronic band, isotropic linearized Migdal-Eliashberg
pairing with a **pairing-only** Coulomb subtraction
$\mu^* 1_{|\omega_n|<\omega_c}1_{|\omega_m|<\omega_c}$ (strict cutoff on **both**
indices, no Coulomb term in the normal self-energy $Z$), in exactly the conventions of
[the bracket-and-mustar records](../the bracket-and-mustar records/RIGOR.md). With the cutoff $\omega_c$ **common**
(spectrum independent, fixed per instance in units of $\sqrt M$, equivalently of
$\Omega_E=\sqrt{M/\lambda}$ at fixed $(\lambda,M)$) and $\mu^*>0$ fixed, does the single
Einstein line maximize the linear onset $T_{\rm lin}$ at fixed $(\lambda,M)$?

## Verdict

**CERTIFIED counterexample** (exact rational certificates in `bounds.json`, re-derived by
a second, differently built verifier, and independently reviewed; see "Status and changes
per review finding" — the label is CERTIFIED, not PROVED, until the revised version is
re-reviewed). No. Three two-line spectra with the same
$(\lambda, M, \mu^*, \omega_c)$ as Einstein, and hence the same
$\Omega_E=\sqrt{M/\lambda}$, have a linear onset strictly above the certified Einstein
upper endpoint. All three have $\mu^*/\lambda>1/2$.

| case | $\lambda$ | $\mu^*$ | $\omega_c/\Omega_E$ | Einstein $q_E$ (certified) | Einstein $C_E$ (outward-rounded) | mixed spectrum ($p_i$ at $u_i=\Omega_i^2/\Omega_E^2$) | unstable at $q$ | $T$ gain |
|---|---|---|---|---|---|---|---|---|
| `einstein-counterexample` | 3 | 2 | 1.5 | $[0.0083,\,0.0095]$ | $[0.0083714088,\,0.0089561490]$ | $590/599$ at $1/10$, $9/599$ at $60$ | $1/100$ | $2.6\%$ |
| `counterexample-wide` | 2 | 3/2 | 2 | $[0.0009,\,0.003]$ | $[0.0033761861,\,0.0061640445]$ | $4975/4998$ at $2/25$, $23/4998$ at $200$ | $1/200$ | $29\%$ |
| `counterexample-strong` | 4 | 4 | 2 | $[129/500000,\,0.003]$ | $[0.0012782034,\,0.0043586377]$ | $2475/2498$ at $2/25$, $23/2498$ at $100$ | $1/100$ | $83\%$ |

Here $q=(2\pi k_BT/\Omega_E)^2$, $C=\sqrt q/(2\pi\sqrt\lambda)$ and
$T$ gain $=\sqrt{q_{\rm mix}/q_E^{\rm hi}}-1$. Every $C_E$ interval above is rounded
**outward** from the exact rationals in `bounds.json` (lower bound down, upper bound up to
eight significant digits), so the printed intervals are still enclosures. In each row the
mixed spectrum has $\sum_i p_i=1$ and $\sum_i p_iu_i=1$ with $p_i$ the listed **probability
weights** (the line couplings are $\lambda p_i$), so $M$ and $\lambda$ match Einstein's
exactly, hence the **same** $\Omega_E$ and the **same** numerical cutoff.
The Einstein column is an exclusion, not an estimate: at $q_E^{\rm hi}$ the two
verifiers certify that no instability exists (minimisation over a finite section plus a
controlled tail), and at $q_E^{\rm lo}$ they certify one does. The mixed spectra are
certified unstable at the quoted $q$ in exact rational arithmetic by an explicit
rational trial vector.

**Consequence for the campaign.** Under the *spectrum-dependent* cutoff
$\omega_c=10\Omega_{\max}$, [the bracket-and-mustar records](../the bracket-and-mustar records/RESULT.md) showed the
supremum is degenerate and Einstein is not a maximizer; that degeneracy used a line of
vanishing weight to open the cutoff. These counterexamples need **no** cutoff change:
the cutoff is a property of the problem instance, not of the spectrum.

## Einstein reference values (CERTIFIED, not ceilings)

Exact rational enclosures of $q_E$ and $C_E$ for the single line are in `bounds.json`;
they are reference values for the comparisons above and are *not* proposed as ceilings
at $\mu^*>0$ (that is exactly what fails).

| instance | $\lambda$ | $\mu^*$ | $\omega_c/\Omega_E$ | $q_E$ | $C_E$ |
|---|---|---|---|---|---|
| `anchor-l1-mu1/2-R1` | 1 | 1/2 | 1 | $[0.0112,\,0.012]$ | $[0.016843375,\,0.017434551]$ |
| `anchor-l1-mu1/10-R1` | 1 | 1/10 | 1 | $[0.308,\,0.3105]$ | $[0.088327408,\,0.088685156]$ |
| `anchor-l3-mu1-R3/2` | 3 | 1 | 1.5 | $[0.456,\,0.4575]$ | $[0.062050019,\,0.062151993]$ |
| `anchor-l10-mu1-R3` | 10 | 1 | 3 | $[4.56,\,4.565]$ | $[0.10747378,\,0.10753270]$ |

All $C_E$ intervals in this table are also rounded **outward** (eight significant digits).

**Zero-Coulomb comparison (not a tie-in).** `C-LAMBDA/brackets.json` brackets the
zero-Coulomb ($\mu^*=0$) onset at $\lambda=1$, $R=1$ by
$q\in[0.51865242539,\,0.51865346269]$, i.e.
$C(1)=\sqrt q/2\pi\in[0.11461945,\,0.11461957]$. The $\mu^*=1/10$ row above gives
$C_E\in[0.088327408,\,0.088685156]$, **strictly below** the zero-Coulomb value: the
pairing-only repulsion lowers the onset at fixed $(\lambda,M,\omega_c)$, which is the
expected monotonicity, and the two numbers are different quantities. The zero-Coulomb
threshold is *not* re-certified in this record: the hot interval of §5 would be
$[q_{\rm hi},q_{\rm ph})$ with $q_{\rm ph}(1)$ equal to that very bracket, hence empty
here. What does tie the conventions together is the transfer kernel itself: this record
uses $a_r=\lambda\int u/(u+qr^2)\,dp$ with $a_0=\lambda$, the same $q=(2\pi
k_BT/\Omega_E)^2$ and the same common cutoff, and `structure.py` re-checks the transfer
weights in exact rationals.

## Structural results (PROVED; independently reviewed)

1. **Reduction.** At fixed $(\lambda,M)$, only $R=\omega_c/\sqrt M$ (equivalently
   $\omega_c/\Omega_E$) and $\mu^*$ matter; the mask size follows from
   $(2i+1)^2q<4R^2$. Proof in [RIGOR.md](RIGOR.md) §2. Confirmed in review.
2. **Einstein transfer dominance.** For every spectrum with $\int u\,dp=1$ and every
   $r\ge1$, $a_r^{\rm E}=\lambda/(1+qr^2)\ge a_r=\lambda\int u/(u+qr^2)\,dp$ (Jensen;
   $u\mapsto u/(u+qr^2)$ is concave, $\int u\,dp=\int dp=1$). So at $\mu^*=0$ the
   Einstein *pairing* kernel dominates every other spectrum entrywise, which is the
   mechanism behind the zero-Coulomb ceiling. Confirmed in review.
3. **Why the mechanism fails at $\mu^*>0$.** The folded quadratic form carries the
   transfer with **both** signs: $+\sum_i x_i^2 2\sum_{j\le i}a_j$ (mass, stabilising)
   and $-\sum_{ij}x_ix_j(a_{|i-j|}+a_{i+j+1})$ (pairing, destabilising), while the
   Coulomb block $+2\mu^*(\sum_{i<k}x_i)^2$ is spectrum independent. Entrywise
   dominance of $a$ therefore does not order the forms. A spectrum can place most of
   its moment at a very low frequency $u_1\ll q$ (so $a_r\approx\lambda_1$ for the
   whole near zone, with a *small* mass gain) and put weight $p\ll1$ at a large
   $u_2\gg q$ (so $a_0=\lambda$ and the moment are restored cheaply). At
   $\mu^*>0$ the repulsion removes the lowest block from the game and this trade
   becomes profitable. Verified exactly on 400 random rational two-line spectra in
   `structure.py`.

## Regime map (labelled)

- **$\mu^*/\lambda>1/2$, $\omega_c\gtrsim\Omega_E$:** certified counterexamples above
  (0.67, 0.75, 1.0). Einstein is not optimal.
- **$\mu^*/\lambda\le1/2$:** no counterexample was found in this record; Einstein
  optimality is **open** there (the numerical control in the next section is consistent
  with it). The certified counterexamples sit at $\mu^*/\lambda\in\{2/3,3/4,1\}$, i.e.
  $\mu^*\in\{3/2,2,4\}$, which is outside the physical range of phonon-mediated
  superconductors ($\mu^*\approx0.1$-$0.15$, $\lambda\gg\mu^*$). The Morel-Anderson
  renormalization $\mu^*=\mu/(1+\mu\ln(E_F/\omega_c))$ contains no $\lambda$ and imposes
  **no** $\mu^*\le\lambda/2$ bound; it maps a large bare $\mu$ or a small
  $\omega_c/E_F$ to a modest $\mu^*$, and physically one expects
  $\mu^*\lesssim1/\ln(E_F/\omega_c)\approx0.1$-$0.2$ independent of $\lambda$. So large
  $\mu^*/\lambda>1/2$ is a statement about the *kernel*, well defined in this truncated
  pairing-only model for any $\omega_c>0$, not a claim about reachable material
  parameters. See RIGOR.md §8 item 4.
- **$\mu^*=0$:** Einstein optimality is the C-LAMBDA theorem, untouched here.
- **Near zone $\omega_c\ll\Omega_E$:** the mask is empty and $\mu^*$ is irrelevant, so
  Einstein is optimal there only if it is optimal at $\mu^*=0$, which it is.

## Cross-check in a direct Matsubara discretization (NUMERICAL)

`crosscheck.py` builds the linearized gap equation directly on the full fermionic
Matsubara line, $\omega_n=(2n+1)\pi T$, $n\in[-240,239]$ (480 modes), with
$K_{nm}=a_{|n-m|}-\mu^*c_nc_m$ and the normal diagonal
$Z_n|\omega_n|/(\pi T)=|2n+1|+a_0+2\sum_{r=1}^{i(n)}a_r$ (closed form of the full-line
$\operatorname{sgn}$ sum), restricted to the even gap subspace
$\Delta_{-1-n}=\Delta_n$ by an explicit projector. It shares no code with `replay.py` or
`independent.py` and is float64 throughout, i.e. NUMERICAL.

| case | Einstein onset $q$ (direct) | mixture onset $q$ (direct) | $T_{\rm mix}/T_E$ (direct) | certified $q_E$ bracket |
|---|---|---|---|---|
| `einstein-counterexample` | $0.0083924335$ | $0.012345679$ | $1.21$ | $[0.0083,\,0.0095]$ |
| `counterexample-wide` | $0.00090451693$ | $0.0076896872$ | $2.92$ | $[0.0009,\,0.003]$ |
| `counterexample-strong` | $0.00025806035$ | $0.0256$ | $9.96$ | $[129/500000,\,0.003]$ |
| control $\mu^*=1/10$, $\lambda=1$, $R=1$ | unstable at $q=0.308$ ($\lambda_{\max}=1.0032$) | stable at $q=0.308$ ($\lambda_{\max}=0.1817$) | $<1$ | $[0.308,\,0.3105]$ |
| control $\mu^*=1/2$, $\lambda=1$, $R=1$ | unstable at $q=0.0112$ ($\lambda_{\max}=1.0058$) | stable at $q=0.0112$ ($\lambda_{\max}=0.4133$) | $<1$ | $[0.0112,\,0.012]$ |

Three conclusions. (i) The ordering of the certificates is reproduced in a
discretization that shares nothing with them: every direct onset sits inside or above the
certified bracket, and every certified-unstable mixture point ($q=1/100$, $1/200$,
$1/100$) is unstable there with $\lambda_{\max}-\text{folded}$ agreeing to
$4.4\times10^{-16}$. (ii) The small-$\mu^*$ control uses the *same* two-line mixture
($590/599$ at $u=1/10$, $9/599$ at $u=60$) at $\mu^*/\lambda=1/10$ and $1/2$: it is
decisively **stable** at the Einstein bracket's lower end, where the Einstein line is
unstable, so its onset is strictly below Einstein's. That is consistent with (and no
evidence against) Einstein optimality below $\mu^*/\lambda=1/2$, which remains open.
(iii) There is **no** odd-channel omission and no normalization mismatch: the earlier
factor-2.6/4.3/7 disagreement came from `crosscheck.v1.py`, which carried the four
discretization bugs listed under Finding 3 below (bosonic instead of fermionic
frequencies, a doubled $\lambda$, a wrong $Z_n$ and an unsymmetrized kernel); the current
script's direct even-sector
eigenvalues agree with the folded form of `replay.py` to round-off on all seven
instances (the `--mutant {mirror,zshift}` self-test shows that agreement check fails
when either term is dropped from the folded side). Band doubling
($N=240\to480$) shifts $\lambda_{\max}$ by at most $6.4\times10^{-5}$ and preserves every
sign, so the ordering is not a truncation artifact. The certified chain does not depend
on this script.

## What is open

1. The exact optimal spectrum and the sharp supremum with a common cutoff at
   $\mu^*>0$; the certified examples give a lower bound on the gain, not the sup.
2. Whether Einstein remains optimal for $\mu^*/\lambda\le1/2$ at every cutoff.
3. The $\mu^*$ threshold at fixed $(\lambda,\omega_c/\sqrt M)$, including whether the
   transition is at $\mu^*/\lambda=1/2$ or at a $\omega_c$-dependent value.
4. Independent re-review of this revised submission. The first review verdict was
   REJECT, its core-mathematics part (the three counterexamples and `replay.py`'s exact
   certificates) was confirmed, and Findings 1-8 are addressed below; the `PROVED` label
   is withheld until the revised files are re-reviewed.
5. No literature claim is made here; the counterexamples are statements about the
   truncated model, not about any material.

## Checks run

All scripts are `python -B` from this directory, NumPy/SciPy through
`uv run --no-project --with numpy --with scipy --with mpmath`.

| command | exit |
|---|---|
| `replay.py` (verifies `bounds.json`, does not rewrite) | 0 |
| `replay.py --mutant {coulomb,spectrum,endpoint,tail,sign}` | 1, 1, 1, 1, 1 |
| `independent.py` | 0 |
| `independent.py --selfcheck` (exact rational enclosure invariant) | 0 |
| `independent.py --adversarial` (three REVIEW2 R2 boxes refused) | 0 |
| `independent.py --mutant {endpoint,coulomb,spectrum,receipt}` | 1, 1, 1, 1 |
| `structure.py` | 0 |
| `structure.py --mutant` | 1 |
| `crosscheck.py` (NUMERICAL) | 0 |

Every command with its log and exit code, including the mutant runs, is listed in
`CHECKS.txt`. No git operations, no publication, no email.

## Status and changes per review finding

The verdict label is **CERTIFIED, not PROVED**: the three counterexamples and `replay.py`'s
exact rational certificates are valid and stood the first review, the eight defects that
review found are repaired below, and the `PROVED` label stays withheld until this revised
version is re-reviewed. Superseded scripts are kept as `*.v1.py` so the review's line
references still resolve.

**Finding 1 (`independent.py` swapped $(u,p)$ unpacking).** `weights()` now consumes the
spectrum as `(p, u)` pairs and builds $a_j=\lambda\sum_i p_iu_i/(u_i+qj^2)$;
`spectrum_of()` asserts $0<p<1$, $0<u_1<1<u_2$ and $(1-p)u_1+pu_2=1$ with exact
rational arithmetic, and `a1_pin_check()` compares $a_1$ against hand-computed rationals
for all three fixture mixtures before any certificate runs. The correct $a_1$ values are
the exact rationals $180300/66011=2.73136$, $1280400/680017=1.88289$ and
$35600/10001=3.55964$; the buggy script returned $108.4$, $191.9$, $192.1$. Its
`hot_ok` was also unsound and is replaced (Finding 2).

**Finding 2 (`independent.py` hot certificate unsound, single point, no interval).** The
hot side is rebuilt and, after REVIEW2 R2-1/R2-2/R2-3, is a signed-matrix interval device
(RIGOR.md §5, `FIX2.md`): one split of the folded matrix at $m=\max(160,2k+1)$, so no mode
is omitted and the whole $\mu_*$ block lies in the head; the head is enclosed by an integer
centre (midpoint of the bracket between the values at $q_{\rm hi}$ and $q_{\rm lo}$) plus a
nonnegative radius that covers both ends of that bracket, and that radius is dominated
**on the diagonal** by weighted AM-GM row
sums $\rho_i=\lceil\frac1{h_i}\sum_j\mathcal R_{ij}h_j\rceil$; the infinite tail is
eliminated by its exact Schur complement against a uniform Gershgorin gap $g$ of the whole
infinite tail, giving the diagonal penalty $\theta_i=\lceil\frac1g\sum_j\sum_{l\ge m}
b_{il}b_{jl}\rceil$. No entrywise (Z-matrix) statement is used, so every domination holds
for all real vectors; the resulting exact integer matrix is decided by an exact int64 Gram
residual. The cover of $[q_{\rm hi},q_{\rm ph})$ is split at every mask jump, starting at
the certified $q_{\rm hi}$ and running to the zero-Coulomb phonon handoff
$q_{\rm ph}(\lambda)$. It reports, for the three counterexamples, "hot Einstein positive on
$[0.0095,3.07269)$ in 19 certified boxes", "on $[0.003,1.76999)$ in 36" and
"on $[0.003,4.38414)$ in 37", and it recomputes every `bounds.json` field including
`einstein_q`, `einstein_C`, `boxes` and `mix`. The mixture side is an exact-rational
full-line witness at a single rational $q$, which is what the claim needs.

**Finding 3 (`crosscheck.py` four bugs and the false odd-channel diagnosis).** The script
now solves the full fermionic line $\omega_n=(2n+1)\pi T$, $n\in[-240,239]$, interval by
interval, with a single $\lambda$, the exact symmetric kernel
$D^{-1/2}KD^{-1/2}$ and an explicit even-subspace projector. Its even-sector eigenvalues
agree with the folded form to $4.4\times10^{-16}$ on all seven instances, its direct
onsets land inside the certified brackets, and the earlier factor-$2.6$/$4.3$/$7$
discrepancy is gone. The $a_{n+m+1}$ "odd-channel omission" diagnosis was wrong and is
deleted from `crosscheck.py`, `RESULT.md` and `RIGOR.md` §8.5: the deleted mirror term is
just the negative-Matsubara-axis image, and the real cause was the $(u,p)$ unpacking bug
of `crosscheck.v1.py`.

**Finding 4 (`replay.py` mutants).** The sign mutant now runs its unmutated control first
(the repulsive-sign hot certificate covering the interval) and only then the flipped-sign
statement, which must be refused; a broken control exits 2, the required refusal exits 1.
The spectrum mutant's mirrored-moment test is reachable: the ordering guard rejects
$u_1\leftrightarrow u_2$ with "bad mixture", the moment guard rejects $p\to1-p$ with
"mixture second moment is not one", and the verdict-transfer claim is refused at
$q=1/100$. The silent $2^{62}$ clamp is gone: `contraction` asserts every int64 entry
fits, falls back to unbounded Python integers otherwise, and any out-of-range value is an
assertion failure, never a clamp.

**Finding 5 (`RIGOR.md` §4 display form).** Corrected to
$$\mathcal F(h)=\underbrace{\sum_{i\ge0}(2i+1)h_i^2-2\sum_{i\ge0}h_i^2\sum_{r>i}a_r
+\tfrac12\sum_{i,j\ge0}a_{|i-j|}(h_i-h_j)^2+\tfrac12\sum_{i,j\ge0}a_{i+j+1}(h_i-h_j)^2}_{\mathcal F_0(h)}
+2\mu^*\Big(\sum_{i<k}h_i\Big)^2,$$
i.e. $1/2$ on both Laplacian sums, the $-2\sum_{r>i}a_r h_i^2$ diagonal term, and no
separate $-2\sum_{i<j}a_{j-i}h_ih_j$ term or further $a_0$ subtraction. `structure.py
--folded` re-checks this identity against the matrix form in exact rationals (120 random
trials) and `structure.py --folded --mutant` shows the display without the tail term
differs in every trial.

**Finding 6 (false C-LAMBDA tie-in).** Deleted. The actual zero-Coulomb value at that
instance ($\lambda=1$, $\mu^*=1/10$, $R=1$) is $C(1)\in[0.11461945,\,0.11461957]$ at
$\mu^*=0$, not the $0.08833$ quoted before, which was the $R=1$ zero-Coulomb column with
the wrong cutoff convention. No number in this section is compared against C-LAMBDA.

**Finding 7 (Morel-Anderson).** Stated accurately in both documents: the
Morel-Anderson renormalization is
$\mu^*=\mu/(1+\mu\ln(E_F/\omega_c))$, it maps a large bare $\mu$ or a small $\omega_c/\Omega_E$
to a modest $\mu^*$ and physically one expects $\mu^*\lesssim1/\ln(E_F/\Omega_c)\approx0.1$
or $0.2$ for phonon-mediated superconductors, with $\mu^*\sim0.1$-$0.15$ typical. It
imposes **no** $\mu^*\le\lambda/2$ bound. The certified regime
$\mu^*/\lambda\in\{2/3,3/4,1,3/2\}$ lies far outside that conventional range physically,
while the model remains mathematically well defined there because the retarded
pairing-only kernel still permits $T_{\rm lin}>0$. The regime $\mu^*/\lambda>1/2$ is
therefore a statement about the truncated pairing-only kernel, not a claim about any
material.

**Finding 8 (rounding, labels, RIGOR corrections).** (1) Every $C_E$ bracket in the table
is rounded outward from the certified $q$ bracket. (2) The mixture entries are the
probability weights $p_i$ at $u_i$, not $\lambda_i$. (3) The `RIGOR.md` §6 table column is
$R^2$ and the `anchor-l10-mu1-R3` row carries $9$, matching $\omega_c/\Omega_E=3$ in this
table. (4) `replay.py`'s docstring reads $\omega_c=R\Omega_E$. (5) `RIGOR.md` §3(ii) uses
the Jensen map $u\mapsto u/(u+qr^2)$ with $r\ge1$. (6) `RIGOR.md` §5 states that the cold
witness is exact with no tail bound (the earlier draft claimed one). (7) The
"Midgal-Eliashberg" typo is fixed. The `RIGOR.md` §4 Coulomb paragraph's illustrative
direct values were also stale and now read $\lambda_{\max}$ $4.4033\to0.7556$ for
Einstein against $3.2054\to1.0975$ for the mixture at $q=1/200$ ($\mu^*=0$ and $3/2$).
