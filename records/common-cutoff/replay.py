"""Common-cutoff certificates: Einstein stability versus a two-line spectrum at one shared mask.

Model (see RIGOR.md): flat DOS, infinite band, isotropic even linear Migdal-Eliashberg,
pairing-only Coulomb mu* 1_{|w_n|<wc} 1_{|w_m|<wc} with no Coulomb in Z, and a cutoff
wc = R Omega_E that depends on (lambda, M) only, hence identical for every spectrum.
Units are those of C-LAMBDA-MU: energies, w_n = (2n+1) pi T, Omega_E = sqrt(M/lambda),
q = (2 pi T / Omega_E)^2, u = (Omega/Omega_E)^2, dp a probability with int u dp = 1,
a_j = lambda int dp u/(u+q j^2), so int u dp = 1 and a_0 = lambda.

The mask in the folded index i (the pair (i,-i-1), |w_i| = d_i pi T, d_i = 2i+1) is
d_i^2 q < 4 R^2, i.e. i < k with k = cutoff(q, R^2).

Every certificate is rational: the weights a_j are exact Fractions at rational q, and the
folded quadratic form is compared against magnitude bounds, never against floating point.
"""
import argparse
import json
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


def control(ok, why):
    """A mutant's unmutated control; breaking it invalidates the mutant (exit 2)."""
    if not ok:
        print(f'CONTROL FAILED (mutant invalid): {why}')
        raise SystemExit(2)
    print(f'control passed: {why}')


def refused(why):
    """The mutant's perturbed statement was refused, as required (exit 1)."""
    print(f'mutant refused: {why}')
    raise SystemExit(1)


def contraction(a, x, extra=0):
    # Exact int64 dot products.  Every row output is bounded by |a|max*cols*|x|max + extra,
    # so the product is exact whenever that bound is below 2**62.  A larger row would
    # overflow silently, so it is an assertion failure, never a clamp.
    limit = 2**62
    row_bound = int(np.abs(a).max())*a.shape[1]*int(np.abs(x).max())+int(extra)
    if row_bound < limit:
        return a@x
    # Crude row bound exceeded: accumulate exactly in Python integers and assert every
    # entry fits int64.  A value outside the range is an assertion failure, never a clamp.
    values = x.tolist()
    out = np.empty(a.shape[0], dtype=np.int64)
    for i, row in enumerate(a.tolist()):
        v = sum(y*z for y, z in zip(row, values))
        need(-limit < v < limit, f'contraction entry {v} exceeds the exact int64 range')
        out[i] = v
    return out


def cutoff(q, scale2):
    # d^2*q < 4*scale2; count admissible positive odd d exactly.
    x = F(4*scale2)/q
    return (isqrt(up(x)-1)+1)//2


def windows(lo, hi, scale2):
    # Each window carries the mask of its left end, the largest on the window.
    while lo < hi:
        k = cutoff(lo, scale2)
        right = min(hi, F(4*scale2, (2*k-1)**2)) if k else hi
        yield lo, right, k
        lo = right


def weights(lam, q, count, spectrum):
    return [F(0)] + [sum(lam*p*u/(u+q*j*j) for p, u in spectrum)
                     for j in range(1, count)]


def directed(a):
    return (np.array([int(x*S) for x in a], dtype=np.int64),
            np.array([up(x*S) for x in a], dtype=np.int64))


class Folded:
    def __init__(self, n):
        self.n = n
        i = np.arange(n, dtype=np.int64)
        j = np.arange(n, 2*n, dtype=np.int64)
        self.odd = 2*i+1
        self.diff = abs(i[:, None]-i)
        self.hank = i[:, None]+i+1
        self.edge0 = j[:, None]-i
        self.edge1 = j[:, None]+i+1
        self.quad = np.maximum(1, 2**27//(i+1)**2)
        self.lin = 2**24//(i+1)
        self.tail_d = j+1

    def hot_head(self, lam, mu, left, right, k):
        n = self.n
        need(k <= n, 'Coulomb overlaps tail')
        b = lam/left
        if n*n < 2*b:
            return None
        lo = directed(weights(lam, right, 2*n, ((F(1), F(1)),)))[0]
        hi = directed(weights(lam, left, 3*n, ((F(1), F(1)),)))[1]
        pot_lo = self.odd*S + 2*lo[:n].cumsum()
        pot_hi = self.odd*S + 2*hi[:n].cumsum()
        lower = -hi[self.diff]-hi[self.hank]
        upper = -lo[self.diff]-lo[self.hank]
        lower[:k, :k] += int(2*mu*S)
        upper[:k, :k] += up(2*mu*S)
        diag = np.diag_indices(n)
        lower[diag] += pot_lo
        upper[diag] += pot_hi
        center = (lower+upper)//2
        radius = upper-center
        h = self.lin
        center[diag] -= (contraction(radius, h, h.max())+h-1)//h
        # F_QQ >= diag(j+1). Bound the signed cross term via weighted Cauchy.
        edge = hi[self.edge0]+hi[self.edge1]
        h = self.quad
        den = self.tail_d*S
        row = (contraction(edge, h, den.max())+den-1)//den
        near = (contraction(edge.T, row, h.max())+h-1)//h
        far = far_lump(b, n, int(h.sum()))
        center[diag] -= near + np.array([up(S*far/int(v)) for v in h], dtype=np.int64)
        return center

    def cold_data(self, lam, mu, q, scale2, spectrum):
        a = weights(lam, q, 2*self.n, spectrum)
        k = min(cutoff(q, scale2), self.n)
        vals = np.array(a, dtype=float)
        mat = np.diag(self.odd+2*vals[:self.n].cumsum()) - vals[self.diff]-vals[self.hank]
        mat[:k, :k] += float(2*mu)
        _, vec = eigh(mat, subset_by_index=(0, 0), check_finite=False)
        return np.rint(vec[:, 0]/max(abs(vec[:, 0]))*2**22).astype(np.int64)

    def cold_check(self, lam, mu, q, x, scale2, spectrum=((F(1), F(1)),)):
        n = self.n
        lo, hi = directed(weights(lam, q, 2*n, spectrum))
        different = (x < 0)[:, None] != (x < 0)
        pair = np.where(different, hi[self.diff]+hi[self.hank], lo[self.diff]+lo[self.hank])
        norm = self.odd*S + 2*hi[:n].cumsum()
        # Contractions of the integer rows are accumulated using unbounded integers.
        bound = sum(int(v)*(int(d)*int(v)-int(y)) for v, d, y in zip(x, norm, contraction(pair, x)))
        k = min(cutoff(q, scale2), n)
        return bound + up(2*mu*S)*int(x[:k].sum())**2 < 0


def far_lump(b, n, head_sum, mutant=False):
    return F(0) if mutant else 25*b*b*head_sum/(4*(2*n)**4)


def gram_positive(a):
    if a is None:
        return False
    n = len(a)
    try:
        l = cholesky(a.astype(float)/S - 2e-4*np.eye(n), lower=True, check_finite=False)
    except np.linalg.LinAlgError:
        return False
    if np.max(abs(l))*G >= 2**31-1 or np.max(abs(a)) >= 2**40:
        return False
    L = np.rint(l*G).astype(np.int64)
    if int(np.max((((abs(L)+255)//256)**2).sum(axis=1))) * 256**2 >= 2**62:
        return False
    res = a*(G*G//S) - L@L.T
    if np.max(abs(res)) >= 2**62//n:
        return False
    return bool(np.all(2*res.diagonal() > abs(res).sum(axis=1)))


def cover(test, lo, hi, k, depth=0):
    if test(lo, hi, k):
        return 1
    need(depth < 18, f'hot interval cannot be certified: {float(lo):.12g} {float(hi):.12g} K={k}')
    mid = (lo+hi)/2
    return cover(test, lo, mid, k, depth+1)+cover(test, mid, hi, k, depth+1)


def phonon_hots():
    # Zero-Coulomb upper endpoints, mu*-independent: adding the positive block only helps.
    prior = json.loads((HERE.parent.parent/'C-LAMBDA'/'brackets.json').read_text(encoding='utf8'))
    out = {lam: prior['q_numerators'][lam] for lam in ('0.5', '1', '1.5', '2', '3', '4', '6', '10')}
    out.update({label.rsplit(':', 1)[1]: bounds for label, bounds in prior['ambient_q_numerators'].items()})
    return {lam: F(bounds[1], prior['q_denominator']) for lam, bounds in out.items()}


def pi_bounds():
    def atan(x):
        lower = sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(20))
        return lower, lower+x**41/41
    l, h = atan(F(1, 5))
    m, n = atan(F(1, 239))
    return 16*l-4*n, 16*h-4*m


def c_bounds(lam, left, right):
    pl, ph = pi_bounds()
    digits = 10**26

    def rounded(q, pi):
        s = digits**2*q/(4*lam*pi*pi)
        return isqrt(s.numerator//s.denominator)
    return F(rounded(left, ph), digits), F(1+rounded(right, pl), digits)


def verify_receipt(recomputed, stored):
    need(recomputed == stored, 'recomputed brackets differ from the stored bounds.json receipt')


def spectrum_of(mix):
    lam_moment = F(mix['high_p'])
    low = F(mix['low_u'])
    high = F(mix['high_u'])
    need(0 < lam_moment < 1 and 0 < low < 1 < high, 'bad mixture')
    need((1-lam_moment)*low+lam_moment*high == 1, 'mixture moment is not one')
    return ((1-lam_moment, low), (lam_moment, high))


def hot_einstein(f, lam, mu, q_hi, scale2, handoff):
    need(q_hi < handoff, 'bracket above the phonon handoff')
    boxes = sum(cover(lambda l, r, k: gram_positive(f.hot_head(lam, mu, l, r, k)), l, r, k)
                for l, r, k in windows(q_hi, handoff, scale2))
    return boxes


def run_case(data, phonon, receipt, write):
    lam, mu, scale2 = F(data['lambda']), F(data['mu']), F(data['R2'])
    low, high = map(F, data['einstein'])
    need(0 < low < high < phonon[data['lambda']], 'bad bracket or phonon handoff')
    f = Folded(int(data['size_cold']))
    x = f.cold_data(lam, mu, low, scale2, ((F(1), F(1)),))
    need(f.cold_check(lam, mu, low, x, scale2), f'Einstein cold sign {data["name"]}')
    boxes = hot_einstein(Folded(int(data['size_hot'])), lam, mu, high, scale2, phonon[data['lambda']])
    cl, ch = c_bounds(lam, low, high)
    receipt[data['name']] = {'einstein_q': [str(low), str(high)],
                             'einstein_C': [str(cl), str(ch)], 'boxes': boxes}
    print(f'{data["name"]:>10} lam={data["lambda"]} mu={data["mu"]} R^2={data["R2"]}: '
          f'Einstein onset q in [{float(low):.10g},{float(high):.10g}] C_E={float(cl):.8g} boxes={boxes}',
          flush=True)
    if 'mix' in data:
        mix = data['mix']
        spectrum = spectrum_of(mix)
        q = F(mix['q'])
        need(q > high, 'mixture witness must sit above the Einstein upper endpoint')
        g = Folded(int(mix['size']))
        y = g.cold_data(lam, mu, q, scale2, spectrum)
        need(g.cold_check(lam, mu, q, y, scale2, spectrum), f'mixture cold sign {data["name"]}')
        receipt[data['name']]['mix'] = {'spectrum': [[str(p), str(u)] for p, u in spectrum],
                                        'q': str(q)}
        print(f'{data["name"]:>10} two-line spectrum unstable at q={q} '
              f'= {float(q/high):.1f} x the Einstein upper endpoint', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--mutant', choices=('coulomb', 'spectrum', 'endpoint', 'tail', 'sign'))
    mode.add_argument('--write', action='store_true', help='explicitly regenerate bounds.json')
    args = parser.parse_args()
    data = json.loads((HERE/'fixtures.json').read_text(encoding='utf8'))
    phonon = phonon_hots()
    receipt_path = HERE/'bounds.json'
    if args.mutant:
        case = next(c for c in data['cases'] if c['name'] == 'einstein-counterexample')
        lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
        low, high = map(F, case['einstein'])
        if args.mutant == 'sign':
            # Control: with the physical (repulsive) sign of the rank-one mask term the
            # Einstein hot certificate covers the whole interval above the endpoint.
            boxes = hot_einstein(Folded(int(case['size_hot'])), lam, mu, high, scale2,
                                 phonon[case['lambda']])
            control(boxes > 0, 'the unmutated (repulsive-sign) hot certificate covers the interval')
            # Mutant: reverse the sign of the rank-one mask term (an attraction).  The
            # same certificate must then fail; the sign is the load-bearing part.
            try:
                hot_einstein(Folded(int(case['size_hot'])), lam, -mu, high, scale2,
                             phonon[case['lambda']])
            except ValueError as exc:
                refused(f'the sign-flipped mask term is not certified positive ({exc})')
            need(False, 'sign mutant: the reversed mask sign passed the hot certificate')
        if args.mutant == 'tail':
            j = 2*Folded(64).n
            a = weights(lam, low, j+2, ((F(1), F(1)),))
            actual = (a[j]+a[j+1])**2/(j+1)
            control(actual < far_lump(lam/low, 64, 1), 'the true far tail term is below the bound')
            if not actual < far_lump(lam/low, 64, 1, True):
                refused('with far_lump disabled the exact tail guess exceeds the bound')
            need(False, 'tail mutant: the disabled far tail bound still dominates the exact term')
        f = Folded(int(case['size_cold']))
        x = f.cold_data(lam, mu, low, scale2, ((F(1), F(1)),))
        control(f.cold_check(lam, mu, low, x, scale2), 'the Einstein cold witness keeps its sign')
        if args.mutant == 'coulomb':
            if not f.cold_check(lam, 2*mu, low, x, scale2):
                refused('the cold certificate at q_lo dies when the Coulomb term is doubled')
            need(False, 'coulomb mutant: the doubled Coulomb term still certified instability')
        if args.mutant == 'endpoint':
            if not f.cold_check(lam, mu, high, x, scale2):
                refused('a cold witness is refused at the certified-stable endpoint q_hi')
            need(False, 'endpoint mutant: a cold witness was certified at the stable endpoint')
        if args.mutant == 'spectrum':
            mix = case['mix']
            q = F(mix['q'])
            # (1) The mirrored spectrum (u_low and u_high exchanged) keeps both line
            # weights, so the moment cannot catch it: the ordering guard must.
            mirrored = dict(mix, low_u=mix['high_u'], high_u=mix['low_u'])
            try:
                spectrum_of(mirrored)
            except ValueError as exc:
                need('bad mixture' in str(exc),
                     f'the mirrored spectrum was refused for the wrong reason: {exc}')
            else:
                need(False, 'spectrum mutant: the mirrored spectrum was accepted')
            # (2) Exchanging the line weights (p -> 1-p) keeps the ordering and breaks
            # only the second moment, which the moment guard must catch.
            swapped = dict(mix, high_p=str(1 - F(mix['high_p'])))
            try:
                spectrum_of(swapped)
            except ValueError as exc:
                need('moment' in str(exc),
                     f'a p -> 1-p mixture was refused for the wrong reason: {exc}')
            else:
                need(False, 'a spectrum with the wrong second moment was accepted')
            # (3) The certificates themselves.  The mutant transfers the mixture's verdict
            # to Einstein, i.e. it claims the Einstein line is unstable at the mixture
            # witness q; the control is that the true mixture is cold there.
            spectrum = spectrum_of(mix)
            g = Folded(int(mix['size']))
            y = g.cold_data(lam, mu, q, scale2, spectrum)
            control(g.cold_check(lam, mu, q, y, scale2, spectrum),
                    'the two-line witness keeps its own sign')
            y_ein = g.cold_data(lam, mu, q, scale2, ((F(1), F(1)),))
            if g.cold_check(lam, mu, q, y_ein, scale2):
                need(False, 'spectrum mutant: the Einstein spectrum was certified unstable at '
                            'the mixture witness q, which would refute the counterexample')
            refused(f'the Einstein line is not unstable at the mixture witness q={q}: the '
                    f'two-line verdict does not transfer')
        return
    receipt = {}
    for case in data['cases']:
        run_case(case, phonon, receipt, args.write)
    for anchor in data['anchors']:
        run_case(anchor, phonon, receipt, args.write)
    if args.write:
        receipt_path.write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf8')
        print('regenerated bounds.json')
    else:
        verify_receipt(receipt, json.loads(receipt_path.read_text(encoding='utf8')))
        print('stored bounds.json verified without rewriting')


if __name__ == '__main__':
    main()
