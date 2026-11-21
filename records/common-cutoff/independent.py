"""Second, independent verification of the common-cutoff certificates (RIGOR.md 2, 4, 5).

Cold side (exact rationals, no folding).  The form is evaluated on the UNFOLDED full
Matsubara line, n in {-N,...,N-1}, w_n = (2n+1) pi T, f_n = Delta_n/|w_n|:

    D_n    = |2n+1| + a_0 + 2 sum_{j=1}^{i(n)} a_j ,   i(n) = max(n, -n-1)
    K_nm   = a_{|n-m|} - mu* c_n c_m ,                 c_n = 1_{(2n+1)^2 q < 4R^2}
    form   = sum_n f_n^2 D_n - sum_nm f_n f_m K_nm
           = sum_d c_d (|2d+1| + a_0 + 2A_{i(d)})  -  sum_e c_e a_{|e|}  +  mu* (sum_{n in mask} f_n)^2

with c_d = sum_n f_n f_{n+d} (integer correlations) and A_m = sum_{j=1}^m a_j, so the
identity is checked in exact rational arithmetic on the whole line with one convolution.
The witness is an integer vector supported on the truncated band and extended by zero, so
the value is finite and exact; the folded identity a_0 = 2 sum a_j - sum 2 a_{...} of
RIGOR.md 4 is never used.  (a[0] is set to 0 throughout, i.e. the a_0 of the mass and the
a_0 of the pairing diagonal are cancelled against each other, exactly as the identity
requires; nothing else depends on that convention.)

Hot side (exact integers, signed interval enclosure).  On a window [q_l, q_r) with
q_l <= q <= q_r and constant mask k = cutoff(q_l), the folded form F(q) (RIGOR.md 4) is
split ONCE at m = max(NB, 2k+1) modes: the head is modes 0..m-1, the infinite tail is the
rest (no mode is dropped and no finite cut is used for the tail).  Every head entry is
bracketed by exact integers,

    lower_ij = -ceil(SC*[a_{|i-j|}(q_l) + a_{i+j+1}(q_l)])   (the value at q_l)
    upper_ij = -floor(SC*[a_{|i-j|}(q_r) + a_{i+j+1}(q_r)])  (the value at q_r)

for i != j, because a_r(q) decreases in q; the diagonal is a one-sided LOWER bound
2i+1 + 2 sum_{j<=i} floor(a_j(q_r)) - ceil(a_{2i+1}(q_l)) + floor(2 mu*) 1_{i<k}.  The
integers C = (lower+upper)//2 (floored midpoint) and R = max(upper-C, C-lower) >= 0 give
|SC*F_ij(q) - C_ij| <= R_ij on every off-diagonal entry and C_ii <= SC*F_ii.  Two
PSD-dominated diagonal penalties are then subtracted:

    A = C - diag(rho) - diag(theta) <= F(q)  (as quadratic forms, for ALL real vectors),

rho from a weighted AM-GM row-sum bound on the off-diagonal radius (head_radius) and theta
from the exact Schur complement of the infinite tail against a uniform Gershgorin gap g of
every tail row (tail_gap, tail_penalty).  No entrywise (Z-matrix) step is used anywhere.
A is certified positive by: a float Cholesky proposal L, then the EXACT integer residual
R = A*(G^2/SC) - L^T L and the sufficient condition 2 R_ii > sum_{j != i} |R_ij| (strict
diagonal dominance of an integer matrix); this is sound for any integer proposal L,
whatever the float code returns.  It shares its family with replay.py (whose proposal is
built from its own matrix scale, residual scale, tail split and witness vectors) but not
its constants, truncation or tail argument.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

import numpy as np
from scipy.linalg import eigh

HERE = Path(__file__).resolve().parent
SC = 1 << 17          # head matrix scale (integer form entries)
GRAM = (1 << 26, 1 << 25, 1 << 24, 1 << 27, 1 << 23, 1 << 22, 1 << 21, 1 << 20)
NB = 160              # head block: modes 0..NB-1, and the infinite tail starts at NB
TAIL_SPAN = 8         # tail columns summed exactly for l <= TAIL_SPAN*m, closed form after
NC = 400             # cold half band: modes n in [-NC, NC-1]
RAD = 22             # witness rounding scale exponent (integers of size ~2**RAD)
NFOLD = 600          # fold count of the adversarial probes' exact folded-form witnesses

# a_1 = lam * int u/(u+q) dp at the mixture witness q of each counterexample, computed by
# hand from the fixture strings (p_high, u_low, u_high) and pinned here so that a swapped
# (u,p) unpacking cannot survive: a_1 = lam[(1-p)u_lo/(u_lo+q) + p u_hi/(u_hi+q)].
A1_PINS = {
    'einstein-counterexample': ((F(1, 100), 3, F(9, 599), F(1, 10), F(60)), F(180300, 66011)),
    'counterexample-wide': ((F(1, 200), 2, F(23, 4998), F(2, 25), F(200)), F(1280400, 680017)),
    'counterexample-strong': ((F(1, 100), 4, F(23, 2498), F(2, 25), F(100)), F(35600, 10001)),
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def control(ok, why):
    """A mutant's unmutated control; breaking it invalidates the mutant (exit 2)."""
    if not ok:
        print(f'CONTROL FAILED (mutant invalid): {why}')
        raise SystemExit(2)


def refused(why):
    """The mutant's perturbed statement was refused, as required (exit 1)."""
    print(f'mutant refused: {why}')
    raise SystemExit(1)


def ceil_(x):
    return -((-x.numerator) // x.denominator)


def flr_(x):
    return x.numerator // x.denominator


def weights(lam, q, count, spectrum):
    """a[0] = 0 (cancelled a_0), a[j] = lam int u/(u+q j^2) dp for j = 1..count-1."""
    a = [F(0)]  # type: list[F]
    for j in range(1, count):
        a.append(sum(lam * p * u / (u + q * j * j) for p, u in spectrum))
    need(all(x >= 0 for x in a), 'negative weight')
    need(a[1] <= lam, 'a_1 exceeds lambda')
    return a


def cutoff(q, scale2):
    """k = #{j >= 1 : (2j-1)^2 q < 4 R^2}, from integer comparisons only."""
    pn, pd = q.numerator, q.denominator
    sn, sd = scale2.numerator, scale2.denominator
    top = 4 * sn * pd                     # (2j-1)^2 * (pn*sd) < top
    run = pn * sd
    if top <= run:                        # 4 R^2 <= q: no odd d >= 1 passes, empty mask
        return 0
    dmax = isqrt((top - 1) // run)
    dmax -= 1 - dmax % 2
    need(dmax >= 1, 'empty mask')
    return (dmax + 1) // 2


def in_mask(d, q, scale2):
    """exact test (2d+1)^2 q < 4 scale2 for the Mat subara index d."""
    return (2 * d + 1) ** 2 * q < 4 * scale2


def spectrum_of(mix):
    p = F(mix['high_p'])
    low, high = F(mix['low_u']), F(mix['high_u'])
    need(0 < p < 1 and 0 < low < 1 < high, f'bad mixture {mix}')
    need((1 - p) * low + p * high == 1, f'mixture second moment is not one: {mix}')
    return ((1 - p, low), (p, high))


def a1_pin_check():
    """Pin a_1 against hand-computed rationals (catches a u<->p unpacking swap)."""
    for name, ((q, lam, p, low, high), expect) in A1_PINS.items():
        spec = ((1 - p, low), (p, high))
        got = weights(F(lam), q, 3, spec)[1]
        need(got == expect, f'{name}: a_1 is {got}, hand value {expect}')
    return len(A1_PINS)


def tail_gap(lam, lo, hi, spec, m):
    """Lower bound g, uniform in j >= m, of every diagonal Gershgorin gap of the tail.

    Row j >= m of the folded matrix has diagonal 2j+1 + 2A_j - a_{2j+1} and off-diagonal
    entries -(a_|j-l| + a_{j+l+1}) for l >= m, l != j.

    Step 1 (fixed q).  Fix q in [lo,hi].  The a_r(q) are nonnegative, so A_r(q) =
    sum_{t<=r} a_t(q) increases in r, and for every j >= m

      2A_j(q) - A_{j-m}(q) = A_j(q) + sum_{t=j-m+1}^{j} a_t(q) >= A_j(q) >= A_m(q).

    Step 2 (endpoints, term by term).  a_r(q) and A_r(q) decrease in q, so A_j(q) >=
    A_j(hi), A_{j-m}(q) <= A_{j-m}(lo), a_{2j+1}(q) <= a_{2j+1}(lo), and with S_T =
    sum_{r>=T} a_r(lo) the off-diagonal absolute row sum at q is at most
    A_{j-m}(lo) + S_1(lo) + S_{j+m+1}(lo).  Combining steps 1 and 2, every tail gap
    (RIGOR.md 5) satisfies

      gap_j >= g = 2m+1 + A_m(hi) - a_{2m+1}(lo) - S_1(lo) - S_{2m+1}(lo) > 0.

    S_1 is summed exactly to R = 8m+8 terms and closed by sum_{r>R} r^-2 <= 1/R, and
    S_{2m+1} = sum_{r>=2m+1} a_r <= lam/(lo 2m) because sum_{r>2m} r^-2 <= 1/(2m).
    g is returned as an integer of scale SC and is a verified LOWER bound on every gap.
    """
    R = TAIL_SPAN * (m + 1)
    a = weights(lam, lo, R + 1, spec)
    a_hi = weights(lam, hi, m + 1, spec)
    s1 = sum(a[1:R + 1]) + lam / (lo * R)
    g = (SC * (2 * m + 1) + flr_(SC * sum(a_hi[1:m + 1])) - ceil_(SC * a[2 * m + 1])
         - ceil_(SC * s1) - ceil_(SC * lam / (lo * 2 * m)))
    need(g > 0, f'tail Gershgorin gap is not positive ({float(g) / SC:.6g} at m={m})')
    return g


def tail_penalty(lam, lo, spec, m, g):
    """Rows of the Schur penalty (1/g) sum_{l>=m} b_il b_jl, b_il = a_|i-l| + a_{i+l+1}.

    Only the columns l >= m couple to the head i < m.  For l >= m both indices |i-l| and
    i+l+1 are at least l-m+1 and a_r <= lam/(lo r^2), so b_il <= 2 lam/(lo (l-m+1)^2);
    the columns beyond L = TAIL_SPAN*m therefore add at most m (2 lam/lo)^2/(3 (L-m)^3)
    to every row, since sum_{t>T} t^-4 <= 1/(3 T^3).  All arithmetic is exact rational
    up to the final outward rounding to integers of scale SC (a larger penalty is safe).
    """
    L = TAIL_SPAN * m
    up = np.array([ceil_(SC * x) for x in weights(lam, lo, L + m + 2, spec)], dtype=np.int64)
    li = np.arange(m, L + 1)
    i = np.arange(m)[:, None]
    be = up[np.abs(i - li)] + up[i + li + 1]   # b_il at scale SC, exact rounded up
    need(int(be.max()) > 0, 'empty head/tail coupling')
    col = be.sum(axis=0)                       # sum_{i<m} b_il
    need(int(be.min()) >= 0 and int(col.min()) >= 0, 'tail coupling must be nonnegative')
    # per_i = sum_l be_il col_l <= max(be) * sum_l col_l: guard the WHOLE sum, not one product
    need(int(be.max()) * int(col.sum()) < 2 ** 62, 'tail column sum overflow')
    per = be @ col                             # sum_j sum_{l<=L} b_il b_jl at SC**2
    far = ceil_(SC * SC * (2 * lam / lo) ** 2 * m / (3 * (L - m) ** 3))
    per = per + far * np.ones(m, dtype=np.int64)
    need(int(per.max()) < 2 ** 62, 'tail penalty overflow')
    return -(-per // g)                        # ceil(per/g): the penalty must dominate


def head_radius(radius):
    """Weighted row sums rho_i = ceil((1/h_i) sum_j R_ij h_j) of the off-diagonal radius.

    For any real x, sum_{i!=j} R_ij |x_i x_j| = sum_{i,j} R~_ij x~_i x~_j with x~_i =
    h_i|x_i| and R~_ij = R_ij h_j/h_i (symmetric because R is); its absolute value is at
    most sum_i rho_i x_i^2.  So the diagonal subtraction diag(rho) dominates the whole
    off-diagonal deviation for EVERY vector, mixed-sign ones included; h > 0 is a free
    weight (h_i = 2^22/(i+1) here, so rho_i is an integer, rounded up).
    """
    need(radius.dtype == np.int64 and bool(np.all(radius >= 0)), 'radius must be int64 >= 0')
    h = np.array([(1 << 22) // (i + 1) for i in range(radius.shape[0])], dtype=np.int64)
    # row_i = sum_j |R_ij| h_j <= max|R| * sum_j h_j: guard BEFORE the matmul
    need(int(np.abs(radius).max()) * int(h.sum()) < 2 ** 62, 'radius row sums overflow int64')
    rows = np.abs(radius) @ h
    need(int(rows.max()) >= 0, 'radius row sums must be nonnegative')
    return -(-rows // h)


def hot_enclosure(lam, mu, lo, hi, scale2, spec, mbase=None):
    """Integer centre+radius enclosure of SC*F on the head block (RIGOR.md 5, item 1).

    Head modes 0..m-1 with m = max(mbase, 2k+1) >= the mask width k, k = cutoff(lo), the
    window [lo,hi) carrying that single mask.  Returns (k, m, lower, upper, center, radius):
    off-diagonal entries -(a_|i-j| + a_{i+j+1}) are bracketed by the exact integers
    lower = -(ceil(SC a(lo)) + ceil(SC a(lo)))  (value at lo: larger magnitude)
    upper = -(floor(SC a(hi)) + floor(SC a(hi))) (value at hi: smaller magnitude),
    so lower <= SC*F_ij(q) <= upper for EVERY q in [lo, hi); the diagonal
    2i+1 + 2A_i - a_{2i+1} + 2 mu [i<k] is bounded BELOW (one-sidedly) by its value with
    A_i at hi and a_{2i+1} at lo, valid because A_i(q) DECREASES in q and a_{2i+1} too.
    The centre is the floored midpoint and the radius covers BOTH ends of the bracket:

      center = (lower+upper)//2,  radius = max(upper-center, center-lower) >= 0,

    hence |SC*F_ij(q) - center_ij| <= radius_ij on every off-diagonal entry (odd brackets
    included) and center_ii <= SC*F_ii.  radius is 0 on the diagonal.
    """
    need(0 < lo < hi, 'empty hot window')
    k = cutoff(lo, scale2)
    m = max(NB if mbase is None else mbase, 2 * k + 1)
    a_lo = weights(lam, lo, 2 * m + 1, spec)   # a_r(lo), r <= 2m
    a_hi = weights(lam, hi, 2 * m + 1, spec)   # a_r(hi), r <= 2m
    up = np.array([ceil_(SC * x) for x in a_lo], dtype=np.int64)
    dn = np.array([flr_(SC * x) for x in a_hi], dtype=np.int64)
    idx = np.arange(m)
    diff = np.abs(idx[:, None] - idx)
    hank = idx[:, None] + idx + 1
    upper = -(dn[diff] + dn[hank])             # value at hi: the smaller magnitude
    lower = -(up[diff] + up[hank])             # value at lo: the larger magnitude
    diag = np.diag_indices(m)
    need(bool(np.all(lower <= upper)), 'hot window endpoint brackets are out of order')
    center = (lower + upper) // 2              # floor: lower <= center <= upper
    # radius covers BOTH ends of the bracket, so |SC*F_ij - center_ij| <= radius_ij holds
    # exactly (upward-rounded brackets); it is never negative.
    radius = np.maximum(upper - center, center - lower)
    radius[diag] = 0
    need(bool(np.all(radius >= 0)), 'hot radius is negative')
    # A_i(hi) = sum_{r=1}^{i} a_r(hi), floored; 2 mu floored: both are lower bounds
    cum = np.array([flr_(SC * sum(a_hi[1:i + 1])) for i in range(m)], dtype=np.int64)
    center[diag] = SC * (2 * idx + 1) + 2 * cum - up[2 * idx + 1]
    if k:
        center[:k, :k] += flr_(SC * 2 * mu)
    return k, m, lower, upper, center, radius


def hot_head(lam, mu, lo, hi, scale2, spec, mbase=None):
    """Certified integer matrix whose positivity implies the folded form's on [lo, hi).

    The head block is enclosed by hot_enclosure (centre plus off-diagonal radius, the
    diagonal being a one-sided lower bound), and the two PSD-dominated penalties are then
    subtracted ON THE DIAGONAL:

      A = center - diag(rho) - diag(theta) <= folded form  (as quadratic forms),

    first for the off-diagonal enclosure radius (head_radius) and then for the Schur
    complement of the infinite tail, which is >= g * ||y||^2 with the tail gap g of
    tail_gap, so 2 x^T B y >= -(1/g)||B^T x||^2 >= -sum_i theta_i x_i^2.  Both steps are
    PSD-dominated, hence valid for all real x (RIGOR.md 5); no entrywise (Z-matrix)
    statement is made anywhere.  Entries are exact integers of scale SC.
    """
    k, m, _, _, center, radius = hot_enclosure(lam, mu, lo, hi, scale2, spec, mbase)
    need(k == cutoff(lo, scale2), 'hot enclosure mask does not match the window')
    g = tail_gap(lam, lo, hi, spec, m)
    center[np.diag_indices(m)] -= head_radius(radius) + tail_penalty(lam, lo, spec, m, g)
    need(int(np.abs(center).max()) < 2 ** 29, 'block too large for the residual product')
    return center


def positive(A):
    """Certify the integer symmetric matrix A > 0 in exact integer arithmetic.

    A float eigenvalue estimate proposes a shift and a float Cholesky a triangular factor;
    the factor is re-rounded to int64 at a power-of-two scale G and the exact integer
    residual R = A*(G**2/SC) - Lh @ Lh.T must be strictly diagonally dominant with
    positive diagonal.  Exactness of every int64 product is GUARDED, never assumed:
    |Lh| < 2^31 and every Cauchy-Schwarz row norm < 2^60 keep each entry of Lh @ Lh.T an
    exact int64 value, |A|*(G**2/SC) < 2^61 keeps A*(factor) exact, and |R| < 2^61/n keeps
    the row sums |R|.sum(axis=1) and 2*R.diagonal() exact.  A failed guard skips the
    candidate (fail closed): nothing is ever clamped or silently rounded, and floats are
    only proposal generators.  The input is asserted to be an exact int64, square,
    symmetric matrix, and the factor is asserted finite BEFORE the int64 cast (a NaN or
    inf factor would otherwise cast to an arbitrary integer and could certify nonsense).
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
        return False
    shifts = [0.0] + [lam * c for c in (0.5, 0.9, 0.25, 0.1, 0.02, 0.004)]
    for G in GRAM:
        factor = G * G // SC
        if amax * factor >= 2 ** 61:
            continue
        for sh in shifts:
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
                if float(np.max((Lh ** 2).sum(axis=1))) * (1 + 1e-9) >= 2 ** 60:
                    break
                Lh = Lh.astype(np.int64)
                res = A * factor - Lh @ Lh.T
                if int(np.abs(res).max()) >= 2 ** 61 // n:
                    break  # row sums could overflow int64: fail closed, never clamp
                if bool(np.all(2 * res.diagonal() > np.abs(res).sum(axis=1))):
                    return True
                dM = np.linalg.solve(np.tril(Lf), (0.5 * res / factor).T).T
                Lf = Lf + dM
    return False


def cover(test, lo, hi, k, depth=0):
    if test(lo, hi, k):
        return 1
    need(depth < 22, f'hot interval cannot be certified: [{float(lo):.12g}, {float(hi):.12g})')
    mid = (lo + hi) / 2
    return cover(test, lo, mid, k, depth + 1) + cover(test, mid, hi, k, depth + 1)


def certified(test, lo, hi, k, budget, depth=0):
    """Bounded version of cover for the adversarial probes: True only on a full cover.

    It returns False as soon as the box budget or the depth limit is exhausted, so it can
    never turn an incomplete search into a certificate; a box that contains a point where
    the folded form is negative is refused by construction, at any budget.
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
    """Split [lo,hi) at the mask jumps; each window carries its own (constant) mask.

    The mask is constant on [lo, 4 R^2/(2k-1)^2) with k = cutoff(lo): inside the window
    (2k-1)^2 q < 4 R^2 <= (2k+1)^2 q, so cutoff(q) = k there, and the right end is where
    index k-1 leaves the mask.
    """
    while lo < hi:
        k = cutoff(lo, scale2)
        right = min(hi, 4 * scale2 / (2 * k - 1) ** 2) if k else hi
        need(right > lo, f'empty window at {float(lo):.12g}')
        yield lo, right, k
        lo = right


def cold_value(lam, mu, q, scale2, spec, n=NC):
    """Exact rational value of the full-line form on a rounded integer witness.

    The instability is a ray-quantity statement: lam_max(D^-1/2 K D^-1/2) > 1 is equivalent
    to x^T(D-K)x < 0 for the generalized eigenvector of Kx = lam_max Dx, so the witness is
    that vector.  x is then rounded to integers of order 2**RAD and the form value is
    recomputed exactly on the whole line from the integer correlations.
    """
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
    # kernel K = a - mu*c c^T, so the defect operator D - K carries +mu*c c^T
    K = K - float(mu) * np.outer(mask, mask)
    K = 0.5 * (K + K.T)
    # a_0 = lam sits in both the mass and the pairing diagonal and cancels; a[0] = 0 drops
    # it from the pairing, so it must not be added to the mass either.
    Dg = np.diag(np.array([abs(2 * int(d) + 1) + 2 * float(cum[i[t]])
                           for t, d in enumerate(idx)]))
    ray, vec = eigh(K, Dg, subset_by_index=(2 * n - 1, 2 * n - 1))
    x = vec[:, 0]
    xi = np.rint(x / float(np.max(np.abs(x))) * (2 ** RAD)).astype(np.int64)
    need(int(np.count_nonzero(xi)) > 1, f'{lam} {q}: degenerate witness')
    diag = [F(int(xi[t]) ** 2) * (abs(2 * int(idx[t]) + 1) + 2 * cum[i[t]])
            for t in range(2 * n)]
    corr = np.convolve(xi, xi[::-1])
    pair = sum(F(int(corr[2 * n - 1 + d])) * a[abs(d)] for d in range(-(2 * n - 1), 2 * n))
    block = int(xi[mask > 0].sum())
    val = sum(diag) - pair + mu * block * block
    return val, float(ray[0])


ADVERSARIAL = (
    # REVIEW2.md R2-1/R2-2 probes: (name, lambda, mu*, R^2, q_bad, box [lo, hi)) where the
    # rejected verifier returned CERTIFIED POSITIVE although the folded form is negative.
    ('l10_m15_R9', F(10), F(15), F(9), F(3745657, 10 ** 8), F(33058, 10 ** 6),
     F(37457, 10 ** 6)),
    ('l12_m12_R9', F(12), F(12), F(9), F(9970489, 10 ** 8), F(81633, 10 ** 6),
     F(99707, 10 ** 6)),
    ('case1_k16', F(3), F(2), F(9, 4), F(83845, 10 ** 7), F(8264, 10 ** 6), F(8385, 10 ** 6)),
)


def folded_exact(lam, mu, q, scale2, spec, nfold=NFOLD, witness=None):
    """Exact rational value of the folded form at a single q on an integer witness.

    The witness is the smallest eigenvector of the float folded block (a proposal only);
    it is rounded to integers of order 2**RAD and the value is recomputed from the exact
    integer correlations, so a negative value proves that this principal block of the
    folded matrix is indefinite at q: no sound certificate can cover a box through q.
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
    else:   # an explicit integer witness (used by the unit test of this formula)
        xi = np.asarray(witness, dtype=np.int64)
        w0 = float('nan')
    need(int(np.count_nonzero(xi)) > 1, f'degenerate probe witness at q={q}')
    sq = [F(int(v) ** 2) for v in xi]
    # x^T F x = sum_i D_i x_i^2 - sum_{i!=j} (a_|i-j| + a_{i+j+1}) x_i x_j with the diagonal
    # D_i = 2i+1 + 2A_i + 2mu[i<k] - a_{2i+1}; the -a_{2i+1} is cancelled exactly by the
    # i=j terms of the Hankel sum (a_0 = 0 for the difference part, so nothing is added
    # there), which is why the diagonal below omits it and no i=j correction is applied.
    diag = sum(sq[i] * ((2 * i + 1) + 2 * cum[i]) for i in range(nfold))
    # The mask term is the rank-one 2 mu on the whole k x k block, i.e. 2 mu (sum_{i<k} x_i)^2;
    # it is NOT 2 mu sum_{i<k} x_i^2 (that is only the diagonal of the block).
    mask = 2 * mu * F(int(sum(int(v) for v in xi[:k])) ** 2)
    corr = np.convolve(xi, xi[::-1])          # corr[nfold-1+r] = sum_i x_i x_{i+r}
    diff = sum(F(int(corr[nfold - 1 + r])) * a[abs(r)]
               for r in range(-(nfold - 1), nfold))
    cc = np.convolve(xi, xi)                  # cc[m] = sum_{i+j=m} x_i x_j
    hank = sum(F(int(cc[m])) * a[m + 1] for m in range(2 * nfold - 1))
    return diag - diff - hank + mask, w0, blk, xi


def pi_bounds():
    """Enclosure of pi from pi/4 = atan(1/2) + atan(1/3), not replay.py's 1/5,1/239 split.

    Both arctangents are alternating with decreasing terms, so the 90-term partial sum
    ending on a negative term is a lower bound and the next term x**181/181 bounds the
    remaining tail.  Using a different pair of series keeps the two pi enclosures (and
    hence the two C_E brackets) arithmetically independent.
    """
    def atan(x):
        lower = sum((-1) ** j * x ** (2 * j + 1) / (2 * j + 1) for j in range(90))
        return lower, lower + x ** 181 / 181
    a, b = atan(F(1, 2))
    c, d = atan(F(1, 3))
    return 4 * (a + c), 4 * (b + d)


def c_bounds(lam, left, right):
    """Directed enclosure of C_E = sqrt(q)/(2 pi sqrt(lam)) on q in [left,right]."""
    pl, ph = pi_bounds()
    digits = 10 ** 30

    def floor_sqrt(q, pi):
        s = digits ** 2 * q / (4 * lam * pi * pi)
        return isqrt(s.numerator // s.denominator)
    return F(floor_sqrt(left, ph), digits), F(1 + floor_sqrt(right, pl), digits)


def phonon_handoff():
    """Certified zero-Coulomb onset numerators (shared input data, C-LAMBDA/brackets.json)."""
    prior = json.loads((HERE.parent.parent / 'C-LAMBDA' / 'brackets.json').read_text(encoding='utf8'))
    out = {lam: prior['q_numerators'][lam] for lam in ('0.5', '1', '1.5', '2', '3', '4', '6', '10')}
    out.update({label.rsplit(':', 1)[1]: v for label, v in prior['ambient_q_numerators'].items()})
    return {lam: F(v[1], prior['q_denominator']) for lam, v in out.items()}


def run_case(data, handoff, receipt):
    lam, mu, scale2 = F(data['lambda']), F(data['mu']), F(data['R2'])
    low, high = map(F, data['einstein'])
    size_cold, size_hot = int(data['size_cold']), int(data['size_hot'])
    need(0 < low < high < handoff[data['lambda']], f'{data["name"]}: bad bracket')
    need(size_cold >= 100 and size_hot >= 100, f'{data["name"]}: degenerate claimed sizes')
    spec = ((F(1), F(1)),)

    val, ray = cold_value(lam, mu, low, scale2, spec)
    need(val < 0, f'Einstein cold sign {data["name"]}: form value {float(val):.6g} >= 0')
    print(f'{data["name"]:>10} cold Einstein: exact form value {float(val):.4g} < 0 '
          f'(float ray quotient {ray:.6g} > 1, {2 * NC} modes)', flush=True)

    start = high
    boxes = sum(cover(lambda l, r, k: positive(hot_head(lam, mu, l, r, scale2, spec)),
                      l, r, k)
                for l, r, k in windows(start, handoff[data['lambda']], scale2))
    print(f'{data["name"]:>10} hot Einstein positive on [{float(start):.6g}, '
          f'{float(handoff[data["lambda"]]):.6g}) in {boxes} certified boxes', flush=True)

    cl, ch = c_bounds(lam, low, high)
    receipt[data['name']] = {'einstein_q': [str(low), str(high)],
                             'einstein_C': [str(cl), str(ch)], 'boxes': boxes}
    print(f'{data["name"]:>10} C_E in [{float(cl):.10g}, {float(ch):.10g}]', flush=True)

    if 'mix' in data:
        mix = data['mix']
        good = spectrum_of(mix)
        spectrum = good
        q = F(mix['q'])
        need(q > high, f'{data["name"]}: mixture witness is not above the Einstein endpoint')
        need(q < handoff[data['lambda']], f'{data["name"]}: mixture witness above the handoff')
        val, ray = cold_value(lam, mu, q, scale2, spectrum, n=int(mix['size']))
        need(val < 0, f'mixture cold sign {data["name"]}: form value {float(val):.6g} >= 0')
        receipt[data['name']]['mix'] = {'spectrum': [[str(p), str(u)] for p, u in good],
                                        'q': str(q)}
        print(f'{data["name"]:>10} mixture: second moment of '
              f'{", ".join(f"{float(u):g}" for _, u in good)} is one, exact form value '
              f'{float(val):.4g} < 0 at q={q} (float ray quotient {ray:.6g})', flush=True)
        # The same q must sit inside the certified hot interval, and Einstein must not be
        # unstable there: the two-line verdict does not transfer.  This is the full-line
        # exact form on Einstein's own ray at the single point q, not the box cover.
        v_ein, ray_ein = cold_value(lam, mu, q, scale2, spec, n=int(mix['size']))
        need(v_ein >= 0, f'{data["name"]}: the Einstein form is negative on its own ray at '
                         f'the mixture witness q={q} (value {float(v_ein):.6g})')
        print(f'{data["name"]:>10} Einstein is stable at q={q} on its own ray (value '
              f'{float(v_ein):.4g} >= 0, ray quotient {ray_ein:.6g} <= 1) while the mixture '
              f'is unstable: the two-line verdict does not transfer')


def check_receipt(receipt, stored):
    need(set(receipt) == set(stored), 'bounds.json case set differs from the fixtures')
    for name, got in receipt.items():
        ref = stored[name]
        need(set(got) <= set(ref), f'{name}: unexpected receipt fields {sorted(got)}')
        need([F(x) for x in got['einstein_q']] == [F(x) for x in ref['einstein_q']],
             f'{name}: stored einstein_q differs from the fixture bracket')
        lo_q, hi_q = (F(x) for x in ref['einstein_q'])
        need(0 < lo_q < hi_q, f'{name}: stored einstein_q is not a positive bracket')
        lo, hi = F(ref['einstein_C'][0]), F(ref['einstein_C'][1])
        need(0 < lo < hi, f'{name}: stored C_E is not a positive bracket')
        mine_lo, mine_hi = F(got['einstein_C'][0]), F(got['einstein_C'][1])
        need(lo <= mine_lo and mine_hi <= hi, f'{name}: stored C_E bracket does not contain the '
             f'recomputed one [{mine_lo}, {mine_hi}] inside [{lo}, {hi}]')
        # The box count is the size of replay.py's certificate, not a mathematical claim:
        # the number of boxes depends on the tightness of the positivity test, so this
        # script checks only that both counts are positive integers.  replay.py pins its
        # own count exactly when it verifies the stored receipt.
        need(isinstance(ref['boxes'], int) and ref['boxes'] >= 1, f'{name}: bad box count')
        need(isinstance(got['boxes'], int) and got['boxes'] >= 1, f'{name}: own box count')
        if 'mix' in got:
            need('mix' in ref, f'{name}: stored receipt lost the mixture')
            need([(F(p), F(u)) for p, u in got['mix']['spectrum']]
                 == [(F(p), F(u)) for p, u in ref['mix']['spectrum']],
                 f'{name}: stored mixture spectrum differs')
            need(F(got['mix']['q']) == F(ref['mix']['q']), f'{name}: stored mixture q differs')
    print('bounds.json: every field (einstein_q, einstein_C, boxes, mix) agrees with the '
          'independent recomputation')


def adversarial():
    """Regression probes from REVIEW2.md R2-1/R2-2, run by `--adversarial` (exit 0 = pass).

    For each probe the exact folded-form value at q_bad is the control: a negative value
    proves that no sound method can certify a box through q_bad.  The corrected device
    must then refuse both the documented box (bounded cover, so the run is cheap) and the
    point-wide box at q_bad, where the rejected verifier returned CERTIFIED POSITIVE.
    """
    spec = ((F(1), F(1)),)
    for name, lam, mu, scale2, q_bad, lo, hi in ADVERSARIAL:
        need(lo < q_bad < hi, f'{name}: q_bad is not inside the documented box')
        val, wmin, blk, xi = folded_exact(lam, mu, q_bad, scale2, spec)
        # Cross-check of the exact correlation formula against the float contraction of the
        # same integers: they are the same bilinear form, so only float rounding separates
        # them.  This catches a missing or doubled term in the exact sum.
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
            return positive(hot_head(lam, mu, left, right, scale2, spec))
        need(not certified(test, lo, hi, cutoff(lo, scale2), [64]),
             f'{name}: the hot cover accepted [{float(lo):.9g}, {float(hi):.9g}) although '
             f'the folded form is negative at q={q_bad}')
        thin = F(1, 10 ** 12)
        need(not positive(hot_head(lam, mu, q_bad - thin, q_bad, scale2, spec)),
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
    (F(3), F(2), F(100), 125),
)


def exact_head(lam, q, scale2, spec, m):
    """Exact rational SC * (Einstein part of F) on the m x m head block.

    The Coulomb block +2 mu* 1_{i,j<k} is a constant (q-independent) matrix and is not
    included; the enclosure adds its floor to the same block, so the two offsets are
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


def selfcheck():
    """`--selfcheck`: verify the enclosure against EXACT rational head entries.

    Each window is evaluated at three interior q in exact rational arithmetic, which is
    independent of the rounded integers, and every head entry must satisfy
    lower <= SC*F_ij(q) <= upper, |SC*F_ij(q) - center_ij| <= radius_ij on the off-diagonal
    and center_ii <= SC*F_ii.  This is exactly the invariant REVIEW3 R3-1 broke by swapping
    lower and upper: on those bytes |value - centre| = radius + 1 on every odd bracket, so
    the check fails there and passes here.
    """
    entries = 0
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
        # The Coulomb block is added to the WHOLE k x k block of the centre; it is a
        # constant of the form, so remove it and check the Einstein part against the
        # bracket, then check the floored constant separately (it must be <= 2 mu* SC).
        offm = np.zeros((m, m), dtype=np.int64)
        if k:
            offm[:k, :k] = flr_(SC * 2 * mu)
            need(F(int(offm[0, 0])) <= SC * 2 * mu, 'selfcheck: Coulomb block not rounded down')
        base = center - offm
        # lower/upper bracket only the OFF-DIAGONAL entries; the diagonal is a one-sided
        # lower bound (2i+1 + 2A_i - a_{2i+1}) and carries radius 0.
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
    print(f'interval enclosure selfcheck: {len(SELFCHECK)} windows x 3 interior q, '
          f'{entries} exact rational entry comparisons against lower/upper/centre/radius: OK')


def mutant_path(kind, data, handoff):
    """Run one deliberate defect; every branch that survives the checks is a failure.

    Each mutant states its unmutated control first (exit 2 if the control breaks, which
    would invalidate the mutant) and then the perturbed statement, which must be refused
    (exit 1).  The two statements always concern the SAME object: the endpoint mutant uses
    the Einstein spectrum at both ends, the Coulomb mutant the mixture at its own witness q.
    """
    case = data['cases'][0]
    name = case['name']
    lam, mu, scale2 = F(case['lambda']), F(case['mu']), F(case['R2'])
    mix_spec = spectrum_of(case['mix'])
    ein_spec = ((F(1), F(1)),)
    low, high = map(F, case['einstein'])
    qm = F(case['mix']['q'])
    if kind == 'spectrum':
        # The mutant swaps the line weights p -> 1-p: the ordering 0 < u_lo < 1 < u_hi
        # survives, so only the second-moment guard can catch it.
        need(len(mix_spec) == 2, 'the true two-line mixture was refused')
        attack = dict(case['mix'], high_p=str(1 - F(case['mix']['high_p'])))
        try:
            spectrum_of(attack)
        except ValueError as exc:
            need('second moment' in str(exc),
                 f'the p -> 1-p mixture was refused for the wrong reason: {exc}')
        else:
            need(False, 'a mixture with the wrong second moment was accepted')
        refused('the p -> 1-p mixture (int u dp != 1) is refused by the second-moment guard')
    if kind == 'coulomb':
        # The mixture's instability at its own witness q needs the repulsion: doubling mu*
        # must remove the exact cold sign of the same witness.
        gate, _ = cold_value(lam, mu, qm, scale2, mix_spec)
        control(gate < 0, 'the unmutated mixture witness lost its sign at its own q')
        v, _ = cold_value(lam, 2 * mu, qm, scale2, mix_spec)
        if v >= 0:
            refused(f'doubling mu* removes the cold sign at q={qm} '
                    f'(form value {float(v):.6g} >= 0)')
        need(False, 'coulomb mutant: the cold mixture witness survives a doubled repulsion')
    # endpoint: the Einstein line is cold at q_lo (control) and the hot certificate, which
    # is valid exactly on [q_hi, q_ph), must refuse to cover [q_lo, q_ph).
    gate, _ = cold_value(lam, mu, low, scale2, ein_spec)
    control(gate < 0, 'the unmutated cold Einstein witness lost its sign at q_lo')

    def certify(left, right, k, depth=0):
        if positive(hot_head(lam, mu, left, right, scale2, ein_spec)):
            return 1
        need(depth < 22, f'hot interval cannot be certified: {float(left):.12g} '
                         f'{float(right):.12g} K={k}')
        mid = (left + right) / 2
        return certify(left, mid, k, depth + 1) + certify(mid, right, k, depth + 1)
    try:
        boxes = sum(certify(left, right, k)
                    for left, right, k in windows(low, handoff[case['lambda']], scale2))
    except ValueError as exc:
        need('cannot be certified' in str(exc),
             f'the hot certificate at q_lo failed for the wrong reason: {exc}')
        refused(f'the Einstein form is not positive on [q_lo, q_ph): {exc}')
    need(False, f'endpoint mutant: the interval below q_hi was certified in {boxes} boxes')


def main():
    parser = argparse.ArgumentParser(description=(__doc__ or '').splitlines()[0])
    parser.add_argument('--mutant', choices=('', 'endpoint', 'coulomb', 'spectrum', 'receipt'),
                        default='', help='deliberate defect, must be rejected')
    parser.add_argument('--adversarial', action='store_true',
                        help='regression probes from REVIEW2.md R2-1/R2-2: a box holding an '
                             'exactly negative folded form must be refused')
    parser.add_argument('--selfcheck', action='store_true',
                        help='verify the hot enclosure against exact rational values '
                             '(REVIEW3 R3-1 regression)')
    args = parser.parse_args()

    print(f'pinned a_1 checks: {a1_pin_check()} mixtures')
    if args.selfcheck:
        selfcheck()
        return 0
    if args.adversarial:
        adversarial()
        return 0
    data = json.loads((HERE / 'fixtures.json').read_text(encoding='utf8'))
    need(len(data['cases']) == 3, 'expected three counterexamples')
    handoff = phonon_handoff()
    stored = None
    if args.mutant != 'endpoint':
        stored = json.loads((HERE / 'bounds.json').read_text(encoding='utf8'))
    if args.mutant and args.mutant != 'receipt':
        mutant_path(args.mutant, data, handoff)
        need(False, f'{args.mutant} mutant: the perturbed statement was accepted')
    receipt = {}
    for case in data['cases'] + data['anchors']:
        run_case(case, handoff, receipt)
    if args.mutant == 'receipt':
        # shave the recomputed C_E lower bound: the stored bracket must fail to contain it
        entry = receipt['einstein-counterexample']
        entry['einstein_C'] = [str(F(entry['einstein_C'][0]) - F(1, 10 ** 6)),
                               entry['einstein_C'][1]]
    try:
        check_receipt(receipt, stored)
    except ValueError as exc:
        if args.mutant == 'receipt':
            refused(f'a shaved C_E bracket escaped the receipt check: {exc}')
        raise
    print('independent verification of the common-cutoff certificates: OK')
    return 0


if __name__ == '__main__':
    sys.exit(main())
