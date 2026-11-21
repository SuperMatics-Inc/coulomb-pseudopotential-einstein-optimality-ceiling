# Independent Delta Review of Section 8 (`CUTOFF-PAPER`, `REVIEW-S8.md`)

**Verdict: PASS-WITH-FIXES**

**Summary.** The Section 8 upgrade after `MUSTAR-HALF/REVIEW3.md` (`PASS`) is mathematically faithful, properly labelled, and passes all text-policy and clean-build checks. All 11 findings from the first review (`REVIEW.md` F1–F11) are cleanly resolved in `main.tex` and `CLAIMS.md`. Every statement in §8 carries the exact label assigned by `MUSTAR-HALF/REVIEW3.md`, all six analytic results (`lem:decomp`, `thm:twodelta`, `thm:nomask`, `thm:large`, `thm:cone`, `thm:asym`) faithfully restate `MUSTAR-HALF/RIGOR.md:31-128` with full hypotheses and no strengthened claims, all eight `CERTIFIED` brackets (`tab:half`, `tab:anchors`) are outward-rounded against `MUSTAR-HALF/bounds.json`, all 14 rows (168 cells) of `tab:phase` match `MUSTAR-HALF/RESULT.md:45-58` verbatim, the rewritten §8.3 (`sec:half:num`) phase reading is accurate and honest, the compiled 20-page PDF builds cleanly with 0 warnings/overfulls/undefined references, and all text-policy rules pass (0 em dashes, 10 en dashes all in compound names, 0 process/lane/path hits, exact disclosures and byline). Zero **P0** or **P1** findings remain; three **P2** factual precision items in the §8.1 Certification proof and one **P3** cross-section wording polish are listed below for quick cleanup before public release.

---

## 1. Per-Claim Label Audit (§8)

| Paper Statement / Location | Assigned Label in `main.tex` | Allowed Label (`MUSTAR-HALF/REVIEW3.md:13-15`) | Status |
|---|---|---|---|
| `thm:half`, `tab:half` (4 sub-$1/2$ counterexamples: $\lambda \in \{25.6, 26, 27, 28\}$, $\mu^*/\lambda \in [0.478602, 0.489]$) (`main.tex:665-770`) | `CERTIFIED` (`\certified`, `\textsc{certified}`) | `CERTIFIED` (`REVIEW3.md:13`) | **PASS** |
| `tab:anchors` (4 Einstein anchors at $\mu^*/\lambda \le 1/2$: $\lambda \in \{2, 3, 10, 20\}$) (`main.tex:776-803`) | `CERTIFIED` (`\textsc{certified}`) | `CERTIFIED` (`REVIEW3.md:13`) | **PASS** |
| `lem:decomp` (Exact finite-support decomposition) (`main.tex:815-846`) | `PROVED` (`\proved`) | `PROVED` (`REVIEW3.md:14`) | **PASS** |
| `thm:twodelta` (Two-line reduction at fixed mask and repulsion on $\mathcal{D}_0$) (`main.tex:848-877`) | `PROVED` (`\proved`) | `PROVED` (`REVIEW3.md:14`) | **PASS** |
| `thm:nomask` (Exact optimality when $4R^2 < q_{\mathrm{ph}}(\lambda)$) (`main.tex:883-907`) | `PROVED` (`\proved`), conditional on zero-repulsion theorem in hypothesis | `PROVED` (conditional on zero-Coulomb theorem, `REVIEW3.md:14`) | **PASS** |
| `thm:large` (Large coupling $\lambda \ge 4R^2 + 1$ at fixed $R$) (`main.tex:914-935`) | `PROVED` (`\proved`), invokes `thm:nomask` | `PROVED` (`REVIEW3.md:14`) | **PASS** (see D4.3) |
| `thm:cone` (Single-mode $k=1$ cone monotonicity for $\mu^* \le 1 + a_1(q;p)$ and sharp failure) (`main.tex:937-995`) | `PROVED` (`\proved`) | `PROVED` (`REVIEW3.md:14`) | **PASS** |
| `thm:asym` (Parameter-free positivity for $q \ge 4\lambda$) (`main.tex:997-1024`) | `PROVED` (`\proved`) | `PROVED` (`REVIEW3.md:14`) | **PASS** |
| `sec:half:num`, `tab:phase`, $r_*(\lambda, R)$, $r_{\min} \approx 0.4785$ at $\lambda \approx 25.58$, $\lambda_{\mathrm{crit}} \approx 25.55$, $k \in \{1,2,3,4\}$ scan, $\lambda=152$ $k=1$ probe, direct $N=600$ ratios (`main.tex:1034-1142`, `tab:half` last col) | `NUMERICAL` (`\textsc{numerical}`) | `NUMERICAL` (`REVIEW3.md:15`) | **PASS** |

---

## 2. Detailed Audit of Tasks (2)–(6)

- **Task (2) — Faithfulness to `MUSTAR-HALF/RIGOR.md:31-128`:** Checked line by line.
  - `lem:decomp` (`main.tex:815-846`): exact match to `RIGOR.md:31-47` (finitely supported $h$, both forms of $L_j(h)$, $|L_j(h)| \le 5\|h\|_2^2$, $L_j(h)=0$ for $j \ge 2n$).
  - `thm:twodelta` (`main.tex:848-877`): exact match to `RIGOR.md:53-59` (form core $\mathcal{D}_0$, Richter–Rogosinski / Markov–Krein on $(u, \Phi_{h,q}(u))$, $0 < u_1 \le 1 \le u_2$).
  - `thm:nomask` (`main.tex:883-907`): exact match to `RIGOR.md:60-65` (explicit assumption of zero-repulsion strict optimality, strict $4R^2 < q_{\mathrm{ph}}(\lambda)$, strictness remark after proof).
  - `thm:large` (`main.tex:914-935`): exact match to `RIGOR.md:66-75` ($\lambda \ge 4R^2+1$, $q_* = \lambda-1$, $v_\varepsilon = e_0 + \varepsilon e_1$, reduction to `thm:nomask`).
  - `thm:cone` (`main.tex:937-995`): exact match to `RIGOR.md:81-115` (window $\frac{4}{9}R^2 \le q < 4R^2$, pointwise condition $\mu^* \le 1 + a_1(q;p)$, unconditional corollaries $\mu^* \le 1$ and $\lambda \le 2$ with $\mu^*/\lambda \le 1/2$, Part (ii) sharp failure with $\tilde D_{p,1}-\tilde D_{p,0} = 2+2a_1-2\mu^*$ and soft-mode limit).
  - `thm:asym` (`main.tex:997-1024`): exact match to `RIGOR.md:117-131` ($q \ge 4\lambda$, row margin $d_i - 2\sum_{j>i} a_j \ge 1 - \pi^2/12 > 1/6$, Schur's test).
- **Task (3) — Numbers, brackets, `tab:phase`, and `CHECKS.txt` margins:**
  - All 8 `C_E` brackets (`tab:half` and `tab:anchors`) verified to 60-digit `mpmath` precision against both `MUSTAR-HALF/bounds.json` and $\sqrt{q}/(2\pi\sqrt{\lambda})$: all 8 are strictly outward-rounded on both endpoints.
  - All 4 `q_mix/q_hi` lower bounds (`1.0476, 1.0379, 1.2171, 1.1893`) and temperature-gain lower bounds (`2.353%, 1.878%, 10.326%, 9.055%`) verified as exact downward truncations of the certified ratios; all 4 `p1*u1 + p2*u2 = 1` identities verified exact in $\mathbb{Q}$.
  - `tab:phase` (`main.tex:1074-1118`): automated cell-by-cell comparison against `MUSTAR-HALF/RESULT.md:45-58` across all 14 rows × 12 columns = **0 mismatches**.
  - Box counts (`2638, 1444, 539, 239` in first verifier; `2843, 1504, 541, 239` in second verifier; `12, 18, 10, 17` for anchors) and second-verifier smallest margins (`0.0697854, 0.244918, 0.504196, 45.2602`) match `bounds.json` and `CHECKS.txt` verbatim (see D1–D3 for small proof-text inaccuracies around head size, margin units, and command/mutant counts).
- **Task (4) — Rewritten §8.3 (`sec:half:num`) phase reading:** Accurate and non-overclaiming. Distinguishes $\infty$ cells ("unbeaten on the grid, which is weaker than optimality", upgraded to a proof only where $4R^2 < q_{\mathrm{ph}}(\lambda)$ by `thm:nomask`), explains that $\inf_R = 0.5000$ rows are bounded by the grid's smallest scanned ratio, correctly locates $r_{\min} \approx 0.4785$ at $\lambda \approx 25.58$, $\omega_c/\OmE \approx 3.36$, and cleanly labels the $k=1$ $\lambda=152$ probe and direct $N=600$ ratios as `NUMERICAL`.
- **Task (5) — Text policy (verified on extracted text of rebuilt 20-page PDF):**
  - Exact sentence `"This preprint has not been peer reviewed."`: present (1 occurrence).
  - AI disclosure: present (1 occurrence).
  - Byline `Davis Rens`, `SuperMatics Inc.`, `ORCID 0000-0001-5839-5197`: present.
  - Em dashes (`U+2014`): `0`.
  - En dashes (`U+2013`): `10`, all inside compound names (`Migdal–Eliashberg` ×4, `Richter–Rogosinski`, `Markov–Krein`, `Birman–Schwinger`, `Krein–Rutman`, `Kiessling–Altshuler–Yuzbashyan` ×2).
  - Process/agent/lane/machine/path strings (`provisional`, `under repair`, `pending`, `being finished`, `currently sound`, `lane`, `scratch`, `D:/`, `C:/`, `MIKUSSY`, `REVIEW`, `FIX-INDEP`, script/JSON filenames): `0` occurrences.
- **Task (6) — Clean Tectonic rebuild:** `D:/dev/tools/tectonic/tectonic.exe -X compile main.tex --keep-logs` in `C:/t/CutoffDelta` exited `0` (20 pages, 0 overfull, 0 underfull, 0 undefined references, 0 LaTeX warnings). Temp directory deleted after verification.

---

## 3. Findings (P0–P3)

Zero **P0** and zero **P1** findings.

### D1 [P2] — First verifier hot head size misstated as $m=200$ instead of $n=240$
- **Location:** `main.tex:724-725`
- **Issue:** The Certification proof states "with integer scale $2^{30}$ and head $m=200$ in the first verifier and integer scale $2^{22}$ and head $m=200$ in the second". In fact, `MUSTAR-HALF/fixtures.json` sets `size_hot: 240` for all eight instances, and `MUSTAR-HALF/replay.py:250` runs `Folded(int(data['size_hot']))`, so the first verifier uses head size **$n=240$** (confirmed in `MUSTAR-HALF/REVIEW3.md:45`), while only the second verifier uses $m=200$.
- **Fix:** Replace `head $m=200$ in the first verifier` with `head $n=240$ in the first verifier`.

### D2 [P2] — Margin units in the Certification proof are unlabelled (`SC` units vs. exact integer / folded-form units)
- **Location:** `main.tex:736-740`, `main.tex:757`
- **Issue:** Lines 736–739 state "Every certified box carries a strictly positive exact integer margin... and the smallest margins of the second verifier are $0.0697854$, $0.244918$, $0.504196$ and $45.2602$". Per `MUSTAR-HALF/REVIEW3.md:65` (Finding N3) and `independent.py:333, 400`, those printed numbers are `float(gap.min()) / factor` in the second verifier's integer-scale (`SC = 2^22`) units, not raw integers and not folded-form units ($0.0697854$ in `SC` units is $1.664\times 10^{-8}$ in folded-form units). Similarly, on line 757, $x^{\!\top}\Fcal x = -85.47\times 10^{12}$ is evaluated on the `SC` integer scale (`CHECKS.txt:26`: `x^T SC*F(q_bad)x = -85.47e12`).
- **Fix:** State explicitly on line 739 that the four quoted margins are in the second verifier's integer-scale ($2^{22}$) units (each backed by a strictly positive integer Gershgorin gap), and note on line 757 that $x^{\!\top}\Fcal x$ is on the same integer scale.

### D3 [P2] — Minor count and wording inaccuracies in the Certification proof ("twenty" commands, `--mutant all`, "sixth self-test")
- **Location:** `main.tex:743-751`, `main.tex:762`, `main.tex:766-767`
- **Issue:**
  1. Line 766 says "All twenty recorded commands of this section return their stated exit codes", whereas `MUSTAR-HALF/CHECKS.txt` records **21** `$RUN` commands (6 `replay.py`, 11 `independent.py`, 2 `structure.py`, 2 `phase_scan.py`).
  2. Line 750 says "each program also refuses when all of its mutants are run together", whereas only `structure.py` has a combined `--mutant` / `--mutant all` mode (`replay.py` and `independent.py` run one named mutant per invocation).
  3. Line 762 says "A sixth self-test recomputes the entries of the head enclosure...", but no first five self-tests are numbered in the preceding text.
- **Fix:** Change `twenty` $\to$ `twenty-one` on line 766; narrow line 750 to say the structural checker also refuses when all three of its mutants are run together; change `A sixth self-test` $\to$ `A self-test` on line 762.

### D4 [P3] — Minor cross-section wording polish
- **Location:** `main.tex:48`, `main.tex:812`, `main.tex:1169`, `main.tex:1177`
- **Issue:**
  1. `main.tex:48` (Abstract) says "certified by the same two verifiers", whereas `main.tex:1176` and `main.tex:1239` accurately explain that §8 uses its own independent pair of exact verifiers in the same two roles as §5.
  2. `main.tex:1169` (§9 item 4) still reads "the contribution here is the positive-pseudopotential common-cutoff question and its certified answer above one half", a v1 phrasing predating the §8 upgrade.
  3. `main.tex:812` and `main.tex:1177` state that "Only Theorem~\ref{thm:nomask} uses a result from outside this paper"; because Theorem~\ref{thm:large} applies Theorem~\ref{thm:nomask}, it inherits that dependency.
- **Fix:** Update line 48 to `certified by a second pair of independent exact verifiers in the same two roles`; update line 1169 to `its certified answers above and below one half`; update lines 812 and 1177 to note `Theorem~\ref{thm:nomask} (and Theorem~\ref{thm:large}, which applies it)`.

---

## 4. Verification Commands and Exit Codes

All temporary artifacts were created under `C:/t/CutoffDelta` and deleted at the end of the review.

| Command | Exit Code | Key Output |
|---|---:|---|
| `D:/dev/tools/tectonic/tectonic.exe -X compile main.tex --keep-logs` (clean copy in `C:/t/CutoffDelta`) | `0` | 20 pages, 211.17 KiB; `grep -nE "Overfull\|Underfull\|Undefined\|Warning\|Error\|!!" main.log` returned `NO_WARNINGS_IN_LOG` |
| `UV_CACHE_DIR=D:/dev/.cache/uv uv run --no-project --with mpmath --with pypdf python -B C:/t/CutoffDelta/verify_delta.py` | `0` | 20 pages, 0 em dashes, 10 en dashes (all in compound names), 0 forbidden process/path hits, all required disclosures present; 8/8 `C_E` brackets strictly outward-rounded; 4/4 `q_mix/q_hi` and temperature gains verified; `tab:phase` 14/14 rows (0 mismatches vs `RESULT.md`) |
| `grep` / `nl` audit of `MUSTAR-HALF/replay.py`, `structure.py`, `CHECKS.txt`, and `main.tex` | `0` | Confirmed `size_hot = 240` in `fixtures.json`/`replay.py`, 21 `$RUN` commands in `CHECKS.txt`, `structure.py` `--mutant all`, and exact line numbers for D1–D4 |
