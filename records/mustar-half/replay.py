"""Common-cutoff certificates for mu*/lambda <= 1/2: Einstein vs two-line spectra.

Uses exact Fraction arithmetic, directed integer-enclosure matrices (scale S = 2**30),
exact Cholesky residual certification on every Coulomb-mask subwindow up to the exact
Theorem 4 asymptotic handoff q_asymp = 4*lambda, and exact finite-support quadratic-form
witnesses on the cold side.

Run:
    python -B replay.py            # verifies bounds.json without rewriting (exit 0)
    python -B replay.py --write    # regenerates bounds.json (exit 0)
    python -B replay.py --mutant {coulomb,spectrum,endpoint,tail,sign}  # exit 1
"""

import argparse
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

import numpy as np
from scipy.linalg import cholesky, eigh

HERE = Path(__file__).resolve().parent
S = 2**30
G = 2**26


def up(x):
    return -(-x.numerator // x.denominator)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def matvec(a, x, extra=0):
    """Exact integer matrix-vector dot product without clamping."""
    limit = 2**62
    rows, cols = a.shape
    if a.size == 0 or x.size == 0:
        return [0] * rows
    max_a = int(np.max(np.abs(a)))
    max_x = int(np.max(np.abs(x)))
    if max_a * max_x * cols + int(extra) < limit:
        return [int(v) for v in (a @ x)]
    xl = x.tolist()
    return [sum(int(u) * int(v) for u, v in zip(row, xl)) for row in a.tolist()]


def cutoff(q, scale2):
    """Exact count k of indices i >= 0 with (2i+1)^2 * q < 4 * scale2."""
    x = F(4 * scale2) / q
    return (isqrt(up(x) - 1) + 1) // 2


def windows(lo, hi, scale2):
    """Partition [lo, hi] into exact subintervals on each of which k(q, scale2) is constant."""
    while lo < hi:
        k = cutoff(lo, scale2)
        right = hi if k == 0 else min(hi, F(4 * scale2, (2 * k - 1) ** 2))
        yield lo, right, k
        lo = right


def weights(lam, q, count, spectrum):
    """Exact rational phonon weights a_j for j = 1..count-1; a_0 cancelled in folded form."""
    return [F(0)] + [
        sum(lam * th * u / (u + q * j * j) for th, u in spectrum)
        for j in range(1, count)
    ]


def directed(a):
    lo = np.array([int(x * S) for x in a], dtype=np.int64)
    hi = np.array([up(x * S) for x in a], dtype=np.int64)
    return lo, hi


def far_lump(b, n, head_sum, mutant=False):
    return F(0) if mutant else 25 * b * b * head_sum / (4 * (2 * n) ** 4)


class Folded:
    def __init__(self, n):
        self.n = n
        i = np.arange(n, dtype=np.int64)
        j = np.arange(n, 2 * n, dtype=np.int64)
        self.odd = 2 * i + 1
        self.diff = np.abs(i[:, None] - i)
        self.hank = i[:, None] + i + 1
        self.edge0 = j[:, None] - i
        self.edge1 = j[:, None] + i + 1
        self.quad = np.maximum(1, 2**27 // (i + 1) ** 2)
        self.lin = 2**24 // (i + 1)
        self.tail_d = j + 1

    def hot_head(self, lam, mu, left, right, k, mutant_sign=False):
        n = self.n
        need(k <= n, 'Coulomb cutoff overlaps truncated tail')
        need(mu >= 0 or mutant_sign, 'negative mu*')
        b = lam / left
        if n * n < 2 * b:
            return None
        lo = directed(weights(lam, right, 2 * n, ((F(1), F(1)),)))[0]
        hi = directed(weights(lam, left, 3 * n, ((F(1), F(1)),)))[1]
        pot_lo = self.odd * S + 2 * lo[:n].cumsum()
        pot_hi = self.odd * S + 2 * hi[:n].cumsum()
        lower = -hi[self.diff] - hi[self.hank]
        upper = -lo[self.diff] - lo[self.hank]
        lower[:k, :k] += int(2 * mu * S) if mu >= 0 else -up(-2 * mu * S)
        upper[:k, :k] += up(2 * mu * S) if mu >= 0 else -int(-2 * mu * S)
        diag = np.diag_indices(n)
        lower[diag] += pot_lo
        upper[diag] += pot_hi
        center = (lower + upper) // 2
        radius = upper - center
        h = self.lin
        rad_pen = matvec(radius, h, int(h.max()))
        center[diag] -= np.array(
            [(r + int(hv) - 1) // int(hv) for r, hv in zip(rad_pen, h)],
            dtype=np.int64,
        )
        # Schur complement bound against F_QQ >= diag(j + 1)
        edge = hi[self.edge0] + hi[self.edge1]
        h = self.quad
        den = self.tail_d * S
        row_raw = matvec(edge, h, int(den.max()))
        row = np.array(
            [(rr + int(dv) - 1) // int(dv) for rr, dv in zip(row_raw, den)],
            dtype=np.int64,
        )
        near_raw = matvec(edge.T, row, int(h.max()))
        near = np.array(
            [(nr + int(hv) - 1) // int(hv) for nr, hv in zip(near_raw, h)],
            dtype=np.int64,
        )
        far = far_lump(b, n, int(h.sum()))
        center[diag] -= near + np.array(
            [up(S * far / int(v)) for v in h], dtype=np.int64
        )
        return center

    def cold_data(self, lam, mu, q, scale2, spectrum):
        a = weights(lam, q, 2 * self.n, spectrum)
        k = min(cutoff(q, scale2), self.n)
        vals = np.array([float(v) for v in a], dtype=float)
        mat = np.diag(self.odd + 2 * vals[: self.n].cumsum()) - vals[self.diff] - vals[self.hank]
        mat[:k, :k] += float(2 * mu)
        d = 1.0 / np.sqrt(self.odd)
        scaled = (mat * d[:, None]) * d[None, :]
        _, vec = eigh(scaled, subset_by_index=(0, 0), check_finite=False)
        raw = vec[:, 0] * d
        return np.rint(raw / max(abs(raw)) * 2**22).astype(np.int64)

    def cold_check(self, lam, mu, q, x, scale2, spectrum=((F(1), F(1)),)):
        n = self.n
        lo, hi = directed(weights(lam, q, 2 * n, spectrum))
        different = (x < 0)[:, None] != (x < 0)
        pair = np.where(different, hi[self.diff] + hi[self.hank], lo[self.diff] + lo[self.hank])
        norm = self.odd * S + 2 * hi[:n].cumsum()
        prod = matvec(pair, x)
        bound = sum(int(v) * (int(d) * int(v) - int(y)) for v, d, y in zip(x, norm, prod))
        k = min(cutoff(q, scale2), n)
        return bound + up(2 * mu * S) * int(x[:k].sum()) ** 2 < 0


def gram_positive(a):
    if a is None:
        return False
    n = len(a)
    a_float = a.astype(float) / S
    for shift in (2e-4, 2e-5, 2e-6):
        try:
            l = cholesky(a_float - shift * np.eye(n), lower=True, check_finite=False)
        except np.linalg.LinAlgError:
            continue
        if np.max(np.abs(l)) * G >= 2**31 - 1 or np.max(np.abs(a)) >= 2**40:
            continue
        L = np.rint(l * G).astype(np.int64)
        if int(np.max((((np.abs(L) + 255) // 256) ** 2).sum(axis=1))) * 256**2 >= 2**62:
            continue
        res = a * (G * G // S) - L @ L.T
        if np.max(np.abs(res)) >= 2**62 // n:
            continue
        if bool(np.all(2 * res.diagonal() > np.abs(res).sum(axis=1))):
            return True
    return False


def cover(test, lo, hi, k, depth=0):
    if test(lo, hi, k):
        return 1
    need(depth < 18, f'hot interval cannot be certified: {float(lo):.12g} {float(hi):.12g} k={k}')
    mid = (lo + hi) / 2
    return cover(test, lo, mid, k, depth + 1) + cover(test, mid, hi, k, depth + 1)


def pi_bounds():
    def atan(x):
        lower = sum((-1) ** j * x ** (2 * j + 1) / (2 * j + 1) for j in range(20))
        return lower, lower + x**41 / 41

    l, h = atan(F(1, 5))
    m, n = atan(F(1, 239))
    return 16 * l - 4 * n, 16 * h - 4 * m


def c_bounds(lam, left, right):
    pl, ph = pi_bounds()
    digits = 10**26

    def rounded(q, pi):
        s = digits**2 * q / (4 * lam * pi * pi)
        return isqrt(s.numerator // s.denominator)

    return F(rounded(left, ph), digits), F(1 + rounded(right, pl), digits)


def spectrum_of(mix):
    th = F(mix['high_p'])
    low = F(mix['low_u'])
    high = F(mix['high_u'])
    need(0 < th < 1 and 0 < low < 1 < high, 'invalid two-line spectrum ordering')
    need((1 - th) * low + th * high == 1, 'mixture normalized first moment != 1')
    return ((1 - th, low), (th, high))


def hot_einstein(f, lam, mu, q_hi, scale2, handoff, mutant_sign=False):
    need(q_hi < handoff, 'upper bracket exceeds asymptotic handoff 4*lambda')
    # Check asymptotic Theorem 4 validity at handoff: pi^2 / 3 < 4 so 1 - lam*pi^2/(3*handoff) > 0
    _, ph = pi_bounds()
    need(lam * ph * ph < 3 * handoff, 'asymptotic row-margin condition failed at handoff')
    need(mu >= 0 or mutant_sign, 'negative mu* rejected')
    return sum(
        cover(lambda l, r, k: gram_positive(f.hot_head(lam, mu, l, r, k, mutant_sign=mutant_sign)), l, r, k)
        for l, r, k in windows(q_hi, handoff, scale2)
    )


def run_case(data, receipt):
    lam, mu, scale2 = F(data['lambda']), F(data['mu']), F(data['R2'])
    low, high = map(F, data['einstein'])
    handoff = 4 * lam
    need(0 < low < high < handoff, f'bad bracket for {data["name"]}')
    f = Folded(int(data['size_cold']))
    x = f.cold_data(lam, mu, low, scale2, ((F(1), F(1)),))
    need(f.cold_check(lam, mu, low, x, scale2), f'Einstein cold sign failed: {data["name"]}')
    boxes = hot_einstein(Folded(int(data['size_hot'])), lam, mu, high, scale2, handoff)
    cl, ch = c_bounds(lam, low, high)
    receipt[data['name']] = {
        'einstein_q': [str(low), str(high)],
        'einstein_C': [str(cl), str(ch)],
        'handoff_q': str(handoff),
        'boxes': boxes,
    }
    print(
        f'{data["name"]:>22} lam={data["lambda"]} mu={data["mu"]} R^2={data["R2"]}: '
        f'q_E in [{float(low):.6g},{float(high):.6g}] C_E={float(cl):.6g} boxes={boxes}',
        flush=True,
    )
    if 'mix' in data:
        mix = data['mix']
        spectrum = spectrum_of(mix)
        q = F(mix['q'])
        need(q > high, 'mixture witness must sit strictly above Einstein upper endpoint')
        g = Folded(int(mix['size']))
        y = g.cold_data(lam, mu, q, scale2, spectrum)
        need(g.cold_check(lam, mu, q, y, scale2, spectrum), f'mixture cold sign failed: {data["name"]}')
        receipt[data['name']]['mix'] = {
            'spectrum': [[str(th), str(u)] for th, u in spectrum],
            'q': str(q),
        }
        print(
            f'{data["name"]:>22} two-line unstable at q={q} = {float(q / high):.4f} * q_E_hi (mu*/lam={float(mu / lam):.6f})',
            flush=True,
        )


def control(ok, why):
    if not ok:
        raise AssertionError(f'control failed: {why}')


def refused(why):
    print(f'REFUSED: {why}')
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--mutant', choices=('coulomb', 'spectrum', 'endpoint', 'tail', 'sign'))
    mode.add_argument('--write', action='store_true', help='explicitly regenerate bounds.json')
    args = parser.parse_args()
    data = json.loads((HERE / 'fixtures.json').read_text(encoding='utf8'))
    receipt_path = HERE / 'bounds.json'

    if args.mutant:
        case = next(c for c in data['cases'] if c['name'] == 'subhalf-26-12over25')
        lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
        low, high = map(F, case['einstein'])
        handoff = 4 * lam
        if args.mutant == 'sign':
            boxes = hot_einstein(Folded(int(case['size_hot'])), lam, mu, high, scale2, handoff)
            control(boxes > 0, 'unmutated repulsive hot certificate passed')
            try:
                hot_einstein(Folded(int(case['size_hot'])), lam, -mu, high, scale2, handoff, mutant_sign=True)
            except ValueError as exc:
                refused(f'sign-flipped Coulomb mask rejected ({exc})')
            need(False, 'sign mutant passed unexpectedly')
        if args.mutant == 'tail':
            j = 2 * Folded(64).n
            a = weights(lam, low, j + 2, ((F(1), F(1)),))
            actual = (a[j] + a[j + 1]) ** 2 / (j + 1)
            control(actual < far_lump(lam / low, 64, 1), 'true far-tail bound holds')
            if not (actual < far_lump(lam / low, 64, 1, mutant=True)):
                refused('disabled far-tail bound is exceeded by exact omitted term')
            need(False, 'tail mutant passed unexpectedly')
        f = Folded(int(case['size_cold']))
        x = f.cold_data(lam, mu, low, scale2, ((F(1), F(1)),))
        control(f.cold_check(lam, mu, low, x, scale2), 'unmutated cold witness holds')
        if args.mutant == 'coulomb':
            if not f.cold_check(lam, 2 * mu, low, x, scale2):
                refused('cold certificate dies when Coulomb repulsion is doubled')
            need(False, 'coulomb mutant passed unexpectedly')
        if args.mutant == 'endpoint':
            if not f.cold_check(lam, mu, high, x, scale2):
                refused('cold witness refused at certified-stable upper endpoint q_hi')
            need(False, 'endpoint mutant passed unexpectedly')
        if args.mutant == 'spectrum':
            mix = case['mix']
            mirrored = dict(mix, low_u=mix['high_u'], high_u=mix['low_u'])
            try:
                spectrum_of(mirrored)
            except ValueError as exc:
                refused(f'mirrored spectrum rejected ({exc})')
            need(False, 'spectrum mutant passed unexpectedly')

    receipt = {}
    for entry in data['cases'] + data['anchors']:
        run_case(entry, receipt)

    if args.write:
        receipt_path.write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf8')
        print(f'wrote {receipt_path.name}')
    else:
        need(receipt_path.exists(), 'bounds.json missing (run with --write first)')
        stored = json.loads(receipt_path.read_text(encoding='utf8'))
        need(receipt == stored, 'recomputed receipt differs from stored bounds.json')
        print('stored bounds.json verified without rewriting')


if __name__ == '__main__':
    main()
