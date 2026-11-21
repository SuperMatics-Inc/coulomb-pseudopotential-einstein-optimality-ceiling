# Independent Re-Review of `mustar-half` (`REVIEW3.md`)

**Overall Verdict: PASS** (all 9 prior findings **F1–F9** from `REVIEW.md` are resolved; zero P0 or P1 findings remain; four non-blocking P2/P3 hardening/polish items noted below).

**Summary.** The rebuilt `independent.py` replaces the rejected v1 hot verifier with a mathematically sound, exact-integer signed-interval enclosure (`SC = 2^22`), weighted Gershgorin radius shift (`head_radius`), per-row infinite-tail Gershgorin gap (`tail_gaps`), and weighted Cauchy–Schwarz column penalty (`tail_penalty`) with fail-closed `int64` overflow guards and exact Gram-residual diagonal dominance (`positive`). It is genuinely independent of `replay.py` (no shared code path; unfolded full-line cold form vs. folded; Cauchy–Schwarz per-row tail penalty vs. Schur-complement matrix; Hutton vs. Machin $\pi$). Re-running `independent.py` (398.0 s), `--selfcheck`, `--adversarial`, and all 8 `--mutant` modes reproduces every claimed exit code and certificate metric (`8/8 CERTIFIED`, min margin `0.0697854` in `SC` units for `subhalf-25p6-0p4786`). Together with `replay.py` (audited sound in `REVIEW.md`) and the repaired `RIGOR.md`, `RESULT.md`, and `structure.py` (`FIX.md`), all four sub-$1/2$ counterexamples and four Einstein anchors earn **CERTIFIED**, and Lemma 1 + Theorems 1–5 earn **PROVED**.

---

## 1. Final Claim Labels

| Claim | Allowed Label | Basis |
|---|---|---|
| Four sub-$1/2$ counterexamples (`subhalf-25p6-0p4786`, `subhalf-26-12over25`, `subhalf-27-0p4848`, `subhalf-28-0p489`) and four Einstein anchors (`bounds.json`) | **CERTIFIED** | Both `replay.py` and rebuilt `independent.py` are mathematically sound, genuinely independent, agree on all 8 brackets/spectra, pass all adversarial probes, and refuse all 13 mutants (5 `replay.py` + 8 `independent.py`). |
| Lemma 1 (Exact Finite-Support Decomposition) & Theorems 1–5 (`RIGOR.md:31-128`, `RESULT.md:13-18`) | **PROVED** | Audited line by line after `FIX.md` repairs (F4–F7 fixed): Lemma 1 display (2) exact; Theorem 1 restricted to form core $\mathcal{D}_0$; Theorem 2 strict $4R^2 < q_E(\lambda, 0)$ (conditional on zero-Coulomb theorem in `C-LAMBDA/RIGOR.md`); Theorem 3 $\lambda \ge 4R^2 + 1$; Theorem 4 exact $k=1$ cone condition $\mu^* \le 1 + a_1(q;p)$ (unconditional for $\mu^* \le 1$ and $\lambda \le 2$ at $\mu^*/\lambda \le 1/2$); Theorem 5 $q \ge 4\lambda$. `structure.py` + all 4 mutant flags pass. |
| Phase diagram $r_*(\lambda, R)$, $r_{\min} \approx 0.4785$, $\lambda_{\mathrm{crit}} \approx 25.55$, $k \in \{1,2,3,4\}$ optimality for $\lambda > 2$, $k=1$ failure at $\lambda \ge 152$, and $N=600$ true $T_{\mathrm{mix}}/T_E$ ratios | **NUMERICAL** | Floating-point scans (`phase_scan.py`) and independent $N=600$ recomputation (`REVIEW.md` §5). |

---

## 2. Independent Verification of Audit Items (a)–(e)

### (a) Hot enclosure soundness (`hot_enclosure`, `head_radius`, `positive`, `windows`)
- **Constant-mask windowing (`independent.py:94-104, 423-429`):** `cutoff(q, scale2)` computes $k = \#\{i \ge 0 : (2i+1)^2 q < 4 R^2\}$ in exact integer arithmetic. `windows(lo, hi, scale2)` partitions $[q_{\mathrm{hi}}, 4\lambda)$ at exact jump points $4 R^2 / (2k-1)^2$, so $k(q, R)$ is strictly constant on every half-open window $[\text{lo}, \text{hi})$.
- **Head/tail coverage (`independent.py:271`):** Head modes are $0 \dots m-1$ with $m = \max(200, 2k+1) > k$, so every Coulomb-masked index lies strictly inside the head block and the infinite tail starts at $j = m$ with zero omitted modes.
- **Endpoint bracketing (`independent.py:272-296`):** Since $a_j(q)$ is strictly decreasing in $q$, `lower = -(up[diff] + up[hank])` and `upper = -(dn[diff] + dn[hank])` bracket $\text{SC}\cdot F_{0,ij}(q)$ for all $q \in [\text{lo}, \text{hi}]$ and $i \neq j$. `center = (lower + upper) // 2` and `radius = max(upper - center, center - lower)` satisfy $|\text{SC}\cdot F_{0,ij}(q) - \text{center}_{ij}| \le \text{radius}_{ij}$ (including odd bracket widths). The diagonal is bounded one-sidedly from below via `SC*(2*i+1) + 2*cum(dn) - up[2*i+1]`. The Coulomb rank-1 block adds `flr_(SC * 2 * mu)` to `center[:k, :k]`; since $\delta = \text{SC}\cdot 2\mu^* - \lfloor \text{SC}\cdot 2\mu^* \rfloor \ge 0$, the omitted piece $\delta \mathbf{1}_k \mathbf{1}_k^T \succeq 0$ is PSD for all real vectors $x$ (mixed-sign included).
- **`head_radius` (`independent.py:234-254`):** With $h_i = \lfloor 2^{22}/(i+1) \rfloor > 0$ and symmetric $R \ge 0$, AM–GM gives $\sum_{i \neq j} R_{ij}|x_i||x_j| \le \sum_i (\frac{1}{h_i}\sum_j R_{ij} h_j) x_i^2 \le \sum_i \rho_i x_i^2$ for **every** real vector $x$ (resolving REVIEW2 R2-1 / `REVIEW.md` F1).
- **Exact one-sided Gershgorin (`independent.py:326-403`):** `positive(A)` requires exact symmetric `int64` $A$, forms $R = A\cdot\text{factor} - L_h L_h^T$ with $\text{factor} = G^2/\text{SC}$ in exact `int64`, and accepts iff $\text{gap}_i = 2 R_{ii} - \sum_j |R_{ij}| > 0$ for all $i$. Since $\text{gap}_i > 0 \implies R_{ii} > 0$, this implies $R_{ii} - \sum_{j \neq i} |R_{ij}| \ge \min_i \text{gap}_i > 0$, hence $A = \text{factor}^{-1}(L_h L_h^T + R) \succeq (\min_i \text{gap}_i / \text{factor}) I \succ 0$.

### (b) Tail gap $g_m$ (`tail_gaps`) and Cauchy–Schwarz column penalty (`tail_penalty`)
- **Per-row tail gap (`independent.py:133-189`):** For $j \ge m > k$, row $j$ of $F_{QQ}(q)$ has no Coulomb term, diagonal $(2j+1) + 2A_j - a_{2j+1}$, and absolute off-diagonal row sum $\le A_{j-m} + S_1 + S_{j+m+1}$. Using $S_1(q) \le \frac{\pi^2}{6}\frac{\lambda}{\text{lo}} < \frac{5}{3}\frac{\lambda}{\text{lo}}$ and $S_{j+m+1}(q) \le \frac{\lambda}{\text{lo}(j+m)}$, every $g_j$ ($j = m \dots m+\text{NCOL}-1$) is a verified lower bound on $\text{SC}\cdot\text{gap}_j(q)$.
- **Cauchy–Schwarz column penalty (`independent.py:192-231`):** Completing the square on $y^T F_{QQ} y + 2 x^T F_{PQ} y$ gives $-\sum_{j \ge m} \frac{\text{SC}}{g_j}(\sum_i b_{ij}|x_i|)^2$, and Cauchy–Schwarz with $h_i = \lfloor 2^{22}/(i+1) \rfloor$ gives $-\sum_i x_i^2 \frac{1}{h_i}\sum_{j \ge m} \frac{\text{be}_{ij}\text{col}_j}{g_j}$ in exact `SC` units (the $\text{SC}^2$ factors cancel identically). Boundary row $j = m$ keeps its true gap $g_m = 2m + O(1)$ and true coupling $a_1 + a_{2m}$ (resolving REVIEW2 R2-2 / `REVIEW.md` F2). Far columns $j \ge m+\text{NCOL}$ are closed via $\sum_{t=\text{NCOL}+1}^\infty t^{-4} \le \frac{1}{3\,\text{NCOL}^3}$ with denominator $g_{\min}$. As checked in Finding **N2**, `gap_j` is guaranteed $\ge g_{\min}/\text{SC}$ for all $j \ge m + \text{NCOL}$ whenever $a_{\text{NCOL}}(\text{lo}) \le 2$; across all 8 instances $\lambda/(\text{lo}\cdot\text{NCOL}^2) \in [3.88\times 10^{-4}, 1.18\times 10^{-3}] \ll 2$ ($>1{,}690\times$ margin).

### (c) Overflow guards (fail closed, never clamp)
- Every `int64` contraction in `head_radius`, `tail_penalty`, `hot_enclosure`, `hot_head`, and `positive` is guarded against `int64` wraparound and raises `ValueError` or returns `None` (never clamps).
- In `positive(A)` (`independent.py:372-399`), $|A|\cdot\text{factor} < 2^{61}$, $|L_h| < 2^{31}$, $\max_i \|L_{h,i}\|_2^2 (1+10^{-9}) < 2^{60}$, so $|A\cdot\text{factor} - L_h L_h^T| < 3\cdot 2^{60} < 2^{62}$ — eliminating the `REVIEW.md` F9 subtraction overflow window. `|res| < 2^61 // n` guarantees `2*res.diagonal() - np.abs(res).sum(axis=1)` cannot overflow.

### (d) Independence from `replay.py`
- No imports or shared code path between `independent.py` and `replay.py`.
- Cold side: unfolded full-line $\{-240, \dots, 239\}$ exact `Fraction` form vs. `replay.py`'s folded half-line integer form.
- Hot side: `SC = 2^22`, $m = 200$, weighted-Gershgorin `head_radius`, per-row infinite-tail Gershgorin + Cauchy–Schwarz `tail_penalty`, 3 Gram scales with Newton refinement vs. `replay.py`'s `S = 2^30`, $n = 240$, unweighted radius, explicit Schur-complement near-tail block + `far_lump`, single Gram scale `G = 2^26`.
- $\pi$ bounds: Hutton's formula (90 terms) vs. Machin's formula.

### (e) `RESULT.md:23,85` claims and `bounds.json` box counts
- `RESULT.md:23` ("verified by `replay.py` and `independent.py`; $C_E$ brackets outward-rounded to 8 decimal places from `bounds.json`") **now holds**.
- `RESULT.md:85` holds (with minor P3 note **N4** that it only enumerates 4 of the 8 mutants).
- **`bounds.json` box counts (`2638, 1444, 539, 239, 12, 18, 10, 17`) are NOT stale and do not affect soundness:** they are `replay.py`'s exact box counts (enforced by `replay.py`'s exact equality check against `bounds.json`). `independent.py` uses a different head size ($m=200$ vs. $240$) and tail penalty, producing `2843, 1504, 541, 239, 12, 18, 10, 17` boxes over the exact same intervals $[q_{\mathrm{hi}}, 4\lambda)$; `independent.py:570` appropriately checks all mathematical receipt fields (`einstein_q`, `einstein_C` containment, `handoff_q`, `mix.spectrum`, `mix.q`) while only validating that `ref['boxes']` is a positive integer.

---

## 3. Findings (P0–P3)

Zero **P0** or **P1** findings. Four non-blocking **P2/P3** items:

1. **N1 [P2] (`independent.py:699-701`) — Unit mismatch and omitted Coulomb term in `--selfcheck` quadratic-form comparison:**
   In `selfcheck()`, `v = exact_head(lam, q, scale2, spec, m)` returns entries already scaled by `SC = 2^22` and omits the Coulomb block $+2\mu^* \mathbf{1}_k \mathbf{1}_k^T$, while `A` from `hot_head` is also scaled by `SC` and includes $\lfloor \text{SC}\cdot 2\mu^* \rfloor \mathbf{1}_k \mathbf{1}_k^T$. Line 701 then checks `F(cert, SC) <= true`, dividing the LHS by `SC = 4,194,304` while leaving the RHS in `SC` units (and missing the Coulomb term). This weakens the `--selfcheck` diagnostic assertion by a factor of `SC` (e.g., on window 0: `F(cert, SC) = 1.1925e+10` vs. `true = 5.0056e+16`). Independent check confirmed the true same-unit inequality `F(cert) <= true + F(SC) * 2 * mu * (sum(xi[:k]))**2` holds (`5.0019e+16 <= 5.0072e+16`), so the certifying path is unaffected. *Fix:* compare `F(cert) <= true + F(SC) * 2 * mu * (sum(xi[:k]) ** 2)`.

2. **N2 [P2] (`independent.py:181-189, 228-230`) — Missing explicit monotonicity guard for far-tail denominator `g.min()` and `far` overflow pre-check:**
   `tail_penalty` closes columns $j \ge m + \text{NCOL}$ using `int(g.min())` (computed only over $j \in [m, m + \text{NCOL} - 1]$). For $j \ge m + \text{NCOL}$, $\text{gap}_j - \text{gap}_{j-1} = 2 + 2a_j + a_{j+m} - a_{j-m} \ge 2 - a_{\text{NCOL}}(\text{lo})$, so $\text{gap}_j \ge g_{\min}/\text{SC}$ is guaranteed whenever $a_{\text{NCOL}}(\text{lo}) \le 2$ (sufficiently, $\lambda \le 2\,\text{lo}\cdot\text{NCOL}^2$). This holds with $>1{,}690\times$ margin on all 8 `fixtures.json` instances ($\max \lambda/(\text{lo}\cdot\text{NCOL}^2) = 1.18\times 10^{-3}$), so all 8 certificates are sound, but an explicit `need(lam <= 2 * lo * ncol * ncol, ...)` and `need(far < 2 ** 62, ...)` before `per = per + far` would make `tail_penalty` unconditionally fail-closed for arbitrary caller parameters.

3. **N3 [P3] (`independent.py:555`) — Margin unit label in `print_table`:**
   `print_table` prints `"margin = exact Gershgorin lower bound on lambda_min of the certified head matrix, in units of the folded form"`, whereas `positive()` (`independent.py:333, 400`) returns `float(gap.min()) / factor`, which is in **`SC` units** (`2^22` times folded-form units; e.g., `0.0697854` in `SC` units = `1.664e-8` in folded-form units, still strictly positive since `gap.min() >= 1`). Update the header text to `"in SC units"` (matching `positive()`'s docstring).

4. **N4 [P3] (`RESULT.md:85`) — Incomplete mutant list in `RESULT.md`:**
   `RESULT.md:85` still lists only `--mutant {endpoint,coulomb,spectrum,receipt}` rather than all 8 mutants (`entrywise,v1pen,rsign,overflow` + `--selfcheck` + `--adversarial`).

---

## 4. Rerun Table and Extra Adversarial Checks

Runner prefix (working directory `records/mustar-half`):
```bash
RUN="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --no-project --with numpy --with scipy python -B"
```

| Command | Expected Exit | Observed Exit | Key Output / Wall Time |
|---|---:|---:|---|
| `$RUN independent.py` | 0 | **0** | 398.0 s; `8/8 CERTIFIED`, boxes `2843/1504/541/239` & `12/18/10/17`, head `m=200`, min margins `0.0697854, 0.244918, 0.504196, 45.2602` & `1827.15, 3330.57, 477249, 106310`; `bounds.json` verified |
| `$RUN independent.py --selfcheck` | 0 | **0** | 6 windows x 3 $q$, 720,000 exact entry comparisons, 18 form comparisons, 8 tail rows x 3 $q$: OK |
| `$RUN independent.py --adversarial` | 0 | **0** | All 3 negative probes (`l10_m15_R9`, `l12_m12_R9`, `mustar26`) refused on documented boxes and point boxes |
| `$RUN independent.py --mutant entrywise` | 1 | **1** | `REFUSED`: F1 entrywise off-diagonal bound refuted (`x^T A x = 565.9e12 > 0`, true `-85.47e12 < 0`, sound `-31.55e12 < 0`) |
| `$RUN independent.py --mutant v1pen` | 1 | **1** | `REFUSED`: F2 v1 tail penalty `2.207x` short of boundary Schur term (`0.619931` vs `0.280929`) |
| `$RUN independent.py --mutant rsign` | 1 | **1** | `REFUSED`: radius sign flip fails at `q=99/200` |
| `$RUN independent.py --mutant overflow` | 1 | **1** | `REFUSED`: dropped overflow guard wraps `2^64` row sum to `0`; guarded path raises `ValueError` |
| `$RUN independent.py --mutant endpoint` | 1 | **1** | `REFUSED`: hot interval `[0.495, 0.495000006785)` cannot be certified |
| `$RUN independent.py --mutant coulomb` | 1 | **1** | `REFUSED`: doubling $\mu^*$ removes cold instability at `q=13/25` (`val=2.16586e+14 >= 0`) |
| `$RUN independent.py --mutant spectrum` | 1 | **1** | `REFUSED`: `p -> 1-p` rejected by second-moment guard |
| `$RUN independent.py --mutant receipt` | 1 | **1** | `REFUSED`: shaved `C_E` bracket rejected (`subhalf-26-12over25`) |
| `$RUN structure.py` | 0 | **0** | 40 random rational trials + F4 refutation witnesses passed |
| `$RUN structure.py --mutant` (and `f4`, `coulomb`, `norm`) | 1 | **1** | All 4 commands exited 1 (`REFUSED`) |

**Additional independent adversarial probes (in `<temporary>/`, deleted after run):**
1. Perturbed `subhalf-26-12over25` mixture past the $k = 5 \to 4$ jump ($q = 53/100 = 0.53 > 4 R^2 / 81 = 0.523457$): `cold_value` returned $+2.7069\times 10^{15} > 0$ ($\text{ray} = 0.779930 < 1$) $\to$ **refused**.
2. Unstable Einstein point just below $q_E$ for `subhalf-25p6-0p4786` ($q = 0.522$, exact folded value $-1.3007\times 10^9 < 0$, $\lambda_{\min} = -6.7\times 10^{-5}$): `positive(hot_head(..., 0.5219, 0.5221))` returned `None` $\to$ **refused**.
