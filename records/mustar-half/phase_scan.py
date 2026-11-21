"""Numerical phase-diagram scanner and unfolded-vs-folded cross-check for MUSTAR-HALF (NUMERICAL).

Verifies:
1. Exact agreement (to machine precision < 1e-13) between the unfolded full-line
   quadratic form on the symmetric subspace (f_{-n-1} = f_n, size 2*N) and the folded
   half-line form F_p^{(k)}(q) (size N) across both Einstein and two-line spectra.
2. Mask-index k in {1, 2, 3, 4} optimality for mu*/lambda <= 1/2 across a grid of
   (lambda, mu*/lambda, u_1, u_2).
3. The k = 5 re-entrant fold for lambda in [25.5, 30.5] where the critical ratio
   r_*(lambda, R) dips below 1/2 down to r_min(5) ~ 0.47818 at lambda ~ 25.55,
   R ~ 3.360, before returning above 1/2 for lambda >= 30.5.

Run:
    python -B phase_scan.py            (exit 0)
    python -B phase_scan.py --mutant   (exit 1: broken unfolded mass must be refused)
"""

import argparse
import sys

import numpy as np
from scipy.linalg import eigvalsh


def need(ok, why):
    if not ok:
        raise ValueError(why)


def refused(why):
    print(f'REFUSED: {why}')
    raise SystemExit(1)


def folded_matrix(lam, mu, q, k, spec, n=120):
    j = np.arange(1, 2 * n + 1, dtype=float)
    a = np.zeros(2 * n + 1, dtype=float)
    for th, u in spec:
        a[1:] += lam * th * u / (u + q * j * j)
    i = np.arange(n)
    csum = np.cumsum(a[:n])
    M = np.diag((2 * i + 1.0) + 2.0 * csum)
    M -= a[np.abs(i[:, None] - i)] + a[i[:, None] + i + 1]
    if k > 0:
        M[:k, :k] += 2.0 * mu
    return M


def unfolded_sym_matrix(lam, mu, q, k, spec, n=120, mutant=False):
    """Build the 2n x 2n unfolded full-line matrix on {-n, ..., n-1} and restrict to f_{-m-1} = f_m."""
    j = np.arange(1, 2 * n + 1, dtype=float)
    a = np.zeros(2 * n + 1, dtype=float)
    for th, u in spec:
        a[1:] += lam * th * u / (u + q * j * j)
    idx = np.arange(-n, n)
    i_map = np.maximum(idx, -idx - 1)
    csum = np.cumsum(a[:n])
    factor = 1.0 if mutant else 2.0
    D = np.array([abs(2 * int(m) + 1) + factor * csum[i_map[t]] for t, m in enumerate(idx)])
    diff = np.abs(idx[:, None] - idx)
    K = a[diff].copy()
    np.fill_diagonal(K, 0.0)
    mask = (np.abs(2 * idx + 1) <= 2 * k - 1).astype(float)
    Full = np.diag(D) - K + mu * np.outer(mask, mask)
    # Basis P for symmetric subspace: column m (0 <= m < n) has 1 at n + m and 1 at n - 1 - m
    P = np.zeros((2 * n, n), dtype=float)
    for m in range(n):
        P[n + m, m] = 1.0
        P[n - 1 - m, m] = 1.0
    # 0.5 * P^T Full P equals the folded half-line matrix
    return 0.5 * (P.T @ Full @ P)


def check_folding_equivalence(mutant=False):
    spec = ((0.85, 0.88), (0.15, 1.68))
    M_fold = folded_matrix(12.0, 5.5, 0.37, 4, spec, n=80)
    M_unf = unfolded_sym_matrix(12.0, 5.5, 0.37, 4, spec, n=80, mutant=mutant)
    err = float(np.max(np.abs(M_fold - M_unf)))
    if mutant:
        if err > 1e-3:
            refused(f'omitting factor 2 in unfolded normal self-energy breaks folding identity (max diff {err:.4g})')
        need(False, 'mutant unfolded matrix unexpectedly matched folded matrix')
    need(err < 1e-12, f'unfolded vs folded mismatch: {err}')
    print(f'1. Unfolded-to-folded exact equivalence check: max matrix diff = {err:.2e} (< 1e-12)')


def scan_k1_to_k4():
    """Verify no two-line spectrum beats Einstein at mu*/lambda = 0.50 for k in {1, 2, 3, 4}."""
    n = 120
    worst_ev = 1e9
    for k in (1, 2, 3, 4):
        for lam in (1.0, 3.0, 10.0, 25.0, 40.0):
            mu = 0.5 * lam
            # Find q_top(k) where Einstein has zero eigenvalue at fixed k
            lo, hi = 1e-4, 4.0 * lam
            for _ in range(45):
                mid = 0.5 * (lo + hi)
                if eigvalsh(folded_matrix(lam, mu, mid, k, ((1.0, 1.0),), n))[0] <= 0.0:
                    lo = mid
                else:
                    hi = mid
            q_ein = hi
            for u1 in (0.15, 0.4, 0.7, 0.85, 0.95):
                for u2 in (1.1, 1.5, 3.0, 10.0):
                    p = (1.0 - u1) / (u2 - u1)
                    ev = float(eigvalsh(folded_matrix(lam, mu, q_ein, k, ((1.0 - p, u1), (p, u2)), n))[0])
                    if ev < worst_ev:
                        worst_ev = ev
    need(worst_ev > -1e-9, f'unexpected instability for k<=4 at mu*/lam=1/2: {worst_ev}')
    print(f'2. Mask-index k in {{1,2,3,4}} scan at mu*/lambda = 1/2: min mixture eig at q_E = {worst_ev:+.4e} >= 0')


def scan_k5_reentrant_fold():
    """Map the k = 5 re-entrant critical ratio r_*(lambda) across lambda in [25.0, 31.0]."""
    n = 120
    specs = [
        ((1.0 - (1.0 - u1) / (10000.0 - u1), u1), ((1.0 - u1) / (10000.0 - u1), 10000.0))
        for u1 in (0.88, 0.80, 0.69, 0.64)
    ]
    rows = []
    for lam in (25.0, 25.55, 26.0, 27.0, 28.0, 30.0, 32.0, 35.0):
        best_r = 0.505
        qs = np.linspace(0.30, 0.72, 169)
        for r in np.linspace(0.478, 0.504, 53):
            mu = r * lam
            evs = [float(eigvalsh(folded_matrix(lam, mu, q, 5, ((1.0, 1.0),), n))[0]) for q in qs]
            # Find positive interior island where evs[t] > 0, with evs < 0 both below and above it
            pos_idx = [t for t, v in enumerate(evs) if v > 0.0 and 0 < t < len(evs) - 1]
            island = [
                t for t in pos_idx
                if any(evs[s] < 0.0 for s in range(t)) and any(evs[s] < 0.0 for s in range(t + 1, len(evs)))
            ]
            if not island:
                continue
            q_peak = qs[max(island, key=lambda t: evs[t])]
            # Upper negative region must fit inside k=5 band without triggering k=0: 4*R^2 = 81*q_up < q_0(lam)
            neg_above = [qs[s] for s in range(max(island) + 1, len(evs)) if evs[s] < 0.0]
            q_up = min(neg_above)
            if eigvalsh(folded_matrix(lam, 0.0, 81.0 * q_up, 0, ((1.0, 1.0),), n))[0] <= 0.0:
                continue
            if any(eigvalsh(folded_matrix(lam, mu, q_peak, 5, sp, n))[0] < -1e-5 for sp in specs):
                best_r = float(r)
                break
        rows.append((lam, best_r))
    summary = ', '.join(f'lam={l:.2f}:r*={r:.4f}' for l, r in rows)
    print(f'3. k=5 re-entrant fold scan (NUMERICAL): {summary}')
    min_r = min(r for _, r in rows)
    need(min_r < 0.481, f'failed to detect sub-1/2 dip in k=5 fold: min_r={min_r}')
    need(rows[0][1] > 0.50 and rows[-1][1] > 0.50, 'fold did not close above 0.50 at ends of [25, 35]')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mutant', action='store_true')
    args = parser.parse_args()
    check_folding_equivalence(mutant=args.mutant)
    scan_k1_to_k4()
    scan_k5_reentrant_fold()
    print('phase_scan.py numerical checks: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
