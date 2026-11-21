# The Coulomb pseudopotential and the optimality of the Einstein spectrum for the linear Eliashberg ceiling

Davis Rens  
SuperMatics Inc.  
[ORCID 0000-0001-5839-5197](https://orcid.org/0000-0001-5839-5197)  
Version 1.0.0

Paper DOI: <https://doi.org/10.5281/zenodo.24409773>  
Replay supplement DOI: <https://doi.org/10.5281/zenodo.24409779>  
Source: <https://github.com/SuperMatics-Inc/coulomb-pseudopotential-einstein-optimality-ceiling>

## What this deposit is

This repository carries the preprint `paper/main.pdf` (20 pages) and the complete replay
supplement for it: the exact certificates behind every certified number in the paper, the
proof notes, the statement-to-source map, and the independent reviews of the reviewed text.
The paper reports seven exact Einstein brackets recording the folded stability form as a
positive semidefinite rank-one term; three two-line spectra sharing a profile; four further
counterexamples at `mu* = 1/2`; four sub-one-half counterexamples and four certified anchors;
a direct-discretization cross-check; and numerical phase data. Each statement in the text
carries exactly one of the labels `PROVED`, `CERTIFIED`, `NUMERICAL`, `OPEN`, defined in the
paper's abstract and matched row by row to its reviewed source in `CLAIMS.md`.

## Scope

Bounds are on the model quantity `T_lin`, the linear instability onset of the linearized
equations; never on a measured critical temperature, and no material or superconductor claim
is made. The Coulomb repulsion is pairing-only and does not enter the quasiparticle
renormalization. The folded identity and the three optimality regimes are proved; the seven
Einstein brackets are certified in exact rational arithmetic by two independently written
verifiers and checked against guarded mutants; the phase table is finite-precision data.
`OPEN` marks what the paper deliberately does not answer.

## Layout

| Path | Contents |
|---|---|
| `paper/` | `main.tex`, `refs.bib`, `main.pdf` (the released bytes); `main.v1.tex`, `main.v2.tex` are the diff bases reviewed by `reviews/REVIEW.md` and `reviews/REVIEW-S8.md` |
| `CLAIMS.md`, `CLAIMS.v1.md`, `CLAIMS.v2.md` | statement-to-source map with one label per statement, and its two snapshots taken before the review rounds |
| `reviews/` | the independent reviews of the manuscript text and the repair log (`REVIEW.md`, `REVIEW-S8.md`, `FIX-S8b.md`) |
| `records/c-lambda/` | the zero-repulsion bracket record and the certified endpoints `records/*/bounds.json` rest on (`brackets.json`, `RESULT.md`, `RIGOR.md`) |
| `records/common-cutoff/` | common-cutoff record: folded-form certificates, independent verifier, cross-check, adversarial probes, `CHECKS.txt` |
| `records/common-cutoff-review/` | the independent review of that record |
| `records/mustar-half/` | `mu* = 1/2` record: hot/cold certificates, `phase_scan.py`, `CHECKS.txt`, and the record's own review and repair logs |
| `records/RESULT.md`, `records/RIGOR.md` | the joint result and rigor notes of the two certificate records |
| `BUILD.md` | the paper's build record, including the byte hashes of `paper/main.tex`, `paper/refs.bib` and `paper/main.pdf` |

## Replay

Python 3.12 with pinned dependencies: `numpy==2.5.5`, `scipy==1.18.1`, `mpmath==1.4.1`.
From the repository root:

```
python -m pip install numpy==2.5.5 scipy==1.18.1 mpmath==1.4.1

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
```

Every command above exits 0 on a correct tree and verifies the stored `bounds.json`
without rewriting it. Each driver also has guarded mutants: `replay.py --mutant NAME`,
`independent.py --mutant NAME`, `structure.py --mutant`, `structure.py --folded --mutant`,
`crosscheck.py --mutant NAME` and `phase_scan.py --mutant` corrupt one ingredient of the
statement, print `mutant refused: ...`, and must exit 1; `records/*/CHECKS.txt` lists every
mutant row with the exit code and the message tail recorded when it was run. An exit code 2
would mean a mutant's unmutated control broke, which invalidates the mutant; it was never
observed. The `CHECKS.txt` receipts were written in the private working tree that produced
this release and keep its paths; every command in them is runnable as written relative to
the corresponding directory under `records/`.

`crosscheck.py` and `phase_scan.py` are the two finite-precision computations; they are
labelled `NUMERICAL` and are not part of any proof.

## CI

`.github/workflows/ci.yml` verifies `MANIFEST.sha256` and `ADMITTED.sha256`, installs the
pinned replay dependencies, runs the replays above with their pass markers, applies the
public prose safeguards to the manuscript and this README, and builds the paper with
Tectonic, failing on any overfull box, underfull box, undefined reference or missing
disclosure sentence.

## Disclosure and review

AI agents generated the proofs, code, and manuscript drafts under D. Rens' direction.
Separate AI agents performed the independent reviews. This preprint has not been peer
reviewed.

## Rights

The manuscript text and bibliography in `paper/` are distributed under CC-BY-4.0 through the
paper record. The replay code, records and other software materials in this repository are
distributed under Apache-2.0. The paper's license does not change the software license.
