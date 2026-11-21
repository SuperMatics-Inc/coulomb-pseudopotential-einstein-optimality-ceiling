# FIX — Proof, Document, and Structural-Check Repair for `mustar-half` (`REVIEW.md` F3–F8)

Status: **proof draft and document/structural repairs applied, awaiting re-review.**
Per project rules, nothing in `RIGOR.md` or `RESULT.md` is self-labeled `PROVED` or `CERTIFIED`; theorems in `RIGOR.md` and `RESULT.md` are labeled **proof draft**.

Backups of the pre-repair v1 files are preserved in this directory:
- `RIGOR.v1.md` (exact copy of v1 `RIGOR.md`)
- `RESULT.v1.md` (exact copy of v1 `RESULT.md`)
- `structure.v1.py` (exact copy of v1 `structure.py`)

`replay.py`, `bounds.json`, `fixtures.json`, `phase_scan.py`, and `REVIEW.md` were not modified (`independent.py` and its `CHECKS.txt` rows are handled in a separate slice for F1, F2, F9).

---

## 1. Per-Finding Changes and `file:line` References

| Finding | Severity | Issue in v1 | Resolution in v2 | `file:line` references |
|---|---|---|---|---|
| **F3** | **P0** | `RIGOR.md` §4.2 table listed stale pre-tuning spectra ($\theta \in \{0.008, 0.006, 0.012, 0.015\}$, $u_2 \in \{36, 42, 32, 30\}$) with $\int u\,dp \in [0.808, 1.158] \neq 1$, contradicting `fixtures.json` and `bounds.json`. | Replaced the `RIGOR.md` §4.2 table with the exact rational two-line spectra $\{(p_1, u_1), (p_2, u_2)\}$ from `fixtures.json` / `bounds.json` (`subhalf-25p6-0p4786`, `subhalf-26-12over25`, `subhalf-27-0p4848`, `subhalf-28-0p489`), added explicit rational moment verification $p_1 + p_2 = 1$ and $p_1 u_1 + p_2 u_2 = 1$ for all four cases, and included both the certified lower bound $T_{\mathrm{mix}}/T_{E,\mathrm{hi}}$ and the reviewer-verified $N=600$ ratio $T_{\mathrm{mix}}/T_E$. Synchronized the same table in `RESULT.md` §2.2. | `RIGOR.md:145-165`<br>`RESULT.md:23-31` |
| **F4** | **P0** | v1 `RIGOR.md` Theorem 2 claimed $\tilde{D}_{p,0} \le \tilde{D}_{p,1}$ and $h^*_0 \ge h^*_1 > h^*_2 > \dots > 0$ on the $k=1$ branch for **all** $\lambda > 0$ whenever $\mu^*/\lambda \le 1/2$, which is false when $\mu^* > 1 + a_1(q;p)$ (e.g., $\tilde{D}_1 - \tilde{D}_0 < 0$ and $h^*_0 < h^*_1$ at $\lambda=20, \mu^*=10$ and $\lambda=50, \mu^*=25$, and for soft-mode mixtures as $u_1 \to 0^+$ whenever $\mu^* > 1$). Moreover, v1 `structure.py` only tested $\mu \in \{0, 1/2, 1\}$ (`randint(0,10)/10`) and had a tautological `--mutant` flag. | **Shrunk and proved exact cone-monotonicity regime (now Theorem 4):**<br>1. Proved Part 1 under the exact diagonal-ordering condition $\mu^* \le 1 + a_1(q; p)$ (`RIGOR.md:81-88, 91-115`), which holds **unconditionally** for all $q > 0$ and all $p \in \mathcal{P}_1$ whenever $\mu^* \le 1$, and across the entire sub-half sector $\mu^*/\lambda \le 1/2$ for all $\lambda \in (0, 2]$. Included the full telescoping pairing identity $(\tilde{A}_p h)_i - (\tilde{A}_p h)_{i+1} = \sum_{s=0}^\infty (a_s - a_{s+1})(y_{i-s} - y_{i+1+s}) > 0$ (Step 1) and Birman–Schwinger / Krein–Rutman cone invariance (Step 2).<br>2. Added Part 2 (`RIGOR.md:89`) explicitly recording the failure of $\tilde{D}_{p,0} \le \tilde{D}_{p,1}$ and $h^*_0 \ge h^*_1$ for $\mu^* > 1 + a_1(q; p)$ (citing the $\lambda=20, \mu^*=10$ and $\lambda=50, \mu^*=25$ witnesses and the $u_1 \to 0^+$ limit) and marking the remaining $k=1$ range $\lambda \in (2, 151]$ for $\mu^* > 1 + a_1(q;p)$ as numerical (`phase_scan.py`) / open in `RESULT.md:17, 66, 74`.<br>3. Extended `structure.py` random trials (`structure.py:92-148`) across $\mu^* \in [0, \lambda/2]$ for $\lambda \in (0, 2]$ (including boundary $\mu^* = \lambda/2$), $\mu^* \in [0, 1]$ for $\lambda \in (0, 40]$, and $\mu^* \in [0, 1+a_1(q;p)]$ for $\lambda \in (0, 40]$, plus explicit F4 refutation witnesses (`structure.py:173-185`) and three guarded mutants `--mutant {coulomb, f4, norm}` (`structure.py:188-261`), where `--mutant f4` specifically tests the false v1 claim $\tilde{D}_0 \le \tilde{D}_1$ at $\lambda > 2, \mu^* = \lambda/2$ and exits 1. | `RIGOR.md:81-115`<br>`RESULT.md:17, 66, 74`<br>`structure.py:69-72, 111-148, 173-261` |
| **F5** | **P1** | (a) Theorem numbering and inventory differed between `RESULT.md` and `RIGOR.md`; (b) `RESULT.md` claimed an unproved small-$\mu^*$ spectral-gap theorem ($\mu^* < \Delta_{\mathrm{gap}}(p)/(2k)$) and an unproved $\mu^*$-dependent large-$\lambda$ formula not in `RIGOR.md`; (c) the $k=0$ theorem included the boundary $4R^2 = q_E(\lambda, 0)$, where $k(q,R) \ge 1$ for $q < q_E(\lambda, 0)$. | 1. **Synchronized theorem list and numbering (Lemma 1 + Theorems 1–5) identically across `RIGOR.md` and `RESULT.md`:**<br>  - Lemma 1: Exact Finite-Support Decomposition (`RIGOR.md:31-44`, `RESULT.md:13`)<br>  - Theorem 1: Universal Two-Delta Reduction at Fixed $(q, k, \mu^*)$ (`RIGOR.md:53-58`, `RESULT.md:14`)<br>  - Theorem 2: Exact Zero-Mask Optimality $k(q,R)=0$ for All $\mu^* \ge 0$ (`RIGOR.md:60-64`, `RESULT.md:15`)<br>  - Theorem 3: Large-Coupling Fixed-$R$ Einstein Optimality (`RIGOR.md:66-73`, `RESULT.md:16`)<br>  - Theorem 4: Single-Mode $k=1$ Cone Monotonicity and Einstein Optimality for $\mu^* \le 1 + a_1(q;p)$ (`RIGOR.md:81-115`, `RESULT.md:17`)<br>  - Theorem 5: Parameter-Free Asymptotic Cutoff Stability for All $q \ge 4\lambda$ (`RIGOR.md:117-128`, `RESULT.md:18`)<br>2. **Dropped the unproved small-$\mu^*$ spectral-gap claim** from `RESULT.md` (recorded in `RESULT.md:16`).<br>3. **Proved Theorem 3 in `RIGOR.md:66-73`** with the sharper $\mu^*$-independent bound $\lambda \ge 4R^2 + 1 \implies q_E(\lambda, 0) > \lambda - 1 \ge 4R^2$ (via the exact trial vector $v_\epsilon = e_0 + \epsilon e_1$ at $q_* = \lambda - 1$, where $(\mathcal{F}_{\delta_1}^{(0)})_{0,0} = 0$ and $(\mathcal{F}_{\delta_1}^{(0)})_{0,1} < -1$; verified in `structure.py:149-160`).<br>4. **Changed Theorem 2 to strict inequality $4R^2 < q_E(\lambda, 0)$** (`RIGOR.md:60-64`, `RESULT.md:15, 62`) so $k(q,R) = 0$ on the open neighborhood $(4R^2, \infty) \supset [q_E(\lambda, 0), \infty)$ and $q_{\mathrm{lin}}(p) < q_E(\lambda, 0)$ cannot jump back across $q_E(\lambda, 0)$. | `RIGOR.md:31-128`<br>`RESULT.md:12-18, 62`<br>`structure.py:149-160` |
| **F6** | **P2** | `RIGOR.md` §2 Theorem 1 claimed $\Phi_{h,q}(u) = \lambda \sum_{j=1}^\infty \frac{u}{u+qj^2} L_j(h)$ is bounded on $(0,\infty)$ for arbitrary $h \in \ell^2$, which is only guaranteed when $\sum_j |L_j(h)| < \infty$. | Restricted the pointwise Richter–Rogosinski / Markov–Krein reduction in Theorem 1 to the finitely supported form core $\mathcal{D}_0 \subset \ell^2(\mathbb{Z}_{\ge 0})$ (`RIGOR.md:53-58`, `RESULT.md:14`): for $h$ supported on $\{0, \dots, N-1\}$, $L_j(h) = 0$ identically for all $j \ge 2N$, so $\Phi_{h,q}(u) = \lambda \sum_{j=1}^{2N-1} \frac{u}{u+qj^2} L_j(h)$ is a finite sum bounded by $\lambda \sum_{j=1}^{2N-1} |L_j(h)| < \infty$ on $(0,\infty)$. Since $\mathcal{D}_0$ is a form core for $\mathcal{F}_p^{(k)}(q)$, taking the infimum over $h \in \mathcal{D}_0$ with $\|h\|_2 = 1$ yields $\inf_{p \in \mathcal{P}_1} \lambda_{\min}(\mathcal{F}_p^{(k)}(q)) = \inf_{p_2 \in \mathcal{P}_1^{(2)}} \lambda_{\min}(\mathcal{F}_{p_2}^{(k)}(q))$. | `RIGOR.md:53-58`<br>`RESULT.md:14` |
| **F7** | **P2** | `RIGOR.md` Lemma 1 display (2) had a missing factor of $2$ on the last sum ($\sum_{i=0}^{j-1} h_i^2$ instead of $2\sum_{i=0}^{j-1} h_i^2$) and contained leftover draft self-correction prose ("Wait: let us check the sign..."). | Corrected display (2) in `RIGOR.md:34` to $L_j(h) = \frac{1}{2}\sum_{i=0}^{j-1}(h_i - h_{j-1-i})^2 + \sum_{i=0}^\infty (h_i - h_{i+j})^2 - 2\sum_{i=0}^{j-1} h_i^2 = -\sum_{i=0}^{j-1} h_i h_{j-1-i} - 2\sum_{i=0}^\infty h_{i+j}(h_i - h_{i+j})$, wrote a clean 3-step proof draft (`RIGOR.md:36-43`), removed all draft self-talk, and added `L_j_rigor(h, j)` in `structure.py:49-56, 100-106` to verify both expressions of display (2) in exact `Fraction` arithmetic on every trial. | `RIGOR.md:31-44`<br>`structure.py:49-56, 100-106` |
| **F8** | **P2** | `RESULT.md` §2.2 table reported single 6-digit decimals for $C_E$ that truncated the upper bound of `bounds.json["einstein_C"]`. | Replaced the single $C_E$ column in `RESULT.md` §2.2 (`RESULT.md:25-30`) and §2.3 (`RESULT.md:34-39`) with outward-rounded 8-decimal-place brackets $[C_{E,\mathrm{lo}},\, C_{E,\mathrm{hi}}]$ computed with `ROUND_FLOOR` / `ROUND_CEILING` from the exact rational `einstein_C` fractions in `bounds.json`. Added explicit physical-extremity caveats ($\lambda \approx 25.6\text{--}28$, $u_2 \in [10^3, 2\times 10^4]$, sharp $k=5 \to 4$ Matsubara step) in `RESULT.md:68-72`. | `RESULT.md:23-39, 68-72` |

---

## 2. Exact Moment Verification for `RIGOR.md` §4.2 / `RESULT.md` §2.2 (Finding F3)

For each two-line spectrum $p = p_1 \delta_{u_1} + p_2 \delta_{u_2}$ in `fixtures.json` / `bounds.json`:
1. `subhalf-25p6-0p4786`: $(p_1, u_1) = \left(\frac{499975}{499978}, \frac{22}{25}\right)$, $(p_2, u_2) = \left(\frac{3}{499978}, 20000\right)$:
   $$p_1 + p_2 = \frac{499975 + 3}{499978} = 1, \qquad p_1 u_1 + p_2 u_2 = \frac{439978 + 60000}{499978} = 1.$$
2. `subhalf-26-12over25`: $(p_1, u_1) = \left(\frac{49995}{49996}, \frac{4}{5}\right)$, $(p_2, u_2) = \left(\frac{1}{49996}, 10000\right)$:
   $$p_1 + p_2 = \frac{49995 + 1}{49996} = 1, \qquad p_1 u_1 + p_2 u_2 = \frac{39996 + 10000}{49996} = 1.$$
3. `subhalf-27-0p4848`: $(p_1, u_1) = \left(\frac{199900}{199931}, \frac{69}{100}\right)$, $(p_2, u_2) = \left(\frac{31}{199931}, 2000\right)$:
   $$p_1 + p_2 = \frac{199900 + 31}{199931} = 1, \qquad p_1 u_1 + p_2 u_2 = \frac{137931 + 62000}{199931} = 1.$$
4. `subhalf-28-0p489`: $(p_1, u_1) = \left(\frac{24975}{24984}, \frac{16}{25}\right) = \left(\frac{2775}{2776}, \frac{16}{25}\right)$, $(p_2, u_2) = \left(\frac{9}{24984}, 1000\right) = \left(\frac{1}{2776}, 1000\right)$:
   $$p_1 + p_2 = \frac{24975 + 9}{24984} = 1, \qquad p_1 u_1 + p_2 u_2 = \frac{15984 + 9000}{24984} = 1.$$

---

## 3. Verification Reruns and Recorded Exit Codes

Runner prefix (from `CHECKS.txt`, working directory `records/mustar-half`):
```bash
RUN="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --no-project --with numpy --with scipy python -B"
```

| Command | Expected exit | Actual exit | Output summary |
|---|---:|---:|---|
| `$RUN structure.py` | `0` | `0` | `structural checks passed on 40 random rational trials + F4 refutation witnesses (exact Fraction arithmetic)` |
| `$RUN structure.py --mutant` | `1` | `1` | `REFUSED: mutant structural checks failed as required: coulomb (dropped 2*mu*s^2 term); f4 (unrestricted F4 D_0 <= D_1 at lam > 2, mu* = lam/2); norm (rescaled u -> 2*u violating Moment-1)` |
| `$RUN structure.py --mutant f4` | `1` | `1` | `REFUSED: mutant structural checks failed as required: f4 (unrestricted F4 D_0 <= D_1 at lam > 2, mu* = lam/2)` |
| `$RUN structure.py --mutant coulomb` | `1` | `1` | `REFUSED: mutant structural checks failed as required: coulomb (dropped 2*mu*s^2 term)` |
| `$RUN structure.py --mutant norm` | `1` | `1` | `REFUSED: mutant structural checks failed as required: norm (rescaled u -> 2*u violating Moment-1)` |
| `$RUN phase_scan.py` | `0` | `0` | `1. Unfolded-to-folded exact equivalence check: max matrix diff = 8.88e-16 (< 1e-12); 2. Mask-index k in {1,2,3,4} scan at mu*/lambda = 1/2: min mixture eig at q_E = +2.0734e-03 >= 0; 3. k=5 re-entrant fold scan (NUMERICAL): OK` |
| `$RUN phase_scan.py --mutant` | `1` | `1` | `REFUSED: omitting factor 2 in unfolded normal self-energy breaks folding identity (max diff 24.33)` |
| `$RUN replay.py` | `0` | `0` | `stored bounds.json verified without rewriting` (4 sub-1/2 counterexamples + 4 anchors) |
| `$RUN replay.py --mutant coulomb` | `1` | `1` | `REFUSED: cold certificate dies when Coulomb repulsion is doubled` |
| `$RUN replay.py --mutant spectrum` | `1` | `1` | `REFUSED: mirrored spectrum rejected (invalid two-line spectrum ordering)` |
| `$RUN replay.py --mutant endpoint` | `1` | `1` | `REFUSED: cold witness refused at certified-stable upper endpoint q_hi` |
| `$RUN replay.py --mutant tail` | `1` | `1` | `REFUSED: disabled far-tail bound is exceeded by exact omitted term` |
| `$RUN replay.py --mutant sign` | `1` | `1` | `REFUSED: sign-flipped Coulomb mask rejected (hot interval cannot be certified: 0.501 0.501000085666 k=5)` |
