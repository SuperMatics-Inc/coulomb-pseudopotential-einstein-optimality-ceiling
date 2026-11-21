# BUILD - `main.pdf`

This is the paper's build record, with repository-relative names for the TeX engine and the
supplement records under `records/` (the Version 2 record is `records/einstein-opt2/`).
`main.tex` abbreviates `paper/main.tex` throughout, and the version log is `CLAIMS.md`.

## Toolchain

- TeX engine: `tectonic` (Tectonic 0.17.0, XeTeX class), no other
  tool required; the bibliography is run by Tectonic itself.
- Reproducible build timestamp: `SOURCE_DATE_EPOCH=1795132800`.
- Files: `main.tex` (source), `refs.bib` (bibliography), `main.pdf` (26 pages), `CLAIMS.md`
  (statement to source map). No figures, no external assets, no data files are read at
  build time.
- The released Version 1 manuscript has sha256
  `3e18408a59fc3f8c2c42ed257d3638fb874ec67f6eea03c7aedba287ea8f8d9e`; it is the archived
  preprint artifact of Version 1, not a file of this tree and not an input to the build.

## Bytes at this build (Version 2)

| File | sha256 |
|---|---|
| `main.tex` | `0eb17fe0de77bb723bcec2233baf3edd752e77fb0c1d6a238d6cd93d56588894` |
| `refs.bib` | `9d56e7292d499f044b6eaf12df61ea7aec5cf216b2f2995b873a1667f4264cd2` |
| `main.pdf` | `9d3bd9975260cc255a6f1b30dd56d018ae6e5afbaaa6b4cee5c24f5387a3bb55` |

The bytes above differ from the delta-reviewed pair (`main.tex`
`a3e0c7e30f66cb72f4fc28a55f3ac843a17496435ca19256c221a545885720f8`, `main.pdf`
`0768b0e6191e25f6b4ad0c8f7851f9881b7184f2efd218052fb1e3d4fd23afb3`) by exactly one added
source line, the `\bottomrule` closing Table 6 (`tab:realizable`, inserted between source
lines 1181 and 1182), which the delta re-review P2-R1 found missing after the reduction of
`49863/250`. The rebuild used the same deterministic command and produced 26 pages with the
same text checks.

Recompute with `sha256sum paper/main.tex paper/refs.bib paper/main.pdf` before quoting
them; a change to `paper/main.tex` or `paper/refs.bib` invalidates the `paper/main.pdf`
hash until the build is rerun with `SOURCE_DATE_EPOCH=1795132800`.

## Build

    SOURCE_DATE_EPOCH=1795132800 tectonic -X compile main.tex --keep-logs

A clean from-scratch build (auxiliary files, `.bbl` and `.log` deleted first) was run on
the final bytes. Result on the final bytes:

| Check | Result |
|---|---|
| Engine exit code | `0` |
| Overfull boxes | `0` |
| Underfull boxes | `0` |
| Undefined references or citations | `0` |
| LaTeX warnings of any kind | none beyond the Fontconfig notice of the local Tectonic install (`Cannot load default config file`), which does not affect output |
| Page count | `26` |
| Tables | seven, numbered 1 to 7 in order: counterexamples, Einstein brackets, direct cross-check, four sub-one-half counterexamples, sub-one-half anchors, realizability audit (`tab:realizable`), phase data (`tab:phase`) |
| LaTeX warnings in the log | `0` (`grep -cE "Overfull|Underfull|Undefined|LaTeX Warning" main.log` returns `0`) |

## Text checks on the produced PDF

Text is extracted from `main.pdf` and matched case sensitively:

| Check | Result |
|---|---|
| Em dash `U+2014` occurrences | `0` |
| En dash `U+2013` occurrences | `10`, all inside compound names (`Migdal-Eliashberg` four times, `Richter-Rogosinski`, `Markov-Krein`, `Birman-Schwinger`, `Krein-Rutman`, `Kiessling-Altshuler-Yuzbashyan` twice, title and text), none used as a dash between words |
| Literal `This preprint has not been peer reviewed.` | present, once (disclosure block) |
| AI disclosure | present: "AI agents generated the proofs, code and drafts under D. Rens' direction, and separate AI agents carried out the independent reviews." |
| Byline | `Davis Rens`, `SuperMatics Inc.`, ORCID `0000-0001-5839-5197` |
| `PROVISIONAL` in the PDF | `0` (the provisional flag lives in `CLAIMS.md` only, and no statement in the current section 8 remains provisional) |
| Process language in the PDF | `0`: no `provisional`, `under repair`, `pending`, `being finished`, `currently sound`, `upgrade or replace`, `expected to be replaced` |
| Internal lane, agent, machine and path names | none: no internal directory, drive, script or JSON file name in the PDF text. The word "agent" occurs only inside the AI disclosure sentence, as required by the template |
| Labels present in the text | printed as small capitals `(proved)`, `(certified)`, `(numerical)`, `(open)`; the abstract defines all four and each is used with its stated meaning |

## Structure of the source

1. Abstract (no label tag), Section 1 `The question and its position` (including `Changes in Version 2`).
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
8. Section 8 `Below one half`: 8.1 the four certified counterexamples (Table 4) and the
   four certified anchors (Table 5), 8.2 the analytic regimes below one half (exact
   finite-support decomposition, two-line reduction at fixed mask, empty mask at the
   crossing, large coupling at fixed cutoff ratio, the single-mode cone and its sharp
   failure, parameter-free positivity above `q = 4 lambda`, the fixed-`k` realizability
   lemma `lem:realizable` (PROVED) and certified `k=1` unrealizability audit `cor:unrealizable`
   in Table 6 (CERTIFIED), the two-line difference kernel `lem:gb` (PROVED), the certified
   `r_0 = 1/64` small-repulsion threshold on `lambda in [3/10,3]` and the jump-cliff onset
   tie `thm:smallr` (CERTIFIED), the second-variation operator `D_2` and local strict
   maximality criterion `thm:d2` (PROVED), and its certified finite-slab and benchmark
   positivity `cor:d2cert` (CERTIFIED)), and 8.3 the numerical phase data (Table 7, with
   the active-mask column `k` corrected at `lambda=10` and `lambda=20`).
9. Section 9 `What is not claimed` and Section 10 `Open problems`.
10. Acknowledgments and disclosures, Data availability, references.

Labels are set as small capitals directly after the statement they qualify, one label per
statement; no statement carries two labels. Every label assignment and its source is in
`CLAIMS.md`.

## Regenerating after a source change

1. Edit `main.tex` (and `refs.bib` only by copying DOI and title pairs from a released
   bibliography under the same project; nothing is invented).
2. Update `CLAIMS.md` with the new statement, its `file:line` source and its label.
3. Rebuild with `SOURCE_DATE_EPOCH=1795132800 tectonic -X compile main.tex --keep-logs`
   and re-run the text checks.
4. If a labelled section changes (a repair landing, or a re-review upgrading it), update
   that section and `CLAIMS.md` together and record the change in the repair log; a label
   may only be raised on a re-review of the current bytes, never on the strength of a fix
   report alone.

## Notes

- The Fontconfig line printed by the engine is a notice about the local Tectonic
  installation, not a build failure; the exit code is `0` and the PDF is written.
- Running the build twice is unnecessary; Tectonic resolves references and the
  bibliography in one invocation.
- Table 7 (`tab:phase`) was verified cell for cell against the source table of the phase
  scan, with the two active-mask attribution corrections at `lambda=10` (`1 -> 2`) and
  `lambda=20` (`1 -> 5`) documented in Section 1 (`Changes in Version 2`) and Section 8.3.
- All findings of the Version 2 adversarial pre-release review (P1-1 through P1-6, P2-1
  through P2-3, and P3-1 through P3-3) are logged in Section 15 of `CLAIMS.md`. P1-1
  through P1-5, P2-1 through P2-3 and P3-1 through P3-3 are resolved in the current paper
  bytes. P1-6 (a self-contained supplement) is resolved by this release tree, which
  carries `C-LAMBDA/`, `records/common-cutoff/` and `records/mustar-half/` verbatim from
  Version 1 next to the Version 2 record `records/einstein-opt2/`; it is not resolved by
  the paper source alone.
- The `\bottomrule` restoration (delta re-review P2-R1) and the `lambda` crossing and
  inverse-ratio corrections in Section 15 of `CLAIMS.md` (P3-R1) are the only changes to
  the reviewed bytes.
