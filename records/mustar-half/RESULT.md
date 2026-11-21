# Positive Coulomb at $\mu^*/\lambda \le 1/2$ under a common cutoff: threshold curve, analytic regimes, and sub-$1/2$ counterexamples

## 1. Question

In the isotropic, constant-DOS ($N_0=1$), infinite-electronic-band linearized Migdal-Eliashberg model with a **two-sided pairing-only** Coulomb subtraction $\mu^* c_n c_m$ ($c_n = \mathbf{1}_{|\omega_n| < \omega_c}$, strict inequality, no Coulomb term in the normal self-energy $Z$) and a **common cutoff** $\omega_c = R \Omega_E$ shared by all spectra at fixed $(\lambda, M)$ ($\Omega_E = \sqrt{M/\lambda}$), does the single Einstein line $\delta(\omega - \Omega_E)$ maximize the linearized onset temperature $T_{\mathrm{lin}}$ throughout $\mu^*/\lambda \le 1/2$, or do counterexamples exist strictly below $\mu^*/\lambda = 1/2$?

## 2. Status and summary of findings

**Status: proof draft and counterexample certificates awaiting re-review** (`replay.py` and the four sub-$1/2$ counterexamples were audited and confirmed genuine in `REVIEW.md`; `RIGOR.md`, `RESULT.md`, `structure.py`, and `independent.py` have been updated in response to `REVIEW.md` F1–F9; see `FIX.md`).

1. **$\mu^*/\lambda = 1/2$ is NOT globally sharp across all $(\lambda, \omega_c/\Omega_E)$ in the sharp-cutoff model, but holds across the analytic regimes below and numerically for all $\lambda < 25.55$ and $k \in \{0, 1, 2, 3, 4\}$.**
   - **Analytic regimes in `RIGOR.md` (proof drafts, numbered identically in `RIGOR.md` and `RESULT.md`):**
     - **Lemma 1 (Exact Finite-Support Decomposition — proof draft):** For every finitely supported $h \in \ell^2(\mathbb{Z}_{\ge 0})$, $\langle h, \mathcal{F}_p^{(k)}(q) h \rangle = \sum_{i=0}^\infty (2i+1)h_i^2 + 2\mu^*(\sum_{i=0}^{k-1} h_i)^2 + \sum_{j=1}^\infty a_j(q;p) L_j(h)$, where $L_j(h) = -\sum_{i=0}^{j-1} h_i h_{j-1-i} - 2\sum_{i=0}^\infty h_{i+j}(h_i - h_{i+j}) < 0$ on nonincreasing positive vectors.
     - **Theorem 1 (Universal Two-Delta Reduction at Fixed $(q, k, \mu^*)$ — proof draft):** On the finitely supported form core $\mathcal{D}_0 \subset \ell^2(\mathbb{Z}_{\ge 0})$, every spectral measure $p \in \mathcal{P}_1$ is matched at fixed $(q, k, \mu^*, h)$ by a two-line spectrum $p_2 \in \mathcal{P}_1^{(2)}$, so $\inf_{p \in \mathcal{P}_1} \lambda_{\min}(\mathcal{F}_p^{(k)}(q)) = \inf_{p_2 \in \mathcal{P}_1^{(2)}} \lambda_{\min}(\mathcal{F}_{p_2}^{(k)}(q))$.
     - **Theorem 2 (Exact Zero-Mask Optimality $k(q,R) = 0$ for All $\mu^* \ge 0$ — proof draft):** Whenever the strict inequality $4 R^2 < q_E(\lambda, 0)$ holds ($\omega_c/\Omega_E < \frac{1}{2}\sqrt{q_E(\lambda, 0)} = \pi C_E(\lambda)\sqrt{\lambda}$), $k(q, R) = 0$ on an open neighborhood of $[q_E(\lambda, 0), \infty)$ and Einstein strictly maximizes $T_{\mathrm{lin}}$ for **all** $\mu^* \ge 0$. (At the boundary $4 R^2 = q_E(\lambda, 0)$ with $\mu^* > 0$, $k(q, R) \ge 1$ for $q < q_E(\lambda, 0)$, so strict inequality is required.)
     - **Theorem 3 (Large-Coupling Fixed-$R$ Einstein Optimality — proof draft):** For every fixed cutoff $R = \omega_c/\Omega_E > 0$, every coupling $\lambda \ge 4 R^2 + 1$, and every $\mu^* \ge 0$, $q_E(\lambda, 0) > \lambda - 1 \ge 4 R^2$, so Theorem 2 applies and Einstein is strictly optimal. *(Note on v1 changes: the unproved small-$\mu^*$ spectral-gap theorem in v1 `RESULT.md` was dropped, and the v1 large-$\lambda$ formula was replaced by the sharper $\mu^*$-independent threshold $\lambda \ge 4 R^2 + 1$ proved in `RIGOR.md`.)*
     - **Theorem 4 (Single-Mode $k = 1$ Cone Monotonicity and Einstein Optimality for $\mu^* \le 1 + a_1(q; p)$ — proof draft):** On the $k = 1$ branch ($\frac{4}{9} R^2 \le q < 4 R^2$), whenever $\mu^* \le 1 + a_1(q; p)$ — which holds **unconditionally** for all $(q, p)$ whenever $\mu^* \le 1$, and across the entire sub-half sector $\mu^*/\lambda \le 1/2$ for all $\lambda \in (0, 2]$ — the ground-state eigenvector satisfies $h^*_0 \ge h^*_1 > h^*_2 > \dots > 0$, every $L_j(h^*) < 0$, and $\lambda_{\min}(\mathcal{F}_{\delta_1}^{(1)}(q)) < \lambda_{\min}(\mathcal{F}_p^{(1)}(q))$ for all $p \in \mathcal{P}_1 \setminus \{\delta_1\}$. *(Note on v1 restriction [F4]: for $\mu^* > 1 + a_1(q; p)$, $\tilde{D}_{p,1} - \tilde{D}_{p,0} = 2 + 2a_1(q;p) - 2\mu^* < 0$, so nonincreasing cone invariance fails — e.g., at $\lambda = 20, \mu^* = 10$ where $h^*_0 < h^*_1$ — and on the fixed $k=1$ branch at $\mu^*/\lambda = 1/2$, two-line spectra with $u_1 \ll 1 \ll u_2$ beat Einstein numerically for $\lambda \ge 152$, while $k=1$ Einstein optimality holds numerically for $\lambda \in (2, 151]$.)*
     - **Theorem 5 (Parameter-Free Asymptotic Cutoff Stability for All $q \ge 4\lambda$ — proof draft):** For all $\lambda > 0, \mu^* \ge 0, R > 0, p \in \mathcal{P}_1$, and $q \ge 4\lambda$, $\mathcal{F}_p^{(k(q,R))}(q) \succeq (1 - \pi^2/12) I \succ \frac{1}{6} I$, providing the exact hot-side handoff $q_{\mathrm{asym}} = 4\lambda$.
   - **Above $\lambda_{\mathrm{crit}} \approx 25.55$ in the narrow $k = 5$ re-entrant fold ($\lambda \in [25.55, 34.0]$, $\omega_c/\Omega_E \in [3.2, 3.6]$):** The critical ratio $r_*(\lambda) = \inf_{R} \{\mu^*/\lambda : \text{Einstein is beaten}\}$ dips **strictly below $1/2$**, reaching a global minimum of
     $$r_{\min} \approx 0.4785 \quad \text{at} \quad \lambda \approx 25.58, \quad \frac{\omega_c}{\Omega_E} \approx 3.36 \quad (\text{NUMERICAL}),$$
     with exact rational counterexample certificates in `bounds.json` at $\mu^*/\lambda = 61261/128000 = 0.4786015625 < 1/2$ ($\lambda = 25.6$), $\mu^*/\lambda = 12/25 = 0.48 < 1/2$ ($\lambda = 26$), $\mu^*/\lambda = 1309/2700 \approx 0.484815 < 1/2$ ($\lambda = 27$), and $\mu^*/\lambda = 489/1000 = 0.489 < 1/2$ ($\lambda = 28$).

2. **Sub-$1/2$ counterexamples (`fixtures.json` / `bounds.json`, verified by `replay.py` and `independent.py`; $C_E$ brackets outward-rounded to 8 decimal places from `bounds.json`):**

| Case | $\lambda$ | $\mu^*$ | $\mu^*/\lambda$ | $R^2 = (\omega_c/\Omega_E)^2$ | Einstein $q_E$ bracket | Outward-rounded $C_E$ bracket | Two-line spectrum $\{(p_1, u_1), (p_2, u_2)\}$ | Unstable $q_{\mathrm{mix}}$ | Ratio $q_{\mathrm{mix}}/q_{E,\mathrm{hi}}$ ($T_{\mathrm{mix}}/T_{E,\mathrm{hi}}$) | True $T_{\mathrm{mix}}/T_E$ ($N=600$, `NUMERICAL`) |
|---|---:|---:|---:|---:|---|---|---|---:|---|---|
| `subhalf-25p6-0p4786` | $128/5 = 25.6$ | $61261/5000$ | **$0.478602$** | $113/10 = 11.3$ | $[0.519,\, 0.525]$ | $[0.02266124,\, 0.02279187]$ | $(\frac{499975}{499978}, \frac{22}{25}) + (\frac{3}{499978}, 20000)$ | $11/20 = 0.55$ | $1.0476\times$ ($\ge 1.0235\times$, $+2.35\%$) | $1.03295\times$ ($+3.30\%$) |
| `subhalf-26-12over25` | $26$ | $312/25 = 12.48$ | **$0.480000$** | $53/5 = 10.6$ | $[0.495,\, 0.501]$ | $[0.02196018,\, 0.02209288]$ | $(\frac{49995}{49996}, \frac{4}{5}) + (\frac{1}{49996}, 10000)$ | $13/25 = 0.52$ | $1.0379\times$ ($\ge 1.0188\times$, $+1.88\%$) | $1.02446\times$ ($+2.45\%$) |
| `subhalf-27-0p4848` | $27$ | $1309/100 = 13.09$ | **$0.484815$** | $63/5 = 12.6$ | $[0.414,\, 0.419]$ | $[0.01970781,\, 0.01982647]$ | $(\frac{199900}{199931}, \frac{69}{100}) + (\frac{31}{199931}, 2000)$ | $51/100 = 0.51$ | $1.2172\times$ ($\ge 1.1033\times$, $+10.33\%$) | $1.16047\times$ ($+16.05\%$) |
| `subhalf-28-0p489` | $28$ | $3423/250 = 13.692$ | **$0.489000$** | $62/5 = 12.4$ | $[0.407,\, 0.412]$ | $[0.01918838,\, 0.01930589]$ | $(\frac{24975}{24984}, \frac{16}{25}) + (\frac{9}{24984}, 1000)$ | $49/100 = 0.49$ | $1.1893\times$ ($\ge 1.0906\times$, $+9.06\%$) | $1.18148\times$ ($+18.15\%$) |

3. **Einstein anchors at $\mu^*/\lambda \le 1/2$ (`bounds.json`, $C_E$ brackets outward-rounded to 8 decimal places):**

| Anchor | $\lambda$ | $\mu^*$ | $\mu^*/\lambda$ | $R^2$ | Einstein $q_E$ bracket | Outward-rounded $C_E$ bracket |
|---|---:|---:|---:|---:|---|---|
| `anchor-l2-mu1-R3/2` | $2$ | $1$ | $0.500$ | $9/4$ | $[0.0402,\, 0.0410]$ | $[0.02256410,\, 0.02278752]$ |
| `anchor-l3-mu3/2-R2` | $3$ | $3/2$ | $0.500$ | $4$ | $[0.0593,\, 0.0601]$ | $[0.02237622,\, 0.02252666]$ |
| `anchor-l10-mu4-R3` | $10$ | $4$ | $0.400$ | $9$ | $[0.441,\, 0.447]$ | $[0.03342253,\, 0.03364914]$ |
| `anchor-l20-mu19/2-R5` | $20$ | $19/2$ | $0.475$ | $25$ | $[0.820,\, 0.827]$ | $[0.03222641,\, 0.03236368]$ |

## 3. Phase diagram and threshold curve $r_*(\lambda, R)$ (NUMERICAL)

Across the 3D parameter space $(\mu^*/\lambda,\, \lambda,\, R = \omega_c/\Omega_E)$, the minimum ratio $r_*(\lambda, R) = \inf\{\mu^*/\lambda : \text{Einstein is beaten at } (\lambda, R)\}$ under optimization over two-delta spectra (which match the infimum of $\lambda_{\min}(\mathcal{F}_p^{(k)}(q))$ at every fixed $(q, k, \mu^*)$ by Theorem 1) behaves as follows:

| $\lambda \backslash R$ | $1.0$ | $1.5$ | $2.0$ | $2.5$ | $3.0$ | $3.36$ | $3.5$ | $4.0$ | $5.0$ | $\inf_{R} r_*(\lambda, R)$ | Active channel $k$ at $\inf_R$ |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| $0.5$ | $\infty$ | $0.578$ | $0.685$ | $0.768$ | $0.835$ | $0.875$ | $0.890$ | $0.941$ | $1.031$ | $0.5000$ ($R \to 0.46^+$) | $k = 1$ |
| $1.0$ | $0.518$ | $0.608$ | $0.692$ | $0.763$ | $0.822$ | $0.858$ | $0.871$ | $0.916$ | $0.992$ | $0.5000$ ($R \to 0.65^+$) | $k = 1$ |
| $2.0$ | $0.500$ | $0.562$ | $0.625$ | $0.680$ | $0.728$ | $0.758$ | $0.770$ | $0.808$ | $0.874$ | $0.5000$ ($R \to 0.93^+$) | $k = 1$ |
| $3.0$ | $\infty$ | $0.525$ | $0.578$ | $0.626$ | $0.668$ | $0.695$ | $0.705$ | $0.739$ | $0.799$ | $0.5000$ ($R \to 1.14^+$) | $k = 1$ |
| $5.0$ | $\infty$ | $0.500$ | $0.528$ | $0.565$ | $0.600$ | $0.622$ | $0.630$ | $0.660$ | $0.712$ | $0.5000$ ($R \to 1.48^+$) | $k = 1$ |
| $10.0$ | $\infty$ | $\infty$ | $\infty$ | $0.511$ | $0.533$ | $0.548$ | $0.554$ | $0.576$ | $0.616$ | $0.5000$ ($R \to 2.10^+$) | $k = 1$ |
| $20.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $0.500$ | $0.508$ | $0.511$ | $0.525$ | $0.552$ | $0.5000$ ($R \to 2.97^+$) | $k = 1$ |
| $25.6$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | **$0.4785$** | $0.502$ | $0.512$ | $0.536$ | **$0.4785$** ($R \approx 3.36$) | **$k = 5$ fold** |
| $26.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | **$0.4795$** | $0.501$ | $0.511$ | $0.534$ | **$0.4795$** ($R \approx 3.26$) | **$k = 5$ fold** |
| $27.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $0.4835$ | **$0.4828$** | $0.508$ | $0.530$ | **$0.4828$** ($R \approx 3.55$) | **$k = 5$ fold** |
| $28.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $0.4875$ | **$0.4860$** | $0.506$ | $0.527$ | **$0.4860$** ($R \approx 3.52$) | **$k = 5$ fold** |
| $30.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | **$0.4910$** | $0.502$ | $0.521$ | **$0.4910$** ($R \approx 3.60$) | **$k = 5$ fold** |
| $35.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $0.500$ | $0.504$ | $0.512$ | $0.5000$ ($R \to 3.93^+$) | $k = 1$ |
| $50.0$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $0.504$ | $0.5000$ ($R \to 4.70^+$) | $k = 1$ |

Here $\infty$ means $4 R^2 < q_E(\lambda, 0)$, where the cutoff lies strictly below the lowest Matsubara frequency at the zero-Coulomb onset ($k = 0$) and Einstein is strictly optimal for all $\mu^* \ge 0$ (Theorem 2).

## 4. Mechanism of the sub-$1/2$ counterexample, physical-extremity caveats, and open questions

- **Why $1/2$ governs small $k$ and moderate $\lambda$:** On $k = 1$, the Coulomb penalty $2\mu^* h_0^2$ touches only index $i = 0$; whenever $\mu^* \le 1 + a_1(q; p)$ (in particular for all $\mu^* \le 1$, or $\lambda \le 2$ with $\mu^*/\lambda \le 1/2$), the modified diagonal $\tilde{D}_{p,i}$ is nondecreasing and the Birman-Schwinger operator forces the ground state $h^*$ of $\mathcal{F}_p^{(1)}(q)$ to be strictly positive and nonincreasing ($h^*_0 \ge h^*_1 > h^*_2 > \dots > 0$), making every $L_j(h^*) < 0$ and proving strict Einstein dominance via Jensen concavity (Theorem 4). For $\lambda \in (2, 151]$ at $\mu^*/\lambda = 1/2$, $k = 1$ Einstein optimality continues to hold numerically even after $h^*_0 \ge h^*_1$ breaks down around $\lambda \approx 20$, and for $k \in \{2, 3, 4\}$ the rank-$1$ critical ratio curve $r_{\mathrm{crit}}^{(k)}(q; \lambda)$ is monotone decreasing across the single-negative-eigenvalue regime (`phase_scan.py`).
- **Why $k = 5$ breaks $1/2$ at $\lambda \in [25.55, 34.0]$:** At $k = 5$ and $q \approx 0.40\text{--}0.60$, the lowest eigenvalue of the zero-Coulomb operator and the $k = 5$ mask overlap vary at different rates, producing a non-monotone S-curve in $\lambda_{\min}(\mathcal{F}_{\delta_1}^{(5)}(q))$ just below the $k = 5 \to 4$ cutoff step $q_c = 4 R^2 / 81$. Lowering the main phonon line to $u_1 \in [0.64, 0.88]$ (with a tiny weight $p_2$ at $u_2 \in [10^3, 2 \times 10^4]$ to preserve $\int u\,dp = 1$) reduces the normal self-energy mass $2\sum_{j=1}^i a_j(q; p)$ on the unmasked modes $i \ge 5$ where the screened sign-changing eigenvector $h^*$ concentrates, triggering instability inside Einstein's stable island $[q_{E,\mathrm{hi}}, q_c)$.
- **Model scope and physical-extremity caveats:**
  1. *Sharp-cutoff linearized model:* All theorems and counterexamples in this folder apply to the linearized onset $T_{\mathrm{lin}}$ in the sharp-cutoff isotropic Migdal-Eliashberg model with pairing-only Coulomb mask $c_n = \mathbf{1}_{|\omega_n| < \omega_c}$.
  2. *Ultra-strong coupling and large $\mu^*$:* The sub-$1/2$ counterexamples require $\lambda \in [25.55, 34.0]$ ($\lambda = 25.6\text{--}28$) and $\mu^* \approx 12.25\text{--}13.69$, orders of magnitude above conventional physical electron-phonon couplings ($\lambda \lesssim 3\text{--}4$, $\mu^* \approx 0.1\text{--}0.2$). In the physical range $\mu^* \le 1$ (and for all $\lambda \le 2$ with $\mu^*/\lambda \le 1/2$), Theorem 4 proves unconditional $k=1$ Einstein optimality, and numerically $r_*(\lambda, R) \ge 1/2$ for all $\lambda < 25.55$.
  3. *Extreme two-line frequency separation:* The counterexample mixtures place a tiny weight $p_2 \in [6 \times 10^{-6}, 3.6 \times 10^{-4}]$ at a stiff mode $u_2 = (\Omega_2/\Omega_E)^2 \in [10^3, 2 \times 10^4]$ ($\Omega_2/\Omega_E \approx 31.6\text{--}141.4$) solely to pay the second-moment constraint $\int u\,dp(u) = 1$ while shifting the active mode to $u_1 < 1$.
  4. *Dependence on the sharp $k = 5 \to 4$ Matsubara step:* The sub-$1/2$ instability window $q_{\mathrm{mix}} \in (q_{E,\mathrm{hi}}, 4 R^2 / 81)$ exploits the discontinuous jump of the sharp cutoff indicator $c_n = \mathbf{1}_{(2n+1)^2 q < 4 R^2}$ as the fifth positive Matsubara frequency $2i+1 = 9$ crosses $\omega_c$.
- **What remains open:**
  1. Closing an analytic proof of Einstein optimality on the fixed $k = 1$ branch for $\lambda \in (2, 151]$ when $\mu^* > 1 + a_1(q; p)$ (where $h^*_0 \ge h^*_1$ no longer holds) and for $k \in \{2, 3, 4\}$ across $\mu^*/\lambda \le 1/2$ (verified numerically in `phase_scan.py`).
  2. Proving analytically that $\lambda_{\mathrm{crit}} \approx 25.55$ is the exact lower coupling boundary for sub-$1/2$ counterexamples across all $k \ge 5$.

## 5. Files and verification commands

All files live in `D:/dev/scratch/ceiling-20261118/C-LAMBDA-MU/MUSTAR-HALF/`:
- `RIGOR.md`: Mathematical derivations, Lemma 1 and Theorems 1–5 (proof drafts), and exact rational/integer certificate specifications.
- `RESULT.md`: This summary of status, theorems, sub-$1/2$ counterexamples, phase diagram, physical-extremity caveats, and open questions.
- `FIX.md`: Per-finding repair log for `REVIEW.md` F3–F8 with file:line references and verification command exit codes.
- `fixtures.json` & `bounds.json`: Exact rational inputs and rational certificate brackets for the 4 sub-$1/2$ counterexamples and 4 anchors.
- `replay.py`: Primary exact-integer / rational certificate verifier (`--mutant {coulomb,spectrum,endpoint,tail,sign}` all exit 1).
- `independent.py`: Secondary verifier using the **unfolded full-line** quadratic form on $\{-N_C, \dots, N_C-1\}$ in exact `Fraction` arithmetic (cold side) and an independent hot-side enclosure + Hutton's $\pi$ formula (no import of or from `replay.py`); `--selfcheck` and `--adversarial` exit 0, and all eight mutants
  (`--mutant {entrywise,v1pen,rsign,overflow,endpoint,coulomb,spectrum,receipt}`) exit 1.
- `structure.py`: Exact rational arithmetic verification of the algebraic identities and theorem hypotheses in `RIGOR.md`, including F4 refutation witnesses (`--mutant {coulomb,f4,norm}` and bare `--mutant` all exit 1).
- `phase_scan.py`: Numerical verification of the unfolded-to-folded matrix identity, the $k \in \{1, 2, 3, 4\}$ optimality scan at $\mu^*/\lambda = 1/2$, and the $k = 5$ re-entrant fold scan across $\lambda \in [25, 35]$ (`--mutant` exits 1).
- `CHECKS.txt`: Exact commands and recorded exit codes.
