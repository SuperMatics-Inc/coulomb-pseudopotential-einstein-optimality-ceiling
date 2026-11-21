# Positive Coulomb at fixed coupling and moment

**CERTIFIED counterexample.** Use pairing-only repulsion \(\mu^*1_{|\omega_n|<\omega_c}1_{|\omega_m|<\omega_c}\), with the strict cutoff on both indices and no Coulomb term in the normal self-energy. Under \(\omega_c=10\Omega_{\max}\), Einstein is not a maximizer: at \(\lambda=M/\Omega_E^2=1\), replace \(\delta_1\) in squared frequency \(u=(\Omega/\Omega_E)^2\) by \((2999/3000)\delta_{2996/2999}+(1/3000)\delta_4\). At \(\mu^*=0.10,0.13\) the pair is unstable at \(q=0.260,0.212\), above the respective Einstein upper bounds \(0.2530,0.2075\), where \(q=(2\pi k_BT/\Omega_E)^2\). The same rule yields different numerical cutoffs: \(10\Omega_E\) versus \(20\Omega_E\).

**Common cutoff: open here.** For a common numerical \(\omega_c\), including \(10\Omega_E\) fixed by the shared \(\Omega_E=\sqrt{M/\lambda}\), neither optimality nor uniqueness at positive \(\mu^*\) is established. Rens Thms. 3, 4, 6 and Kondratev Prop. 1/§12 are zero-Coulomb results; Rens Cor. 9 and the finite-band PSD corollary retain the zero-Coulomb ceiling, not the positive-Coulomb Einstein value. See [RIGOR.md](RIGOR.md) for the equations and the precise comparison gap.

**PROVED ([independent review](../C-LAMBDA-MU-REVIEW/REVIEW.md#verdicts-by-claim)).** For spectra each with finite maximum frequency, with no common upper cap, the sharp supremum under \(\omega_c=10\Omega_{\max}\) is the zero-Coulomb Einstein ceiling even with \(\mu^*>0\). A line of vanishing weight can open an arbitrarily large cutoff, allowing the repulsive form to be canceled at arbitrarily small phonon-only cost. This is a degeneracy of the cutoff convention, not a physical prediction.

**CERTIFIED Einstein reference values** \(C_E=k_BT_{\rm lin}/\sqrt M\), not ceilings. \(T_{\rm lin}\) is the supremum of temperatures with a negative stability direction, not a presumed root. Both cutoff choices give \(10\Omega_E\) for Einstein. Two exact verifiers exclude hotter instabilities, including across cutoff changes. Rounded endpoints below enclose the exact rational bounds in `bounds.json`.

| λ | μ*=0.10 | μ*=0.13 |
|---:|---:|---:|
| 0.158 | [1.2661e-11, 4.0040e-5] | [1.2661e-21, 1.2662e-5] |
| 0.5 | [0.022190, 0.022339] | [0.016677, 0.016829] |
| 0.551 | [0.029162, 0.029281] | [0.022932, 0.023063] |
| 1 | [0.079815, 0.080054] | [0.072253, 0.072499] |
| 1.128 | [0.089197, 0.089386] | [0.081776, 0.081969] |
| 1.5 | [0.107787, 0.108023] | [0.101076, 0.101328] |
| 2 | [0.121730, 0.122042] | [0.115592, 0.115922] |
| 2.1 | [0.123769, 0.124062] | [0.117520, 0.117828] |
| 2.67 | [0.131977, 0.132266] | [0.126208, 0.126510] |
| 3 | [0.135359, 0.135641] | [0.129526, 0.129852] |
| 3.175 | [0.136837, 0.137129] | [0.131090, 0.131425] |
| 3.278 | [0.137537, 0.137847] | [0.131916, 0.132268] |
| 3.783 | [0.140782, 0.141115] | [0.135127, 0.135499] |
| 3.86 | [0.141195, 0.141521] | [0.135576, 0.135915] |
| 4 | [0.141906, 0.142242] | [0.136330, 0.136679] |
| 6 | [0.148506, 0.148862] | [0.142973, 0.143358] |
| 10 | [0.154101, 0.154463] | [0.148884, 0.149250] |

**NUMERICAL application, predictions only.** From [Gao et al., Nat. Commun. 16, 8253 (2025)](https://doi.org/10.1038/s41467-025-63702-w), 10 of 24 prediction rows over nine material/spectrum combinations have \(R_\mu=T_c^{\rm pred}/T_E(\lambda,0.10)>0.6\); none exceeds 1. BC11 Eliashberg is highest at 0.8719 (Einstein bracket gives about 0.8701 to 0.8737). Gao's nominal \(\mu^*=0.1\) and their Eliashberg, Allen–Dynes and McMillan treatments do not guarantee the same Coulomb kernel or cutoff as this reference. This is not a falsification filter, matched solver comparison, or a measured-temperature result.

Ratios use published point inputs, not uncertainty intervals. NaNiH₃ ratios of zero reflect the reported precision (0.0 K), not a demonstrated absence of a transition. Li₂AgH₆ uses the harmonic tabulation despite a small imaginary acoustic branch near Γ; the source reports anharmonic stabilization.

| Material / spectrum | Rμ: McMillan / Allen–Dynes / Eliashberg | M*(0.10) / M*(0.13), eV² |
|---|---:|---:|
| Tl2AgH2 harmonic | 0.260 / 0.282 / 0.293 | 0.08382 / 0.09970 |
| NaNiH3 harmonic | 0 / 0 / 0 (printed 0.0 K) | [4.16e5, 4.17e18] / [4.16e6, 4.17e38] |
| BC11 harmonic | 0.752 / 0.770 / 0.872 | 0.7827 / 1.264 |
| B2C8Cl harmonic | 0.448 / 0.674 / 0.784 | 0.03525 / 0.03830 |
| Al2H7Os harmonic | 0.258 / 0.394 / 0.687 | 0.03562 / 0.03879 |
| Li2AgH6 harmonic | 0.370 / 0.616 / 0.737 | 0.03364 / 0.03650 |
| Li2AuH6 harmonic | 0.313 / 0.537 / n/a | 0.03345 / 0.03627 |
| Li2AuH6 SSCHA auxiliary | 0.482 / 0.607 / n/a | 0.04353 / 0.04826 |
| Li2AuH6 SSCHA Hessian | 0.458 / 0.628 / n/a | 0.03829 / 0.04186 |

Here \(M^*=(300k_B/C_E)^2\) is the 300 K **Einstein target moment** as \(\omega_c=10\Omega_E\) scales with \(M\), not a necessary moment for arbitrary spectra or for a cutoff fixed while \(M\) varies. Table point values use the midpoint of \(C_E\); only an interval is reported at \(\lambda=0.158\). The `_lo` and `_hi` fields in `ambient.csv` and `thresholds.csv` enclose the propagated Einstein intervals at the published point inputs using directed rounding.

**NUMERICAL illustration.** At \(\lambda=1,\mu^*=0.13\), for the growing-cutoff family in RIGOR, \(k_BT/\sqrt M\) near the highest sampled finite-section crossing increases from 0.069796 at \(U=2\) to 0.086675 at \(U=256\), still below the zero-Coulomb limit 0.114620. This shows the direction, not numerical convergence to the limit. On this grid doubling the head changed crossings by at most \(3.4\times10^{-10}\) in normalized units.

**Replay.** From this directory, use `UV_CACHE_DIR=D:/dev/.cache/uv uv run --no-project --with numpy --with mpmath --with scipy --with sympy python -B SCRIPT.py` (one BLAS thread used). Run `replay`, `independent`, `application`, then `sequence`; only explicit `replay.py --write` regenerates `bounds.json`. The default verifies the stored receipt without rewriting it.
`replay.py`, `independent.py`, `application.py` and `sequence.py` each exited **0**; byte comparison of `bounds.json` before and after exited **0**. On **each** verifier, `--mutant coulomb`, `--mutant tail`, `--mutant endpoint` and `--mutant sign` each exited **1** at the intended check. Logs: `D:/t/CLambdaMu/`.
