# Sharp fixed-coupling ceiling: proof and replay contract

**Scope.** Standard isotropic, constant-DOS (A=1), infinite-band linearized Migdal–Eliashberg model, with zero Coulomb term and equal phonon transfers in the normal and anomalous equations. The onset is the first loss of normal-state linear stability on cooling. Here τ=k_B T, phonon arguments Ω>0 are *energies* (not angular frequencies), λ>0 is finite, and 0<M<∞. The proof below is self-contained in this model; see the literature disposition in `RESULT.md` for priority. It makes no claim for an observed transition, anisotropic pairing, a nonflat DOS or finite bands. Status: mathematical proof supplied, independent human review pending.

## 1. Folded stability operator

For the nonnegative spectral measure μ(dΩ)=α²F(dΩ), write

```
λ = 2∫ μ(dΩ)/Ω,     M = 2∫ Ω μ(dΩ),     p(dΩ)=2 μ(dΩ)/(λΩ),
a_j(τ) = λ ∫ Ω²/[Ω²+(2πτj)²] p(dΩ),  a_0=λ,  a_{-j}=a_j.
```

Thus p is a probability with mean square M/λ. For τ>0 the transfers a are positive, decreasing in |j|, and absolutely summable, since a_j≤M/(2πτj)² for j≠0. In the full integer equation use f_n=Δ_n/|ω_n|, ω_n=πτ(2n+1). The normal term in units πτ is 2∑_{j=1}^{l(n)}a_j+a_0, where l(n)=max(n,−n−1): for n≥0, the positive and negative Matsubara sums of a cancel except a_0+2∑_{j=1}^n a_j. Thus the uncanceled stability form is diagonal |2n+1|+a_0+2∑_{j=1}^{l(n)}a_j minus the convolution a_{n−m}. This symmetrizes the linearized problem and gives the stated signs and factor of two.

The normalized convolution (divide left and right by the square root of that diagonal) is compact, self-adjoint and positivity improving. Compactness follows from the diagonal inverse square root tending to zero and a∈ℓ¹; positivity follows entrywise. Its spectral top is positive, simple and strictly greater in modulus than every other eigenvalue: replacing an eigenvector by its absolute value increases the Rayleigh numerator unless it has one sign, and the strictly positive entries force a sign-definite principal eigenvector to be strictly positive; orthogonality then excludes another principal eigenvector. Equality in the triangle inequality with a positive diagonal entry rules out a negative eigenvalue of opposite magnitude. Reflection n↦−n−1 preserves the operator, so its unique positive principal vector is even. First instability is therefore captured by reducing to n≥0, regardless of the other sectors.

Set d_n=2n+1 and A_{nm}=a_{n+m+1}+1_{n≠m}a_{|n−m|}. With even reflection the folded form (half the full quadratic form on reflected vectors) is

```
F = diag(d_n + 2∑_{j=1}^n a_j) − A,
S = diag(d_n)^(-1/2) [A − diag(2∑_{j=1}^n a_j)] diag(d_n)^(-1/2),
g(τ)=max σ(S).
```

The reflection includes n+m+1, and the a_0 from convolution cancels against the normal a_0. The compact operator S has g≥S_00=a_1>0. F has form domain ∑d_n|f_n|²<∞ with finite-support core; all non-bare terms are bounded by summability. F is positive for g<1, has a null vector at g=1, and has a negative direction for g>1.

## 2. Transfer comparison accounts for normal mass

Entrywise dominance of the pairing kernel alone does **not** suffice because increasing a_j also increases the negative normal term in S. Instead the top S trial f_n=(diag(d_n)^(-1/2)x)_n can be taken strictly positive and nonincreasing. To see this, set D_n=a_0+2∑_{j=1}^n a_j+g d_n. The top eigen-equation for S is Kf=Df, with K_{nm}=a_{|n−m|}+a_{n+m+1}. The compact B=D^(-1/2) K D^(-1/2) has top 1: the Rayleigh inequality for S gives B≤I (first on finite supports), and D^(1/2)f is square summable and solves Bv=v, since D_n/d_n is bounded. The positive eigenvector and spectral separation follow as in §1.

If h≥0 is decreasing on n≥0, reflect it about −1/2. Convolution on Z by a preserves this property: express the reflection as nonnegative layers of indicators of blocks [−L−1,L]. For one block the difference between consecutive convolved values at n,n+1, n≥0, is a_{n−L}−a_{n+L+2}≥0. Division by the increasing D_n also preserves it. Start the iteration D^(-1)K at e_0; conjugate by D^(1/2) to B. The iterates converge in the latter ℓ² coordinates to a nonzero multiple of the positive top vector, because the projection is positive and all other eigenvalues have modulus below 1. Componentwise limits preserve the order. This proves the asserted shape of f.

For this f, the coefficient of each a_j (j≥1) in ⟨f,(diag(d)−F)f⟩ is

```
L_j(f) = 2∑_{n≥0} f_{n+j}(f_n−f_{n+j}) + ∑_{n=0}^{j−1} f_n f_{j−1−n} > 0.
```

The sums converge; the second sum is strictly positive, and |L_j| is bounded by a constant times ||f||² uniformly in j. Hence if ã_j≥a_j for every j≥1, with one strict inequality, g̃>g: evaluate the larger operator at the *smaller* one's positive decreasing maximizing trial, normalizing ∑d_n f_n²=1. The argument also compares kernels whose a_0 differ: a_0 cancels identically in F.

## 3. Single Einstein optimizer and exact formula

At fixed τ, for every j≥1 the function x↦x/(x+(2πτj)²) on x≥0 is strictly concave (second derivative −2(2πτj)²/[x+(2πτj)²]³). By Jensen, every a_j is at most the Einstein a_j with Ω_E=√(M/λ); equality anywhere holds iff Ω²=M/λ almost surely. Combined with §2, this maximizes the stability top strictly at every positive τ. In particular a single spike with measure `(λΩ_E/2) δ_{Ω_E}` is the unique optimizer, not just a two-point extreme measure. A restriction to ≤2 spikes from convexity of the spectral maximum would not identify the optimum and would need a separate argument for the noncompact moment set; strict comparison bypasses that issue.

For any fixed admissible spectrum, g(τ) is continuous for τ>0 by ℓ¹ dominated convergence and strictly decreases by §2. Its hot limit is 0 by the ℓ¹ majorant proportional to τ⁻². For the cold limit every fixed transfer tends to λ. For f_n=(2n+1)⁻¹ on 0≤n<N (zero outside), the quotient for S tends as τ→0 to `2λ ∑_{n<N}(2n+1)⁻¹−λ`, unbounded as N→∞. Its unique root g=1 is therefore precisely T_lin; evaluating a non-Einstein spectrum at the Einstein root gives g<1 and a strictly lower onset.

A sharp scalar spectral formula for every λ>0 is

```
q = (2πτ/Ω_E)²,      a_j = λ/(1+q j²),
q_λ = the unique q>0 for which max σ(S_E(q;λ))=1,
C(λ) = sqrt(q_λ/λ)/(2π),      τ_lin ≤ C(λ) sqrt(M).
```

Equality is attained by the Einstein witness. This is a spectral formula, not an elementary fit. At fixed M, the Einstein transfers `1/[1/λ + (2πτj)²/M]` increase strictly with λ, with ℓ¹ convergence for j≠0 to `M/(2πτj)²` as λ→∞. The latter gives the existing γ=2 stability top, proportional to τ⁻², and its crossing is τ=C∞√M (see `../G3X/RESULT.md` and `../GAMMA/RIGOR.md`). To apply §2 to the limiting transfers, extend them by a finite a_0≥a_1, which cancels. This gives C(λ)<C∞ for every finite λ. Norm convergence at every τ>0 gives C(λ)↑C∞ by testing temperatures just below the limiting crossing; the inequality is strict between every pair of finite λ. The vanishing-transfer index j=0 does not enter this limit argument because its cancellation is exact at every finite λ.

## 4. Exact enclosures on the infinite lattice

Both scripts are proof replays, not finite-size convergence claims. Float SciPy is used only to propose positive rational trial vectors. Correctness of each returned sign uses integers and rational arithmetic only. The bracket file holds rational squared dimensionless T endpoints q; the monotonicity in §3 makes a negative form at q_lo plus positivity at q_hi a strict enclosure. One may set M=1 eV² for explicit witnesses at all rows, so Ω_E=1/√λ eV and the spike coefficient is √λ/2 eV; scale the spectrum uniformly for any other M. For the decimal C enclosure, `replay.py` encloses π using Machin's identity 16 atan(1/5)−4 atan(1/239) and alternating series tails, then encloses the square root with exact integer arithmetic and rounds outward.

### Folded block proof (`replay.py`)

At a cold endpoint an integer vector on the first N indices, extended by zero, has a negative quadratic form after rounding all attractive terms down and all normal terms up. At a hot endpoint split P=[0,N), Q=[N,∞). Let b=λ/q. The full folded row sum of A is `2∑_{j≥1}a_j`; indeed the missing terms in the Toeplitz row are restored by the Hankel row. Consequently

```
F_QQ ≥ δ I,     δ = 2N+1−2b/N > 0,
```

by diagonal dominance (or |2xy|≤x²+y²) and `∑_{j>N} j⁻²≤1/N`. For i<N and r=N−i≥1, `||A_QP e_i||₂ ≤ u_i = 2b sqrt(r^(-4) + 1/(3r³))`, since each `A_ji≤2b/(j−i)²` and the decreasing-series remainder is bounded by integration. For any real v, `||A_QP v||²≤(∑u_i|v_i|)²`; this does not assert Loewner dominance by uuᵀ on signed vectors. The Schur complement therefore dominates `|v|ᵀ(F_PP−uuᵀ/δ)|v|` as a form: the off-diagonals of F_PP are nonpositive. A strictly positive h with `(F_PP−uuᵀ/δ)h>0` proves this comparison matrix positive definite via conjugation by diag(h) and strict row dominance. The code rounds u and attractive entries upward, normal entries downward. Completing the square controls Q without truncating its normal term or any Matsubara tail. This proves strict stability; alternatively compactness plus absence of a null vector gives a gap in the normalized problem.

### Signed-lattice proof (`independent.py`)

Uses the uncanceled convolution on [−N,N−1], not S or its Schur complement. Its lower endpoint is a separate signed-lattice Rayleigh witness using exact rounded bounds. For the high endpoint it constructs a positive infinite vector h by reflecting the positive half-head and appending `h_j=t/(j+1)³` for j≥N. Let B be the exact upper bound `a_0+2(∑_{k=1}^N a_k+b/N)` on the full convolution row sum. For tail j, split positive source m≥N by m+1≥(j+1)/2. The near part costs at most `8B h_j`. In the far part each folded coefficient is bounded by `5b/(j+1)²`, from distances `j−m≥(j+1)/2` and `j+m+1≥j+1`, and `∑_{m≥N} h_m ≤ t/(2N²)`, so the far tail-to-tail sum at site j is bounded by `5bt/[2N²(j+1)²] = [5b/(2N²)](j+1) h_j`. Write `loss = 5b/(2N²)` and

```
L_j = (2−loss)(j+1) − (1+8B),      t = ceil(max(far, near)) + 1,
```

where `near` runs over N≤j<2N of `(j+1)³ (K_QP h)_j/L_j` using upward-rounded entries, and `far = 5b ∑_{i<N}h_i/[(2−loss)−(1+8B)/(2N+1)]` covers j≥2N because `L_j/(j+1)` increases. The remaining tail margin is at least `L_j h_j`, which exceeds the head-to-tail source. The normal term is simply dropped for this tail estimate and retained exactly for the head. The omitted tail-to-head sum at j≥2N is at most `5bt/(4(2N)^4)` by integration of (j+1)^−5. The finite near feed is summed with rational upper bounds, verifying strictly positive rows on the head too.

A positive vector h with strict rows for the full form proves positivity on the untruncated space. For a finite trial v, `2|v_i v_j|≤h_j v_i²/h_i+h_i v_j²/h_j` shows the quadratic form bounded below by the positive row margins times v_i²/h_i. Density of finitely supported trials in the form norm, and nonnegative limiting lower margins, exclude a nonzero null vector. Compactness of the diagonally normalized convolution then puts its spectral top strictly below 1. This proof has no spectral-tail norm estimate in common with the folded block proof. Both scripts include explicit failure checks for reversed endpoint roles and for wrong mass and reflection terms.
