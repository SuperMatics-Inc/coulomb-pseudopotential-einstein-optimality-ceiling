# FIX2 — `independent.py` hot-side repair (REVIEW2 R2-1, R2-2, R2-3; REVIEW3 R3-1…R3-4)

Status: **fix applied, awaiting review.** Nothing here is self-certified `PROVED`/`CERTIFIED`;
the labelling is the reviewer's call. No file outside this lane was modified; `replay.py`,
`bounds.json`, `fixtures.json` and every `REVIEW*.md` are untouched.

Rejected bytes are preserved as `independent.v2-rejected.py` (the version REVIEW2 audited).
The round-3 candidate that REVIEW3 audited is preserved as `independent.v3.py`; the current
`independent.py` is that file plus the R3-1/R3-2/R3-3 patch and the new `--selfcheck` mode
(§3b). Superseded `independent.v1.py`, `replay.v1.py`, `crosscheck.v1.py` are unchanged.

## 0. What changed, at a glance

The rejected hot device was replaced wholesale (entrywise lower bound → signed interval
centre + radius; head/tail split with no omitted modes; infinite-tail Schur penalty
subtracted on the diagonal; exact `int64` Gram check). Every certified quantity in the file
is now an exact integer (scale `SC = 2**17`) or an exact `Fraction`; `float64` appears only
as a *proposal generator* (eigenvector guesses, Cholesky factors), and every proposal is
re-verified in exact integer arithmetic or refused.

| finding | rejected code | new code | RIGOR.md |
|---|---|---|---|
| R2-1 entrywise off-diagonal lower bound | `hot_bound` `independent.v2-rejected.py:152-183` (`A -= upa[...]`) | `hot_enclosure` `independent.py:224-268`, `hot_head` `independent.py:270-291`, `head_radius` `independent.py:206-221` | §5 items 1-2 |
| R2-2 omitted modes / finite-`m` tail / penalty off every entry | `hot_bound` `independent.v2-rejected.py:179-181` (`tail_gap(...,NB)`, `A -= ceil_(...)` on all entries) | `hot_head` `independent.py:244,287-288`, `tail_gap` `independent.py:147-178`, `tail_penalty` `independent.py:180-204` | §5 item 3 |
| R2-3 float Gram / float residual | `positive` `independent.v2-rejected.py:186-208` (`Lh = np.rint(L*GS)` at :198 stays float64) | `positive` `independent.py:293-346` (`independent.py:308-310,330,336`) | §5 item 4 |
| adversarial regression | absent | `adversarial` `independent.py:597-635`, table `independent.py:425-435`, flag `independent.py:783-785` | §5 «Regression probes» |
| R3-1 swapped endpoint brackets (`radius <= 0`) | `independent.v3.py:235-236` (`lower = -(dn…)`, `upper = -(up…)`, `radius = upper - center`) | `hot_enclosure` `independent.py:252-261`; new `--selfcheck` `independent.py:636-717`, flag `independent.py:786-789` | §5 items 1, «Enclosure self-check» |
| R3-2 false endpoint inequality in the `tail_gap` proof | `independent.v3.py:150` (`2A_j(hi) - A_{j-m}(lo) >= A_m(hi)`) | `tail_gap` docstring `independent.py:147-178` (fixed-$q$ first) | §5 item 3 |
| R3-3 `NaN`/overflow guards | `independent.v3.py:184,203,283` | `independent.py:198,218,310,330` | §5 item 4 |

Two prose descriptions of the rejected hot device became false when it was replaced, and
are corrected here (same lane, no other change): `RIGOR.md` §8 item 3 (the truncation list)
and the `RESULT.md` Finding-2 paragraph (which also listed a non-existent `einstein_hi`
receipt field and the old 15-box count; current fields are `einstein_q`, `einstein_C`,
`boxes`, `mix`, and the count is 19). Neither correction changes a number.

## 1. R2-1 — entrywise off-diagonal lower bound invalid for mixed-sign vectors

**Defect (confirmed).** `hot_bound` replaced every off-diagonal pairing entry
$-a_r(q)$ by $-a_r(q_{\rm lo})$ and the diagonal by a lower bound, i.e. it produced a matrix
$A$ with $A_{ij}\le F_{ij}$ entrywise, then subtracted a scalar. Entrywise domination gives
$x^{\sf T}Ax\le x^{\sf T}Fx$ only for $x\ge0$ (Z-matrix reasoning). With $\mu^*>0$ the
$\mu_*$ block puts positive entries on the diagonal and the off-diagonal bound on the
off-diagonal, so the block is not a Z-matrix and the implication fails; the rejected
verifier returned CERTIFIED POSITIVE on boxes where the folded form is negative (§4 below).

**Fix.** A signed-matrix interval enclosure plus one PSD domination step, valid for all
real vectors (`hot_enclosure` `independent.py:224-268` + `hot_head` `independent.py:270-291`):

* `up = ceil(SC*a_r(q_lo))`, `dn = flr(SC*a_r(q_hi))`; the head block is enclosed between
  `lower = -(up+up)` (the value at $q_{\rm lo}$, the larger magnitude) and `upper =
  -(dn+dn)` (the value at $q_{\rm hi}$, the smaller magnitude), so `lower <= F*SC <= upper`
  with `lower <= upper`; the centre is `center = (lower+upper)//2` and the radius is
  `radius = max(upper-center, center-lower) = ceil((upper-lower)/2) >= 0`, which covers
  BOTH ends of the bracket (see the R3-1 patch below; the round-2 bytes had the two names
  swapped). `independent.py:250-259`. Symmetry is preserved because Hankel
  indices are symmetric in $(i,j)$.
  The diagonal deviation is one-sided: it is bounded below by
  $2i+1+2A_i(q_{\rm hi})-a_{2i+1}(q_{\rm lo})+\lfloor2\mu_*\rfloor 2^{17}$
  (`independent.py:262-266`) — $A_i$ is *decreasing* in $q$ and $a_{2i+1}$ too, so both
  bounds are exact lower bounds.
* The radius is removed **on the diagonal only**: with a positive weight vector $h$,
  $\rho_i=\lceil\frac{1}{h_i}\sum_j\mathcal R_{ij}h_j\rceil$ (`head_radius`,
  `independent.py:206-221`, exact integer row sums, one ceiling per row,
  $h_i=2^{22}/(i+1)$). By AM-GM $2|x_ix_j|\le x_i^2h_j/h_i+x_j^2h_i/h_j$, hence
  $\sum_{i\ne j}\mathcal R_{ij}|x_ix_j|\le\sum_i\rho_ix_i^2$ for **every** real $x$, mixed
  signs included, so $C-\mathrm{diag}(\rho)\preceq F$ on the head block. Nothing is
  subtracted entrywise.

The bound is strict (no sign or Z-matrix statement is used anywhere in the hot path).

## 2. R2-2 — omitted modes, finite-`m` tail bound, penalty on every entry

**Defect (confirmed).** (i) the block covered modes $i<400$ while `tail_gap` was called with
`n = 800`, so modes $400\le j<800$ were in neither the block nor the tail, and the boundary
coupling distance $|i-j|=1$ (at $i=399,j=400$) was replaced by $m+1$; (ii) `A -=
ceil_(...)` subtracted a scalar from *every* entry of `A`, i.e. the rank-one matrix
$c\,\mathbf 1\mathbf 1^{\sf T}$, which vanishes on zero-sum vectors instead of shifting the
diagonal; (iii) the infinite tail was bounded as if it had only $m$ columns.

**Fix.** One split at $m=\max(NB,2k+1)=\max(160,2k+1)$ with **no gap**
(`independent.py:244`); the head is $0\le i<m$ and the infinite tail is $j\ge m$
(`hot_head`, `independent.py:270-291`). Because $m\ge 2k+1$ the whole $\mu_*$ block lies in
the head, so the tail carries no Coulomb term at all.

* Infinite tail (`tail_gap`, `independent.py:147-178`): row $j\ge m$ has diagonal
  $2j+1+2A_j-a_{2j+1}$ and off-diagonal absolute row sum
  $\le A_{j-m}(q_{\rm lo})+S_1(q_{\rm lo})+S_{j+m+1}(q_{\rm lo})$ (each distance
  $r\le j-m$ occurs at most twice, and the whole rest is dominated by $S_1$). At FIXED
  $q\in[q_{\rm lo},q_{\rm hi}]$ the $a_r(q)\ge0$ give
  $2A_j(q)-A_{j-m}(q)=A_j(q)+\sum_{t=j-m+1}^{j}a_t(q)\ge A_j(q)\ge A_m(q)$ for every
  $j\ge m$; only then pass to the endpoints term by term ($A_j(q)\ge A_j(q_{\rm hi})$,
  $A_{j-m}(q)\le A_{j-m}(q_{\rm lo})$, $a_{2j+1}(q)\le a_{2j+1}(q_{\rm lo})$,
  $A_m(q)\ge A_m(q_{\rm hi})$). So **every** gap is at least
  $$g=2m+1+A_m(q_{\rm hi})-a_{2m+1}(q_{\rm lo})-S_1(q_{\rm lo})-S_{2m+1}(q_{\rm lo})>0,$$
  uniformly over the infinitely many rows. $S_1$ is summed exactly to $R=8(m+1)$ terms and
  closed by $\sum_{r>R}r^{-2}\le1/R$; $S_{2m+1}\le\lambda/(2m\,q_{\rm lo})$
  (`a_r <= lam/(q lo r^2)` because $\sum_ip_iu_i=1$). So the tail block $T$ satisfies
  $T\succeq gI$ — a statement about the infinite tail, not a finite truncation.
* Schur complement (`tail_penalty`, `independent.py:180-204`). Completing the square in the
  tail variable, $x^{\sf T}Hx+2x^{\sf T}B^{\sf T}y+y^{\sf T}Ty\ge
  x^{\sf T}(H-\tfrac1gB^{\sf T}B)x$ for every real $(x,y)$; column $l\ge m$ of $B$ obeys
  $|B_{il}|=a_{|i-l|}+a_{i+l+1}\le2\lambda/(q_{\rm lo}(l-m+1)^2)$. Then
  $\theta_i=\lceil\frac1g\sum_j\sum_{l=m}^{L}b_{il}b_{jl}\rceil$ with integer
  $b_{il}\ge|B_{il}|$ rounded up at scale $2^{17}$, exact $l$-sums to $L=8m$, and the far
  columns $l>L$ bounded by $m(2\lambda/q_{\rm lo})^2/(3(L-m)^3)$ (since
  $\sum_{t>T}t^{-4}\le1/(3T^3)$ and there are $m$ head rows) added to every row. This
  dominates the whole quadratic form of $\tfrac1gB^{\sf T}B$, i.e.
  $\tfrac1gB^{\sf T}B\preceq\mathrm{diag}(\theta)$ — **the penalty is subtracted on the
  diagonal only** (`independent.py:288`): `center[np.diag_indices(m)] -=
  head_radius(radius) + tail_penalty(lam, lo, spec, m, g)`.

Therefore $A:=C-\mathrm{diag}(\rho)-\mathrm{diag}(\theta)\preceq F$ on the whole half-line,
as a quadratic form.

## 3. R2-3 — `positive()` in exact integers

`positive` (`independent.py:293-346`) now requires and produces exact integers:

* `need(A.dtype == np.int64, ...)` (`independent.py:308`); the matrix entering it is built
  from integer `ceil_`/`flr_` of exact `Fraction` values.
* The float Cholesky only *proposes* $L$; the factor is re-rounded and **cast** to int64
  (`independent.py:336`, `Lh = Lh.astype(np.int64)`), so `Lh @ Lh.T` and
  `res = A*(G*G//SC) - Lh @ Lh.T` are exact int64 products.
* Exactness of every int64 product is *guarded*, never assumed: $|L_h|<2^{31}$ and every
  Cauchy-Schwarz row norm $<2^{60}$ keep each entry of $L_hL_h^{\sf T}$ exact,
  $|A|G^2/2^{17}<2^{61}$ keeps $A\cdot$factor exact, $|R|<2^{61}/n$ keeps
  $2R_{ii}$ and $\sum_j|R_{ij}|$ exact. A failed guard skips that candidate (fail closed):
  nothing is clamped, rounded silently or dropped in favour of a float verdict.
* The exact test is $R_{ii}>0$ and $2R_{ii}>\sum_j|R_{ij}|$ for all $i$; a symmetric matrix
  that is strictly diagonally dominant with positive diagonal satisfies
  $R\succ0$, so $A\,G^2/2^{17}=L_hL_h^{\sf T}+R\succ0$ and hence $A\succ0$.
* Several scales $G\in\{2^{26},\dots,2^{20}\}$ and shifts are tried, with one exact-residual
  Newton correction of $L$; a failure of one proposal is not a verdict, a failure of them
  all refuses the box and `cover` bisects.

## 3b. REVIEW3 findings (R3-1 … R3-4)

REVIEW3 kept all three R2 fixes but rejected the *written* enclosure step and two guards.
All four findings were confirmed against the round-3 bytes (`independent.v3.py`) and fixed
by editing `independent.py` only; no parameter, fixture, bracket or claim was changed.

**R3-1 (P1, confirmed): the endpoint brackets were swapped, so the radius was nonpositive.**
`independent.v3.py:235-236` computed `lower = -(dn[diff]+dn[hank])` (the value at $q_{\rm hi}$)
and `upper = -(up[diff]+up[hank])` (the value at $q_{\rm lo}$). Since $a_r$ decreases in $q$,
`upper <= lower`: the centre `(lower+upper)//2` is still the midpoint, but
`radius = upper - center <= 0`, so the enclosure claimed a nonpositive (and in fact negative,
clamped to 0 only on the diagonal) radius over a bracket whose half-width is thousands of
integer units at scale $2^{17}$.

*Fix* (`independent.py:250-259`): the names now follow the values,

```
upper = -(dn[diff] + dn[hank])      # value at hi: the smaller magnitude
lower = -(up[diff] + up[hank])      # value at lo: the larger magnitude
need(np.all(lower <= upper), ...)
center = (lower + upper) // 2
radius = np.maximum(upper - center, center - lower)   # = ceil((upper-lower)/2)
need(np.all(radius >= 0), ...)
```

so `center - radius <= lower` and `upper <= center + radius` entrywise, i.e.
$|2^{17}F_{ij}(q)-C_{ij}|\le\mathcal R_{ij}$ for **every** $q\in[q_{\rm lo},q_{\rm hi})$ and
every off-diagonal entry, odd bracket widths included (the `-((x))//2` vs `(x)//2` one-unit
slack that REVIEW3 measured is exactly what `np.maximum(...)` removes). The diagonal stays
one-sided ($C_{ii}\le2^{17}F_{ii}$, $\mathcal R_{ii}=0$), which is all §5 item 1 needs.

*New regression* — `independent.py --selfcheck` (`independent.py:636-717`): six windows
($r=1,3,4,8,9,125$) enclosing, in **exact rational arithmetic** (`exact_head`), the head
entries at three interior $q$ and requiring `lower <= value <= upper`,
`|value - centre| <= radius` and `centre_ii <= value_ii` entrywise with the same mask.
573\,003 exact rational comparisons, exit 0 on the current bytes. Teeth: replaying the
round-3 formula (`v2_enclosure`, i.e. `lower/upper` swapped and `radius = upper - center`)
on the same six windows violates the invariant on **189\,950 / 189\,950** off-diagonal
entries — `radius <= 0` on every one of them, `upper <= lower` on every one — with a maximum
excess of $|2^{17}F_{ij}(q_{\rm mid})-C_{ij}|$ over $\mathcal R_{ij}$ of $45\,239$ integer
units at scale $2^{17}$ (worst window $r=3$, $\lambda=10$)
(throwaway probe `C:/t/CutoffFix2/r31_teeth.py`, deleted with the temp dir). The invariant
is also the premise of §5 item 2, so the fix is load-bearing: on the round-3 bytes the
"enclosure" certified nothing.

**R3-2 (P1, confirmed): the written `tail_gap` proof used a false endpoint inequality.**
`independent.v3.py:150` argued $2A_j(q_{\rm hi})-A_{j-m}(q_{\rm lo})\ge A_m(q_{\rm hi})$;
that is false for a wide window at $j\approx2m$ (the two terms are evaluated at *different*
$q$). The *code* was already sound because both terms are taken at the same $q$.

*Fix* (proof only, no arithmetic change): `tail_gap`'s docstring (`independent.py:147-178`)
and RIGOR.md §5 item 3 now argue in two steps — first at a FIXED $q\in[q_{\rm lo},q_{\rm hi}]$,
$2A_j(q)-A_{j-m}(q)=A_j(q)+\sum_{t=j-m+1}^{j}a_t(q)\ge A_j(q)\ge A_m(q)$; only then pass to
the endpoints term by term ($A_j(q)\ge A_j(q_{\rm hi})$, $A_{j-m}(q)\le A_{j-m}(q_{\rm lo})$,
$a_{2j+1}(q)\le a_{2j+1}(q_{\rm lo})$, $A_m(q)\ge A_m(q_{\rm hi})$) to obtain
$g=2m+1+A_m(q_{\rm hi})-a_{2m+1}(q_{\rm lo})-S_1(q_{\rm lo})-S_{2m+1}(q_{\rm lo})>0$.
The certified integer `g` is identical to the round-3 value on every window: the proof was
wrong, the number was not.

**R3-3 (P2, confirmed): guard placement.** (i) `tail_penalty` guarded one product
`max(be) * max(col)`; it now guards the whole sum
`need(int(be.max()) * int(col.sum()) < 2**62)` *before* `be @ col`
(`independent.py:196-199`), plus nonnegativity of the coupling. (ii) `head_radius` guarded
`rows.max()` *after* the matmul; it now guards
`max|radius| * sum(h) < 2**62` before `np.abs(radius) @ h` (`independent.py:216-219`).
(iii) `positive` now asserts an exactly square (`independent.py:309`) and exactly symmetric
(`independent.py:310`) `int64` matrix and requires the proposal factor to be finite before
the `int64` cast (`independent.py:330`), so a `NaN`/`inf` from `np.linalg.solve` fails
closed instead of wrapping to `-2**63`. Documented in RIGOR.md §5 item 4.

**R3-4 (P2/P3, confirmed): prose drift.** `m = max(160, 2k+1)` (`NB = 160`) is now stated
in RIGOR.md §5/§8, `RESULT.md`'s Finding-2 paragraph and §2 above; the module docstring
(`independent.py:19-45`) describes the signed-interval device instead of the rejected
entrywise `hot_bound`; "$A_i$ is increasing in $q$" was corrected to *decreasing* there and
in RIGOR.md (the code already used $A_i(q_{\rm hi})$, the correct lower bound); the
`RESULT.md` $a_1$ decimals are the exact values ($180300/66011=2.73136$,
$1280400/680017=1.88289$, $35600/10001=3.55964$) and the `crosscheck.v1.py` disagreement is
attributed to its four discretization bugs, not to a `(u,p)` swap. No number in any
certificate changed.

## 3c. REVIEW4 (verdict PASS) — the two remaining P3 prose nits, now closed

`COMMON-CUTOFF-REVIEW/REVIEW4.md` (20 Nov 2026, 16:14) records R3-1…R3-4 resolved on the
current bytes, 20/20 `CHECKS.txt` rows at their expected exit codes, `--selfcheck` with
teeth against `independent.v3.py`, the three REVIEW2 boxes plus the five round-4 probes
refused, and **no claim shrinking**. It left two non-blocking P3 prose items; both are fixed
here, and neither touches code, proofs or any certified number:

* **P3-1 (direction typo in the enclosure prose).** `RIGOR.md:209` and `FIX2.md:162` wrote
  the containment as `lower <= C - R` / `C + R <= upper`, the reverse of what the radius
  means. The ring is `center - radius <= lower` and `upper <= center + radius`; both files
  now say exactly that (the code in `independent.py:257` and its `--selfcheck` always used
  the correct direction, which is why no numeric result moved).
* **P3-2 (stale attribution).** `RIGOR.md` §8 item 5 (line 398) still blamed the factor
  2.6–7 `crosscheck.v1.py` disagreement on a `(u,p)` unpacking swap; it now names the four
  discretization bugs that `RESULT.md` Finding 3 documents (bosonic instead of fermionic
  frequencies, doubled $\lambda$, wrong $Z_n$, unsymmetrized kernel).

Status of this file: **fix applied, awaiting review.** The labels PROVED/CERTIFIED for the
published statements are the reviewer's to assign; §6 only reports what the two checkers
do and what they agree on.

## 4. Adversarial probes (REVIEW2 R2-1/R2-2 regression)

`independent.py --adversarial` (table `independent.py:425-435`, driver `independent.py:597-635`).
For each probe the **control** is an exact rational evaluation of the folded form at
$q_{\rm bad}$ on an integer witness (`folded_exact`, one integer correlation
$c_d=\sum_ix_ix_{i+d}$ times exact rational weights, cross-checked against the float
contraction of the same integers); a negative value proves no sound device can certify a box
through $q_{\rm bad}$. Then both the documented box (bounded `certified` cover, budget 64)
and a point-wide box ending at $q_{\rm bad}$ must be refused.

| probe $(\lambda,\mu^*,R^2)$ | $q_{\rm bad}$ | exact folded-form value (600 modes) | float block $\lambda_{\min}$ | documented box | result |
|---|---|---|---|---|---|
| (10, 15, 9) | 3745657/10^8 | $-8.41646\times10^{12}<0$ | −0.392949 | [0.033058, 0.037457) | box **refused**, point box **refused** |
| (12, 12, 9) | 9970489/10^8 | $-2.89796\times10^{12}<0$ | −0.140239 | [0.081633, 0.099707) | box **refused**, point box **refused** |
| (3, 2, 9/4) | 83845/10^7 | $-3.82551\times10^{10}<0$ | −0.00184531 | [0.008264, 0.008385) | box **refused**, point box **refused** |

`independent.py --adversarial` → **exit 0**,
`"adversarial probes: every box with an exactly negative folded form was refused"`.

Rejected-verifier reproduction (`independent.v2-rejected.py`, loaded by path, same probe
table; script kept only under `C:/t/CutoffFix2/repro_rejected.py` and deleted with it):

```
l10_m15_R9: rejected verifier CERTIFIED POSITIVE on [0.033058, 0.037457) in 1 boxes (folded form is negative at q=3745657/100000000)
l10_m15_R9: rejected verifier point box at q_bad -> False
l12_m12_R9: rejected verifier CERTIFIED POSITIVE on [0.081633, 0.099707) in 1 boxes (folded form is negative at q=9970489/100000000)
l12_m12_R9: rejected verifier point box at q_bad -> False
case1_k16: rejected verifier CERTIFIED POSITIVE on [0.008264, 0.008385) in 1 boxes (folded form is negative at q=16769/2000000)
case1_k16: rejected verifier point box at q_bad -> False
```

The documented false positive is reproduced on all three probes; the corrected device
refuses them. (In this reconstruction the rejected verifier's own point-wide box at
$q_{\rm bad}$ returned False — the false positives it produces are the documented *boxes*.)

## 5. Every CHECKS.txt command, re-run

All commands run from `C-LAMBDA-MU/COMMON-CUTOFF` with
`UV_CACHE_DIR=D:/dev/.cache/uv uv run --no-project --with numpy --with scipy --with mpmath
python -B <script>`, 20 Nov 2026, CPython 3.13 on Davis's laptop. Exit codes: 0 = verified,
1 = mutant refused as required, 2 = a mutant's control broke (never observed).

| command | exit | key output |
|---|---|---|
| `replay.py` | 0 | all 7 instances bracketed (`C_E` 0.0083714088, 0.0033761862, 0.0012782035, 0.016843376, 0.088327409, 0.06205002, 0.10747379), "stored bounds.json verified without rewriting" |
| `replay.py --mutant sign` | 1 | "control passed: the unmutated (repulsive-sign) hot certificate covers the interval" / "mutant refused: the sign-flipped mask term is not certified positive (… 0.0095 0.00950000458353 K=15)" |
| `replay.py --mutant spectrum` | 1 | two controls passed; "mutant refused: the Einstein line is not unstable at the mixture witness q=1/100: the two-line verdict does not transfer" |
| `replay.py --mutant tail` | 1 | "control passed: the true far tail term is below the bound" / "mutant refused: with far_lump disabled the exact tail guess exceeds the bound" |
| `replay.py --mutant coulomb` | 1 | "control passed: the Einstein cold witness keeps its sign" / "mutant refused: the cold certificate at q_lo dies when the Coulomb term is doubled" |
| `replay.py --mutant endpoint` | 1 | "control passed: the Einstein cold witness keeps its sign" / "mutant refused: a cold witness is refused at the certified-stable endpoint q_hi" |
| `independent.py` | 0 | 3 counterexamples + 4 anchors: cold Einstein negative at $q_{\rm lo}$; hot Einstein positive on `[0.0095, 3.07269) in 19 boxes`, `[0.003, 1.76999) in 36`, `[0.003, 4.38414) in 37`, `[0.012, 0.518653) in 10`, `[0.3105, 0.518653) in 12`, `[0.4575, 3.07269) in 14`, `[4.565, 12.2824) in 11`; `C_E` in 0.008371408803-0.008956148933, 0.003376186186-0.006164044441, 0.00127820346-0.004358637623, 0.01684337597-0.01743455049, 0.08832740877-0.08868515592, 0.06205001997-0.06215199214, 0.1074737872-0.1075326931; mixtures unstable at their witness while Einstein is stable on its own ray; "bounds.json: every field … agrees with the independent recomputation" / "independent verification of the common-cutoff certificates: OK" |
| `independent.py --selfcheck` | 0 | `"interval enclosure selfcheck: 6 windows x 3 interior q, 573003 exact rational entry comparisons against lower/upper/centre/radius: OK"` |
| `independent.py --adversarial` | 0 | §4 above |
| `independent.py --mutant endpoint` | 1 | "mutant refused: the Einstein form is not positive on [q_lo, q_ph): hot interval cannot be certified: 0.0083 0.00830000025397 K=16" |
| `independent.py --mutant coulomb` | 1 | "mutant refused: doubling mu* removes the cold sign at q=1/100 (form value 3.41541e+13 >= 0)" |
| `independent.py --mutant spectrum` | 1 | "mutant refused: the p -> 1-p mixture (int u dp != 1) is refused by the second-moment guard" |
| `independent.py --mutant receipt` | 1 | "mutant refused: a shaved C_E bracket escaped the receipt check: …" |
| `structure.py` | 0 | "structural checks passed on 400 rational two-line spectra (exact arithmetic)" |
| `structure.py --mutant` | 1 | "mutant controls refused 36 perturbed statements (as required)" |
| `structure.py --folded` | 0 | "folded identity (matrix form = display form) verified exactly in 120 rational trials" |
| `structure.py --folded --mutant` | 1 | "folded mutant: the display missing the tail term differs from the matrix in 120/120 trials (detected, as required)" |
| `crosscheck.py` | 0 | every Einstein bracket reproduced, every mixture unstable with a strictly larger onset $q$; direct vs folded $\lambda_{\max}$ agree to $\le4.4\times10^{-16}$ (no FAIL lines in the base run) |
| `crosscheck.py --mutant mirror` | 1 | refused (direct vs folded eigenvalues no longer agree) |
| `crosscheck.py --mutant zshift` | 1 | refused (same) |

Wall times on this machine (one batch run of all 20 rows, 294 s total): `replay.py` 31 s,
its mutants 1-6 s; `independent.py` 83 s (37 s when run alone); `--selfcheck` 7 s;
`--adversarial` 51 s; `independent.py` mutants 1-44 s; `structure.py` and its mutants <1 s;
`crosscheck.py` 15 s, its mutants 17 s each.

## 6. Do the published statements still hold?

* **Hot side, every instance.** `independent.py` certifies positivity of the Einstein
  spectral form on `[q_hi, q_ph)` for all three counterexamples and all four anchors with
  the new device, i.e. the whole claimed region is still covered. The certified intervals
  are exactly the contract of `run_case` (`[high, phonon handoff)`), and the bases `q_hi`
  are taken from the fixtures, unchanged.
* **Brackets.** Every recomputed `C_E` bracket lies inside the stored `bounds.json` bracket
  (checked field by field by `check_receipt`), and `replay.py` re-verifies the stored
  `bounds.json` without rewriting it. The two checkers therefore agree on every published
  bracket: 0.008371408803, 0.003376186186, 0.00127820346, 0.01684337597, 0.08832740877,
  0.06205001997, 0.1074737872 (matching RESULT.md's outward-rounded decimals).
* **$C(1)\in[0.11461945,0.11461957]$.** Unaffected by this repair: it is the zero-Coulomb
  (`C-LAMBDA/brackets.json`) statement consumed by `phonon_handoff()`, and the hot-side
  change does not alter any cold number, any `q_hi` or any bracket. No part of the claim
  shrinks; nothing had to be weakened.
* The only observable difference is the number of certified boxes per interval (a
  tightness artefact of a different bound; `check_receipt` requires a positive integer
  exactly because `replay.py`'s count is its own receipt pin).
* **REVIEW3 round.** None of R3-1…R3-4 changed a certified number: the R3-1 fix repairs a
  *bound* (the enclosure now really encloses), the R3-2 fix repairs a *proof*, R3-3
  tightens guards that never fire on these inputs, R3-4 fixes prose. Re-running everything
  gives the same seven intervals, the same boxes (19/36/37/10/12/14/11) and the same
  brackets as the round-3 bytes: `replay.py` exit 0, `independent.py` exit 0, the two
  checkers agree on all seven published statements, and the three REVIEW2 boxes plus their
  point boxes are still refused (`--adversarial` exit 0), as are all nine certificate
  mutants (5 `replay.py`, 4 `independent.py`) and the 5 `structure.py`/`crosscheck.py`
  refusals.
  **The claimed region does not shrink** — but certification is the reviewer's call: this
  file claims only "fix applied, checks green".

## 7. Cleanup

Scratch `C:/t/CutoffFix2/` (batch logs `runall.log`/`runall2.log`, `independent.out`, the
round-4 rerun's `runchecks.sh` and `logs/` (20 per-row logs), and the throwaway probes,
among them `repro_rejected.py` and `r31_teeth.py`), plus the exploratory `C:/t/CutoffFix2b/`
probe directory, were deleted after this file was written (`rmdir /s /q`, verified absent);
no other temporary state was created, and nothing outside this lane was
touched (`replay.py`, `bounds.json`, `fixtures.json`, `REVIEW*.md` are unchanged). No paid compute, no git operation, no push,
no email, no publication.
