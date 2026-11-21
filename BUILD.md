# BUILD - `paper/main.pdf`

This is the paper's own build record, with the private working-tree location and the local
engine path replaced by repository-relative names. No check, number, hash or claim changed.
The paper is `paper/main.pdf`; the record files it refers to are under `records/`, and the
review and repair logs under `reviews/`.

## Toolchain

- TeX engine: `tectonic` (Tectonic 0.17.0, XeTeX class), no other
  tool required; the bibliography is run by Tectonic itself.
- Files: `paper/main.tex` (source), `paper/refs.bib` (bibliography), `paper/main.pdf` (20 pages), `CLAIMS.md`
  (statement to source map). No figures, no external assets, no data files are read at
  build time.
- `paper/main.v1.tex` and `CLAIMS.v1.md` are the pre-review-fix copies of the source and the
  claim map, kept only as the diff base for `reviews/REVIEW.md`; `paper/main.v2.tex` and `CLAIMS.v2.md`
  are the copies taken before the `reviews/REVIEW-S8.md` repairs and serve as the diff base for
  `reviews/FIX-S8b.md`. None of them is an input to the build.

## Bytes at this build

| File | sha256 |
|---|---|
| `paper/main.tex` | `3e18408a59fc3f8c2c42ed257d3638fb874ec67f6eea03c7aedba287ea8f8d9e` |
| `paper/refs.bib` | `9d56e7292d499f044b6eaf12df61ea7aec5cf216b2f2995b873a1667f4264cd2` |
| `paper/main.pdf` | `c8f9201000e3f4ec4d69b2bb3b36095bdd4bdb477112a4b1de2ebba619d8502e` |

Recompute with `sha256sum paper/main.tex paper/refs.bib paper/main.pdf` before quoting them; a change to
`paper/main.tex` or `paper/refs.bib` invalidates the `paper/main.pdf` hash until the build is rerun.

## Build

    cd paper
    tectonic -X compile paper/main.tex --keep-logs

A clean from-scratch build (auxiliary files, `.bbl` and `.log` deleted first) was run on
the final bytes. Result on the final bytes:

| Check | Result |
|---|---|
| Engine exit code | `0` |
| Overfull boxes | `0` |
| Underfull boxes | `0` |
| Undefined references or citations | `0` |
| LaTeX warnings of any kind | none beyond the Fontconfig notice of the local Tectonic install (`Cannot load default config file`), which does not affect output |
| Page count | `20` |
| Tables | six, numbered 1 to 6 in order: counterexamples, Einstein brackets, direct cross-check, four sub-one-half counterexamples, sub-one-half anchors, phase data |
| LaTeX warnings in the log | `0` (`grep -cE "Overfull|Underfull|Undefined|LaTeX Warning" paper/main.log` returns `0`) |

## Text checks on the produced PDF

Text is extracted from `paper/main.pdf` and matched case sensitively:

| Check | Result |
|---|---|
| Em dash `U+2014` occurrences | `0` |
| En dash `U+2013` occurrences | `10`, all inside compound names (`Migdal-Eliashberg` four times, `Richter-Rogosinski`, `Markov-Krein`, `Birman-Schwinger`, `Krein-Rutman`, `Kiessling-Altshuler-Yuzbashyan` twice, title and text), none used as a dash between words |
| Literal `This preprint has not been peer reviewed.` | present, once (disclosure block) |
| AI disclosure | present: "AI agents generated the proofs, code and drafts under D. Rens' direction, and separate AI agents carried out the independent reviews." |
| Byline | `Davis Rens`, `SuperMatics Inc.`, ORCID `0000-0001-5839-5197` |
| `PROVISIONAL` in the PDF | `0` (the provisional flag lives in `CLAIMS.md` only, and no statement in the current section 8 remains provisional) |
| Process language in the PDF | `0`: no `provisional`, `under repair`, `pending`, `being finished`, `currently sound`, `upgrade or replace`, `expected to be replaced` |
| Lane, agent, machine and path names | none: no `C-LAMBDA`, `MUSTAR`, `CUTOFF-PAPER`, `D:/`, `C:/`, `scratch`, `.py`, `bounds.json`, `phase_scan`, lane or machine name. The word "agent" occurs only inside the AI disclosure sentence, as required by the template |
| Labels present in the text | printed as small capitals `(proved)`, `(certified)`, `(numerical)`, `(open)`; the abstract defines all four and each is used with its stated meaning |

## Structure of the source

1. Abstract (no label tag), Section 1 `The question and its position`.
2. Section 2 `Model and the common cutoff`.
3. Section 3 `Structural reduction at fixed coupling and moment` (Theorem, PROVED).
4. Section 4 `Einstein dominance and its failure`: Jensen lemma and folded Laplacian
   identity (PROVED), rank-one proposition and Coulomb-robust corollary (PROVED), the
   mechanism remark, and two subsections on the regimes where the repulsion cannot disturb
   the optimum.
5. Section 5 `Certified counterexamples above one half`: theorem, Table 1, the
   certification proof and the method, verifier independence, mutants.
6. Section 6 `Certified brackets and the zero-repulsion calibration`: Table 2, the
   `C(1)` calibration and the monotone chain.
7. Section 7 `Direct-discretization cross-check`: Table 3, NUMERICAL.
8. Section 8 `Below one half`: 8.1 the four certified counterexamples (Table 4), 8.2 the
   four certified anchors (Table 5), 8.3 the analytic regimes below one half (exact
   finite-support decomposition, two-line reduction at fixed mask, empty mask at the
   crossing, large coupling at fixed cutoff ratio, the single-mode cone and its sharp
   failure, and parameter-free positivity above `q = 4 lambda`), and 8.4 the numerical
   phase data (Table 6). The certified labels of 8.1 and 8.2 and of the analytic
   statements of 8.3 come from the re-review of the sub-one-half sources; 8.4 stays
   NUMERICAL.
9. Section 9 `What is not claimed`, Section 10 `Open problems`.
10. Acknowledgments and disclosures, Data availability, references.

Labels are set as small capitals directly after the statement they qualify, one label per
statement; no statement carries two labels. Every label assignment and its source is in
`CLAIMS.md`.

## Regenerating after a source change

1. Edit `paper/main.tex` (and `paper/refs.bib` only by copying DOI and title pairs from a released
   bibliography under the same project; nothing is invented).
2. Update `CLAIMS.md` with the new statement, its `file:line` source and its label.
3. Rebuild with the command above and re-run the text checks.
4. If a labelled section changes (a repair landing, or a re-review upgrading it), update
   that section and `CLAIMS.md` together and record the change in the repair log; a label
   may only be raised on a re-review of the current bytes, never on the strength of a fix
   report alone.

## Notes

- The Fontconfig line printed by the engine is a notice about the local Tectonic
  installation, not a build failure; the exit code is `0` and the PDF is written.
- Running the build twice is unnecessary; Tectonic resolves references and the
  bibliography in one invocation.
- Table 6 was additionally verified cell for cell against the source table of the phase
  scan (a comparison script that normalizes typesetting only); all fourteen rows agree.
- The last round of repairs is the four textual items of `reviews/REVIEW-S8.md`; `reviews/FIX-S8b.md`
  maps each to its line and its evidence. No statement, label, number or bracket moved in
  that round.
