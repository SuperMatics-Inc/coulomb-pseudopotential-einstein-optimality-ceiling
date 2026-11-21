# FIX-INDEP — `independent.py` hot-side repair for `MUSTAR-HALF` (`REVIEW.md` F1, F2, F9)

Status: **hot side rebuilt as a sound enclosure; all 8 instances (4 sub-$1/2$ counterexamples + 4 Einstein anchors) CERTIFIED by `independent.py` alone; every mutant refused.**
Per project rules nothing here is labelled `PROVED` or `CERTIFIED` at the result level; the per-instance word below is `CERTIFIED` in the narrow sense "this checker's exact-arithmetic certificate covers every box of $[q_E(\lambda,0),\,4\lambda)$", which is what `RESULT.md` §2 quotes for the second checker.

Files: `independent.py` (repaired), `CHECKS.txt` (rows updated and rerun), this note.
Not touched: `replay.py`, `fixtures.json`, `bounds.json`, `RIGOR.md`, `RESULT.md`, `structure.py`, `REVIEW.md`, `FIX.md`.
Backups, not overwritten: `independent.v1-rejected.py` (review-era unsound device, 15:48), `independent.v2-preR3.py` (checkpoint of `independent.py` after the R3 machinery landed, 17:13). `diff independent.v2-preR3.py independent.py` is exactly two hunks, both inside `--mutant` code (`independent.py:861-862`, `independent.py:882`): the certified path is byte-identical between the checkpoint and the final file.

---

## 1. Per-finding resolution

| Finding | Severity | Defect in the reviewed file | Resolution in v2 | `file:line` |
|---|---|---|---|---|
| **F1** | **P0** | Off-diagonal entries were bounded **from below** entrywise (largest magnitude over the window) and positivity was then argued entrywise. Valid only on the cone $x \ge 0$; for $\mu^* > 0$ the mask block's off-diagonals are $-a_r + 2\mu^*$, so an entrywise order does not even imply $x^{\mathsf T}Ax \le x^{\mathsf T}Fx$ for mixed-sign $x$. | The enclosure is rebuilt so that **no sign assumption enters**: `hot_enclosure` returns `centre` and `radius = max(upper-centre, centre-lower)` with `lower <= SC*F_ij(q) <= upper` for **every** $q \in [lo,hi)$ (both endpoints covered, odd brackets included), and `hot_head` subtracts `diag(rho)` with `rho = head_radius(radius)`, the weighted row-sum bound $\sum_{i\ne j}R_{ij}\lvert x_ix_j\rvert \le \sum_i \rho_ix_i^2$, which holds for **every real $x$**, mixed-sign included. The acceptance test is exact and one-sided, so the matrix order is the only thing used. | `independent.py:255-299` (`hot_enclosure`), `:234-252` (`head_radius`), `:300-322` (`hot_head`), `:323-384` (`positive`) |
| **F2** | **P0** | The tail penalty used a single scalar gap $g \approx 2m$ per row, i.e. $O(1/(mg))$, which underestimates the **boundary** Schur complement $B_{m,m-1}^2/g_m$ by $O(m)$: the row $j=m$ couples to the head through $b_{m-1,m} = a_1 + a_{2m}$, the $\lvert j-i\rvert = 1$ term. | Replaced by the per-row Gershgorin gap of the tail, `tail_gaps`, which keeps $g_m = 2m + O(1)$ at the boundary row (each $A_r$ accumulated as an outward-rounded integer sum, all subtracted terms bounded at $lo$, added terms at $hi$, the two tail sums closed by $\lambda/(q r^2)$ with $\sum_{r\ge T} r^{-2} \le 1/(T-1)$), and by the Cauchy–Schwarz column bound `tail_penalty` with free weights $h_i = 2^{22}/(i+1)$, so each boundary column keeps its true weight rather than an averaged one. | `independent.py:138-189` (`tail_gaps`), `:191-232` (`tail_penalty`), `:474-495` (`hot_claim`) |
| **F9** | **P2** | Residual `int64` subtraction overflow windows in `positive()` (and unguarded row sums/column shifts elsewhere). | Every `int64` product is now **guarded, never assumed**: `positive` requires `int64` dtype, exact symmetry, finite float proposals, refuses `NaN/inf` casts, bounds `|A|*factor < 2^61`, `|Lh| < 2^31`, row norms $< 2^{60}$ and `|R| < 2^61/n` before any integer row sum, and returns the exact Gershgorin lower bound $\min_i (R_{ii}-\sum_{j\ne i}\lvert R_{ij}\rvert)/\text{factor}$ — a failure skips the candidate, nothing is clamped. `head_radius` guards its row sums, `tail_penalty` its columns/shifts, `hot_enclosure` its cumulative diagonal sums. | `independent.py:323-384` (`positive`), `:234-252`, `:191-232`, `:289-293` (cumulative-sum guard and superadditivity spot check) |

Everything else on the hot side follows `COMMON-CUTOFF` (`FIX2.md`, `RIGOR.md` §5, `COMMON-CUTOFF-REVIEW/REVIEW4.md` PASS): window partition at the exact mask jumps `:410-419`, head size $m = \max(NB/2, 2k+1) = 200$ with $k \le 5$ for this package (`NB = 400`, `:55`; the sibling's $m = \max(160, 2k+1)$ is a floor, and taking the larger floor only adds margin), exact integer centre/radius across a window `:255-297`, PSD-dominated Schur completion of the infinite tail `:300-322`, exact integer acceptance `:323-384`, unbounded cover with a hard depth limit that **raises** instead of accepting `:385-392`.

Independence from `replay.py` is preserved: no import, and a different arithmetic path (cold side unfolded exact `Fraction` full line with Hutton's $\pi$ `:420-451`, `:452-462`; hot side folded-form integer enclosure plus exact Gram acceptance; `replay.py` uses the folded identity and a scalar tail bound).

New modes: `--selfcheck` (`:742-806`, `:699-741`) re-verifies the enclosure against **exact rational** head entries and the tail gaps/schur shift exactly; `--adversarial` (`:635-681`) refuses every box through an exactly negative folded form.

---

## 2. Per-instance certify table (`independent.py`, default run)

Head $m = 200$ on every instance; `margin` is the exact Gershgorin lower bound on $\lambda_{\min}$ of the certified head matrix in folded-form units; `boxes` is the number of certified boxes visited by the unbounded cover of the hot range $[q_E(\lambda,0),\,4\lambda)$.

| instance | kind | hot range | status | boxes | tries | head $m$ | min margin | s |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `subhalf-25p6-0p4786` | counterexample | $[0.525,\,102.4)$ | **CERTIFIED** | 2843 | 5680 | 200 | $0.0697854$ | 249.99 |
| `subhalf-26-12over25` | counterexample | $[0.501,\,104)$ | **CERTIFIED** | 1504 | 3002 | 200 | $0.244918$ | 123.92 |
| `subhalf-27-0p4848` | counterexample | $[0.419,\,108)$ | **CERTIFIED** | 541 | 1076 | 200 | $0.504196$ | 39.65 |
| `subhalf-28-0p489` | counterexample | $[0.412,\,112)$ | **CERTIFIED** | 239 | 472 | 200 | $45.2602$ | 16.77 |
| `anchor-l2-mu1-R3/2` | Einstein anchor | $[0.041,\,8)$ | **CERTIFIED** | 12 | 17 | 200 | $1827.15$ | 0.61 |
| `anchor-l3-mu3/2-R2` | Einstein anchor | $[0.0601,\,12)$ | **CERTIFIED** | 18 | 28 | 200 | $3330.57$ | 1.00 |
| `anchor-l10-mu4-R3` | Einstein anchor | $[0.447,\,40)$ | **CERTIFIED** | 10 | 15 | 200 | $477249$ | 0.55 |
| `anchor-l20-mu19/2-R5` | Einstein anchor | $[0.827,\,80)$ | **CERTIFIED** | 17 | 29 | 200 | $106310$ | 1.01 |

REFUSED instances: **none**. Default run (final bytes) exit code 0, wall time 434.34 s; the table's boxes, tries and margins are identical across the two full runs (459 s and 434 s).

The known difficulty — the hot-margin failure of the reviewed file near $q_{hi} = 0.525$ on `subhalf-25p6-0p4786` (the near-onset region where $\lambda_{\min}$ of the folded form changes sign) — is resolved **soundly** by finer boxes, not by weakening: the cover of $[0.525, 102.4)$ succeeds in 2843 boxes with every box carrying a strictly positive exact integer margin, the smallest being $0.0697854$, and the cost is 249.99 s (2843 boxes for that single instance, concentrated in the bisection of the near-onset region); `cover` never buys speed by weakening — an exhausted depth budget raises instead of accepting (`independent.py:385-392`). No instance needed the escape hatch of an exact-rational endpoint with a monotonicity argument, so none is refused on that ground.

---

## 3. Adversarial probes (`--adversarial`, exit 0)

| probe | box tested | exact folded form at $q_{\mathrm{bad}}$ | sound device |
|---|---|---:|---|
| $(\lambda,\mu^*,R^2) = (10,15,9)$ (REVIEW.md adversarial probe 1) | $[0.033058,\,0.037457)$ and the point box at $q_{\mathrm{bad}}$ | $-8.41646\times10^{12} < 0$ | **REFUSED** (both boxes) |
| $(\lambda,\mu^*,R^2) = (12,12,9)$ (REVIEW.md adversarial probe 2) | $[0.081633,\,0.099707)$ and the point box | $-2.89796\times10^{12} < 0$ | **REFUSED** (both boxes) |
| $(\lambda,\mu^*,R^2) = (26,312/25,53/5)$ (the package's own $\mu^*>0$ instance at $q=0.495$) | $[0.49,\,0.505)$ and the point box | $-7.70777\times10^{9} < 0$ | **REFUSED** (both boxes) |

The negativity is exhibited by an **exact integer witness** on an $N=480$ folded block (`folded_exact`, `independent.py:583-622`, `:623-634`), recomputed from exact integer correlations, so no sound certificate can cover a box through $q_{\mathrm{bad}}$ — which is why the two `REVIEW.md` probes must be refused and are.

---

## 4. Mutants (all refused, all exit 1)

| mutant | what it reintroduces | refusal evidence |
|---|---|---|
| `--mutant entrywise` | the F1 entrywise off-diagonal lower bound | on the probe box every entry satisfies $A_{ij} \le SC\,F_{ij}$, yet the exact folded witness $x$ (mixed sign, support $0..199$) gives $x^{\mathsf T}Ax = +565.9\times10^{12}$ while $x^{\mathsf T}SC\,F(q_{\mathrm{bad}})x = -85.47\times10^{12}$; the sound enclosure gives $-31.55\times10^{12}$ and refuses (`:833-871`) |
| `--mutant v1pen` | the F2 scalar-gap tail penalty | exact shortfall $2.207\times$ of the boundary Schur term $B_{m,m-1}^2/g_m = 0.619931$ at $q = 0.49$ versus the claimed $0.280929$ (`m = 200`), with $g_m$ bounded **above** from exact rationals (`:872-893`) |
| `--mutant rsign` | a radius sign flip ($F - \text{centre} \ge +\operatorname{diag}(\rho)$) | at $q = hi$ the entry $(198,199)$ deviates by $0.0291817$ from the centre, so the flipped claim needs $-2\,dev \ge 0.362224$ but $-2\,dev = -0.0583634$ (`:894-911`) |
| `--mutant overflow` | the dropped `int64` overflow guard in `head_radius` | the unguarded row sum wraps to $0$ while the exact row sum is $18446744073709551616 = 2^{64} \ge 2^{63}$, so $\rho$ stops dominating; the guarded path raises for the same input (`:912-935`) |
| `--mutant endpoint` | Einstein bracket taken below $q_{hi}$ | `hot interval cannot be certified: [0.495, 0.495000006785)` |
| `--mutant coulomb` | doubled $\mu^*$ in the cold gate | `doubling mu* removes cold instability at q=13/25 (val=2.16586e+14 >= 0)` |
| `--mutant spectrum` | $p \mapsto 1-p$ mirrored two-line spectrum | rejected by the second-moment guard $p_1u_1+p_2u_2 = 1$ |
| `--mutant receipt` | a $C_E$ bracket shaved inward by $10^{-6}$ | `subhalf-26-12over25: stored C_E bracket does not contain 30-digit Hutton bracket` (control first: the unshaved stored brackets pass) |

---

## 5. Claims that must shrink

**None.** Every one of the 8 instances is certified, so `RESULT.md:23` ("`verified by replay.py and independent.py`") stands as written for the four counterexamples and the four anchors, and `RESULT.md:85` can keep describing `independent.py` as a secondary verifier.

Two notes for whoever next edits `RESULT.md` / `bounds.json` (not changes made here, and neither is a shrink):

1. `RESULT.md:85` describes the hot side as "an independent hot-side enclosure"; after this repair it is specifically a PSD-dominated Schur enclosure with exact integer acceptance, plus the two new modes. A sharper sentence is available if wanted.
2. `bounds.json[*]["boxes"]` still holds the v1 split counts ($2638, 1444, 539, \dots$); the v2 cover visits $2843, 1504, 541, 239, \dots$. `check_receipt` only requires the stored count to be a positive integer, so nothing fails, but the stored counts are stale with respect to the current checker and should either be refreshed or labelled as v1 counts.

---

## 6. Commands and exit codes

All rows rerun after the final edit; working directory `D:/dev/scratch/ceiling-20261118/C-LAMBDA-MU/MUSTAR-HALF`, runner prefix
`RUN="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 UV_CACHE_DIR=D:/dev/.cache/uv uv run --no-project --with numpy --with scipy python -B"`.

| command | exit | note |
|---|---:|---|
| `$RUN independent.py` | **0** | 434 s; 8/8 CERTIFIED, `bounds.json` receipt verified against the unfolded form and 30-digit Hutton brackets |
| `$RUN independent.py --selfcheck` | **0** | 10.9 s; 6 windows × 3 interior $q$ × 720000 exact rational entry comparisons, 18 exact quadratic-form comparisons $A \le F$, tail gaps and Schur shift exact |
| `$RUN independent.py --adversarial` | **0** | 7.9 s; all three exactly-negative probes refused (boxes and point boxes) |
| `$RUN independent.py --mutant entrywise` | **1** | 0.7-2.0 s; refusal message quoted in §4 |
| `$RUN independent.py --mutant v1pen` | **1** | idem |
| `$RUN independent.py --mutant rsign` | **1** | idem |
| `$RUN independent.py --mutant overflow` | **1** | idem |
| `$RUN independent.py --mutant endpoint` | **1** | idem |
| `$RUN independent.py --mutant coulomb` | **1** | idem |
| `$RUN independent.py --mutant spectrum` | **1** | idem |
| `$RUN independent.py --mutant receipt` | **1** | idem |

`replay.py`, `structure.py` and `phase_scan.py` rows are unchanged and listed in `CHECKS.txt`; they were not rerun in this slice except for `replay.py` in an earlier pass of the same session.

---

## 7. `REVIEW3.md` (PASS) non-blocking notes N1-N4 — applied

Backups taken first: `independent.v3-preN.py` (sha256 `7abdb918abf81a214630051338050f964830665600bce02e70c8a7cb9014adb1`) and `RESULT.v2.md` (sha256 `0c4fd77681008b2bc7a5d41c5522e8599124094b7245094ddfbe7758c3937a8c`). No `REVIEW*.md` file was touched.

| note | change | `file:line` |
|---|---|---|
| **N1** [P2] | The `--selfcheck` integer-vector comparison is now **same-unit and Coulomb-complete**: `need(F(cert) <= true + F(SC) * 2 * mu * sum(xi[:k]) ** 2, ...)`. Previously `F(cert, SC) <= true` divided only the left side by `SC = 2**22` and dropped the $q$-independent block $+2\mu^*\mathbf{1}_k\mathbf{1}_k^T$, weakening the diagnostic by a factor $SC$; the exact block is now added back in `SC` units. | `independent.py:803-808` |
| **N2** [P2] | `tail_penalty` fails closed on both far-column preconditions: `need(lam <= 2 * lo * ncol * ncol, 'far-tail closure: a_NCOL(lo) may exceed 2, so gaps are not monotone')` makes explicit the monotonicity that licenses the single denominator `g.min()` for $j \ge m+\text{NCOL}$ (since $\text{gap}_j-\text{gap}_{j-1} \ge 2 - a_{\text{NCOL}}(lo)$), and `need(0 <= far < 2 ** 62, 'far-tail penalty overflow')` guards the far term before it is added. Both hold with huge margin ($\max \lambda/(lo\,\text{NCOL}^2) = 1.18\times10^{-3}$ against the ceiling 2; `far` $\le 1.6\times10^{9}$ against $2^{62}$). | `independent.py:222-226`, `:234-235` |
| **N3** [P3] | `print_table` header now reads `margin = exact Gershgorin lower bound on lambda_min of the certified head matrix, in SC units = 2**22 x folded-form units`, matching `positive()`'s docstring (the returned value is `gap.min()/factor`). | `independent.py:558-560` |
| **N4** [P3] | `RESULT.md:85-86` now lists all eight mutants (`entrywise,v1pen,rsign,overflow,endpoint,coulomb,spectrum,receipt`) and records `--selfcheck` / `--adversarial` exit 0. | `RESULT.md:85-86` |

Effect on the certificate: **none** — pure hardening (N1 tightens a diagnostic, N2 adds fail-closed guards that hold by a wide margin, N3/N4 are text).

Rerun after N1-N4 (final bytes, sha256 below):

| command | exit | result |
|---|---:|---|
| `$RUN independent.py` | **0** | 389 s; 8/8 CERTIFIED with **identical** boxes (2843/1504/541/239, 12/18/10/17), tries (5680/3002/1076/472, 17/28/15/29) and margins (0.0697854, 0.244918, 0.504196, 45.2602; 1827.15, 3330.57, 477249, 106310); `bounds.json` verified |
| `$RUN independent.py --selfcheck` | **0** | 12.1 s; 720000 entry comparisons + 18 now same-unit quadratic-form comparisons + 8 tail rows |
| `$RUN independent.py --adversarial` | **0** | 7.4 s; all three probes refused |
| `$RUN independent.py --mutant entrywise` | **1** | 2.4 s |
| `$RUN independent.py --mutant v1pen` | **1** | 1.5 s |
| `$RUN independent.py --mutant rsign` | **1** | 0.6 s |
| `$RUN independent.py --mutant overflow` | **1** | 0.6 s |
| `$RUN independent.py --mutant endpoint` | **1** | 1.3 s |
| `$RUN independent.py --mutant coulomb` | **1** | 1.0 s |
| `$RUN independent.py --mutant spectrum` | **1** | 0.5 s |
| `$RUN independent.py --mutant receipt` | **1** | 0.7 s |

### SHA256 of the artifacts

| file | sha256 |
|---|---|
| `independent.py` (after N1-N4, verified by the run above) | `26e1379c17f66e54626e7b481688a7134529c68525c9aa52584c615a5553110d` |
| `independent.v3-preN.py` (before N1-N4) | `7abdb918abf81a214630051338050f964830665600bce02e70c8a7cb9014adb1` |
| `independent.v2-preR3.py` (R3 checkpoint) | `dc25482537ccd3e27cbbb543d363e134e1f5aa58ec090aa1235e2a2dbfc36538` |
| `independent.v1-rejected.py` (review-era unsound device) | `3365b76b0887d9da47d35e1985ee25234e3e4de5c84ef50c8651ccffae8a44e0` |
| `RESULT.md` (after N4) | `ddec869dca4088537a004f13083454af1a8337bcb7dd6a2ced06c9cae2b4188d` |
| `RESULT.v2.md` (backup of `RESULT.md` before N4) | `0c4fd77681008b2bc7a5d41c5522e8599124094b7245094ddfbe7758c3937a8c` |
| `replay.py` | `d7f83656e0c6e47664519e4d1bb6acc6602473391dfc1c7d6b3642b08f58bbc4` |
| `bounds.json` | `dfccb6776db72fc4c21443007a88a7b10f3fd7d0c281f14543f47f6959b8009c` |
| `fixtures.json` | `bf1d6ca29dcf640ef99782d01ea34a9e5192b678e4b43610dc457acecad891ee` |
| `RIGOR.md` | `cbf06f9c700be1af748c70ccb062bcf5a75789e9b744a54ba5b9f507a6a19989` |
| `structure.py` | `6d3b2dae169a936fadd7598ec90884ef781ee88bf93a3d17fdd365c002c31eae` |
| `phase_scan.py` | `2c07a5837cab74b5eaf0ab86015e536b3ca04f29b553884d9177a87258a0ebaf` |

Note on §5 item 2 above: `REVIEW3.md` §2(e) establishes that the `bounds.json` box counts are **not** stale — they are `replay.py`'s exact counts, enforced by equality there, while `independent.py` uses a different head size ($m=200$ vs 240) and tail penalty and visits `2843/1504/541/239`. That note is therefore withdrawn; no change to `bounds.json` is needed.
