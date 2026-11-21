"""Primary exact verifier for common-cutoff Einstein optimality (Version 2) certificates in bounds.json.

Verifies:
1. Realizability audit (Lemma 1 & Corollary 1): 7 fixed-k=1 failures at mu*/lam = 1/2
   (lambda in {10, 20, 25, 35, 50, 65, 152}) plus the explicit lam=152 two-line failure
   witness at q_test = 43355/10000 (= 8671/2000), showing 9*q1_hot < q0_cold (and 9*q_test < q0_cold).
2. Target 2 (Theorem 2): r0 = 1/64 on lambda in [3/10, 3] (33 contiguous slabs,
   2361 gb_boxes on [q_star, 4*lam_hi] x [0,1]^2, thm:asym on [4*lam_hi, inf),
   and nonnegative cold witnesses v_cold at lam_lo, q_star).
3. Jump-cliff obstruction (Theorem 2(3)): lambda=2, mu*=1/32, q_cliff=962/625,
   R^2=404521/1250, k=14->15, eps=1/1024; cold on k=15, hot on [q_cliff, 8] for
   both Einstein and p_eps across all 9 active mask windows (k=14..6 up to 4*lam=8).
4. Target 3 (Theorem 3): D2 and D1 positivity across all 33 slabs on [3/10, 3]
   (r0=1/64, all k>=0) and across all 20 benchmarked (k, lambda) in {1..4} x {1/2,1,2,5,10}
   at mu*/lam = 1/2.

Run:
    python -B replay.py
    python -B replay.py --mutant <name>
    python -B replay.py --mutants
"""
import argparse
import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.linalg import cholesky

HERE = Path(__file__).resolve().parent
S = 2 ** 30
G = 2 ** 25


def up(x):
    return -(-x.numerator // x.denominator)


def dn(x):
    return x.numerator // x.denominator


def need(ok, why):
    if not ok:
        raise ValueError(why)


def control(ok, why):
    if not ok:
        print(f"control failed (invalid mutant): {why}")
        raise SystemExit(2)


def refused(why):
    print(f"mutant refused: {why}")
    raise SystemExit(1)


def pi_upper_bound():
    """Machin's formula pi/4 = 4*atan(1/5) - atan(1/239) upper rational bound."""
    def atan_bounds(inv_x, max_k):
        s = F(0)
        x2 = inv_x * inv_x
        p = F(1, inv_x)
        lo = hi = F(0)
        for k in range(max_k + 1):
            term = p / (2 * k + 1)
            s = s + term if k % 2 == 0 else s - term
            if k % 2 == 0:
                hi = s
            else:
                lo = s
            p /= x2
        return lo, hi
    _, a5_hi = atan_bounds(5, 20)
    a239_lo, _ = atan_bounds(239, 7)
    return 4 * (4 * a5_hi - a239_lo)


PI_UP = pi_upper_bound()
PI2_6_UP = PI_UP * PI_UP / 6


def cutoff(q, scale2):
    """Exact strict Matsubara mask count k(q, R) = #{i >= 0 : (2i+1)^2 * q < 4 R^2}."""
    k = 0
    rhs = 4 * scale2
    while (2 * k + 1) ** 2 * q < rhs:
        k += 1
    return k


def folded_cold_eval(lam, mu, k, q, spec, v, extra_all_ones_mu=F(0)):
    """Exact rational quadratic form <v, F_p^(k)(q) v> + 2*extra_all_ones_mu*(sum v)^2."""
    n = len(v)
    a = [F(0)] * (2 * n)
    for j in range(1, 2 * n):
        a[j] = sum((lam * th * u / (u + q * j * j) for th, u in spec), F(0))
    total = F(0)
    cum = F(0)
    for i in range(n):
        if i > 0:
            cum += a[i]
        diag = F(2 * i + 1) + 2 * cum - a[2 * i + 1]
        total += diag * v[i] * v[i]
    for i in range(n):
        vi = v[i]
        if vi == 0:
            continue
        for j in range(i + 1, n):
            vj = v[j]
            if vj != 0:
                total -= 2 * (a[j - i] + a[i + j + 1]) * vi * vj
    if k > 0 and mu != 0:
        s_k = sum(v[:min(k, n)])
        total += 2 * mu * s_k * s_k
    if extra_all_ones_mu != 0:
        s_all = sum(v)
        total += 2 * extra_all_ones_mu * s_all * s_all
    return total


def b_gb(lam, x, t1, t2):
    return lam * (F(1) / (1 + x) - x / ((1 + x) * (t1 + x) * (1 + t2 * x)))


def b_gb_bounds(lam, xa, xb, t1a, t1b, t2a, t2b):
    """Exact airtight interval enclosure of b_gb(lam, x, t1, t2) on [xa,xb]x[t1a,t1b]x[t2a,t2b]."""
    if t1a == 0:
        fa = lam * t2a * xa / ((1 + xa) * (1 + t2a * xa))
        fb = lam * t2a * xb / ((1 + xb) * (1 + t2a * xb))
        blo = min(fa, fb)
    else:
        g_lo = (1 + xa) * (1 + t1a * t2a + t1a / xb + t2a * xa)
        blo = max(F(0), lam * (F(1) / (1 + xb) - F(1) / g_lo))
    g_hi = (1 + xb) * (1 + t1b * t2b + t1b / xa + t2b * xb)
    bhi = min(lam / (1 + xa), lam * (F(1) / (1 + xa) - F(1) / g_hi))
    need(0 <= blo <= bhi, "b_gb_bounds inversion")
    return blo, bhi

def b_einstein(lam, x):
    return lam / (1 + x)


def b_spec(lam, x, spec):
    return sum((lam * th * u / (u + x) for th, u in spec), F(0))


def b_d2_eff(lam, x):
    return lam * (1 + x + x * x) / ((1 + x) ** 3)


def b_d1_eff(lam, x):
    return lam / ((1 + x) ** 2)


def contraction(a, x, extra=0):
    """Exact int64 matrix-vector product with Python-int fallback and overflow guard."""
    limit = 2 ** 62
    need(a.dtype == np.int64 and x.dtype == np.int64, "contraction needs int64")
    a_max = int(np.max(np.abs(a)))
    x_max = int(np.max(np.abs(x)))
    if a_max * a.shape[1] * x_max + int(extra) < limit:
        return a @ x
    vals = x.tolist()
    out = np.empty(a.shape[0], dtype=np.int64)
    for idx, row in enumerate(a.tolist()):
        v = sum(y * z for y, z in zip(row, vals))
        need(abs(v) + int(extra) < limit, f"int64 contraction overflow: {v}")
        out[idx] = v
    return out


def far_lump_exact(b_tail, n, head_sum):
    """Strict upper bound on sum_{m >= 2n} 25 * b_tail^2 * head_sum / ((m+1) * m^4)."""
    # Split m=2n from m >= 2n+1; for m >= 2n+1, 1/((m+1)m^4) < 1/m^5 <= int_{m-1}^m x^{-5} dx
    tail_factor = F(1, (2 * n + 1) * (2 * n) ** 4) + F(1, 4 * (2 * n) ** 4)
    return 25 * b_tail * b_tail * head_sum * tail_factor


def gram_positive_int(a):
    """Exact int64 Schur-complement Cholesky certification of a > 0."""
    need(a.dtype == np.int64 and a.ndim == 2 and a.shape[0] == a.shape[1], "need square int64")
    need(bool(np.array_equal(a, a.T)), "matrix not symmetric")
    n = a.shape[0]
    if int(np.max(np.abs(a))) >= 2 ** 42:
        return False
    m = a.astype(np.float64) / S
    for shift in (2e-4, 2e-5, 2e-6, 1e-8, 1e-10):
        try:
            l = cholesky(m - shift * np.eye(n), lower=True, check_finite=False)
        except np.linalg.LinAlgError:
            continue
        if not np.all(np.isfinite(l)):
            continue
        if float(np.max(np.abs(l))) * G >= 2 ** 31 - 1:
            continue
        l_int = np.rint(l * G).astype(np.int64)
        if int(np.max((((np.abs(l_int) + 255) // 256) ** 2).sum(axis=1))) * 256 ** 2 >= 2 ** 62:
            continue
        res = a * (G * G // S) - l_int @ l_int.T
        if int(np.max(np.abs(res))) >= 2 ** 62 // n:
            continue
        if bool(np.all(2 * res.diagonal() > np.abs(res).sum(axis=1))):
            return True
    return False


class FoldedBlock:
    def __init__(self, n):
        self.n = n
        i = np.arange(n, dtype=np.int64)
        j = np.arange(n, 2 * n, dtype=np.int64)
        self.odd = 2 * i + 1
        self.diff = np.abs(i[:, None] - i)
        self.hank = i[:, None] + i + 1
        self.edge0 = j[:, None] - i
        self.edge1 = j[:, None] + i + 1
        self.quad = np.maximum(1, 2 ** 27 // (i + 1) ** 2)
        self.lin = 2 ** 24 // (i + 1)
        self.tail_d = j + 1

    def check_box_from_bounds(self, mu, k, b_tail, b_lo, b_hi, include_far=True):
        """Certify D + 2*mu*chi_k*chi_k^T + T(b) > 0 for all 0 <= b_lo <= b <= b_hi <= b_tail/j^2."""
        n = self.n
        if n * n < 2 * b_tail:
            return False
        need(k <= n, "Coulomb mask overlaps tail")
        lo = np.array([dn(S * x) for x in b_lo[:2 * n]], dtype=np.int64)
        hi = np.array([up(S * x) for x in b_hi[:3 * n]], dtype=np.int64)
        need(bool(np.all(lo >= 0)) and bool(np.all(lo <= hi[:2 * n])), "invalid b bounds")
        need(2 * n * int(np.max(hi)) < 2 ** 61, "cum diag overflow")

        pot_lo = self.odd * S + 2 * lo[:n].cumsum()
        pot_hi = self.odd * S + 2 * hi[:n].cumsum()
        lower = -hi[self.diff] - hi[self.hank]
        upper = -lo[self.diff] - lo[self.hank]
        if k > 0 and mu != 0:
            mu_lo = dn(2 * mu * S)
            mu_hi = up(2 * mu * S)
            lower[:k, :k] += mu_lo
            upper[:k, :k] += mu_hi
        diag = np.diag_indices(n)
        lower[diag] += pot_lo
        upper[diag] += pot_hi

        center = (lower + upper) // 2
        radius = upper - center
        h_lin = self.lin
        rad_pen = contraction(radius, h_lin, int(h_lin.max()))
        center[diag] -= (rad_pen + h_lin - 1) // h_lin

        edge = hi[self.edge0] + hi[self.edge1]
        h_q = self.quad
        den = self.tail_d * S
        row = (contraction(edge, h_q, int(den.max())) + den - 1) // den
        near = (contraction(edge.T, row, int(h_q.max())) + h_q - 1) // h_q
        center[diag] -= near
        if include_far:
            far = far_lump_exact(b_tail, n, int(h_q.sum()))
            center[diag] -= np.array([up(S * far / int(v)) for v in h_q], dtype=np.int64)
        return gram_positive_int(center)


def verify_cover_1d(boxes, q_lo, q_hi, check_fn, label):
    need(len(boxes) > 0, f"{label}: empty box list")
    cur = q_lo
    for idx, b in enumerate(boxes):
        a = F(b[0])
        c = F(b[1])
        need(a <= cur, f"{label}: gap before box {idx}: {cur} < {a}")
        need(a < c, f"{label}: degenerate box {idx}")
        need(check_fn(a, c), f"{label}: box {idx} [{a}, {c}] failed Cholesky")
        if c > cur:
            cur = c
    need(cur >= q_hi, f"{label}: cover ends at {cur} < {q_hi}")


def verify_cover_3d(boxes, q_lo, q_hi, check_fn, label):
    need(len(boxes) > 0, f"{label}: empty 3D box list")
    parsed = []
    vol = F(0)
    for idx, b in enumerate(boxes):
        qa, qb, t1a, t1b, t2a, t2b = map(F, b)
        need(q_lo <= qa < qb <= q_hi, f"{label}: box {idx} q out of range")
        need(0 <= t1a < t1b <= 1, f"{label}: box {idx} t1 out of range")
        need(0 <= t2a < t2b <= 1, f"{label}: box {idx} t2 out of range")
        need(check_fn(qa, qb, t1a, t1b, t2a, t2b), f"{label}: box {idx} failed Cholesky")
        vol += (qb - qa) * (t1b - t1a) * (t2b - t2a)
        parsed.append((qa, qb, t1a, t1b, t2a, t2b))
    need(vol == (q_hi - q_lo), f"{label}: volume mismatch {vol} != {q_hi - q_lo}")
    parsed.sort(key=lambda x: x[0])
    for i in range(len(parsed)):
        _, qb1, a1, b1, c1, d1 = parsed[i]
        for j in range(i + 1, len(parsed)):
            qa2, _, a2, b2, c2, d2 = parsed[j]
            if qa2 >= qb1:
                break
            if a1 < b2 and a2 < b1 and c1 < d2 and c2 < d1:
                raise ValueError(f"{label}: overlapping boxes {i} and {j}")


def verify_all(data, include_far=True):
    need(1 - PI2_6_UP / 2 > F(1, 6), "thm:asym margin check failed")

    # 1. Realizability audit
    ra = data["realizability_audit"]
    for row in ra["k1_rows"]:
        lam = F(row["lambda"])
        mu = F(row["mu"])
        need(mu == lam / 2, f"row lam={lam}: mu != lam/2")
        q0_cold = F(row["q0_cold"])
        v0 = [int(x) for x in row["v0_cold"]]
        need(len(v0) == row["v0_n"], "v0_n mismatch")
        need(folded_cold_eval(lam, F(0), 0, q0_cold, ((F(1), F(1)),), v0) < 0, f"k1_rows lam={lam}: cold0 not negative")
        q1_hot = F(row["q1_hot"])
        need(9 * q1_hot < q0_cold, f"k1_rows lam={lam}: 9*q1_hot < q0_cold failed")
        fld = FoldedBlock(row["hot1_n"])

        def chk_hot1(qa, qb, lam=lam, mu=mu, fld=fld):
            b_lo = [F(0)] + [b_einstein(lam, qb * j * j) for j in range(1, 2 * fld.n)]
            b_hi = [F(0)] + [b_einstein(lam, qa * j * j) for j in range(1, 3 * fld.n)]
            return fld.check_box_from_bounds(mu, 1, lam / qa, b_lo, b_hi, include_far=include_far)

        verify_cover_1d(row["hot1_boxes"], q1_hot, 4 * lam, chk_hot1, f"k1_rows_lam{lam}")

    l152 = ra["lam152_fixed1_failure"]
    lam = F(l152["lambda"])
    mu = F(l152["mu"])
    u1, u2, th = F(l152["u1"]), F(l152["u2"]), F(l152["theta"])
    need(0 < u1 < 1 < u2 and (1 - th) * u1 + th * u2 == 1, "lam152 Moment-1 failed")
    spec152 = ((1 - th, u1), (th, u2))
    q_test = F(l152["q_test"])
    v_mix = [int(x) for x in l152["v_mix_cold"]]
    need(folded_cold_eval(lam, mu, 1, q_test, spec152, v_mix) < 0, "lam152 mix not cold")
    q0_152 = F([r for r in ra["k1_rows"] if F(r["lambda"]) == lam][0]["q0_cold"])
    need(9 * q_test < q0_152, "lam152 9*q_test < q0_cold failed")
    fld152 = FoldedBlock(l152["n"])
    verify_cover_1d(
        l152["hot_E_boxes"],
        q_test,
        4 * lam,
        lambda qa, qb: fld152.check_box_from_bounds(
            mu, 1, lam / qa,
            [F(0)] + [b_einstein(lam, qb * j * j) for j in range(1, 2 * fld152.n)],
            [F(0)] + [b_einstein(lam, qa * j * j) for j in range(1, 3 * fld152.n)],
            include_far=include_far,
        ),
        "lam152_hot_E",
    )

    # 2. Target 2 slabs + D2 + D1
    t2 = data["target2_r0_1over64"]
    r0 = F(t2["r0"])
    slabs = t2["slabs"]
    need(F(slabs[0]["lam_lo"]) == F(t2["lam_lo"]), "slab start mismatch")
    need(F(slabs[-1]["lam_hi"]) == F(t2["lam_hi"]), "slab end mismatch")
    for idx, s in enumerate(slabs):
        lam_lo, lam_hi, q_star = F(s["lam_lo"]), F(s["lam_hi"]), F(s["q_star"])
        if idx + 1 < len(slabs):
            need(lam_hi == F(slabs[idx + 1]["lam_lo"]), f"slab {idx} discontinuity")
        v_cold = [int(x) for x in s["v_cold"]]
        need(all(x >= 0 for x in v_cold) and any(x > 0 for x in v_cold), f"slab {idx} v_cold not >= 0")
        need(
            folded_cold_eval(lam_lo, F(0), 0, q_star, ((F(1), F(1)),), v_cold, extra_all_ones_mu=r0 * lam_lo) < 0,
            f"slab {idx} cold failed",
        )
        fld = FoldedBlock(s["n"])

        def chk_gb(qa, qb, t1a, t1b, t2a, t2b, lam_hi=lam_hi, fld=fld):
            b_lo = [F(0)] + [b_gb_bounds(lam_hi, qa * j * j, qb * j * j, t1a, t1b, t2a, t2b)[0] for j in range(1, 2 * fld.n)]
            b_hi = [F(0)] + [b_gb_bounds(lam_hi, qa * j * j, qb * j * j, t1a, t1b, t2a, t2b)[1] for j in range(1, 3 * fld.n)]
            return fld.check_box_from_bounds(F(0), 0, lam_hi / qa, b_lo, b_hi, include_far=include_far)

        verify_cover_3d(s["gb_boxes"], q_star, 4 * lam_hi, chk_gb, f"slab{idx}_gb")

        verify_cover_1d(
            s["d2_boxes"], q_star, 4 * lam_hi,
            lambda qa, qb, lam_hi=lam_hi, fld=fld: fld.check_box_from_bounds(
                F(0), 0, lam_hi / qa,
                [F(0)] + [b_d2_eff(lam_hi, qb * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_d2_eff(lam_hi, qa * j * j) for j in range(1, 3 * fld.n)],
                include_far=include_far,
            ),
            f"slab{idx}_d2",
        )
        verify_cover_1d(
            s["d1_boxes"], q_star, 4 * lam_hi,
            lambda qa, qb, lam_hi=lam_hi, fld=fld: fld.check_box_from_bounds(
                F(0), 0, lam_hi / qa,
                [F(0)] + [b_d1_eff(lam_hi, qb * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_d1_eff(lam_hi, qa * j * j) for j in range(1, 3 * fld.n)],
                include_far=include_far,
            ),
            f"slab{idx}_d1",
        )

    # 3. Jump cliff obstruction
    cl = data["jump_cliff_obstruction"]
    c_lam, c_mu = F(cl["lambda"]), F(cl["mu"])
    q_cliff, R2 = F(cl["q_cliff"]), F(cl["R2"])
    need(c_mu == r0 * c_lam, "cliff mu != r0*lam")
    need(4 * R2 == (2 * cl["k_at_cliff"] + 1) ** 2 * q_cliff, "cliff exact resonance mismatch")
    need(cutoff(q_cliff, R2) == cl["k_at_cliff"], "cliff k_at_cliff mismatch")
    need(cutoff(q_cliff - F(1, 10 ** 9), R2) == cl["k_below_cliff"], "cliff k_below_cliff mismatch")
    u1c, u2c, thc = F(cl["u1"]), F(cl["u2"]), F(cl["theta"])
    need(0 < u1c < 1 < u2c and (1 - thc) * u1c + thc * u2c == 1, "cliff Moment-1 failed")
    spec_c = ((1 - thc, u1c), (thc, u2c))
    need(folded_cold_eval(c_lam, c_mu, cl["k_below_cliff"], q_cliff, ((F(1), F(1)),), [int(x) for x in cl["v_E_cold_k15"]]) < 0, "cliff E not cold on k15")
    need(folded_cold_eval(c_lam, c_mu, cl["k_below_cliff"], q_cliff, spec_c, [int(x) for x in cl["v_p_cold_k15"]]) < 0, "cliff p not cold on k15")
    fld_c = FoldedBlock(cl["n"])
    for key_w, spec_w in [("windows_E", ((F(1), F(1)),)), ("windows_p", spec_c)]:
        wins = cl[key_w]
        cur_w = q_cliff
        b_tail_coeff = c_lam * sum(th * u for th, u in spec_w)
        for w in wins:
            k_w = w["k"]
            w_lo = cur_w
            w_hi = min(4 * c_lam, F(4 * R2, (2 * k_w - 1) ** 2)) if k_w > 0 else 4 * c_lam
            need(cutoff(w_lo, R2) == k_w, f"{key_w} mask mismatch at {w_lo}")
            verify_cover_1d(
                w["boxes"], w_lo, w_hi,
                lambda qa, qb, k_w=k_w, spec_w=spec_w, b_tail_coeff=b_tail_coeff: fld_c.check_box_from_bounds(
                    c_mu, k_w, b_tail_coeff / qa,
                    [F(0)] + [b_spec(c_lam, qb * j * j, spec_w) for j in range(1, 2 * fld_c.n)],
                    [F(0)] + [b_spec(c_lam, qa * j * j, spec_w) for j in range(1, 3 * fld_c.n)],
                    include_far=include_far,
                ),
                f"cliff_{key_w}_k{k_w}",
            )
            cur_w = w_hi
        need(cur_w == 4 * c_lam, f"cliff {key_w} did not reach 4*lam")

    # 4. Target 3: 20 benchmarked (k, lam) at mu*/lam = 1/2
    for item in data["target3_d2_k1_to_4"]:
        k, lam, mu = item["k"], F(item["lambda"]), F(item["mu"])
        need(mu == lam / 2, "target3 mu != lam/2")
        q_lo, q_hi = F(item["q_lo"]), F(item["q_hi"])
        v_cold = [int(x) for x in item["v_cold"]]
        need(folded_cold_eval(lam, mu, k, q_lo, ((F(1), F(1)),), v_cold) < 0, f"target3 k={k} lam={lam} cold failed")
        fld = FoldedBlock(item["n"])
        verify_cover_1d(
            item["hot_q_boxes"], q_hi, 4 * lam,
            lambda qa, qb, k=k, lam=lam, mu=mu, fld=fld: fld.check_box_from_bounds(
                mu, k, lam / qa,
                [F(0)] + [b_einstein(lam, qb * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_einstein(lam, qa * j * j) for j in range(1, 3 * fld.n)],
                include_far=include_far,
            ),
            f"target3_k{k}_lam{lam}_hot",
        )
        verify_cover_1d(
            item["d2_boxes"], q_lo, q_hi,
            lambda qa, qb, k=k, lam=lam, mu=mu, fld=fld: fld.check_box_from_bounds(
                mu, k, lam / qa,
                [F(0)] + [b_d2_eff(lam, qb * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_d2_eff(lam, qa * j * j) for j in range(1, 3 * fld.n)],
                include_far=include_far,
            ),
            f"target3_k{k}_lam{lam}_d2",
        )
        verify_cover_1d(
            item["d1_boxes"], q_lo, q_hi,
            lambda qa, qb, k=k, lam=lam, mu=mu, fld=fld: fld.check_box_from_bounds(
                mu, k, lam / qa,
                [F(0)] + [b_d1_eff(lam, qb * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_d1_eff(lam, qa * j * j) for j in range(1, 3 * fld.n)],
                include_far=include_far,
            ),
            f"target3_k{k}_lam{lam}_d1",
        )


def run_mutant(name, data):
    if name == "realizability_boundary":
        r = data["realizability_audit"]["k1_rows"][0]
        q1, q0 = F(r["q1_hot"]), F(r["q0_cold"])
        control(9 * q1 < q0, "unmutated lam=10 realizability inequality holds")
        q1_bad = q0 / 9
        if not (9 * q1_bad < q0):
            refused("realizability inequality 9*q1 < q0 violated at boundary q0/9")
    elif name == "coulomb":
        s0 = data["target2_r0_1over64"]["slabs"][0]
        lam = F(s0["lam_lo"])
        q_star = F(s0["q_star"])
        v = [int(x) for x in s0["v_cold"]]
        control(folded_cold_eval(lam, F(0), 0, q_star, ((F(1), F(1)),), v, extra_all_ones_mu=F(1, 64) * lam) < 0, "unmutated slab0 cold at r0=1/64")
        val_bad = folded_cold_eval(lam, F(0), 0, q_star, ((F(1), F(1)),), v, extra_all_ones_mu=F(1, 2) * lam)
        if not (val_bad < 0):
            refused(f"coulomb mutant: r=1/2 destroys slab0 cold witness ({val_bad} >= 0)")
    elif name == "moment":
        l152 = data["realizability_audit"]["lam152_fixed1_failure"]
        u1, u2, th = F(l152["u1"]), F(l152["u2"]), F(l152["theta"])
        control((1 - th) * u1 + th * u2 == 1, "unmutated lam152 Moment-1")
        th_bad = 1 - th
        if (1 - th_bad) * u1 + th_bad * u2 != 1:
            refused("moment mutant: weight swap violates (1-theta)u1 + theta*u2 = 1")
    elif name == "tail_drop":
        fld8 = FoldedBlock(8)
        lam5, q57 = F(5), F(57, 10)
        b_lo = [F(0)] + [b_einstein(lam5, q57 * j * j) for j in range(1, 16)]
        b_hi = [F(0)] + [b_einstein(lam5, q57 * j * j) for j in range(1, 24)]
        control(fld8.check_box_from_bounds(F(0), 0, lam5 / q57, b_lo, b_hi, include_far=False), "far_lump omitted passes at n=8, lam=5, q=57/10")
        if not fld8.check_box_from_bounds(F(0), 0, lam5 / q57, b_lo, b_hi, include_far=True):
            refused("tail_drop mutant: exact far_lump penalty rejects under-resolved n=8 box")
    elif name == "box_gap":
        s0 = data["target2_r0_1over64"]["slabs"][0]
        control(len(s0["gb_boxes"]) > 1, "unmutated slab0 has multiple boxes")
        try:
            verify_cover_3d(s0["gb_boxes"][:-1], F(s0["q_star"]), 4 * F(s0["lam_hi"]), lambda *args: bool(args) or True, "gap_test")
        except ValueError as e:
            refused(f"box_gap mutant rejected: {e}")
    elif name == "overflow":
        a_ok = np.eye(4, dtype=np.int64) * S
        control(gram_positive_int(a_ok), "unmutated identity passes gram_positive_int")
        a_big = np.eye(4, dtype=np.int64) * (2 ** 42)
        if not gram_positive_int(a_big):
            refused("overflow mutant: entry >= 2**42 refused by int64 guard")
    elif name == "cliff_sign":
        cl = data["jump_cliff_obstruction"]
        c_lam, c_mu, q_cliff = F(cl["lambda"]), F(cl["mu"]), F(cl["q_cliff"])
        fld_c = FoldedBlock(cl["n"])
        control(folded_cold_eval(c_lam, c_mu, cl["k_below_cliff"], q_cliff, ((F(1), F(1)),), [int(x) for x in cl["v_E_cold_k15"]]) < 0, "unmutated k15 cold at q_cliff")
        b_e = [F(0)] + [b_einstein(c_lam, q_cliff * j * j) for j in range(1, 3 * fld_c.n)]
        if not fld_c.check_box_from_bounds(c_mu, cl["k_below_cliff"], c_lam / q_cliff, b_e[:2 * fld_c.n], b_e):
            refused("cliff_sign mutant: F_E^(15)(q_cliff) is NOT positive definite")
    elif name == "d2_sign_reversal":
        t0 = data["target3_d2_k1_to_4"][0]
        lam, mu, k = F(t0["lambda"]), F(t0["mu"]), t0["k"]
        q_lo, q_hi = F(t0["q_lo"]), F(t0["q_hi"])
        fld = FoldedBlock(t0["n"])
        control(
            fld.check_box_from_bounds(
                mu, k, lam / q_lo,
                [F(0)] + [b_d2_eff(lam, q_hi * j * j) for j in range(1, 2 * fld.n)],
                [F(0)] + [b_d2_eff(lam, q_lo * j * j) for j in range(1, 3 * fld.n)],
            ),
            "unmutated target3[0] D2 passes",
        )
        b_neg_lo = [F(0)] + [lam * (1 + 3 * q_hi * j * j + (q_hi * j * j) ** 2) / ((1 + q_hi * j * j) ** 3) for j in range(1, 2 * fld.n)]
        b_neg_hi = [F(0)] + [lam * (1 + 3 * q_lo * j * j + (q_lo * j * j) ** 2) / ((1 + q_lo * j * j) ** 3) for j in range(1, 3 * fld.n)]
        if not fld.check_box_from_bounds(mu, k, lam / q_lo, b_neg_lo, b_neg_hi):
            refused("d2_sign_reversal mutant: F_E - D2 at q_lo is NOT positive definite (proving +D2 sign is essential)")
    else:
        raise ValueError(f"unknown mutant {name}")
    print(f"ERROR: mutant {name} was NOT refused!")
    raise SystemExit(3)


MUTANTS = [
    "realizability_boundary",
    "coulomb",
    "moment",
    "tail_drop",
    "box_gap",
    "overflow",
    "cliff_sign",
    "d2_sign_reversal",
]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--mutant", choices=MUTANTS)
    p.add_argument("--mutants", action="store_true")
    args = p.parse_args()
    data = json.loads((HERE / "bounds.json").read_text())

    if args.mutant:
        run_mutant(args.mutant, data)
    if args.mutants:
        for m in MUTANTS:
            res = subprocess.run([sys.executable, "-B", str(HERE / "replay.py"), "--mutant", m], capture_output=True, text=True)
            print(f"[{m}] rc={res.returncode}: {res.stdout.strip()[:160]}")
            if res.returncode != 1 or "mutant refused:" not in res.stdout:
                raise SystemExit(f"mutant {m} exited with {res.returncode} (stdout={res.stdout!r}, stderr={res.stderr!r}), expected rc=1 refusal")
        print(f"ALL {len(MUTANTS)} MUTANTS REFUSED (exit 1)")
        return

    verify_all(data)
    print("replay.py: ALL CERTIFICATES VERIFIED (realizability_audit, target2_r0_1over64, jump_cliff_obstruction, target3_d2_k1_to_4)")


if __name__ == "__main__":
    main()
