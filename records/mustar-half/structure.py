"""Exact rational checks of the structural lemmas in RIGOR.md (mu*/lambda <= 1/2 study).

Every identity and inequality is checked in exact Fraction arithmetic on random
rational inputs (plus guarded --mutant controls that must fail with exit code 1).

Run:
    python -B structure.py                 # exit 0
    python -B structure.py --mutant        # exit 1 (runs all mutant controls)
    python -B structure.py --mutant f4     # exit 1 (tests F4 diagonal-order failure at lam > 2, mu* = lam/2)
    python -B structure.py --mutant coulomb
    python -B structure.py --mutant norm
"""

import argparse
import random
import sys
from fractions import Fraction as F


def weights(lam, q, count, spec):
    """a_j = lam * sum_m theta_m u_m / (u_m + q * j^2), including a_0 = lam."""
    return [sum(lam * th * u / (u + q * j * j) for th, u in spec) for j in range(count)]


def folded_form(a, h, mu=F(0), k=0):
    """Exact <h, F_p^{(k)} h> for h supported on 0..N-1 using folded matrix entries."""
    n = len(h)
    total = F(0)
    for i in range(n):
        diag = F(2 * i + 1) + 2 * sum(a[1 : i + 1]) - a[2 * i + 1]
        total += diag * h[i] * h[i]
        for m in range(n):
            if m != i:
                total -= (a[abs(i - m)] + a[i + m + 1]) * h[i] * h[m]
    if k > 0:
        s = sum(h[: min(k, n)])
        total += 2 * mu * s * s
    return total


def L_j(h, j):
    """Negative of RIGOR.md Lemma 1 L_j(h): equals -L_j^{RIGOR}(h) (> 0 on nonincreasing h > 0)."""
    n = len(h)
    diff_part = sum(2 * h[i + j] * (h[i] - h[i + j]) for i in range(max(0, n - j)))
    hank_part = sum(h[i] * h[j - 1 - i] for i in range(j) if i < n and j - 1 - i < n)
    return diff_part + hank_part


def L_j_rigor(h, j):
    """Exact RIGOR.md Lemma 1 display (2): 1/2 sum (h_i-h_{j-1-i})^2 + sum (h_i-h_{i+j})^2 - 2 sum_{i<j} h_i^2."""
    n = len(h)
    hi = lambda idx: h[idx] if 0 <= idx < n else F(0)
    hank = F(1, 2) * sum((hi(i) - hi(j - 1 - i)) ** 2 for i in range(j))
    toep = sum((hi(i) - hi(i + j)) ** 2 for i in range(n))
    diag = 2 * sum(hi(i) ** 2 for i in range(j))
    return hank + toep - diag


def random_two_line(rng, u1_max_num=399):
    u1 = F(rng.randint(1, u1_max_num), 400)
    u2 = F(rng.randint(401, 2000), 400)
    th = (1 - u1) / (u2 - u1)
    spec = ((1 - th, u1), (th, u2))
    assert sum(t for t, _ in spec) == 1
    assert sum(t * u for t, u in spec) == 1
    return spec


def diag_tilde(a, mu, n):
    """Modified diagonal D_tilde_{p,i} = (2i+1) + a_0 + 2*sum_{j=1}^i a_j + 2*mu*1_{i=0}."""
    return [F(2 * i + 1) + a[0] + 2 * sum(a[1 : i + 1]) + (2 * mu if i == 0 else F(0)) for i in range(n)]


def verify_all():
    rng = random.Random(20261120)
    for trial in range(40):
        lam = F(rng.randint(1, 40), rng.randint(1, 5))
        q = F(rng.randint(1, 40), rng.randint(1, 10))
        n = 12
        spec = random_two_line(rng)
        a = weights(lam, q, 2 * n + 2, spec)
        aE = weights(lam, q, 2 * n + 2, ((F(1), F(1)),))

        # 1. Closed-form Jensen gap a_j(E) - a_j(p) > 0 for j >= 1
        (_, u1), (_, u2) = spec
        for j in range(1, 2 * n):
            diff = aE[j] - a[j]
            exact_gap = lam * q * j * j * (1 - u1) * (u2 - 1) / ((1 + q * j * j) * (u1 + q * j * j) * (u2 + q * j * j))
            if diff != exact_gap or diff <= 0:
                raise AssertionError(f'Jensen gap failed at trial {trial}, j={j}')

        # 2. Lemma 1 exact finite-support decomposition across full mu* in [0, lam/2]
        h = sorted([F(rng.randint(1, 50), 10) for _ in range(n)], reverse=True)
        mu_full = lam * F(rng.randint(0, 10), 20)  # in [0, lam/2]
        k = rng.randint(0, 4)
        rhs = sum(F(2 * i + 1) * h[i] * h[i] for i in range(n))
        if k > 0:
            rhs += 2 * mu_full * sum(h[:k]) ** 2
        for j in range(1, 2 * n):
            lj = L_j(h, j)
            lj_r = L_j_rigor(h, j)
            if lj_r != -lj:
                raise AssertionError(f'L_j_rigor != -L_j at j={j}: {lj_r} vs {-lj}')
            if lj < 0 or (j == 1 and lj <= 0):
                raise AssertionError(f'L_j positivity failed at j={j}: {lj}')
            rhs += a[j] * lj_r
        lhs = folded_form(a, h, mu=mu_full, k=k)
        if lhs != rhs:
            raise AssertionError(f'Lemma 1 identity mismatch: {lhs} != {rhs}')

        # 3. Cone-preservation identity (A_tilde x)_i - (A_tilde x)_{i+1} > 0
        x = sorted([F(rng.randint(1, 50), 10) for _ in range(n)], reverse=True)
        Ax = [sum((a[abs(i - m)] + a[i + m + 1]) * x[m] for m in range(n)) for i in range(n)]

        def y(idx):
            idx_r = idx if idx >= 0 else -idx - 1
            return x[idx_r] if idx_r < n else F(0)

        for i in range(n - 1):
            lhs_d = Ax[i] - Ax[i + 1]
            rhs_d = sum((a[s] - a[s + 1]) * (y(i - s) - y(i + 1 + s)) for s in range(n + i + 2))
            if lhs_d != rhs_d or lhs_d <= 0:
                raise AssertionError(f'Theorem 4 cone preservation failed at i={i}')

        # 4a. Theorem 4 unconditional range: lam in (0, 2], mu* up to lam/2 (including boundary mu* = lam/2)
        lam_small = F(rng.randint(1, 20), 10)
        mu_small = lam_small * F(rng.randint(0, 10), 20) if trial % 2 == 0 else lam_small / 2
        a_small = weights(lam_small, q, 2 * n + 2, spec)
        D_small = diag_tilde(a_small, mu_small, n)
        if not (0 < D_small[0] <= D_small[1]):
            raise AssertionError(f'Theorem 4 (lam<=2, mu*<=lam/2) failed: {D_small[0]} vs {D_small[1]}')
        for i in range(1, n - 1):
            if not (D_small[i] < D_small[i + 1]):
                raise AssertionError(f'Theorem 4 strict tail order failed at i={i}')

        # 4b. Theorem 4 unconditional mu* <= 1 for general lam in (0, 40], and pointwise mu* <= 1 + a_1(q;p)
        mu_le1 = F(rng.randint(0, 10), 10)
        D_le1 = diag_tilde(a, mu_le1, n)
        if not (0 < D_le1[0] <= D_le1[1]):
            raise AssertionError(f'Theorem 4 (mu*<=1) failed: {D_le1[0]} vs {D_le1[1]}')
        mu_pt = min(lam / 2, 1 + a[1]) if trial % 2 == 0 else (1 + a[1]) * F(rng.randint(0, 10), 10)
        D_pt = diag_tilde(a, mu_pt, n)
        if not (0 < D_pt[0] <= D_pt[1]):
            raise AssertionError(f'Theorem 4 (mu*<=1+a_1) failed: {D_pt[0]} vs {D_pt[1]}')
        for i in range(1, n - 1):
            if not (D_pt[i] < D_pt[i + 1]):
                raise AssertionError(f'Theorem 4 strict tail order failed at i={i}')

        # 5. Theorem 3 large-coupling fixed-R bound: lam >= 4*R^2 + 1 => q_E(lam, 0) > lam - 1 >= 4*R^2
        R2 = F(rng.randint(1, 30), rng.randint(1, 5))
        lam_big = 4 * R2 + 1 + F(rng.randint(0, 10), 5)
        q_test = lam_big - 1
        a_big = weights(lam_big, q_test, 4, ((F(1), F(1)),))
        F00 = F(1) - a_big[1]
        F01 = -(a_big[1] + a_big[2])
        F11 = F(3) + 2 * a_big[1] - a_big[3]
        eps = -F01 / (F11 + 1)
        qform_v = F00 + 2 * eps * F01 + eps * eps * F11
        if F00 != 0 or qform_v >= 0:
            raise AssertionError(f'Theorem 3 e_0+eps*e_1 test failed: F00={F00}, qform={qform_v}')

        # 6. Theorem 5 asymptotic row-margin bound for F_p^{(0)}(q) at q >= 4*lam (using pi^2/3 < 7/2)
        q_asymp = 4 * lam + F(rng.randint(0, 20), 5)
        a_as = weights(lam, q_asymp, 2 * n + 2, spec)
        for i in range(n):
            diag_0 = F(2 * i + 1) + 2 * sum(a_as[1 : i + 1]) - a_as[2 * i + 1]
            off_0 = sum(a_as[abs(i - m)] + a_as[i + m + 1] for m in range(n) if m != i)
            margin_finite = diag_0 - off_0
            lower_bound = F(2 * i + 1) - F(7, 2) * lam / q_asymp
            if margin_finite < lower_bound or lower_bound <= 0:
                raise AssertionError(f'Theorem 5 row margin bound failed: {margin_finite} < {lower_bound}')

    # 4c. Explicit F4 refutation witness outside mu* <= 1 + a_1: D_tilde_1 < D_tilde_0 at mu* = lam/2
    u1_r, u2_r = F(1, 100), F(100)
    th_r = (1 - u1_r) / (u2_r - u1_r)
    for lam_ref, q_ref, spec_ref in [
        (F(20), F(186444, 100000), ((F(1), F(1)),)),
        (F(50), F(272444, 100000), ((F(1), F(1)),)),
        (F(5), F(1), ((1 - th_r, u1_r), (th_r, u2_r))),
    ]:
        a_ref = weights(lam_ref, q_ref, 4, spec_ref)
        D_ref = diag_tilde(a_ref, lam_ref / 2, 2)
        if not (D_ref[1] < D_ref[0]):
            raise AssertionError(f'F4 refutation witness unexpectedly preserved D_0 <= D_1 at lam={lam_ref}')
    return True


def mutant_coulomb():
    """Mutant: omit 2*mu*s^2 from Lemma 1 identity; must be refused."""
    rng = random.Random(20261120)
    n = 12
    lam = F(10)
    q = F(3, 2)
    spec = random_two_line(rng)
    a = weights(lam, q, 2 * n + 2, spec)
    h = sorted([F(rng.randint(1, 50), 10) for _ in range(n)], reverse=True)
    mu = F(3)
    k = 2
    lhs = folded_form(a, h, mu=mu, k=k)
    rhs_bad = sum(F(2 * i + 1) * h[i] * h[i] for i in range(n)) + sum(a[j] * L_j_rigor(h, j) for j in range(1, 2 * n))
    return lhs == rhs_bad


def mutant_f4():
    """Mutant (F4): test the false unrestricted claim D_0 <= D_1 for mu* = lam/2 across lam > 2."""
    rng = random.Random(20261121)
    n = 6
    for _ in range(40):
        lam = F(rng.randint(4, 40))
        q = F(rng.randint(1, 5), 2)
        u1 = F(rng.randint(1, 20), 400)
        u2 = F(rng.randint(800, 4000), 400)
        th = (1 - u1) / (u2 - u1)
        spec = ((1 - th, u1), (th, u2))
        a = weights(lam, q, 2 * n + 2, spec)
        D = diag_tilde(a, lam / 2, n)
        if D[1] < D[0]:
            return False
    return True
def mutant_norm():
    """Mutant: rescale u -> 2*u (violating Moment-1) and expect a_j(E) > a_j(p); must fail."""
    lam = F(4)
    q = F(1)
    spec = ((F(1, 2), F(9, 10)), (F(1, 2), F(11, 10)))
    aE = weights(lam, q, 10, ((F(1), F(1)),))
    a_ok = weights(lam, q, 10, spec)
    assert all(aE[j] > a_ok[j] for j in range(1, 10))
    bad_spec = tuple((th, F(2) * u) for th, u in spec)
    a_bad = weights(lam, q, 10, bad_spec)
    for j in range(1, 10):
        if aE[j] <= a_bad[j]:
            return False
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        '--mutant',
        nargs='?',
        const='all',
        choices=['all', 'coulomb', 'f4', 'norm'],
        help='run guarded mutant control (must exit 1)',
    )
    args = ap.parse_args()
    if args.mutant is not None:
        controls = {
            'coulomb': ('dropped 2*mu*s^2 term', mutant_coulomb),
            'f4': ('unrestricted F4 D_0 <= D_1 at lam > 2, mu* = lam/2', mutant_f4),
            'norm': ('rescaled u -> 2*u violating Moment-1', mutant_norm),
        }
        selected = list(controls.keys()) if args.mutant == 'all' else [args.mutant]
        refused = []
        for name in selected:
            desc, fn = controls[name]
            if fn():
                print(f'ERROR: mutant {name} ({desc}) passed unexpectedly')
                return 0
            refused.append(f'{name} ({desc})')
        print('REFUSED: mutant structural checks failed as required: ' + '; '.join(refused))
        return 1
    verify_all()
    print('structural checks passed on 40 random rational trials + F4 refutation witnesses (exact Fraction arithmetic)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
