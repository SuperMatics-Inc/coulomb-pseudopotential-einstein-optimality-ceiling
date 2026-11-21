"""Generate exact rational/int64 certificate witnesses in bounds.json for common-cutoff Einstein optimality (Version 2)."""
import json
import time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.linalg import cholesky, eigh, eigvalsh

HERE = Path(__file__).resolve().parent
S = 2**30
G = 2**25


def up(x):
    return -(-x.numerator // x.denominator)


def fstr(x):
    x = F(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def matvec(a, x):
    return (a @ x).astype(np.int64)


def far_lump_exact(b, n, head_sum):
    tail_factor = F(1, (2 * n + 1) * (2 * n) ** 4) + F(1, 4 * (2 * n) ** 4)
    return 25 * b * b * head_sum * tail_factor


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

    def check_hot_from_bounds(self, lo, hi, mu_lo, mu_hi, k, b_tail):
        n = self.n
        if n * n < 2 * b_tail:
            return False
        pot_lo = self.odd * S + 2 * lo[:n].cumsum()
        pot_hi = self.odd * S + 2 * hi[:n].cumsum()
        lower = -hi[self.diff] - hi[self.hank]
        upper = -lo[self.diff] - lo[self.hank]
        if k > 0:
            lower[:k, :k] += mu_lo
            upper[:k, :k] += mu_hi
        diag = np.diag_indices(n)
        lower[diag] += pot_lo
        upper[diag] += pot_hi
        center = (lower + upper) // 2
        radius = upper - center
        h = self.lin
        rad_pen = matvec(radius, h)
        center[diag] -= np.array([(int(r) + int(hv) - 1) // int(hv) for r, hv in zip(rad_pen, h)], dtype=np.int64)
        edge = hi[self.edge0] + hi[self.edge1]
        hq = self.quad
        den = self.tail_d * S
        row_raw = matvec(edge, hq)
        row = np.array([(int(rr) + int(dv) - 1) // int(dv) for rr, dv in zip(row_raw, den)], dtype=np.int64)
        near_raw = matvec(edge.T, row)
        near = np.array([(int(nr) + int(hv) - 1) // int(hv) for nr, hv in zip(near_raw, hq)], dtype=np.int64)
        far = far_lump_exact(b_tail, n, int(hq.sum()))
        center[diag] -= near + np.array([up(S * far / int(v)) for v in hq], dtype=np.int64)
        return gram_positive(center)


def gram_positive(a):
    n = len(a)
    a_float = a.astype(float) / S
    for shift in (2e-4, 2e-5, 2e-6):
        try:
            l = cholesky(a_float - shift * np.eye(n), lower=True, check_finite=False)
        except np.linalg.LinAlgError:
            continue
        if np.max(np.abs(l)) * G >= 2**31 - 1 or np.max(np.abs(a)) >= 2**42:
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


def weights_spec(lam, q, count, spectrum):
    return [F(0)] + [sum(lam * th * u / (u + q * j * j) for th, u in spectrum) for j in range(1, count)]


def directed(a):
    lo = np.array([int(x * S) for x in a], dtype=np.int64)
    hi = np.array([up(x * S) for x in a], dtype=np.int64)
    return lo, hi


def cold_vec_spec(lam, mu, q, k, spectrum, n, nonneg=False):
    j = np.arange(2 * n + 2)
    b = np.zeros(2 * n + 2)
    for th, u in spectrum:
        b[1:] += float(lam * th * u) / (float(u) + float(q) * j[1:]**2)
    i = np.arange(n)
    M = np.diag(2 * i + 1.0 + 2 * b[:n].cumsum()) - b[np.abs(i[:, None] - i)] - b[i[:, None] + i + 1]
    if k > 0:
        M[:k, :k] += 2.0 * float(mu)
    d = 1.0 / np.sqrt(2 * i + 1.0)
    _, vec = eigh((M * d[:, None]) * d[None, :], subset_by_index=(0, 0), check_finite=False)
    raw = vec[:, 0] * d
    if raw[0] < 0:
        raw = -raw
    if nonneg:
        raw = np.maximum(raw, 0.0)
    return np.rint(raw / max(abs(raw)) * 2**20).astype(np.int64)


def cold_check_exact(folded, lam, mu, q, k, x, spectrum):
    n = folded.n
    lo, hi = directed(weights_spec(lam, q, 2 * n, spectrum))
    different = (x < 0)[:, None] != (x < 0)
    pair = np.where(different, hi[folded.diff] + hi[folded.hank], lo[folded.diff] + lo[folded.hank])
    norm = folded.odd * S + 2 * hi[:n].cumsum()
    prod = matvec(pair, x)
    bound = sum(int(v) * (int(d) * int(v) - int(y)) for v, d, y in zip(x, norm, prod))
    return bound + up(2 * mu * S) * int(x[:k].sum()) ** 2 < 0


def cover_hot_1d(folded, lam, mu, ql, qr, k, spectrum=((F(1), F(1)),), extra_fn=None):
    def ok(a, b):
        if extra_fn is None:
            lo = directed(weights_spec(lam, b, 2 * folded.n, spectrum))[0]
            hi = directed(weights_spec(lam, a, 3 * folded.n, spectrum))[1]
            b_tail = lam * sum(th * u for th, u in spectrum) / a
        else:
            lo, hi, b_tail = extra_fn(lam, a, b)
        return folded.check_hot_from_bounds(lo, hi, int(2 * mu * S), up(2 * mu * S), k, b_tail)
    boxes = []
    stack = [(ql, qr, 0)]
    while stack:
        a, b, d = stack.pop()
        if ok(a, b):
            boxes.append((a, b))
        else:
            if d >= 26:
                raise RuntimeError(f"1D hot failed at {float(a)}..{float(b)} k={k}")
            m = (a + b) / 2
            stack.append((m, b, d + 1))
            stack.append((a, m, d + 1))
    boxes.sort()
    return boxes
def gb0_bounds(lam, ql, qr, t1l, t1r, t2l, t2r, count):
    lo = np.zeros(count, dtype=np.int64)
    hi = np.zeros(count, dtype=np.int64)
    for j in range(1, count):
        jj = j * j
        xa = ql * jj
        xb = qr * jj
        if t1l == 0:
            fa = lam * t2l * xa / ((1 + xa) * (1 + t2l * xa))
            fb = lam * t2l * xb / ((1 + xb) * (1 + t2l * xb))
            b_lo = fa if fa < fb else fb
        else:
            g_lo = (1 + xa) * (1 + t1l * t2l + t1l / xb + t2l * xa)
            b_lo = lam * (F(1) / (1 + xb) - F(1) / g_lo)
            if b_lo < 0:
                b_lo = F(0)
        g_hi = (1 + xb) * (1 + t1r * t2r + t1r / xa + t2r * xb)
        b_hi = min(lam / (1 + xa), lam * (F(1) / (1 + xa) - F(1) / g_hi))
        lo[j] = int(b_lo * S)
        hi[j] = up(b_hi * S)
    return lo, hi
def find_q_gb_approx(lam_val):
    n_num = 55
    j = np.arange(2 * n_num + 2)
    i = np.arange(n_num)
    best_q = 0.0
    for t1 in [0.0, 0.5, 1.0]:
        for t2 in [0.0, 0.5, 1.0]:
            lo, hi = 1e-5, 4.0 * lam_val
            for _ in range(30):
                mid = 0.5 * (lo + hi)
                x = mid * j * j
                b = np.zeros_like(x)
                b[1:] = lam_val * (1.0 / (1 + x[1:]) - x[1:] / ((1 + x[1:]) * (t1 + x[1:]) * (1 + t2 * x[1:])))
                M = np.diag(2 * i + 1.0 + 2 * b[:n_num].cumsum()) - b[np.abs(i[:, None] - i)] - b[i[:, None] + i + 1]
                if eigvalsh(M)[0] > 0:
                    hi = mid
                else:
                    lo = mid
            if 0.5 * (lo + hi) > best_q:
                best_q = 0.5 * (lo + hi)
    return best_q


def build_slabs(lam_start, lam_end, r0):
    slabs = []
    la = lam_start
    n_num = 85
    j = np.arange(2 * n_num + 2)
    i = np.arange(n_num)
    while la < lam_end:
        qgb = find_q_gb_approx(float(la))
        lo, hi = qgb, 4.0 * float(la)
        for _ in range(35):
            mid = 0.5 * (lo + hi)
            b = np.zeros(2 * n_num + 2)
            b[1:] = float(la) / (1.0 + mid * j[1:]**2)
            M = np.diag(2 * i + 1.0 + 2 * b[:n_num].cumsum()) - b[np.abs(i[:, None] - i)] - b[i[:, None] + i + 1] + 2.0 * float(la * r0)
            if eigvalsh(M)[0] > 0:
                hi = mid
            else:
                lo = mid
        qe_a = 0.5 * (lo + hi)
        target_qgb = qgb + 0.45 * (qe_a - qgb)
        lb_f = float(la) * 1.05
        while lb_f < float(lam_end) and find_q_gb_approx(lb_f) < target_qgb:
            lb_f += (float(lb_f) - float(la)) * 0.35 + 0.002
        lb = min(lam_end, F(int(lb_f * 10000), 10000))
        if lb <= la:
            lb = min(lam_end, la + F(1, 1000))
        while lb > la + F(1, 1000) and find_q_gb_approx(float(lb)) >= qe_a - 0.15 * (qe_a - qgb):
            lb = la + (lb - la) * F(3, 4)
        qgb_b = find_q_gb_approx(float(lb))
        qs_f = 0.55 * qgb_b + 0.45 * qe_a
        q_star = F(int(qs_f * 100000), 100000)
        if q_star <= 0:
            q_star = F(int(qs_f * 10000000), 10000000)
        slabs.append((la, lb, q_star))
        la = lb
    return slabs


def d2_eff_bounds(lam, a, b, count):
    lo = np.zeros(count, dtype=np.int64)
    hi = np.zeros(count, dtype=np.int64)
    for j in range(1, count):
        jj = j * j
        xL = a * jj
        xR = b * jj
        vL = lam * (1 + xL + xL * xL) / ((1 + xL) ** 3)
        vR = lam * (1 + xR + xR * xR) / ((1 + xR) ** 3)
        lo[j] = int(vR * S)
        hi[j] = up(vL * S)
    return lo, hi, lam / a


def d1_eff_bounds(lam, a, b, count):
    lo = np.zeros(count, dtype=np.int64)
    hi = np.zeros(count, dtype=np.int64)
    for j in range(1, count):
        jj = j * j
        xL = a * jj
        xR = b * jj
        vL = lam / ((1 + xL) ** 2)
        vR = lam / ((1 + xR) ** 2)
        lo[j] = int(vR * S)
        hi[j] = up(vL * S)
    return lo, hi, lam / a


def main():
    t0 = time.time()
    out = {}

    # 1. REALIZABILITY AUDIT (Target 1)
    print("1. Generating realizability audit...")
    f80 = Folded(80)
    real_rows = []
    for lam_int in [10, 20, 25, 35, 50, 65, 152]:
        lam = F(lam_int)
        mu = lam / 2
        j = np.arange(400)

        def qE_approx(l, m, kk):
            lo, hi = 1e-4, 4.0 * float(l)
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                b = np.zeros(400)
                b[1:] = float(l) / (1.0 + mid * j[1:]**2)
                i = np.arange(140)
                M = np.diag(2 * i + 1.0 + 2 * b[:140].cumsum()) - b[np.abs(i[:, None] - i)] - b[i[:, None] + i + 1]
                if kk > 0:
                    M[:kk, :kk] += 2.0 * float(m)
                if eigvalsh(M)[0] > 0:
                    hi = mid
                else:
                    lo = mid
            return 0.5 * (lo + hi)

        q0_est = qE_approx(lam, F(0), 0)
        q1_est = qE_approx(lam, mu, 1)
        q0_cold = F(int(q0_est * 10000) - 5, 10000)
        q1_hot = F(int(q1_est * 10000) + (50 if lam_int == 10 else 250), 10000)
        assert 9 * q1_hot < q0_cold, (lam_int, float(9 * q1_hot), float(q0_cold))
        v0 = cold_vec_spec(lam, F(0), q0_cold, 0, ((F(1), F(1)),), 80, nonneg=True)
        assert cold_check_exact(f80, lam, F(0), q0_cold, 0, v0, ((F(1), F(1)),))
        fld = Folded(280) if lam_int >= 50 else (Folded(120) if lam_int >= 25 else f80)
        boxes = cover_hot_1d(fld, lam, mu, q1_hot, 4 * lam, 1)
        real_rows.append({
            "lambda": lam_int,
            "mu": fstr(mu),
            "q0_cold": fstr(q0_cold),
            "v0_n": 80,
            "v0_cold": v0.tolist(),
            "q1_hot": fstr(q1_hot),
            "hot1_n": fld.n,
            "hot1_boxes": [[fstr(a), fstr(b)] for a, b in boxes],
        })
        print(f"  lam={lam_int:3d}: 9*q1_hot={float(9*q1_hot):.4f} < q0_cold={float(q0_cold):.4f}, boxes={len(boxes)}")

    u1, u2 = F(1, 100000), F(35, 2)
    th = (1 - u1) / (u2 - u1)
    spec152 = ((1 - th, u1), (th, u2))
    q152_test = F(43355, 10000)
    fld152 = Folded(280)
    boxes152_E = cover_hot_1d(fld152, F(152), F(76), q152_test, F(4 * 152), 1)
    v152_mix = cold_vec_spec(F(152), F(76), q152_test, 1, spec152, 280, nonneg=False)
    assert cold_check_exact(fld152, F(152), F(76), q152_test, 1, v152_mix, spec152)
    assert 9 * q152_test < F(real_rows[-1]["q0_cold"])
    out["realizability_audit"] = {
        "k1_rows": real_rows,
        "lam152_fixed1_failure": {
            "lambda": 152, "mu": 76, "k": 1,
            "u1": fstr(u1), "u2": fstr(u2), "theta": fstr(th),
            "q_test": fstr(q152_test),
            "n": 280,
            "hot_E_boxes": [[fstr(a), fstr(b)] for a, b in boxes152_E],
            "v_mix_cold": v152_mix.tolist(),
        },
    }

    # 2. TARGET 2: r0 = 1/64 on [3/10, 3] + D2/D1 corollary
    print("2. Generating Target 2 slabs on [3/10, 3] at r0 = 1/64...")
    r0 = F(1, 64)
    slabs_raw = build_slabs(F(3, 10), F(3), r0)
    print(f"  Built {len(slabs_raw)} slabs on [3/10, 3]. Certifying boxes + D2/D1...")

    slab_records = []
    total_gb_boxes = 0
    total_d2_boxes = 0
    for idx, (la, lb, q_star) in enumerate(slabs_raw):
        b_bound = float(lb / q_star)
        n_req = max(64, int(np.ceil(np.sqrt(2.2 * b_bound))) + 14)
        fld = Folded(n_req)
        v_cold = cold_vec_spec(la, r0 * la, q_star, n_req, ((F(1), F(1)),), n_req, nonneg=True)
        assert np.all(v_cold >= 0)
        assert cold_check_exact(fld, la, r0 * la, q_star, n_req, v_cold, ((F(1), F(1)),)), f"cold failed at slab {idx}"

        gb_boxes = []
        stack = [(q_star, 4 * lb, F(0), F(1), F(0), F(1), 0)]
        while stack:
            ql, qr, t1l, t1r, t2l, t2r, d = stack.pop()
            lo, hi = gb0_bounds(lb, ql, qr, t1l, t1r, t2l, t2r, 3 * n_req)
            if fld.check_hot_from_bounds(lo, hi, 0, 0, 0, lb / ql):
                gb_boxes.append([fstr(x) for x in (ql, qr, t1l, t1r, t2l, t2r)])
            else:
                if d >= 24:
                    raise RuntimeError(f"GB0 failed at slab {idx} q=[{float(ql)}, {float(qr)}]")
                qm = (ql + qr) / 2
                t1m = (t1l + t1r) / 2
                t2m = (t2l + t2r) / 2
                w_q = float((qr - ql) / ql)
                w_t1 = float(t1r - t1l)
                w_t2 = float(t2r - t2l)
                if w_q > 0.15 * max(w_t1, w_t2, 1e-9):
                    stack.append((qm, qr, t1l, t1r, t2l, t2r, d + 1))
                    stack.append((ql, qm, t1l, t1r, t2l, t2r, d + 1))
                elif w_t1 >= w_t2:
                    stack.append((ql, qr, t1m, t1r, t2l, t2r, d + 1))
                    stack.append((ql, qr, t1l, t1m, t2l, t2r, d + 1))
                else:
                    stack.append((ql, qr, t1l, t1r, t2m, t2r, d + 1))
                    stack.append((ql, qr, t1l, t1r, t2l, t2m, d + 1))
        total_gb_boxes += len(gb_boxes)

        d2_boxes = cover_hot_1d(fld, lb, F(0), q_star, 4 * lb, 0, extra_fn=lambda L, a, b, n3=3 * fld.n: d2_eff_bounds(L, a, b, n3))
        d1_boxes = cover_hot_1d(fld, lb, F(0), q_star, 4 * lb, 0, extra_fn=lambda L, a, b, n3=3 * fld.n: d1_eff_bounds(L, a, b, n3))
        total_d2_boxes += len(d2_boxes) + len(d1_boxes)

        slab_records.append({
            "lam_lo": fstr(la), "lam_hi": fstr(lb),
            "q_star": fstr(q_star), "n": n_req,
            "v_cold": v_cold.tolist(),
            "gb_boxes": gb_boxes,
            "d2_boxes": [[fstr(a), fstr(b)] for a, b in d2_boxes],
            "d1_boxes": [[fstr(a), fstr(b)] for a, b in d1_boxes],
        })
    print(f"  Certified all {len(slab_records)} slabs! gb_boxes={total_gb_boxes}, d2+d1_boxes={total_d2_boxes}")
    out["target2_r0_1over64"] = {
        "r0": fstr(r0),
        "lam_lo": "3/10", "lam_hi": "3",
        "slabs": slab_records,
    }

    # 3. JUMP-CLIFF OBSTRUCTION AT r = 1/64 (lam=2, mu=1/32)
    print("3. Generating jump-cliff obstruction at lam=2, mu=1/32, q_cliff=962/625...")
    lam_c = F(2)
    mu_c = F(1, 32)
    qc = F(962, 625)
    m_c = 14
    R2_c = (2 * m_c + 1) ** 2 * qc / 4
    eps_c = F(1, 1024)
    spec_c = ((F(1, 2), 1 - eps_c), (F(1, 2), 1 + eps_c))
    fld_c = Folded(60)
    v_E_c = cold_vec_spec(lam_c, mu_c, qc, 15, ((F(1), F(1)),), 60, nonneg=False)
    v_p_c = cold_vec_spec(lam_c, mu_c, qc, 15, spec_c, 60, nonneg=False)
    assert cold_check_exact(fld_c, lam_c, mu_c, qc, 15, v_E_c, ((F(1), F(1)),))
    assert cold_check_exact(fld_c, lam_c, mu_c, qc, 15, v_p_c, spec_c)
    cliff_windows_E = []
    cliff_windows_p = []
    for kk in range(14, -1, -1):
        w_lo = max(qc, 4 * R2_c / (2 * kk + 1) ** 2)
        w_hi = min(4 * lam_c, 4 * R2_c / (2 * kk - 1) ** 2) if kk > 0 else 4 * lam_c
        if w_lo >= 4 * lam_c or w_lo >= w_hi:
            continue
        bE = cover_hot_1d(fld_c, lam_c, mu_c, w_lo, w_hi, kk, ((F(1), F(1)),))
        bp = cover_hot_1d(fld_c, lam_c, mu_c, w_lo, w_hi, kk, spec_c)
        cliff_windows_E.append({"k": kk, "boxes": [[fstr(a), fstr(b)] for a, b in bE]})
        cliff_windows_p.append({"k": kk, "boxes": [[fstr(a), fstr(b)] for a, b in bp]})
    out["jump_cliff_obstruction"] = {
        "lambda": 2, "mu": "1/32", "q_cliff": fstr(qc), "R2": fstr(R2_c),
        "k_at_cliff": 14, "k_below_cliff": 15,
        "eps": fstr(eps_c), "u1": fstr(1 - eps_c), "u2": fstr(1 + eps_c), "theta": "1/2",
        "n": 60,
        "v_E_cold_k15": v_E_c.tolist(),
        "v_p_cold_k15": v_p_c.tolist(),
        "windows_E": cliff_windows_E,
        "windows_p": cliff_windows_p,
    }
    print(f"  Jump-cliff certified across {len(cliff_windows_E)} mask windows!")

    # 4. TARGET 3: D2 & D1 positivity for k=1..4 at r = 1/2 (lam in {1/2, 1, 2, 5, 10})
    print("4. Generating Target 3 D2 certificates for k=1..4 at r=1/2...")
    d2_benchmarks = []
    j = np.arange(300)
    for k in [1, 2, 3, 4]:
        for lam_rat in [F(1, 2), F(1), F(2), F(5), F(10)]:
            mu_rat = lam_rat / 2
            n_b = 80 if lam_rat <= 2 else 120
            fld_b = Folded(n_b)
            i = np.arange(n_b)
            lo, hi = 1e-5, 4.0 * float(lam_rat)
            for _ in range(42):
                mid = 0.5 * (lo + hi)
                b = np.zeros(300)
                b[1:] = float(lam_rat) / (1.0 + mid * j[1:]**2)
                M = np.diag(2 * i + 1.0 + 2 * b[:n_b].cumsum()) - b[np.abs(i[:, None] - i)] - b[i[:, None] + i + 1]
                M[:k, :k] += 2.0 * float(mu_rat)
                if eigvalsh(M)[0] > 0:
                    hi = mid
                else:
                    lo = mid
            q_est = 0.5 * (lo + hi)
            q_lo = F(int(q_est * 100000) - 5, 100000)
            q_hi = F(int(q_est * 100000) + 5, 100000)
            if q_lo <= 0:
                q_lo = F(int(q_est * 1000000) - 5, 1000000)
                q_hi = F(int(q_est * 1000000) + 5, 1000000)
            v_c = cold_vec_spec(lam_rat, mu_rat, q_lo, k, ((F(1), F(1)),), n_b, nonneg=False)
            assert cold_check_exact(fld_b, lam_rat, mu_rat, q_lo, k, v_c, ((F(1), F(1)),))
            hot_q = cover_hot_1d(fld_b, lam_rat, mu_rat, q_hi, 4 * lam_rat, k)
            d2_b = cover_hot_1d(fld_b, lam_rat, mu_rat, q_lo, q_hi, k, extra_fn=lambda L, a, b, n3=3 * fld_b.n: d2_eff_bounds(L, a, b, n3))
            d1_b = cover_hot_1d(fld_b, lam_rat, mu_rat, q_lo, q_hi, k, extra_fn=lambda L, a, b, n3=3 * fld_b.n: d1_eff_bounds(L, a, b, n3))
            d2_benchmarks.append({
                "k": k, "lambda": fstr(lam_rat), "mu": fstr(mu_rat),
                "q_lo": fstr(q_lo), "q_hi": fstr(q_hi), "n": n_b,
                "v_cold": v_c.tolist(),
                "hot_q_boxes": [[fstr(a), fstr(b)] for a, b in hot_q],
                "d2_boxes": [[fstr(a), fstr(b)] for a, b in d2_b],
                "d1_boxes": [[fstr(a), fstr(b)] for a, b in d1_b],
            })
    print(f"  Certified {len(d2_benchmarks)} (k, lam) D2+D1 brackets at r=1/2!")
    out["target3_d2_k1_to_4"] = d2_benchmarks

    out_path = HERE / "bounds.json"
    with open(out_path, "w") as fh:
        json.dump(out, fh)
    print(f"ALL DONE in {time.time() - t0:.2f}s! Wrote {out_path}.")


if __name__ == "__main__":
    main()
