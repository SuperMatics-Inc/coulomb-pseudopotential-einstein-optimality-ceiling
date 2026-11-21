# CLAIMS - statement to source map for `main.pdf`

Every statement in `main.tex` maps below to a reviewed source with `file:line`, or is
flagged as derived in this paper or as provisional. Source paths are relative to
`D:/dev/scratch/ceiling-20261118/`. Paper locations are given by `main.tex` line and by
section label.

## 0. Label vocabulary used in the paper

The paper uses exactly one label per statement and carries it in the text, printed as
small capitals `(proved)`, `(certified)`, `(numerical)`, `(open)` and defined in the abstract:
`PROVED` (an argument is given in the paper), `CERTIFIED` (a finite exact computer
assisted certificate exists, verified by two independently written checkers), `NUMERICAL`
(float results that establish no bound), `OPEN` (no result). No statement in the paper is a
measurement, and no statement about any material is made.

**No row below is provisional.** Section 8 was written while its second exact verifier was
under repair and was flagged provisional in this file at that time; the repair landed
(`MUSTAR-HALF/FIX.md`, `MUSTAR-HALF/FIX-INDEP.md`) and an independent re-review of the
current bytes returned PASS (`MUSTAR-HALF/REVIEW3.md:3`) with `CERTIFIED` allowed for the
four instances and the four anchors and `PROVED` for Lemma 1 and Theorems 1 to 5
(`REVIEW3.md:13-14`). Section 8 was upgraded to those labels and its numerical part kept
separate. The PDF never carried the provisional flag.

The reviewed label sets are `C-LAMBDA-MU/COMMON-CUTOFF-REVIEW/REVIEW4.md:72-84` (§5, table
with the five rows and their labels, verdict PASS at `REVIEW4.md:4`) and
`C-LAMBDA-MU/MUSTAR-HALF/REVIEW3.md:11-15` (§1, table of final claim labels, verdict PASS
at `REVIEW3.md:3`).

## 1. Model, conventions, and the common cutoff (§`sec:model`, `main.tex:125-197`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Flat density of states, infinite band, isotropic even linear Migdal-Eliashberg pairing; pairing-only mask `mu* c_n c_m` on both indices; no Coulomb term in `Z`; strict cutoff; `omega_c` common to every spectrum compared | `COMMON-CUTOFF/RIGOR.md:3-27` (§1) | model definition, as reviewed | no |
| `lambda`, `M`, `Omega_E=sqrt(M/lambda)`, `u=omega^2/Omega_E^2`, `dp=2 alpha^2F d omega/(lambda omega)` a probability measure with `int u dp = 1`; transfer weights `a_j`, `a_0=lambda`, compound Poisson structure | `COMMON-CUTOFF/RIGOR.md:3-16`, `C-LAMBDA-MU/RIGOR.md` §1 (same conventions restated) | model definition | no |
| `mu* = mu/(1+mu ln(E_F/omega_c))` is the quantity a pairing-only subtraction stands for | classical strong-coupling normalization, as in `RESULT.md` §1 of `C-LAMBDA-MU` and the cited textbooks | interpretative, not used in any bound | no |
| Energies absolute, Matsubara frequencies `(2n+1) pi k_B T`; `k_B T_lin` is a model quantity | `COMMON-CUTOFF/RIGOR.md:3-16` | definition | no |

## 2. Structural reduction (§`sec:reduce`, `main.tex:198-229`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:reduce`: at fixed `(lambda,M)` and common `omega_c` the only parameters are `(R, mu*)` with `R=omega_c/Omega_E=omega_c sqrt(lambda/M)`; the mask is `(2i+1)^2 q < 4R^2`; two spectra compete only at equal `lambda`, equal `M`, equal `R` | `COMMON-CUTOFF/RIGOR.md:28-38` (§2) | PROVED (`REVIEW4.md:76`) | no |
| In the fixtures `sum_i lambda_i = lambda` and `sum_i lambda_i u_i = lambda`, so `M`, `Omega_E` and `R^2` coincide with Einstein's exactly | `COMMON-CUTOFF/RIGOR.md:28-38`, `COMMON-CUTOFF/RIGOR.md:325-330` (exact rationals, `structure.py`), `COMMON-CUTOFF/fixtures.json` (`R2` fields) | PROVED | no |
| Exact rational confirmation over 400 random two-line spectra and six `r` values | `COMMON-CUTOFF/RIGOR.md:40-62` (iii), `COMMON-CUTOFF/CHECKS.txt` | PROVED + tool check | no |

## 3. Einstein dominance at zero repulsion (§`sec:dom`, `main.tex:230-281`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Lemma `lem:jensen`: `a_r^E >= a_r` for every `q>0`, `r>=1`; equality for some `r>=1` iff the spectrum is the single line | `COMMON-CUTOFF/RIGOR.md:40-62` (§3(ii), the Jensen step at line 52) | PROVED (`REVIEW4.md:76`) | no |
| Lemma `lem:laplace`: exact folded stability form, matrix identity `F_ij = (2i+1+2A_i-a_{2i+1}+2mu* 1_{i<k}) delta_ij - a_{|i-j|} - a_{i+j+1}` for `i != j`, equivalently `F = diag(d_i+2A_i) - T - H + 2mu* 1_{i<k}1_{j<k}` with `T` the Toeplitz and `H` the Hankel part, the Laplacian display form equivalent to it, and the quotient identity | `COMMON-CUTOFF/RIGOR.md:83-116` (§4, matrix form at 83, display form at 93, bookkeeping at 102); exact rational confirmation 120 trials (`COMMON-CUTOFF/RIGOR.md:63-116`, `CHECKS.txt`) | PROVED (`REVIEW4.md:76`) | no |
| `a_r = lambda int u/(u+qr^2) dp` for a two-line spectrum, with `u_1=(1-p u_2)/(1-p)` | `COMMON-CUTOFF/RIGOR.md:56-62` (iii) | PROVED | no |
| The repulsion adds a positive semidefinite rank-one term on the masked block and acts only along the all-ones direction there | `COMMON-CUTOFF/RIGOR.md:117-131` (§4, Coulomb block) | PROVED (`REVIEW4.md:76`) | no |

## 4. Failure of entrywise dominance at positive `mu*` (§`sec:dom`, `main.tex:282-393`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Proposition `prop:rank`: at `mu*>0` every form is the `mu*=0` form plus the same rank-one term; no ordering theorem transfers `a_r` dominance to the forms; the effect is spectrum dependent | `COMMON-CUTOFF/RIGOR.md:117-131` | PROVED (`REVIEW4.md:76`, "mechanism for failure of entrywise `a_r` dominance at `mu*>0`") | no |
| Remark `rem:mech`: the zero-repulsion margin that must be overcome is spectrum dependent, so dominance of the phonon entries decides nothing at `mu*>0` | `COMMON-CUTOFF/RIGOR.md:336-358` (§7, the mechanism in the same language) | PROVED (mechanism) | no |
| Corollary `cor:value`: `k_B T_lin <= C(lambda) sqrt(M)` holds at every `mu*>=0`; the ceiling value is Coulomb robust and the optimizer is not | `COMMON-CUTOFF/RIGOR.md:117-131` (rank-one term raises every form), ceiling input from `FINITEBAND`/`univglue` as cited in the paper | PROVED here (one line from Proposition `prop:rank` plus the reviewed zero-repulsion ceiling); the underlying ceiling is prior work, cited | no |
| Direct full-line values `lambda_max` `4.4033 -> 0.7556` (Einstein) against `3.2054 -> 1.0975` (mixture) at `q=1/200`, for `mu*=0` and `3/2` | `COMMON-CUTOFF/RIGOR.md:132-134` | NUMERICAL (float, `crosscheck.py`) | no |
| Empty-mask observation: if `4R^2 < q_ph(lambda)` then on the nonempty open interval `(4R^2, q_ph(lambda))` the mask is empty, so `F = F_0` there and the Einstein form is indefinite arbitrarily close to `q_ph(lambda)`; hence the Einstein onset stays `q_ph(lambda)` at every `mu* >= 0` and strictly dominates every non-Einstein onset | derived in this paper from Lemma `lem:laplace` and the mask condition of `COMMON-CUTOFF/RIGOR.md:28-38`; not covered by `REVIEW4.md` | proved in the paper, elementary, flagged in `main.tex:338-380` as one-line observations | no |
| Large-`q` observation: `a_r <= lambda/(q r^2)`, hence `S_1 <= pi^2 lambda/(6q)`, and the difference part of `F` is bounded below by `-2 S_1 I`, giving `F >= (1-pi^2/12) I > 0` once `q >= 4 lambda` | derived in this paper; the same asymptotic stability statement appears as `C-LAMBDA-MU/MUSTAR-HALF/RIGOR.md:77-131` (§3, asymptotic cutoff stability for `q >= 4 lambda`) | proved in the paper, elementary; the same statement is reviewed only incidentally inside MUSTAR-HALF §3 | no |

Note on the two observations: `REVIEW4.md` does not list them, so they are **not**
presented as PROVED/CERTIFIED claims derived from the reviewed corpus. They are labelled
and proved inside the paper, in a subsection that says so, and they are not used by any
other result. Deleting them would not change any reviewed statement.

## 5. Certified counterexamples (§`sec:cert`, `main.tex:394-529`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:cert` / Table `tab:cex`: three two-line spectra at `mu*/lambda = 2/3, 3/4, 1` that share `(lambda,M,mu*,omega_c)` with the Einstein line and have strictly larger `T_lin` | `COMMON-CUTOFF/RESULT.md:26-28` (cases, `q_mix`, gains), `COMMON-CUTOFF/RIGOR.md:309-335` (§6), `COMMON-CUTOFF/bounds.json`, `COMMON-CUTOFF/fixtures.json` | CERTIFIED (`REVIEW4.md:78`, first half) | no |
| Einstein `q_E` brackets `[0.0083,0.0095]`, `[0.0009,0.003]`, `[129/500000,0.003]`; hot intervals `[q_hi, q_ph(lambda))` | `COMMON-CUTOFF/bounds.json`, `COMMON-CUTOFF/RIGOR.md:309-335`, `COMMON-CUTOFF/RESULT.md:26-28` | CERTIFIED (`REVIEW4.md:78`) | no |
| `C_E` brackets `[0.00837140,0.00895615]`, `[0.00337618,0.00616405]`, `[0.00127820,0.00435864]`, rounded outward at eight decimals from the exact `sqrt(q_lo)` and `sqrt(q_hi)` of each certified `q_E` bracket | `COMMON-CUTOFF/bounds.json`, `COMMON-CUTOFF/RESULT.md:26-28` | CERTIFIED (`REVIEW4.md:78`) | no |
| Two-line spectra `590/599` at `u=1/10` with `9/599` at `60`; `4975/4998` at `2/25` with `23/4998` at `200`; `2475/2498` at `2/25` with `23/2498` at `100`; `sum p_i = 1`, `sum p_i u_i = 1` exactly | `COMMON-CUTOFF/RIGOR.md:325-335`, `COMMON-CUTOFF/fixtures.json` | CERTIFIED (`REVIEW4.md:76-78`) | no |
| Temperature gain `sqrt(q_mix/q_hi)-1` is a lower bound on the gain, with the displayed values `>=2.59%`, `>=29.09%`, `>=82.57%` | computed here from the exact rationals `q_mix` and `q_hi` of `COMMON-CUTOFF/bounds.json` and `COMMON-CUTOFF/fixtures.json`; the rounded source figures are `2.6%, 29%, 83%` (`RESULT.md:26-28`, `REVIEW4.md:74`) | arithmetic consequence of the CERTIFIED brackets | no |
| Certification method: cold witness exact with no tail bound; hot cover by entrywise integer enclosure, diagonal radius penalty, Schur complement against a Gershgorin gap, exact residual with strict diagonal dominance; mask jump split points | `COMMON-CUTOFF/RIGOR.md:139-215` (§5, enclosure at 201-215), `COMMON-CUTOFF/CHECKS.txt:72-75` (573003 exact rational entry comparisons, radius slack up to 45239 integer units at scale 2**17), `COMMON-CUTOFF/FIX2.md:290` | PROVED/CERTIFIED machinery, as reviewed | no |
| Two verifiers share no code and no formulation: different `pi` enclosures (Machin against `arctan 1/2 + arctan 1/3`), folded against unfolded | `COMMON-CUTOFF/RIGOR.md:139-215`, `COMMON-CUTOFF/CHECKS.txt` | CERTIFIED (`REVIEW4.md:9-19`, `20-28`) | no |
| Nine mutants of the two exact verifiers (five in the first, four in the second), each with an unmutated control, each refused with an exit code and a message naming the statement | `COMMON-CUTOFF/RIGOR.md:285-305` (mutant table), `COMMON-CUTOFF/CHECKS.txt:19-30` (one row per mutant), `COMMON-CUTOFF/FIX2.md:284-295` | CERTIFIED (`REVIEW4.md:43-71`) | no |
| All 20 `CHECKS.txt` rows pass with their expected exit codes, no broken control | `COMMON-CUTOFF/CHECKS.txt`, `COMMON-CUTOFF-REVIEW/REVIEW4.md:43-71` | CERTIFIED | no |
| Receipt check: stored certificate fields recomputed and compared; a shaved `C_E` bracket is refused | `COMMON-CUTOFF/RIGOR.md:165-215`, `CHECKS.txt` | CERTIFIED | no |
| Box counts `19`, `36`, `37` and `10`, `12`, `14`, `11` for the seven hot covers (the second verifier's counts; `COMMON-CUTOFF/bounds.json` stores the first verifier's own counts `18`, `36`, `37`, `10`, `18`, `14`, `11`, checked as a receipt) | `COMMON-CUTOFF/CHECKS.txt` Note 2, `COMMON-CUTOFF/RIGOR.md:309-335`, `COMMON-CUTOFF/bounds.json` | CERTIFIED | no |

## 6. Certified brackets and the calibration (§`sec:brackets`, `main.tex:530-593`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:brackets`, seven Einstein `q_E` brackets and `C_E` brackets, four of them at `mu*/lambda <= 1/2` | `COMMON-CUTOFF/RESULT.md:55-60`, `COMMON-CUTOFF/bounds.json` | CERTIFIED (`REVIEW4.md:78`) | no |
| `q_ph(lambda)` is the zero-repulsion Einstein onset of the fixed-`(lambda,M)` problem, and every spectrum is stable at `q > q_ph` (that is the ceiling statement) | definition in `main.tex:186-191`; outward six-digit upper endpoints `q_ph^hi(1) = 0.518654`, `q_ph^hi(2) = 1.77000`, `q_ph^hi(3) = 3.07270`, `q_ph^hi(4) = 4.38414`, `q_ph^hi(10) = 12.2824` computed from `C-LAMBDA/brackets.json`, as quoted in `COMMON-CUTOFF/RIGOR.md:161-163`, `COMMON-CUTOFF/RESULT.md:64-74`, `:225-226`, `COMMON-CUTOFF/FIX2.md:289` | PROVED (from the reviewed zero-repulsion ceiling) | no |
| The right endpoint of every hot interval is an outward display of the certified upper endpoint `q_ph^hi(lambda) >= q_ph(lambda)`; the certified range and Corollary `cor:value` together cover every larger `q` with no gap | `COMMON-CUTOFF/RESULT.md:225-226`, `COMMON-CUTOFF/FIX2.md:289`, `COMMON-CUTOFF/RESULT.md:72-74`, `C-LAMBDA/brackets.json` (`q_numerators`, denominator `10^11`) | CERTIFIED | no |
| Zero-repulsion calibration `C(1) in [0.11461945, 0.11461957]`, i.e. `q in [0.51865242539,0.51865346269]`, distinct from the `mu*=1/10` anchor | `COMMON-CUTOFF/RESULT.md:64-70`, `C-LAMBDA/brackets.json` | CERTIFIED upstream (`REVIEW4.md:80`) | no |
| `mu*=1/10` anchor `C_E in [0.088327408,0.088685156]` is strictly below the zero-repulsion value | `COMMON-CUTOFF/RESULT.md:64-70` | CERTIFIED | no |
| Monotone chain `0.1146194547`, `0.1610715064` at `lambda=3`, `0.1763847604` at `lambda=10`, `0.18272624777232952` as `lambda -> infinity` | `C-LAMBDA/RESULT.md:18`, `:22`, `:25`; limit constant from `univglue` (§`C_inf`) and `gamma` | CERTIFIED upstream | no |

## 7. Direct-discretization cross-check (§`sec:num`, `main.tex:594-638`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:direct`: onsets `0.0083924335`, `0.00090451693`, `0.00025806035` and `T_mix/T_E = 1.21, 2.92, 9.96` | `COMMON-CUTOFF/RESULT.md:130-134` | NUMERICAL (`REVIEW4.md:82`) | no |
| Band doubling `|n|<=240 -> |n|<=480` shifts `lambda_max` by at most `6.4e-5` and flips no sign | `COMMON-CUTOFF/RIGOR.md:396-405` (§8 item 5/6) | NUMERICAL (`REVIEW4.md:82`) | no |
| Small-`mu*` controls: Einstein `lambda_max` `1.0032` against mixture `0.1817` at `q=0.308`; `1.0058` against `0.4133` at `q=0.0112` | `COMMON-CUTOFF/RESULT.md:135-136`, `COMMON-CUTOFF/RIGOR.md:396-405` | NUMERICAL (`REVIEW4.md:82`) | no |
| Direct even-sector eigenvalue agrees with the folded form to `4.4e-16` on all seven instances | `COMMON-CUTOFF/RESULT.md:137-148` | NUMERICAL | no |

## 8. Below one half: certified instances, analytic regimes, numerical phase data (§`sec:half`, `main.tex:639-1142`)

Section 8 has three parts: the certified instances (`sec:half:cert`, `main.tex:663-708`), the
proved analytic statements (`sec:half:proof`, `main.tex:805-1033`), and the numerical phase
data (`sec:half:num`, `main.tex:1034-1142`). Labels follow
`MUSTAR-HALF/REVIEW3.md:13-14` (verdict PASS at `REVIEW3.md:3`): `CERTIFIED` for the four
counterexamples and the four anchors, `PROVED` for Lemma 1 and Theorems 1 to 5, `NUMERICAL`
for the phase scans and the direct values. The two-verifier standard of Section 5 is met
here: `replay.py` and the rebuilt `independent.py` share no code path, no formulation and no
pi enclosure, and each certifies all eight instances (`REVIEW3.md:5,13`,
`MUSTAR-HALF/FIX-INDEP.md:3-4,34-41`). This section carried a provisional flag in this file
while the second verifier was under repair; the repair landed in
`MUSTAR-HALF/FIX-INDEP.md` and the flag is retired.

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:half` / Table `tab:half`: four rational two-line spectra at `mu*/lambda = 61261/128000`, `12/25`, `1309/2700`, `489/1000`, each sharing `(lambda,M,mu*,omega_c)` with the Einstein line, with certified margins `q_mix/q_hi >= 1.0476, 1.0379, 1.2171, 1.1893`, that is temperature gains `>= 2.353, 1.878, 10.326, 9.055` percent | `MUSTAR-HALF/RESULT.md:23-30` (cases), `MUSTAR-HALF/bounds.json`, `MUSTAR-HALF/fixtures.json` | CERTIFIED (`REVIEW3.md:13`) | no |
| `q_E` and `C_E` brackets `[0.519,0.525]` / `[0.02266124,0.02279187]`; `[0.495,0.501]` / `[0.02196018,0.02209288]`; `[0.414,0.419]` / `[0.01970781,0.01982647]`; `[0.407,0.412]` / `[0.01918838,0.01930589]`, eight-decimal outward rounding of the exact rational brackets | `MUSTAR-HALF/bounds.json`, `MUSTAR-HALF/RESULT.md:23-30` | CERTIFIED (`REVIEW3.md:13`) | no |
| Spectra `1-6.0e-6` at `0.88` with `6.0e-6` at `20000`, that is `499975/499978` at `22/25` with `3/499978` at `20000`; `1-2.0e-5` at `0.8` with `2.0e-5` at `10000`; `1-1.55e-4` at `0.69` with `1.55e-4` at `2000`; `1-3.6e-4` at `0.64` with `3.6e-4` at `1000` | `MUSTAR-HALF/fixtures.json`, `MUSTAR-HALF/RESULT.md:23-30` | CERTIFIED (`REVIEW3.md:13`) | no |
| Four Einstein anchors `anchor-l2-mu1-R3/2`, `anchor-l3-mu3/2-R2`, `anchor-l10-mu4-R3`, `anchor-l20-mu19/2-R5` at `mu*/lambda` `0.500`, `0.500`, `0.400`, `0.475`, with their `q_E` and `C_E` brackets | `MUSTAR-HALF/RESULT.md:32-39`, `MUSTAR-HALF/bounds.json` | CERTIFIED (`REVIEW3.md:13`) | no |
| Lemma `lem:decomp`: exact finite-support decomposition of the form into the free term, the masked rank-one term and the weight sum `sum_j a_j L_j` | `MUSTAR-HALF/RIGOR.md:31` | PROVED (`REVIEW3.md:14`) | no |
| Theorem `thm:twodelta`: at fixed `(q,k,mu*)` the infimum of `lambda_min(F_p^(k)(q))` over `P_1` equals the infimum over two-line spectra, on the finitely supported form core | `MUSTAR-HALF/RIGOR.md:53`, `MUSTAR-HALF/RESULT.md:15` | PROVED (`REVIEW3.md:14`) | no |
| Theorem `thm:nomask`: whenever `4R^2 < q_E(lambda,0)`, the mask is empty on an open neighbourhood of `[q_E(lambda,0),inf)` and Einstein strictly maximizes `T_lin` for all `mu* >= 0`; strictness is needed, and the statement is conditional on the zero-repulsion ceiling theorem of `C-LAMBDA/RIGOR.md` | `MUSTAR-HALF/RIGOR.md:60`, `MUSTAR-HALF/RESULT.md:16` | PROVED (`REVIEW3.md:14`, conditional on the cited ceiling theorem) | no |
| Theorem `thm:large`: for fixed `R > 0`, `lambda >= 4R^2+1` implies `q_ph(lambda) > lambda-1 >= 4R^2` and strict Einstein optimality for every `mu* >= 0` | `MUSTAR-HALF/RIGOR.md:66` | PROVED (`REVIEW3.md:14`) | no |
| Theorem `thm:cone`: on the single-mode window `4R^2/9 <= q < 4R^2`, `mu* <= 1+a_1(q;p)` gives a simple positive nonincreasing ground state, every `L_j(h*) < 0` and strict Einstein dominance; the condition holds unconditionally for `mu* <= 1` and for `lambda <= 2` throughout `mu*/lambda <= 1/2` | `MUSTAR-HALF/RIGOR.md:81-115`, `MUSTAR-HALF/RESULT.md:17` | PROVED (`REVIEW3.md:14`) | no |
| The sharpness example of Theorem `thm:cone`: at `lambda=152`, `mu*=76`, `q=4.33295` the two-line spectrum `(u_1,u_2)=(1e-5,17.5)` has `lambda_min = -6.717e-5 < 0` while `h*_0 < h*_1` already at `lambda=20` | `MUSTAR-HALF/RESULT.md:18`, `MUSTAR-HALF/RESULT.md:66,70` | NUMERICAL (`REVIEW3.md:15`) | no |
| Theorem `thm:asym`: for every `lambda>0`, `mu*>=0`, `R>0` and `p`, `q >= 4 lambda` gives `F_p >= (1-pi^2/12) I`, the hot-side handoff `q_asym = 4 lambda` | `MUSTAR-HALF/RIGOR.md:117-131` | PROVED (`REVIEW3.md:14`) | no |
| Structural checker: exact verification of the cone pairing difference, the modified diagonal ordering, Theorem `thm:large` and Lemma `lem:decomp` on the probes, with three guarded negative controls refused | `MUSTAR-HALF/RIGOR.md:168-177`, `MUSTAR-HALF/CHECKS.txt` | PROVED machinery, as reviewed (`REVIEW3.md:14`) | no |
| Two independent exact verifiers certify all eight instances (folded full-line cold form with a Schur-complement tail against unfolded with a Cauchy-Schwarz per-row tail, Machin against Hutton `pi`); thirteen mutants (five in `replay.py`, eight in `independent.py`) are refused with their controls passing; self-check and adversarial probes pass | `MUSTAR-HALF/FIX-INDEP.md:3-4,63-66`, `MUSTAR-HALF/REVIEW3.md:5,13,76`, `MUSTAR-HALF/CHECKS.txt` | CERTIFIED (`REVIEW3.md:13`) | no |
| Unstable `q_mix` `0.55, 0.52, 0.51, 0.49`, gains `>=2.353%`, `>=1.878%`, `>=10.326%`, `>=9.055%` as the exact arithmetic of each certified bracket pair | `MUSTAR-HALF/RESULT.md:23-30`, `MUSTAR-HALF/bounds.json` | CERTIFIED bracket arithmetic (`REVIEW3.md:13`) | no |
| Direct `T_mix/T_E` `1.03295`, `1.02446`, `1.16047`, `1.18148` on a 600-point window | `MUSTAR-HALF/RESULT.md:23-30` (column "True `T_mix/T_E`", `N=600`), `REVIEW3.md:15` | NUMERICAL (`REVIEW3.md:15`) | no |
| Phase data: `mu*/lambda = 1/2` holds numerically for all `lambda < 25.55` and mask counts `k in {0,1,2,3,4}`; above that a `k=5` window `lambda in [25.55,34.0]`, `omega_c/Omega_E in [3.2,3.6]` dips to `r_min ≈ 0.4785` at `lambda ≈ 25.58`, `omega_c/Omega_E ≈ 3.36`; Table `tab:phase` in full | `MUSTAR-HALF/RESULT.md:11,19-21,41-57`, `MUSTAR-HALF/phase_scan.py`, `REVIEW3.md:15` | NUMERICAL (`REVIEW3.md:15`) | no |

## 9. What is not claimed (§`sec:not`, `main.tex:1143-1185`) and open problems (§`sec:open`, `main.tex:1186-1229`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Einstein optimality is open in the interior of `mu*/lambda <= 1/2`: no proof in either direction between the proved regimes, and one half is not a threshold | `MUSTAR-HALF/RESULT.md:11` (one half not globally sharp, holds numerically for `lambda < 25.55`), `MUSTAR-HALF/RESULT.md:74-75` (open questions), `REVIEW4.md:84` (open above the certified window) | OPEN | no |
| The exact threshold curve, its full extent, the critical coupling of the `k=5` window and the single-mode failure from `lambda=152` are numerical | `MUSTAR-HALF/RESULT.md:19-21,66,70,75`, `REVIEW3.md:15` | NUMERICAL (`REVIEW3.md:15`) | no |
| No measured `T_c`, no material prediction, no priority claim, no claim about other Coulomb kernels | scope section of `COMMON-CUTOFF/RIGOR.md:359-405` (§8, honest qualifications) | scope | no |
| Rens arXiv:2611.20496 Thms 3, 4, 6 and Kondratev Prop. 1 are zero-Coulomb results and do not settle the positive-`mu*` question | `COMMON-CUTOFF/RIGOR.md:396-405` (§8 item 6) | prior-work scope | no |

## 10. Deviations and repair log for this paper

1. `REVIEW4.md:88` P3 nit 1 (reversed enclosure direction) is written correctly here:
   `main.tex:431-433` states `C - R <= 2^17 F_ij <= C + R` for every off-diagonal entry,
   matching the code direction `(base-radius)[off] <= lower[off] <= upper[off] <=
   (base+radius)[off]`.
2. `REVIEW4.md:89` P3 nit 2 (the factor 2.6/4.3/7 discrepancy attributed to a `(u,p)`
   unpack swap) is not repeated: the paper never attributes that discrepancy to a swap.
   The only swap mentioned (`main.tex:490-493`) is the mutant that must be refused.
3. Rounded source figures "at least 2.6, 29, 83 percent" (`RESULT.md:26-28`,
   `REVIEW4.md:74`) are printed as the exact floors `2.59`, `29.09`, `82.57` percent,
   because `sqrt(q_mix/q_hi)-1` evaluates to `2.597835%`, `29.099445%`, `82.574186%`;
   the same treatment is applied to the four sub-half gains.
4. The sharp scalar constant `C_inf = 0.18272624777232952` is cited to `univglue`
   (addendum `anisosharp` states the same value), not to `optimum`: the released
   bibliography of the coupled-branch papers gives `optimum` the coefficient
   `sqrt(377/250)/(2pi)` approximately `0.19544330695` and imports `C_inf` from the
   scalar ceiling (`UNIV-GLUE/OPTIMUM2/ANISO-SHARP-PAPER/refs.bib`, entries `finite`,
   `predecessor`; `UNIV-GLUE/release-bundle/main.tex:35`). All DOI and title pairs are
   copied from those released bibliographies.
5. The two elementary observations of §`sec:dom` (empty mask, large `q`) are derived in
   the paper and are not part of the reviewed label set; see the note in §4 above.
6. The sub-half section was first written while the second exact verifier was under repair,
   with a provisional flag in this file and a REJECT verdict for `CERTIFIED`
   (`MUSTAR-HALF/REVIEW.md:3`). `MUSTAR-HALF/FIX.md` and `MUSTAR-HALF/FIX-INDEP.md` then
   landed, `MUSTAR-HALF/REVIEW3.md:3` returned PASS, and Section 8 was upgraded to the
   labels `REVIEW3.md:13-14` allows, with the phase data left NUMERICAL. The upgrade
   rewrote the section's statement of its evidence (`main.tex:639-662`) and added the
   analytic subsection `sec:half:proof` (`main.tex:805-1033`) with Lemma `lem:decomp` and
   Theorems `thm:twodelta`, `thm:nomask`, `thm:large`, `thm:cone`, `thm:asym`; in the
   pre-repair source the `q >= 4 lambda` handoff appeared as prose (`main.v1.tex:359-376`)
   and the two-line reduction not at all. No statement was weakened to match a certificate
   and none was promoted above its reviewed label.

## 11. Preprint review fixes (`MASSIVE/CUTOFF-PAPER/REVIEW.md`, verdict PASS-WITH-FIXES)

`main.v1.tex` and `CLAIMS.v1.md` are the pre-fix copies. Nothing in `REVIEW.md` was edited.

| Finding | Severity | Change | Location after fix |
|---|---|---|---|
| F1 | P0 | the onset was defined as a supremum over stable temperatures; it is now `k_B T_lin = sup{k_B T : F not >= 0}`, consistent with the following sentence | `main.tex:177` |
| F2 | P0 | the extraneous `sqrt(lambda)` is removed from Corollary `cor:value`; the ceiling is `C(lambda) sqrt(M) <= C_inf sqrt(M)` | `main.tex:294` |
| F3 | P0 | all seven `C_E` brackets were rounded inward in v1 (for example `0.00837141` against an exact lower endpoint `0.00837140880`, and `0.01684338`, `0.06215199` in Table 2); each is now eight-decimal rounding outward from the exact rational bracket, checked against `COMMON-CUTOFF/bounds.json` endpoint by endpoint | `main.tex:408,410,412` (Table `tab:cex`), `main.tex:542-548` (Table `tab:brackets`), `main.tex:569,571` (prose), this file §5 and §6 |
| F4 | P1 | E1 decimal weights corrected to `0.984975` at `0.1` and `0.015025` at `60` (exact `590/599` and `9/599`) | `main.tex:409` |
| F5 | P1 | the obstruction copied from a Lorentzian-width context is deleted and replaced by the sign flip inside single entries of the folded form, `F_ii = d_i+2A_i-a_{2i+1}+2mu*[i<k]` against `F_ij = -a_{|i-j|}-a_{i+j+1}` | `main.tex:311-319` |
| F6 | P1 | the empty-mask argument no longer invokes the rank-one term, which is positive semidefinite and cannot preserve indefiniteness; it uses the empty mask on the open interval `(4R^2, q_ph(lambda))` | `main.tex:354-358` |
| F7 | P1 | all process language is removed from the PDF: `provisional`, `currently sound`, `is being finished`, `expected to be replaced or withdrawn`, `upgrade or replace`, and the truncation wording. Section 8 was a plain NUMERICAL section at that point and was later upgraded on the re-review of its sources (§10 item 6); the prohibition on process language holds for every version | `main.tex:50-52`, `main.tex:97-98`, `main.tex:110-111`, `main.tex:639-662`, `main.tex:669`, `main.tex:680-689`, `main.tex:698-699`, `main.tex:728-732`, `main.tex:749-751`, `main.tex:786-788` |
| F8 | P2 | the hot-interval caption now states that the printed right endpoint is an outward display of `q_ph^hi(lambda) >= q_ph(lambda)`, so the certified range plus Corollary `cor:value` cover every larger `q` with no gap; the displayed endpoints are outward (`0.518654`, `1.77000`, `3.07270`, `4.38414`, `12.2824`) | `main.tex:542-548`, `main.tex:551-560` |
| F9 | P2 | the normal diagonal is written as dimensionless, `D_n = Z_n|omega_n|/(pi k_B T) = |2n+1| + a_0 + 2 sum_j a_j` | `main.tex:154` |
| F10 | P2 | this file only: empty-mask row (§4), folded matrix identity (§3), box-count citation moved to `CHECKS.txt` Note 2 with the stored first-verifier counts recorded (§5), `C_E` row (§5), hot-endpoint row (§6), one-verifier row (§8), every section line range renumbered, and §0 restated | this file |
| F11 | P3 | `Migdal--Eliashberg` on the last open-problem item, and Table `tab:brackets` names `E1, E2, E3` and `A1, A2, A3, A4` instead of "the rows above them" | `main.tex:558`, `main.tex:765` |
| P12 (`REVIEW4.md` §6 item 1) | P3 | the enclosure direction is stated as soundness requires it, `C_ij - R_ij <= F_ij(q_lo)` and `F_ij(q_hi) <= C_ij + R_ij`, with the monotonicity of the off-diagonal entries in `q` supplying the direction, instead of the reversed wording used in the source prose | `main.tex:476-478` |
| P13 (`REVIEW4.md` §6 item 2) | P3 | the mirror term is described as automatic in any discretization that spans the negative Matsubara axis, and the earlier `2.6` to `7` disagreement is attributed to four defects of the earlier direct implementation (bosonic frequencies, a doubled `lambda`, a wrong normal diagonal, an unsymmetrized kernel), not to a weight-position unpacking | `main.tex:271-274`, `main.tex:599-603` |

## 12. Second repair round (after the section 8 upgrade)

The changes below were made after the fixes of Section 11, when Section 8 was upgraded on
`MUSTAR-HALF/REVIEW3.md` and the numerical phase material was checked line by line against
`MUSTAR-HALF/RESULT.md`'s own table.

1. Section 8 gained the analytic subsection and the certified labels of
   `REVIEW3.md:13-14` (§10 item 6), and the whole section now states its evidence standard
   once (`main.tex:641-652`).
2. Every entry of Table `tab:phase` was verified against `MUSTAR-HALF/RESULT.md:45-58` with
   a comparison script that normalizes the typesetting only: all fourteen rows match cell
   for cell (nine cutoff columns, the infimum and the mask count per row, 154 tabulated
   values), so the table reproduces the scan grid exactly.
3. The caption and the three readings of Table `tab:phase` were rewritten so that the
   meaning of the `infinity` cells, of the rows whose infimum reads one half, and of the
   mask-count column match what the scan computes (`main.tex:1046-1054`,
   `main.tex:1113-1119`). In particular the paper no longer claims that every `infinity`
   cell is one where the mask is empty at the crossing: that is true of the cells in the
   small-cutoff staircase, where Theorem `thm:nomask` proves optimality, and the other
   cells are recorded as unbeaten on the grid only.
4. `r_min` is quoted at the coupling of the source's finer estimate, `lambda ≈ 25.58`
   (`MUSTAR-HALF/RESULT.md:19-21`), with `lambda = 25.6` kept in Table `tab:half` where it
   is the certified row (`MUSTAR-HALF/RESULT.md:27`).

Build after the second round: from-scratch Tectonic, exit `0`, 20 pages, `0` overfull, `0`
underfull, `0` undefined references or citations, `0` em dashes, `0` matches of
`provisional|under repair|pending|being finished|currently sound` in the PDF text.
