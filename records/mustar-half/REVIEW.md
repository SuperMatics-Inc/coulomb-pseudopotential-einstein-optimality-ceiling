# Independent Review of `MUSTAR-HALF` (`REVIEW.md`)

**Overall Verdict: REJECT** (for `CERTIFIED` and `PROVED` status).

**Executive Summary.** The central mathematical discovery is **genuine and verified**: in the sharp common-cutoff linearized Migdal-Eliashberg model (identical conventions to `COMMON-CUTOFF`), all four rational two-line spectra in `fixtures.json` / `bounds.json` are genuine sub-$1/2$ counterexamples ($\mu^*/\lambda \in \{0.478602, 0.48, 0.484815, 0.489\}$ at $\lambda \in [25.6, 28]$), independently confirmed on both folded and unfolded full-line eigenproblems with 7-digit truncation stability ($N = 300$ vs $600$), and **`replay.py` is mathematically and numerically sound** on both cold and hot sides. However, the package **cannot** currently carry `CERTIFIED` or `PROVED` labels due to **four P0 defects**:
1. **`independent.py` hot verifier inherits two P0 soundness bugs from `COMMON-CUTOFF` `REVIEW2.md` (R2-1 and R2-2):** its entrywise off-diagonal lower bound is invalid on mixed-sign vectors at $\mu^* > 0$ (producing two reproducible false-positive certificates on provably unstable boxes), and its boundary tail penalty `pen` underestimates the single $j=m, i=m-1$ Schur-complement diagonal term by $19.85\times$ at $(\lambda, q_{\mathrm{lo}}, m) = (26, 10, 200)$.
2. **`RIGOR.md` §4.2 lists four completely different, stale two-line spectra** ($u_2 \in [1.55, 2.27]$) that contradict `fixtures.json`/`bounds.json`/`RESULT.md`, are **all strictly stable** ($\lambda_{\min} \in [+0.116, +0.294] > 0$, not counterexamples), and one of which violates $\int u\,dp = 1$ ($59525/59644 \neq 1$).
3. **`RIGOR.md` Theorem 3 (`RESULT.md` Theorem 2, $k=1$ for $\mu^*/\lambda \le 1/2$) has a broken proof and a false intermediate theorem claim:** it asserts $h_0^* \ge h_1^* > \dots > 0$ for all $\lambda > 0$ at $\mu^*/\lambda \le 1/2$ using the false inequality $1 + \lambda - a_1 < 3 + a_1$. Explicitly refuted at $\lambda = 20, \mu^* = 10$ ($h_0^* = 0.5695 < h_1^* = 0.6094$, $\tilde{D}_1 - \tilde{D}_0 = -4.036 < 0$) and $\lambda = 50, \mu^* = 25$ ($h_0^* = 0.4115 < h_1^* = 0.6019$).
4. **`RESULT.md` claims `PROVED (pending review)` for Theorems 3 and 4 (small-$\mu^*$ spectral gap stability and large-$\lambda$ fixed-$R$ optimality) that do not exist anywhere in `RIGOR.md`**, while `RIGOR.md` Theorem 2 ($k=0$ optimality) is false at exact equality $4R^2 = q_E(\lambda, 0)$ for any $\mu^* > 0$.

---

## 1. Per-Claim Verdict and Allowed Label

| Claim | Author Label | Review Verdict | Allowed Label | Rationale |
|---|---|---|---|---|
| 4 sub-$1/2$ counterexamples (`fixtures.json`, `bounds.json`) | `CERTIFIED` | **FAILS `CERTIFIED`** (core claim true) | `SINGLE-CHECKER CERTIFIED (replay.py only)` / `VERIFIED NUMERICALLY` | `replay.py` is sound and passes; independent recomputation confirms all 4 counterexamples. Fails `CERTIFIED` because `independent.py` hot verifier is unsound (**F1, F2**). |
| 4 Einstein anchors (`fixtures.json`, `bounds.json`) | `CERTIFIED` | **FAILS `CERTIFIED`** | `SINGLE-CHECKER CERTIFIED (replay.py only)` | Same `independent.py` hot-side unsoundness (**F1, F2**); also 5/8 `RESULT.md` $C_E$ decimal entries are inward-rounded/stale (**F8**). |
| `RIGOR.md` Lemma 1 (Finite-support decomposition) | `PROVED (pending review)` | **NEEDS CLEANUP** | `VERIFIED (formula 2' only)` | Formula `(2')` is algebraically exact, but display `(2)` is wrong ($2\times$ error) and draft scratch text (`?? Wait:`) remains in the proof (**F7**). |
| `RIGOR.md` Theorem 1 (Two-delta LP reduction) | `PROVED (pending review)` | **MINOR GAP** | `SKETCHED (fixable)` | Conclusion is true, but proof claims $\Phi_{h,q}(u)$ is bounded on $(0,\infty)$ for all $h \in \mathcal{D}(\mathcal{F})$ using $\frac{u}{u+qj^2} \le \frac{u}{qj^2}$ (grows linearly in $u$). Fix: restrict to finitely supported core (**F6**). |
| `RIGOR.md` Theorem 2 / `RESULT.md` Theorem 1 ($k=0$ mask) | `PROVED (pending review)` | **FALSE AT BOUNDARY** | `PROVED FOR STRICT 4R^2 < q_E(lambda, 0)` | Fails at exact equality $4R^2 = q_E(\lambda, 0)$ for any $\mu^* > 0$, where $k(q,R) \ge 1$ on $q < q_E(\lambda,0)$ pushes $q_{\mathrm{lin}}(\delta_1) < q_E(\lambda, 0)$ (**F5**). |
| `RIGOR.md` Theorem 3 / `RESULT.md` Theorem 2 ($k=1$, $\mu^*/\lambda \le 1/2$) | `PROVED (pending review)` | **PROOF BROKEN / MONOTONICITY FALSE** | `CONJECTURED / NUMERICAL` (proved only for $2\mu^* \le 2 + 2a_1$) | Claimed $h_0^* \ge h_1^*$ and inequality $1+\lambda-a_1 < 3+a_1$ are explicitly false for $\lambda \ge 20$ (**F4**). |
| `RESULT.md` Theorem 3 (small-$\mu^*$ spectral gap stability) | `PROVED (pending review)` | **MISSING** | `UNPROVED` | No statement or proof exists in `RIGOR.md` (**F5**). |
| `RESULT.md` Theorem 4 (large-$\lambda$ fixed-$R$ optimality) | `PROVED (pending review)` | **MISSING** | `UNPROVED` | No statement or proof exists in `RIGOR.md` (**F5**). |
| `RIGOR.md` Theorem 4 ($q \ge 4\lambda$ asymptotic stability) | `PROVED (pending review)` | **PASS** (minor phrasing slip) | `PROVED` | Line-by-line sound; trivial `- \sum (missing)` phrasing slip on `RIGOR.md:100` (**F7**). |
| Phase diagram $r_*(\lambda, R)$, $r_{\min} \approx 0.4785$, $k \in \{1..4\}$ scan | `NUMERICAL` | **PASS** | `NUMERICAL` | Consistent with independent checks and `phase_scan.py` (exit 0). |

---

## 2. Certificate Soundness Audit (`replay.py` vs `independent.py`)

### 2.1 `replay.py` — **SOUND** (Cold and Hot Sides)
Line-by-line audit of `replay.py`:
- **Cutoff & windows (`replay.py:49-60`):** `cutoff(q, scale2)` computes `(isqrt(up(F(4*scale2)/q) - 1) + 1) // 2`, which is exact for all rational $q, R^2 > 0$ including $k = 0$ (when $4R^2 \le q$). `windows(lo, hi, scale2)` partitions `[lo, hi)` at exact mask-jump points $4R^2/(2k-1)^2$ so $k$ is constant on every half-open subinterval.
- **Hot head & signed interval enclosure (`replay.py:95-140`):** Identical architecture to `COMMON-CUTOFF/replay.py` (audited sound in `REVIEW2.md` §2.1). Computes exact entrywise `lower <= S * F_PP(q) <= upper` over $q \in [\text{left}, \text{right}]$, forms `center = (lower + upper) // 2` and `radius = upper - center` (so $|S F_{PP}(q) - \text{center}| \le \text{radius}$ entrywise), and subtracts weighted Gershgorin diagonal penalty `ceil((radius @ lin)_i / lin_i)`. Valid for **all** real vectors $x$, including mixed-sign vectors when $\mu^* > 0$.
- **Tail diagonal & Schur complement (`replay.py:99-101, 124-139`):** Enforces `k <= n` (no Coulomb in $F_{QQ}$) and $n^2 \ge 2b$ ($b = \lambda/\text{left}$), guaranteeing $F_{QQ} \succeq \operatorname{diag}(j+1)$ on $j \ge n$. Near tail ($n \le j < 2n$) is bounded via weighted Cauchy-Schwarz with `quad`; far tail ($j \ge 2n$) uses `far_lump(b, n, sum(h)) = 25*b^2*sum(h)/(4*(2n)^4)`. Exact.
- **Exact integer Cholesky & matvec (`replay.py:36-46, 162-179`):** `matvec` checks `max_a * max_x * cols + extra < 2**62` with Python `int` fallback (no silent clamping). `gram_positive` casts `L = np.rint(l * G).astype(np.int64)`, checks overflow guards before `L @ L.T`, `a * (G*G//S)`, and `abs(res).sum(axis=1)`, and certifies strict diagonal dominance of `res`.
- **Cold side (`replay.py:151-159`):** `different = (x < 0)[:, None] != (x < 0)` selects `hi` on opposite-sign pairs ($x_i x_j < 0$) and `lo` on same-sign pairs ($x_i x_j \ge 0$), upper-bounds the normal self-energy diagonal with `hi` and the Coulomb term with `up(2*mu*S)`, and uses `k = min(cutoff(q, scale2), n)` (exact for $x$ supported on $0 \dots n-1$).
- **Handoff & $\pi$ (`replay.py:189-215`):** Exact Theorem 4 handoff at $q = 4\lambda$ verified with Machin's $\pi$ enclosure (20 alternating terms).

### 2.2 `independent.py` — **COLD SIDE SOUND; HOT SIDE UNSOUND (P0)**
- **Cold side (`independent.py:186-210`) & Hutton $\pi$ (`independent.py:213-230`):** Sound and genuinely independent of `replay.py` (evaluates the unfolded full Matsubara line $n \in \{-N_C, \dots, N_C-1\}$ in exact `Fraction` arithmetic without using the folded identity, and computes 90-term Hutton $\pi$ enclosures).
- **Hot side (`independent.py:116-172`):** **UNSOUND** — fails both **R2-1** (Finding **F1**) and **R2-2** (Finding **F2**), with a minor residual overflow window in **R2-3** (Finding **F9**). Because `independent.py`'s hot verifier is unsound, `MUSTAR-HALF` lacks a valid second independent hot certificate.

---

## 3. Numbered Findings (P0–P3)

### F1. [P0] `independent.py` `hot_bound` uses an entrywise off-diagonal lower bound invalid for $\mu^* > 0$ (REVIEW2 defect R2-1)
- **Location:** `independent.py:124-143`
- **Issue:** `hot_bound` constructs `A/SC = D(hi) - P(lo) + 2*mu*1_k 1_k^T - diag(pen)`, replacing every off-diagonal pairing entry $-a_r(q)$ by its lower bound $-a_r(q_{\mathrm{lo}})$. Entrywise lower-bounding of off-diagonals guarantees $A/\mathrm{SC} \preceq F(q)$ only on nonnegative vectors ($x \ge 0$, Z-matrices). For $\mu^* > 0$, the positive Coulomb block produces mixed-sign unstable eigenvectors on which $x^T(A/\mathrm{SC} - F(q))x > 0$ is possible, yielding **false-positive certificates on provably unstable intervals**.
- **Evidence:** Direct calls to `independent.cover` + `independent.hot_bound` + `independent.positive` on two provably unstable boxes (see §5):
  - $(\lambda, \mu^*, R^2) = (10, 15, 9)$ on $[0.033058, 0.037457)$ ($k=16$, containing $q_{\mathrm{bad}} = 3745657/10^8$ with true $\lambda_{\min} = -0.392949 < 0$): `replay.py` **refuses**, while `independent.py` **certifies POSITIVE in 1 box**.
  - $(\lambda, \mu^*, R^2) = (12, 12, 9)$ on $[0.081633, 0.099707)$ ($k=10$, containing $q_{\mathrm{bad}} = 9970489/10^8$ with true $\lambda_{\min} = -0.140239 < 0$): `replay.py` **refuses**, while `independent.py` **certifies POSITIVE in 1 box**.
- **Fix:** Replace the entrywise off-diagonal bound with a signed-matrix interval enclosure (e.g., midpoint matrix minus an operator-norm/Frobenius/weighted-Gershgorin radius diagonal shift, valid for arbitrary-sign vectors).

### F2. [P0] `independent.py` `hot_bound` tail penalty `pen` underestimates the boundary Schur complement by $O(m)$ (REVIEW2 defect R2-2)
- **Location:** `independent.py:144-150`
- **Issue:** Although `independent.py` fixes two of `COMMON-CUTOFF`'s R2-2 bugs (it passes `m = NB // 2` to `tail_gap` and subtracts `pen` on the diagonal), its penalty formula
  $$\mathrm{pen}[i]/\mathrm{SC} = \frac{2 m}{g} \cdot \frac{2\lambda}{q_{\mathrm{lo}}(m-i)^2} \cdot \frac{2\lambda}{q_{\mathrm{lo}} m^2}$$
  is **mathematically invalid**. The factor $\eta_0 = 2\lambda/(q_{\mathrm{lo}} m^2)$ causes `pen[m-1]/SC` to decay as $O(1/(m g))$, whereas at the block boundary $i = m - 1, j = m$ we have $|j - i| = 1$, so $B_{m, m-1} = a_1(q_{\mathrm{lo}}) + a_{2m}(q_{\mathrm{lo}}) = O(1)$ and the true Schur-complement diagonal $(B^T F_{QQ}^{-1} B)_{m-1, m-1} \ge B_{m, m-1}^2 / F_{QQ, mm} = O(1/g)$ does **not** carry the extra $1/m$ factor.
- **Evidence:** At $\lambda = 26, q_{\mathrm{lo}} = 10, m = 200$: `independent.py` computes `pen[m-1]/SC = 6.881e-4`, whereas just the single $(j=m, i=m-1)$ term $B_{m, m-1}^2 / F_{QQ, mm} = 1.366 \times 10^{-2}$ is **$19.85\times$ larger** than the claimed upper bound.
- **Fix:** Bound the full infinite tail $\sum_{j=m}^\infty \frac{1}{g_j} b_j b_j^T$ rigorously (e.g., via exact row/column $\ell^1$ sums of $B$ over $j \ge m$, using $a_{j-i} \le a_1$ at $j - i = 1$ and $\sum_{r=1}^\infty r^{-2} = \pi^2/6$, without an invalid $1/m^2$ factor).

### F3. [P0] `RIGOR.md` §4.2 table and prose report four wrong, stale spectra that are not counterexamples (and one violates $\int u\,dp = 1$)
- **Location:** `RIGOR.md:111, 122-125`
- **Issue:** `RIGOR.md` §4.2 lists two-line spectra $(u_1, u_2, \theta)$ that completely disagree with `fixtures.json`, `bounds.json`, and `RESULT.md`:
  - `subhalf-25p6-0p4786`: `RIGOR.md` gives $(91/100, 16/10, 9/69)$ vs `fixtures.json` $(22/25, 20000, 3/499978)$. At $q = 11/20$, the `RIGOR.md` spectrum has $\lambda_{\min} = +0.1158 > 0$ (**stable, not a counterexample**).
  - `subhalf-26-12over25`: `RIGOR.md` gives $(22/25, 31/20, 12/67)$ vs `fixtures.json` $(4/5, 10000, 1/49996)$. At $q = 13/25$, `RIGOR.md`'s spectrum has $\lambda_{\min} = +0.1524 > 0$ (**stable**).
  - `subhalf-27-0p4848`: `RIGOR.md` gives $(89/100, 19/10, 11/101)$ vs `fixtures.json` $(69/100, 2000, 31/199931)$. At $q = 51/100$, `RIGOR.md`'s spectrum has $\lambda_{\min} = +0.2220 > 0$ (**stable**).
  - `subhalf-28-0p489`: `RIGOR.md` gives $(55/62, 25/11, 77/962)$ vs `fixtures.json` $(16/25, 1000, 9/24984)$. Its first moment is $(1-\theta)u_1 + \theta u_2 = 59525/59644 \neq 1$ (**not in $\mathcal{P}_1$**) and $\lambda_{\min} = +0.2944 > 0$ (**stable**).
  - `RIGOR.md:111` prose also states "$u_1 \in [0.88, 0.91]$ and $u_2 \in [1.50, 2.25]$", contradicting the actual certified spectra ($u_1 \in [0.64, 0.88], u_2 \in [1000, 20000]$).
- **Fix:** Replace the stale table and prose in `RIGOR.md` §4.1–§4.2 with the exact rational spectra from `fixtures.json`/`bounds.json`.

### F4. [P0] `RIGOR.md` Theorem 3 (`RESULT.md` Theorem 2, $k=1$ for $\mu^*/\lambda \le 1/2$) has a broken proof and a false monotonicity claim
- **Location:** `RIGOR.md:77-94`, `RESULT.md:16, 64`, `structure.py:86-90`
- **Issue:** `RIGOR.md` Theorem 3 claims that for **all** $\lambda > 0$ and $\mu^* \le \lambda/2$, the $k=1$ ground-state eigenvector $h^*$ satisfies $h_0^* \ge h_1^* > h_2^* > \dots > 0$, asserting on line 92 that $\tilde{D}_{p,0} \le \tilde{D}_{p,1}$ holds "for all $\lambda$ at the onset when $\mu^*/\lambda \le 1/2$ because $1 + 2\mu^* - a_1 \le 1 + \lambda - a_1 < 3 + a_1$." That algebraic inequality is **false**: $1 + \lambda - a_1 < 3 + a_1 \iff \lambda < 2 + 2a_1$, which fails at large $\lambda$. When $\tilde{D}_{p,1} - \tilde{D}_{p,0} = 2 + 2a_1 - 2\mu^* < 0$, the monotone cone $\mathcal{C} = \{h_0 \ge h_1 \ge \dots \ge 0\}$ is **not invariant**, and $h_0^* \ge h_1^*$ **explicitly fails**:
  - Einstein, $k=1, \lambda = 20, \mu^* = 10$ ($q_{\mathrm{on}} = 1.86444$): $a_1 = 6.9822$, $\tilde{D}_1 - \tilde{D}_0 = -4.0357 < 0$, **$h_0^* = 0.56948 < h_1^* = 0.60935$**.
  - Einstein, $k=1, \lambda = 50, \mu^* = 25$ ($q_{\mathrm{on}} = 2.72444$): $a_1 = 13.4248$, $\tilde{D}_1 - \tilde{D}_0 = -21.1503 < 0$, **$h_0^* = 0.41153 < h_1^* = 0.60185$**.
  - Non-Einstein $p = 0.9\delta_{0.2} + 0.1\delta_{8.2}$, $k=1, \lambda = 20, \mu^* = 10$ ($q_{\mathrm{on}} = 1.03274$): $\tilde{D}_1 - \tilde{D}_0 = -8.6068 < 0$, **$h_0^* = 0.44978 < h_1^* = 0.64681$**.
  - Furthermore, `structure.py:66, 86-90` only samples $\mu^* \in [0, 1]$ (where $2 + 2a_1 - 2\mu^* > 0$ trivially holds), masking the failure for $\mu^* > 1$. Also `RIGOR.md:76-80` omits $+a_0$ from $\tilde{D}_{p,i}$ when moving $a_0$ into $\tilde{A}_p$, and leaves unresolved draft text (`... in fact, ... Wait:`) on line 83.
- **Fix:** Either restrict Theorem 3 to the genuinely proved parameter regime $\mu^* \le 1 + a_1(q;p)$ (where $\tilde{D}_0 \le \tilde{D}_1$ and $h_0^* \ge h_1^*$ hold rigorously), or supply a new proof that does not assume $h_0^* \ge h_1^*$ for large $\lambda$; downgrade the unrestricted $k=1$ claim to `CONJECTURED / NUMERICAL` in the meantime.

### F5. [P1] `RESULT.md` claims `PROVED` for two theorems absent from `RIGOR.md`, misnumbers theorems, and `RIGOR.md` Theorem 2 fails at $4R^2 = q_E(\lambda, 0)$
- **Location:** `RESULT.md:14-18`, `RIGOR.md:67-72`
- **Issue:**
  1. `RESULT.md:17` (Theorem 3: small-$\mu^*$ spectral gap stability $\mu^* < g_{\mathrm{gap}}(\lambda)/(2k_E)$) and `RESULT.md:18` (Theorem 4: large-$\lambda$ fixed-$R$ optimality $\lambda > \frac{16}{3}(\frac{\pi^2}{3} + 2\frac{\mu^*}{\lambda}) R^2$) are labeled `PROVED (pending review)` in `RESULT.md`, but **neither statement nor proof appears anywhere in `RIGOR.md`**.
  2. Theorem numbering disagrees between `RESULT.md` and `RIGOR.md` (`RESULT.md` Theorems 1–2 correspond to `RIGOR.md` Theorems 2–3; `RIGOR.md` Theorem 1 is unnumbered in `RESULT.md`; `RIGOR.md` Theorem 4 is $q \ge 4\lambda$ asymptotic stability).
  3. `RIGOR.md` Theorem 2 (`k = 0` optimality) states $4R^2 \le q_E(\lambda, 0)$ (non-strict). At exact equality $4R^2 = q_E(\lambda, 0)$ with any $\mu^* > 0$, every $q < q_E(\lambda, 0)$ has $k(q, R) \ge 1$, so $\lambda_{\min}(\mathcal{F}_{\delta_1}^{(k)}(q))$ jumps upward discontinuously at $q_E(\lambda, 0)^-$ and stays strictly positive on $(q_E(\lambda,0)-\epsilon, q_E(\lambda,0))$, making $q_{\mathrm{lin}}(\delta_1) < q_E(\lambda, 0)$ (contradicting the stated equality $q_{\mathrm{lin}}(\delta_1) = q_E(\lambda, 0)$).
- **Fix:** Tighten `RIGOR.md` Theorem 2 to strict inequality $4R^2 < q_E(\lambda, 0)$; synchronize theorem numbering between `RESULT.md` and `RIGOR.md`; remove `PROVED` claims for Theorems 3–4 of `RESULT.md` until full proofs are written in `RIGOR.md`.

### F6. [P2] `RIGOR.md` Theorem 1 (two-delta reduction) boundedness justification is invalid for general $h \in \mathcal{D}(\mathcal{F})$
- **Location:** `RIGOR.md:59-64`
- **Issue:** The proof claims $\Phi_{h,q}(u) = \lambda \sum_{j=1}^\infty \frac{u}{u+qj^2} L_j(h)$ is "continuous and bounded on $(0, \infty)$ (since $|L_j(h)| \le 6\|h\|_2^2$ and $\frac{u}{u+qj^2} \le \frac{u}{qj^2}$)." That bound gives $|\Phi_{h,q}(u)| \le \frac{\pi^2\lambda}{q} u \|h\|_2^2$, which grows linearly in $u$ as $u \to \infty$ rather than being bounded.
- **Fix:** Take the infimum over the core of **finitely supported** $h$ (where $L_j(h) = 0$ for $j \ge 2N$, so $\Phi_{h,q}(u)$ is a finite sum and genuinely continuous and bounded on $(0, \infty)$), then apply Richter-Rogosinski to $(u, \Phi_{h,q}(u))$.

### F7. [P2] Unfinished draft text and wrong display `(2)` in `RIGOR.md` Lemma 1; minor phrasing slip in Theorem 4
- **Location:** `RIGOR.md:36-48, 100`
- **Issue:** Lemma 1 displays the wrong formula `(2)` (missing factor $1/2$ on the Hankel sum and extra factor $2$ on the Toeplitz sum) followed by draft self-correction text (`?? Wait:`), then gives the correct `(2')`. Also `RIGOR.md:100` writes `- \sum_{m=0}^{i-1}(missing)` for the off-diagonal row sum, which is actually identically $2\sum_{j=1}^\infty a_j - a_{2i+1}$ (so subtracting from $2i+1 + 2\sum_{j=1}^i a_j - a_{2i+1}$ gives $(2i+1) - 2\sum_{j=i+1}^\infty a_j \ge (2i+1) - 2\sum_{j=1}^\infty a_j$).
- **Fix:** Replace `(2)` directly with `(2')`, remove all `?? Wait:` draft scratch text, and clean up line 100.

### F8. [P2] `RESULT.md` $C_E$ decimal tables are inward-rounded / stale relative to `bounds.json` on 5 of 8 entries
- **Location:** `RESULT.md:27-40`
- **Issue:** Comparing `RESULT.md` against `bounds.json`:
  - `subhalf-27-0p4848`: `bounds.json` upper bound is `0.0198264638`, `RESULT.md` gives `0.01982610` (**inward / too low**).
  - `anchor-l2-mu1-R3/2`: `bounds.json` lower bound is `0.0225641075`, `RESULT.md` gives `0.02256758` (**inward**).
  - `anchor-l3-mu3/2-R2`: `bounds.json` upper bound is `0.0225266567`, `RESULT.md` gives `0.02252521` (**inward**).
  - `anchor-l10-mu4-R3`: `bounds.json` lower bound is `0.0334225380`, `RESULT.md` gives `0.03342336` (**inward**).
  - `anchor-l20-mu19/2-R5`: `bounds.json` lower bound is `0.0322264198`, `RESULT.md` gives `0.03222749` (**inward**).
- **Fix:** Recompute every `RESULT.md` decimal bracket directly from `bounds.json` with strict outward rounding.

### F9. [P2] `independent.py` `positive()` has a residual `int64` subtraction overflow window (REVIEW2 defect R2-3 partial)
- **Location:** `independent.py:151, 163-168`
- **Issue:** Unlike `COMMON-CUTOFF/independent.py`, line 163 properly casts `Lh = np.rint(L * GS).astype(np.int64)`. However, line 151 permits `|A| < 2**35` with `factor = GS*GS // SC = 2**28`, so `|A * factor|` can approach $2^{63}$, and subtracting `Lh @ Lh.T` (bounded by $2^{62}$) in `res = A * factor - Lh @ Lh.T` can overflow signed `int64` ($2^{63}-1$) on large-entry blocks (not triggered on the 8 current fixtures, where `|A|` is well below $2^{35}$).
- **Fix:** Tighten the guard in `hot_bound` to `int(np.abs(A).max()) < 2**33` (so `|A * factor| < 2**61` and `|A * factor - Lh @ Lh.T| < 2**62 + 2**61 < 2**63`).

---

## 4. `CHECKS.txt` Rerun Table (All 15 Commands)

Re-run in `D:/dev/scratch/ceiling-20261118/C-LAMBDA-MU/MUSTAR-HALF` with the exact `RUN` prefix from `CHECKS.txt`:

| Command | Exit | Observed Outcome |
|---|---:|---|
| `replay.py` | 0 | All 4 counterexamples + 4 anchors verified (`2638, 1444, 539, 239, 12, 18, 10, 17` boxes); `stored bounds.json verified without rewriting` (275.9s) |
| `replay.py --mutant coulomb` | 1 | `REFUSED: cold certificate dies when Coulomb repulsion is doubled` |
| `replay.py --mutant spectrum` | 1 | `REFUSED: mirrored spectrum rejected (invalid two-line spectrum ordering)` |
| `replay.py --mutant endpoint` | 1 | `REFUSED: cold witness refused at certified-stable upper endpoint q_hi` |
| `replay.py --mutant tail` | 1 | `REFUSED: disabled far-tail bound is exceeded by exact omitted term` |
| `replay.py --mutant sign` | 1 | `REFUSED: sign-flipped Coulomb mask rejected (hot interval cannot be certified: 0.501 0.501000085666 k=5)` |
| `independent.py` | 0 | Exited 0 (27.4s), **but hot verifier is unsound (F1, F2)** |
| `independent.py --mutant endpoint` | 1 | `REFUSED: Einstein form is not positive on [q_lo, 4*lam)` |
| `independent.py --mutant coulomb` | 1 | `REFUSED: doubling mu* removes cold instability at q=13/25 (val=2.16586e+14 >= 0)` |
| `independent.py --mutant spectrum` | 1 | `REFUSED: p -> 1-p mixture rejected by second-moment guard` |
| `independent.py --mutant receipt` | 1 | `REFUSED: shaved C_E bracket rejected by receipt check` |
| `structure.py` | 0 | `structural checks passed on 40 random rational trials (exact Fraction arithmetic)` (only samples $\mu^* \le 1$, see **F4**) |
| `structure.py --mutant` | 1 | `REFUSED: mutant structural check failed as required` |
| `phase_scan.py` | 0 | Unfolded-vs-folded diff `8.88e-16`; $k \in \{1..4\}$ min eig `+2.0734e-03`; $k=5$ fold `r*` dips to `0.4800` at $\lambda=26$ |
| `phase_scan.py --mutant` | 1 | `REFUSED: omitting factor 2 in unfolded normal self-energy breaks folding identity (max diff 24.33)` |

---

## 5. Adversarial Inputs and Outcomes

| Adversarial Probe | Parameters | True State | `replay.py` | `independent.py` |
|---|---|---|---|---|
| **R2-1 smoking gun 1** | $\lambda=10, \mu^*=15, R^2=9$, box $[0.033058, 0.037457)$, $q_{\mathrm{bad}}=3745657/10^8$ ($k=16$) | Unstable ($\lambda_{\min} = -0.392949$) | **REFUSED (`False`)** | **FALSE POSITIVE (`True`, 1 box)** |
| **R2-1 smoking gun 2** | $\lambda=12, \mu^*=12, R^2=9$, box $[0.081633, 0.099707)$, $q_{\mathrm{bad}}=9970489/10^8$ ($k=10$) | Unstable ($\lambda_{\min} = -0.140239$) | **REFUSED (`False`)** | **FALSE POSITIVE (`True`, 1 box)** |
| **Unstable Einstein box (`MUSTAR-HALF`)** | $\lambda=26, \mu^*=312/25, R^2=53/5$, box $[0.490, 0.505)$, $q_{\mathrm{bad}}=0.495$ ($k=5$) | Unstable ($\lambda_{\min} = -3.96\times 10^{-4}$) | **REFUSED (`False`)** | **REFUSED (`False`)** |
| **Perturbed non-counterexample** | `subhalf-26-12over25` at $q=13/25$ with $(u_1, u_2, p) = (99/100, 10000, 1/999901)$ | Stable ($\lambda_{\min} = +8.76\times 10^{-4}$) | **REFUSED (`False`)** | **REFUSED (`False`)** |
| **R2-2 boundary Schur diagonal** | $\lambda=26, q_{\mathrm{lo}}=10, m=200$, single term $B_{m,m-1}^2 / F_{QQ,mm}$ | True term $= 1.366\times 10^{-2}$ | Bounded via exact `near` | **`pen[m-1]/SC = 6.881e-4` ($19.85\times$ too small)** |

---

## 6. Independent Recomputation of $T_{\mathrm{mix}}/T_E$ and Convention / Discontinuity Check

Independent folded ($N=300, 600$) and unfolded full-line ($2N=600$, retaining $a_0$ in $D_n$ and $K_{nm}$) recomputations for all four counterexamples in `fixtures.json`:

| Case | $\mu^*/\lambda$ | $k=5 \to 4$ jump $4R^2/81$ | $q_E$ ($N=600$) | $q_{\mathrm{mix}}$ ($N=600$) | True $T_{\mathrm{mix}}/T_E$ ($N=300$ vs $600$) | Unfolded $\lambda_{\max}(D^{-1/2}KD^{-1/2})$ at $q_{\mathrm{mix,cert}}$ (E vs mix) |
|---|---:|---:|---:|---:|---|---|
| `subhalf-25p6-0p4786` | $0.478602$ | $0.55802469$ | $0.52298891$ | $0.55802469$ (at jump) | $1.03295368$ vs $1.03295278$ ($+3.30\%$) | $0.99997634 < 1$ vs $1.00000540 > 1$ |
| `subhalf-26-12over25` | $0.480000$ | $0.52345679$ | $0.49876077$ | $0.52345679$ (at jump) | $1.02445912$ vs $1.02445828$ ($+2.45\%$) | $0.99997300 < 1$ vs $1.00019221 > 1$ |
| `subhalf-27-0p4848` | $0.484815$ | $0.62222222$ | $0.41652893$ | $0.56093575$ (interior) | $1.16047009$ vs $1.16047016$ ($+16.05\%$) | $0.99903242 < 1$ vs $1.00017277 > 1$ |
| `subhalf-28-0p489` | $0.489000$ | $0.61234568$ | $0.40991736$ | $0.57220079$ (interior) | $1.18147915$ vs $1.18147918$ ($+18.15\%$) | $0.99812356 < 1$ vs $1.00035749 > 1$ |

- **Conventions:** Identical to `COMMON-CUTOFF` ($c_n = \mathbf{1}_{(2n+1)^2 q < 4R^2}$, strict inequality, pairing-only $\mu^*$, common $R = \omega_c/\Omega_E$).
- **Truncation sensitivity:** Not a truncation artefact ($N=300$ and $N=600$ agree to 7 significant figures, and `replay.py` certifies on infinite $\ell^2(\mathbb{Z}_{\ge 0})$).
- **Role of the mask discontinuity:** For `subhalf-26-12over25` at fixed $k=5$, Einstein is unstable at $q = 0.495$ ($\lambda_{\min} = -4.0\times 10^{-4}$), enters a narrow stable island on $[0.501, 0.5234]$ ($\lambda_{\min} \in [+2.0, +9.0]\times 10^{-4}$), and becomes unstable *again* on $[0.55, 0.70]$ ($\lambda_{\min} \approx -6.6\times 10^{-3}$). The sharp $k = 5 \to 4$ cutoff jump at $q = 4R^2/81 = 0.523457$ (where $\lambda_{\min}(k=4) = +3.273$) truncates Einstein's upper $k=5$ unstable branch, leaving Einstein stable for all $q \ge 0.501$ while the two-line mixture is unstable inside Einstein's stable island. Thus the counterexample is mathematically exact in the sharp-cutoff model, **but** physically depends on the sharp Matsubara step discontinuity.

---

## 7. Physical Framing and Preprint Combination with `COMMON-CUTOFF`

- **Model-class membership vs physical realism:** Mathematically, $\lambda \in [25.6, 28]$ and two-delta spectra with $\theta \sim 10^{-5}\text{--}3.6\times 10^{-4}$ at $u_2 \in [1000, 20000]$ lie strictly inside the stated model class $\mathcal{P}_1 = \{p \text{ on } (0,\infty) : \int u\,dp = 1\}$ with $\lambda > 0$. Physically, however, $\lambda \sim 26$ is far outside the realistic Migdal-Eliashberg regime ($\lambda \lesssim 2\text{--}3$), $u_2 = 20000$ places a tiny spectral weight at $\Omega_2 \approx 141\,\Omega_E \gg \omega_c$, and the mechanism relies on the sharp Matsubara step-mask jump $k = 5 \to 4$.
- **Headline scoping:** The headline that $\mu^*/\lambda = 1/2$ is **not** a universal threshold is mathematically true and genuinely surprising, provided it is explicitly scoped to the sharp common-cutoff linearized Eliashberg model in the ultra-strong-coupling $k=5$ re-entrant fold ($\lambda \in [25.55, 34]$) with extreme high-frequency-tail two-delta spectra (and noting that no counterexample is observed below $\lambda \approx 25.55$ or for $k \in \{0, 1, 2, 3, 4\}$).
- **Combining `MUSTAR-HALF` with `COMMON-CUTOFF` into one preprint:** **YES — strongly recommended, once the P0 defects are fixed.** Both packages share the exact same model, conventions, and `replay.py` certification engine, and both currently fail review for the exact same `independent.py` hot-verifier bugs (R2-1, R2-2). Fixing `independent.py` once with a sound signed-matrix hot verifier, correcting `RIGOR.md` §4.2 and Theorems 1–3, and synchronizing `RESULT.md` produces a single, cohesive, substantially stronger preprint: Einstein optimality fails above $\mu^*/\lambda = 1/2$ (`COMMON-CUTOFF`), *and* even $\mu^*/\lambda = 1/2$ is broken in the sharp-cutoff model by the $k=5$ re-entrant fold (`MUSTAR-HALF`).
