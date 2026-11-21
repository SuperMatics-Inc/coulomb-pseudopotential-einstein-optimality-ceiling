# Replay supplement (Version 2 additions): realizability, small-repulsion optimality, jump-cliff tie, and second variation

Davis Rens  
SuperMatics Inc.  
[ORCID 0000-0001-5839-5197](https://orcid.org/0000-0001-5839-5197)

This directory contains the Version 2 exact verification programs and stored rational
certificates for the preprint *The Coulomb pseudopotential and the optimality of the
Einstein spectrum for the linear Eliashberg ceiling* (Version 2, updating the Version 1
release at `10.5281/zenodo.24409773` and its Version 1 supplement at
`10.5281/zenodo.24409779`).

## Contents

| File | Description |
| --- | --- |
| `replay.py` | Primary exact verifier (`fractions.Fraction`, `int64` contractions at $S = 2^{30}$ and $G = 2^{25}$ with an explicit $< 2^{62}$ overflow guard, Machin $\pi$ enclosure, folded quadratic form on the cold side, weighted-Gershgorin + Schur-complement tail with uniform $j+1$ Cauchy-Schwarz bound, interval Cholesky $L D L^T$ rounding check). |
| `independent.py` | Independently written second exact verifier (`SC = 2^{29}`, `GR = 2^{26}`, Hutton Machin-like $\pi/4 = \arctan(1/2) + \arctan(1/3)$ enclosure, unfolded full-line Matsubara quadratic form on $\{-N, \dots, N-1\}$ retaining $a_0 = \lambda$ in exact Python integer correlation + `Fraction` arithmetic on the cold side, per-row Gershgorin tail gaps $g_j$ on $[m, m+\mathrm{ncol})$ and $g_{\mathrm{far}}$ at $m+\mathrm{ncol}$ with exact $S_1$ and far-tail Schur complement on the hot side, and exact integer congruence $M = R^T A R$ via overflow-guarded 16-bit limb `int64` matrix multiplication certified strictly diagonally dominant $2 M_{ii} > \sum_j |M_{ij}|$ in exact Python integers). |
| `bounds.json` | Stored rational certificates for Corollary 8.9 and Table 6 (`realizability_audit`), Theorem 8.11 (`target2_r0_1over64` and `jump_cliff_obstruction`), and Corollary 8.13 (`target3_d2_k1_to_4` plus `d2_boxes` and `d1_boxes` in `target2_r0_1over64`). |
| `generate_bounds.py` | Certificate generator that produces `bounds.json` from scratch. |
| `README.md` | This file. |
| `SHA256SUMS` | SHA-256 digests of the files in this directory. |

## Requirements

Python 3.10 or newer with `numpy`, `scipy`, `sympy`, and `mpmath`. Both `replay.py` and
`independent.py` import `numpy` and `scipy.linalg` (`cholesky` in `replay.py`; `cholesky`
and `solve_triangular` in `independent.py` to propose the approximate inverse factor $R$
before certifying $M = R^T A R$ in exact integer arithmetic). All certified inequalities
are decided in exact Python `Fraction` and `int` arithmetic (with an explicit $< 2^{62}$
overflow guard on `int64` contractions). Neither verifier writes to disk or uses network
access.

## Commands and expected results

Run from this directory:

```
python -B replay.py
python -B replay.py --mutants
python -B independent.py
python -B independent.py --mutants
```

Or with `uv`:

```
uv run --no-project --with sympy --with mpmath --with numpy --with scipy python -B replay.py
uv run --no-project --with sympy --with mpmath --with numpy --with scipy python -B replay.py --mutants
uv run --no-project --with sympy --with mpmath --with numpy --with scipy python -B independent.py
uv run --no-project --with sympy --with mpmath --with numpy --with scipy python -B independent.py --mutants
```

All four commands must exit `0`. Each individual mutant (`replay.py --mutant <name>` for
`{realizability_boundary, coulomb, moment, tail_drop, box_gap, overflow, cliff_sign, d2_sign_reversal}`
and `independent.py --mutant <name>` for
`{unfolded_a0, pi_bound, coulomb_slab, cliff_resonance, d2_weight_sign, receipt_shave}`)
corrupts one certificate ingredient, verifies that the unmutated control still passes, prints
`mutant refused: ...`, and exits `1` (`8 + 6 = 14` guarded mutants in total).

## What is certified

1. **Realizability audit (Lemma 8.8, Corollary 8.9, and Table 6, `realizability_audit`):**
   - For every $\lambda \in \{10, 20, 25, 35, 50, 65, 152\}$ at $\mu^* = \lambda/2$ (`k1_rows`),
     certifies $q_E^{(1)}(\lambda, \lambda/2) < q_1^{\mathrm{hot}}(\lambda)$ on
     $[q_1^{\mathrm{hot}}(\lambda), 4\lambda]$ (`hot1_boxes`: `[14, 13, 19, 21, 25, 30, 49]`,
     `171` boxes total), $q_{\mathrm{ph}}(\lambda) > q_0^{\mathrm{cold}}(\lambda)$ via an
     exact rational cold vector `v0_cold`, and the strict inequality
     $9\,q_1^{\mathrm{hot}}(\lambda) < q_0^{\mathrm{cold}}(\lambda)$, proving that no common
     cutoff $R > 0$ can realize the fixed-$k=1$ crossing.
   - At $\lambda = 152, \mu^* = 76$ (`lam152_fixed1_failure`), certifies at
     $q_{\mathrm{test}} = 43355/10000 = 8671/2000$ that
     $\mathcal{F}_{\delta_1}^{(1)}(q) \succ 0$ on $[q_{\mathrm{test}}, 4\lambda = 608]$
     (`hot_E_boxes`: `66` boxes) while the two-line spectrum $(u_1, u_2) = (10^{-5}, 35/2)$
     with $\theta = 99999/1749999 = 33333/583333$ has a negative quadratic form value on
     `v_mix_cold`, whereas $9\,q_{\mathrm{test}} < q_0^{\mathrm{cold}}(152) < q_{\mathrm{ph}}(152)$.
2. **Small-repulsion threshold $r_0 = 1/64$ on $\lambda \in [3/10, 3]$ and jump-cliff onset tie
   (Lemma 8.10 and Theorem 8.11, `target2_r0_1over64` and `jump_cliff_obstruction`):**
   - Across `33` contiguous coupling slabs $[\lambda_a^{(s)}, \lambda_b^{(s)}]$ covering
     $\lambda \in [3/10, 3]$, certifies via an exact nonnegative cold vector $v_{\mathrm{cold}}^{(s)}$
     at $\lambda_a^{(s)}$ that $q_{\mathrm{lin}}(\lambda, \mu^*, R; \delta_1) > q_*^{(s)}$
     for all $\lambda \in [\lambda_a^{(s)}, \lambda_b^{(s)}]$, $\mu^* \in [0, r_0\lambda]$,
     $R > 0$, and certifies $G_B^{(0)}(\lambda_b^{(s)}; q, t_1, t_2) \succ 0$ at the upper
     slab endpoint $\lambda_b^{(s)}$ (yielding $G_B^{(0)}(\lambda; q, t_1, t_2) \succ 0$ for
     all $\lambda \in (0, \lambda_b^{(s)}]$ by affine linearity in $\lambda$ and $D(q) \succ 0$)
     across $(q, t_1, t_2) \in [q_*^{(s)}, 4\lambda_b^{(s)}] \times [0, 1]^2$ (`gb_boxes`:
     `2,361` rational 3D boxes total), with Theorem 8.7 covering $q \ge 4\lambda_b^{(s)}$.
   - At $\lambda = 2, \mu^* = 1/32$ ($\mu^*/\lambda = r_0 = 1/64$), certifies at
     $q_{\mathrm{cliff}} = 962/625$ and $R^2 = 404521/1250$ ($4R^2 = 29^2\,q_{\mathrm{cliff}}
     = 809042/625$, the mask jump between $k = 14$ and $k = 15$) that both $\delta_1$ and the
     two-line perturbation $p_\varepsilon$ ($\varepsilon = 1/1024$, $u_1 = 1023/1024$,
     $u_2 = 1025/1024$, $\theta = 1/2$) are strictly positive definite on
     $[q_{\mathrm{cliff}}, 4\lambda = 8]$ across all `9` active mask windows
     $k = 14, 13, \dots, 6$ (`windows_E`: `18` boxes `[10, 1, 1, 1, 1, 1, 1, 1, 1]` for
     $\delta_1$; `windows_p`: `18` boxes `[10, 1, 1, 1, 1, 1, 1, 1, 1]` for $p_\varepsilon$)
     and both are strictly unstable at $q_{\mathrm{cliff}}$ on mask $k = 15$ (`v_E_cold_k15`
     and `v_p_cold_k15`), proving the exact onset tie
     $q_{\mathrm{lin}}(p_\varepsilon) = q_{\mathrm{lin}}(\delta_1) = 962/625$.
3. **Second-variation operator $D_2(\lambda, q)$ (Theorem 8.12 and Corollary 8.13,
   `target2_r0_1over64` and `target3_d2_k1_to_4`):**
   - Certifies $\mathcal{F}_{\delta_1}^{(k)}(q) + D_2(\lambda, q) \succ 0$ (`d2_boxes`: `266`
     boxes) and $\mathcal{F}_{\delta_1}^{(k)}(q) + D_1(\lambda, q) \succ 0$ (`d1_boxes`: `117`
     boxes, `383` slab boxes total) at the upper slab endpoint $\lambda_b^{(s)}$ across all
     `33` slabs covering $\lambda \in [3/10, 3]$ and $q \in [q_*^{(s)}, 4\lambda_b^{(s)}]$
     (extending to all $\lambda \in (0, \lambda_b^{(s)}]$ by affine linearity and to
     $q \ge 4\lambda_b^{(s)}$ by Theorem 8.7).
   - Across all `20` benchmarked pairs $(k, \lambda) \in \{1, 2, 3, 4\} \times \{1/2, 1, 2, 5, 10\}$
     at $\mu^*/\lambda = 1/2$ (`target3_d2_k1_to_4`), brackets
     $q_E^{(k)}(\lambda, \lambda/2) \in (q_{\mathrm{lo}}, q_{\mathrm{hi}})$ via an exact cold
     vector `v_cold` at $q_{\mathrm{lo}}$ and `hot_q_boxes` on $[q_{\mathrm{hi}}, 4\lambda]$
     (`352` boxes total), and certifies
     $\mathcal{F}_{\delta_1}^{(k)}(q) + D_2(\lambda, q) \succ 0$ (`d2_boxes`: `20` boxes, 1
     per pair) and $\mathcal{F}_{\delta_1}^{(k)}(q) + D_1(\lambda, q) \succ 0$ (`d1_boxes`:
     `20` boxes, 1 per pair) on $[q_{\mathrm{lo}}, q_{\mathrm{hi}}]$.

## Disclosure

AI agents generated the proofs, code, and manuscript drafts under D. Rens' direction.
Separate AI agents performed the independent reviews. This preprint has not been peer reviewed.
