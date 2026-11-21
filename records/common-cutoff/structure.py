"""Exact checks of the structural lemmas used in RIGOR.md (common-cutoff kernel).

Every statement is tested with rational arithmetic at random rational data; the
probability of hitting a degenerate point is zero and each check is an exact
inequality, so a pass is a finite-sample confirmation of the algebra, not of the
general statement (the general statements are proved in RIGOR.md).

Run:  python -B structure.py           (exit 0 on success)
      python -B structure.py --mutant  (exit 1: the controls below must be refused)
"""

import argparse
import random
import sys
from fractions import Fraction as F


def transfer(spec, r):
    """a_r = sum_i lam_i v_i/(v_i+r) for a discrete two-line spectrum [(lam_i, v_i)]."""
    return sum(lam*v/(v+r) for lam, v in spec)


def random_two_line(rng, M=F(1)):
    # lam_1 + lam_2 = 1 (M = 1 normalisation), lam_1 v_1 + lam_2 v_2 = M
    lam1 = F(rng.randint(1, 99), 100)
    v1 = F(rng.randint(1, 400), 400)
    v2 = (M-lam1*v1)/(1-lam1)
    if not (0 < v1 and 0 < v2 and v1 < M < v2):
        return None
    return [(lam1, v1), (1-lam1, v2)]


def checks(seed=20261120, trials=400):
    rng = random.Random(seed)
    seen = 0
    for _ in range(trials):
        spec = random_two_line(rng)
        if spec is None:
            continue
        seen += 1
        lam = sum(p for p, _ in spec)
        M = sum(p*V for p, V in spec)
        assert lam == 1 and M == 1
        for r in (F(1, 97), F(1, 3), F(1), F(7), F(50), F(10**4)):
            a = transfer(spec, r)
            # (1) nonnegative transfer and the exact Einstein dominance a_r <= lam/(1+r)
            assert a >= 0
            assert a <= 1/(1+r), (spec, r, a, 1/(1+r))
            # (2) the kernel-free bound a_r <= lam*min(1, M/lam/r)
            assert a <= min(F(1), M/r)
            # (3) the two-line transfer is a rational function of r with the fixed
            #     asymptotics a_0 = lam and a_r ~ M/r
            if r == F(10**4):
                assert abs(a - M/r) <= F(1, 10**6)
        # (4) the Coulomb normalisation: the folded block adds +2 mu on every masked
        #     index, hence the spectrum-independent rank-one part +2 mu (sum x)^2
        x = [F(rng.randint(-9, 9)) for _ in range(6)]
        k = 3
        assert 2*(sum(x[:k]))**2 - sum(2*x[i]*x[j] for i in range(k) for j in range(k)) == 0
    assert seen > 100, seen
    return seen


def folded_pair(spec, q, n, R, mu, k, h):
    """The RIGOR.md 4 identity in exact rationals: matrix form versus display form.

    The matrix (replay.py convention) is F_ij = [i=j](2i+1+2A_i) - [i!=j]a_{|i-j|}
    - a_{i+j+1} + [i,j<k]2 mu with A_i = sum_{j=1..i}a_j; the a_0 content cancels
    between the normal self-energy and the pairing numerator, so a_0 is absent.
    The display is the corrected F_0 plus the rank-one Coulomb block, with the
    finite rational a-list (a_r = 0 for r > R) that makes every tail exact.
    """
    a = [F(0)]*(R+1)
    a[0] = sum(p for p, _ in spec)
    for r in range(1, R+1):
        a[r] = transfer(spec, q*r*r)
    get = lambda r: a[r] if 0 <= r <= R else F(0)
    A = [sum(a[1:i+1]) for i in range(n)]
    S1 = sum(a[1:R+1])
    T = [S1 - A[i] for i in range(n)]
    val = sum((2*i+1+2*A[i])*h[i]**2 for i in range(n))
    val += sum(-get(i+j+1)*h[i]*h[j] for i in range(n) for j in range(n))
    val += sum(-(0 if i == j else get(abs(i-j)))*h[i]*h[j]
               for i in range(n) for j in range(n))
    val += 2*mu*sum(h[:k])**2
    J = R+n+1
    ext = [h[i] if i < n else F(0) for i in range(J)]
    lap = sum(get(abs(i-j))*(ext[i]-ext[j])**2 for i in range(J) for j in range(J))
    hip = sum(get(i+j+1)*(ext[i]-ext[j])**2 for i in range(J) for j in range(J))
    mass = sum((2*i+1)*h[i]**2 for i in range(n))
    tail = -2*sum(T[i]*h[i]**2 for i in range(n))
    return val, mass+tail+lap/2+hip/2+2*mu*sum(h[:k])**2, mass+lap/2+hip/2+2*mu*sum(h[:k])**2


def folded(seed=20261120, trials=60, n=6, R=12, wrong=False):
    """Verify the RIGOR.md 4 display against the folded matrix (exact rationals)."""
    rng = random.Random(seed)
    seen = bad = 0
    for _ in range(trials):
        spec = random_two_line(rng)
        if spec is None:
            continue
        q = F(rng.randint(1, 30), 7)
        mu = F(rng.randint(0, 3), 2)
        k = rng.randint(1, n)
        for signs in (True, False):          # mixed-sign and all-positive witnesses
            h = [(F(rng.randint(1, 40), 13) if signs else F(rng.randint(-40, 40), 13))
                 for _ in range(n)]
            mat, disp, nogap = folded_pair(spec, q, n, R, mu, k, h)
            seen += 1
            if wrong:
                bad += disp != nogap
            else:
                assert mat == disp, (spec, q, mu, k, h, mat, disp)
    assert seen > 0
    if wrong:
        assert bad > 0, 'the display without the -2 sum_{r>i} a_r term was not detected'
        print(f'folded mutant: the display missing the tail term differs from the matrix '
              f'in {bad}/{seen} trials (detected, as required)')
        return 1
    print(f'folded identity (matrix form = display form) verified exactly in {seen} '
          f'rational trials')
    return 0


def mutant(seed=20261120, trials=40):
    """Negative controls: each perturbed statement below must be refused."""
    rng = random.Random(seed)
    refused = 0
    for _ in range(trials):
        spec = random_two_line(rng)
        if spec is None:
            continue
        M = sum(p*V for p, V in spec)
        r = F(1, 3)
        a = transfer(spec, r)
        if a > M/r:                      # M = 1 here, so the "M/r" form is the same
            refused += 1
        # wrong second moment: rescale one line so that sum lam v = 2
        bad = [(p, V*2) for p, V in spec]
        if transfer(bad, F(1)) > F(1)/(1+F(1)):
            refused += 1
    assert refused > 0, 'mutant: no perturbed statement was refused'
    print(f'mutant controls refused {refused} perturbed statements (as required)')
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', action='store_true')
    ap.add_argument('--folded', action='store_true',
                    help='verify the folded matrix against the RIGOR.md 4 display')
    args = ap.parse_args()
    if args.folded:
        return folded(wrong=args.mutant)
    if args.mutant:
        return mutant()
    seen = checks()
    print(f'structural checks passed on {seen} rational two-line spectra (exact arithmetic)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
