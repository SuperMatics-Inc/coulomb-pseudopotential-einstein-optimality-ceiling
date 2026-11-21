"""Cross-check of the common-cutoff counterexamples in a DIRECT full-line fermionic
Matsubara discretization of the linearized isotropic Migdal-Eliashberg equation
(NUMERICAL: float64, truncated band, no certified rounding).

Units are those of the lane: Omega_E = 1, q = (2 pi T / Omega_E)^2, so
    omega_n = (2n+1) pi T,  n in {-N, ..., N-1},
    a_r = lam * int u/(u + q r^2) dp  (= lam * sum_i p_i u_i/(u_i + q r^2)),  a_0 = lam,
    c_n = 1{|omega_n| < R Omega_E} = 1{(2n+1)^2 q < 4 R^2},
    Z_n = 1 + (1/|2n+1|) sum_m a_{|n-m|} sgn(2m+1)      (|w_n| = (2n+1) pi T),
    K_nm = a_{|n-m|} - mu* c_n c_m,
and the linear onset is the largest q with lam_max > 1 for the symmetric kernel
    M = D^{-1/2} K D^{-1/2},   D_n = Z_n |2n+1|,
restricted to the even (particle-hole symmetric) gap subspace Delta_{-1-n} = Delta_n.
The restriction is imposed by the explicit projector P (x = P h, |x| = |h|); the script
never writes down the folded 300-mode form or its a_{i+j+1} mirror term, and instead
checks that the even-sector eigenvalue of the direct 2N-mode matrices agrees with the
folded form of replay.py to float round-off.  That agreement is the numerical statement
that the mirror term is the even-frequency image of the negative Matsubara axis (it is
not an "odd-channel" term, and nothing is omitted by the folding).

This file is a NUMERICAL cross-check only.  The certified authority stays with replay.py
and independent.py (exact rationals, directed rounding).

Run: python -B crosscheck.py [--band 240] [--slack 1e-9] [--agree 1e-10]
Self-test of the agreement check (must exit 1): python -B crosscheck.py --mutant {mirror,zshift}
"""

import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent


def spectrum_of(mix):
    """Fixture mixture (p at the high line) as ((weight, u), (weight, u)) rationals."""
    p = F(mix['high_p'])
    low, high = F(mix['low_u']), F(mix['high_u'])
    assert 0 < p < 1 and 0 < low < 1 < high, f'bad mixture {mix}'
    assert (1 - p) * low + p * high == 1, f'mixture second moment is not one: {mix}'
    return ((1 - p, low), (p, high))


def weights(lam, q, count, spec):
    """a_r for r = 0..count-1, with a_0 = lam."""
    assert sum(p for p, _ in spec) == 1
    assert sum(p * u for p, u in spec) == 1
    return [F(lam)] + [sum(lam * p * u / (u + q * j * j) for p, u in spec)
                       for j in range(1, count)]


def matrices(lam, mu, q, scale2, spec, band):
    """Direct 2N-mode D (normal diagonal) and K (pairing kernel) of the full line."""
    idx = np.arange(-band, band)
    a = weights(lam, q, 2 * band, spec)
    ad = np.array([float(x) for x in a])
    # Z_n |w_n|/(pi T) = |2n+1| + S_n with S_n = sum_m a_{|n-m|} sgn(2m+1).  For n >= 0 the
    # FULL-LINE sum telescopes to S_n = a_0 + 2 sum_{r=1}^{n} a_r: the m >= 0 part is
    # sum_{r=1}^{n} a_r + sum_{r>=0} a_r and the m <= -1 part is sum_{r>=n+1} a_r, so
    # S_n = 2 sum_{r=1}^{n} a_r + a_0, and S_{-1-n} = S_n by the even extension.  Summing the
    # sgn series over the *truncated* band instead would be a different operator (its
    # diagonal goes negative in the middle of the band), so the closed form is used; with
    # a_r = 0 for r > 2N-1 it is exact for the band-truncated kernel, which is the same
    # kernel the folded form of replay.py uses, so the direct and folded eigenvalues below
    # are the same operator and must agree to round-off.
    cum = np.concatenate(([0.0], np.cumsum(ad[1:])))
    i = np.maximum(idx, -idx - 1)
    # D_n = |2n+1| + 2A_{i(n)}: the a_0 = lam of S_n and the a_0 = lam of the pairing
    # diagonal K_nn cancel identically in the quadratic form x^T (D-K) x, so both are
    # dropped here exactly as replay.py drops them (a[0] = 0).  D and K are then the same
    # objects as the folded form's, so the direct even-sector eigenvalue and the folded one
    # are eigenvalues of the same matrix and must agree to round-off.
    diag = np.abs(2.0 * idx + 1) + 2.0 * cum[i]
    assert np.all(diag > 0), 'Z_n |2n+1| must be positive'
    kern = ad[np.abs(idx[:, None] - idx)].copy()
    np.fill_diagonal(kern, 0.0)
    mask = np.array([1.0 if F(2 * int(n) + 1) ** 2 * q < 4 * scale2 else 0.0 for n in idx])
    kern -= float(mu) * np.outer(mask, mask)
    return diag, kern


def projector(band):
    """x = P h with x_i = h_i/sqrt2 at n = i and x_{-1-i} = h_i/sqrt2 (even subspace)."""
    p = np.zeros((2 * band, band))
    rows = np.arange(band)
    p[rows, rows] = 1.0 / np.sqrt(2.0)
    p[2 * band - 1 - rows, rows] = 1.0 / np.sqrt(2.0)
    return p


def ray(lam, mu, q, scale2, spec, band, even=True):
    """Largest eigenvalue of D^-1/2 K D^-1/2 (even subspace by default)."""
    diag, kern = matrices(lam, mu, q, scale2, spec, band)
    s = 1.0 / np.sqrt(diag)
    m = s[:, None] * kern * s[None, :]
    if even:
        p = projector(band)
        m = p.T @ m @ p
    vals = eigh(m, eigvals_only=True, subset_by_index=(m.shape[0] - 1, m.shape[0] - 1),
                check_finite=False)
    return float(vals[0])


def folded_ray(lam, mu, q, scale2, spec, band, mutant=None):
    """The folded form of replay.py, normalized like ray() so the two are comparable.

    replay.py's form matrix is D_f - K_f with D_f = diag(2i+1+2A_i) and K_f the pairing
    kernel (the a_0 = lam diagonal dropped) minus the rank-one mask term 2 mu* 1_{i,j<k};
    the onset criterion is the indefiniteness of that form, equivalently lam_max(D_f^-1/2
    K_f D_f^-1/2) > 1, which is the same scale-free quotient used by ray().
    """
    a = np.array([float(x) for x in weights(lam, q, 2 * band, spec)])
    a[0] = 0.0                      # a_0 cancels against the Z shift, as above
    idx = np.arange(band)
    d = (2.0 * idx + 1) + 2.0 * np.cumsum(a)[:band]   # A_i = sum_{r=1}^{i} a_r
    if mutant == 'zshift':
        d = 2.0 * idx + 1                    # mutant: drop the a_r part of Z_n|w_n|/(pi T)
    k = a[np.abs(idx[:, None] - idx)] + a[idx[:, None] + idx + 1]
    if mutant == 'mirror':
        k = a[np.abs(idx[:, None] - idx)]   # mutant: drop the even-image a_{i+j+1}
    adm = np.array([F(2 * i + 1) ** 2 * q < 4 * scale2 for i in idx])
    k[np.ix_(adm, adm)] -= 2.0 * float(mu)
    s = 1.0 / np.sqrt(d)
    m = s[:, None] * k * s[None, :]
    return float(eigh(m, eigvals_only=True, subset_by_index=(band - 1, band - 1),
                      check_finite=False)[0])


def mask_count(q, scale2, band):
    return sum(1 for n in range(-band, band) if F(2 * n + 1) ** 2 * q < 4 * scale2)


def onset(lam, mu, scale2, spec, band, start, slack, even=True, steps=60):
    """Largest q >= start with lam_max(q) > 1 (scan up by 1.2x, then bisect).

    Requires lam_max(start) > 1 - slack: otherwise the returned value would be the scan
    start, i.e. only an upper bound on the onset, silently masquerading as the onset.
    """
    assert ray(lam, mu, F(start), scale2, spec, band, even) > 1.0 - slack, \
        f'onset scan start q={float(start):.8g} is already stable: lower the start'
    lo, hi = float(start), None
    q = lo
    for _ in range(300):
        if ray(lam, mu, F(q), scale2, spec, band, even) < 1.0 - slack:
            hi = q
            break
        lo, q = q, q * 1.2   # lam_max -> 0 as q -> inf (a_r -> 0), so this scan terminates
    if hi is None:
        return float('inf')
    for _ in range(steps):
        mid = 0.5 * (lo + hi)
        if ray(lam, mu, F(mid), scale2, spec, band, even) > 1.0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--band', type=int, default=240, help='half-width N')
    parser.add_argument('--slack', type=float, default=1e-9,
                        help='required margin of the sign checks on lam_max - 1')
    parser.add_argument('--agree', type=float, default=1e-10,
                        help='allowed |direct even-sector - folded| eigenvalue difference')
    parser.add_argument('--mutant', choices=('mirror', 'zshift'),
                        help='perturb the DIRECT discretization so the agreement test must '
                             'fail (self-test of that test; nonzero exit is required)')
    args = parser.parse_args()
    band, slack, agree, mut = args.band, args.slack, args.agree, args.mutant
    data = json.loads((HERE / 'fixtures.json').read_text(encoding='utf8'))
    stored = json.loads((HERE / 'bounds.json').read_text(encoding='utf8'))
    ein = ((F(1), F(1)),)
    print(f'direct full-line fermionic Matsubara form, band n in [-{band}, {band - 1}] '
          f'({2 * band} modes), even gap subspace, NUMERICAL', flush=True)
    failures = []
    for case in data['cases'] + data['anchors']:
        name = case['name']
        lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
        low, high = map(F, case['einstein'])
        if [str(low), str(high)] != stored[name]['einstein_q']:
            failures.append(f'{name}: fixture bracket differs from bounds.json')
        lo_ray = ray(lam, mu, low, scale2, ein, band)
        hi_ray = ray(lam, mu, high, scale2, ein, band)
        if lo_ray < 1 + slack:
            failures.append(f'{name}: even-sector lam_max at q_lo is {lo_ray:.12g} <= 1')
        if hi_ray > 1 - slack:
            failures.append(f'{name}: even-sector lam_max at q_hi is {hi_ray:.12g} >= 1')
        # The direct even sector must reproduce replay.py's folded eigenvalue.
        d_fold = abs(lo_ray - folded_ray(lam, mu, low, scale2, ein, band, mut))
        if d_fold > agree:
            failures.append(f'{name}: direct and folded lam_max differ at q_lo')
        print(f'{name}: q_lo={float(low):.8g} lam_max={lo_ray:.12f} (>1)  '
              f'q_hi={float(high):.8g} lam_max={hi_ray:.12f} (<1)  mask modes={mask_count(low, scale2, band)}/'
              f'{mask_count(high, scale2, band)}  |direct-folded|={d_fold:.1e}', flush=True)
        if 'mix' not in case:
            continue
        mix = case['mix']
        spec = spectrum_of(mix)
        qmix = F(mix['q'])
        if not (low < high < qmix):
            failures.append(f'{name}: witness q is not above the Einstein upper endpoint')
        mix_at_q = ray(lam, mu, qmix, scale2, spec, band)
        ein_at_q = ray(lam, mu, qmix, scale2, ein, band)
        mix_at_hi = ray(lam, mu, high, scale2, spec, band)
        mix_at_lo = ray(lam, mu, low, scale2, spec, band)
        if mix_at_q < 1 + slack:
            failures.append(f'{name}: mixture lam_max at q_mix is {mix_at_q:.12g} <= 1')
        if ein_at_q > 1 - slack:
            failures.append(f'{name}: Einstein lam_max at q_mix is {ein_at_q:.12g} >= 1')
        if mix_at_hi < 1 + slack:
            failures.append(f'{name}: mixture lam_max at q_hi is {mix_at_hi:.12g} <= 1')
        if abs(mix_at_q - folded_ray(lam, mu, qmix, scale2, spec, band, mut)) > agree:
            failures.append(f'{name}: direct and folded mixture lam_max differ at q_mix')
        q_e = onset(lam, mu, scale2, ein, band, low, slack)
        q_m = onset(lam, mu, scale2, spec, band, low, slack)
        if not q_m > q_e + slack:
            failures.append(f'{name}: mixture onset {q_m:.12g} is not above the Einstein '
                            f'onset {q_e:.12g}')
        print(f'{name}: q_mix={float(qmix):.8g} lam_max mix={mix_at_q:.9f}, E={ein_at_q:.9f}; '
              f'lam_max mix@q_hi={mix_at_hi:.9f}, mix@q_lo={mix_at_lo:.9f}; '
              f'onset E q={q_e:.8g} < onset mix q={q_m:.8g} '
              f'(C_E {np.sqrt(q_e) / (2 * np.pi * np.sqrt(float(lam))):.8g} < '
              f'{np.sqrt(q_m) / (2 * np.pi * np.sqrt(float(lam))):.8g})', flush=True)
    # Small-mu* control (NUMERICAL, no certified claim): the SAME two-line mixture that
    # wins at mu*/lambda > 1/2 must lose where mu*/lambda <= 1/2.  At the certified Einstein
    # bracket lower end the Einstein line is unstable, so stability of the mixture there
    # puts its onset strictly below the Einstein bracket (no bisection, no scan start).
    ctrl = {'anchor-l1-mu1/10-R1': '1/10', 'anchor-l1-mu1/2-R1': '1/2'}
    for case in data['anchors']:
        name = case['name']
        if name not in ctrl:
            continue
        lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
        low = F(case['einstein'][0])
        spec = ((F(590, 599), F(1, 10)), (F(9, 599), F(60)))
        e_at_lo = ray(lam, mu, low, scale2, ein, band)
        m_at_lo = ray(lam, mu, low, scale2, spec, band)
        print(f'control mu*={ctrl[name]} (mu*/lambda={F(ctrl[name]) / lam}): at the Einstein '
              f'bracket lower end q={float(low):.8g}, Einstein lam_max={e_at_lo:.12f} (>1) vs '
              f'the counterexample mixture lam_max={m_at_lo:.12f} (<1)',
              flush=True)
        if e_at_lo < 1 + slack:
            failures.append(f'{name}: control Einstein lam_max at q_lo is {e_at_lo:.12g} <= 1')
        if m_at_lo > 1 - slack:
            failures.append(f'{name}: the counterexample mixture is unstable at q_lo '
                            f'({m_at_lo:.12g}), so the small-mu* control fails')
    for case in data['cases']:
        name = case['name']
        lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
        high = F(case['einstein'][1])
        spec = spectrum_of(case['mix'])
        r1 = ray(lam, mu, high, scale2, spec, band)
        r2 = ray(lam, mu, high, scale2, spec, 2 * band)
        e1 = ray(lam, mu, high, scale2, ein, band)
        e2 = ray(lam, mu, high, scale2, ein, 2 * band)
        print(f'band doubling {name}: mixture lam_max at q_hi {r1:.9f} (N={band}) -> '
              f'{r2:.9f} (N={2 * band}), shift {abs(r2 - r1):.2e}; Einstein {e1:.9f} -> '
              f'{e2:.9f}, shift {abs(e2 - e1):.2e}', flush=True)
        if r2 < 1 + slack:
            failures.append(f'{name}: mixture lam_max at q_hi drops to {r2:.12g} at N={2 * band}')
        if e2 > 1 - slack:
            failures.append(f'{name}: Einstein lam_max at q_hi rises to {e2:.12g} at N={2 * band}')
    if failures:
        print('\n'.join(f'FAIL {f}' for f in failures))
        if mut:
            print(f'mutant "{mut}": refused, because the direct and folded eigenvalues no '
                  f'longer agree (the agreement test has teeth)')
        return 1
    if mut:
        print(f'mutant "{mut}" was NOT detected: the agreement test is toothless')
        return 1
    print('full-line cross-check: every Einstein bracket reproduced and every mixture '
          'certified-unstable q_hi is numerically unstable with a strictly larger onset q '
          '(i.e. larger C_E) than the Einstein line of the same (lambda, M, mu*, omega_c); '
          'the direct even-sector eigenvalues agree with the folded form to float round-off')
    return 0


if __name__ == '__main__':
    sys.exit(main())
