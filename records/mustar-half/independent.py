"""Second, independent verification of the MUSTAR-HALF common-cutoff certificates.

Cold side (exact rationals on the UNFOLDED full Matsubara line, n in {-NC,...,NC-1}):
    D_n  = |2n+1| + 2 * sum_{j=1}^{i(n)} a_j ,   i(n) = max(n, -n-1)
    K_nm = a_{|n-m|} - mu* c_n c_m ,             c_n = 1_{(2n+1)^2 q < 4 R^2}, a_0 cancelled
    form = sum_n f_n^2 D_n - sum_{n,m} f_n f_m K_nm
         = sum_n f_n^2 D_n - sum_{d != 0} corr_d a_{|d|} + mu* (sum_{n in mask} f_n)^2
evaluated in exact Fraction arithmetic without using the folded identity of RIGOR.md.

Hot side (signed interval enclosure, exact integers, PSD-dominated penalties):
    the head block 0..m-1 (m = max(NB//2, 2k+1) >= the mask width k) is enclosed
    ENTRYWISE by exact integers of scale SC on every window [lo,hi) of constant mask k,

        lower <= SC*F_ij(q) <= upper      for EVERY q in [lo,hi),

    with the off-diagonal magnitude bracketed by its values at lo (largest) and at hi
    (smallest), and the diagonal bounded BELOW one-sidedly (A_i at hi, a_{2i+1} at lo).
    The enclosure centre (lower+upper)//2 and radius max(upper-centre, centre-lower) >= 0
    then satisfy |SC*F_ij(q) - centre_ij| <= radius_ij, and the whole deviation matrix is
    dominated for EVERY real vector x (mixed-sign ones included, mu* > 0 allowed) by two
    diagonal, PSD-dominated shifts: the weighted-Gershgorin shift diag(rho) of the finite
    radius (head_radius) and the Schur shift diag(theta) of the infinite tail j >= m
    (tail_penalty).  The tail shift uses the PER-ROW gap g_j of the infinite tail, not a
    single worst-case scalar gap: g_j grows with j (tail_gaps), and the boundary row
    j = m, which carries the (i,j) = (m-1,m) coupling a_1 = O(1), keeps a gap of size
    2m + O(1) instead of being penalised with a factor 1/m that would miss it by 19.85x
    (REVIEW.md F2).  No entrywise (Z-matrix) statement about off-diagonal signs is made
    anywhere, and the tail is the INFINITE tail, never a finite block: RIGOR.md 5 carries
    the proof, FIX-INDEP.md the derivation of both shifts.

    pi uses Hutton's identity pi/4 = atan(1/2) + atan(1/3) with 90 terms, arithmetically
    independent of replay.py's Machin formula.

Run:
    python -B independent.py
    python -B independent.py --mutant {endpoint,coulomb,spectrum,receipt,entrywise,v1pen,rsign,overflow}
    python -B independent.py --adversarial
    python -B independent.py --selfcheck
"""

import argparse
import json
import sys
import time
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
SC = 1 << 22          # head matrix scale (integer form entries)
GRAM = (1 << 24, 1 << 25, 1 << 26)   # Gram factor scales tried by positive()
NB = 400              # head block: modes 0..NB//2-1, and the infinite tail starts there
NCOL = 240            # tail columns m..m+NCOL-1 summed exactly, closed form beyond
NC = 240              # cold half band: modes n in [-NC, NC-1]
RAD = 22              # witness rounding scale exponent (integers of size ~2**RAD)
NFOLD = 480           # fold count of the adversarial probes' exact folded witnesses


def need(ok, why):
    if not ok:
        raise ValueError(why)


def control(ok, why):
    if not ok:
        print(f'CONTROL FAILED (mutant invalid): {why}')
        raise SystemExit(2)


def refused(why):
    print(f'REFUSED: {why}')
    raise SystemExit(1)


def ceil_(x):
    return -((-x.numerator) // x.denominator)


def flr_(x):
    return x.numerator // x.denominator


def weights(lam, q, count, spectrum):
    """a[0] = 0 (cancelled a_0), a[j] = lam * sum_{th, u} th * u / (u + q * j^2)."""
    a = [F(0)]
    for j in range(1, count):
        a.append(sum((lam * th * u / (u + q * j * j) for th, u in spectrum), F(0)))
    need(all(x >= 0 for x in a), 'negative weight')
    need(a[1] <= lam, 'a_1 exceeds lambda')
    return a


def cutoff(q, scale2):
    """k = #{i >= 0 : (2i+1)^2 * q < 4 * scale2}, from integer comparisons only."""
    pn, pd = q.numerator, q.denominator
    sn, sd = scale2.numerator, scale2.denominator
    top = 4 * sn * pd
    run = pn * sd
    if top <= run:
        return 0
    dmax = isqrt((top - 1) // run)
    dmax -= 1 - dmax % 2
    need(dmax >= 1, 'empty mask')
    return (dmax + 1) // 2


def in_mask(d, q, scale2):
    return (2 * d + 1) ** 2 * q < 4 * scale2


def spectrum_of(mix):
    p = F(mix['high_p'])
    low, high = F(mix['low_u']), F(mix['high_u'])
    need(0 < p < 1 and 0 < low < 1 < high, f'bad mixture ordering {mix}')
    need((1 - p) * low + p * high == 1, f'mixture second moment is not one: {mix}')
    return ((1 - p, low), (p, high))


def a1_pin_check(cases):
    """Verify a_1 at each mixture witness against direct rational formula."""
    count = 0
    for case in cases:
        lam = F(case['lambda'])
        mix = case['mix']
        q = F(mix['q'])
        p, u1, u2 = F(mix['high_p']), F(mix['low_u']), F(mix['high_u'])
        spec = spectrum_of(mix)
        got = weights(lam, q, 3, spec)[1]
        expect = lam * ((1 - p) * u1 / (u1 + q) + p * u2 / (u2 + q))
        need(got == expect and (1 - p) * u1 + p * u2 == 1, f'{case["name"]}: a_1 pin mismatch')
        count += 1
    return count


def tail_gaps(lam, lo, hi, spec, m, ncol=NCOL):
    """Integer per-row lower bounds g_j (scale SC) on the Gershgorin gaps of the tail j >= m.

    Row j >= m of the folded matrix (j >= m > k, so it carries no Coulomb block) has
    diagonal 2j+1 + 2A_j - a_{2j+1} and off-diagonal entries -(a_|j-l| + a_{j+l+1}), so for
    S_T = sum_{r>=T} a_r its absolute off-diagonal row sum is

        rowsum_j = [sum_{l=m}^{j-1} a_{j-l} + sum_{l>j} a_{l-j}] + sum_{l>=m} a_{j+l+1}
                 = [A_{j-m} + S_1] + S_{j+m+1}

    and the gap gap_j = diag_j - rowsum_j (RIGOR.md 5) satisfies, for EVERY q in [lo,hi],

        gap_j = 2j+1 + 2A_j - a_{2j+1} - A_{j-m} - S_1 - S_{j+m+1}
              >= 2j+1 + 2A_j - a_{2j+1} - A_{j-m} - S_1(lo) - lam/(lo*(j+m)) ,
        2A_j(q) >= 2A_j(hi),  A_{j-m}(q) <= A_{j-m}(lo),  a_{2j+1}(q) <= a_{2j+1}(lo),
        S_1(q) <= S_1(lo) = sum_{r>=1} a_r(lo) <= (lam/lo) sum_{r>=1} r^-2 < (5/3) lam/lo,
        S_{j+m+1}(q) <= (lam/lo) sum_{r>j+m} r^-2 <= lam/(lo*(j+m)) ,

    because a_r(q) and A_r(q) decrease in q.  Each A_r is accumulated as a sum of
    outward-rounded integers of scale SC (flr for the positive 2A_j term, ceil for every
    subtracted term), so each g_j is a verified LOWER bound and g_j grows with j: the
    boundary row j = m keeps g_m = 2m + O(1), which the O(1/(mg)) scalar penalty of
    REVIEW.md F2 misses at the |j-i| = 1 coupling a_1 of the row (m-1, m).  Because
    a_r <= lam/(q r^2) for every mixture (u/(u+q r^2) <= 1/(q r^2) and the second moment of
    the weights is one), both closed forms hold for all of the package's spectra, and the
    bound is evaluated only through weights(), so it is uniform over the window.
    """
    need(0 < lo <= hi and m >= 1 and ncol >= 1, 'bad tail gaps window')
    top = 2 * (m + ncol) + 2
    a_lo = weights(lam, lo, top, spec)
    a_hi = weights(lam, hi, top, spec)
    dn = [0] * top                     # dn[r] <= SC * A_r(hi), A_r = sum_{t<=r} a_t
    acc = 0
    for r in range(1, top):
        acc += flr_(SC * a_hi[r])
        dn[r] = acc
    up = [0] * top                     # up[r] >= SC * A_r(lo)
    acc = 0
    for r in range(1, top):
        acc += ceil_(SC * a_lo[r])
        up[r] = acc
    s1 = ceil_(SC * lam * F(5, 3) / lo)
    j = np.arange(m, m + ncol)
    g = (SC * (2 * j + 1) + 2 * np.array([dn[t] for t in j], dtype=np.int64)
         - np.array([up[t - m] for t in j], dtype=np.int64)
         - np.array([ceil_(SC * a_lo[2 * t + 1]) for t in j], dtype=np.int64)
         - np.array([ceil_(SC * lam / (lo * (t + m))) for t in j], dtype=np.int64) - s1)
    need(bool(np.all(g > 0)),
         f'tail Gershgorin gap is not positive (min {int(g.min()) / SC:.6g} at m={m}, '
         f'lo={float(lo):.9g})')
    return g


def tail_penalty(lam, lo, spec, m, g, ncol=NCOL):
    """Diagonal Schur shift theta_i of the head/tail coupling, with the per-row gaps g_j.

    Write the folded form as x^T A x + 2 x^T B y + y^T F_QQ y on (head x, tail y).  The tail
    block is a Z-matrix, so 2|x_i||y_j| >= 2 x_i y_j and the per-row gaps give
    y^T F_QQ y >= sum_j g_j y_j^2 for EVERY y (mixed-sign included), hence
    2 x^T B y >= -sum_j (1/g_j)(sum_i b_ij x_i)^2 and, with col_l = sum_i b_il h_i,

        sum_j (1/g_j)(sum_i b_ij x_i)^2 <= sum_j (1/g_j) col_j sum_i b_ij x_i^2/h_i
                                        = sum_i x_i^2 theta_i ,  theta_i = (1/h_i) col_j/g_j ,
    by Cauchy-Schwarz with the free weights h > 0.  This is valid for all real x and keeps
    the boundary rows (b_{i,m} = a_{m-i} + ..., i.e. the a_1 coupling) at their true weight.
    Columns l >= m+NCOL are closed by b_il, col_l <= 2 lam/(lo t^2) and t = l-m+1 > NCOL:
    they add at most SC (2 lam/lo)^2 sum_j h_j / (3 NCOL^3 g_min) per head row.  All
    arithmetic is exact int64 with an explicit power-of-two column downscale c_j >= col_j/2^k
    (guarded, so the downscale can only make theta LARGER) and directed rounding up.
    """
    L = m + ncol - 1
    up = np.array([ceil_(SC * x) for x in weights(lam, lo, 2 * L + 2, spec)], dtype=np.int64)
    li = np.arange(m, L + 1)
    i = np.arange(m)[:, None]
    be = up[np.abs(i - li)] + up[i + li + 1]          # SC * b_il, rounded up, >= 0
    h = np.array([(1 << 22) // (t + 1) for t in range(m)], dtype=np.int64)
    need(int(be.max()) > 0 and int(be.min()) >= 0, 'empty head/tail coupling')
    need(int(be.max()) * int(h.sum()) < 2 ** 62, 'tail coupling column sums overflow int64')
    col = h @ be                                      # col_l >= (SC) sum_i b_il h_i
    need(int(col.min()) >= 0, 'tail column sums must be nonnegative')
    k = np.maximum(0, np.array([int(c).bit_length() for c in col], dtype=np.int64) - 24)
    c = (col + (np.ones_like(k) << k) - 1) >> k       # ceil(col / 2^k) >= col / 2^k
    need(int(be.max()) * int(c.max()) < 2 ** 62, 'tail penalty numerator overflow')
    need(int(g.min()) > 0, 'tail gaps must be positive')
    # far columns l >= m+NCOL are closed with the single denominator g.min(); that needs
    # gap_j -> g_min/SC, i.e. gap_j - gap_{j-1} = 2 + 2 a_j + a_{j+m} - a_{j-m} >= 2 -
    # a_NCOL(lo) >= 0, which holds whenever a_NCOL(lam, lo) <= lam/(lo NCOL^2) <= 2.
    need(lam <= 2 * lo * ncol * ncol,
         'far-tail closure: a_NCOL(lo) may exceed 2, so gaps are not monotone')
    num = be * c
    term = -(-num // g)                               # ceil(num/g) >= num/g, exact int64
    need(int(term.max()) < 2 ** 62 >> int(k.max()), 'tail penalty column shift overflow')
    shift = term << k                                 # >= 2^k * num/g >= SC^2 b col/g
    need(int(shift.max()) * ncol < 2 ** 62, 'tail penalty row sum overflow')
    per = shift.sum(axis=1)
    far = ceil_(SC * SC * (2 * lam / lo) ** 2 * int(h.sum()) / (3 * ncol ** 3 * int(g.min())))
    need(0 <= far < 2 ** 62, 'far-tail penalty overflow')
    per = per + far
    need(int(per.max()) < 2 ** 62, 'tail penalty overflow')
    return -(-per // h)                                # ceil(per/h_i) >= theta_i


def head_radius(radius, guard=True):
    """Weighted row sums rho_i = ceil((1/h_i) sum_j R_ij h_j) of the off-diagonal radius.

    For any real x, sum_{i!=j} R_ij |x_i x_j| = sum_{i,j} R~_ij x~_i x~_j with x~_i =
    h_i |x_i| and R~_ij = R_ij h_j/h_i (symmetric because R is), and that is at most
    sum_i rho_i x_i^2.  So diag(rho) dominates the whole off-diagonal deviation for EVERY
    vector, mixed-sign ones included; h > 0 is a free weight (h_i = 2^22/(i+1) here).
    guard=False is the REVIEW.md F9 regression path (mutant mode only): it drops the int64
    overflow guard, which makes the returned row sums wrap and stop dominating the radius.
    """
    need(radius.dtype == np.int64 and bool(np.all(radius >= 0)), 'radius must be int64 >= 0')
    h = np.array([(1 << 22) // (i + 1) for i in range(radius.shape[0])], dtype=np.int64)
    if guard:
        need(int(np.abs(radius).max()) * int(h.sum()) < 2 ** 62,
             'radius row sums overflow int64')
    rows = np.abs(radius) @ h
    if guard:
        need(int(rows.max()) >= 0, 'radius row sums must be nonnegative')
    return -(-rows // h)


def hot_enclosure(lam, mu, lo, hi, scale2, spec, mbase=None):
    """Integer centre+radius enclosure of SC*F on the head block (RIGOR.md 5, item 1).

    Head modes 0..m-1 with m = max(NB//2 (or mbase), 2k+1) >= the mask width k, k =
    cutoff(lo), the window [lo,hi) carrying that single mask.  Returns
    (k, m, lower, upper, center, radius): off-diagonal entries -(a_|i-j| + a_{i+j+1}) are
    bracketed by the exact integers
    lower = -(ceil(SC a(lo)) + ceil(SC a(lo)))   (value at lo: the larger magnitude),
    upper = -(floor(SC a(hi)) + floor(SC a(hi))) (value at hi: the smaller magnitude),
    so lower <= SC*F_ij(q) <= upper for EVERY q in [lo, hi); the diagonal
    2i+1 + 2A_i - a_{2i+1} + 2 mu [i<k] is bounded BELOW (one-sidedly) by its value with
    A_i at hi and a_{2i+1} at lo, valid because A_i and a_{2i+1} DECREASE in q.
    center = (lower+upper)//2 and radius = max(upper-center, center-lower) >= 0 cover BOTH
    ends (odd brackets included), hence |SC*F_ij(q) - center_ij| <= radius_ij.
    """
    need(0 < lo < hi, 'empty hot window')
    k = cutoff(lo, scale2)
    m = max(NB // 2 if mbase is None else mbase, 2 * k + 1)
    a_lo = weights(lam, lo, 2 * m + 1, spec)
    a_hi = weights(lam, hi, 2 * m + 1, spec)
    up = np.array([ceil_(SC * x) for x in a_lo], dtype=np.int64)
    dn = np.array([flr_(SC * x) for x in a_hi], dtype=np.int64)
    idx = np.arange(m)
    diff = np.abs(idx[:, None] - idx)
    hank = idx[:, None] + idx + 1
    upper = -(dn[diff] + dn[hank])
    lower = -(up[diff] + up[hank])
    need(bool(np.all(lower <= upper)), 'hot window endpoint brackets are out of order')
    center = (lower + upper) // 2
    radius = np.maximum(upper - center, center - lower)
    radius[np.diag_indices(m)] = 0
    need(bool(np.all(radius >= 0)), 'hot radius is negative')
    # flr is superadditive downwards, so summing the floored per-term integers keeps a valid
    # LOWER bound on SC*A_i(hi) while staying in exact int64 (no rational accumulation).
    need(2 * m * int(dn[1:m].max()) < 2 ** 61, 'diagonal cumulative sum overflows int64')
    cum = np.concatenate((np.zeros(1, dtype=np.int64), np.cumsum(dn[1:m])))
    for t in {1, m // 2, m - 1}:                      # spot-check the superadditivity claim
        need(int(cum[t]) <= flr_(SC * sum(a_hi[1:t + 1])),
             'cumulative diagonal sum is not a lower bound')
    center[np.diag_indices(m)] = SC * (2 * idx + 1) + 2 * cum - up[2 * idx + 1]
    if k:
        center[:k, :k] += flr_(SC * 2 * mu)
    return k, m, lower, upper, center, radius


def hot_head(lam, mu, lo, hi, scale2, spec, mbase=None):
    """(A, m): certified integer matrix whose positivity implies the folded form's on [lo,hi).

    A = center - diag(rho) - diag(theta) <= folded form (as quadratic forms) for all real
    x: first the off-diagonal enclosure radius (head_radius), then the Schur complement of
    the INFINITE tail, which is >= sum_j g_j y_j^2 with the per-row tail gaps g_j of
    tail_gaps, so 2 x^T B y >= -sum_j (1/g_j)||B^T x||_j^2 >= -sum_i theta_i x_i^2.  Both
    steps are PSD-dominated, so positivity of A certifies the folded form for every vector,
    mixed-sign included.  No off-diagonal sign assumption is used anywhere (REVIEW.md F1),
    and the boundary row j = m is weighted by its own gap 2m+O(1) (REVIEW.md F2).
    """
    k, m, _, _, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, spec, mbase)
    need(k == cutoff(lo, scale2), 'hot enclosure mask does not match the window')
    g = tail_gaps(lam, lo, hi, spec, m)
    rho = head_radius(radius)
    theta = tail_penalty(lam, lo, spec, m, g)
    need(int(np.abs(rho).max()) < 2 ** 33 and int(np.abs(theta).max()) < 2 ** 33,
         'head/tail shifts too large for exact int64 assembly')
    center[np.diag_indices(m)] -= rho + theta
    need(int(np.abs(center).max()) < 2 ** 33, 'block too large for the residual product')
    return center, m


def positive(A):
    """Margin of a certified A > 0, or None: exact integer arithmetic, fail closed.

    A float eigenvalue estimate proposes a shift and a float Cholesky a triangular factor;
    the factor is re-rounded to int64 at a power-of-two scale G and the exact integer
    residual R = A*(G**2//SC) - Lh @ Lh.T must be strictly diagonally dominant with
    positive diagonal.  Gershgorin then gives the exact bound
        lambda_min(A) >= min_i (R_ii - sum_{j != i} |R_ij|) / factor
    which is the returned margin (in SC units, so A > 0 iff a margin is returned).
    Exactness of every int64 product is GUARDED, never assumed: |A|*(G**2//SC) < 2^61 keeps
    A*factor exact, |Lh| < 2^31 and every row norm < 2^60 (summed in float64, where the
    relative error is <= n*2^-53 << 1e-9 and the test is the conservative one) keep each
    entry of Lh @ Lh.T and each Cauchy-Schwarz product exact, and |R| < 2^61/n keeps the row
    sums |R|.sum(axis=1) and 2*R.diagonal() exact (REVIEW.md F9).  A failed guard skips the
    candidate: nothing is clamped or silently wrapped, floats only propose.
    """
    need(A.dtype == np.int64, 'positive() needs an exact int64 matrix')
    need(A.ndim == 2 and A.shape[0] == A.shape[1], 'positive() needs a square matrix')
    need(bool(np.array_equal(A, A.T)), 'positive() needs an EXACT symmetric matrix')
    n = A.shape[0]
    M = A.astype(np.float64) / SC
    M = 0.5 * (M + M.T)
    amax = float(np.max(np.abs(A)))
    lam = float(np.linalg.eigvalsh(M)[0])
    if not np.isfinite(lam):
        return None
    if lam <= 0.0:
        # Sound early rejection: with a nonpositive float estimate the box is left to
        # bisection instead of burning the exact Gram attempts.  Never an acceptance.
        return None
    shifts = [lam * c for c in (0.5, 0.9, 0.25, 0.1, 0.02)] + [0.0]
    for G in GRAM:
        factor = G * G // SC
        if amax * factor >= 2 ** 61:
            continue
        for sh in shifts:
            if not (np.isfinite(sh) and abs(sh) < 1e18):
                continue
            try:
                Lf = np.linalg.cholesky(M - sh * np.eye(n))
            except np.linalg.LinAlgError:
                continue
            for _ in range(4):
                Lh = np.rint(Lf * G)
                if not bool(np.all(np.isfinite(Lh))):
                    break  # never cast NaN/inf to int64: fail closed
                if float(np.max(np.abs(Lh))) >= 2 ** 31:
                    break
                if float(np.max((Lh.astype(np.float64) ** 2).sum(axis=1))) * (1 + 1e-9) >= 2 ** 60:
                    break
                Lh = Lh.astype(np.int64)
                res = A * factor - Lh @ Lh.T
                if int(np.abs(res).max()) >= 2 ** 61 // n:
                    break  # row sums could overflow int64: fail closed, never clamp
                gap = 2 * res.diagonal() - np.abs(res).sum(axis=1)
                if bool(np.all(gap > 0)):
                    return float(gap.min()) / factor
                dM = np.linalg.solve(np.tril(Lf), (0.5 * res / factor).T).T
                Lf = Lf + dM
    return None


def cover(test, lo, hi, k, depth=0):
    if test(lo, hi, k):
        return 1
    need(depth < 22, f'hot interval cannot be certified: [{float(lo):.12g}, {float(hi):.12g})')
    mid = (lo + hi) / 2
    return cover(test, lo, mid, k, depth + 1) + cover(test, mid, hi, k, depth + 1)


def certified(test, lo, hi, k, budget, depth=0):
    """Bounded cover for the adversarial probes: True only on a complete cover.

    It returns False as soon as the box budget or the depth limit is exhausted, so an
    incomplete search can never be read as a certificate; a box through a point where the
    folded form is negative is refused at any budget.
    """
    budget[0] -= 1
    if budget[0] < 0 or depth >= 22:
        return False
    if test(lo, hi, k):
        return True
    mid = (lo + hi) / 2
    return (certified(test, lo, mid, k, budget, depth + 1)
            and certified(test, mid, hi, k, budget, depth + 1))


def windows(lo, hi, scale2):
    """Partition [lo, hi) at the mask jumps; each window carries a constant mask."""
    while lo < hi:
        k = cutoff(lo, scale2)
        right = hi if k == 0 else min(hi, 4 * scale2 / (2 * k - 1) ** 2)
        need(right > lo, f'empty window at {float(lo):.12g}')
        yield lo, right, k
        lo = right


def cold_value(lam, mu, q, scale2, spec, n=NC):
    """Exact rational value of the unfolded full-line quadratic form on a rounded integer witness."""
    a = weights(lam, q, 2 * n + 1, spec)
    idx = np.arange(-n, n)
    i = np.maximum(idx, -idx - 1)
    cum = [F(0)]
    for m in range(1, n):
        cum.append(cum[-1] + a[m])
    mask = np.array([1.0 if in_mask(int(d), q, scale2) else 0.0 for d in idx])
    ad = np.array([float(x) for x in a])
    K = ad[np.abs(idx[:, None] - idx)].astype(float)
    np.fill_diagonal(K, 0.0)
    K = K - float(mu) * np.outer(mask, mask)
    K = 0.5 * (K + K.T)
    Dg = np.diag(np.array([abs(2 * int(d) + 1) + 2 * float(cum[i[t]]) for t, d in enumerate(idx)]))
    ray, vec = eigh(K, Dg, subset_by_index=(2 * n - 1, 2 * n - 1))
    x = vec[:, 0]
    xi = np.rint(x / float(np.max(np.abs(x))) * (2**RAD)).astype(np.int64)
    need(int(np.count_nonzero(xi)) > 1, f'{lam} {q}: degenerate witness')
    diag = [
        F(int(xi[t]) ** 2) * (abs(2 * int(idx[t]) + 1) + 2 * cum[i[t]])
        for t in range(2 * n)
    ]
    corr = np.convolve(xi, xi[::-1])
    pair = sum(
        F(int(corr[2 * n - 1 + d])) * a[abs(d)] for d in range(-(2 * n - 1), 2 * n)
    )
    block = int(xi[mask > 0].sum())
    val = sum(diag) - pair + mu * block * block
    return val, float(ray[0])


def pi_bounds():
    """Hutton's formula pi/4 = atan(1/2) + atan(1/3), 90 terms."""
    def atan(x):
        lower = sum((-1) ** j * x ** (2 * j + 1) / (2 * j + 1) for j in range(90))
        return lower, lower + x**181 / 181

    a, b = atan(F(1, 2))
    c, d = atan(F(1, 3))
    return 4 * (a + c), 4 * (b + d)


def c_bounds(lam, left, right):
    pl, ph = pi_bounds()
    digits = 10**30

    def floor_sqrt(q, pi):
        s = digits**2 * q / (4 * lam * pi * pi)
        return isqrt(s.numerator // s.denominator)

    return F(floor_sqrt(left, ph), digits), F(1 + floor_sqrt(right, pl), digits)


def hot_claim(lam, mu, lo, hi, scale2, spec):
    """Bounded cover of [lo, hi) by certified boxes; returns (boxes, m_max, min_margin).

    Raises ValueError (REFUSED) if the depth budget is exhausted on a window, which is the
    only way the hot claim can fail: every accepted box carries an exact certificate.
    """
    stat = {'tries': 0, 'm': 0, 'margin': float('inf')}

    def test(left, right, _k):
        A, m = hot_head(lam, mu, left, right, scale2, spec)
        mar = positive(A)
        stat['tries'] += 1
        if mar is None:
            return False
        stat['m'] = max(stat['m'], m)
        stat['margin'] = min(stat['margin'], mar)
        return True

    boxes = sum(cover(test, l, r, k) for l, r, k in windows(lo, hi, scale2))
    return boxes, stat['tries'], stat['m'], stat['margin']


def run_case(data, receipt, table):
    t0 = time.perf_counter()
    row = {'name': data['name'], 'kind': 'counterexample' if 'mix' in data else 'anchor',
           'status': 'CERTIFIED', 'reason': '', 'boxes': 0, 'tries': 0, 'm': 0,
           'margin': float('nan'), 'seconds': 0.0}
    try:
        lam, mu, scale2 = F(data['lambda']), F(data['mu']), F(data['R2'])
        low, high = map(F, data['einstein'])
        handoff = 4 * lam
        need(0 < low < high < handoff, f'{data["name"]}: bad bracket')
        spec = ((F(1), F(1)),)

        val, ray = cold_value(lam, mu, low, scale2, spec)
        need(val < 0, f'Einstein cold sign {data["name"]}: form value {float(val):.6g} >= 0')
        print(
            f'{data["name"]:>22} cold Einstein: exact unfolded form {float(val):.4g} < 0 '
            f'(ray {ray:.6g} > 1)', flush=True)

        boxes, tries, m, margin = hot_claim(lam, mu, high, handoff, scale2, spec)
        row.update(boxes=boxes, tries=tries, m=m, margin=margin)
        print(
            f'{data["name"]:>22} hot Einstein positive on [{float(high):.6g}, '
            f'{float(handoff):.6g}) in {boxes} boxes ({tries - boxes} bisections, head '
            f'm={m}, min margin {margin:.6g})', flush=True)

        cl, ch = c_bounds(lam, low, high)
        receipt[data['name']] = {
            'einstein_q': [str(low), str(high)],
            'einstein_C': [str(cl), str(ch)],
            'handoff_q': str(handoff),
            'boxes': boxes,
        }
        if 'mix' in data:
            mix = data['mix']
            good = spectrum_of(mix)
            q = F(mix['q'])
            need(high < q < handoff, f'{data["name"]}: mixture q not in (high, handoff)')
            val_m, ray_m = cold_value(lam, mu, q, scale2, good, n=int(mix['size']))
            need(val_m < 0, f'mixture cold sign {data["name"]}: form {float(val_m):.6g} >= 0')
            receipt[data['name']]['mix'] = {
                'spectrum': [[str(p), str(u)] for p, u in good],
                'q': str(q),
            }
            v_ein, ray_ein = cold_value(lam, mu, q, scale2, spec, n=int(mix['size']))
            need(v_ein >= 0, f'{data["name"]}: Einstein negative on own ray at mixture q={q}')
            print(
                f'{data["name"]:>22} mixture unstable at q={q} (form {float(val_m):.4g} < 0, '
                f'ray {ray_m:.6g} > 1) while Einstein ray <= 1 ({ray_ein:.6g})', flush=True)
    except ValueError as exc:
        row['status'], row['reason'] = 'REFUSED', str(exc)
        print(f'{data["name"]:>22} REFUSED: {exc}', flush=True)
    row['seconds'] = time.perf_counter() - t0
    table.append(row)
    return row['status'] == 'CERTIFIED'


def print_table(table):
    print('\ncertify table (margin = exact Gershgorin lower bound on lambda_min of the '
          'certified head matrix, in SC units = 2**22 x folded-form units):')
    print(f'{"instance":>22} {"kind":>14} {"status":>9} {"boxes":>6} {"tries":>6} '
          f'{"head m":>6} {"min margin":>12} {"sec":>7}')
    for row in table:
        print(f'{row["name"]:>22} {row["kind"]:>14} {row["status"]:>9} {row["boxes"]:>6} '
              f'{row["tries"]:>6} {row["m"]:>6} {row["margin"]:>12.6g} {row["seconds"]:>7.2f}')


def check_receipt(receipt, stored):
    need(set(receipt) == set(stored), 'bounds.json case set differs from fixtures')
    for name, got in receipt.items():
        ref = stored[name]
        need([F(x) for x in got['einstein_q']] == [F(x) for x in ref['einstein_q']], f'{name}: einstein_q mismatch')
        need(F(got['handoff_q']) == F(ref['handoff_q']), f'{name}: handoff 4*lambda mismatch')
        lo, hi = F(ref['einstein_C'][0]), F(ref['einstein_C'][1])
        mine_lo, mine_hi = F(got['einstein_C'][0]), F(got['einstein_C'][1])
        need(lo <= mine_lo and mine_hi <= hi, f'{name}: stored C_E bracket does not contain 30-digit Hutton bracket')
        need(isinstance(ref['boxes'], int) and ref['boxes'] >= 1, f'{name}: invalid stored box count')
        if 'mix' in got:
            need('mix' in ref, f'{name}: missing mix in stored receipt')
            need(
                [(F(p), F(u)) for p, u in got['mix']['spectrum']]
                == [(F(p), F(u)) for p, u in ref['mix']['spectrum']],
                f'{name}: mix spectrum mismatch',
            )
            need(F(got['mix']['q']) == F(ref['mix']['q']), f'{name}: mix q mismatch')
    print('bounds.json verified against independent unfolded-form + Hutton-pi recomputation')


def folded_exact(lam, mu, q, scale2, spec, nfold=NFOLD, witness=None):
    """Exact rational value of the folded form at a single q on an integer witness.

    The witness is the smallest eigenvector of the float folded block (a proposal only);
    it is rounded to integers and the value recomputed from exact integer correlations,
    so a negative value proves that this principal block of the folded matrix is
    indefinite at q and no sound certificate can cover a box through q.
    """
    a = weights(lam, q, 2 * nfold + 1, spec)
    cum = [F(0)]
    for i in range(1, nfold):
        cum.append(cum[-1] + a[i])
    k = min(cutoff(q, scale2), nfold)
    idx = np.arange(nfold)
    ad = np.array([float(x) for x in a])
    blk = -(ad[np.abs(idx[:, None] - idx)] + ad[idx[:, None] + idx + 1])
    blk[np.diag_indices(nfold)] = ((2 * idx + 1) + 2 * np.array([float(x) for x in cum])
                                   - ad[2 * idx + 1])
    if k:
        blk[:k, :k] += 2 * float(mu)
    if witness is None:
        w, vec = eigh(blk)
        x = vec[:, 0]
        w0 = float(w[0])
        xi = np.rint(x / float(np.max(np.abs(x))) * (2 ** RAD)).astype(np.int64)
    else:
        xi = np.asarray(witness, dtype=np.int64)
        w0 = float('nan')
    need(int(np.count_nonzero(xi)) > 1, f'degenerate probe witness at q={q}')
    sq = [F(int(v) ** 2) for v in xi]
    # The mask is the rank-one 2 mu on the WHOLE k x k block, i.e. 2 mu (sum_{i<k} x_i)^2.
    diag = sum(sq[i] * ((2 * i + 1) + 2 * cum[i]) for i in range(nfold))
    mask = 2 * mu * F(int(sum(int(v) for v in xi[:k])) ** 2)
    corr = np.convolve(xi, xi[::-1])          # corr[nfold-1+r] = sum_i x_i x_{i+r}
    diff = sum(F(int(corr[nfold - 1 + r])) * a[abs(r)] for r in range(-(nfold - 1), nfold))
    cc = np.convolve(xi, xi)                  # cc[m] = sum_{i+j=m} x_i x_j
    hank = sum(F(int(cc[m])) * a[m + 1] for m in range(2 * nfold - 1))
    return diag - diff - hank + mask, w0, blk, xi


ADVERSARIAL = (
    # (name, lambda, mu*, R^2, q_bad, box [lo, hi)) where a certifier returned POSITIVE
    # although the folded form is exactly negative.  Probes 1 and 2 are REVIEW.md F1
    # (= REVIEW2.md R2-1); probe 3 is this package's own unstable Einstein box.
    ('l10_m15_R9', F(10), F(15), F(9), F(3745657, 10 ** 8), F(33058, 10 ** 6),
     F(37457, 10 ** 6)),
    ('l12_m12_R9', F(12), F(12), F(9), F(9970489, 10 ** 8), F(81633, 10 ** 6),
     F(99707, 10 ** 6)),
    ('mustar26', F(26), F(312, 25), F(53, 5), F(99, 200), F(490, 1000), F(505, 1000)),
)


def adversarial():
    """Regression probes for REVIEW.md F1/F2, run by `--adversarial` (exit 0 = pass).

    For each probe the exact folded-form value at q_bad is the control: a negative value
    proves that no sound method can certify a box through q_bad.  The corrected device
    must then refuse both the documented box (bounded cover) and the point-wide box at
    q_bad, where the rejected verifier returned CERTIFIED POSITIVE.
    """
    spec = ((F(1), F(1)),)
    for name, lam, mu, scale2, q_bad, lo, hi in ADVERSARIAL:
        need(lo < q_bad < hi, f'{name}: q_bad is not inside the documented box')
        val, wmin, blk, xi = folded_exact(lam, mu, q_bad, scale2, spec)
        xf = xi.astype(np.float64)
        ref = float(xf @ blk @ xf)
        span = float(xi @ xi) * float(np.abs(blk).max())
        need(abs(ref - float(val)) <= 1e-10 * (abs(ref) + span),
             f'{name}: exact value {float(val):.6g} disagrees with the float contraction '
             f'{ref:.6g} of the same witness')
        need(val < 0, f'{name}: the folded form is not negative at q_bad ({float(val):.6g})')
        print(f'{name:>11}: lambda {lam}, mu* {mu}, R^2 {scale2}: exact folded-form value '
              f'{float(val):.6g} < 0 at q={q_bad} (float block eigenvalue {wmin:.6g})',
              flush=True)

        def test(left, right, k):
            return positive(hot_head(lam, mu, left, right, scale2, spec)[0])
        need(not certified(test, lo, hi, cutoff(lo, scale2), [64]),
             f'{name}: the hot cover accepted [{float(lo):.9g}, {float(hi):.9g}) although '
             f'the folded form is negative at q={q_bad}')
        thin = F(1, 10 ** 12)
        need(not positive(hot_head(lam, mu, q_bad - thin, q_bad, scale2, spec)[0]),
             f'{name}: the point-wide box at q_bad was certified positive')
        print(f'{name:>11}: box [{float(lo):.9g}, {float(hi):.9g}) and the point box at '
              f'q_bad both refused, as the exact negativity requires', flush=True)
    print('adversarial probes: every box with an exactly negative folded form was refused')


SELFCHECK = (
    # (lambda, mu*, R^2, r): window [4R^2/(2r+1)^2, (1+1/(2r)) * 4R^2/(2r+1)^2), mask r
    (F(1), F(3), F(9), 1),
    (F(1), F(3), F(9), 4),
    (F(10), F(1), F(9), 3),
    (F(1), F(1, 2), F(1), 9),
    (F(15), F(25), F(16), 8),
    (F(26), F(312, 25), F(53, 5), 5),
)


def exact_head(lam, q, scale2, spec, m):
    """Exact rational SC * (Einstein part of F) on the m x m head block.

    The Coulomb block +2 mu* 1_{i,j<k} is a constant (q-independent) matrix and is not
    included; the enclosure adds its floor to the same block, so both offsets are
    compared separately in `selfcheck`.
    """
    a = weights(lam, q, 2 * m + 1, spec)
    v = np.empty((m, m), dtype=object)
    for i in range(m):
        A_i = sum(a[1:i + 1])
        for j in range(m):
            v[i, j] = (F(SC) * ((2 * i + 1) + 2 * A_i - a[2 * i + 1]) if i == j
                       else -F(SC) * (a[abs(i - j)] + a[i + j + 1]))
    return v


def tail_selfcheck():
    """`--selfcheck` part 2: the per-row tail gap and the Schur shift, exactly.

    On a small head (m = 16) every number of the derivation is recomputed in exact rational
    arithmetic with the infinite tail closed by sum_{r>T} r^-2 <= 1/T:
      * g_j must not exceed the true gap at q = lo, mid, hi (so it is a valid lower bound);
      * theta_i must cover the exact boundary term b_im^2/g_m that REVIEW.md F2 shows the
        v1 penalty misses (checked against an UPPER bound of g_m, the conservative side).
    """
    lam, mu, scale2 = F(26), F(312, 25), F(53, 5)
    spec = ((F(1), F(1)),)
    lo, hi, m, ncol = F(490, 1000), F(505, 1000), 16, 8
    a_lo = weights(lam, lo, 2 * (m + ncol) + 4, spec)
    g = tail_gaps(lam, lo, hi, spec, m, ncol)
    need(bool(np.all(g > 0)), 'tail selfcheck: nonpositive gap')
    worst = None
    for t in (F(0), F(1, 2), F(1)):
        q = lo + (hi - lo) * t
        a = weights(lam, q, 2 * (m + ncol) + 4, spec)
        big_r = 400
        s1 = sum(a[1:big_r + 1], F(0)) + lam / (q * big_r)      # >= sum_{r>=1} a_r(q)
        A = [F(0)] * (2 * (m + ncol) + 4)
        for r in range(1, len(A)):
            A[r] = A[r - 1] + a[r]
        for j in range(m, m + ncol):
            gap = (F(2 * j + 1) + 2 * A[j] - a[2 * j + 1] - A[j - m]
                   - s1 - lam / (q * (j + m)))
            need(F(int(g[j - m]), SC) <= gap,
                 f'tail selfcheck: g_{j} exceeds the true gap at q={q} '
                 f'({F(int(g[j - m]), SC)} > {gap})')
            worst = gap if worst is None else min(worst, gap)
    a = weights(lam, lo, 2 * (m + ncol) + 4, spec)
    theta = tail_penalty(lam, lo, spec, m, g, ncol)
    gup = F(2 * m + 1) + 2 * sum(a[1:m + 1], F(0)) - a[2 * m + 1]   # >= g_m(lo)
    for i in (m - 2, m - 1):
        b = a[m - i] + a[m + i + 1]
        need(F(int(theta[i]), SC) >= b * b / gup,
             f'tail selfcheck: theta_{i} does not cover b_im^2/g_m')
    print(f'tail selfcheck: {ncol} rows x 3 exact q inside [{float(lo):.6g}, {float(hi):.6g}): '
          f'every gap bound g_j <= true gap (min true gap {float(worst):.6g}), and the shift '
          f'theta covers the exact boundary terms b_im^2/g_m: OK')


def selfcheck():
    """`--selfcheck`: verify the enclosure against EXACT rational head entries.

    Each window is evaluated at three interior q in exact rational arithmetic, which is
    independent of the rounded integers, and every head entry must satisfy
    lower <= SC*F_ij(q) <= upper, |SC*F_ij(q) - center_ij| <= radius_ij off the diagonal
    and center_ii <= SC*F_ii on it.  This is exactly the invariant that an upper-minus-
    centre radius built from swapped endpoint brackets breaks: there |value - centre| =
    radius + 1 on every odd bracket, so the check fails on such bytes and passes here.
    """
    entries = 0
    forms = 0
    for lam, mu, scale2, r in SELFCHECK:
        jump = 4 * scale2 / (2 * r + 1) ** 2
        lo, hi = jump, jump * (1 + F(1, 2 * r))
        spec = ((F(1), F(1)),)
        k, m, lower, upper, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, spec)
        need(k == r, f'selfcheck: window [{float(lo):.6g}, {float(hi):.6g}) has mask {k} != {r}')
        need(bool(np.array_equal(center, center.T)), 'selfcheck: centre is not symmetric')
        need(bool(np.array_equal(radius, radius.T)), 'selfcheck: radius is not symmetric')
        diag = np.diag_indices(m)
        off = np.ones((m, m), dtype=bool)
        off[diag] = False
        offm = np.zeros((m, m), dtype=np.int64)
        if k:
            offm[:k, :k] = flr_(SC * 2 * mu)
            need(F(int(offm[0, 0])) <= SC * 2 * mu, 'selfcheck: Coulomb block not rounded down')
        base = center - offm
        need(bool(np.all(lower[off] <= upper[off])), 'selfcheck: lower exceeds upper')
        need(bool(np.all(radius >= 0)), 'selfcheck: negative radius')
        need(bool(np.all((base - radius)[off] <= lower[off]))
             and bool(np.all(upper[off] <= (base + radius)[off])),
             'selfcheck: the radius does not cover both bracket ends')
        lo_o, up_o = np.array(lower[off], dtype=object), np.array(upper[off], dtype=object)
        ra_o, ce_o = np.array(radius[off], dtype=object), np.array(base[off], dtype=object)
        cd = np.array(base[diag], dtype=object)
        for t in (F(1, 10), F(1, 2), F(9, 10)):
            q = lo + (hi - lo) * t
            need(cutoff(q, scale2) == k, 'selfcheck: mask changed inside the window')
            v = exact_head(lam, q, scale2, spec, m)
            vo = v[off]
            need(bool(np.all(vo <= up_o)), f'selfcheck: value above upper at q={q}')
            need(bool(np.all(lo_o <= vo)), f'selfcheck: value below lower at q={q}')
            need(bool(np.all(np.abs(vo - ce_o) <= ra_o)),
                 f'selfcheck: |value - centre| > radius at q={q}')
            need(bool(np.all(cd <= v[diag])), f'selfcheck: diagonal centre above value at q={q}')
            entries += m * m
            if t == F(1, 2):
                A, mm = hot_head(lam, mu, lo, hi, scale2, spec, mbase=m)
                need(mm == m, 'selfcheck: production head size differs from the check size')
                rng = np.random.default_rng(1000 + r)
                for _ in range(3):
                    xi = [int(v) for v in rng.integers(-1000, 1001, size=m)]
                    cert = sum(xi[i] * xi[j] * int(A[i, j]) for i in range(m) for j in range(m))
                    true = sum(xi[i] * xi[j] * v[i, j] for i in range(m) for j in range(m))
                    # exact F omits the q-independent Coulomb block; A carries its floor,
                    # so add the exact block back and compare in the SAME (SC) units
                    coul = F(SC) * 2 * mu * sum(xi[:k]) ** 2
                    need(F(cert) <= true + coul,
                         'selfcheck: the certified head matrix exceeds the exact folded form '
                         f'on an integer vector at q={q}')
                    forms += 1
    print(f'interval enclosure selfcheck: {len(SELFCHECK)} windows x 3 interior q, '
          f'{entries} exact rational entry comparisons against lower/upper/centre/radius and '
          f'{forms} exact quadratic-form comparisons A <= F: OK')
    tail_selfcheck()


def v1_tail_penalty(lam, lo, spec, m, g):
    """REVIEW.md F2 regression (mutant mode only): pen[i] = (2m/g) eta_i eta_0, eta_0 = O(1/m^2)."""
    eta0 = ceil_(SC * 2 * lam / (lo * m * m))
    eta = np.array([ceil_(SC * 2 * lam / (lo * t * t)) for t in range(m, 0, -1)], dtype=np.int64)
    gm = int(np.asarray(g, dtype=np.int64).ravel()[0])     # v1 used the single gap g_m
    need(int(eta.max()) * eta0 * 2 * m < 2 ** 62 and gm > 0, 'v1 penalty overflow')
    return -(-(2 * m) * eta * eta0 // gm)


def v1pen_head(lam, mu, lo, hi, scale2, spec):
    """Sound enclosure with the rejected v1 tail penalty (mutant mode only)."""
    k, m, _, _, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, spec)
    d = np.diag_indices(m)
    g = tail_gaps(lam, lo, hi, spec, m)
    center[d] -= head_radius(radius) + v1_tail_penalty(lam, lo, spec, m, g)
    return center


def exact_gap_upper(lam, lo, spec, m):
    """Exact rational UPPER bound on the tail gap g_m at q = lo (drops both tail sums)."""
    a = weights(lam, lo, 2 * m + 2, spec)
    return F(2 * m + 1) + 2 * sum(a[1:m + 1], F(0)) - a[2 * m + 1]


def mutant_hot(kind, lam, mu, scale2, spec):
    """Refuse each REVIEW.md F1/F2/F9 regression; the sound device must not reproduce it."""
    if kind == 'entrywise':
        # REVIEW.md F1: the v1 device bounded every off-diagonal from BELOW (largest magnitude,
        # A_ij <= SC*F_ij for all i,j) and then read "A >= 0" as "SC*F >= 0".  An entrywise
        # order does not survive multiplication by a mixed-sign vector, so the step is invalid
        # for mu* > 0.  Refutation, exact and per probe: (i) every entry of the entrywise
        # matrix A satisfies A_ij <= SC*F_ij(q) at q in the box (control: the premise of the
        # v1 argument holds); (ii) the exact integer witness x of the folded form gives
        # x^T A x > 0 > x^T (SC*F(q_bad)) x, so the entrywise positivity of x^T A x certifies a
        # NEGATIVE direction of the true form as positive; (iii) the sound mixed-sign
        # enclosure gives x^T (SC*Fbar) x < 0 on the same box and x, and refuses it.
        for name, l10, m10, r10, q_bad, lo, hi in ADVERSARIAL:
            lam, mu, scale2 = F(l10), F(m10), F(r10)
            sp = ((F(1), F(1)),)
            val, _w, _b, xi = folded_exact(lam, mu, q_bad, scale2, sp)
            control(val < 0, f'{name}: folded form is not negative at q_bad')
            k, m, lower, upper, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, sp)
            d = np.diag_indices(m)
            A = lower.copy()                                   # v1 entrywise-lower off-diagonals
            A[d] = center[d]
            head = exact_head(lam, q_bad, scale2, sp, m)       # exact completed head block at q_bad
            bad = [(i, j) for i in range(m) for j in range(m)
                   if i != j and F(int(A[i, j])) > head[i, j]]
            control(not bad, f'{name}: the entrywise lower bound fails on entry {bad[:1]}')
            x = np.asarray(xi[:m], dtype=object)
            nz = [i for i in range(m) if int(x[i]) != 0]
            need(len(nz) > 0, f'{name}: the folded witness vanishes on the head')
            lhs = sum(int(x[i]) * int(x[j]) * int(A[i, j]) for i in nz for j in nz)
            rhs = sum(int(x[i]) * int(x[j]) * head[i, j] for i in nz for j in nz)
            S = hot_head(lam, mu, lo, hi, scale2, sp)[0]
            snd = sum(int(x[i]) * int(x[j]) * int(S[i, j]) for i in nz for j in nz)
            control(F(snd) < 0, f'{name}: the sound device does not refuse the box')
            if lhs > 0 and F(rhs) < 0:
                refused(f'entrywise off-diagonal bound (REVIEW.md F1) is invalid at {name}: on the '
                        f'box [{float(lo):.6g}, {float(hi):.6g}) every entry satisfies A <= SC*F, '
                        f'yet the exact witness x (support 0..{nz[-1]}) gives x^T A x = '
                        f'{lhs / SC / 1e12:.4g}e12 SC-units > 0 because x is mixed sign, while '
                        f'x^T SC*F(q={float(q_bad):.9g})x = {float(rhs) / SC / 1e12:.4g}e12 < 0; '
                        f'the sound enclosure gives {snd / SC / 1e12:.4g}e12 < 0 and refuses')
            need(False, f'{name}: entrywise mutant not separated ({lhs / SC:.6g}, {float(rhs) / SC:.6g})')
    if kind == 'v1pen':
        # REVIEW.md F2: the v1 penalty pen[m-1] is short of the single boundary Schur term
        # B_{m,m-1}^2 / F_QQ,mm = (a_1 + a_2m)^2 / g_m by a factor ~20.  Refutation: exact
        # rational shortfall at q = lo, with g_m bounded ABOVE (1/g_low <= 1/g_true).
        lo = F(490, 1000)
        k, m, _, _, center, radius = hot_enclosure(lam, mu, lo, F(505, 1000), scale2, spec)
        g = tail_gaps(lam, lo, F(505, 1000), spec, m)
        pen = v1_tail_penalty(lam, lo, spec, m, g)
        a_lo = weights(lam, lo, 2 * m + 2, spec)
        gup = exact_gap_upper(lam, lo, spec, m)
        need(gup > 0 and F(int(g[0])) / SC <= gup, 'tail gap bound exceeds the exact gap')
        need(a_lo[1] + a_lo[2 * m] > 0, 'boundary coupling vanished')
        need_b = (a_lo[1] + a_lo[2 * m]) ** 2 / gup          # <= B_{m,m-1}^2 / g_m(q_lo)
        got = F(int(pen[m - 1])) / SC
        ratio = need_b / got
        need(ratio > 1, f'v1 penalty is not short of the exact boundary term ({float(ratio):.6g})')
        hits = certified(lambda l, r, _k: positive(v1pen_head(lam, mu, l, r, scale2, spec)),
                         F(490, 1000), F(505, 1000), cutoff(F(490, 1000), scale2), [64])
        refused(f'v1 tail penalty (REVIEW.md F2) is {float(ratio):.4g}x short of the exact '
                f'boundary Schur term B_(m,m-1)^2/g_m = {float(need_b):.6g} at q={lo} '
                f'(m={m}, claimed {float(got):.6g}); it {"certifies" if hits else "fails to certify"} '
                f'the exactly unstable box [0.49, 0.505)')
    if kind == 'rsign':
        # A radius sign flip claims F - centre >= +diag(rho).  Refutation at q = hi with the
        # vector x = e_(m-2) - e_(m-1): the claim needs -2 E_ij >= rho_i + rho_j, which fails
        # exactly, while the sound direction -2 E_ij >= -(rho_i + rho_j) holds (control).
        lo, hi = F(490, 1000), F(495, 1000)
        k, m, _, _, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, spec)
        rho = head_radius(radius)
        i, j = m - 2, m - 1
        a = weights(lam, hi, 2 * m + 2, spec)
        entry = -F(SC) * (a[j - i] + a[i + j + 1])
        dev = entry - F(int(center[i, j]))
        need(2 * dev < F(int(rho[i])) + F(int(rho[j])), 'control: the flipped bound holds here')
        need(-2 * dev >= -(F(int(rho[i])) + F(int(rho[j]))), 'the sound bound fails (control)')
        need(dev != 0, 'degenerate off-diagonal deviation')
        refused(f'radius sign flip: at q={hi} the entry ({i},{j}) deviates by '
                f'{float(dev) / SC:.6g} from the centre, so the flipped claim needs '
                f'-2*dev >= {(int(rho[i]) + int(rho[j])) / SC:.6g} but -2*dev = '
                f'{float(-2 * dev) / SC:.6g}; the radius does not cover the value at hi')
    if kind == 'overflow':
        # REVIEW.md F9 / dropped overflow guard in head_radius: the unguarded row sums wrap
        # int64 and stop dominating the radius.  Refutation: exact comparison of the returned
        # rho with the exact Fraction row sum; the guarded path raises ValueError (control).
        n = 960
        rad = np.zeros((n, n), dtype=np.int64)
        rad[0, 0] = 1 << 42                         # a single large off-diagonal deviation
        try:
            head_radius(rad)
            control(False, 'the guarded head_radius accepted an overflowing radius')
        except ValueError:
            pass
        bad = head_radius(rad, guard=False)
        h = np.array([(1 << 22) // (i + 1) for i in range(n)], dtype=np.int64)
        exact0 = int(rad[0, 0]) * int(h[0])
        need(exact0 >= 2 ** 63, 'control: the exact row sum does not overflow int64')
        need(F(int(bad[0])) < F(exact0, int(h[0])),
             'the unguarded row sum still dominates (control)')
        refused(f'dropped overflow guard: the unguarded radius row sum wraps to '
                f'{int(bad[0])} while the exact row sum is {exact0} (>= 2^63), so rho no '
                f'longer dominates the off-diagonal deviation; the guarded path refuses the '
                f'same input with ValueError')


def mutant_path(kind, data):
    case = next(c for c in data['cases'] if c['name'] == 'subhalf-26-12over25')
    lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
    mix_spec = spectrum_of(case['mix'])
    ein_spec = ((F(1), F(1)),)
    low, _ = map(F, case['einstein'])
    qm = F(case['mix']['q'])
    handoff = 4 * lam
    if kind == 'spectrum':
        need(len(mix_spec) == 2, 'valid mixture refused')
        attack = dict(case['mix'], high_p=str(1 - F(case['mix']['high_p'])))
        try:
            spectrum_of(attack)
        except ValueError as exc:
            need('second moment' in str(exc), f'wrong rejection reason: {exc}')
            refused('p -> 1-p mixture rejected by second-moment guard')
        need(False, 'spectrum mutant accepted')
    if kind in ('entrywise', 'v1pen', 'rsign', 'overflow'):
        mutant_hot(kind, lam, mu, scale2, ein_spec)
        need(False, f'{kind} mutant accepted')
    if kind == 'coulomb':
        gate, _ = cold_value(lam, mu, qm, scale2, mix_spec)
        control(gate < 0, 'unmutated mixture witness lost negative sign')
        v, _ = cold_value(lam, 2 * mu, qm, scale2, mix_spec)
        if v >= 0:
            refused(f'doubling mu* removes cold instability at q={qm} (val={float(v):.6g} >= 0)')
        need(False, 'coulomb mutant survived doubled repulsion')
    gate, _ = cold_value(lam, mu, low, scale2, ein_spec)
    control(gate < 0, 'unmutated Einstein witness lost negative sign at q_lo')
    try:
        sum(
            cover(lambda l, r, _k: positive(hot_head(lam, mu, l, r, scale2, ein_spec)[0]), l, r, k)
            for l, r, k in windows(low, handoff, scale2)
        )
    except ValueError as exc:
        need('cannot be certified' in str(exc), f'unexpected error: {exc}')
        refused(f'Einstein form is not positive on [q_lo, 4*lam): {exc}')
    need(False, 'endpoint mutant certified interval below q_hi')


def main():
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--mutant', choices=('', 'endpoint', 'coulomb', 'spectrum', 'receipt',
                                            'entrywise', 'v1pen', 'rsign', 'overflow'), default='')
    parser.add_argument('--adversarial', action='store_true',
                        help='regression probes from REVIEW.md F1: a box holding an exactly '
                             'negative folded form must be refused')
    parser.add_argument('--selfcheck', action='store_true',
                        help='verify the hot enclosure against exact rational values')
    args = parser.parse_args()
    if args.selfcheck:
        selfcheck()
        return 0
    if args.adversarial:
        adversarial()
        return 0
    data = json.loads((HERE / 'fixtures.json').read_text(encoding='utf8'))
    need(len(data['cases']) == 4, 'expected 4 certified sub-1/2 counterexamples')
    print(f'pinned a_1 checks: {a1_pin_check(data["cases"])} mixtures')
    if args.mutant and args.mutant != 'receipt':
        mutant_path(args.mutant, data)
        need(False, f'{args.mutant} mutant accepted')
    stored = json.loads((HERE / 'bounds.json').read_text(encoding='utf8'))
    if args.mutant == 'receipt':
        # The stored C_E brackets must CONTAIN the recomputed ones: a table shaved inward
        # (or an inward-rounded decimal like RESULT.md F8) must not pass.  Control first.
        check_receipt(stored, stored)
        shaved = json.loads(json.dumps(stored))
        e = shaved['subhalf-26-12over25']['einstein_C']
        e[0] = str(F(e[0]) + F(1, 10 ** 6))
        try:
            check_receipt(stored, shaved)
        except ValueError as exc:
            refused(f'shaved C_E bracket rejected by receipt check ({exc})')
        need(False, 'receipt mutant accepted a shaved C_E bracket')
    receipt = {}
    table = []
    for entry in data['cases'] + data['anchors']:
        run_case(entry, receipt, table)
    print_table(table)
    bad = [row for row in table if row['status'] != 'CERTIFIED']
    if bad:
        print(f'\n{len(bad)} of {len(table)} instances REFUSED:')
        for row in bad:
            print(f'{row["name"]:>22}: {row["reason"]}')
        print('REFUSED: the hot claim is not certified for the instances listed above')
        return 1
    check_receipt(receipt, stored)
    print('independent verification of MUSTAR-HALF certificates: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
