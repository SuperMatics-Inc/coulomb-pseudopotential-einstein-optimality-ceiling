# CLAIMS - statement to source map for `main.pdf`

Every statement in `paper/main.tex` maps below to a reviewed source with `file:line`, or is
flagged as derived in this paper or as provisional. Source paths are relative to this repository. Paper locations are given by `paper/main.tex` line and by
section label.

## 0. Label vocabulary used in the paper

The paper uses exactly one label per statement and carries it in the text:
`PROVED` (an argument is given in the paper), `CERTIFIED` (a finite exact computer
assisted certificate exists, verified by two independently written checkers), `NUMERICAL`
(float results that establish no bound), `OPEN` (no result). One section is additionally
`PROVISIONAL` in this file only, never in the PDF: it is expected to be replaced by a
certified statement or withdrawn. No statement in the paper is a measurement, and no
statement about any material is made.

The reviewed label set is `records/common-cutoff-review/REVIEW4.md:72-84` (§5, table
with the five rows and their labels, verdict PASS at `records/common-cutoff-review/REVIEW4.md:4`).

## 1. Model, conventions, and the common cutoff (§`sec:model`, `paper/main.tex:118-190`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Flat density of states, infinite band, isotropic even linear Migdal-Eliashberg pairing; pairing-only mask `mu* c_n c_m` on both indices; no Coulomb term in `Z`; strict cutoff; `omega_c` common to every spectrum compared | `records/common-cutoff/RIGOR.md:3-27` (§1) | model definition, as reviewed | no |
| `lambda`, `M`, `Omega_E=sqrt(M/lambda)`, `u=omega^2/Omega_E^2`, `dp=2 alpha^2F d omega/(lambda omega)` a probability measure with `int u dp = 1`; transfer weights `a_j`, `a_0=lambda`, compound Poisson structure | `records/common-cutoff/RIGOR.md:3-16`, `records/RIGOR.md` §1 (same conventions restated) | model definition | no |
| `mu* = mu/(1+mu ln(E_F/omega_c))` is the quantity a pairing-only subtraction stands for | classical strong-coupling normalization, as in `records/RESULT.md` §1 and the cited textbooks | interpretative, not used in any bound | no |
| Energies absolute, Matsubara frequencies `(2n+1) pi k_B T`; `k_B T_lin` is a model quantity | `records/common-cutoff/RIGOR.md:3-16` | definition | no |

## 2. Structural reduction (§`sec:reduce`, `paper/main.tex:191-222`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:reduce`: at fixed `(lambda,M)` and common `omega_c` the only parameters are `(R, mu*)` with `R=omega_c/Omega_E=omega_c sqrt(lambda/M)`; the mask is `(2i+1)^2 q < 4R^2`; two spectra compete only at equal `lambda`, equal `M`, equal `R` | `records/common-cutoff/RIGOR.md:28-38` (§2) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| In the fixtures `sum_i lambda_i = lambda` and `sum_i lambda_i u_i = lambda`, so `M`, `Omega_E` and `R^2` coincide with Einstein's exactly | `records/common-cutoff/RIGOR.md:28-38`, `records/common-cutoff/RIGOR.md:325-330` (exact rationals, `structure.py`), `records/common-cutoff/fixtures.json` (`R2` fields) | PROVED | no |
| Exact rational confirmation over 400 random two-line spectra and six `r` values | `records/common-cutoff/RIGOR.md:40-62` (iii), `records/common-cutoff/CHECKS.txt` | PROVED + tool check | no |

## 3. Einstein dominance at zero repulsion (§`sec:dom`, `paper/main.tex:223-272`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Lemma `lem:jensen`: `a_r^E >= a_r` for every `q>0`, `r>=1`; equality for some `r>=1` iff the spectrum is the single line | `records/common-cutoff/RIGOR.md:40-62` (§3(ii), the Jensen step at line 52) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| Lemma `lem:laplace`: exact folded stability form, matrix identity `F_ij = (2i+1) delta_ij - a_{|i-j|} + 2A_i delta_ij - 2A_min + mu* 1_{i<k}1_{j<k}`, the Laplacian display form equivalent to it, and the quotient identity | `records/common-cutoff/RIGOR.md:83-116` (§4, matrix form at 83, display form at 93, bookkeeping at 102); exact rational confirmation 120 trials (`records/common-cutoff/RIGOR.md:63-116`, `CHECKS.txt`) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| `a_r = lambda int u/(u+qr^2) dp` for a two-line spectrum, with `u_1=(1-p u_2)/(1-p)` | `records/common-cutoff/RIGOR.md:56-62` (iii) | PROVED | no |
| The repulsion adds a positive semidefinite rank-one term on the masked block and acts only along the all-ones direction there | `records/common-cutoff/RIGOR.md:117-131` (§4, Coulomb block) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |

## 4. Failure of entrywise dominance at positive `mu*` (§`sec:dom`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Proposition `prop:rank`: at `mu*>0` every form is the `mu*=0` form plus the same rank-one term; no ordering theorem transfers `a_r` dominance to the forms; the effect is spectrum dependent | `records/common-cutoff/RIGOR.md:117-131` | PROVED (`records/common-cutoff-review/REVIEW4.md:76`, "mechanism for failure of entrywise `a_r` dominance at `mu*>0`") | no |
| Remark `rem:mech`: the zero-repulsion margin that must be overcome is spectrum dependent, so dominance of the phonon entries decides nothing at `mu*>0` | `records/common-cutoff/RIGOR.md:336-358` (§7, the mechanism in the same language) | PROVED (mechanism) | no |
| Corollary `cor:value`: `k_B T_lin <= C(lambda) sqrt(M)` holds at every `mu*>=0`; the ceiling value is Coulomb robust and the optimizer is not | `records/common-cutoff/RIGOR.md:117-131` (rank-one term raises every form), ceiling input from `FINITEBAND`/`univglue` as cited in the paper | PROVED here (one line from Proposition `prop:rank` plus the reviewed zero-repulsion ceiling); the underlying ceiling is prior work, cited | no |
| Direct full-line values `lambda_max` `4.4033 -> 0.7556` (Einstein) against `3.2054 -> 1.0975` (mixture) at `q=1/200`, for `mu*=0` and `3/2` | `records/common-cutoff/RIGOR.md:132-134` | NUMERICAL (float, `crosscheck.py`) | no |
| Empty-mask observation: if `4R^2 < q_ph(lambda)` the mask contains only the fold `i=0`; for a single-line mask the Einstein form is `h_0^2+2mu* h_0^2` plus a positive semidefinite difference term, so `mu*>=0` cannot destabilize the Einstein line there | derived in this paper from Lemma `lem:laplace` and the mask condition of `records/common-cutoff/RIGOR.md:28-38`; not covered by `records/common-cutoff-review/REVIEW4.md` | proved in the paper, elementary, flagged in `paper/main.tex:338-380` as one-line observations | no |
| Large-`q` observation: `a_r <= lambda/(q r^2)`, hence `S_1 <= pi^2 lambda/(6q)`, and the difference part of `F` is bounded below by `-2 S_1 I`, giving `F >= (1-pi^2/12) I > 0` once `q >= 4 lambda` | derived in this paper; the same asymptotic stability statement appears as `records/mustar-half/RIGOR.md:77-131` (§3, asymptotic cutoff stability for `q >= 4 lambda`) | proved in the paper, elementary; the same statement is reviewed only incidentally inside the mustar-half record, §3 | no |

Note on the two observations: `records/common-cutoff-review/REVIEW4.md` does not list them, so they are **not**
presented as PROVED/CERTIFIED claims derived from the reviewed corpus. They are labelled
and proved inside the paper, in a subsection that says so, and they are not used by any
other result. Deleting them would not change any reviewed statement.

## 5. Certified counterexamples (§`sec:cert`, `paper/main.tex:381-509`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:cert` / Table `tab:cex`: three two-line spectra at `mu*/lambda = 2/3, 3/4, 1` that share `(lambda,M,mu*,omega_c)` with the Einstein line and have strictly larger `T_lin` | `records/common-cutoff/RESULT.md:26-28` (cases, `q_mix`, gains), `records/common-cutoff/RIGOR.md:309-335` (§6), `records/common-cutoff/bounds.json`, `records/common-cutoff/fixtures.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`, first half) | no |
| Einstein `q_E` brackets `[0.0083,0.0095]`, `[0.0009,0.003]`, `[129/500000,0.003]`; hot intervals `[q_hi, q_ph(lambda))` | `records/common-cutoff/bounds.json`, `records/common-cutoff/RIGOR.md:309-335`, `records/common-cutoff/RESULT.md:26-28` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| `C_E` brackets `[0.00837141,0.00895615]`, `[0.00337619,0.00616405]`, `[0.00127821,0.00435864]`, outward rounded from exact rationals | `records/common-cutoff/bounds.json`, `records/common-cutoff/RESULT.md:26-28` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| Two-line spectra `590/599` at `u=1/10` with `9/599` at `60`; `4975/4998` at `2/25` with `23/4998` at `200`; `2475/2498` at `2/25` with `23/2498` at `100`; `sum p_i = 1`, `sum p_i u_i = 1` exactly | `records/common-cutoff/RIGOR.md:325-335`, `records/common-cutoff/fixtures.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:76-78`) | no |
| Temperature gain `sqrt(q_mix/q_hi)-1` is a lower bound on the gain, with the displayed values `>=2.59%`, `>=29.09%`, `>=82.57%` | computed here from the exact rationals `q_mix` and `q_hi` of `records/common-cutoff/bounds.json` and `records/common-cutoff/fixtures.json`; the rounded source figures are `2.6%, 29%, 83%` (`RESULT.md:26-28`, `records/common-cutoff-review/REVIEW4.md:74`) | arithmetic consequence of the CERTIFIED brackets | no |
| Certification method: cold witness exact with no tail bound; hot cover by entrywise integer enclosure, diagonal radius penalty, Schur complement against a Gershgorin gap, exact residual with strict diagonal dominance; mask jump split points | `records/common-cutoff/RIGOR.md:139-215` (§5, enclosure at 201-215), `RIGOR.md:272-282` (573003 exact rational comparisons, radius slack up to 45239 integer units) | PROVED/CERTIFIED machinery, as reviewed | no |
| Two verifiers share no code and no formulation: different `pi` enclosures (Machin against `arctan 1/2 + arctan 1/3`), folded against unfolded | `records/common-cutoff/RIGOR.md:139-215`, `records/common-cutoff/CHECKS.txt` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:9-19`, `20-28`) | no |
| Nine mutants of the two exact verifiers (five in the first, four in the second), each with an unmutated control, each refused with an exit code and a message naming the statement | `records/common-cutoff/RIGOR.md:285-305` (mutant table), `records/common-cutoff/CHECKS.txt:19-30` (one row per mutant), `records/common-cutoff/FIX2.md:284-295` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:43-71`) | no |
| All 20 `CHECKS.txt` rows pass with their expected exit codes, no broken control | `records/common-cutoff/CHECKS.txt`, `records/common-cutoff-review/REVIEW4.md:43-71` | CERTIFIED | no |
| Receipt check: stored certificate fields recomputed and compared; a shaved `C_E` bracket is refused | `records/common-cutoff/RIGOR.md:165-215`, `CHECKS.txt` | CERTIFIED | no |
| Box counts `19`, `36`, `37` and `10`, `12`, `14`, `11` for the seven hot covers | `records/common-cutoff/bounds.json`, `records/common-cutoff/RIGOR.md:309-335` | CERTIFIED | no |

## 6. Certified brackets and the calibration (§`sec:brackets`, `paper/main.tex:510-572`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:brackets`, seven Einstein `q_E` brackets and `C_E` brackets, four of them at `mu*/lambda <= 1/2` | `records/common-cutoff/RESULT.md:55-60`, `records/common-cutoff/bounds.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| `q_ph(lambda)` is the zero-repulsion Einstein onset of the fixed-`(lambda,M)` problem, and every spectrum is stable at `q > q_ph` (that is the ceiling statement) | definition in `paper/main.tex:186-189`; values `q_ph(1) = 0.518653`, `q_ph(3) = 3.07269`, `q_ph(4) = 4.38414`, `q_ph(10) = 12.2824` from `records/C-LAMBDA/brackets.json` as quoted in `records/common-cutoff/RIGOR.md:161-163`, `records/common-cutoff/RESULT.md:64-74`, `records/common-cutoff/RESULT.md:225-226`, `records/common-cutoff/FIX2.md:289` | PROVED (from the reviewed zero-repulsion ceiling) | no |
| The right endpoint of every hot interval is truncated inside `q_ph(lambda)` | `records/common-cutoff/RESULT.md:225-226`, `records/common-cutoff/FIX2.md:289`, `records/common-cutoff/RESULT.md:72-74` (`q_ph(1)` equals that very bracket) | CERTIFIED | no |
| Zero-repulsion calibration `C(1) in [0.11461945, 0.11461957]`, i.e. `q in [0.51865242539,0.51865346269]`, distinct from the `mu*=1/10` anchor | `records/common-cutoff/RESULT.md:64-70`, `records/C-LAMBDA/brackets.json` | CERTIFIED upstream (`records/common-cutoff-review/REVIEW4.md:80`) | no |
| `mu*=1/10` anchor `C_E in [0.088327408,0.088685156]` is strictly below the zero-repulsion value | `records/common-cutoff/RESULT.md:64-70` | CERTIFIED | no |
| Monotone chain `0.1146194547`, `0.1610715064` at `lambda=3`, `0.1763847604` at `lambda=10`, `0.18272624777232952` as `lambda -> infinity` | `records/C-LAMBDA/RESULT.md:18`, `:22`, `:25`; limit constant from `univglue` (§`C_inf`) and `gamma` | CERTIFIED upstream | no |

## 7. Direct-discretization cross-check (§`sec:num`, `paper/main.tex:573-613`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:direct`: onsets `0.0083924335`, `0.00090451693`, `0.00025806035` and `T_mix/T_E = 1.21, 2.92, 9.96` | `records/common-cutoff/RESULT.md:130-134` | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Band doubling `|n|<=240 -> |n|<=480` shifts `lambda_max` by at most `6.4e-5` and flips no sign | `records/common-cutoff/RIGOR.md:396-405` (§8 item 5/6) | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Small-`mu*` controls: Einstein `lambda_max` `1.0032` against mixture `0.1817` at `q=0.308`; `1.0058` against `0.4133` at `q=0.0112` | `records/common-cutoff/RESULT.md:135-136`, `records/common-cutoff/RIGOR.md:396-405` | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Direct even-sector eigenvalue agrees with the folded form to `4.4e-16` on all seven instances | `records/common-cutoff/RESULT.md:137-148` | NUMERICAL | no |

## 8. Below one half, the provisional section (§`sec:half`, `paper/main.tex:614-678`)

**This whole section is PROVISIONAL.** Its reviewed status is REJECT for `CERTIFIED`:
`records/mustar-half/REVIEW.md:3` ("Overall Verdict: REJECT for `CERTIFIED` and
`PROVED` status"), with repairs in progress (`records/mustar-half/FIX.md`, and a separate
independent-checker slice not yet delivered). Nothing in it may be cited as certified.
Its four counterexamples are labelled NUMERICAL in the paper even though their cold
witnesses and brackets come from exact rational arithmetic, because the reviewed bar of
two independent sound checkers is not met for these instances.

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| The four sub-`1/2` instances are genuine counterexamples on the folded and unfolded eigenproblem, with seven-digit stability under window doubling | `records/mustar-half/REVIEW.md` (Executive Summary) | review finding, not a certification; reported in the paper as `records/mustar-half/REVIEW.md` finding | **yes** |
| Only one of the two exact verifiers is currently sound for these instances | `records/mustar-half/REVIEW.md` (P0 findings on `independent.py`), `records/mustar-half/FIX.md` §1 (F1, F2, F9 handled in a separate slice) | open repair | **yes** |
| `q_E` and `C_E` brackets `[0.519,0.525]` / `[0.02266124,0.02279187]`; `[0.495,0.501]` / `[0.02196018,0.02209288]`; `[0.414,0.419]` / `[0.01970781,0.01982647]`; `[0.407,0.412]` / `[0.01918838,0.01930589]` | `records/mustar-half/bounds.json` (recomputed and cross-checked for this paper), `records/mustar-half/RESULT.md:25-30` | NUMERICAL | **yes** |
| Spectra `1-6.0e-6` at `0.88` with `6.0e-6` at `20000`; `1-2.0e-5` at `0.8` with `2.0e-5` at `10000`; `1-1.55e-4` at `0.69` with `1.55e-4` at `2000`; `1-3.6e-4` at `0.64` with `3.6e-4` at `1000` | `records/mustar-half/RESULT.md:25-30`, `records/mustar-half/fixtures.json` | NUMERICAL | **yes** |
| Unstable `q_mix` `0.55, 0.52, 0.51, 0.49`, gains `>=2.353%`, `>=1.878%`, `>=10.326%`, `>=9.055%` | `records/mustar-half/RESULT.md:25-30`; gains recomputed here from the exact rationals | NUMERICAL (each gain is the exact arithmetic of its bracket pair) | **yes** |
| Direct `T_mix/T_E` `1.03295`, `1.02446`, `1.16047`, `1.18148` on a 600-point window | `records/mustar-half/RESULT.md:25-30` (column "True `T_mix/T_E`", `N=600`) | NUMERICAL | **yes** |
| Four anchors at `mu*/lambda <= 1/2` with their `q_E` and `C_E` brackets | `records/mustar-half/bounds.json`, `records/mustar-half/RESULT.md:34-40` | NUMERICAL | **yes** |
| Scan minimum `r_* = inf_{lambda,R} r_*` approximately `0.4785` at `lambda` approximately `25.58`, `omega_c/Omega_E` approximately `3.36`, active fold `k=5` | `records/mustar-half/RESULT.md:20`, `records/mustar-half/RESULT.md:41-57` | NUMERICAL | **yes** |

## 9. What is not claimed (§`sec:not`, `paper/main.tex:679-711`) and open problems (§`sec:open`, `paper/main.tex:712-748`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Einstein optimality at `mu*/lambda <= 1/2` is open in general | `records/common-cutoff/RESULT.md` §verdict (open), `records/common-cutoff/RIGOR.md:396-405`, `records/common-cutoff-review/REVIEW4.md:84` | OPEN (`records/common-cutoff-review/REVIEW4.md:84`) | yes for the sub-half window only |
| No measured `T_c`, no material prediction, no priority claim, no claim about other Coulomb kernels | scope section of `records/common-cutoff/RIGOR.md:359-405` (§8, honest qualifications) | scope | no |
| Rens arXiv:2611.20496 Thms 3, 4, 6 and Kondratev Prop. 1 are zero-Coulomb results and do not settle the positive-`mu*` question | `records/common-cutoff/RIGOR.md:396-405` (§8 item 6) | prior-work scope | no |

## 10. Deviations and repair log for this paper

1. `records/common-cutoff-review/REVIEW4.md:88` P3 nit 1 (reversed enclosure direction) is written correctly here:
   `paper/main.tex:431-433` states `C - R <= 2^17 F_ij <= C + R` for every off-diagonal entry,
   matching the code direction `(base-radius)[off] <= lower[off] <= upper[off] <=
   (base+radius)[off]`.
2. `records/common-cutoff-review/REVIEW4.md:89` P3 nit 2 (the factor 2.6/4.3/7 discrepancy attributed to a `(u,p)`
   unpack swap) is not repeated: the paper never attributes that discrepancy to a swap.
   The only swap mentioned (`paper/main.tex:490-493`) is the mutant that must be refused.
3. Rounded source figures "at least 2.6, 29, 83 percent" (`RESULT.md:26-28`,
   `records/common-cutoff-review/REVIEW4.md:74`) are printed as the exact floors `2.59`, `29.09`, `82.57` percent,
   because `sqrt(q_mix/q_hi)-1` evaluates to `2.597835%`, `29.099445%`, `82.574186%`;
   the same treatment is applied to the four provisional gains.
4. The sharp scalar constant `C_inf = 0.18272624777232952` is cited to `univglue`
   (addendum `anisosharp` states the same value), not to `optimum`: the released
   bibliography of the coupled-branch papers gives `optimum` the coefficient
   `sqrt(377/250)/(2pi)` approximately `0.19544330695` and imports `C_inf` from the
   scalar ceiling (the released bibliography of the coupled-branch papers, entries `finite`,
   `predecessor`; the released preprint doi:10.5281/zenodo.24372930, main.tex:35). All DOI and title pairs are
   copied from those released bibliographies.
5. The two elementary observations of §`sec:dom` (empty mask, large `q`) are derived in
   the paper and are not part of the reviewed label set; see the note in §4 above.
6. The sub-half section is written against the current records/mustar-half state: one sound
   verifier, the second under repair, review verdict REJECT for CERTIFIED. If
   `records/mustar-half/FIX-INDEP.md` lands with a sound port and a confirming re-review, this
   section and this file must be upgraded to match, or shrunk.
