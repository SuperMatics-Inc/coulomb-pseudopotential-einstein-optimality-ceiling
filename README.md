# The Coulomb pseudopotential and the optimality of the Einstein spectrum for the linear Eliashberg ceiling

Davis Rens  
SuperMatics Inc.  
[ORCID 0000-0001-5839-5197](https://orcid.org/0000-0001-5839-5197)  
Version 2.0.0

Paper DOI: <https://doi.org/10.5281/zenodo.24416391>  
Replay supplement DOI: <https://doi.org/10.5281/zenodo.24416392>  
Source: <https://github.com/SuperMatics-Inc/coulomb-pseudopotential-einstein-optimality-ceiling>

Version 1 of the same records: paper <https://doi.org/10.5281/zenodo.24409773>, replay
supplement <https://doi.org/10.5281/zenodo.24409779>.

## What this deposit is

This repository carries the preprint `paper/main.pdf` (26 pages) and the complete replay
supplement for it: the exact certificates behind every certified number in the paper, the
proof notes, the statement-to-source map, and the independent reviews of the reviewed text.
The paper reports seven exact Einstein brackets recording the folded stability form as a
positive semidefinite rank-one term; three two-line spectra sharing a profile; four further
counterexamples at `mu* = 1/2`; four sub-one-half counterexamples and four certified anchors;
a direct-discretization cross-check; numerical phase data; and, new in Version 2, the exact
realizability lemma for a common cutoff with its certified `k = 1` unrealizability audit, an
explicit small-repulsion optimality threshold with its jump-cliff onset tie, and the
second-variation operator with its certified positivity. Each statement in the text carries
exactly one of the labels `PROVED`, `CERTIFIED`, `NUMERICAL`, `OPEN`, defined in the paper's
abstract and matched row by row to its reviewed source in `CLAIMS.md`.

## What changed in Version 2

Version 2 adds Section 8.2 results and corrects the numerical phase table; it withdraws
nothing. No `PROVED` theorem and no `CERTIFIED` counterexample or bracket of Version 1
changed. The additions are Lemma `lem:realizable` (exact necessary and sufficient conditions
for a common cutoff to realize a fixed-`k` crossing), Corollary `cor:unrealizable` and
Table `tab:realizable` (the single-mode crossing at `mu*/lambda = 1/2` is unrealizable under
any common cutoff for `lambda >= 10`), Lemma `lem:gb` (exact two-line difference kernel),
Theorem `thm:smallr` (the threshold `r_0 = 1/64` on `lambda in [3/10,3]` for all `R >= 0`
and the exact jump-cliff onset tie), Theorem `thm:d2` (the second-variation operator and the
local strict maximality criterion) and Corollary `cor:d2cert` (its certified positivity on
the 33 slabs and the 20 fixed-`k` benchmarks). In the numerical phase table the active-mask
column is corrected at `lambda = 10` (`1 -> 2`) and `lambda = 20` (`1 -> 5`), and the
crossing `9 q_E^(1) = q_ph` is reported at `lambda ≈ 9.85` instead of the earlier `5.85`.
Version 2 is deposited as a new version of the Version 1 records, so both versions stay
citable.

## Scope

Bounds are on the model quantity `T_lin`, the linear instability onset of the linearized
equations; never on a measured critical temperature, and no material or superconductor claim
is made. The Coulomb repulsion is pairing-only and does not enter the quasiparticle
renormalization. The folded identity and the optimality regimes are proved; the brackets,
the realizability audit, the threshold and the second-variation positivity are certified in
exact rational arithmetic by independently written verifiers and checked against guarded
mutants; the phase table is finite-precision data. `OPEN` marks what the paper deliberately
does not answer: optimality in the interior of `mu*/lambda <= 1/2` outside the proved and
certified regions is not settled, and the exact threshold curve is numerical.

## Peer review and disclosure

This preprint has not been peer reviewed. The paper states, and this record carries out,
its independence protocol: separate AI agents carried out the independent reviews, targeting
the certificate chain, the two independent verifiers in exact rational and exact integer
arithmetic, the proof notes and the manuscript text in separate passes; their reports are
deposited beside the text they reviewed (`records/common-cutoff-review/`,
`records/mustar-half/REVIEW.md`, `records/einstein-opt2/REVIEW.md`). Every claim the
records make about a number in the paper is a claim about the bytes of the version released
here.

## Layout

| Path | Contents |
|---|---|
| `paper/` | `main.tex`, `refs.bib`, `main.pdf` (the released bytes) |
| `CLAIMS.md` | statement-to-source map with one label per statement, and the version log |
| `BUILD.md` | the paper's build record, including the byte hashes of `paper/main.tex`, `paper/refs.bib` and `paper/main.pdf` |
| `CITATION.cff` | citation metadata for this version |
| `LICENSE` | licence statement for the deposit |
| `reviews/` | the independent reviews of the manuscript text and the repair log (`REVIEW.md`, `REVIEW-S8.md`, `FIX-S8b.md`); their diff bases are carried in the Version 1 deposit, not here |
| `C-LAMBDA/` | the zero-repulsion bracket record and the certified endpoints `records/*/bounds.json` rest on (`brackets.json`, `RESULT.md`, `RIGOR.md`) |
| `records/common-cutoff/` | common-cutoff record: folded-form certificates, independent verifier, cross-check, adversarial probes, `CHECKS.txt` |
| `records/common-cutoff-review/` | the independent review of that record |
| `records/mustar-half/` | `mu* = 1/2` record: hot/cold certificates, `phase_scan.py`, `CHECKS.txt`, and the record's own review and repair logs |
| `records/einstein-opt2/` | Version 2 record: `replay.py`, `independent.py`, `generate_bounds.py`, `bounds.json`, `SHA256SUMS`, `README.md` |
| `records/RESULT.md`, `records/RIGOR.md` | the joint result and rigor notes of the two Version 1 certificate records |
| `MANIFEST.sha256`, `ADMITTED.sha256` | every file of the tree with its SHA-256 |

## Replay

Python 3.12 with pinned dependencies: `numpy==2.5.5`, `scipy==1.18.1`, `mpmath==1.4.1`,
`sympy==1.14.0`. From a checkout (or from the unpacked release archive) at the repository
root:

```
python -m pip install numpy==2.5.5 scipy==1.18.1 mpmath==1.4.1 sympy==1.14.0

(cd records/common-cutoff && python -B replay.py)
(cd records/common-cutoff && python -B independent.py)
(cd records/common-cutoff && python -B independent.py --selfcheck)
(cd records/common-cutoff && python -B independent.py --adversarial)
(cd records/common-cutoff && python -B structure.py --folded)
(cd records/common-cutoff && python -B crosscheck.py)

(cd records/mustar-half && python -B replay.py)
(cd records/mustar-half && python -B independent.py)
(cd records/mustar-half && python -B independent.py --selfcheck)
(cd records/mustar-half && python -B independent.py --adversarial)
(cd records/mustar-half && python -B structure.py)
(cd records/mustar-half && python -B phase_scan.py)

(cd records/einstein-opt2 && python -B replay.py)
(cd records/einstein-opt2 && python -B independent.py)
```

Every command above exits 0 on a correct tree and verifies the stored `bounds.json`
without rewriting it. Each driver also has guarded mutants: `replay.py --mutant NAME`,
`independent.py --mutant NAME`, `structure.py --mutant`, `structure.py --folded --mutant`,
`crosscheck.py --mutant NAME` and `phase_scan.py --mutant` corrupt one ingredient of the
statement, print `mutant refused: ...`, and must exit 1. `records/einstein-opt2/replay.py --mutants` and
`records/einstein-opt2/independent.py --mutants` run every mutant of that driver plus its
unmutated control and exit 0 only when each mutant is refused and the control passes;
`records/*/CHECKS.txt` lists every Version 1 mutant row with the exit code and the message
tail recorded when it was run, and `records/einstein-opt2/README.md` lists the fourteen
Version 2 mutants. None of the verifiers writes to disk or uses network access. An exit
code 2 would mean a mutant's unmutated control broke, which invalidates the mutant; it was
never observed.

File integrity can be checked before replaying:

```
sha256sum -c MANIFEST.sha256
(cd records/einstein-opt2 && sha256sum -c SHA256SUMS)
```

## Continuous integration

`.github/workflows/ci.yml` runs on every push and pull request:

- `tree`: verifies `MANIFEST.sha256` and `ADMITTED.sha256` on the committed tree, checks
  the release identifiers in `README.md`, `CITATION.cff`, `CLAIMS.md` and `BUILD.md`, and
  applies a forbidden-file policy: only the listed files may sit in the repository root and
  in `paper/`, and no backup copy, release-process note, TeX build log, patch residue,
  archive or credential file may be tracked anywhere.
- `replay`: installs the pinned dependencies and runs `.github/replay.sh` on the checkout:
  every verifier, every self-test, every individual guarded mutant, the combined
  `--mutants` modes of the two Version 2 verifiers, and a certificate re-hash, exiting 0
  only when every expected message appeared and every mutant was refused.
- `archive`: unpacks `git archive HEAD` into a temporary directory, verifies
  `MANIFEST.sha256` on the unpacked bytes, and runs the same `.github/replay.sh` there, so
  the archive proves itself without the git checkout.
- `paper`: builds `paper/main.tex` with Tectonic at the pinned `SOURCE_DATE_EPOCH` and
  requires the rebuilt PDF to hash to the released `paper/main.pdf` byte for byte
  (`9d3bd9975260cc255a6f1b30dd56d018ae6e5afbaaa6b4cee5c24f5387a3bb55`), 26 pages, no
  overfull or underfull boxes, no undefined reference, no Version 2 DOI inside the text,
  and every text check of `BUILD.md` re-run on the rebuilt PDF.

## Licence

The paper (`paper/`, `CLAIMS.md`, `BUILD.md`) is released under CC BY 4.0; the replay
supplement (the scripts under `records/` and `C-LAMBDA/`) is released under the Apache
License 2.0. See `LICENSE`.
