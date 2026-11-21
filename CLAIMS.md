# CLAIMS - statement to source map for `main.pdf`

Every statement in `main.tex` maps below to a reviewed source with `file:line`, or is
flagged as derived in this paper or as provisional. Source paths are relative to the
release repository (`records/common-cutoff/`, `records/mustar-half/`,
`records/einstein-opt2/`, `C-LAMBDA/`), and `main.tex` abbreviates `paper/main.tex`
throughout. Paper locations are given by `main.tex` line and by section label.

## 0. Label vocabulary used in the paper

The paper uses exactly one label per statement and carries it in the text, printed as
small capitals `(proved)`, `(certified)`, `(numerical)`, `(open)` and defined in the abstract:
`PROVED` (an argument is given in the paper), `CERTIFIED` (a finite exact computer
assisted certificate exists, verified by two independently written checkers), `NUMERICAL`
(float results that establish no bound), `OPEN` (no result). No statement in the paper is a
measurement, and no statement about any material is made.

**No row below is provisional.** Section 8 was written while its second exact verifier was
under repair and was flagged provisional in this file at that time; the repair landed
(`records/mustar-half/FIX.md`, `records/mustar-half/FIX-INDEP.md`) and an independent
re-review of the current bytes returned PASS (`records/mustar-half/REVIEW3.md:3`) with
`CERTIFIED` allowed for the four instances and the four anchors and `PROVED` for Lemma 1
and Theorems 1 to 5 (`records/mustar-half/REVIEW3.md:13-14`). In Version 2, Section 8.2
adds Lemma `lem:realizable` (`PROVED`), Corollary `cor:unrealizable` and Table
`tab:realizable` (`CERTIFIED`), Lemma `lem:gb` (`PROVED`), Theorem `thm:smallr`
(`CERTIFIED`), Theorem `thm:d2` (`PROVED`), and Corollary `cor:d2cert` (`CERTIFIED`),
following an independent review of the `records/einstein-opt2/` bytes (verdict PASS WITH
FIXES) and of the Version 2 manuscript, both of whose findings are applied. The PDF never
carried the provisional flag.

The reviewed label sets are `records/common-cutoff-review/REVIEW4.md:72-84` (§5, table
with the five rows and their labels, verdict PASS at `REVIEW4.md:4`),
`records/mustar-half/REVIEW3.md:11-15` (§1, table of final claim labels, verdict PASS
at `REVIEW3.md:3`), together with the independent review of the `records/einstein-opt2/`
bytes (verdict PASS WITH FIXES) and of the Version 2 manuscript, which use the same
`PROVED`, `CERTIFIED`, `NUMERICAL` labels as Section 8 below.

## 1. Model, conventions, and the common cutoff (§`sec:model`, `main.tex:154-226`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Flat density of states, infinite band, isotropic even linear Migdal-Eliashberg pairing; pairing-only mask `mu* c_n c_m` on both indices; no Coulomb term in `Z`; strict cutoff; `omega_c` common to every spectrum compared | `records/common-cutoff/RIGOR.md:3-27` (§1) | model definition, as reviewed | no |
| `lambda`, `M`, `Omega_E=sqrt(M/lambda)`, `u=omega^2/Omega_E^2`, `dp=2 alpha^2F d omega/(lambda omega)` a probability measure with `int u dp = 1`; transfer weights `a_j`, `a_0=lambda`, compound Poisson structure | `records/common-cutoff/RIGOR.md:3-16` | model definition | no |
| `mu* = mu/(1+mu ln(E_F/omega_c))` is the quantity a pairing-only subtraction stands for | classical strong-coupling normalization, as in `records/common-cutoff/RESULT.md` §1 and the cited textbooks | interpretative, not used in any bound | no |
| Energies absolute, Matsubara frequencies `(2n+1) pi k_B T`; `k_B T_lin` is a model quantity | `records/common-cutoff/RIGOR.md:3-16` | definition | no |

## 2. Structural reduction (§`sec:reduce`, `main.tex:227-258`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:reduce`: at fixed `(lambda,M)` and common `omega_c` the only parameters are `(R, mu*)` with `R=omega_c/Omega_E=omega_c sqrt(lambda/M)`; the mask is `(2i+1)^2 q < 4R^2`; two spectra compete only at equal `lambda`, equal `M`, equal `R` | `records/common-cutoff/RIGOR.md:28-38` (§2) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| In the fixtures `sum_i lambda_i = lambda` and `sum_i lambda_i u_i = lambda`, so `M`, `Omega_E` and `R^2` coincide with Einstein's exactly | `records/common-cutoff/RIGOR.md:28-38`, `records/common-cutoff/RIGOR.md:325-330` (exact rationals, `structure.py`), `records/common-cutoff/fixtures.json` (`R2` fields) | PROVED | no |
| Exact rational confirmation over 400 random two-line spectra and six `r` values | `records/common-cutoff/RIGOR.md:40-62` (iii), `records/common-cutoff/CHECKS.txt` | PROVED + tool check | no |

## 3. Einstein dominance at zero repulsion (§`sec:dom`, `main.tex:259-310`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Lemma `lem:jensen`: `a_r^E >= a_r` for every `q>0`, `r>=1`; equality for some `r>=1` iff the spectrum is the single line | `records/common-cutoff/RIGOR.md:40-62` (§3(ii), the Jensen step at line 52) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| Lemma `lem:laplace`: exact folded stability form, matrix identity `F_ij = (2i+1+2A_i-a_{2i+1}+2mu* 1_{i<k}) delta_ij - a_{|i-j|} - a_{i+j+1}` for `i != j`, equivalently `F = diag(d_i+2A_i) - T - H + 2mu* 1_{i<k}1_{j<k}` with `T` the Toeplitz and `H` the Hankel part, the Laplacian display form equivalent to it, and the quotient identity | `records/common-cutoff/RIGOR.md:83-116` (§4, matrix form at 83, display form at 93, bookkeeping at 102); exact rational confirmation 120 trials (`records/common-cutoff/RIGOR.md:63-116`, `CHECKS.txt`) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |
| `a_r = lambda int u/(u+qr^2) dp` for a two-line spectrum, with `u_1=(1-p u_2)/(1-p)` | `records/common-cutoff/RIGOR.md:56-62` (iii) | PROVED | no |
| The repulsion adds a positive semidefinite rank-one term on the masked block and acts only along the all-ones direction there | `records/common-cutoff/RIGOR.md:117-131` (§4, Coulomb block) | PROVED (`records/common-cutoff-review/REVIEW4.md:76`) | no |

## 4. Failure of entrywise dominance at positive `mu*` (§`sec:dom`, `main.tex:311-422`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Proposition `prop:rank`: at `mu*>0` every form is the `mu*=0` form plus the same rank-one term; no ordering theorem transfers `a_r` dominance to the forms; the effect is spectrum dependent | `records/common-cutoff/RIGOR.md:117-131` | PROVED (`records/common-cutoff-review/REVIEW4.md:76`, "mechanism for failure of entrywise `a_r` dominance at `mu*>0`") | no |
| Remark `rem:mech`: the zero-repulsion margin that must be overcome is spectrum dependent, so dominance of the phonon entries decides nothing at `mu*>0` | `records/common-cutoff/RIGOR.md:336-358` (§7, the mechanism in the same language) | PROVED (mechanism) | no |
| Corollary `cor:value`: `k_B T_lin <= C(lambda) sqrt(M)` holds at every `mu*>=0`; the ceiling value is Coulomb robust and the optimizer is not | `records/common-cutoff/RIGOR.md:117-131` (rank-one term raises every form), ceiling input from `finite` / `univglue` as cited in the paper | PROVED here (one line from Proposition `prop:rank` plus the reviewed zero-repulsion ceiling); the underlying ceiling is prior work, cited | no |
| Direct full-line values `lambda_max` `4.4033 -> 0.7556` (Einstein) against `3.2054 -> 1.0975` (mixture) at `q=1/200`, for `mu*=0` and `3/2` | `records/common-cutoff/RIGOR.md:132-134` | NUMERICAL (float, `crosscheck.py`) | no |
| Empty-mask observation: if `4R^2 < q_ph(lambda)` then on the nonempty open interval `(4R^2, q_ph(lambda))` the mask is empty, so `F = F_0` there and the Einstein form is indefinite arbitrarily close to `q_ph(lambda)`; hence the Einstein onset stays `q_ph(lambda)` at every `mu* >= 0` and strictly dominates every non-Einstein onset | derived in this paper from Lemma `lem:laplace` and the mask condition of `records/common-cutoff/RIGOR.md:28-38`; not covered by `records/common-cutoff-review/REVIEW4.md` | proved in the paper, elementary, flagged in `main.tex:379-422` as one-line observations | no |
| Large-`q` observation: `a_r <= lambda/(q r^2)`, hence `S_1 <= pi^2 lambda/(6q)`, and the difference part of `F` is bounded below by `-2 S_1 I`, giving `F >= (1-pi^2/12) I > 0` once `q >= 4 lambda` | derived in this paper; the same asymptotic stability statement appears as `records/mustar-half/RIGOR.md:77-131` (§3, asymptotic cutoff stability for `q >= 4 lambda`) | proved in the paper, elementary; the same statement is reviewed inside `records/mustar-half/RIGOR.md` §3 | no |

Note on the two observations: `records/common-cutoff-review/REVIEW4.md` does not list them, so they are **not**
presented as PROVED/CERTIFIED claims derived from that review. They are labelled
and proved inside the paper, in a subsection that says so, and they are not used by any
other result. Deleting them would not change any reviewed statement.

## 5. Certified counterexamples (§`sec:cert`, `main.tex:423-558`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:cert` / Table `tab:cex`: three two-line spectra at `mu*/lambda = 2/3, 3/4, 1` that share `(lambda,M,mu*,omega_c)` with the Einstein line and have strictly larger `T_lin` | `records/common-cutoff/RESULT.md:26-28` (cases, `q_mix`, gains), `records/common-cutoff/RIGOR.md:309-335` (§6), `records/common-cutoff/bounds.json`, `records/common-cutoff/fixtures.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`, first half) | no |
| Einstein `q_E` brackets `[0.0083,0.0095]`, `[0.0009,0.003]`, `[129/500000,0.003]`; hot intervals `[q_hi, q_ph(lambda))` | `records/common-cutoff/bounds.json`, `records/common-cutoff/RIGOR.md:309-335`, `records/common-cutoff/RESULT.md:26-28` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| `C_E` brackets `[0.00837140,0.00895615]`, `[0.00337618,0.00616405]`, `[0.00127820,0.00435864]`, rounded outward at eight decimals from the exact `sqrt(q_lo)` and `sqrt(q_hi)` of each certified `q_E` bracket | `records/common-cutoff/bounds.json`, `records/common-cutoff/RESULT.md:26-28` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| Two-line spectra `590/599` at `u=1/10` with `9/599` at `60`; `4975/4998` at `2/25` with `23/4998` at `200`; `2475/2498` at `2/25` with `23/2498` at `100`; `sum p_i = 1`, `sum p_i u_i = 1` exactly | `records/common-cutoff/RIGOR.md:325-335`, `records/common-cutoff/fixtures.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:76-78`) | no |
| Temperature gain `sqrt(q_mix/q_hi)-1` is a lower bound on the gain, with the displayed values `>=2.59%`, `>=29.09%`, `>=82.57%` | computed here from the exact rationals `q_mix` and `q_hi` of `records/common-cutoff/bounds.json` and `records/common-cutoff/fixtures.json`; the rounded source figures are `2.6%, 29%, 83%` (`records/common-cutoff/RESULT.md:26-28`, `records/common-cutoff-review/REVIEW4.md:74`) | arithmetic consequence of the CERTIFIED brackets | no |
| Certification method: cold witness exact with no tail bound; hot cover by entrywise integer enclosure, diagonal radius penalty, Schur complement against a Gershgorin gap, exact residual with strict diagonal dominance; mask jump split points | `records/common-cutoff/RIGOR.md:139-215` (§5, enclosure at 201-215), `records/common-cutoff/CHECKS.txt:72-75` (573003 exact rational entry comparisons, radius slack up to 45239 integer units at scale 2**17), `records/common-cutoff/FIX2.md:290` | PROVED/CERTIFIED machinery, as reviewed | no |
| Two verifiers share no code and no formulation: different `pi` enclosures (Machin against `arctan 1/2 + arctan 1/3`), folded against unfolded | `records/common-cutoff/RIGOR.md:139-215`, `records/common-cutoff/CHECKS.txt` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:9-19`, `20-28`) | no |
| Nine mutants of the two exact verifiers (five in the first, four in the second), each with an unmutated control, each refused with an exit code and a message naming the statement | `records/common-cutoff/RIGOR.md:285-305` (mutant table), `records/common-cutoff/CHECKS.txt:19-30` (one row per mutant), `records/common-cutoff/FIX2.md:284-295` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:43-71`) | no |
| All 20 `CHECKS.txt` rows pass with their expected exit codes, no broken control | `records/common-cutoff/CHECKS.txt`, `records/common-cutoff-review/REVIEW4.md:43-71` | CERTIFIED | no |
| Receipt check: stored certificate fields recomputed and compared; a shaved `C_E` bracket is refused | `records/common-cutoff/RIGOR.md:165-215`, `records/common-cutoff/CHECKS.txt` | CERTIFIED | no |
| Box counts `19`, `36`, `37` and `10`, `12`, `14`, `11` for the seven hot covers (the second verifier's counts; `records/common-cutoff/bounds.json` stores the first verifier's own counts `18`, `36`, `37`, `10`, `18`, `14`, `11`, checked as a receipt) | `records/common-cutoff/CHECKS.txt` Note 2, `records/common-cutoff/RIGOR.md:309-335`, `records/common-cutoff/bounds.json` | CERTIFIED | no |

## 6. Certified brackets and the calibration (§`sec:brackets`, `main.tex:559-622`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:brackets`, seven Einstein `q_E` brackets and `C_E` brackets, four of them at `mu*/lambda <= 1/2` | `records/common-cutoff/RESULT.md:55-60`, `records/common-cutoff/bounds.json` | CERTIFIED (`records/common-cutoff-review/REVIEW4.md:78`) | no |
| `q_ph(lambda)` is the zero-repulsion Einstein onset of the fixed-`(lambda,M)` problem, and every spectrum is stable at `q > q_ph` (that is the ceiling statement) | definition in `main.tex:210-217`; outward six-digit upper endpoints `q_ph^hi(1) = 0.518654`, `q_ph^hi(2) = 1.77000`, `q_ph^hi(3) = 3.07270`, `q_ph^hi(4) = 4.38414`, `q_ph^hi(10) = 12.2824` computed from `C-LAMBDA/brackets.json`, as quoted in `records/common-cutoff/RIGOR.md:161-163`, `records/common-cutoff/RESULT.md:64-74`, `:225-226`, `records/common-cutoff/FIX2.md:289` | PROVED (from the reviewed zero-repulsion ceiling) | no |
| The right endpoint of every hot interval is an outward display of the certified upper endpoint `q_ph^hi(lambda) >= q_ph(lambda)`; the certified range and Corollary `cor:value` together cover every larger `q` with no gap | `records/common-cutoff/RESULT.md:225-226`, `records/common-cutoff/FIX2.md:289`, `records/common-cutoff/RESULT.md:72-74`, `C-LAMBDA/brackets.json` (`q_numerators`, denominator `10^11`) | CERTIFIED | no |
| Zero-repulsion calibration `C(1) in [0.11461945, 0.11461957]`, i.e. `q in [0.51865242539,0.51865346269]`, distinct from the `mu*=1/10` anchor | `records/common-cutoff/RESULT.md:64-70`, `C-LAMBDA/brackets.json` | CERTIFIED upstream (`records/common-cutoff-review/REVIEW4.md:80`) | no |
| `mu*=1/10` anchor `C_E in [0.088327408,0.088685156]` is strictly below the zero-repulsion value | `records/common-cutoff/RESULT.md:64-70` | CERTIFIED | no |
| Monotone chain `0.1146194547`, `0.1610715064` at `lambda=3`, `0.1763847604` at `lambda=10`, `0.18272624777232952` as `lambda -> infinity` | `C-LAMBDA/RESULT.md:18`, `:22`, `:25`; limit constant from `univglue` (§`C_inf`) and `gamma` | CERTIFIED upstream | no |

## 7. Direct-discretization cross-check (§`sec:num`, `main.tex:623-667`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Table `tab:direct`: onsets `0.0083924335`, `0.00090451693`, `0.00025806035` and `T_mix/T_E = 1.21, 2.92, 9.96` | `records/common-cutoff/RESULT.md:130-134` | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Band doubling `|n|<=240 -> |n|<=480` shifts `lambda_max` by at most `6.4e-5` and flips no sign | `records/common-cutoff/RIGOR.md:396-405` (§8 item 5/6) | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Small-`mu*` controls: Einstein `lambda_max` `1.0032` against mixture `0.1817` at `q=0.308`; `1.0058` against `0.4133` at `q=0.0112` | `records/common-cutoff/RESULT.md:135-136`, `records/common-cutoff/RIGOR.md:396-405` | NUMERICAL (`records/common-cutoff-review/REVIEW4.md:82`) | no |
| Direct even-sector eigenvalue agrees with the folded form to `4.4e-16` on all seven instances | `records/common-cutoff/RESULT.md:137-148` | NUMERICAL | no |

## 8. Below one half: certified instances, analytic regimes, numerical phase data (§`sec:half`, `main.tex:668-1543`)

Section 8 has three parts: the certified instances (`sec:half:cert`, `main.tex:696-840`), the
proved and certified analytic statements (`sec:half:proof`, `main.tex:841-1433`), and the numerical phase
data (`sec:half:num`, `main.tex:1434-1543`). Labels follow
`records/mustar-half/REVIEW3.md:13-14` (verdict PASS at `records/mustar-half/REVIEW3.md:3`) and
the independent review of the `records/einstein-opt2/` bytes (verdict PASS WITH FIXES, all
findings applied):
`CERTIFIED` for the four counterexamples, the four anchors, Corollary `cor:unrealizable` / Table `tab:realizable`,
Theorem `thm:smallr`, and Corollary `cor:d2cert`; `PROVED` for
Lemmas `lem:decomp`, `lem:realizable`, `lem:gb` and Theorems `thm:twodelta`, `thm:nomask`,
`thm:large`, `thm:cone`, `thm:asym`, `thm:d2`; `NUMERICAL` for the phase scans and
the direct values.

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Theorem `thm:half` / Table `tab:half`: four rational two-line spectra at `mu*/lambda = 61261/128000`, `12/25`, `1309/2700`, `489/1000`, each sharing `(lambda,M,mu*,omega_c)` with the Einstein line, with certified margins `q_mix/q_hi >= 1.0476, 1.0379, 1.2171, 1.1893`, that is temperature gains `>= 2.353, 1.878, 10.326, 9.055` percent | `records/mustar-half/RESULT.md:23-30` (cases), `records/mustar-half/bounds.json`, `records/mustar-half/fixtures.json` | CERTIFIED (`records/mustar-half/REVIEW3.md:13`) | no |
| `q_E` and `C_E` brackets `[0.519,0.525]` / `[0.02266124,0.02279187]`; `[0.495,0.501]` / `[0.02196018,0.02209288]`; `[0.414,0.419]` / `[0.01970781,0.01982647]`; `[0.407,0.412]` / `[0.01918838,0.01930589]`, eight-decimal outward rounding of the exact rational brackets | `records/mustar-half/bounds.json`, `records/mustar-half/RESULT.md:23-30` | CERTIFIED (`records/mustar-half/REVIEW3.md:13`) | no |
| Spectra `1-6.0e-6` at `0.88` with `6.0e-6` at `20000`, that is `499975/499978` at `22/25` with `3/499978` at `20000`; `1-2.0e-5` at `0.8` with `2.0e-5` at `10000`; `1-1.55e-4` at `0.69` with `1.55e-4` at `2000`; `1-3.6e-4` at `0.64` with `3.6e-4` at `1000` | `records/mustar-half/fixtures.json`, `records/mustar-half/RESULT.md:23-30` | CERTIFIED (`records/mustar-half/REVIEW3.md:13`) | no |
| Four Einstein anchors `anchor-l2-mu1-R3/2`, `anchor-l3-mu3/2-R2`, `anchor-l10-mu4-R3`, `anchor-l20-mu19/2-R5` at `mu*/lambda` `0.500`, `0.500`, `0.400`, `0.475`, with their `q_E` and `C_E` brackets | `records/mustar-half/RESULT.md:32-39`, `records/mustar-half/bounds.json` | CERTIFIED (`records/mustar-half/REVIEW3.md:13`) | no |
| Lemma `lem:decomp`: exact finite-support decomposition of the form into the free term, the masked rank-one term and the weight sum `sum_j a_j L_j` | `records/mustar-half/RIGOR.md:31` | PROVED (`records/mustar-half/REVIEW3.md:14`) | no |
| Theorem `thm:twodelta`: at fixed `(q,k,mu*)` the infimum of `lambda_min(F_p^(k)(q))` over `P_1` equals the infimum over two-line spectra, on the finitely supported form core | `records/mustar-half/RIGOR.md:53`, `records/mustar-half/RESULT.md:15` | PROVED (`records/mustar-half/REVIEW3.md:14`) | no |
| Theorem `thm:nomask`: whenever `4R^2 < q_E(lambda,0)`, the mask is empty on an open neighbourhood of `[q_E(lambda,0),inf)` and Einstein strictly maximizes `T_lin` for all `mu* >= 0`; strictness is needed, and the statement is conditional on the zero-repulsion ceiling theorem of `C-LAMBDA/RIGOR.md` | `records/mustar-half/RIGOR.md:60`, `records/mustar-half/RESULT.md:16` | PROVED (`records/mustar-half/REVIEW3.md:14`, conditional on the cited ceiling theorem) | no |
| Theorem `thm:large`: for fixed `R > 0`, `lambda >= 4R^2+1` implies `q_ph(lambda) > lambda-1 >= 4R^2` and strict Einstein optimality for every `mu* >= 0` | `records/mustar-half/RIGOR.md:66` | PROVED (`records/mustar-half/REVIEW3.md:14`) | no |
| Theorem `thm:cone`: on the single-mode window `4R^2/9 <= q < 4R^2`, `mu* <= 1+a_1(q;p)` gives a simple positive nonincreasing ground state, every `L_j(h*) < 0` and strict Einstein dominance; the condition holds unconditionally for `mu* <= 1` and for `lambda <= 2` throughout `mu*/lambda <= 1/2` | `records/mustar-half/RIGOR.md:81-115`, `records/mustar-half/RESULT.md:17` | PROVED (`records/mustar-half/REVIEW3.md:14`) | no |
| The sharpness example of Theorem `thm:cone`: at `lambda=152`, `mu*=76`, `q=4.33295` the two-line spectrum `(u_1,u_2)=(1e-5,17.5)` has `lambda_min = -6.717e-5 < 0` while `h*_0 < h*_1` already at `lambda=20` | `records/mustar-half/RESULT.md:18`, `records/mustar-half/RESULT.md:66,70` | NUMERICAL (`records/mustar-half/REVIEW3.md:15`) | no |
| Theorem `thm:asym`: for every `lambda>0`, `mu*>=0`, `R>0` and `p`, `q >= 4 lambda` gives `F_p >= (1-pi^2/12) I`, the hot-side handoff `q_asym = 4 lambda` | `records/mustar-half/RIGOR.md:117-131` | PROVED (`records/mustar-half/REVIEW3.md:14`) | no |
| Structural checker: exact verification of the cone pairing difference, the modified diagonal ordering, Theorem `thm:large` and Lemma `lem:decomp` on the probes, with three guarded negative controls refused | `records/mustar-half/RIGOR.md:168-177`, `records/mustar-half/CHECKS.txt` | PROVED machinery, as reviewed (`records/mustar-half/REVIEW3.md:14`) | no |
| Two independent exact verifiers certify all eight instances (folded full-line cold form with a Schur-complement tail against unfolded with a Cauchy-Schwarz per-row tail, Machin against Hutton `pi`); thirteen mutants (five in `replay.py`, eight in `independent.py`) are refused with their controls passing; self-check and adversarial probes pass | `records/mustar-half/FIX-INDEP.md:3-4,63-66`, `records/mustar-half/REVIEW3.md:5,13,76`, `records/mustar-half/CHECKS.txt` | CERTIFIED (`records/mustar-half/REVIEW3.md:13`) | no |
| Unstable `q_mix` `0.55, 0.52, 0.51, 0.49`, gains `>=2.353%`, `>=1.878%`, `>=10.326%`, `>=9.055%` as the exact arithmetic of each certified bracket pair | `records/mustar-half/RESULT.md:23-30`, `records/mustar-half/bounds.json` | CERTIFIED bracket arithmetic (`records/mustar-half/REVIEW3.md:13`) | no |
| Direct `T_mix/T_E` `1.03295`, `1.02446`, `1.16047`, `1.18148` on a 600-point window | `records/mustar-half/RESULT.md:23-30` (column "True `T_mix/T_E`", `N=600`), `records/mustar-half/REVIEW3.md:15` | NUMERICAL (`records/mustar-half/REVIEW3.md:15`) | no |
| Lemma `lem:realizable`: exact realizability conditions `(2k-1)^2 q_E^(k) < 4R^2 <= (2k+1)^2 q_E^(k)`, non-preemption at lower masks `m in {0,...,k-1}`, non-preemption of every competitor on `(q_lin(p),4lambda)`, necessary lower bound `q_E^(k)(lambda,mu*) >= q_ph(lambda)/(2k+1)^2`, and dichotomy when `(2k+1)^2 q_E^(k) < q_ph(lambda)` | `main.tex:1074-1124` | PROVED | no |
| Corollary `cor:unrealizable` / Table `tab:realizable`: certified strict separation `9 q_E^(1)(lambda,lambda/2) < 9 q_1^hot(lambda) < q_0^cold(lambda) < q_ph(lambda)` for all `lambda in {10,20,25,35,50,65,152}` (`171` rational boxes) and certification of the `lambda=152`, `mu*=76` fixed-`k=1` witness (`theta=33333/583333`, `q_test=8671/2000`, `66` boxes) as genuine at fixed `k=1` yet unrealizable under any common cutoff `R>0` | `main.tex:1147-1190`, `records/einstein-opt2/bounds.json` (`realizability_audit`) | CERTIFIED | no |
| Lemma `lem:gb`: exact two-line difference kernel `B_j(q;t_1,t_2)` and affine decomposition `F_{p_2}^(k)(q) = (1-eta) F_{delta_1}^(k)(q) + eta (G_B^(0)(lambda;q,t_1,t_2) + 2 mu* chi_k chi_k^T)` with `0 < b_{GB,j} < lambda/(q j^2)` | `main.tex:1196-1229` | PROVED | no |
| Theorem `thm:smallr`: explicit small-repulsion optimality threshold `r_0 = 1/64` across all `lambda in [3/10,3]`, `mu* in [0, r_0 lambda]`, `R >= 0` and `p in P_1 \ {delta_1}` (`2,361` rational boxes across `33` slabs), strict dominance on non-cliff instances, and exact onset tie `q_lin(p_eps) = q_lin(delta_1) = 962/625` at `lambda=2`, `mu*=1/32`, `4R^2 = 29^2 q_cliff` (`36` boxes across `9` active mask windows) | `main.tex:1248-1275`, `records/einstein-opt2/bounds.json` (`target2_r0_1over64`, `jump_cliff_obstruction`) | CERTIFIED | no |
| Theorem `thm:d2`: exact second-variation operator `D_2(lambda,q)` and `q`-derivative operator `D_1(lambda,q)`, and local strict maximality at non-cliff onsets when `F_{delta_1}^(k)(q_E) + D_2(lambda,q_E) > 0` and `F_{delta_1}^(k)(q_E) + D_1(lambda,q_E) > 0` | `main.tex:1309-1364` | PROVED | no |
| Corollary `cor:d2cert`: certified positivity of `F_{delta_1}^(k)(q) + D_2(lambda,q)` and `F_{delta_1}^(k)(q) + D_1(lambda,q)` across all `33` slabs of `[3/10,3]` (`383` boxes: `266` for `D_2`, `117` for `D_1`) and at the certified upper onset bound `q_E^(k)` for all `20` benchmarks `(k,lambda) in {1,2,3,4} x {1/2,1,2,5,10}` at `mu*/lambda = 1/2` (`352` hot boxes plus `20` `D_2` boxes and `20` `D_1` boxes), with the explicit distinction between local non-degeneracy at `q_E^(k)` and global stability over all `q > q_E^(k)` | `main.tex:1390-1415`, `records/einstein-opt2/bounds.json` (`target3_d2_k1_to_4`) | CERTIFIED | no |
| Third pair of independent exact verifiers (`records/einstein-opt2/replay.py` and `records/einstein-opt2/independent.py`) with `14` guarded mutants (`8` in `replay.py` and `6` in `independent.py`) all exiting `1` | `records/einstein-opt2/replay.py`, `records/einstein-opt2/independent.py`, `records/einstein-opt2/README.md` | CERTIFIED | no |
| Phase data: `mu*/lambda = 1/2` holds numerically for all `lambda < 25.55` and mask counts `k in {0,1,2,3,4}`; above that a `k=5` window `lambda in [25.55,34.0]`, `omega_c/Omega_E in [3.2,3.6]` dips to `r_min ≈ 0.4785` at `lambda ≈ 25.58`, `omega_c/Omega_E ≈ 3.36`; `9 q_E^(1)(lambda,lambda/2) >= q_ph(lambda)` holds for `lambda in {0.5,1,2,3,5}` (passing up to `lambda ≈ 9.85`); Table `tab:phase` with corrected active-mask column `k` at `lambda=10` (`1 -> 2`) and `lambda=20` (`1 -> 5`) | `records/mustar-half/RESULT.md:11,19-21,41-57`, `main.tex:1468-1522` | NUMERICAL | no |

## 9. What is not claimed (§`sec:not`, `main.tex:1544-1588`) and open problems (§`sec:open`, `main.tex:1589-1631`)

| Paper statement | Source | Label | Provisional |
|---|---|---|---|
| Einstein optimality is open in the interior of `mu*/lambda <= 1/2` outside the proved and certified regimes (including uniform `r_0 > 0` as `lambda -> 0` or `lambda -> infinity` and `1/64 < mu*/lambda <= 1/2` above `mu* = 1`), and one half is not a threshold | `records/mustar-half/RESULT.md:11,74-75`, `main.tex:1544-1631` | OPEN | no |
| The exact threshold curve, its full extent, the critical coupling of the `k=5` window and the fixed-`k=1` matrix failure from `lambda=152` (which is unrealizable by any common cutoff `R>0` by Corollary `cor:unrealizable`, while its fixed-`k=1` witness at `lambda=152` is certified) are numerical | `records/mustar-half/RESULT.md:19-21,66,70,75`, `main.tex:1468-1522` | NUMERICAL / CERTIFIED | no |
| No measured `T_c`, no material prediction, no priority claim, no claim about other Coulomb kernels | scope section of `records/common-cutoff/RIGOR.md:359-405` (§8, honest qualifications) | scope | no |
| Rens arXiv:2611.20496 Thms 3, 4, 6 and Kondratev Prop. 1 are zero-Coulomb results and do not settle the positive-`mu*` question | `records/common-cutoff/RIGOR.md:396-405` (§8 item 6) | prior-work scope | no |

## 10. Deviations and repair log for Version 1

1. `records/common-cutoff-review/REVIEW4.md:88` P3 nit 1 (reversed enclosure direction) is written correctly here:
   `main.tex:460-462` states `C - R <= 2^17 F_ij <= C + R` for every off-diagonal entry,
   matching the code direction `(base-radius)[off] <= lower[off] <= upper[off] <=
   (base+radius)[off]`.
2. `records/common-cutoff-review/REVIEW4.md:89` P3 nit 2 (the factor 2.6/4.3/7 discrepancy attributed to a `(u,p)`
   unpack swap) is not repeated: the paper never attributes that discrepancy to a swap.
   The only swap mentioned (`main.tex:519-522`) is the mutant that must be refused.
3. Rounded source figures "at least 2.6, 29, 83 percent" (`records/common-cutoff/RESULT.md:26-28`,
   `records/common-cutoff-review/REVIEW4.md:74`) are printed as the exact floors `2.59`, `29.09`, `82.57` percent,
   because `sqrt(q_mix/q_hi)-1` evaluates to `2.597835%`, `29.099445%`, `82.574186%`;
   the same treatment is applied to the four sub-half gains.
4. The sharp scalar constant `C_inf = 0.18272624777232952` is cited to `univglue`
   (addendum `anisosharp` states the same value), not to `optimum`: the released
   bibliography of the coupled-branch papers gives `optimum` the coefficient
   `sqrt(377/250)/(2pi)` approximately `0.19544330695` and imports `C_inf` from the
   scalar ceiling (`refs.bib`, entries `finite`, `predecessor`). All DOI and title pairs
   are copied from those released bibliographies.
5. The two elementary observations of §`sec:dom` (empty mask, large `q`) are derived in
   the paper and are not part of the reviewed label set; see the note in §4 above.
6. The sub-half section was first written while the second exact verifier was under repair,
   with a provisional flag in this file and a REJECT verdict for `CERTIFIED`
   (`records/mustar-half/REVIEW.md:3`). `records/mustar-half/FIX.md` and
   `records/mustar-half/FIX-INDEP.md` then landed, `records/mustar-half/REVIEW3.md:3`
   returned PASS, and Section 8 was upgraded to the labels `REVIEW3.md:13-14` allows,
   with the phase data left NUMERICAL.

## 11. Preprint review fixes (independent review of the Version 1 manuscript, verdict PASS-WITH-FIXES)

The Version 1 pre-fix manuscript copy and its statement-map copy are not part of this
release tree; the released Version 1 bytes are the archived artifact of preprint Version 1.
Nothing in the independent review was edited.

| Finding | Severity | Change | Location |
|---|---|---|---|
| F1 | P0 | the onset was defined as a supremum over stable temperatures; it is now `k_B T_lin = sup{k_B T : F not >= 0}`, consistent with the following sentence | `main.tex:205` |
| F2 | P0 | the extraneous `sqrt(lambda)` is removed from Corollary `cor:value`; the ceiling is `C(lambda) sqrt(M) <= C_inf sqrt(M)` | `main.tex:327` |
| F3 | P0 | all seven `C_E` brackets were rounded inward in v1; each is now eight-decimal rounding outward from the exact rational bracket, checked against `records/common-cutoff/bounds.json` endpoint by endpoint | `main.tex:437,439,441` (Table `tab:cex`), `main.tex:571-577` (Table `tab:brackets`), `main.tex:598,600` (prose), this file §5 and §6 |
| F4 | P1 | E1 decimal weights corrected to `0.984975` at `0.1` and `0.015025` at `60` (exact `590/599` and `9/599`) | `main.tex:438` |
| F5 | P1 | the obstruction copied from a Lorentzian-width context is deleted and replaced by the sign flip inside single entries of the folded form, `F_ii = d_i+2A_i-a_{2i+1}+2mu*[i<k]` against `F_ij = -a_{|i-j|}-a_{i+j+1}` | `main.tex:340-348` |
| F6 | P1 | the empty-mask argument no longer invokes the rank-one term, which is positive semidefinite and cannot preserve indefiniteness; it uses the empty mask on the open interval `(4R^2, q_ph(lambda))` | `main.tex:383-387` |
| F7 | P1 | all process language is removed from the PDF: `provisional`, `currently sound`, `is being finished`, `expected to be replaced or withdrawn`, `upgrade or replace`, and the truncation wording | `main.tex` throughout |
| F8 | P2 | the hot-interval caption now states that the printed right endpoint is an outward display of `q_ph^hi(lambda) >= q_ph(lambda)`, so the certified range plus Corollary `cor:value` cover every larger `q` with no gap; the displayed endpoints are outward (`0.518654`, `1.77000`, `3.07270`, `4.38414`, `12.2824`) | `main.tex:571-577`, `main.tex:580-589` |
| F9 | P2 | the normal diagonal is written as dimensionless, `D_n = Z_n|omega_n|/(pi k_B T) = |2n+1| + a_0 + 2 sum_j a_j` | `main.tex:182` |
| F10 | P2 | this file only: empty-mask row (§4), folded matrix identity (§3), box-count citation moved to `CHECKS.txt` Note 2 with the stored first-verifier counts recorded (§5), `C_E` row (§5), hot-endpoint row (§6), one-verifier row (§8), every section line range renumbered, and §0 restated | this file |
| F11 | P3 | `Migdal--Eliashberg` on the last open-problem item, and Table `tab:brackets` names `E1, E2, E3` and `A1, A2, A3, A4` instead of "the rows above them" | `main.tex:587`, `main.tex:794` |
| P12 (`records/common-cutoff-review/REVIEW4.md` §6 item 1) | P3 | the enclosure direction is stated as soundness requires it, `C_ij - R_ij <= F_ij(q_lo)` and `F_ij(q_hi) <= C_ij + R_ij`, with the monotonicity of the off-diagonal entries in `q` supplying the direction | `main.tex:505-507` |
| P13 (`records/common-cutoff-review/REVIEW4.md` §6 item 2) | P3 | the mirror term is described as automatic in any discretization that spans the negative Matsubara axis, and the earlier `2.6` to `7` disagreement is attributed to four defects of the earlier direct implementation (bosonic frequencies, a doubled `lambda`, a wrong normal diagonal, an unsymmetrized kernel), not to a weight-position unpacking | `main.tex:300-303`, `main.tex:628-632` |

## 12. Second repair round (after the Version 1 section 8 upgrade)

1. Section 8 gained the analytic subsection and the certified labels of
   `records/mustar-half/REVIEW3.md:13-14` (§10 item 6), and the whole section states its
   evidence standard once.
2. Every entry of Table `tab:phase` was verified against `records/mustar-half/RESULT.md:45-58`
   with a comparison script that normalizes the typesetting only.
3. The caption and the readings of Table `tab:phase` were rewritten so that the meaning of
   the `infinity` cells, of the rows whose infimum reads one half, and of the mask-count
   column match what the scan computes.
4. `r_min` is quoted at the coupling of the source's finer estimate, `lambda ≈ 25.58`
   (`records/mustar-half/RESULT.md:19-21`), with `lambda = 25.6` kept in Table `tab:half`
   where it is the certified row (`records/mustar-half/RESULT.md:27`).

## 13. Third round (section 8 delta review, verdict PASS-WITH-FIXES, zero P0 and zero P1)

| Item | Change | Location |
|---|---|---|
| D1 | the first verifier's hot head size is `n = 240`, not `m = 200`; only the second verifier uses `m = 200` (`records/mustar-half/fixtures.json`, `replay.py` head build) | `main.tex:754` |
| D2 | the four second-verifier margins are stated to be in that verifier's `2^22`-scaled integer units with a strictly positive integer Gershgorin gap, and the rejected entrywise-bound witness states that both quadratic forms are on that same scale (`records/mustar-half/CHECKS.txt:26`) | `main.tex:770`, `main.tex:790` |
| D3 | the Section 8.1 command count is twenty-one, not twenty (`records/mustar-half/CHECKS.txt`); only the structural checker has a combined-mutant mode, and the self-test loses its unfounded ordinal | `main.tex:782`, `main.tex:795`, `main.tex:799` |
| D4 | the abstract attributes the sub-one-half certificates to the second pair of exact verifiers in the same two roles; Section 9 item 4 reads `above and below one half`; Theorem `thm:large` is recorded as inheriting the zero-repulsion dependency of Theorem `thm:nomask` | `main.tex:53`, `main.tex:846`, `main.tex:1576`, `main.tex:1585` |

## 14. Version 2 (`records/einstein-opt2/` integration)

The released Version 1 manuscript has sha256
`3e18408a59fc3f8c2c42ed257d3638fb874ec67f6eea03c7aedba287ea8f8d9e`. Version 2 adds:

1. A "Changes in Version 2" subsection in Section 1 (`main.tex:132-152`) stating what was
   added, what was corrected in the numerical phase table, the Version 1 DOIs
   (`10.5281/zenodo.24409773` and `10.5281/zenodo.24409779`), and that no `PROVED` theorem
   or `CERTIFIED` table of Version 1 changed.
2. Lemma `lem:realizable` (`PROVED`), Corollary `cor:unrealizable` (`CERTIFIED`), and
   Table `tab:realizable` (`CERTIFIED`) in Section 8.2 (`main.tex:1074-1190`), establishing
   the exact necessary conditions for a common cutoff `R` to realize a fixed-`k` crossing
   and certifying `9 q_E^(1) < q_ph(lambda)` across `lambda in {10,20,25,35,50,65,152}` at
   `mu*/lambda = 1/2`.
3. Lemma `lem:gb` (`PROVED`), Theorem `thm:smallr` (`CERTIFIED`), Theorem `thm:d2`
   (`PROVED`), and Corollary `cor:d2cert` (`CERTIFIED`) in Section 8.2 (`main.tex:1196-1415`),
   establishing the explicit small-repulsion threshold `r_0 = 1/64` on `lambda in [3/10,3]`
   for all `R >= 0`, the exact jump-cliff onset tie at `lambda=2, mu*=1/32, q_cliff=962/625,
   4R^2=29^2 q_cliff`, and the second-variation operator `D_2(lambda,q)` with its certified
   positivity on the `33` slabs and `20` fixed-`k` benchmarks.
4. Correction of the numerical Section 8.3 reading (3) and the last column `k` of
   Table `tab:phase` (`main.tex:1434-1523`) at `lambda=10` (`1 -> 2`) and `lambda=20`
   (`1 -> 5`).

## 15. Version 2 pre-release review fixes (independent review of the Version 2 manuscript)

The pre-fix Version 2 manuscript copy, its statement-map copy, its build record and its
supplement README are not part of this release tree. Nothing in the independent review was
edited.

| Finding | Severity | Change | Location after fix |
|---|---|---|---|
| P1-1 | P1 | restored necessary ("only if") conditions in Lemma `lem:realizable`(a): mask-window containment `(2k-1)^2 q_E^(k) < 4R^2 <= (2k+1)^2 q_E^(k)`, non-preemption at lower masks `m in {0,...,k-1}`, and non-preemption of every competitor on `(q_lin(p), 4lambda)`; fixed the definition `k(q,R) = |{i>=0 : (2i+1)^2 q < 4R^2}|` and stated that `k(q,R)` is right-continuous in `q` and left-continuous in `R^2` | `main.tex:1074-1124` |
| P1-2 | P1 | inserted exact `theta = (1-u_1)/(u_2-u_1) = 33333/583333` in Corollary `cor:unrealizable` (`main.tex:1158`), eliminating the `10^-9` moment violation of the decimal approximation `19999/174990` | `main.tex:1156-1163` |
| P1-3 | P1 | restored all three hypotheses in Theorem `thm:d2` (`q_E` not a jump cliff, non-preemption of Einstein at lower masks, and non-preemption of perturbations at higher `q`), split the analytic statement `thm:d2` (`PROVED`) from the finite-certificate Corollary `cor:d2cert` (`CERTIFIED`), and added the scope note that fixed-`k` positivity at `q_E^(k)` certifies local non-degeneracy near `q_E^(k)` while global stability over all `q > q_E^(k)` is certified on the `33` slabs of Theorem `thm:smallr` | `main.tex:1309-1415`, this file §8 |
| P1-4 | P1 | recomputed the exact crossing of `9 q_E^(1)(lambda,lambda/2) = q_ph(lambda)` (`lambda ≈ 9.85`, with `q_0^cold / (9 q_1^hot) = 122818/122229 ≈ 1.004819 > 1` certified at `lambda=10`), corrected `5.85` to `9.85`, and narrowed the `lambda=10` active-mask entry in Table `tab:phase` and Section 8.3 reading (3) to `k=2` (the lowest realizable non-empty mask count at `mu*/lambda = 1/2`) | `main.tex:137-146`, `main.tex:1444-1466`, `main.tex:1513`, `main.tex:1533` |
| P1-5 | P1 | rewrote `records/einstein-opt2/README.md` so every theorem number (`Lemma 8.8`, `Corollary 8.9`, `Table 6`, `Lemma 8.10`, `Theorem 8.11`, `Theorem 8.12`, `Corollary 8.13`, `Table 7`), box count (`171 + 66`, `2,361`, `18 + 18`, `352 + 20 + 20`, `266 + 117`), CLI flag (`--mutants`, `--mutant <name>`, `--bounds <path>`) and mutant list (`8` in `replay.py`, `6` in `independent.py`) matches `bounds.json`, the scripts, and `main.pdf`; regenerated `records/einstein-opt2/SHA256SUMS` | `records/einstein-opt2/README.md`, `records/einstein-opt2/SHA256SUMS` |
| P1-6 | P1 | made the supplement self-contained: the release tree carries `C-LAMBDA/`, `records/common-cutoff/` and `records/mustar-half/` verbatim from Version 1 next to the Version 2 record `records/einstein-opt2/`, so every replay command named in the paper and in the records resolves inside the tree | `C-LAMBDA/`, `records/common-cutoff/`, `records/mustar-half/`, `records/einstein-opt2/`, `MANIFEST.sha256` |
| P2-1 | P2 | added the Version 1 DOIs (`10.5281/zenodo.24409773` and `10.5281/zenodo.24409779`) in Section 1 (`Changes in Version 2`) and the Data Availability section | `main.tex:133-135` |
| P2-2 | P2 | updated Section 9 (`sec:not`) and Section 10 (`sec:open`) to reflect Version 2's proved and certified results (`lem:realizable`, `cor:unrealizable`, `lem:gb`, `thm:smallr`, `thm:d2`, `cor:d2cert`) and the settled `r_*(lambda,R) >= 1/64` lower bound on `lambda in [3/10,3]` | Sections 9 and 10 (`main.tex:1544-1631`) |
| P2-3 | P2 | sanitized all private working-tree paths and lane names in `BUILD.md` and `CLAIMS.md` to repository-relative paths | `BUILD.md`, `CLAIMS.md` |
| P3-1 | P3 | defined `b_{eff,2,j} = lambda(1+x+x^2)/(1+x)^3` and `b_{eff,1,j} = lambda/(1+x)^2` (with `x = q j^2`) explicitly in the proof of Theorem `thm:d2` before using them | `main.tex:1422-1426` |
| P3-2 | P3 | reduced the unreduced fractions in Corollary `cor:unrealizable` and Table `tab:realizable` (`8671/2000`, `81253/1250`, `49863/250`) to match `bounds.json` | `main.tex:1158`, `main.tex:1179,1181` |
| P3-3 | P3 | pinned `SOURCE_DATE_EPOCH=1795132800` in `BUILD.md` and rebuilt `main.pdf` deterministically | `BUILD.md:12,33`, `main.pdf` |

Build of Version 2 after all findings of both independent reviews: from-scratch Tectonic
with `SOURCE_DATE_EPOCH=1795132800`, exit `0`, 26 pages, `0` overfull, `0` underfull, `0`
undefined references or citations, `0` LaTeX warnings in `main.log`, `0` em dashes, `0`
forbidden tokens in `main.tex` or `main.pdf`. The only change to the reviewed bytes after
the re-review is the restoration of the `\bottomrule` that closes Table 6
(`tab:realizable`), recorded in `BUILD.md`. Bytes:
`main.tex` sha256 `0eb17fe0de77bb723bcec2233baf3edd752e77fb0c1d6a238d6cd93d56588894`,
`refs.bib` sha256 `9d56e7292d499f044b6eaf12df61ea7aec5cf216b2f2995b873a1667f4264cd2`,
`main.pdf` sha256 `9d3bd9975260cc255a6f1b30dd56d018ae6e5afbaaa6b4cee5c24f5387a3bb55`.
