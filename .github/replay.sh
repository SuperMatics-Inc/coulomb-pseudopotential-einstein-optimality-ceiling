#!/usr/bin/env bash
# Runs every exact verifier, every self-test and every guarded mutant of the three
# certificate records, then re-checks the stored certificates. Exits 0 only when every
# expected message appears and every mutant is refused. Run from the repository root of a
# checkout or of an unpacked release archive; nothing outside those directories is touched.
set -euo pipefail

PY=${PY:-python}

expect_ok() {
  marker=$1; shift
  "$@" > out.txt 2>&1
  cat out.txt
  grep -qF "$marker" out.txt
  rm -f out.txt
}
expect_refuse() {
  if "$@" > mutant.txt 2>&1; then
    cat mutant.txt
    rm -f mutant.txt
    echo "mutant accepted: $*"
    exit 1
  fi
  rm -f mutant.txt
}
expect_mutant() {
  marker=$1; shift
  if "$@" > mutant.txt 2>&1; then
    cat mutant.txt
    rm -f mutant.txt
    echo "mutant accepted: $*"
    exit 1
  fi
  cat mutant.txt
  grep -qF "$marker" mutant.txt
  rm -f mutant.txt
}

echo "== records/common-cutoff =="
cd records/common-cutoff
expect_ok 'stored bounds.json verified without rewriting' "$PY" -B replay.py
for m in sign spectrum tail coulomb endpoint; do expect_refuse "$PY" -B replay.py --mutant "$m"; done
expect_ok 'independent verification of the common-cutoff certificates: OK' "$PY" -B independent.py
expect_ok 'interval enclosure selfcheck:' "$PY" -B independent.py --selfcheck
expect_ok 'adversarial probes: every box with an exactly negative folded form was refused' "$PY" -B independent.py --adversarial
for m in endpoint coulomb spectrum receipt; do expect_refuse "$PY" -B independent.py --mutant "$m"; done
expect_ok 'structural checks passed on 400 rational two-line spectra (exact arithmetic)' "$PY" -B structure.py
expect_mutant 'mutant controls refused 36 perturbed statements (as required)' "$PY" -B structure.py --mutant
expect_ok 'folded identity (matrix form = display form) verified exactly in 120 rational trials' "$PY" -B structure.py --folded
expect_mutant 'folded mutant: the display missing the tail term differs from the matrix in 120/120 trials' "$PY" -B structure.py --folded --mutant
expect_ok 'full-line cross-check: every Einstein bracket reproduced' "$PY" -B crosscheck.py
for m in mirror zshift; do expect_refuse "$PY" -B crosscheck.py --mutant "$m"; done
cd ../..

echo "== records/mustar-half =="
cd records/mustar-half
expect_ok 'stored bounds.json verified without rewriting' "$PY" -B replay.py
for m in coulomb spectrum endpoint tail sign; do expect_refuse "$PY" -B replay.py --mutant "$m"; done
expect_ok 'independent verification of MUSTAR-HALF certificates: OK' "$PY" -B independent.py
expect_ok 'interval enclosure selfcheck:' "$PY" -B independent.py --selfcheck
expect_ok 'adversarial probes: every box with an exactly negative folded form was refused' "$PY" -B independent.py --adversarial
for m in entrywise v1pen rsign overflow endpoint coulomb spectrum receipt; do expect_refuse "$PY" -B independent.py --mutant "$m"; done
expect_ok 'structural checks passed on 40 random rational trials + F4 refutation witnesses' "$PY" -B structure.py
expect_mutant 'REFUSED: mutant structural checks failed as required' "$PY" -B structure.py --mutant
expect_ok 'phase_scan.py numerical checks: OK' "$PY" -B phase_scan.py
expect_refuse "$PY" -B phase_scan.py --mutant
cd ../..

echo "== records/einstein-opt2 =="
cd records/einstein-opt2
sha256sum -c SHA256SUMS
expect_ok 'replay.py: ALL CERTIFICATES VERIFIED' "$PY" -B replay.py
expect_ok 'MUTANTS REFUSED (exit 1)' "$PY" -B replay.py --mutants
expect_ok 'independent.py: ALL CERTIFICATES VERIFIED' "$PY" -B independent.py
expect_ok 'INDEPENDENT MUTANTS REFUSED (exit 1)' "$PY" -B independent.py --mutants
sha256sum -c SHA256SUMS
cd ../..

echo "replay.sh: every verifier passed, every mutant refused, stored certificates intact"
