# Literature notes: verified models, results, and limits

**3 November 2026.** This replaces the previous notes. **L** denotes a published result; **A** a project assumption; **R** our own analysis/result. Do not turn one into another. Numerical benchmarks and their source locations are indexed in `sim/literature_targets.csv`. Our simulation numbers belong in `VALIDATION_REPORT.md` and its linked CSV files.

## 0. What was and was not read

The earlier passes used snippets and page summaries. This session used literal, line-numbered full-text HTML/PDF extraction. “Full text” below means the article's main text and captions were read, not that every raster plot was visually inspected. Screenshot calls supplied no image payload. Plot coordinates have **not** been guessed. The detailed retrieval record is in [sources/READING_LOG.md](sources/READING_LOG.md).

| Paper | Read status in this session | Remaining limits |
|---|---|---|
| Kozma & Barrat 2008 | Full arXiv text; published PDF checked for model/threshold notation | Journal Greek fonts garbled; equations recovered from HTML; plot-only values unavailable |
| Deffuant et al. 2000 | Full prose; **partial mathematical recovery** | Readable pair rule/captions recovered from author-uploaded OCR; density equation and exact typography of peak formula remain [UNVERIFIED] |
| Vazquez et al. 2008 | Full arXiv text, including previously missing ending | Plots read through captions, not digitized |
| Holme & Newman 2006 | Full arXiv text | Exact coordinates in Fig.4 not recovered |
| Sasahara et al. 2021 | Full arXiv text, Methods and appendix; relevant author code | Code read, not executed; questionable triad formula not adopted |
| Hegselmann & Krause 2002 | Full PDF narrative, simulations, appendix statements | Several appendix expressions garbled; central averaging rule cross-checked against Lorenz |
| Baumann et al. 2020 | Full arXiv text and supplementary §§I–VIII | Journal metadata verified separately; one supplement caption/prose discrepancy |
| Flache et al. 2017 | Full main HTML review and Frontiers | Cited underlying experiments not independently all read |
| Nardini et al. 2008 | Full arXiv text | Published typeset version not compared |
| Gross & Blasius 2008 | Full arXiv main review | Not an independent read of every model reviewed; some graphical box material not recoverable |
| Diakonova et al. 2015 | Full arXiv text and appendices A–C | Extraction has notation/figure-reference errors; no noisy-model replication claimed |
| Bail et al. 2018 | Full published main article, pp.9216–9221 | Attached 56-page supporting information **not fully read** |
| Kan, Feng & Porter 2023 | Full arXiv article; journal excerpts checked | Algorithm pseudocode has an inequality inconsistent with its definition; no reproduction attempted |
| Lorenz 2007 | Full survey text | Density-equation transcription has apparent errors; not used as executable equations |
| Newman 2006 | Full arXiv main article and benchmark table | We implement partition evaluation, not the spectral optimizer |
| Balsamo et al. 2019 | Full arXiv main text | Supplement not independently read; journal publication not verified |
| Pansanella, Rossetti & Milli 2022 | Full main HTML article | Supplement and image-only algorithms not fully inspected |
| Baldassarri & Gelman 2008 | Published author PDF, main article | Table/footnote disagree about centering year; no fit reproduced |
| DiMaggio, Evans & Bryson 1996 | **Abstract only**; full scan located | Institutional PDF returns zero text; readable/OCR PDF needed |
| Zhao, Sasahara & Chen 2026 | Full main/supplement HTML text | Preprint; stopping-time and homophily-formula inconsistencies noted below |
| Guerra et al. 2013 | Full 10-page main PDF text and tables | Plot coordinates not digitized; boundary-index qualifications below |
| Interian et al. 2023 | **Partial main text**, through §3.6, extraction lines 0–612 | Remaining review not read; printed modularity expression questioned below |
| Delre et al. 2007; Delre et al. 2010; Kempe et al. 2003; Bass 1969 | Product-specific sources, with individual read limits | See product_launch/LITERATURE_NOTES.md; do not silently upgrade Delre 2010 or Bass to full reading |

Access attempts: HAL returned an access-denied challenge; PMC returned reCAPTCHA. These were not bypassed. Public arXiv/author copies were used where available. Deffuant's first fetch timed out, then the indexed PDF worked. A readable original Deffuant PDF and an OCR/text-enabled DiMaggio PDF would resolve the main extraction gaps.

## 1. Paper by paper

### 1.1 Kozma & Barrat (2008): our closest baseline

*Consensus formation on adaptive networks*, **Physical Review E 77, 016102**, [published PDF](https://www.cpt.univ-mrs.fr/~barrat/PhysRevE_77_016102.pdf), [clear-equation arXiv text](https://arxiv.org/html/0707.4416), DOI [10.1103/PhysRevE.77.016102](https://doi.org/10.1103/PhysRevE.77.016102).

**L — exact mechanism, §II.** Uniform initial opinions on [0,1], random ER graph. Choose a uniform node and one uniform neighbor. With probability `w`, attempt discordant-edge rewiring to a uniform existing non-neighbor, chosen **before** deletion; otherwise attempt simultaneous pair compromise. Both old opinions enter Eq.1. `0 ≤ μ ≤ 1/2`; simulations use `μ=1/2`. Isolates are allowed and have no activation partner.

**L — measures.** An opinion cluster is a connected component after retaining only edges whose endpoint opinions are within tolerance. It is a **communication-path** definition. A topological cluster is a component of the unfiltered graph. Their “fragmentation” at tiny tolerance concerns absence of extensive **opinion** clusters, not simply any network disconnection.

| Target ID | Published location | Quantitative target/setup |
|---|---|---|
| KB1 | Figs.1–2 | N=1000, mean degree=5, d=.15; static versus w=.7 |
| KB2 | Figs.3–4, §III | mean degree=10; N=500,1000,2000,5000; 100 network realizations; d₁≈.256; largest/second-largest fractions near 1/0 versus 1/2,1/2 |
| KB3 | §III, Fig.6 | d₂≈1/(2k̄); k̄=10,20,30; inset uses 2(k̄−1)d |
| KB4 | Fig.7 | w=.5; N=500,2000,5000,20000; inset N=5000, w=0,.1,.5,.9; d₁(w) increases |
| KB5 | Figs.8–11 | d=.1 debris analysis; cutoff N/50 in Fig.10; debris count scales N^β(w), β(0)=1; numerical nonzero-w exponents [UNVERIFIED]; small-d mean-field comparison 1/(2d) |
| KB6 | Figs.12–13 | Fig.12: d=.1,N=1000 and d=.005,N=10000, k̄=10; Fig.13: N=2000,w=.5,d=.05 |

**L — recovered equations, §V–VI:**

- (4) `t_f ∝ 1/(w d)`.
- (5) `t_l ∝ k̄(1−2d)/(w d)`.
- Opinion timescale: `t_o ∝ τ_o/(1−w)`; at fast rewiring an inverse `(1−w)` scale is expected, with slow bridge-mediated mergers complicating it.
- (6) For disagreement `Δ>d`, compromise probability `p=exp(1−Δ/d)`.
- (7) For `Δ>d`, rewiring probability `p_rw=1−exp(1−Δ/d)`.

Example of equations 6–7: `Δ=2d` gives `p=e⁻¹` and `p_rw=1−e⁻¹`. These equations describe their **soft-confidence variant**, not our implemented hard cutoff.

**Authors' qualifications:** scaling arguments are heuristic; some results are not shown; the hard cutoff is deliberately softened in a variant. **Our assessment:** the `2d` matching probability ignores boundaries; for independent uniforms the population-wide probability is `2d−d²`. Do not present d₂ as an exact finite-N law. The arXiv percolation sentence labels the threshold d₁; the published PDF correctly labels it **d₂**.

**A/R — relationship to us:** random reconnection and pair averaging are replications. The legacy no-new-isolates rule changes the process; the recommended primary model allows isolates. Project `φ=w/(1−w)` matches the ratio of update rates only for `w≤.5` when `φ≤1`; clocks also differ: `t_project=(1−w)t_KB`. We implement their scheduler separately for w=.9. Our gap clusters cannot validate KB3.

### 1.2 Deffuant, Neau, Amblard & Weisbuch (2000)

*Mixing beliefs among interacting agents*, **Advances in Complex Systems 3(1–4), 87–98**, DOI [10.1142/S0219525900000078](https://doi.org/10.1142/S0219525900000078); [PDF](https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/dbba/2023/deffuantmixingbeliefsamonginteractingagents.pdf), [author-uploaded OCR](https://www.researchgate.net/publication/235737446_Mixing_beliefs_among_interacting_agents).

**L — scalar model, §2:** choose two uniformly random agents. If `|x−y|<d`, replace them simultaneously by `x+μ(y−x)` and `y+μ(x−y)`; otherwise neither changes. Initial opinions are uniform [0,1]. The simulated convergence parameter is between 0 and .5. Example: (.2,.3), μ=.3 becomes (.23,.27).

| ID | Location | Recovered setup/result |
|---|---|---|
| DW1 | Fig.1 | d=.5, μ=.5, N=2000 **in caption**; surrounding prose says N=1000 |
| DW2 | Fig.2 | d=.2, μ=.5, N=1000; multiple surviving peaks |
| DW3 | Figs.3–4 | Fig.3 d=.1, μ=.5; Fig.4 N=1000, μ=.5, 250 samples, “wings” excluded |
| DW4 | Figs.5–7, §3 | 29×29 square lattice, four neighbors; d=.3/.15, μ=.3, 100000 pair iterations; Fig.7 main histogram peak at .76 |

**Other model in the paper:** binary opinion vectors, Hamming-distance bounded interaction, random copying on differing coordinates; §4/Figs.8–9. These are **not** the scalar model and are not our validation targets. Its damaged numerical expressions are not silently reconstructed.

**Limits:** constant symmetric confidence is an explicit simplification; other network claims are conjectures. Peak means/widths fluctuate in finite samples. **Correction:** this paper does not establish a precise universal complete-mixing critical d. The rough `1/(2d)` **major-peak heuristic** is verified in Lorenz's survey; the exact printed original formula remains [UNVERIFIED]. The original claim that μ and N “only” affect time/width must not be generalized to adaptive networks or all bounded-confidence variants. Our model inherits the scalar compromise rule, not the vector model or a universal threshold.

### 1.3 Vazquez, Eguíluz & San Miguel (2008)

*Generic absorbing transition in coevolution dynamics*, **PRL 100, 108702**, DOI [10.1103/PhysRevLett.100.108702](https://doi.org/10.1103/PhysRevLett.100.108702), [full text](https://arxiv.org/html/0710.4910).

**L — model:** initially random simple degree-regular network; independent ±1 states with equal probabilities. Uniform node/neighbor activation. A discordant pair triggers rewiring to a uniform same-state non-neighbor with probability p, or copying of the neighbor by the focal node with probability 1−p. One time unit is N attempts. Edge count is fixed.

| ID | Location | Target |
|---|---|---|
| V1 | Eq.2 | `dρ/dt=(2ρ/k̄)[(1−p)(k̄−1)(1−2ρ)−1]` |
| V2 | Eqs.3–4, Fig.2 | Mean-field `ρ_s=[(1−p)(k̄−1)−1]/[2(1−p)(k̄−1)]`; `p_c=(k̄−2)/(k̄−1)` |
| V3 | Fig.3 | k̄=4; N=250,1000,4000; 10000 realizations; simulated p_c≈.38; largest fraction ≈1 below, ≈1/2 above |
| V4 | Fig.4, Eq.6 | N=10000,k̄=4; p=0,.35,.4; `ρ_p(m)=ξ_p(1−m²)` |
| V5 | Convergence-times paragraph, Fig.3c | Below: `τ∼N/(p_c−p)`; above: `τ∼ln[k̄(p−p_c)N]/(p−p_c)` |

**Authors' limitation:** correlations invalidate the mean-field threshold: 2/3 predicted versus ≈.38 simulated at degree 4. **Our assessment:** finite active systems eventually absorb; do not call their finite-size subcritical state permanently active. The complete article reports **no numerical other-degree sweep and no rewire-to-random variant**. A degree trend in the mean-field formula is not a validated degree trend for our continuous model. Its binary benchmark is implemented separately; no `.38` target is imposed on our project φ.

### 1.4 Holme & Newman (2006)

*Nonequilibrium phase transition in the coevolution of networks and opinions*, **PRE 74, 056108**, DOI [10.1103/PhysRevE.74.056108](https://doi.org/10.1103/PhysRevE.74.056108), [full text](https://arxiv.org/html/physics/0603023).

**L — model:** N nodes, M initially random edges, G uniformly assigned categorical opinions; γ=N/G. Select a node; skip isolates. With probability φ move a random incident edge to a uniform same-opinion node; otherwise copy a uniform neighbor. Rewiring is **not restricted to disagreement**. Self-edges/multiedges are allowed. Their “consensus” means no disagreeing connected neighbors and can contain many distinct opinions.

| ID | Location | Target |
|---|---|---|
| HN1 | Figs.2–3 | k̄=4,γ=10; N=3200 for Fig.2; φ_c=.458±.008; community-size exponent 3.5±.3 |
| HN2 | Eq.1, Fig.3 | `S=N^(−a) F[N^b(φ−φ_c)]`; a=.61±.05; b=.7±.1; 10000 realizations |
| HN3 | Fig.4 | Other k̄,γ: N=200,400,800,1600; 10000 realizations; threshold varies; exponents compatible with same values |
| HN4 | Fig.5, §IV | Time in updates/node: φ=0, τ∼N; φ=1, τ∼ln N; critical z=.61±.15 |

**Authors' scope:** large G proportional to N, loops/multiedges permitted for simplicity. **Our assessment:** Fig.4 is a dependency plot, not a closed-form threshold formula. Exact curve coordinates and monotonicities are [UNVERIFIED] without the plot. Initial-condition sensitivity was not systematically tested. Neither φ=.458 nor their meaning of consensus transfers to us. In particular, **our φ=1 still permits compromise**; it is not their pure-rewiring limit.

### 1.5 Sasahara et al. (2021)

*Social influence and unfollowing accelerate the emergence of echo chambers*, **Journal of Computational Social Science 4, 381–402**, DOI [10.1007/s42001-020-00084-7](https://doi.org/10.1007/s42001-020-00084-7), [article text](https://arxiv.org/html/1905.03919), [author code](https://github.com/soramame0518/echo_chamber_model/blob/master/agent.py).

**L — model:** random directed follower graph; opinions [−1,1]; one random user views its latest l messages. With `C={messages m:|o−m|<ε}`, update `o'=o+μ mean_C(m−o)`. Repost with probability p; discordant-message-driven unfollow/reconnect with probability q. Reconnect randomly, via repost originators, or via concordant-message recommendations. Out-degree is conserved; influence is one-sided, so mean opinion need not be conserved.

| ID | Location | Target |
|---|---|---|
| S1 | Figs.3–4 | N=100,E=400,l=10,ε=.4,μ=p=q=.5; Fig.4:20 runs |
| S2 | Figs.5–6 | μ/q=0 or .1 comparisons; 200 attempted runs/configuration; cap100000; joint rates above .1 accelerate segregation; some impossible-segregation runs excluded |
| S3 | Effects of Rewiring Strategies, Fig.7 | Comparable opinion-cluster end states; recommendation convergence >2× faster; triad comparison20 runs |

**Resolved ambiguity:** `agent.py` leaves opinion unchanged when C is empty and posts the user's own message. “Both required” concerns producing joint opinion change/segregation; “unfollowing sufficient” concerns **which reconnection strategy** is necessary. Unfollowing alone does not move fixed opinions into new peaks.

**Authors' limits:** excluded undersized clusters, idealized sharing, mitigation requires further study. **Our assessment:** empirical segregation is used as a stopping target (Methods C–D), not an independent prediction. Directed follower/retweet graphs and opinion inference differ. The caption-normalization of triads in the HTML is questionable; not adopted. Our `h` analogy is qualitative; normalize their ε by two before comparing opinion scales.

### 1.6 Hegselmann & Krause (2002)

*Opinion dynamics and bounded confidence: models, analysis and simulation*, **JASSS 5(3), 2**, [article/PDF](https://jasss.soc.surrey.ac.uk/5/3/2.html).

**L — BC rule, §2 Eq.2.3/BC:** `I_i(x)={j:|x_j−x_i|≤ε_i}`, including i; `x_i(t+1)=sum_{j∈I_i}x_j(t)/|I_i|`. Everyone updates from the same old profile. Also examined: classical linear averaging, Friedkin–Johnsen anchoring, time-dependent weights, asymmetric confidence. These are not our pairwise algorithm.

| ID | Location | Target |
|---|---|---|
| HK1 | Fig.2 | N=625; one common random start: ε=.01→38 opinions; .15→2 camps; .25→consensus, within15 periods |
| HK2 | Fig.3, §4.1 | 50 runs each; ε=.01,.02,…,.40; transition around .25 for this experiment |
| HK3 | Figs.7–8 | Regular 100-opinion profile: ε=.05→8 splits; ε=.25→consensus |
| HK4 | Fig.12 | N=625;25 runs/point; ε_left/right in0,.02,…,.4 |
| HK5 | Figs.17–18 | Total confidence .2,.4,.6; bias m=0,.04,…,1; at total .6, consensus breaks around m=.4; Fig.18 regular50-agent examples |

**L — definitions/qualification:** cluster means equal final opinions; “fragmentation” is multiple opinions, not graph components. §4.3 p.29 says random serial updating gives extremes somewhat more survival; qualitative conclusions survive. Appendix establishes finite-time stabilization for homogeneous synchronous BC. **Our assessment:** .25 is a finite-population example/region, not a universal mathematical critical constant; Lorenz finds different density-model thresholds. The exact Fig.2 count cannot be seed-replicated without their initial vector. Our separate HK benchmark checks the published pattern, not our adaptive model directly.

### 1.7 Baumann et al. (2020)

*Modeling echo chambers and polarization dynamics in social networks*, **PRL 124, 048301**, DOI [10.1103/PhysRevLett.124.048301](https://doi.org/10.1103/PhysRevLett.124.048301). [Full article + supplement](https://arxiv.org/html/1906.12325); [journal metadata](https://arxiv.org/abs/1906.12325).

**L — model, Eqs.1–2:** `dx_i/dt=−x_i+K sum_j A_ij(t)tanh(α x_j)`; contacts weighted by `|x_i−x_j|^(−β)` after normalization. Directed activity-driven contacts, reciprocity r, unbounded convictions. This is reinforcement, not bounded-confidence pair averaging.

| ID | Location | Target |
|---|---|---|
| B1 | Fig.1, supplement I | N=1000; initial opinions uniformly **spaced** [−1,1]; m=10, activity cutoff=.01, exponent2.1; RK4 dt=.01; K=3,r=.5; (α,β)=(.05,2),(3,0),(3,3) |
| B2 | Eq.3 / supplement IV Eq.10 | `α_c≈1/[(1+r)Km〈a〉]`; finite-N factor N/(N−1), derived neglecting homophily |
| B3 | Supplement III/Fig.S2 | N=250,1000 runs,dt=.05,K=1; polarized lifetime grows at least exponentially with β |
| B4 | Fig.4 | 200 simulations; K=2.5,α=4.5,β=2,r=.65;45 aggregated snapshots |

**L — outcomes:** neutral consensus, one-sided radicalization, metastable two-sided polarization; echo chambers via own-opinion versus neighbor-mean density. **Authors' limits:** minimal assumptions, omitted advertising/credibility, empirical work needed. **Our assessment:** lifetime text/caption disagree about reduced r (.65/.5); do not reconstruct this curve yet. Our model cannot validate these reinforcement thresholds. Their empirical illustration does not establish universal historical growth of polarization.

### 1.8 Flache et al. (2017)

*Models of social influence: towards the next frontiers*, **JASSS 20(4), 2**, DOI [10.18564/jasss.3521](https://doi.org/10.18564/jasss.3521), [full text](https://www.jasss.org/20/4/2.html).

**L — review, not one calibrated model.** Table1 separates assimilation, similarity-biased influence, and repulsion. Illustrative Eq.3 is a one-sided update `o_i'=o_i+f_w(o_i,o_j)(o_j−o_i)`; Eq.4 uses f=μ inside confidence and zero outside; Eq.5 uses `f=μ(1−2|o_i−o_j|)` with boundary truncation. Illustrations use N=100; Fig.1b ε=.15. These are examples, not universal benchmark thresholds.

**L — definitions/limits:** distinguish clustering, group extremization and bipolarization. Bounded-confidence averaging cannot leave the initial opinion range. Frontier1 asks for explicit mechanisms and implementation comparisons; Frontier2 separates calibration of assumptions from empirical validation of predictions.

**Correction affecting our files:** the statement about higher initial variance increasing bipolarization occurs under **Critical conditions and limitations of repulsive influence**. It cannot be cited as a proved prediction for our purely attractive model. Communication-regime robustness is qualified; the review itself warns that small technical changes can matter.

**Our assessment:** this supports a careful synthetic mechanism study and sensitivity checks; it supplies no empirically measured values for d,φ,h,μ. It also does not mean that bounded confidence can never move a particular moderate toward an existing extreme. The rigorous restriction is on the **population's initial range**.

### 1.9 Nardini, Kozma & Barrat (2008)

*Who's talking first? Consensus or lack thereof in coevolving opinion formation models*, **PRL 100, 158701**, DOI [10.1103/PhysRevLett.100.158701](https://doi.org/10.1103/PhysRevLett.100.158701), [full text](https://arxiv.org/html/0711.1261v1).

**L — models:** binary direct voter model: uniform node i copies neighbor j; reverse model: j copies i. Rewiring attempts occur with probability Φ, only on disagreeing pairs, to a random target; copying otherwise. N attempts/unit time. Naming-game variants additionally permit a both-names intermediate state and mutual agreement after successful communication.

| ID | Location | Target |
|---|---|---|
| N1 | Fig.1 and text | 100 realizations; static voter t_c∝N; adaptive direct voter t_c∝ln N, reverse voter t_c exponential in N |
| N2 | Note3 | Near direct-voter transition, t_c∼N^a,a≈.43 |
| N3 | Fig.2 | N=1000,k̄=10 ensemble; single runs N=500,k̄=10,Φ=.4 |
| N4 | Figs.3–4 | Naming-game direct/reverse t_c∝ln N; Fig.4 N=10000,k̄=10,Φ=.2 |

**L — diagnostics:** magnetization, cross-state link density and state-specific mean degrees; majority-degree feedback drives the direct/reverse difference. No transferable critical Φ is supplied for us.

**Authors' scope:** slight asymmetry changes can have drastic consequences; mean-field explains mechanisms. **Our assessment:** an important counterexample to our previous blanket claim that update schemes affect only details. It does not contradict limited HK serial/synchronous robustness; those are different mechanisms. Our symmetric compromise preserves the pair sum, unlike copying.

### 1.10 Gross & Blasius (2008)

*Adaptive coevolutionary networks: a review*, **Journal of the Royal Society Interface 5, 259–271**, DOI [10.1098/rsif.2007.1229](https://doi.org/10.1098/rsif.2007.1229), [full main text](https://arxiv.org/html/0709.1858).

**L — scope:** node states affect topology and topology affects states. The review covers Boolean networks, oscillators, evolutionary games, opinions and epidemics. It has **no single N, initialization, update rule or opinion-cluster definition** to copy. Four recurrent themes: self-organization, differentiation of node roles, complex topology and complex dynamics.

**Quantities illustrated, not our targets:** Fig.2 connectivity tends to2; §III quotes `K=2+12.4N^(−.47)` for a Boolean-network study; Fig.3 quotes an oscillator-network exponent −.48. These require their original models for reproduction. §VI discusses the Holme–Newman transition, with its probability symbol used in the **opposite convention** from the original paper.

**Authors' qualifications:** naive mean-field approximations can fail when distinct node classes emerge; a general inventory/theory is incomplete. **Our assessment:** use the feedback definition and methodological framing. Do not borrow unrelated biological exponents or infer that adaptivity always polarizes, always produces power laws, or guarantees a particular threshold.

### 1.11 Diakonova, Eguíluz & San Miguel (2015)

*Noise in coevolving networks*, **PRE 92, 032803**, DOI [10.1103/PhysRevE.92.032803](https://doi.org/10.1103/PhysRevE.92.032803), [full text + appendices](https://arxiv.org/html/1411.5181).

**L — exact stochastic rule, §II:** degree-regular random graph, mean degree4, independent equiprobable binary states. Node-centric copy/rewire-to-same as Vazquez; no eligible target means skip rewiring. Then, independently, a designated noisy focal node is reset uniformly with probability ε (flip probability ε/2). Fraction q is noisy. N attempts/time unit.

| ID | Location | Quantitative reference |
|---|---|---|
| D1 | Figs.2,4–5 | N=250; Fig.2 ensemble1000; full noise gives active-link density1/2; examples(p,ε)=(.5,.1),(.2,10⁻⁴),(.8,10⁻⁴) |
| D2 | Appendix A Eq.10, Fig.10 | Approximation `ε_c=[1+N/(2(1−p))]^(−1)`; not valid around the fragmentation transition |
| D3 | §IV | `q_max≈1−sqrt(k̄/N)`; noisy nodes isolate in topologically absorbing states; at least qN components |
| D4 | Fig.8 / Appendix B | N=250,1000 realizations,Tmax=2000 snapshots; at(p=.8,q=.45), giant≈N/2, second≈8 nodes |

**L — measures:** state absorption differs from **topological** absorption; largest/second component and active-link density distinguish regimes. Homogeneous noise removes the absorbing transition; targeted noise can preserve it with isolated noisy nodes.

**Authors' limits:** enormous absorption times, cutoff-dependent finite-size boundaries; approximations permit otherwise unavailable links and miss saturation. **Our assessment:** “add noise” is not an innocuous robustness test. Its location, interpretation and sampling design must be specified. The legacy no-isolate rule excludes their shattered-fragmentation mechanism. No noisy version is added to the project.

### 1.12 Bail et al. (2018)

*Exposure to opposing views on social media can increase political polarization*, **PNAS 115(37), 9216–9221**, DOI [10.1073/pnas.1804840115](https://doi.org/10.1073/pnas.1804840115), [published main article and SI bundle](https://dlab.epfl.ch/teaching/spring2019/cs718/papers/bail2018exposure.pdf).

**L — empirical design, not a simulation model:** recruited frequent Twitter users identifying with either party; 1652 pretreatment responses (901 Democrats,751 Republicans). Block-randomized offer of payment to follow an opposing-view bot for one month;24 posts/day. Outcome:10-item policy scale, seven response points; analyze posttreatment attitudes conditional on baseline and covariates.

| ID | Location | Main-article result |
|---|---|---|
| BA1 | Fig.3 | Analytic samples Democrats697,Republicans542 |
| BA2 | Fig.3 | ITT: Democrats−.02,p=.45; Republicans+.12,p=.008 |
| BA3 | Fig.3 | Fully compliant CACE: Democrats−.14,p=.46; Republicans+.60,p<.01 |

**Authors' limitations:** cannot generalize to all Americans, independents, infrequent users or other countries; incentivized exposure and elite messages; exact causal mechanism unresolved; alternative explanations remain.

**Our assessment:** a warning against assuming universal attractive response, not proof of our rewiring rule or evidence that all cross-party exposure backfires. This is attitudinal change on an empirical scale, not a network-component validation target. Do not claim its supporting robustness analyses were independently read; only the main article was fully checked.

## 2. Check of our simulator against the literature

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md). The previous N=500, eight-replication, sorted-gap comparison was a preliminary behavioral check. It did **not** validate communication-path clusters or precisely locate d₁/d₂.

This handoff supplies a separate KB update scheduler, an isolate switch, path-based clusters, N=1000/100-replication threshold checks, degree/size checks near d₂, a synchronous HK benchmark and a separate binary voter benchmark. The supplied 2790-run dataset was reproduced exactly by an acceleration engine before longer runs or metric changes were interpreted. Published numbers remain distinct from our measurements.

## 3. Corrections to earlier claims

| Earlier wording | Verified replacement |
|---|---|
| Our result discovers that opinion groups disconnect | Replication of KB §IV; Pansanella2022 also explicitly separates opinion convergence and later graph separation |
| h introduces similarity-based reconnection to bounded confidence | Prior homophilic adaptive BC exists, notably Kan2023; h is our controlled mixture parameterization |
| Separating polarization and network structure is novel | KB, Sasahara and Balsamo already distinguish them |
| A positive rewiring phase boundary rises with degree in our experiments | Original plot is a fixed-horizon result. Longer runs invalidate that long-run interpretation at d=.2; see report |
| Every time cap means critical slowing down | Some cases are blocked or retain unmatched agents under isolate protection |
| No-isolate protection is needed for constant edge count | Replacing one edge with one conserves edge count with or without isolates |
| No agent can ever be isolated | Initialization can create isolates; the rule only forbids **new** isolates caused by cutting |
| φ=1 freezes opinions | False in our scheduler: compatible agents still compromise |
| h has no end-state effect | H3 not supported in tested cells; absence of evidence is not statistical equivalence |
| Flache's higher-variance result predicts our attractive model | That passage concerns repulsive influence; our start-distribution result is empirical within our synthetic model |
| μ,N and updating are always secondary | Limited basic-model observations, not a general result; see Lorenz and Nardini |
| HK's universal consensus threshold is .25 | Finite-N benchmark/example; density formulations give other thresholds |
| Variance rising measures our polarization | Impossible under our symmetric averaging rule; use cluster/graph measures separately |
| Sasahara leaves an empty concordant screen undefined | Author code skips influence and posts own opinion |
| Sasahara proves both mechanisms separately sufficient for opinion change | No influence means opinions do not change; strategy-sufficiency and joint dynamics are distinct claims |
| Baumann journal citation from memory | PRL124,048301(2020), DOI verified in arXiv metadata |
| AnyLogic/Python have already been cross-verified | Still false until students compile/run AnyLogic and export comparison results |

## 4. What is established, assumed, and contributed here

**L:** bounded-confidence clustering, adaptive separation, homophilic reconnection and differing temporal scales all predate this project. A 5% “major cluster” convention appears explicitly in Kan2023. Modularity is standard. Even the distinction between persistent opinions and changing exposure is prior work.

**A:** our graph ensemble, homogeneous parameters, hard tolerance, fixed edge count, no-new-isolates switch, horizon and operational cutoffs. None is empirically calibrated.

**R:** our defensible contribution is a **replication and extension in simulation methodology**: reproduce reference behavior, compare h under fixed scenarios, expose horizon-sensitive conclusions, diagnose the isolate restriction and measure threshold sensitivity. To our knowledge, this particular combination of controls and reproducible analysis has not been located in the sources reviewed; this is **not** an exhaustive novelty search or a claim of a new social mechanism.

A useful elementary deduction for the viva is that one compatible compromise changes the population variance by

`ΔVar = −2μ(1−μ)(x_i−x_j)²/N ≤ 0`.

Rewiring does not change opinions. Mean opinion is conserved. Thus multimodality and disconnection can develop while overall variance decreases. This is our algebraic diagnostic, not a claim of a new theorem. The derivation and numerical check belong in the blueprint and verification script.

## 5. What to say aloud

“Our starting mechanism is published work, especially Kozma and Barrat's adaptive bounded-confidence model. We replicated it and investigated contact selection and measurement choices. Our initial short runs suggested a rewiring threshold that changed with network density. Longer runs showed that much of that threshold was a delay in fragmentation. We also checked what our stopping rule really means. The result is a study of when a simulation conclusion is reliable, rather than a claim that we discovered why real societies polarize.”

## 6. Additional literature and novelty checks

### Kan, Feng & Porter (2023)

*An adaptive bounded-confidence model of opinion dynamics on networks*, **Journal of Complex Networks 11(1), cnac055**, DOI [10.1093/comnet/cnac055](https://doi.org/10.1093/comnet/cnac055), [full preprint](https://arxiv.org/html/2112.05856).

**L:** separate confidence C and discordance β; choose up to M discordant edges uniformly, choose an endpoint, reconnect with normalized weight `1−|x_i−x_a|`. Avoid loops/multiedges; the just-dropped neighbor is eligible. Then choose K edges without replacement for opinion updates. If an agent occurs repeatedly, only its final old-profile update is applied; mean opinion is not conserved. N=1000,p=.01,M=1,K=5,α=.1;50 runs. Stop below total opinion-change tolerance10⁻⁵ for100 consecutive steps or a bailout. Major clusters have≥5% of agents.

**Targets:** Figs.3–5 baseline C≈.26 versus up to≈.34 with rewiring; Fig.2 subcluster difference≈.0003; Fig.6 opinion assortativity; Fig.7 convergence/capping. N=5000 exploration changes M,K **and mean degree** to50, so it is not a pure size comparison. Authors call for finite-size, update-rule and heterogeneity analysis. Our h mixture differs, but the underlying reconnection idea is prior art. ArXiv Algorithm1 line8 has `<β` where the definition of discordance requires `>β`; do not copy it uncritically.

### Lorenz (2007)

*Continuous opinion dynamics under bounded confidence: a survey*, **International Journal of Modern Physics C 18, 1819–1838**, [full text](https://arxiv.org/html/0707.1762v2).

**L:** agent-based DW and HK, their density formulations, multidimensional opinions, heterogeneity, communication regimes and μ. Fig.1 uses1001 opinion bins and a10⁻⁹ mass threshold. It describes the approximate integer-part `1/(2ε)` major-cluster rule, minor clusters and finite-population departures. Fig.2's density HK consensus region starts around .19, compared with .22 in another density treatment; longest reported numerical convergence21431. It explicitly discusses discretization and overly rough stopping criteria. §4 notes lower μ changes minor-cluster sizes and that who meets whom can encourage or prevent consensus.

**Our assessment:** use the survey to define communication regimes and qualify thresholds. Its density equations are not a substitute for a separately verified solver, and the survey itself records unproved generalizations. It directly rebuts our earlier blanket claims of update/μ/N insensitivity.

### Measures: Newman (2006) and Balsamo et al. (2019)

Newman, *Modularity and community structure in networks*, **PNAS103,8577–8582**, DOI [10.1073/pnas.0601602103](https://doi.org/10.1073/pnas.0601602103), [full text](https://arxiv.org/html/physics/0602124). **L:** modularity compares observed within-group edges to a degree-based random-graph null. Our equivalent form is `Q=sum_c[m_c/m−(D_c/(2m))²]`, with `m_c` internal edges and `D_c` degree sum. His optimizer's Table1 results, such as karate Q=.419, are **not** targets for evaluating an arbitrary opinion partition. Our code does not detect communities by optimizing Q.

Balsamo et al., *Inside the Echo Chamber: Disentangling network dynamics from polarization*, [full arXiv1906.09076v2](https://arxiv.org/html/1906.09076). **L:** empirical directed mentions, not a generative simulation;43 weekly windows,285670 users,2066042 mentions. Opinion coherence is `C(t)=sum_ij w_ij exp(−|x_i−x_j|)/W(t)` for their selected β=1. Fixed polarized distributions can coexist with weakening interaction segregation. They use randomized-opinion nulls and mutual information. **Our assessment:** association/mutual information do not by themselves identify causal influence; signs inferred from hashtags are noisy. Their work is direct prior art for separating network and opinion dynamics. We cite the preprint, without inventing a journal citation.

### Pansanella, Rossetti & Milli (2022)

*Modeling algorithmic bias: simplicial complexes and evolving network topologies*, **Applied Network Science7,57**, DOI [10.1007/s41109-022-00495-7](https://doi.org/10.1007/s41109-022-00495-7), [full article](https://link.springer.com/article/10.1007/s41109-022-00495-7).

**L:** a neighbor is sampled with weight proportional to opinion-distance^(−γ), then bounded-confidence pair averaging is applied. Following discordance, rewiring with probability p_r tests **one** random non-neighbor and succeeds only if compatible. This differs from our uniform draw over **all** compatible candidates. They also examine triadic majority influence. N=250,30 runs,μ=.5; ε=.2,.3,.4;γ=0,.4,.8,1.2,1.6;p_r=0,.1,…,.5;cap10⁵ iterations. ER p=.1 and BA m=5 have different mean degrees. Cluster participation ratio is `1/sum_c f_c²`.

**L:** Figs.5–6 explicitly distinguish stabilized opinions from later network separation; extending rewiring can eventually split the graph. **Our assessment:** related timescale findings are already published. Our extension is the particular finite-cap audit and controls, not the idea that network separation can lag opinion clustering. Their equilibrium and 1000-quiet-iteration checks are not proof of exact absorption. Authors request comparisons of candidate-selection rules and empirical justification.

### The two sociological leads

**Baldassarri & Gelman (2008)**, *Partisans without constraint: political polarization and trends in American public opinion*, **AJS114,408–446**, [published author PDF](https://sites.stat.columbia.edu/gelman/surveys.course/BaldassarriGelman2008.pdf). **L:** NES1972–2004,47 issues; multilevel varying-intercept/slope models of issue/party correlations and issue-pair correlations. Table1: average correlation growth .05/decade with party identity and .04 with ideology (SE .01). Table3: issue-pair growth .02/decade, interpreted as substantively weak. Issue sorting differs from cross-issue alignment. No agent-network rewiring rule is estimated. **Our assessment:** historical correlational evidence cannot demonstrate our micro-mechanism or today's trend. One-dimensional opinions cannot represent their cross-issue concept. A correlation of .17 must not be translated into17% variance explained; it would imply r²≈.029 in a simple bivariate linear interpretation. The table and footnote also disagree on centering year; slopes are the safer quoted quantities.

**DiMaggio, Evans & Bryson (1996)**, *Have Americans' Social Attitudes Become More Polarized?*, **AJS102,690–755**, DOI [10.1086/230995](https://doi.org/10.1086/230995), [publisher abstract](https://www.journals.uchicago.edu/doi/10.1086/230995), [unreadable institutional scan](https://cpi.stanford.edu/_media/pdf/Reference%20Media/DiMaggio_1996_Public_Opinion.pdf). **Abstract-level only:** differentiates dispersion, distribution shape, ideological constraint and group differences; reports limited broad evidence in its historical period, with exceptions. Detailed methods, tables and quantitative values are **[UNVERIFIED]** pending a readable PDF. Do not cite it as evidence that all real attitudes have become more polarized.

### Zhao, Sasahara & Chen (2026): temporal paths already have direct precedent

[arXiv2601.16457v2](https://arxiv.org/html/2601.16457v2), **preprint**, full main/supplement HTML text read. Directed message/continuous-opinion model: N=500, mean outgoing degree15, tolerance .45, influence/posting rates .005–.1, recommendation controls and histories, 1024 settings with36 trials each. Homophily and local/global polarization are separate; a path integral describes their temporal ordering. This directly rules out claiming that studying temporal paths is generally our invention.

The reported stopping rule uses60 quiet steps with changes below10⁻⁷ and a20000-step cap, while a supplement activity example discusses10⁵: this needs clarification. The printed initial-homophily approximation also appears inconsistent with its uniform-interval algebra. We do not copy these as verified benchmarks. Retrospective pathway classification can use future trajectory information, which complicates a real-time intervention interpretation. Multipolar opinions also challenge a single polarization index.

### Guerra et al. (2013): community structure is not automatically antagonism

[Full primary PDF](https://ojs.aaai.org/index.php/ICWSM/article/download/14421/14270/17939), ten-page main text read. Boundary nodes have both a cross-group neighbor and a qualifying internal neighbor. Their score averages `d_i/(d_i+d_b) − 1/2` over this boundary. It distinguishes boundary structure beyond modularity; empty boundaries need explicit handling rather than an automatic antagonism score.

Table2 supplies useful counterexamples: university Q=.24/P=−.24 versus karate Q=.35/P=.17, and soccer Q=.39/P=.20 versus political blogs Q=.42/P=.18. These are source examples, not our simulated values. Authors acknowledge that separation alone need not imply antagonism; a node-level cutoff sentence appears inconsistent with the centered index. We use the conceptual caution, not an uncritically transcribed replacement KPI.

### Interian et al. (2023): partial OR measures review

[Author-hosted review](https://ic.unicamp.br/~ruben/publications/2023%20-%20Network%20polarization%20filter%20bubbles%20and%20echo%20chambers%20An%20annotated%20review.pdf), DOI [10.1111/itor.13224](https://doi.org/10.1111/itor.13224). Read literal text through §3.6, including earlier extraction gaps, **not the whole37-page review**. It distinguishes several network measures and reviews78 selected papers; reading the review is not reading those78 sources. Its E–I index is `(external−internal)/total`, equivalent to `2×cross-edge fraction−1` for that edge partition. A printed modularity normalization differs from Newman's standard expression, so our implementation follows the verified primary Newman definition. Remaining sections are an explicit open reading task.

### Product-launch application

The selected final domain is now implemented, with actual AnyLogic default evidence and new sales experiments. Marketing-paper readings, source links and a second claim-verification table are in [product_launch/LITERATURE_NOTES.md](product_launch/LITERATURE_NOTES.md). The original opinion results are mechanism evidence rather than sales observations. Product experiences break the original global mean/variance invariant; the pairwise compromise identity itself remains valid.

## 7. Claim verification in the supplied files

The table appended below audits **the original supplied versions**, so its line references remain stable under `../handoff/`. Bibliographic entries are included. A row can contain several connected claims; any necessary qualification makes the row **corrected**. `sim/claim_inventory.csv` retains the complete original text, source locator and reason. This is a claim inventory, not a declaration that every cited article was fully recovered. Prompts/instructions with no factual assertion are identified as such.

<!-- GENERATED CLAIM TABLE -->

| ID | Original location and claim (abbreviated) | Status | Verification / correction |
|---|---|---|---|
| C001 | `01_MANIFEST.md:9` —  /  LITERATURE_NOTES.md  /  What each paper says, read status, corrections to earlier claims, validation against Kozma & Barrat… | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C002 | `01_MANIFEST.md:14` —  /  sim/validate_kb.py  /  Check against Kozma & Barrat setup (N = 500, 8 reps)  /  Run; broadly consistent, not exact  /  | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C003 | `01_MANIFEST.md:22` — - No rewiring: polarized but connected. With rewiring: opinion clusters become separate components (replicates Kozma & Barrat). | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C004 | `01_MANIFEST.md:23` — - Network threshold in φ rises with mean degree; slowing near it. Qualitative agreement with Vazquez et al. | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C005 | `01_MANIFEST.md:24` — - Similar vs random reconnection (h) changes speed, not the end state. H3 not supported. Agrees with Sasahara et al. | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C006 | `01_MANIFEST.md:29` — Deffuant parameters and thresholds; Kozma & Barrat garbled equations; four abstract-only papers; Baumann journal version; AnyLo… | **corrected** | Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report. |
| C007 | `FIVE_HOUR_PLAN.md:31` —  /  F1  /  Opinion polarization and network fragmentation are different things, and rewiring converts one into the other. Witho… | **corrected** | Replication credit confirmed, but snapshots and initial small components qualify fully connected/any-rewiring language. |
| C008 | `FIVE_HOUR_PLAN.md:33` —  /  F3  /  There is a transition in φ, and it moves with mean degree. At d = 0.2 the network fragments at φ ≈ 0.005 to 0.01 for… | **corrected** | Long-cap check invalidates the claimed positive long-run threshold and its degree shift at d=.2. |
| C009 | `FIVE_HOUR_PLAN.md:34` —  /  F4  /  Choosing *similar* contacts (h = 1) vs random contacts (h = 0) does not change how fragmented the network ends up. I… | **corrected** | H3 is not supported, not an equivalence result; isolate-controlled runs show speed advantage is not universal. |
| C010 | `FIVE_HOUR_PLAN.md:39` — Headline story for the presentation: *We re-implemented the adaptive bounded-confidence model of Kozma and Barrat, checked it a… | **corrected** | Rewrite headline around observation-time sensitivity and qualified h comparison, with direct prior credit. |
| C011 | `FIVE_HOUR_PLAN.md:45` — - We did not compare quantitatively with Vazquez's mean-field critical value (it is for binary opinions); only qualitative agre… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C012 | `FIVE_HOUR_PLAN.md:100` — 2. Literature (1 page): bounded confidence (Deffuant; Hegselmann-Krause); coevolving networks (Holme-Newman; Vazquez et al.; Ko… | **corrected** | Bibliographic gaps partly resolved; central extraction and SI gaps remain explicitly marked. |
| C013 | `FIVE_HOUR_PLAN.md:104` — 6. Verification and validation (1 page): edge conservation (2,790 runs), φ = 0 reproduces bounded-confidence behaviour, KPI uni… | **corrected** | AnyLogic comparison remains a task, not a completed validation result. |
| C014 | `FIVE_HOUR_PLAN.md:129` — 2. Where do the rules come from? Update rule from Deffuant bounded confidence; rewiring idea from Holme-Newman and Kozma-Barrat… | **corrected** | Credit Kan and other homophilic BC precedents; isolate protection is separate from edge conservation. |
| C015 | `FIVE_HOUR_PLAN.md:138` — 11. What would you do with more time? Longer caps near the threshold; test thresholds; add opinion noise (Diakonova et al. show… | **corrected** | Long-cap/KPI checks now done; noise type must be specified; exact binary critical-point scaling still incomplete. |
| C016 | `polarization_project_blueprint.md:62` —  /  Deffuant et al. (2000); Hegselmann & Krause (2002)  /  Bounded confidence: agents influence each other only if opinions are… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C017 | `polarization_project_blueprint.md:63` —  /  Holme & Newman (2006)  /  Discrete opinions; with probability φ an edge is rewired to a random agent of the *same* opinion,… | **corrected** | Discrete-opinion model; clarify the direction and their local-consensus definition; no initial-state sensitivity test. |
| C018 | `polarization_project_blueprint.md:64` —  /  Vazquez, Eguíluz, San Miguel (2008)  /  Binary-state coevolving voter model: below a critical rewiring rate the network sta… | **corrected** | Finite systems absorb below the transition too; other-degree dependence is mean-field, not a simulated sweep or our threshold. |
| C019 | `polarization_project_blueprint.md:65` —  /  Kozma & Barrat (2008)  /  Nearly our model with h = 0: adaptive Deffuant on an Erdős–Rényi graph, rewiring to a random non-… | **corrected** | Closest replication, with different clocks/isolate protection; previous gap-based check was preliminary. |
| C020 | `polarization_project_blueprint.md:66` —  /  Nardini, Kozma, Barrat (2008)  /  Depending on the dynamics, rewiring can speed consensus, break the network apart, or sust… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C021 | `polarization_project_blueprint.md:67` —  /  Sasahara et al. (2021)  /  Influence alone or unfollowing alone is very slow; both above 0.1 together give echo chambers mu… | **corrected** | Separate joint influence/segregation from reconnection-strategy sufficiency; speed is model/regime-specific. |
| C022 | `polarization_project_blueprint.md:68` —  /  Baumann et al. (2020, arXiv)  /  Adding radicalization dynamics, the transition from consensus to radicalized states is gov… | **corrected** | Journal metadata now verified: PRL124,048301(2020). |
| C023 | `polarization_project_blueprint.md:69` —  /  Flache et al. (2017)  /  Many theoretical influence models, few empirical tests  /  Justifies our "literature-informed, not… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C024 | `polarization_project_blueprint.md:70` —  /  Bail et al. (2018)  /  Field experiment where exposure to opposing views increased polarization for some participants  /  C… | **corrected** | Republican effect significant; Democratic effect not significant; restricted sample and intervention. |
| C025 | `polarization_project_blueprint.md:71` —  /  Gross & Blasius (2008)  /  Review of adaptive networks and their shared dynamical themes  /  Framing and terminology  /  | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C026 | `polarization_project_blueprint.md:81` — Novelty, stated modestly. Kozma & Barrat and Holme & Newman already study adaptive bounded-confidence or voter-type models. Our… | **corrected** | Homophilic bounded confidence and separating opinions from topology already have direct precedents. |
| C027 | `polarization_project_blueprint.md:90` — - opinion x_i ∈ [0,1], initial x_i ~ Uniform(0,1) (the standard Deffuant-style initialization) | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C028 | `polarization_project_blueprint.md:102` —  /  μ  /  susceptibility  /  0.3  /  0.1, 0.3, 0.5  /  Deffuant allows 0 to 0.5 (0.5 means full averaging); value is an assumpt… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C029 | `polarization_project_blueprint.md:148` —  /  Behavioural validation  /  Qualitative comparison to published model outcomes only (Deffuant, Kozma & Barrat, Sasahara, Vaz… | **corrected** | Separate literature-model replication from empirical validation; new quantitative benchmarks are available. |
| C030 | `polarization_project_blueprint.md:151` — Empirical data could only be used to *test* qualitative patterns (for example, the Twitter data in Sasahara et al.), and that i… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C031 | `polarization_project_blueprint.md:210` —  /   /  Modularity Q of the opinion-cluster partition  /  Newman modularity of the network under that partition  /  | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C032 | `polarization_project_blueprint.md:233` —  /  φ = 0  /  Verification and V1  /  Network unchanged; opinion clusters shrink in number as d rises (qualitative match to Def… | **corrected** | Network unchanged at phi=0; trend is qualitative, with finite-size/minor-cluster qualifications. |
| C033 | `polarization_project_blueprint.md:236` —  /  Qualitative match to Kozma & Barrat and Sasahara  /  V2 (behavioural)  /  Adaptation produces cluster formation and splitti… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C034 | `polarization_project_blueprint.md:237` —  /  *Optional:* binary-opinion voter mode vs Vazquez et al.  /  V3  /  Fragmentation near the *simulated* critical rewiring rat… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C035 | `polarization_project_blueprint.md:247` —  /  Finite size and initial conditions  /  Flache et al. report that outcomes depend on the initial opinion distribution and va… | **corrected** | Flache variance passage is about repulsive-influence models, not a prediction for our attractive model. |
| C036 | `polarization_project_blueprint.md:249` —  /  No true "radicalization"  /  Assimilative bounded confidence cannot push opinions to the extremes; Baumann et al. need a re… | **corrected** | Averaging cannot expand the initial range; it can move individual moderates toward an existing extreme. |
| C037 | `polarization_project_blueprint.md:250` —  /  No repulsive influence  /  Bail et al. suggest exposure can backfire; we model only attraction  /  Listed as a limitation; … | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C038 | `polarization_project_blueprint.md:256` — Optional extensions (pick at most one at the Week 6 gate): (a) opinion noise (note Diakonova et al. find that noise changes the… | **corrected** | Homogeneous and targeted noise have distinct effects; no noisy extension was implemented. |
| C039 | `polarization_project_blueprint.md:283` — 1. Holme, P. & Newman, M.E.J. (2006). Nonequilibrium phase transition in the coevolution of networks and opinions. *Phys. Rev. … | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C040 | `polarization_project_blueprint.md:284` — 2. Vazquez, F., Eguíluz, V.M. & San Miguel, M. (2008). Generic absorbing transition in coevolution dynamics. *Phys. Rev. Lett.*… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C041 | `polarization_project_blueprint.md:285` — 3. Kozma, B. & Barrat, A. (2008). Consensus formation on adaptive networks. *Phys. Rev. E* 77, 016102. arXiv: [0707.4416](https… | **corrected** | DOI10.1103/PhysRevE.77.016102 now directly verified. |
| C042 | `polarization_project_blueprint.md:286` — 4. Nardini, C., Kozma, B. & Barrat, A. (2008). Who's talking first? Consensus or lack thereof in coevolving opinion formation m… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C043 | `polarization_project_blueprint.md:287` — 5. Deffuant, G., Neau, D., Amblard, F. & Weisbuch, G. (2000). Mixing beliefs among interacting agents. *Advances in Complex Sys… | **corrected** | Completed bibliographic record: ACS3(1-4),87-98(2000),DOI10.1142/S0219525900000078. |
| C044 | `polarization_project_blueprint.md:288` — 6. Hegselmann, R. & Krause, U. (2002). Opinion dynamics and bounded confidence: models, analysis and simulation. *JASSS* 5(3), … | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C045 | `polarization_project_blueprint.md:289` — 7. Sasahara, K., Chen, W., Peng, H., Ciampaglia, G.L., Flammini, A. & Menczer, F. (2021). Social influence and unfollowing acce… | **corrected** | Completed pages381-402; distinguish 2020 online/preprint from 2021 journal volume. |
| C046 | `polarization_project_blueprint.md:290` — 8. Baumann, F., Lorenz-Spreen, P., Sokolov, I.M. & Starnini, M. Modeling echo chambers and polarization dynamics in social netw… | **corrected** | Verified journal record rather than memory: PRL124,048301(2020). |
| C047 | `polarization_project_blueprint.md:291` — 9. Flache, A., Mäs, M., Feliciani, T., Chattoe-Brown, E., Deffuant, G., Huet, S. & Lorenz, J. (2017). Models of social influenc… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C048 | `polarization_project_blueprint.md:292` — 10. Gross, T. & Blasius, B. (2008). Adaptive coevolutionary networks: a review. *J. R. Soc. Interface* 5, 259–271. DOI: [10.109… | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C049 | `polarization_project_blueprint.md:293` — 11. Diakonova, M., Eguíluz, V.M. & San Miguel, M. (2015). Noise in coevolving networks. *Phys. Rev. E* 92, 032803. *Checked.* | **confirmed** | Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model. |
| C050 | `polarization_project_blueprint.md:294` — 12. Bail, C.A. et al. (2018). Exposure to opposing views on social media can increase political polarization. *PNAS.* DOI: [10.… | **corrected** | Completed journal record: PNAS115(37),9216-9221. |
| C051 | `polarization_project_blueprint.md:307` — - [ ] Plot opinion trajectories; compare qualitatively with the Deffuant description | **unverifiable** | Instruction or future check, not a completed literature-validation result. |
| C052 | `polarization_project_blueprint.md:324` — "We went through the main families of models. The Deffuant and Hegselmann-Krause models give us the idea that people only get i… | **corrected** | Do not generalize binary/categorical transitions to our model; empirical segregation was a stopping target in Sasahara. |
| C053 | `polarization_project_blueprint.md:326` — Two cautions came out of it. Flache and co-authors point out that this field has far more theory than empirical testing, so we … | **corrected** | Retain empirical caveat; specify the significant partisan group and limit generalization. |
| C054 | `polarization_project_blueprint.md:331` — "We aren't collecting real data. Our question is about mechanism, and real data wouldn't tell us values like tolerance or rewir… | **corrected** | No small-world/scale-free project runs were done; synthetic mixed opinions do not ensure a connected initial graph. |
| C055 | `polarization_project_blueprint.md:352` — - Where's the update rule from? "Deffuant for the bounded-confidence update. The rewiring part is our own adaptation, informed … | **corrected** | Rewiring is substantially inherited from KB; h is a parameterization, not the invention of this mechanism. |
| C056 | `sim/validate_kb.py:1` — """Validation against Kozma & Barrat (2008): ER graph, mean degree 10, mu=0.5, uniform opinions. | **corrected** | The supplied script is a preliminary N500/eight-rep gap-cluster check; replaced as quantitative evidence by run_validation.py. |
| C057 | `sim/validate_kb.py:3` — KB's w (prob. of attempting rewiring) maps to our phi = w/(1-w)  (our phi=1 <-> w=0.5).""" | **corrected** | phi=w/(1-w) is admissible only for w<=.5 when phi is a probability; compare clocks too. |
