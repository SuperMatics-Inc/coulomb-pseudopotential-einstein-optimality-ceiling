# Independent Preprint Review

**Verdict: PASS-WITH-FIXES**

**Summary.** The underlying `common-cutoff` certificates, structural theorems, bibliography DOIs/titles, $C_\infty$ attribution, and Tectonic build (`0` overfull/underfull boxes, `0` undefined references) are sound, and the prose is clear and journal-grade. However, the draft cannot be released as-is due to **three P0 defects** in `main.tex` (an inverted definition of $k_{\mathrm B} T_{\mathrm{lin}}$, an extraneous $\sqrt{\lambda}$ factor in Corollary 4.4, and inward-rounded $C_E$ endpoints across all seven rows of Tables 1–2) and **four P1 defects** (wrong E1 decimal weights in Table 1, a garbled copy-paste from `univglue` in §4.2, a reversed sign step in the empty-mask proof, and process language in Section 8 of the PDF). All defects have discrete, localized fixes requiring no recomputation of certificates.

---

## 1. Per-Claim Verification and Allowed Labels

| Paper Claim / Location | Source | Review Status | Allowed Label |
|---|---|---|---|
| Theorem 3.1 (`thm:reduce`, `main.tex:193-204`): reduction to $(\lambda, R^2, \mu^*)$ at fixed $(\lambda, M)$ and common $\omega_c$ | `common-cutoff/RIGOR.md:28-38`, `REVIEW4.md:76` | Matches source; proof sound | **PROVED** |
| Lemma 4.1 (`lem:jensen`, `main.tex:227-239`): Jensen dominance $a_r(q) \le a_r^{\mathrm E}(q)$ with strictness for $p \ne \delta_1$ | `common-cutoff/RIGOR.md:40-62`, `REVIEW4.md:76` | Matches source; proof sound | **PROVED** |
| Lemma 4.2 (`lem:laplace`, `main.tex:246-267`): folded Laplacian identity $\mathcal F_0(h)$ | `common-cutoff/RIGOR.md:83-116`, `REVIEW4.md:76` | Matches source; independently verified in 30 exact rational trials (max error `0`) | **PROVED** |
| Proposition 4.3 (`prop:rank`, `main.tex:275-287`): rank-one Coulomb block $2\mu^*(\sum_{i<k} h_i)^2$ | `common-cutoff/RIGOR.md:117-131`, `REVIEW4.md:76` | Matches source; proof sound | **PROVED** |
| Corollary 4.4 (`cor:value`, `main.tex:289-299`): ceiling value Coulomb robustness | `common-cutoff/RIGOR.md:117-131`, `univglue`, `finiteband` | **FAILS as written (F2)**: extraneous $\sqrt{\lambda}$ in $C_\infty\sqrt{\lambda M}$; **PROVED** once corrected to $C_\infty\sqrt{M}$ | **PROVED** *(after F2 fix)* |
| Empty-mask observation (`main.tex:346-358`): strict Einstein optimality when $4R^2 < q_{\mathrm{ph}}(\lambda)$ | Derived in this paper | Conclusion true, **proof step broken (F6)**: eq. (10) cannot preserve indefiniteness; fix via empty mask on $(4R^2, q_{\mathrm{ph}})$ | **PROVED** *(after F6 fix)* |
| Large-$q$ stability observation (`main.tex:360-377`): $\mathcal F \succeq (1-\pi^2/12)I \succ \frac16 I$ for $q \ge 4\lambda$ | Derived in this paper | Re-derived and verified in 30 exact rational trials ($L_j(h) \ge -2\|h\|^2$, $1-\pi^2/12 = 0.177533 > 1/6$) | **PROVED** |
| Theorem 5.1 & Table 1 (`thm:cert`, `tab:cex`, `main.tex:383-443`): three counterexamples E1–E3 at $\mu^*/\lambda \in \{2/3, 3/4, 1\}$, gains $\ge 2.59\%, 29.09\%, 82.57\%$ | `common-cutoff/bounds.json`, `fixtures.json`, `RESULT.md:26-28`, `REVIEW4.md:78` | Exact rationals, gains, and instability/stability signs independently confirmed; **display errors in Table 1 (F3, F4)** | **CERTIFIED** *(after F3, F4 fixes)* |
| Section 6 & Table 2 (`tab:brackets`, `main.tex:515-577`): seven Einstein $q_E$ and $C_E$ brackets, box counts `19,36,37,10,12,14,11` | `common-cutoff/bounds.json`, `CHECKS.txt` Note 2, `REVIEW4.md:78` | $q_E$ brackets and box counts match source; **all 7 $C_E$ brackets rounded inward (F3)**; hot-endpoint caption imprecise (**F8**) | **CERTIFIED** *(after F3, F8 fixes)* |
| Zero-repulsion calibration $C(1) \in [0.11461945, 0.11461957]$ and monotone chain $C(1), C(3), C(10), C_\infty$ (`main.tex:558-576`) | `C-LAMBDA/brackets.json`, `C-LAMBDA/RESULT.md:18-25`, `REVIEW4.md:80` | Independently verified to 60 digits in `mpmath`; matches upstream | **CERTIFIED** *(upstream)* |
| Section 7 & Table 3 (`sec:num`, `tab:direct`, `main.tex:578-618`): direct full-line onsets, $4.4\times 10^{-16}$ agreement, band doubling, small-$\mu^*$ controls | `common-cutoff/RESULT.md:130-148`, `RIGOR.md:396-405`, `REVIEW4.md:82` | Matches source and properly labelled | **NUMERICAL** |
| Section 8 & Table 4 (`sec:half`, `tab:half`, `main.tex:619-683`): sub-$1/2$ instances and anchors | `mustar-half/RESULT.md`, `bounds.json`, `REVIEW.md` | Correctly labelled **NUMERICAL** and does not overclaim certification; **violates paper rule against process language in PDF (F7)** | **NUMERICAL** *(after F7 fix; delta review pending)* |
| Sections 9–10 (`sec:not`, `sec:open`, `main.tex:684-753`): scope disclaimers and open status for $\mu^*/\lambda \le 1/2$ | `common-cutoff/RIGOR.md:359-405`, `REVIEW4.md:84` | Accurate scope; no measured $T_c$ or material claims | **OPEN** / Scope |

---

## 2. Findings (P0–P3)

### F1. [P0] Inverted definition of linear onset $k_{\mathrm B} T_{\mathrm{lin}}$
- **Location:** `main.tex:174`
- **Issue:** The text writes `and the linear onset is $\kb\Tlin=\sup\{\kb T:\Fcal\succeq0\}$.` Because $\mathcal F \succeq 0$ holds for all sufficiently *high* temperatures (indeed for all $q \ge 4\lambda$), $\sup\{k_{\mathrm B} T : \mathcal F \succeq 0\} = +\infty$. This directly contradicts the next sentence (`main.tex:174-176`), which correctly states that $k_{\mathrm B} T_{\mathrm{lin}}$ is the supremum of temperatures at which the linearized form has a negative direction.
- **Fix:** Replace `$\kb\Tlin=\sup\{\kb T:\Fcal\succeq0\}$` with `$\kb\Tlin=\sup\{\kb T:\Fcal\not\succeq0\}$` (or equivalently `$\inf\{\kb T:\Fcal\succeq0\}$`).

### F2. [P0] Extraneous $\sqrt{\lambda}$ factor in Corollary 4.4 (`cor:value`)
- **Location:** `main.tex:291`
- **Issue:** Corollary~\ref{cor:value} states `Every spectrum has $\kb\Tlin\le C(\lambda)\sqrt M\le C_\infty\sqrt{\lambda M}$.` Since $M = \lambda\Omega_E^2$ already incorporates $\lambda$ and eq. \eqref{eq:ceiling} (`main.tex:218`) has $C(\lambda)\Uparrow C_\infty$, the $\lambda$-independent ceiling is $C_\infty\sqrt{M}$, not $C_\infty\sqrt{\lambda M}$. Including $\sqrt{\lambda}$ double-counts the coupling factor and does not follow from \eqref{eq:ceiling}.
- **Fix:** Change `$\kb\Tlin\le C(\lambda)\sqrt M\le C_\infty\sqrt{\lambda M}$` to `$\kb\Tlin\le C(\lambda)\sqrt M\le C_\infty\sqrt M$`.

### F3. [P0] All seven certified $C_E$ brackets are rounded inward, violating outward-rounding claims
- **Location:** `main.tex:398, 400, 402` (Table 1), `main.tex:532-538` (Table 2), `main.tex:558, 560` (prose), `CLAIMS.md:75`
- **Issue:** Both table captions assert that the displayed 8-decimal $C_E$ brackets are outward rounded from the exact rationals in `common-cutoff/bounds.json`. In fact, all seven lower endpoints were rounded to nearest (upward) instead of floored, so every displayed lower bound exceeds both the certified rational in `bounds.json` and the exact $\sqrt{q_{\mathrm{lo}}}/(2\pi\sqrt{\lambda})$. For row A3, the upper endpoint `0.06215199` is also rounded inward (`0.06215199214... > 0.06215199`).
- **Evidence (exact vs displayed):**
  - E1: exact `[0.008371408803, 0.008956148933]` $\to$ outward 8-dec `[0.00837140, 0.00895615]` (displayed `0.00837141` is inward).
  - E2: exact `[0.003376186186, 0.006164044441]` $\to$ outward 8-dec `[0.00337618, 0.00616405]` (displayed `0.00337619` is inward).
  - E3: exact `[0.001278203460, 0.004358637623]` $\to$ outward 8-dec `[0.00127820, 0.00435864]` (displayed `0.00127821` is inward).
  - A1: exact `[0.016843375974, 0.017434550494]` $\to$ outward 8-dec `[0.01684337, 0.01743456]` (displayed `0.01684338` is inward).
  - A2: exact `[0.088327408772, 0.088685155918]` $\to$ outward 8-dec `[0.08832740, 0.08868516]` (displayed `0.08832741` is inward).
  - A3: exact `[0.062050019971, 0.062151992135]` $\to$ outward 8-dec `[0.06205001, 0.06215200]` (**both** displayed endpoints `0.06205002` and `0.06215199` are inward).
  - A4: exact `[0.107473787201, 0.107532693090]` $\to$ outward 8-dec `[0.10747378, 0.10753270]` (displayed `0.10747379` is inward; `0.10753271` is outward by an extra ULP).
- **Fix:** Replace the seven $C_E$ brackets in Table 1, Table 2, `main.tex:558, 560`, and `CLAIMS.md:75` with the outward-rounded 8-decimal enclosures listed above (or match the 8-significant-digit outward values of `common-cutoff/RESULT.md:26-28, 55-58`).

### F4. [P1] Wrong decimal weights for E1 spectrum in Table 1
- **Location:** `main.tex:399`
- **Issue:** Table 1 row E1 prints `$0.98504$ at $0.1$, $0.01496$ at $60$` (5 decimals, off in the 4th decimal place). The exact rational weights certified in `bounds.json` and stated in the caption are $590/599 = 0.984974958\ldots$ and $9/599 = 0.015025041\ldots$.
- **Fix:** Replace `$0.98504$ at $0.1$, $0.01496$ at $60$` with `$0.984975$ at $0.1$, $0.015025$ at $60$` (6 decimals, matching the caption and rows E2–E3).

### F5. [P1] Garbled "explicit obstruction" copied from `univglue`
- **Location:** `main.tex:304-308`
- **Issue:** The text writes: `The explicit obstruction is short: if $R>1$ then $4R^2/(R^2+j^2)$ dominates $4/(1+j^2)$ for the whole near zone, yet its folded $(0,0)$ entry is $4/(R^2+1)<2$, so an entrywise statement about transfers cannot be read as a statement about the $(0,0)$ entry of the form.` This sentence was copied verbatim from `UNIV-GLUE/release-bundle/main.tex:55`, where $R$ was a Lorentzian width parameter and "folded $(0,0)$ entry" meant $P_{00} = K_0 - K_1 = 4 - 4R^2/(R^2+1) = 4/(R^2+1) < 2$. In the present paper, $R$ is already fixed as the cutoff ratio $R = \omega_c/\Omega_E$, $P = D - H$ is never defined, and the $(0,0)$ entry of $\mathcal F$ in \eqref{eq:form} is $F_{00} = 1 - a_1 + 2\mu^*[0<k]$, which is $1 - 4R^2/(R^2+1) < -1$, not $4/(R^2+1) < 2$.
- **Fix:** Delete the copied sentence and replace it with an obstruction in this paper's own variables (e.g., comparing $F_{ii} = 2i+1 + 2A_i - a_{2i+1} + 2\mu^*[i<k]$, where increasing $a_r$ raises the diagonal $+2A_i$ while lowering the off-diagonal $-a_{|i-j|}-a_{i+j+1}$, or directly referencing Remark~\ref{rem:mech}).

### F6. [P1] Reversed sign argument in the empty-mask observation
- **Location:** `main.tex:355-356`
- **Issue:** In the empty-mask observation ($4R^2 < q_{\mathrm{ph}}(\lambda)$), the text writes: `while the Einstein form is indefinite below $q_{\rm ph}$ and stays indefinite at $\muS>0$ by \eqref{eq:rank}.` Equation \eqref{eq:rank} adds the *positive semidefinite* term $2\mu^*(\sum_{i<k} h_i)^2$, which raises the form and cannot preserve indefiniteness. The actual reason the Einstein onset remains $q_{\mathrm{ph}}(\lambda)$ is that $4R^2 < q_{\mathrm{ph}}(\lambda)$ is a strict inequality, so $k(q,R) = 0$ (empty mask, $\mathcal F = \mathcal F_0$) on the entire open interval $(4R^2, q_{\mathrm{ph}}(\lambda))$ strictly below $q_{\mathrm{ph}}(\lambda)$, where the zero-repulsion Einstein form is indefinite.
- **Fix:** Replace `while the Einstein form is indefinite below $q_{\rm ph}$ and stays indefinite at $\muS>0$ by \eqref{eq:rank}` with `while on the nonempty open interval $(4R^2,q_{\rm ph}(\lambda))$ the mask is still empty, so $\Fcal=\Fcal_0$ and the Einstein form remains indefinite arbitrarily close to $q_{\rm ph}(\lambda)$`.

### F7. [P1] Process language in the PDF (`provisional`, `is being finished`, `expected to be replaced or withdrawn`)
- **Location:** `main.tex:51, 97, 110, 619, 621-624, 655, 666-668, 681, 693, 711, 732, 769`
- **Issue:** Paper rules prohibit process language like "under repair" or "pending review" in the PDF, and `BUILD.md:45` / `CLAIMS.md:14` state that the provisional status lives only in `CLAIMS.md` and never in the PDF. However, `main.tex` contains:
  - `main.tex:666-668`: `Only one of the two exact verifiers of Section~\ref{sec:cert} is currently sound for these instances; the second, whose hot device had to be repaired as described in Section~\ref{sec:cert}, is being finished.`
  - `main.tex:623-624`: `Every statement here is expected to be replaced by a certified statement or withdrawn.`
  - 11 occurrences of `provisional`/`Provisional` in the PDF (`main.tex:51, 97, 110, 619, 621, 655, 681, 693, 711, 732, 769`).
- **Fix:** Remove all process/repair-status phrasing ("provisional", "currently sound", "is being finished", "expected to be replaced ... or withdrawn") from `main.tex`. Frame Section 8 cleanly as a separate **numerical** section (e.g., `\section{Below one half: numerical evidence}`), stating neutrally that these four instances are reported as `NUMERICAL` rather than `CERTIFIED` because they do not carry the two-independent-verifier certificate required by Section 5.

### F8. [P2] Imprecise description of hot-interval right endpoints
- **Location:** `main.tex:544-546` (Table 2 caption), `CLAIMS.md:94`
- **Issue:** Table 2's caption states: `The right endpoint is truncated inside the certified zero-repulsion crossing $q_{\rm ph}(\lambda)$, beyond which Corollary~\ref{cor:value} supplies stability with no further computation.` If the hot interval stopped *inside* (strictly below) $q_{\mathrm{ph}}(\lambda)$, there would be an uncertified gap up to $q_{\mathrm{ph}}(\lambda)$. In both `replay.py:194-200` and `independent.py:509-515`, the actual certified hot interval runs up to the exact *upper* endpoint $q_{\mathrm{ph}}^{\mathrm{hi}}(\lambda) \ge q_{\mathrm{ph}}(\lambda)$ from `C-LAMBDA/brackets.json` (no gap); Table 2 merely prints 6-significant-digit rounded values of $q_{\mathrm{ph}}^{\mathrm{hi}}(\lambda)$ (which happen to round down for $\lambda=1,2,3$ and up for $\lambda=4,10$).
- **Fix:** Reword to: `The right endpoint shown is a six-digit display of the exact certified upper endpoint $q_{\rm ph}^{\rm hi}(\lambda)\ge q_{\rm ph}(\lambda)$ of the zero-repulsion bracket, beyond which Corollary~\ref{cor:value} supplies stability with no gap.` (Alternatively, print outward-rounded upper endpoints.)

### F9. [P2] Dimension mismatch in normal-diagonal shorthand
- **Location:** `main.tex:154`
- **Issue:** Writes `With the normal diagonal $D_n=Z_n|\omega_n|=|\omega_n|+a_0+2\sum_{j=1}^{i(n)}a_j$`, which adds energy $|\omega_n|$ to dimensionless $a_j$. In `main.tex:158` and eq. \eqref{eq:quotient}, the matrix is written in dimensionless units of $\pi k_{\mathrm B} T$ where $d_i = |2i+1|$.
- **Fix:** Write `$D_n=Z_n|\omega_n|/(\pi\kb T)=|2n+1|+a_0+2\sum_{j=1}^{i(n)}a_j$` (matching `common-cutoff/RIGOR.md:69`).

### F10. [P2] Inaccuracies and line-number drift in `CLAIMS.md`
- **Location:** `CLAIMS.md:14, 40, 57, 75, 85, 90-142`
- **Issue:**
  1. `CLAIMS.md:57` summarizes the empty-mask observation as `if 4R^2 < q_ph(lambda) the mask contains only the fold i=0; for a single-line mask the Einstein form is h_0^2+2mu* h_0^2 plus a positive semidefinite difference term`, which is mathematically false (when $q > 4R^2$, the mask is empty, $k=0$, not $k=1$) and contradicts `main.tex:346-358`.
  2. `CLAIMS.md:40` misprints the folded matrix identity as `F_ij = (2i+1) delta_ij - a_{|i-j|} + 2A_i delta_ij - 2A_min + mu* 1_{i<k}1_{j<k}` (missing `-a_{i+j+1}`, spurious `-2A_min`, missing factor `2` on `mu*`).
  3. `CLAIMS.md:85` cites `common-cutoff/bounds.json` for box counts `19, 36, 37` and `10, 12, 14, 11`. Those are `independent.py`'s box counts (`CHECKS.txt` Note 2); `bounds.json` stores `replay.py`'s counts (`18, 36, 37, 10, 18, 14, 11`).
  4. `CLAIMS.md:75` repeats the inward-rounded $C_E$ brackets (F3), `CLAIMS.md:14` claims `PROVISIONAL` is never in the PDF (F7), and section line ranges from §6 onward are shifted by 5 lines (`sec:brackets` is `515-577`, `sec:num` is `578-618`, `sec:half` is `619-683`, `sec:not` is `684-716`, `sec:open` is `717-753`).
- **Fix:** Update `CLAIMS.md` at the listed lines to match the corrected `main.tex` and exact source citations.

### F11. [P3] Minor typography and phrasing nits
- **Location:** `main.tex:546-548, 743`
- **Issue:**
  1. `main.tex:743` writes `Migdal-Eliashberg` with a hyphen instead of `Migdal--Eliashberg` (used on lines 39, 61, 120).
  2. `main.tex:546-548` writes `for the three rows above them` (referring to E1–E3 in Table 2); naming `E1--E3` (or `E1, E2 and E3`, avoiding an en dash outside compound names) and `A1, A2, A3 and A4` is clearer.
- **Fix:** Change `Migdal-Eliashberg` to `Migdal--Eliashberg` on line 743, and name the row labels explicitly in Table 2's caption.

---

## 3. Paper Rules, Bibliography, and Prose Audit

| Check | Result | Details |
|---|---|---|
| Em dashes (`U+2014`, `---`) | **PASS** | `0` occurrences in `main.tex` and rebuilt `main.pdf`. |
| En dashes (`U+2013`, `--`) | **PASS** | `5` occurrences in rebuilt `main.pdf`, all in compound names (`Migdal–Eliashberg` $\times 3$, `Kiessling–Altshuler–Yuzbashyan` $\times 2$). |
| Exact non-peer-review sentence | **PASS** | `This preprint has not been peer reviewed.` present once (`main.tex:759`, `main.pdf`). |
| AI disclosure | **PASS** | Present (`main.tex:756-757`): `AI agents generated the proofs, code and drafts under D. Rens' direction, and separate AI agents carried out the independent reviews.` |
| Byline & ORCID | **PASS** | `Davis Rens`, `SuperMatics Inc.`, `ORCID 0000-0001-5839-5197` (`main.tex:32`). |
| No record/agent/machine/path names | **PASS** | `0` occurrences of record, machine, or file paths; `agent` occurs only in the AI disclosure. |
| No process language in PDF | **FAIL (F7)** | `is being finished`, `currently sound`, `expected to be replaced ... or withdrawn`, and 11 occurrences of `provisional`/`Provisional` appear in `main.pdf`. |
| Model $T_{\mathrm{lin}}$ only; no measured $T_c$ or materials | **PASS** | Strictly model $T_{\mathrm{lin}}$; explicit disclaimers in Abstract, §2, §9, and Data availability. |
| Bibliography DOIs, titles, $C_\infty$ attribution | **PASS** | All 14 entries in `refs.bib` verified against released workspace bibliographies (`PUBLISH/RESULT.md`, `PUBLISH/anisosharp/repo/paper/refs.bib`, `MASSIVE/CAPSTONE-PAPER/refs.bib`). $C_\infty = 0.18272624777232952$ is accurately attributed to `univglue`/`anisosharp`/`gamma`/`finiteband` (not `optimum`). |
| Clean Tectonic rebuild (temp copy) | **PASS** | Exit `0`, 13 pages, `0` overfull boxes, `0` underfull boxes, `0` undefined references/citations. |
| Prose quality | **PASS** | Clear, restrained, human, journal-grade prose (subject to fixing F5 and F7). |

---

## 4. Commands Executed and Exit Codes

All temporary artifacts were placed in `<temporary>/` and removed at completion.

| # | Command | Exit | Key Output |
|---:|---|---:|---|
| 1 | `tectonic -X compile main.tex --keep-logs` (in `<temporary>/`) | `0` | 13 pages, `0` overfull/underfull, `0` undefined references/warnings |
| 2 | `uv run --no-project --with mpmath python -B <temporary>/verify_paper.py` | `0` | Verified all `common-cutoff`, `C-LAMBDA`, and `mustar-half` brackets/gains; detected F3 (7 inward-rounded $C_E$ rows), F4 (`590/599 = 0.984975`), and F7 (11 `provisional` + 4 process-language hits) |
| 3 | `uv run --no-project --with numpy --with mpmath python -B <temporary>/spotcheck_math_and_bib.py` | `0` | Verified all DOIs in workspace; 30 exact rational trials confirmed Lemma 4.2, eq. (11), and $L_j(h) \ge -2\|h\|^2$ (max error `0`); confirmed $1-\pi^2/12 = 0.177533 > 1/6$; independently confirmed E1–E3 folded $\lambda_{\min}$ signs at $q_{\mathrm{lo}}, q_{\mathrm{hi}}, q_{\mathrm{mix}}$ |
| 4 | `uv run --no-project --with pypdf python -B <temporary>/check_pdf.py` | `0` | 13 pages; `0` em dashes, `5` en dashes (all compound names); confirmed exact disclosure strings and F7 hits in compiled PDF |
