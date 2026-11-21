# Fourth-Round Independent Review of `COMMON-CUTOFF` (`REVIEW4.md`)

**Final Verdict: PASS** (for `CERTIFIED` / `PROVED` status per claim table below).

**Preprint readiness:** **YES — `COMMON-CUTOFF` is ready to be staged for the combined preprint with `MUSTAR-HALF`.** All four findings from `REVIEW3.md` (**R3-1, R3-2, R3-3, R3-4**) are cleanly resolved on current bytes. No P0, P1, or P2 defects remain. Both independent checkers (`replay.py` and `independent.py`) are sound, all 20 `CHECKS.txt` rows pass with their expected exit codes (0 broken controls), `--selfcheck` has verified teeth against `independent.v3.py`, five new round-4 adversarial probes pass/refuse as required, and **no claim shrinks**. (Two non-blocking P3 prose nits in `RIGOR.md:207, 398` are noted in §6 for optional polish during preprint assembly.)

---

## 1. Resolution of `REVIEW3.md` Findings (R3-1 – R3-4)

| ID | Round-3 Finding | Status | Verification on Current Bytes |
|---|---|---|---|
| **R3-1 [P1]** | Swapped `lower`/`upper` in `hot_head` (`radius <= 0`, 1-ULP underestimate on odd-parity brackets) | **RESOLVED** | `independent.py:250-261` (`hot_enclosure`) sets `upper = -(dn[diff]+dn[hank])`, `lower = -(up[diff]+up[hank])`, asserts `lower <= upper`, computes `center = (lower+upper)//2` and `radius = np.maximum(upper-center, center-lower) >= 0` (`= ceil((upper-lower)/2)`), and asserts `radius >= 0`. Guaranteed `center - radius <= lower <= SC*F_ij(q) <= upper <= center + radius` on every off-diagonal entry (odd brackets included), verified at endpoints ($q = lo, hi$) and by `independent.py --selfcheck` (573,003 exact rational comparisons, exit 0). |
| **R3-2 [P1]** | False intermediate inequality $2A_j(r) - A_{j-m}(l) \ge A_m(r)$ in written `tail_gap` proof | **RESOLVED** | `independent.py:147-178` and `RIGOR.md:221-232` now prove the bound in two valid steps: first at a **fixed** $q \in [l, u]$, $2A_j(q) - A_{j-m}(q) = A_j(q) + \sum_{t=j-m+1}^j a_t(q) \ge A_j(q) \ge A_m(q)$, then passing to endpoints term-by-term ($A_m(q) \ge A_m(u)$, $a_{2j+1}(q) \le a_{2m+1}(l)$, $S_1(q) \le S_1(l)$, $S_{j+m+1}(q) \le S_{2m+1}(l)$). Certified integer `g` is unchanged. |
| **R3-3 [P2]** | Incomplete overflow / `NaN` / symmetry guards in `tail_penalty`, `head_radius`, `positive` | **RESOLVED** | `tail_penalty` (`independent.py:194-199`) asserts nonnegativity and guards `int(be.max()) * int(col.sum()) < 2**62` **before** `be @ col`; `head_radius` (`independent.py:214-220`) asserts `radius.dtype == np.int64` and `radius >= 0` and guards `int(np.abs(radius).max()) * int(h.sum()) < 2**62` **before** `@`; `positive` (`independent.py:308-336`) asserts `int64`, square, exact symmetry (`np.array_equal(A, A.T)`), and `np.all(np.isfinite(Lh))` **before** casting `Lh` to `int64`. |
| **R3-4 [P2/P3]** | Prose/docstring mismatches (`m=max(400,2k+1)`, stale docstring, "$A_i$ increasing in $q$", `RESULT.md` R2-5 typos) | **RESOLVED** | `RIGOR.md:191, 364`, `RESULT.md:208`, and `FIX2.md` now state `m = max(160, 2k+1)` (`NB = 160`); `independent.py:19-45` module docstring accurately describes the signed-interval enclosure; `A_i(q)` is stated as *decreasing* in $q$ (`independent.py:239`, `RIGOR.md:201, 227`); `RESULT.md:124, 153` fix the `crosscheck.v1.py` attribution and `180300/66011 = 2.73136`. |

---

## 2. `--selfcheck` Teeth Verification (Against `independent.v3.py`)

Loaded `independent.v3.py` directly by path and replayed its round-3 enclosure formula (`lower = -(dn+dn)`, `upper = -(up+up)`, `radius = upper - center`) on the 6 `SELFCHECK` windows (`independent.py:636-643`):
- **Entrywise failure on `independent.v3.py`:** `189,950 / 189,950` off-diagonal entries violate `lower <= upper`, `189,950 / 189,950` have `radius < 0`, and `189,950 / 189,950` violate `|SC*F(q_mid) - center| <= radius`, with a maximum excess of **`45,239.22`** integer units at scale $2^{17}$ (worst window $\lambda=10, \mu^*=1, R^2=9, r=3$).
- **Direct monkeypatch test:** Substituting `v3`'s enclosure into `independent.hot_enclosure` and invoking `independent.selfcheck()` fails immediately with `ValueError: selfcheck: lower exceeds upper`.
- **Current bytes:** `independent.py --selfcheck` exits `0` in `5.9s` after `573,003` exact rational entry comparisons across 6 windows $\times$ 3 interior $q$ values.

---

## 3. New Round-4 Adversarial Probes (5 New Probes)

In addition to `independent.py --adversarial` (exit 0) and the 5 round-3 probes, 5 **new** probes were run against the fixed `independent.py`:

| Probe | Target / Parameters | Exact Independent Check | Outcome |
|---|---|---|---|
| **R4-A (Guard teeth)** | Asymmetric `int64`, non-square `int64`, `float64`, negative `radius`, indefinite `int64` | Direct calls to `positive()` and `head_radius()` | All 4 invalid inputs raise `ValueError`; indefinite matrix returns `False` (**PASS**) |
| **R4-B (Small $\lambda$, $\mu^*/\lambda=2/3$)** | $(\lambda, \mu^*, R^2) = (3/2, 1, 1)$, $k=14$, $q_{\rm bad}=292046/61005649$ | 1200-mode unfolded exact form $= -1.9109 \times 10^{11} < 0$ ($a_0$ retained) | `independent.py` box & pt **Refused**; `replay.py` box & pt **Refused** (**PASS**) |
| **R4-C (Large $R^2, \mu^*$)** | $(\lambda, \mu^*, R^2) = (8, 12, 25)$, $k=9$, $q_{\rm bad}=13835322/40064209$ | 1200-mode unfolded exact form $= -1.0324 \times 10^{13} < 0$ ($a_0$ retained) | `independent.py` box & pt **Refused**; `replay.py` box & pt **Refused** (**PASS**) |
| **R4-D (Two-line mixture hot refusal)** | `counterexample-wide` mixture at $q=1/200$, $k=28$, box $[49/10000, 51/10000)$ | 1200-mode unfolded exact form $= -1.2455 \times 10^{13} < 0$ ($a_0$ retained) | `independent.py` `hot_head`+`positive` box & pt **Refused** (**PASS**) |
| **R4-E (Odd-parity endpoints)** | $(3, 2, 9/4)$ on $[0.0095, 0.0096)$, $m=160$, `12,524/25,440` odd brackets | `exact_head` at exact boundary endpoints $q = lo$ and $q = hi$ | **0 violations** of `|SC*F - center| <= radius` at both endpoints (**PASS**) |

---

## 4. Rerun of All 20 `CHECKS.txt` Commands

Every command in `CHECKS.txt` was re-run verbatim from `D:/dev/scratch/ceiling-20261118/C-LAMBDA-MU/COMMON-CUTOFF` via `UV_CACHE_DIR=D:/dev/.cache/uv uv run --no-project --with numpy --with scipy --with mpmath python -B <cmd>` (total wall time 269.0 s; zero exit-2 broken controls):

| # | Command | Exit | Time | Observed Outcome |
|---:|---|---:|---:|---|
| 1 | `replay.py` | **0** | 26.2s | `stored bounds.json verified without rewriting` |
| 2 | `replay.py --mutant sign` | **1** | 4.9s | Control passed; sign-flipped mask term refused |
| 3 | `replay.py --mutant spectrum` | **1** | 1.6s | Controls passed; Einstein not unstable at `q=1/100` |
| 4 | `replay.py --mutant tail` | **1** | 1.7s | Control passed; disabled `far_lump` refused |
| 5 | `replay.py --mutant coulomb` | **1** | 1.6s | Control passed; doubled Coulomb kills cold witness |
| 6 | `replay.py --mutant endpoint` | **1** | 1.3s | Control passed; cold witness refused at `q_hi` |
| 7 | `independent.py` | **0** | 48.3s | `bounds.json` fields agree; `independent verification ... OK` |
| 8 | `independent.py --selfcheck` | **0** | 5.9s | `6 windows x 3 interior q, 573003 exact rational entry comparisons ... OK` |
| 9 | `independent.py --adversarial` | **0** | 66.6s | All 3 REVIEW2 boxes & point boxes refused |
| 10 | `independent.py --mutant endpoint` | **1** | 5.1s | Refused hot cover on `[q_lo, q_ph)` (`K=16`) |
| 11 | `independent.py --mutant coulomb` | **1** | 2.0s | Refused doubled $\mu^*$ at `q=1/100` (`+3.415e13 >= 0`) |
| 12 | `independent.py --mutant spectrum` | **1** | 1.2s | Refused $p \to 1-p$ via second-moment guard |
| 13 | `independent.py --mutant receipt` | **1** | 39.6s | Refused shaved `C_E` bracket in `bounds.json` check |
| 14 | `structure.py` | **0** | 0.2s | 400 rational two-line spectra passed |
| 15 | `structure.py --mutant` | **1** | 0.2s | 36 perturbed statements refused |
| 16 | `structure.py --folded` | **0** | 1.8s | Folded matrix = display verified in 120/120 trials |
| 17 | `structure.py --folded --mutant` | **1** | 0.5s | Missing tail term detected in 120/120 trials |
| 18 | `crosscheck.py` | **0** | 18.2s | Direct even-sector eigenvalues match folded to float round-off |
| 19 | `crosscheck.py --mutant mirror` | **1** | 19.4s | Refused dropped mirror term |
| 20 | `crosscheck.py --mutant zshift` | **1** | 22.2s | Refused wrong $Z_n$ shift |

---

## 5. Claim Integrity & Per-Claim Status Labels

**Did any claim shrink?** **No.** `bounds.json` and `fixtures.json` are untouched; all 3 counterexample onset gains ($\ge 2.6\%, 29\%, 83\%$), all 7 Einstein $q_E$ and $C_E$ brackets, all 7 hot stability intervals $[q_{\rm hi}, q_{\rm ph})$, and the zero-Coulomb reference $C(1) \in [0.11461945, 0.11461957]$ stand intact without any weakening.

| Claim | Label | Basis |
|---|---|---|
| Reduction to $(R, \mu^*)$, Einstein transfer dominance $a_r^E \ge a_r$ (Jensen), exact folded stability-form Laplacian identity, and mechanism for failure of entrywise $a_r$ dominance at $\mu^* > 0$ | **PROVED** | Analytic proofs in `RIGOR.md` §2–§4, independently confirmed in exact rationals by `structure.py` (400 trials) and `structure.py --folded` (120 trials). |
| Three common-cutoff Einstein-optimality counterexamples at $\mu^*/\lambda \in \{2/3, 3/4, 1\}$ (`(3, 2, 1.5)`, `(2, 1.5, 2)`, `(4, 4, 2)`), all 7 `bounds.json` Einstein $q_E$ and $C_E$ brackets, and all 7 hot intervals $[q_{\rm hi}, q_{\rm ph})$ | **CERTIFIED** | Exact rational/integer computer-assisted certificates independently verified by two sound checkers (`replay.py` and `independent.py`) with 20/20 `CHECKS.txt` rows, `--selfcheck`, `--adversarial`, and 10 total independent adversarial probes passing. |
| Zero-Coulomb reference $C(1) \in [0.11461945, 0.11461957]$ (explicitly noted as distinct from $\mu^* = 1/10$, not a tie-in) | **CERTIFIED** *(upstream)* | `C-LAMBDA/brackets.json`, independently verified to 60-digit `mpmath` (`[0.114619454762, 0.114619569381]`). |
| Direct full-line fermionic Matsubara onsets ($T_{\rm mix}/T_E = 1.21, 2.92, 9.96$), band-doubling stability ($N=240\to480$), and small-$\mu^*$ control stability at $\mu^*/\lambda \in \{1/10, 1/2\}$ | **NUMERICAL** | Float64 `crosscheck.py` (independent discretization; certified chain does not depend on it). |
| Einstein optimality for $\mu^*/\lambda \le 1/2$ at a common cutoff | **OPEN** | Explicitly qualified as open in `RESULT.md` and `RIGOR.md` §7–§8. |

---

## 6. Non-Blocking P3 Prose Nits (Optional Polish for Preprint)

1. `RIGOR.md:207` and `FIX2.md:148` write `lower <= C - R and C + R <= upper` instead of `C - R <= lower` and `upper <= C + R` (the code in `independent.py:257, 689-690` has the exact right direction `(base - radius)[off] <= lower[off]` and `upper[off] <= (base + radius)[off]`).
2. `RIGOR.md:398` (§8 item 5) still attributes `crosscheck.v1.py`'s factor 2.6–7 discrepancy to a `(u,p)` unpack swap, whereas `RESULT.md:124` was updated to its four discretization bugs.

Neither nit affects code soundness, proofs, or certificates.

---

## 7. Combined Preprint Readiness

**Ready.** `COMMON-CUTOFF` meets the two-independent-sound-checkers bar and is ready to be staged for the combined preprint with `MUSTAR-HALF`.
