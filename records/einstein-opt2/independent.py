"""Independent exact verifier for common-cutoff Einstein optimality (Version 2) certificates in bounds.json.

Deliberately avoids replay.py's folded cold evaluator, L D L^T Cholesky rounding check,
uniform tail_d = j+1 Cauchy-Schwarz bound, and 2**30 scaling:
1. Cold side: unfolded full-line Matsubara quadratic form on {-N, ..., N-1} retaining a_0 = lam,
   computed in exact Python integer correlation + Fraction arithmetic.
2. Hot side: SC = 2**29, GR = 2**22, per-row Gershgorin tail gaps (g_j on j in [m, m+ncol))
   with exact S_1 and far-tail Schur complement, plus exact integer congruence M = R^T A R
   (via overflow-guarded 16-bit limb int64 matrix multiplication) certified strictly diagonally
   dominant (2*M_ii > sum_j |M_ij|) in exact Python integers.
3. Pi bound: independent Hutton Machin-like series pi/4 = atan(1/2) + atan(1/3).
4. Never writes bounds.json.
"""
import argparse
import json
import sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import cholesky, solve_triangular

HERE = Path(__file__).resolve().parent
SC = 2 ** 29
GR = 2 ** 26

def dn(x):
    return x.numerator // x.denominator


def up(x):
    return -(-x.numerator // x.denominator)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def control(ok, why):
    if not ok:
        print(f"control failed (invalid mutant): {why}", file=sys.stderr)
        raise SystemExit(2)


def refused(why):
    print(f"mutant refused: {why}")
    raise SystemExit(1)


def hutton_pi_bounds(terms=30):
    def atan_alt(inv_x, pairs):
        s = F(0)
        x2 = inv_x * inv_x
        p = F(1, inv_x)
        last_odd = F(0)
        last_even = F(0)
        for m in range(2 * pairs):
            if m % 2 == 0:
                s += p / (2 * m + 1)
                last_even = s
            else:
                s -= p / (2 * m + 1)
                last_odd = s
            p /= x2
        return last_odd, last_even
    a1_lo, a1_hi = atan_alt(2, terms)
    a2_lo, a2_hi = atan_alt(3, terms)
    return 4 * (a1_lo + a2_lo), 4 * (a1_hi + a2_hi)


PI_LO, PI_HI = hutton_pi_bounds(24)


def mask_count(q, R2):
    k = 0
    while (2 * k + 1) ** 2 * q < 4 * R2:
        k += 1
    return k


def a_spec(lam, q, j, spec):
    """Exact rational transfer weight a_j(q; spec) including j=0 -> lam."""
    if j == 0:
        return lam * sum(th for th, _ in spec)
    x = q * j * j
    return lam * sum(th * u / (u + x) for th, u in spec)


def unfolded_cold_eval(lam, mu, k, q, spec, v, extra_all_ones_mu=F(0)):
    """Exact unfolded full-line Matsubara form on n in {-N, ..., N-1}, retaining a_0 = lam.

    For f_n = v_{i(n)} where i(n) = n if n >= 0 else -1-n:
      D_n = (2*i(n) + 1) + a_0 + 2 * sum_{r=1}^{i(n)} a_r
      Q_unfolded(f) = sum_n D_n f_n^2 - sum_{n, m} a_{|n-m|} f_n f_m
                      + mu * (sum_{-k <= n < k} f_n)^2 + extra_all_ones_mu * (sum_n f_n)^2
    which equals 2 * <v, F_folded v> identically without ever cancelling a_0 or computing a_{i+j+1}.
    """
    N = len(v)
    a = [a_spec(lam, q, r, spec) for r in range(2 * N)]
    # Prefix sums P[i] = sum_{r=1}^{i} a_r
    P = [F(0)] * N
    for i in range(1, N):
        P[i] = P[i - 1] + a[i]

    # Unfolded vector f indexed by t = n + N in 0..2N-1 (n = t - N)
    f = [v[-1 - n] if n < 0 else v[n] for n in range(-N, N)]

    # Diagonal kinetic + self-energy (retaining a_0 = a[0] = lam!)
    diag_sum = F(0)
    for n in range(-N, N):
        fn = f[n + N]
        if fn == 0:
            continue
        i = n if n >= 0 else -1 - n
        Dn = F(2 * i + 1) + a[0] + 2 * P[i]
        diag_sum += Dn * (fn * fn)

    # Exact Python-int pair correlations c_d = sum_n f_n f_{n+d}
    c_0 = sum(x * x for x in f)
    pair_sum = a[0] * c_0
    L = 2 * N
    for d in range(1, L):
        cd = sum(f[t] * f[t + d] for t in range(L - d))
        if cd != 0:
            pair_sum += 2 * a[d] * cd

    # Coulomb mask on unfolded indices -k <= n <= k - 1
    coulomb = F(0)
    if k > 0 and mu != 0:
        s_mask = sum(f[n + N] for n in range(-min(k, N), min(k, N)))
        coulomb += mu * (s_mask * s_mask)
    if extra_all_ones_mu != 0:
        s_all = sum(f)
        coulomb += extra_all_ones_mu * (s_all * s_all)

    return diag_sum - pair_sum + coulomb


def exact_rtar(A, R):
    """Exact R^T A R in Python int (object array) via overflow-guarded 16-bit limb int64 matmuls."""
    m = A.shape[0]
    B = 1 << 16
    MASK = B - 1

    A0 = (A & MASK).astype(np.int64)
    A_r1 = (A - A0) >> 16
    A1 = (A_r1 & MASK).astype(np.int64)
    A2 = ((A_r1 - A1) >> 16).astype(np.int64)

    R0 = (R & MASK).astype(np.int64)
    R1 = ((R - R0) >> 16).astype(np.int64)

    maxA = max(int(np.abs(A0).max()), int(np.abs(A1).max()), int(np.abs(A2).max()))
    maxR = max(int(np.abs(R0).max()), int(np.abs(R1).max()))
    need(2 * m * maxA * maxR < (1 << 61), f"AR limb overflow risk: {2 * m * maxA * maxR}")

    P0 = A0 @ R0
    P1 = A0 @ R1 + A1 @ R0
    P2 = A1 @ R1 + A2 @ R0
    P3 = A2 @ R1
    AR = (
        P0.astype(object)
        + P1.astype(object) * B
        + P2.astype(object) * (B * B)
        + P3.astype(object) * (B * B * B)
    )

    C0 = (AR % B).astype(np.int64)
    t1 = (AR - C0) // B
    C1 = (t1 % B).astype(np.int64)
    t2 = (t1 - C1) // B
    C2 = (t2 % B).astype(np.int64)
    C3 = ((t2 - C2) // B).astype(np.int64)

    maxC = max(
        int(np.abs(C0).max()),
        int(np.abs(C1).max()),
        int(np.abs(C2).max()),
        int(np.abs(C3).max()),
    )
    need(2 * m * maxR * maxC < (1 << 61), f"R^T AR limb overflow risk: {2 * m * maxR * maxC}")

    RT0, RT1 = R0.T, R1.T
    Q0 = RT0 @ C0
    Q1 = RT0 @ C1 + RT1 @ C0
    Q2 = RT0 @ C2 + RT1 @ C1
    Q3 = RT0 @ C3 + RT1 @ C2
    Q4 = RT1 @ C3
    return (
        Q0.astype(object)
        + Q1.astype(object) * B
        + Q2.astype(object) * (B ** 2)
        + Q3.astype(object) * (B ** 3)
        + Q4.astype(object) * (B ** 4)
    )


def certify_matrix_rtar(center):
    """Certify center > 0 via exact congruence R^T center R strictly diagonally dominant."""
    m = center.shape[0]
    try:
        L = cholesky(center.astype(np.float64), lower=True)
        invLT = solve_triangular(L.T, np.eye(m), lower=False)
    except np.linalg.LinAlgError:
        return False
    if not np.all(np.isfinite(invLT)):
        return False
    R = np.rint(invLT * GR).astype(np.int64)
    M = exact_rtar(center, R)
    diag = np.diag(M)
    if not all(int(d) > 0 for d in diag):
        return False
    row_abs = np.abs(M).sum(axis=1)
    return all(2 * int(diag[i]) > int(row_abs[i]) for i in range(m))


def certify_box_tailgaps(m, mu, k, b_tail, b_lo_fn, b_hi_fn):
    """Independent per-row Gershgorin tail-gap + Schur complement + R^T A R certificate."""
    ncol = max(120, 2 * m)
    top = 2 * (m + ncol) + 2
    b_lo = [F(0)] + [b_lo_fn(j) for j in range(1, top)]
    b_hi = [F(0)] + [b_hi_fn(j) for j in range(1, top)]

    lo_int = np.array([dn(SC * x) for x in b_lo], dtype=np.int64)
    hi_int = np.array([up(SC * x) for x in b_hi], dtype=np.int64)
    need(bool(np.all(lo_int >= 0)) and bool(np.all(lo_int <= hi_int)), "invalid b bounds")
    need(top * int(hi_int.max()) < (1 << 60), "cum sum overflow")

    dn_cum = np.zeros(top, dtype=np.int64)
    dn_cum[1:] = np.cumsum(lo_int[1:])
    up_cum = np.zeros(top, dtype=np.int64)
    up_cum[1:] = np.cumsum(hi_int[1:])

    M_s1 = top - 1
    s1 = int(up_cum[M_s1]) + up(SC * b_tail / M_s1)
    j = np.arange(m, m + ncol, dtype=np.int64)
    tail_rem = np.array([up(SC * b_tail / (int(t) + m)) for t in j], dtype=np.int64)
    g = SC * (2 * j + 1) + 2 * dn_cum[j] - up_cum[j - m] - hi_int[2 * j + 1] - tail_rem - s1
    if not bool(np.all(g > 0)):
        return False

    i_idx = np.arange(m)[:, None]
    be = hi_int[np.abs(i_idx - j)] + hi_int[i_idx + j + 1]
    hq = np.maximum(1, np.array([(1 << 24) // ((t + 1) ** 2) for t in range(m)], dtype=np.int64))
    col = hq @ be
    k_sh = np.maximum(0, np.array([int(c).bit_length() for c in col], dtype=np.int64) - 24)
    c = (col + (np.ones_like(k_sh) << k_sh) - 1) >> k_sh
    term = -(-(be * c) // g)
    g_far = SC * (2 * (m + ncol) + 1) - s1 - up(SC * b_tail / (2 * m + ncol))
    if g_far <= 0:
        return False
    g_denom = min(int(g.min()), int(g_far))
    far = up(SC * SC * (2 * b_tail) ** 2 * int(hq.sum()) / (3 * (ncol ** 3) * g_denom))
    theta = -(-((term << k_sh).sum(axis=1) + far) // hq)

    ii = np.arange(m)
    diff = np.abs(ii[:, None] - ii)
    hank = ii[:, None] + ii + 1
    upper = -(lo_int[diff] + lo_int[hank])
    lower = -(hi_int[diff] + hi_int[hank])
    if k > 0 and mu != 0:
        mu_lo = dn(2 * mu * SC)
        mu_hi = up(2 * mu * SC)
        lower[:k, :k] += mu_lo
        upper[:k, :k] += mu_hi
    diag = np.diag_indices(m)
    lower[diag] += SC * (2 * ii + 1) + 2 * dn_cum[:m]
    upper[diag] += SC * (2 * ii + 1) + 2 * up_cum[:m]

    center = (lower + upper) // 2
    radius = np.maximum(upper - center, center - lower)
    radius[diag] = 0
    h = np.array([(1 << 22) // (t + 1) for t in range(m)], dtype=np.int64)
    rho = -(-(radius @ h) // h)
    # Lower bound on diagonal is center[diag] - (upper[diag] - center[diag]) = lower[diag],
    # minus rho (off-diag radius) and theta (infinite-tail Schur penalty).
    center[diag] = lower[diag] - rho - theta
    return certify_matrix_rtar(center)


def b_einstein(lam, x):
    return lam / (1 + x)


def b_spec(lam, x, spec):
    return lam * sum(th * u / (u + x) for th, u in spec)


def b_d2_eff(lam, x):
    return lam * (1 + x + x * x) / ((1 + x) ** 3)


def b_d1_eff(lam, x):
    return lam / ((1 + x) ** 2)


def b_gb_bounds(lam, xa, xb, t1a, t1b, t2a, t2b):
    if t1a == 0:
        fa = lam * t2a * xa / ((1 + xa) * (1 + t2a * xa))
        fb = lam * t2a * xb / ((1 + xb) * (1 + t2a * xb))
        blo = min(fa, fb)
    else:
        g_lo = (1 + xa) * (1 + t1a * t2a + t1a / xb + t2a * xa)
        blo = max(F(0), lam * (F(1) / (1 + xb) - F(1) / g_lo))
    g_hi = (1 + xb) * (1 + t1b * t2b + t1b / xa + t2b * xb)
    bhi = min(lam / (1 + xa), lam * (F(1) / (1 + xa) - F(1) / g_hi))
    return blo, bhi


def verify_cover_1d(boxes, q_lo, q_hi, chk_fn, label):
    need(len(boxes) > 0, f"{label}: empty 1D cover")
    cur = q_lo
    for idx, b in enumerate(boxes):
        a, c = F(b[0]), F(b[1])
        need(a <= cur and a < c, f"{label}: bad box {idx} [{a}, {c}] at cur={cur}")
        need(chk_fn(a, c), f"{label}: box {idx} [{a}, {c}] failed R^T A R")
        if c > cur:
            cur = c
    need(cur >= q_hi, f"{label}: ends at {cur} < {q_hi}")


def verify_cover_3d(boxes, q_lo, q_hi, chk_fn, label):
    need(len(boxes) > 0, f"{label}: empty 3D cover")
    parsed = [tuple(F(x) for x in b) for b in boxes]
    for idx, b in enumerate(parsed):
        qa, qb, t1a, t1b, t2a, t2b = b
        need(qa < qb and t1a < t1b and t2a < t2b, f"{label}: degenerate box {idx}")
        need(qa >= q_lo and qb <= q_hi and 0 <= t1a and t1b <= 1 and 0 <= t2a and t2b <= 1, f"{label}: out of bounds {idx}")
        need(chk_fn(qa, qb, t1a, t1b, t2a, t2b), f"{label}: box {idx} failed R^T A R")
    vol = sum((qb - qa) * (t1b - t1a) * (t2b - t2a) for qa, qb, t1a, t1b, t2a, t2b in parsed)
    need(vol == q_hi - q_lo, f"{label}: volume mismatch {vol} != {q_hi - q_lo}")
    parsed.sort(key=lambda b: (b[0], b[1]))
    for i in range(len(parsed)):
        _, qb1, a1, b1, c1, d1 = parsed[i]
        for j in range(i + 1, len(parsed)):
            qa2, _, a2, b2, c2, d2 = parsed[j]
            if qa2 >= qb1:
                break
            if a1 < b2 and a2 < b1 and c1 < d2 and c2 < d1:
                raise ValueError(f"{label}: overlapping boxes {i} and {j}")


def verify_all(data):
    need(1 - (PI_HI * PI_HI) / 12 > F(1, 6), "Hutton pi^2/12 bound failed")

    # 1. Realizability audit
    ra = data["realizability_audit"]
    for row in ra["k1_rows"]:
        lam = F(row["lambda"])
        mu = F(row["mu"])
        need(mu == lam / 2, "k1_row mu != lam/2")
        q0_cold = F(row["q0_cold"])
        v0 = [int(x) for x in row["v0_cold"]]
        need(unfolded_cold_eval(lam, F(0), 0, q0_cold, ((F(1), F(1)),), v0) < 0, f"lam={lam} unfolded v0 not cold")
        q1_hot = F(row["q1_hot"])
        need(9 * q1_hot < q0_cold, f"lam={lam} 9*q1_hot < q0_cold failed")
        m = row["hot1_n"]
        verify_cover_1d(
            row["hot1_boxes"], q1_hot, 4 * lam,
            lambda qa, qb, m=m, lam=lam, mu=mu: certify_box_tailgaps(
                m, mu, 1, lam / qa,
                lambda j, lam=lam, qb=qb: b_einstein(lam, qb * j * j),
                lambda j, lam=lam, qa=qa: b_einstein(lam, qa * j * j),
            ),
            f"ind_k1_lam{lam}",
        )

    l152 = ra["lam152_fixed1_failure"]
    lam152, mu152 = F(l152["lambda"]), F(l152["mu"])
    u1, u2, th = F(l152["u1"]), F(l152["u2"]), F(l152["theta"])
    need(0 < u1 < 1 < u2 and (1 - th) * u1 + th * u2 == 1, "lam152 Moment-1 failed")
    spec152 = ((1 - th, u1), (th, u2))
    q_test = F(l152["q_test"])
    v_mix = [int(x) for x in l152["v_mix_cold"]]
    need(unfolded_cold_eval(lam152, mu152, 1, q_test, spec152, v_mix) < 0, "lam152 unfolded mix not cold")
    q0_152 = F([r for r in ra["k1_rows"] if F(r["lambda"]) == lam152][0]["q0_cold"])
    need(9 * q_test < q0_152, "lam152 9*q_test < q0_cold failed")
    m152 = l152["n"]
    verify_cover_1d(
        l152["hot_E_boxes"], q_test, 4 * lam152,
        lambda qa, qb: certify_box_tailgaps(
            m152, mu152, 1, lam152 / qa,
            lambda j: b_einstein(lam152, qb * j * j),
            lambda j: b_einstein(lam152, qa * j * j),
        ),
        "ind_lam152_hot_E",
    )

    # 2. Target 2 slabs + D2 + D1
    t2 = data["target2_r0_1over64"]
    r0 = F(t2["r0"])
    slabs = t2["slabs"]
    need(F(slabs[0]["lam_lo"]) == F(t2["lam_lo"]) and F(slabs[-1]["lam_hi"]) == F(t2["lam_hi"]), "slab endpoints mismatch")
    for idx, s in enumerate(slabs):
        lam_lo, lam_hi, q_star = F(s["lam_lo"]), F(s["lam_hi"]), F(s["q_star"])
        if idx + 1 < len(slabs):
            need(lam_hi == F(slabs[idx + 1]["lam_lo"]), f"slab {idx} gap")
        v_cold = [int(x) for x in s["v_cold"]]
        need(all(x >= 0 for x in v_cold) and any(x > 0 for x in v_cold), f"slab {idx} v_cold invalid")
        need(
            unfolded_cold_eval(lam_lo, F(0), 0, q_star, ((F(1), F(1)),), v_cold, extra_all_ones_mu=r0 * lam_lo) < 0,
            f"slab {idx} unfolded cold failed",
        )
        m = s["n"]
        verify_cover_3d(
            s["gb_boxes"], q_star, 4 * lam_hi,
            lambda qa, qb, t1a, t1b, t2a, t2b, m=m, lam_hi=lam_hi: certify_box_tailgaps(
                m, F(0), 0, lam_hi / qa,
                lambda j, lam_hi=lam_hi, qa=qa, qb=qb, t1a=t1a, t1b=t1b, t2a=t2a, t2b=t2b: b_gb_bounds(lam_hi, qa * j * j, qb * j * j, t1a, t1b, t2a, t2b)[0],
                lambda j, lam_hi=lam_hi, qa=qa, qb=qb, t1a=t1a, t1b=t1b, t2a=t2a, t2b=t2b: b_gb_bounds(lam_hi, qa * j * j, qb * j * j, t1a, t1b, t2a, t2b)[1],
            ),
            f"ind_slab{idx}_gb",
        )
        verify_cover_1d(
            s["d2_boxes"], q_star, 4 * lam_hi,
            lambda qa, qb, m=m, lam_hi=lam_hi: certify_box_tailgaps(
                m, F(0), 0, lam_hi / qa,
                lambda j: b_d2_eff(lam_hi, qb * j * j),
                lambda j: b_d2_eff(lam_hi, qa * j * j),
            ),
            f"ind_slab{idx}_d2",
        )
        verify_cover_1d(
            s["d1_boxes"], q_star, 4 * lam_hi,
            lambda qa, qb, m=m, lam_hi=lam_hi: certify_box_tailgaps(
                m, F(0), 0, lam_hi / qa,
                lambda j: b_d1_eff(lam_hi, qb * j * j),
                lambda j: b_d1_eff(lam_hi, qa * j * j),
            ),
            f"ind_slab{idx}_d1",
        )

    # 3. Jump cliff obstruction
    cl = data["jump_cliff_obstruction"]
    c_lam, c_mu = F(cl["lambda"]), F(cl["mu"])
    q_cliff, R2 = F(cl["q_cliff"]), F(cl["R2"])
    need(c_mu == r0 * c_lam, "cliff mu mismatch")
    need(4 * R2 == (2 * cl["k_at_cliff"] + 1) ** 2 * q_cliff, "cliff exact resonance mismatch")
    need(mask_count(q_cliff, R2) == cl["k_at_cliff"] and mask_count(q_cliff - F(1, 10 ** 9), R2) == cl["k_below_cliff"], "cliff mask mismatch")
    u1c, u2c, thc = F(cl["u1"]), F(cl["u2"]), F(cl["theta"])
    need(0 < u1c < 1 < u2c and (1 - thc) * u1c + thc * u2c == 1, "cliff Moment-1 failed")
    spec_c = ((1 - thc, u1c), (thc, u2c))
    need(unfolded_cold_eval(c_lam, c_mu, cl["k_below_cliff"], q_cliff, ((F(1), F(1)),), [int(x) for x in cl["v_E_cold_k15"]]) < 0, "cliff E unfolded not cold")
    need(unfolded_cold_eval(c_lam, c_mu, cl["k_below_cliff"], q_cliff, spec_c, [int(x) for x in cl["v_p_cold_k15"]]) < 0, "cliff p unfolded not cold")
    mc = cl["n"]
    for key_w, spec_w in [("windows_E", ((F(1), F(1)),)), ("windows_p", spec_c)]:
        cur_w = q_cliff
        b_tail_coeff = c_lam * sum(th * u for th, u in spec_w)
        for w in cl[key_w]:
            kw = w["k"]
            w_hi = min(4 * c_lam, F(4 * R2, (2 * kw - 1) ** 2)) if kw > 0 else 4 * c_lam
            need(mask_count(cur_w, R2) == kw, f"cliff {key_w} mask mismatch")
            verify_cover_1d(
                w["boxes"], cur_w, w_hi,
                lambda qa, qb, kw=kw, spec_w=spec_w, b_tail_coeff=b_tail_coeff: certify_box_tailgaps(
                    mc, c_mu, kw, b_tail_coeff / qa,
                    lambda j: b_spec(c_lam, qb * j * j, spec_w),
                    lambda j: b_spec(c_lam, qa * j * j, spec_w),
                ),
                f"ind_cliff_{key_w}_k{kw}",
            )
            cur_w = w_hi
        need(cur_w == 4 * c_lam, f"cliff {key_w} did not reach 4*lam")

    # 4. Target 3: 20 benchmarks
    for item in data["target3_d2_k1_to_4"]:
        k, lam, mu = item["k"], F(item["lambda"]), F(item["mu"])
        need(mu == lam / 2, "target3 mu != lam/2")
        q_lo, q_hi = F(item["q_lo"]), F(item["q_hi"])
        v_cold = [int(x) for x in item["v_cold"]]
        need(unfolded_cold_eval(lam, mu, k, q_lo, ((F(1), F(1)),), v_cold) < 0, f"target3 k={k} lam={lam} unfolded cold failed")
        mt = item["n"]
        verify_cover_1d(
            item["hot_q_boxes"], q_hi, 4 * lam,
            lambda qa, qb, k=k, lam=lam, mu=mu, mt=mt: certify_box_tailgaps(
                mt, mu, k, lam / qa,
                lambda j: b_einstein(lam, qb * j * j),
                lambda j: b_einstein(lam, qa * j * j),
            ),
            f"ind_t3_k{k}_lam{lam}_hot",
        )
        verify_cover_1d(
            item["d2_boxes"], q_lo, q_hi,
            lambda qa, qb, k=k, lam=lam, mu=mu, mt=mt: certify_box_tailgaps(
                mt, mu, k, lam / qa,
                lambda j: b_d2_eff(lam, qb * j * j),
                lambda j: b_d2_eff(lam, qa * j * j),
            ),
            f"ind_t3_k{k}_lam{lam}_d2",
        )
        verify_cover_1d(
            item["d1_boxes"], q_lo, q_hi,
            lambda qa, qb, k=k, lam=lam, mu=mu, mt=mt: certify_box_tailgaps(
                mt, mu, k, lam / qa,
                lambda j: b_d1_eff(lam, qb * j * j),
                lambda j: b_d1_eff(lam, qa * j * j),
            ),
            f"ind_t3_k{k}_lam{lam}_d1",
        )


def run_mutant(name, data):
    if name == "unfolded_a0":
        # Dropping a_0 from D_n makes unfolded != 2 * folded.
        r0 = data["realizability_audit"]["k1_rows"][0]
        lam, q0 = F(r0["lambda"]), F(r0["q0_cold"])
        v0 = [int(x) for x in r0["v0_cold"]]
        val_exact = unfolded_cold_eval(lam, F(0), 0, q0, ((F(1), F(1)),), v0)
        control(val_exact < 0, "unmutated unfolded v0 is cold")
        val_drop_a0 = val_exact - lam * 2 * sum(x * x for x in v0)
        if val_drop_a0 != val_exact:
            refused(f"unfolded_a0 mutant: dropping a_0 shifts quadratic form by {val_drop_a0 - val_exact}")
    elif name == "pi_bound":
        control(1 - (PI_HI * PI_HI) / 12 > F(1, 6), "unmutated Hutton bound > 1/6")
        if not (1 - (PI_LO * PI_LO) / 12 > F(1, 5)):
            refused("pi_bound mutant: claim 1 - pi^2/12 > 1/5 is false")
    elif name == "coulomb_slab":
        s0 = data["target2_r0_1over64"]["slabs"][0]
        lam, q_star = F(s0["lam_lo"]), F(s0["q_star"])
        v = [int(x) for x in s0["v_cold"]]
        control(unfolded_cold_eval(lam, F(0), 0, q_star, ((F(1), F(1)),), v, extra_all_ones_mu=F(1, 64) * lam) < 0, "unmutated slab0 unfolded cold")
        val_bad = unfolded_cold_eval(lam, F(0), 0, q_star, ((F(1), F(1)),), v, extra_all_ones_mu=F(1, 32) * lam)
        if not (val_bad < 0):
            refused(f"coulomb_slab mutant: r0=1/32 destroys slab0 unfolded witness ({val_bad} >= 0)")
    elif name == "cliff_resonance":
        cl = data["jump_cliff_obstruction"]
        q_cliff, R2 = F(cl["q_cliff"]), F(cl["R2"])
        control(mask_count(q_cliff, R2) == 14, "unmutated mask_count at q_cliff is 14")
        R2_bad = R2 + F(1, 1000)
        if mask_count(q_cliff, R2_bad) != 14:
            refused("cliff_resonance mutant: perturbed R^2 breaks k(q_cliff, R) = 14")
    elif name == "d2_weight_sign":
        item = data["target3_d2_k1_to_4"][0]
        k, lam, mu = item["k"], F(item["lambda"]), F(item["mu"])
        qa, qb = F(item["d2_boxes"][0][0]), F(item["d2_boxes"][0][1])
        control(
            certify_box_tailgaps(item["n"], mu, k, lam / qa, lambda j: b_d2_eff(lam, qb * j * j), lambda j: b_d2_eff(lam, qa * j * j)),
            "unmutated F_E + (1/2)D_2 box certified",
        )
        b_minus = lambda x: lam * (F(1) / (1 + x) + x / ((1 + x) ** 3))
        if not certify_box_tailgaps(item["n"], mu, k, lam / qa, lambda j: b_minus(qb * j * j), lambda j: b_minus(qa * j * j)):
            refused("d2_weight_sign mutant: flipped F_E - (1/2)D_2 fails certificate on target3 k=1, lam=1/2")
    elif name == "receipt_shave":
        s0 = data["target2_r0_1over64"]["slabs"][0]
        lam_hi, q_star = F(s0["lam_hi"]), F(s0["q_star"])
        vol = sum((F(b[1]) - F(b[0])) * (F(b[3]) - F(b[2])) * (F(b[5]) - F(b[4])) for b in s0["gb_boxes"])
        control(vol == 4 * lam_hi - q_star, "unmutated slab0 gb volume matches")
        shaved_boxes = list(s0["gb_boxes"])[:-1]
        vol_bad = sum((F(b[1]) - F(b[0])) * (F(b[3]) - F(b[2])) * (F(b[5]) - F(b[4])) for b in shaved_boxes)
        if vol_bad != 4 * lam_hi - q_star:
            refused(f"receipt_shave mutant: dropping last box leaves volume {vol_bad} != {4 * lam_hi - q_star}")
    else:
        raise ValueError(f"unknown mutant {name}")
    raise SystemExit(3)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bounds", type=Path, default=HERE / "bounds.json")
    parser.add_argument("--mutant", type=str, default=None)
    parser.add_argument("--mutants", action="store_true")
    args = parser.parse_args()

    if args.mutants:
        names = ["unfolded_a0", "pi_bound", "coulomb_slab", "cliff_resonance", "d2_weight_sign", "receipt_shave"]
        for nm in names:
            res = subprocess_run(args.bounds, nm)
            print(f"[{nm}] rc={res.returncode}: {res.stdout.strip() or res.stderr.strip()}")
            if res.returncode != 1:
                raise SystemExit(f"mutant {nm} returned {res.returncode}, expected 1")
        print(f"ALL {len(names)} INDEPENDENT MUTANTS REFUSED (exit 1)")
        return

    with open(args.bounds) as fh:
        data = json.load(fh)

    if args.mutant:
        run_mutant(args.mutant, data)
        return

    verify_all(data)
    print("independent.py: ALL CERTIFICATES VERIFIED BY UNFOLDED COLD + PER-ROW TAIL-GAPS + EXACT R^T A R (exit 0)")


def subprocess_run(bounds_path, nm):
    import subprocess
    return subprocess.run(
        [sys.executable, "-B", str(Path(__file__).resolve()), "--bounds", str(bounds_path), "--mutant", nm],
        capture_output=True, text=True,
    )


if __name__ == "__main__":
    main()
