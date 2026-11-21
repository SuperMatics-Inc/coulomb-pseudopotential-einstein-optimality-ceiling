# Common-cutoff certificates: model, folding, and the exact devices

## 1. Model

Flat density of states $N_0$, infinite electronic band, isotropic even linear
Migdal-Eliashberg pairing at the onset, in the conventions of
[the bracket-and-mustar records](../the bracket-and-mustar records/RIGOR.md) and [C-LAMBDA](../../C-LAMBDA/RIGOR.md):

- energies in absolute units, Matsubara frequencies $\omega_n=(2n+1)\pi k_BT$;
- $\lambda=2\int_0^\infty\alpha^2F(\omega)\omega^{-1}d\omega$,
  $M=2\int_0^\infty\alpha^2F(\omega)\omega\,d\omega$,
  $\Omega_E=\sqrt{M/\lambda}$, $u=\omega^2/\Omega_E^2$,
  $dp=2\alpha^2F(d\omega)/(\lambda\omega)$ a probability measure with $\int u\,dp=1$;
- transfer weights $a_j=\lambda\int u/(u+qj^2)\,dp$ with $q=(2\pi k_BT/\Omega_E)^2$,
  so $a_0=\lambda$, $a_j>0$, and $\sum_j a_j$ is finite;
- **pairing-only** repulsion $\mu^*c_nc_m$ with $c_n=1_{|\omega_n|<\omega_c}$, applied
  to the pairing kernel only, never to the normal self-energy $Z$;
- $\omega_c$ **common**: one number per instance, the same for every spectrum compared
  at that instance.

The linearized isotropic gap equation is the eigenproblem
$\lambda_{\max}(D^{-1/2}KD^{-1/2})=1$ with the pairing kernel
$K_{nm}=a_{|n-m|}-\mu^*c_nc_m$ and the exact normal-state diagonal
$D_n=Z_n|\omega_n|=|\omega_n|+a_0+2\sum_{j=1}^{i(n)}a_j$, $i(n)=\max(n,-n-1)$; in the
folded even-frequency coordinates of §4 it is the stability condition
$\mathcal F\succeq0$ for the quadratic form below.

## 2. Reduction at fixed $(\lambda,M)$ (PROVED)

Fix $\lambda$ and $M$; then $\Omega_E$ is fixed and any two spectra with the same
$(\lambda,M)$ share $\Omega_E$. Rescaling all frequencies by $\Omega_E$ maps an instance
to $(q, R^2,\mu^*)$ with $R=\omega_c/\Omega_E=\omega_c\sqrt{\lambda/M}$, and the mask is
determined by $(2i+1)^2q<4R^2$ (equivalently $|2i+1|\pi k_BT<\omega_c$). The onset is a
function of $(\lambda,R^2,\mu^*)$ only. Two spectra therefore compete on the same
footing iff they have equal $\lambda$, equal $M$, and they are compared at equal
$R$. In the fixtures all mixed spectra satisfy $\sum_i\lambda_i=\lambda$ and
$\sum_i\lambda_iv_i=\lambda$, so $M$ and $\Omega_E$ coincide with Einstein's and $R^2$ is
literally the same rational number.

## 3. Transfer kernel (PROVED)

For a spectrum $\{(\lambda_i,u_i)\}$ with $\sum\lambda_i=\lambda$ and
$\sum\lambda_iu_i=\lambda$, the weights are the exact rational functions
$a_r=\sum_i\lambda_iu_i/(u_i+qr^2)$.

(i) $a_r>0$ and $a_0=\lambda$.

(ii) **Einstein dominates entrywise**: for $q>0$ and $r\ge1$ the map
$u\mapsto u/(u+qr^2)$ is concave on $(0,\infty)$, and $\int u\,dp=\int dp=1$, so
$$a_r=\lambda\int\frac{u}{u+qr^2}\,dp\le\lambda\frac{\int u\,dp}{\int u\,dp+qr^2}=\frac{\lambda}{1+qr^2}=a_r^{\rm E}.$$
Equality for some $r\ge1$ (strictly concave map, non-degenerate spectrum) iff the
spectrum is the single line. This is the Jensen step behind the zero-Coulomb ceiling.

(iii) For the two-line family the map $(p,u_1,u_2)\mapsto a_r$ is explicit:
$a_r=\lambda\big((1-p)u_1/(u_1+qr^2)+pu_2/(u_2+qr^2)\big)$ with
$u_1=(1-pu_2)/(1-p)$. Every counterexample below is such a pair at rational
$(p,u_1,u_2)$.

Exact finite-sample confirmation: `structure.py` (400 random rational two-line spectra,
six values of $r$, exact rational inequalities; `--mutant` refuses rescaled spectra
whose second moment is wrong).

## 4. Folded stability form and the Coulomb block

**Reduction to the folded half-line (exact).** With $a_r=\lambda\int u/(u+qr^2)\,dp$ and
$a_0=\lambda$, on the full Matsubara line ($|\omega_n|=|2n+1|\pi T=2\pi T|n+\tfrac12|$) the
normal self-energy of this model is
$$Z_n|\omega_n|=|\omega_n|+\frac{\pi T}{|\omega_n|}\sum_m a_{|n-m|}\,{\rm sgn}\,\omega_m
=\pi T\Big[d_{i(n)}+a_0+2A_{i(n)}\Big],\qquad A_i=\sum_{j=1}^{i}a_j,$$
because $\operatorname{sgn}\omega_m=\operatorname{sgn}(2m+1)$ alternates and
$\sum_{m\ne n}a_{|n-m|}{\rm sgn}\,\omega_m\,{\rm sgn}\,\omega_n=a_0+2A_{i(n)}$ with
$i(n)=\max(n,-n-1)$ the folded index of $n$. The pairing kernel is
$K_{nm}=a_{|n-m|}-\mu^*c_nc_m$, and the linearized gap equation is
$\lambda_{\max}(D^{-1/2}KD^{-1/2})=1$. On the even subspace, $h_n=h_{-n-1}$ (the folds
$n=(i,-i-1)$ with $d_i=|2i+1|=2i+1$), the quotient $h^{\rm T}Kh/h^{\rm T}Dh$ equals
$$1-\frac{\mathcal F(h)}{\sum_{i\ge0}\big(d_i+a_0+2A_i\big)h_i^2},$$
(the full-line form of $D-K$ is **twice** the folded $\mathcal F$, and the full-line
$h^{\rm T}Dh$ is twice the half-line sum, so both factors of two cancel; checked in exact
rationals on random $h$ with a finite $a$-list) whose denominator is positive for $h\ne0$, so the medium is stable iff
$\mathcal F(h)\ge0$ for every $h$, i.e. iff the folded matrix below is positive
semidefinite. This is the criterion every script tests.

**Matrix form (primary identity, exact and finite).** For $i,j\ge0$ put
$$F^{(n)}_{ij}=\delta_{ij}\big(d_i+2A_i\big)-\mathbf 1_{i\ne j}\,a_{|i-j|}-a_{i+j+1}
+\mathbf 1_{i,j<k}\,2\mu^*,$$
that is, with $h$ of finite support and the sums over the full half-line,
$$\mathcal F(h)=\sum_{i\ge0}(2i+1+2A_i)h_i^2-2\sum_{i<j}a_{j-i}h_ih_j
-\sum_{i,j\ge0}a_{i+j+1}h_ih_j+2\mu^*\Big(\sum_{i<k}h_i\Big)^2 .$$
The $a_0$ content of $Z_n$ cancels against the $a_0$ on the diagonal of $K$ (both because
$\int u\,dp=\int dp=1$ fixes $a_0=\lambda$ as a plain constant), so $a_0$ appears in
neither the mass nor the folded diagonal; it survives only through the scale $q$.

**Display (Laplacian) form (equivalent, needs the tails).** Using
$\sum_{i<j}a_{j-i}(h_i-h_j)^2=S_1\sum_ih_i^2+\sum_jA_jh_j^2-2\sum_{i<j}a_{j-i}h_ih_j$ with
$S_1=\sum_{r\ge1}a_r$, and
$\sum_{i,j}a_{i+j+1}(h_i-h_j)^2=2\sum_ih_i^2T_i-2\sum_{i,j}a_{i+j+1}h_ih_j$ with
$T_i=\sum_{r>i}a_r=S_1-A_i$, the same form reads
$$\mathcal F(h)=\underbrace{\sum_{i\ge0}(2i+1)h_i^2-2\sum_{i\ge0}h_i^2\sum_{r>i}a_r
+\tfrac12\sum_{i,j\ge0}a_{|i-j|}(h_i-h_j)^2
+\tfrac12\sum_{i,j\ge0}a_{i+j+1}(h_i-h_j)^2}_{\mathcal F_0(h)}
+2\mu^*\Big(\sum_{i<k}h_i\Big)^2 .$$
Three points of bookkeeping matter and were wrong in an earlier draft: the two Laplacian
sums carry $1/2$ (each unordered pair is counted twice), the diagonal carries
$-2\sum_{r>i}a_r$ (with $T_i=S_1-A_i$, the coefficient of $h_i^2$ is
$(2i+1)-2T_i$, not $(2i+1)-T_i$), and there is no separate $-2\sum_{i<j}a_{j-i}h_ih_j$
term or further $a_0$ subtraction (double counting). In the display the sums run over the
*full* half-line: for finitely supported $h$ the pairs $(i,j)$ with $j\ge0$ and $j\ge n$
contribute $a_{|i-j|}h_i^2$ and are not optional.
Exact verification: `structure.py --folded` checks the matrix form against this display in
exact rationals (120 random rational trials, mixed-sign and all-positive $h$, random
two-line spectra, random $\mu^*$, random mask $k$), and
`structure.py --folded --mutant` confirms that the display *without* the tail term
differs from the matrix in every trial (so the test detects the error it was written to
catch). `crosscheck.py` builds $F$ directly from the full Matsubara line and reproduces
the folded form.

**Coulomb block.** The strict pairing-only mask restricts the repulsion to folded indices
$i<k=\#\{i: d_i^2q<4R^2\}$ and adds the positive semidefinite rank-one term
$2\mu^*(\sum_{i<k}h_i)^2$. The sign is the important structural fact: the repulsion
**raises** $\mathcal F$ on the masked block, but only along the all-ones direction of that
block; on the orthogonal directions it does nothing, so at $\mu^*>0$ every form is the
$\mu^*=0$ (phonon) form plus the same rank-one term, and the term's effect on the relevant
test direction is $\mu^*(\sum_{i<k}h_i)^2/\sum_id_ih_i^2$, which is large for a witness
spread over the mask and vanishes for one orthogonal to the masked all-ones direction,
while the zero-Coulomb margin being overcome is spectrum dependent. The $\mu^*$-independent
Einstein ceiling of §3(ii) bounds the phonon entries $a$ only; there is therefore no
ordering theorem transferring Einstein dominance from $a$ to the forms at $\mu^*>0$, and
no argument in either direction for $\mu^*<0$ (the rank-one term then lowers every form).
The $\mu^*>0$ case is a genuine competition, which is what the counterexamples exploit.
Because the rank-one term only raises forms, a mixture that is indefinite at $\mu^*>0$ is
necessarily indefinite already at $\mu^*=0$; what the Coulomb does is to remove the
*Einstein* instability far more effectively than the mixture's (direct full-line values at
the wide witness $q=1/200$, straight from today's `crosscheck.py`:
$\lambda_{\max}$ $4.4033\to0.7556$ for Einstein against $3.2054\to1.0975$ for the
mixture, the two numbers of a pair being $\mu^*=0$ and $\mu^*=3/2$). The $\mu^*=0$ ordering is the case covered by the C-LAMBDA
ceiling; the $\mu^*>0$ ordering is not implied by it, and the certificates below settle it
case by case.

## 5. Certificate architecture (`replay.py`, `independent.py`)

Both verifiers work with exact rationals for every quantity that enters a sign
decision; floating point is used only to generate trial vectors and to seed brackets,
and no floating comparison is ever the final word.

**Cold witness (instability).** At a rational $q$ a rational integer vector $x$ on the
first $n$ folds is produced and **extended by zero beyond the head**. For a finitely
supported $x$ the folded form of the infinite model is exactly the finite quadratic form
$\sum_{i,j<n}x_iF_{ij}x_j$: every pair with $j\ge n$ multiplies $x_j=0$, and the weights
$a_r$ needed are the rational $a_r$ with $r\le2n-1$, all of which are computed. No tail
bound is involved (an earlier draft claimed one; there is none). `replay.py` evaluates
this finite form as
$$\mathcal F(x)\le\sum_i x_i\big(d_ix_i-y_i\big)+\lceil 2\mu^*S\rceil\Big(\sum_{i<k}x_i\Big)^2,$$
with $d_i\ge S(d_i+2A_i)$ and $y_i$ the contraction of the pair block in which every entry
$a_{|i-j|}+a_{i+j+1}$ is replaced by an upper bound when $x_ix_j<0$ and by a lower bound
when $x_ix_j>0$; the integer right-hand side is then an upper bound of $S\mathcal F(x)$,
and a negative value certifies $\mathcal F(x)<0$ in the infinite model. Entries are scaled
by $S=2^{30}$ and accumulated in unbounded integers wherever the int64 fast path is not
provably safe (see `contraction`).

**Hot certificate (no instability).** Positivity of the infinite form is certified on a
whole interval $[q_{\rm hi},q_{\rm ph})$ up to the zero-Coulomb phonon endpoint
$q_{\rm ph}(\lambda)$ taken from `../../C-LAMBDA/brackets.json` (there the form is
positive without the repulsion, and the repulsion only adds a positive semidefinite
term, so no further work is needed beyond that endpoint). The interval is split into
windows $[l,u)$ on which the mask is constant (`windows`), and inside a window a head
matrix is formed, its tail eliminated by a Schur complement with a rigorous magnitude
bound (`far_lump`), and positivity of the head certified by an integer device: a floating
Cholesky of the scaled matrix with a fixed shift, an integer reproduction of the factor,
an exact residual, and strict diagonal dominance of the residual (`gram_positive`). If
any window fails, `cover` bisects adaptively.

**Brackets.** For each instance the receipt records
$[q_{\rm lo},q_{\rm hi}]$ with a cold witness at $q_{\rm lo}$ and a hot certificate on
$[q_{\rm hi},q_{\rm ph})$, and the rational enclosure
$C_E=\sqrt q/(2\pi\sqrt\lambda)$ obtained by directed rounding of $\sqrt{q/(4\lambda\pi^2)}$
with rational arctangent bounds for $\pi$ (`pi_bounds`, `c_bounds`).

**Independence.** `independent.py` shares no code and no formulation with `replay.py`.

* Cold side: the form is evaluated on the **unfolded** full Matsubara line
  $n\in\{-N,\dots,N-1\}$ ($N=400$, $800$ modes) with $a_0=\lambda$ retained, as
  $\sum_n f_n^2D_n-\sum_{nm}f_nf_mK_{nm}$, rewritten as one integer correlation
  $c_d=\sum_nf_nf_{n+d}$ times the exact rational weights; the folding of §4 (and hence the
  mirror term $a_{i+j+1}$ and the $a_0$ cancellation) is never used, so the two verifiers
  agree only if the folding is right. The witness is the rounded generalized eigenvector of
  $Kx=\lambda_{\max}Dx$ and the value is then recomputed exactly for that integer vector.
* Hot side: the same folded display matrix, but a genuinely different *device*, valid for
  every real vector (no entry sign, no Z-matrix statement, is used anywhere). Write the
  folded form as the single infinite symmetric matrix $F$ on modes $i\ge0$, with
  $a_r=\lambda\sum_ip_iu_i/(u_i+qr^2)$, $a_0=0$, $A_i=\sum_{r\le i}a_r$:
  $$F_{ii}=2i+1+2A_i-a_{2i+1}+2\mu_*\,[i<k],\qquad F_{ij}=-(a_{|i-j|}+a_{i+j+1})\ (i\ne j),$$
  where $k$ is the mask width of the window. `independent.py` splits that one matrix at the
  fixed head size $m=\max(160,2k+1)$ (`hot_head`), so that (a) no mode is omitted (the tail
  starts exactly at mode $m$, never later than the head ends) and (b) $m\ge2k+1$ puts the
  whole $\mu_*$ block inside the head, so the tail carries no Coulomb term at all.
  Positivity is then certified by two PSD-domination steps and one exact decision.
  1. *Entrywise enclosure.* $a_r(q)$ is decreasing in $q$, so on a window $[l,u)$ each head
     entry lies between its value at $u$ (smaller magnitude) and at $l$, both rounded
     outward: $\text{lower}_{ij}=-\lceil2^{17}(a_{|i-j|}(l)+a_{i+j+1}(l))\rceil$ and
     $\text{upper}_{ij}=-\lfloor2^{17}(a_{|i-j|}(u)+a_{i+j+1}(u))\rfloor$, so
     $\text{lower}_{ij}\le2^{17}F_{ij}\le\text{upper}_{ij}$ for every $q\in[l,u)$ and every
     $i\ne j$. The diagonal $2i+1+2A_i-a_{2i+1}+2\mu_*[i<k]$ is bounded below, one-sidedly, by
     its value with $A_i$ taken at $u$ (a lower bound because $A_i(q)$ is *decreasing* in $q$)
     and $a_{2i+1}$ at $l$, with $2\mu_*$ floored. With the integer centre
     $C_{ij}=\lfloor(\text{lower}_{ij}+\text{upper}_{ij})/2\rfloor$ (`center`) and radius
     $\mathcal R_{ij}=\max(\text{upper}_{ij}-C_{ij},\,C_{ij}-\text{lower}_{ij})
     =\lceil(\text{upper}_{ij}-\text{lower}_{ij})/2\rceil\ge0$
     (`radius`; diagonal $\mathcal R_{ii}=0$, the diagonal deviation being one-sided and
     dropped) we have $C-\mathcal R\le\text{lower}$ and $\text{upper}\le C+\mathcal R$
     entrywise: the radius covers BOTH ends of the bracket, so $|2^{17}F_{ij}-C_{ij}|\le
     \mathcal R_{ij}$ holds on every off-diagonal entry (odd brackets included), and hence
     $F\succeq C-\mathcal R$ on the head block, for all real vectors.
  2. *Radius as a diagonal domination.* Let $h>0$ and $\rho_i=\lceil\frac1{h_i}\sum_j\mathcal R_{ij}h_j\rceil$
     (`head_radius`, exact integer row sums with $h_i=2^{22}/(i+1)$, one ceiling per row).
     By AM-GM, $2|x_ix_j|\le x_i^2h_j/h_i+x_j^2h_i/h_j$, so for every real $x$
     $\sum_{i\ne j}\mathcal R_{ij}|x_ix_j|\le\sum_i\rho_ix_i^2$, hence
     $C-\mathrm{diag}(\rho)\preceq F$ on the head block. The radius is subtracted **on the
     diagonal only**; nothing is subtracted entrywise.
  3. *The infinite tail.* Row $j\ge m$ of $F$ has diagonal $2j+1+2A_j-a_{2j+1}$. Since
     $a_r\le\lambda/(l\,r^2)$ for $r\ge1$ ($\sum_ip_iu_i=1$), the absolute row sum of its
     off-diagonal entries inside the tail is at most $A_{j-m}(l)+S_1(l)+S_{j+m+1}(l)$ with
     $S_T=\sum_{r\ge T}a_r$. Fix $q\in[l,u]$ FIRST: the $a_r(q)$ are nonnegative, so $A_r(q)$
     is increasing in $r$ and
     $2A_j(q)-A_{j-m}(q)=A_j(q)+\sum_{t=j-m+1}^{j}a_t(q)\ge A_j(q)\ge A_m(q)$ for every
     $j\ge m$. Only then pass to the endpoints, term by term: $A_j(q)\ge A_j(u)$,
     $A_{j-m}(q)\le A_{j-m}(l)$, $a_{2j+1}(q)\le a_{2j+1}(l)$ and $A_m(q)\ge A_m(u)$
     ($A_r$ is decreasing in $q$). Hence **every** gap is at least
     $$g=2m+1+A_m(u)-a_{2m+1}(l)-S_1(l)-S_{2m+1}(l)>0,$$
     uniformly over the infinitely many tail rows (`tail_gap`); $S_1$ is summed exactly to
     $R=8m+8$ terms and closed by $\sum_{r>R}r^{-2}\le1/R$, and
     $S_{2m+1}\le\lambda/(2ml)$ because $\sum_{r>2m}r^{-2}\le1/(2m)$. So the tail block
     $T$ satisfies $T\succeq gI$ (a Gershgorin statement about the whole infinite tail, not
     a bound taken from a finite truncation). Splitting $F=\begin{pmatrix}H&B^T\\B&T\end{pmatrix}$
     and completing the square in the tail variable gives, for every real $(x,y)$,
     $x^THx+2x^TB^Ty+y^TTy\ge x^T(H-\tfrac1gB^TB)x$; column $l\ge m$ of $B$ obeys
     $|B_{il}|=a_{|i-l|}+a_{i+l+1}\le2\lambda/(l(l-m+1)^2)$, so
     $\theta_i=\lceil\frac1g\sum_{j}\sum_{l=m}^{L}b_{il}b_{jl}\rceil$ (`tail_penalty`, integer
     $b_{il}\ge|B_{il}|$ rounded up at scale $2^{17}$, exact $l$-sums to $L=8m$, and the far
     columns $l>L$ bounded by $m(2\lambda/l)^2/(3(L-m)^3)$) dominates the whole quadratic
     form of $\tfrac1gB^TB$ on the diagonal, so
     $$A:=C-\mathrm{diag}(\rho)-\mathrm{diag}(\theta)\preceq F .$$
  4. *Decision.* $A$ is an exact integer matrix; $x^TAx>0$ for all $x\ne0$ is certified by
     `positive`: a float Cholesky of $A/2^{17}$ only *proposes* $L$, the factor is rounded to
     integers at a power-of-two scale $G$, and the exact int64 residual
     $R=A\,G^2/2^{17}-L_hL_h^T$ must have all $R_{ii}>0$ and $2R_{ii}>\sum_j|R_{ij}|$. Then
     $A\,G^2/2^{17}=L_hL_h^T+R\succ0$ *exactly* (a symmetric matrix that is strictly
     diagonally dominant with positive diagonal is positive definite), hence $A\succ0$. Every
     int64 product is guarded ($|L_h|<2^{31}$, row norms $<2^{60}$, $|A|G^2/2^{17}<2^{61}$,
     $|R|<2^{61}/n$); a guard that does not hold *skips* the candidate, so exactness is never
     assumed and nothing is clamped. The two integer row guards are evaluated
     *before* the `int64` sums that they protect (`tail_penalty` bounds
     $\max_i b_{il}\cdot\sum_l\sum_i b_{il}$ rather than one product; `head_radius` bounds
     $\max\mathcal R\cdot\sum_jh_j$ before `radius @ h`), and the proposal factor must be
     finite and $A$ exactly symmetric before it is cast to `int64` — a `NaN` or `inf` factor
     fails closed instead of wrapping to an arbitrary integer (`independent.py:180-221,
     293-346`). Several scales and shifts are tried and $L$ is improved
     by the exact residual, so a failure of one proposal is not a verdict: a failure of them
     all refuses the box and `cover` bisects the window.
  The cover of $[q_{\rm hi},q_{\rm ph})$ uses its own mask-jump windows and its own bisection.

  *Regression probes (`--adversarial`).* The three boxes of REVIEW2 R2-1/R2-2 where the
  rejected hot verifier returned CERTIFIED POSITIVE are replayed: at each $q_{\rm bad}$ the
  folded form is evaluated *exactly* on an integer witness (`folded_exact`, one integer
  correlation $c_d=\sum_ix_ix_{i+d}$ times the exact rational weights, cross-checked against
  the float contraction of the same integers), the value must be negative, and then both the
  documented box (bounded cover, 64 boxes) and the point-wide box at $q_{\rm bad}$ must be
  refused.

  *Enclosure self-check (`--selfcheck`).* The step-1 invariant is verified directly, without
  any device in the loop: for six windows $[4R^2/(2r+1)^2,\,(1+\tfrac1{2r})4R^2/(2r+1)^2)$
  ($r=1,3,4,8,9,125$; $\lambda=1,10,15,3$; $\mu_*=1/2,1,3,25$) the head entries
  $2^{17}F_{ij}(q)$ are recomputed in **exact rational arithmetic** (`exact_head`) at three
  interior points $q$ and compared with the integers returned by `hot_enclosure`: every
  off-diagonal entry must satisfy $\text{lower}\le2^{17}F_{ij}(q)\le\text{upper}$,
  $|2^{17}F_{ij}(q)-C_{ij}|\le\mathcal R_{ij}$ and every diagonal entry
  $C_{ii}\le2^{17}F_{ii}(q)$, with the mask constant. 573\,003 exact rational comparisons, no
  float anywhere in the test (`independent.py:636-717`). This is the regression for the
  swapped-endpoint defect REVIEW3 R3-1: on those bytes $\mathcal R\le0$ on every entry and
  all 189\,950 off-diagonal comparisons fail, with
  $|2^{17}F_{ij}(q_{\rm mid})-C_{ij}|-\mathcal R_{ij}$ up to $45\,239$ integer units.
* $\pi$ is enclosed from $\pi/4=\arctan\frac12+\arctan\frac13$ instead of
  $\arctan\frac15+\arctan\frac1{239}$, so the two $C_E$ brackets are arithmetically
  independent as well.
* Every field of `bounds.json` is recomputed and compared: `einstein_q` (exact equality with
  the fixture, and $0<q_{\rm lo}<q_{\rm hi}$), `einstein_C` (the stored bracket must contain
  the recomputed one), `boxes` (a positive integer; its exact value is `replay.py`'s own
  receipt pin), and `mix` (spectrum and $q$, with $\sum p_i=1$ and $\sum p_iu_i=1$ checked
  exactly). `independent.py` never writes `bounds.json`, and pins $a_1$ of the three
  mixtures against hand-computed rationals so a swapped $(p,u)$ unpacking cannot survive.

**Mutations.** `replay.py --mutant {coulomb,spectrum,endpoint,tail,sign}` and
`independent.py --mutant {endpoint,coulomb,spectrum,receipt}`, each with an unmutated
control that must pass first (a broken control exits 2 and invalidates the mutant):

| mutant | perturbed statement it must refuse |
|---|---|
| `replay.py coulomb` | the cold Einstein witness survives a doubled repulsion at $q_{\rm lo}$ |
| `replay.py spectrum` | the mirrored spectrum ($u_1\leftrightarrow u_2$) is accepted; the weight swap $p\to1-p$ is accepted (wrong second moment); the mixture's verdict transfers to Einstein at $q_{\rm mix}$ |
| `replay.py endpoint` | a cold witness is certified at the stable endpoint $q_{\rm hi}$ |
| `replay.py tail` | the exact far-tail term is dominated by `far_lump` with the bound disabled |
| `replay.py sign` | the hot certificate still covers $[q_{\rm hi},q_{\rm ph})$ with the rank-one mask term reversed (attractive) |
| `independent.py endpoint` | the hot cover reaches down to $q_{\rm lo}$, where the form is indefinite |
| `independent.py coulomb` | the mixture witness keeps its cold sign with $\mu^*\to2\mu^*$ |
| `independent.py spectrum` | the weight swap $p\to1-p$ (wrong second moment) is accepted |
| `independent.py receipt` | a shaved $C_E$ bracket still passes the receipt check |

Each exits 1 with the message naming the refused statement; the base runs exit 0.

## 6. What is certified, exactly

For each instance below: (a) at $q_{\rm lo}$ the Einstein form is negative (a rational
witness), (b) on $[q_{\rm hi},q_{\rm ph})$ the Einstein form is positive, (c) for the
cases with a mixture, at the integer-quoted witness $q$ the two-line form is negative
(a rational witness) and $q>q_{\rm hi}$.

| instance | $\lambda$ | $\mu^*$ | $R^2$ | $[q_{\rm lo},q_{\rm hi}]$ | witness $q$ (mixture) |
|---|---|---|---|---|---|
| `einstein-counterexample` | 3 | 2 | 9/4 | $[83/10000,\,19/2000]$ | $1/100$ |
| `counterexample-wide` | 2 | 3/2 | 4 | $[9/10000,\,3/1000]$ | $1/200$ |
| `counterexample-strong` | 4 | 4 | 4 | $[129/500000,\,3/1000]$ | $1/100$ |
| `anchor-l1-mu1/2-R1` | 1 | 1/2 | 1 | $[0.0112,\,0.012]$ | none |
| `anchor-l1-mu1/10-R1` | 1 | 1/10 | 1 | $[0.308,\,0.3105]$ | none |
| `anchor-l3-mu1-R3/2` | 3 | 1 | 9/4 | $[0.456,\,0.4575]$ | none |
| `anchor-l10-mu1-R3` | 10 | 1 | 9 | $[4.56,\,4.565]$ | none |

($R^2=9$ means $\omega_c=3\Omega_E$, as in `fixtures.json`.) The mixed spectra (exact
rationals in `bounds.json`) are, with $p_i$ the **probability weights** and $u_i$ the
squared line frequencies in units of $\Omega_E^2$:
$p=(590/599,\ 9/599)$ at $u=(1/10,\ 60)$; $p=(4975/4998,\ 23/4998)$ at
$u=(2/25,\ 200)$; $p=(2475/2498,\ 23/2498)$ at $u=(2/25,\ 100)$. Each has
$\sum_i p_i=1$ and $\sum_i p_iu_i=1$ exactly, so the line couplings $\lambda p_i$ give
$\sum_i\lambda p_i=\lambda$ and $\sum_i\lambda p_iu_i=\lambda=M/\Omega_E^2$: same
$\lambda$, same $M$, same $\Omega_E$, and the same $R$ as the Einstein line.
`structure.py` checks $\sum p_i=1$, $\sum p_iu_i=1$ and $a_r$ against exact rationals.

## 7. The mechanism, in the same language

At $\mu^*=0$, C-LAMBDA's theorem says the Einstein line maximizes the onset. The proof
uses a maximization over probability measures with a fixed first moment of a
frequency-dependent functional; the Jensen inequality of §3(ii) is its transfer-level
core. At $\mu^*>0$ the functional to be maximized is the same one **minus** a
rank-one repulsion on the leading block. The repulsion is independent of the spectrum,
so the functional is unchanged in $p$ but the *competitor set* is now evaluated with the
lowest block penalized. A spectrum that puts most of its moment at $u_1\ll q$ keeps
$a_r\approx\lambda_1$ across the whole near zone while paying only a small mass penalty
$2\sum_{j\le i}a_j$ at small $i$; the remaining weight $p$ at $u_2\gg q$ restores
$a_0=\lambda$ and the second moment at almost no cost in the near zone. With the
repulsion in place, the near zone is no longer where the instability has to happen, so
the trade becomes favourable. This is what the three certified spectra do; it is also
why at fixed $R$ a larger $\mu^*$ makes the trade easier: the repulsion only bites on
the modes it can mask, and the mask $k(q)=\#\{i:d_i^2q<4R^2\}$ grows as $q$ falls, so a
larger $\mu^*$ buys more near-zone suppression for the same mass penalty.

The examples all satisfy $\mu^*/\lambda>1/2$ ($2/3$, $3/4$, $1$). At
$\mu^*\le\lambda/2$ the Coulomb block is small enough that the near-zone instability is
the binding one in every configuration tested in this record, but no proof is offered
here and the question is recorded as open.

## 8. Scope and honest qualifications

1. The statements are about the truncated pairing-only model with a strict common
   cutoff, not about a material, not about an exact many-body $T_c$, and not about the
   full Coulomb interaction.
2. $T_{\rm lin}$ is the supremum of temperatures at which the linearized form has a
   negative direction; no root of a nonlinear gap equation is computed.
3. Truncation enters only through explicit bounds. `replay.py` uses a 400-fold cold
   witness (extended by zero, so the cold side is exact, not truncated) and a hot head
   whose tail is eliminated by the rigorous Schur bound `far_lump`; `independent.py`
   evaluates the cold side exactly on the same 800-mode line and, on the hot side, splits
   the folded matrix once at $m=\max(160,2k+1)$ (`NB`, widened to $2k+1$ when the
   mask is wider than the head), encloses the head block by a signed
   interval centre plus a radius dominated on the diagonal, and eliminates the whole
   infinite tail by its exact Schur complement against a uniform Gershgorin gap (§5). Band
   doubling in `crosscheck.py`, and the head doubling already reported in the parent
   record, moves the thresholds by float round-off only.
4. **Physical reach of $\mu^*/\lambda>1/2$.** The three counterexamples sit at
   $\mu^*/\lambda\in\{2/3,3/4,1\}$, i.e. $\mu^*\in\{3/2,2,4\}$. That is far outside the
   conventional range of phonon-mediated superconductors, where
   $\mu^*\approx0.1\text{--}0.15$ and $\lambda\gg\mu^*$. The Morel-Anderson
   renormalization $\mu^*=\mu/(1+\mu\ln(E_F/\omega_c))$ contains no $\lambda$ and imposes
   **no** $\mu^*\le\lambda/2$ bound; it merely maps a large bare $\mu$ or a small
   $\omega_c/E_F$ to a modest $\mu^*$, and physically one expects
   $\mu^*\lesssim1/\ln(E_F/\omega_c)\approx0.1\text{--}0.2$ independent of $\lambda$.
   So $\mu^*/\lambda>1/2$ is a statement about the *kernel*, reachable in this truncated
   pairing-only model for any $\omega_c>0$ (retardation keeps $T_{\rm lin}>0$), and not a
   claim that such a parameter set occurs in a real material. Whether any material falls
   into this regime is not addressed here.
5. `crosscheck.py` implements the direct full-line fermionic Matsubara equation with the
   same kernel, no shared code and a float64 (NUMERICAL) count. It reproduces the
   ordering and the absolute scale: its even-sector $\lambda_{\max}$ agrees with the
   folded form to $4.4\times10^{-16}$ on all seven instances, and its direct onsets are
   $q=0.008392$, $0.000905$, $0.000258$ on the Einstein column (each inside the
   certified bracket) against $q=0.0123457$, $0.007690$, $0.0256$ for the mixtures,
   i.e. $T_{\rm mix}/T_{\rm E}=1.21$, $2.92$, $9.96$. An earlier draft reported
   factors $2.6$-$7$ of disagreement and attributed them to an omitted "odd-channel
   mirror term" $a_{n+m+1}$; that was false. The mirror term is the even-frequency image
   of the negative Matsubara axis, a correct discretization contains it automatically,
   and the discrepancy came from `crosscheck.v1.py`, which carried four discretization
   bugs (bosonic instead of fermionic frequencies, a doubled $\lambda$, a wrong $Z_n$ and
   an unsymmetrized kernel; see `RESULT.md` Finding 3), not from a $(u,p)$ unpacking swap.
   Below the certified regime the
   *same* two-line mixture is stable at the Einstein bracket's lower end for
   $\mu^*/\lambda=1/10$ and $1/2$ ($\lambda_{\max}=0.182$ and $0.413$ against $1.0032$
   and $1.0058$), consistent with Einstein optimality there, which stays open. Band
   doubling $|n|\le240\to480$ shifts $\lambda_{\max}$ by at most $6.4\times10^{-5}$ and
   flips no sign. Reported as NUMERICAL evidence for the ordering only; the certified
   chain does not depend on this script.
6. No literature claim is made. Rens arXiv:2611.20496 Thms. 3, 4, 6 and Kondratev
   Prop. 1/§12 are zero-Coulomb results (see the the bracket-and-mustar records review); nothing there
   settles the positive-$\mu^*$ common-cutoff question, which these counterexamples
   answer negatively.
