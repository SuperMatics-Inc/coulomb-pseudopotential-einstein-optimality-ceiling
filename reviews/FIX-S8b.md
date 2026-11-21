# FIX-S8b - repairs for `REVIEW-S8.md`

Status: **D1 to D4 applied exactly as stated; clean rebuild done; text checks re-run.**
`REVIEW-S8.md` reports PASS-WITH-FIXES with zero P0 and zero P1. No statement, label,
number or bracket was changed: every edit below is textual, and the two count/scope
corrections make the paper match the recorded evidence.

Backups of the pre-fix bytes: `main.v2.tex` (source) and `CLAIMS.v2.md` (claim map).
`main.v1.tex` and `CLAIMS.v1.md` remain the diff base for `REVIEW.md`.

## Per-item changes

| Item | Fix | Location after fix | Evidence the wording now matches |
|---|---|---|---|
| **D1** | first verifier hot head size `m=200` changed to `n=240`; the second verifier keeps `m=200` | `main.tex:725` | `mustar-half/fixtures.json` sets `size_hot: 240` for all eight instances and `replay.py` builds `Folded(int(data['size_hot']))`; only the second verifier's enclosure uses 200, as `REVIEW3.md:45` records |
| **D2** | the four quoted second-verifier margins are now stated to be in that verifier's `2^22`-scaled integer units, each backed by a strictly positive integer Gershgorin gap; the entrywise-bound witness now states that both quadratic forms, `+565.9e12` for the rejected lower bound and `-85.47e12` for the folded form, are taken on the same `2^22` integer scale | `main.tex:741`, `main.tex:761` | `REVIEW3.md:65` (finding N3) and the second verifier's own printing at `independent.py:333,400`, `gap.min()/factor`; `CHECKS.txt:26` prints `x^T SC*F(q_bad)x = -85.47e12`, and the rejected matrix is `lower.copy()` at `independent.py:859`, so both forms share the scale |
| **D3.1** | `All twenty recorded commands` changed to `All twenty-one recorded commands` in the Section 8 proof | `main.tex:770` | `mustar-half/CHECKS.txt` records 21 `$RUN` rows (6 `replay.py`, 11 `independent.py`, 2 `structure.py`, 2 `phase_scan.py`) |
| **D3.2** | `each program also refuses when all of its mutants are run together` narrowed to the structural checker, which refuses when all three of its mutants are run together | `main.tex:753` | only `structure.py` has a combined-mutant mode (`--mutant all`); `replay.py` and `independent.py` take one named mutant per invocation, `independent.py:36` |
| **D3.3** | `A sixth self-test` changed to `A self-test` | `main.tex:766` | the preceding text numbers no earlier self-tests, so the ordinal had no referent |
| **D4.1** | abstract now says the four below-one-half counterexamples are `certified by a second pair of independent exact verifiers in the same two roles`, instead of `by the same two verifiers` | `main.tex:52` | consistent with `main.tex:1180-1183` (Section 9 item 6) and with the data-availability paragraph, which describes a separate pair of verifiers for Section 8 |
| **D4.2** | Section 9 item 4 now reads `its certified answers above and below one half` | `main.tex:1175` | Section 8 carries CERTIFIED statements below one half, so the priority item no longer reads as if only the above-one-half answer existed |
| **D4.3** | Section 8.3's introduction now records that `thm:large` applies `thm:nomask` and inherits the zero-repulsion dependency, and Section 9 item 6 records that the dependency is inherited by `thm:large` | `main.tex:817`, `main.tex:1184` | `thm:large`'s proof ends by applying `thm:nomask` (`main.tex:937`), so its hypothesis carries the cited zero-Coulomb theorem |

Small rewraps were made inside the four touched paragraphs of the Section 8 proof and in
the abstract sentence of D4.1 so that no line is left short or long relative to the rest
of the source. No content moved.

Unchanged by design: `main.tex:527` still reads `All twenty recorded checks`, because that
sentence describes Section 5, whose source table records exactly 20 rows; `REVIEW-S8.md`
flagged only the Section 8 count.

## Rebuild and checks

Clean Tectonic (`main.aux`, `.bbl`, `.blg`, `.log`, `.out`, `.toc` deleted first),
`tectonic -X compile --keep-logs main.tex`:

| Check | Result |
|---|---|
| Engine exit code | `0` |
| Overfull boxes | `0` |
| Underfull boxes | `0` |
| Undefined references or citations | `0` |
| LaTeX warnings in the log | `0` |
| Page count | `20` |
| Em dash `U+2014` | `0` |
| En dash `U+2013` | `10`, all inside compound names (Migdal-Eliashberg four times, Richter-Rogosinski, Markov-Krein, Birman-Schwinger, Krein-Rutman, Kiessling-Altshuler-Yuzbashyan twice) |
| `This preprint has not been peer reviewed.` | present, once |
| AI disclosure | present, once |
| Byline and ORCID | present |
| Process language and path or record names | `0` occurrences |

Bytes at this build:

    main.tex   sha256 3e18408a59fc3f8c2c42ed257d3638fb874ec67f6eea03c7aedba287ea8f8d9e
    refs.bib   sha256 9d56e7292d499f044b6eaf12df61ea7aec5cf216b2f2995b873a1667f4264cd2
    main.pdf   sha256 c8f9201000e3f4ec4d69b2bb3b36095bdd4bdb477112a4b1de2ebba619d8502e
