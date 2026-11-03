# Opinion-network foundation and the selected product-launch extension

**IE305 Simulation Lab — Mihir Vasave and Vaibhav Mathur — revised 3 November 2026**

Suggested presentation subtitle: **Can more contacts prevent echo chambers—or only delay them?**

**Selected final application:** a synthetic reusable-bottle launch. Use [product_launch/PROJECT_REPORT.md](product_launch/PROJECT_REPORT.md), its model specification, sales CSVs and actual tested `.alp`. The original opinion/contact model below is the mechanism foundation; its sales-free results are not product observations.

## 0. Current, honest status

| Item | Status |
|---|---|
| Original assignment and supplied handoff | Read; originals preserved in `../handoff/` |
| Literature | Actual text reviewed; explicit extraction/reading gaps in `LITERATURE_NOTES.md` |
| Python reference grid | Supplied 2790 output rows reproduced, including saved KPIs; not 2790 independently observed trajectories |
| Additional validation | Published-model benchmarks, longer caps, isolate-rule and KPI sensitivity checks executed; see `VALIDATION_REPORT.md` |
| Recommended main model | Allow isolates. Matched primary grid in `sim/results_primary.csv`; legacy protected-isolate output retained separately |
| AnyLogic | Original opinion-only port unexecuted; selected product default has actual successful run/animation/export evidence |
| Product engine comparison | Actual default matches matching Java except cohort/runtime; large reference grid remains separately labeled |
| Interpretation | Original positive rewiring-threshold interpretation revised after longer runs |

Provenance: AI assisted source review, code and analysis. Students must understand the mechanism and personally verify the AnyLogic model they present. This document does not assert that unfinished implementation work has happened.

## 1. Research question and hypotheses

**Question:** How do tolerance, disagreement-driven rewiring and selection of new contacts affect opinion groups and network connectivity? Which conclusions survive a longer observation horizon?

An opinion distribution can have several peaks while paths still connect their members. A graph can also split while its components hold similar opinions. We measure these separately. “Polarization” here means separated major opinion groups; it does not imply hostility or movement beyond the initial opinion range.

| ID | Original hypothesis | Current interpretation |
|---|---|---|
| H1 | Larger tolerance generally produces fewer major opinion clusters without rewiring | Supported as a qualitative baseline pattern; finite populations and small minorities matter |
| H2 | Rewiring can increase network fragmentation at fixed tolerance | Supported in a substantial part of the tested grid; replication of published adaptive-network behavior |
| H3 | Similar reconnection fragments the network more than random reconnection at equal φ | **Not supported.** Paired intervals include zero in the examined comparisons. This is not proof of equivalence |
| H4 | A positive rewiring threshold separates long-run connected/fragmented phases, and shifts with degree | **Not established; the original long-run interpretation fails at d=.2.** The apparent threshold changes substantially with the time cap |
| H5 | High tolerance weakens the effect of rewiring | Supported within the tested grid, especially d=.4; finite replications do not prove a zero failure probability |

The horizon, application and stopping-rule audits are exploratory follow-up analyses prompted by censoring, not hypotheses registered before the original runs.

## 2. Literature foundation and contribution

The direct baseline is Kozma & Barrat's adaptive Deffuant model. The scalar compromise rule originates in Deffuant et al.; HK is a different simultaneous-averaging benchmark. Similarity-based reconnection in continuous bounded-confidence networks is already studied by Kan, Feng & Porter. Sasahara studies a directed message-sharing model. Pansanella et al. explicitly discuss delayed graph separation after opinions stabilize. Balsamo et al. separate opinion polarization and interaction dynamics empirically. Exact rules, citations and source locations are in `LITERATURE_NOTES.md` §§1 and6.

**Established:** these mechanisms and distinctions are prior work. **Our assumptions:** the particular graph ensemble, homogeneous parameters, reconnection mixture, optional isolate restriction and numerical measurements. **Our results:** scenario comparisons, longer-horizon correction, stopping diagnostics and sensitivity estimates.

Our contribution is a **replication and extension** through controlled simulation experiments and output analysis. To our knowledge, we have not located this exact combination of controls in the reviewed sources. We do not claim a new social mechanism, a new polarization metric, or a new theory of society.

## 3. Minimum viable mathematical model

### 3.1 State and initialization

There are N agents. Agent i holds one scalar opinion `x_i∈[0,1]`. All agents use the same tolerance d and compromise fraction μ. The implemented MVP has no heterogeneous tolerances or activities.

The undirected simple graph starts as **G(N,M)** with exactly `M=floor(N k0/2)` edges. Uniformly sample pairs, rejecting self-pairs and existing edges, until M distinct edges exist. It is not a complete graph, a built-in network generator with an unspecified degree distribution, or a guaranteed connected graph. Initial isolates can occur.

Initialize opinions after the graph:

- `init=0`: independent Uniform(0,1).
- `init=1`: median of three independent uniforms, **exactly Beta(2,2)**.
- `init=2`: equal-probability mixture centered at .25 and .75, Gaussian SD .08, **clipped** to[0,1]. Clipping differs from rejection-based truncation.

### 3.2 Parameters and implemented ranges

| Parameter | Baseline | Actually examined in the original project grid | Status |
|---|---|---|---|
| N |300|100,300,600|Synthetic size choice|
| k0 |8|4,8,16|Synthetic density choice|
| d |.2|.1,.15,.2,.25,.3,.4|Scenario factor, not empirically estimated|
| μ |.3|.1,.3,.5|Scenario factor; nonzero and≤.5|
| φ |.25|0 to1 on the grids in §6|Probability after disagreement|
| h |1|0,.5,1|Probability of selecting from compatible non-neighbors|
| allow_isolates |**true**|false legacy; true primary/literature checks|Allow isolates in the recommended model; preserve false as an explicit sensitivity variant|
| numerical ε |10⁻³|10⁻⁵ in KB benchmark|Computational tolerance, not social tolerance d|
| check interval |10 sweeps|10|Stopping inspection interval|
| cap |**30000 sweeps**|3000 legacy and matching short-horizon D check|Observation horizon|

### 3.3 One activation, exactly as implemented

```
Choose i uniformly from all N agents.
If degree(i)=0, end this activation.
Choose j uniformly among i's neighbors.
Let Δ=|x_i−x_j|.
If Δ<d:
    store old xi and xj
    x_i := xi + μ(xj−xi)
    x_j := xj + μ(xi−xj)
Otherwise:
    with probability φ, try to rewire:
        if allow_isolates=false and degree(j)=1, do nothing
        otherwise choose k BEFORE deleting the old edge:
            with probability h, sample uniformly from compatible non-neighbors
            if this set is empty, fall back to all non-neighbors
            with probability 1−h, sample uniformly from all non-neighbors
            exclude i and every existing neighbor, including j
        if no candidate exists, do nothing
        else remove(i,j), add(i,k)
```

One **sweep** is N independent activations, with replacement. An agent can activate several times or zero times in a sweep. It is random sequential updating, without a Poisson clock. Exact equality Δ=d goes into the disagreement branch in this project.

Example: x_i=.20,x_j=.30,d=.20,μ=.30 gives(.23,.27). For(.20,.70), the opinions stay fixed during that encounter; a φ=.25 coin may replace the edge. At h=1, “similar” means within d of the current focal opinion, not necessarily the same emerging cluster.

Edge count is conserved because each successful rewire replaces one edge by one. Isolate protection is **not required** for this conservation law. It forbids a newly isolated dropped neighbor, but does not remove initial isolates. φ=1 still permits opinion changes on compatible pairs.

### 3.4 Stopping and censoring

The recommended main model allows isolates. The earlier protected-isolate version is retained as a legacy sensitivity case, not silently mixed with the primary output.

Check every10 sweeps. The supplied numerical-freezing predicate requires every compatible edge to have endpoint difference≤10⁻³ and, if φ>0, **no discordant edge**. Stop early if it passes; otherwise record the state at the cap and set `censored=1`.

This predicate is not a proof of exact mathematical absorption. With μ=.3, exact equality is generally approached gradually. Also, isolate protection can prevent removal of discordant edges or keep an agent searching for a nonexistent compatible contact. Such cases can fail the predicate indefinitely.

The analysis therefore distinguishes a measured finite-horizon state, numerical freezing, and diagnosed nonfreezing. A mean of capped stopping times is a **restricted mean**, `E[min(T,cap)]`, not an uncensored mean convergence time. Warm-up removal is not used: the transient evolution from the specified initial condition is the object of study.

### 3.5 Structural verification identities

A compatible pair update conserves `x_i+x_j`, so the population mean stays fixed. Direct expansion gives

`(xi')²+(xj')²−xi²−xj² = −2μ(1−μ)(xi−xj)²`.

Since the mean is fixed, divide by N to obtain

`Var_after−Var_before = −2μ(1−μ)(xi−xj)²/N ≤0`.

Rewiring changes no opinions. Thus population variance cannot rise in this homogeneous symmetric model, although multiple peaks and disconnected components can emerge. An individual can move away from the center; the entire population cannot leave its initial minimum/maximum range. These are elementary verification properties, not claimed research novelties.

An additional audit explains why the legacy rule can prevent freezing forever. If an agent has no other opinion within d, all other opinions lie at least d to its left or right. Same-side averaging stays outside its confidence interval; opposite sides are at least2d apart and cannot compromise. The unmatched agent therefore stays unmatched. Forbidding its last tie from being cut forces a discordant edge to survive. This is why the recommended model permits isolates and records them rather than protecting them. See `sim/stall_audit.csv`.

### 3.6 Comparison with Kozma & Barrat

Set μ=.5,h=0,allow_isolates=true and use their separate update scheduler: with probability w attempt discordant rewiring, otherwise attempt compromise. Our project scheduler has relative-rate mapping `φ=w/(1−w)`, or `w=φ/(1+φ)`. A probability φ≤1 only covers w≤.5. For example w=.5 corresponds to φ=1; w=.9 would require φ=9 and is **not** admissible in the project scheduler. Simulation clocks differ by `t_project=(1−w)t_KB`.

`sim/run_validation.py` uses the KB scheduler directly for all w. ER G(N,M) is documented; the paper does not specify enough implementation detail to promise identical graph samples, seeds or numerical stopping behavior.

## 4. Data and parameter plan

All input data are synthetic. Parameter values are swept rather than calibrated to people. Uniform opinions and random graphs enable comparisons to published models; they are not claims about real populations. Beta and clipped bimodal starts test dependence on that convention. Empirical estimation of influence would require a different study design.

The two students can defend distributions by naming their purpose and sensitivity check. They should not say a source measured μ=.3 or φ=.25 in real life. No empirical social-media dataset is required or introduced here. The user confirmed that simulation-generated data are acceptable. `data/` exposes one actual generated300-person/1200-edge population. The application study has180 realizations and900 repeated snapshots; horizons must be analyzed separately.

## 5. AnyLogic architecture

Use an agent-based model with `Person` and `Main`, one `people` population and one cyclic sweep event. The paste-ready Java body in `anylogic/Main_additional_class_code.java.txt` holds initialization, activation, metrics and export. `Person` needs only opinion and a stable index. Two actions call the body: initialize on startup, advance one sweep per event.

Use user-defined bidirectional connections and explicitly generate G(N,M). Use a private `java.util.Random` initialized from the logged replication seed so display/layout randomness does not consume the model stream. The API audit is in `AnyLogic_port.md`; it verifies documentation signatures, not compilation.

Export before `finishSimulation()`, with a once-only guard. Do not depend on `onDestroy`, because finishing preserves the model. Per-run CSVs merge using `sim/ingest_anylogic.py`; the resulting file goes directly into `sim/analyze.py`.

The exact installed AnyLogic version and available experiment types remain unknown. The current edition documentation says Custom experiments are unavailable in PLE. A Simulation experiment with manual replications is a valid fallback. Use the freeform Parameter Variation setup described in the port if available.

## 6. Experiments and output analysis

### 6.1 Original and matched primary experiments

The original grid uses30 replications per cell, cap3000 and isolate protection. The matched primary grid uses the same factors/seeds, cap30000 and allows isolates. Files identify each variant. A matching primary D run at cap3000 isolates the effect of observation horizon. The factor counts below apply to each full grid. Counts include repeated scenarios across experiments; do not pool repeated seed/scenario rows as independent observations.

| Experiment | Factors | Runs |
|---|---|---|
| A |d=.1,.15,.2,.25,.3,.4 × φ=0,.01,.02,.05,.1,.25,.5,1; h=1|1440|
| B |d=.15,.25 × h=0,.5,1 × φ=.05,.25,1|540|
| C |N=100,600; μ=.1,.5; init=1,2, one at a time around baseline|180|
| D |k0=4,8,16 × φ=0,.005,.01,.02,.05,.1,.25 at d=.2,h=1|630|

The legacy follow-up reruns all707 originally capped rows to30000 sweeps, preserving their initial seeds and model rules. A separate1170-run B/D check allows isolates, followed by a full matched primary grid. The report separates these runs and their inference. Literature validation is a separate verification suite, not extra project features.

### 6.2 Seeds and uncertainty

Original replication r uses seed1000+r. Within fixed N,k0 and initialization mode, A/B scenarios share their initial graph and opinions. Conditional random draws diverge during evolution. Across changed N or k0, graph generation consumes different numbers of draws, so **the same seed does not guarantee identical initial opinions**. No blanket claim of separate streams is made for the original Python data.

Different replications use distinct seeds. Comparisons of h within B are paired by r. Pairing only reduces variance when covariance is favorable; it is not guaranteed by reusing seed labels. Cross-language seeds do not imply identical random draws.

New analyses use10000 seeded percentile-bootstrap resamples for mean/paired-difference intervals; binary proportions use Wilson95% intervals. The old `summary.txt` is retained as legacy output. The updated analysis records its interval method explicitly. Thirty replications are a tractable choice, not a demonstrated precision guarantee. For example0/30 events still has a Wilson upper limit around.114.

### 6.3 KPIs and operational classification

| KPI | Exact definition and qualification |
|---|---|
| K |Sort opinions; split at adjacent gaps>.05; count groups with≥5% of N. Can be zero. This is not KB's path definition|
| Variance |Population variance, divisor N. A spread diagnostic; cannot measure increasing spread in this model|
| S |Largest connected component size/N|
| C, isolated fraction |Number of components; fraction of singleton components|
| Cross fraction |Number of graph edges whose endpoints have different gap-cluster labels divided by total edges; minor clusters are included in these labels|
| Q |Modularity of the fixed full gap-cluster partition, including minor clusters. We do not optimize Q|
| Time/censoring |Numerical stopping sweep or cap; retain the indicator and isolate rule|
| KB benchmark |Components of the compatible-edge subgraph; largest, second-largest, total count|

| Opinion measure |S≥.9: one large component|S<.9: fragmented by the operational cutoff|
|---|---|---|
| K=1 |One **major** opinion group|One major group, fragmented graph|
| K≥2 |Multiple major groups, still largely linked|Multiple major groups, fragmented graph|
| K=0 |No major group; report separately|No major group; report separately|

S≥.9 is not exact graph connectivity. K=1 is not proof that everyone agrees. The multiple-groups/fragmented case is an **echo-chamber proxy**, not evidence of misinformation, hostility or repeated message reinforcement. Q alone cannot prove an echo chamber. For two disconnected equal-volume groups Q=.5; its value depends on group sizes.

The robustness suite recomputes all27 combinations of gap=.02,.05,.08; minimum fraction=.01,.05,.10; S cutoff=.80,.90,.95 on the **same** final states. It does not infer new opinion groups from aggregate CSV columns alone.

### 6.4 Verification and validation

`VALIDATION_REPORT.md` supplies pass/partial/pending judgments. Conservation and hand-calculated graph fixtures verify code. Published-model comparisons check behavior. Independent AnyLogic results are still needed to establish cross-implementation agreement. Neither check establishes that the synthetic model predicts society.

## 7. Limitations and alternative explanations

- Bounded confidence already creates opinion clusters with rewiring off. Graph separation is a different additional outcome.
- The isolate restriction can create persistent searching or blocked discordant pairs. The isolate-allowed sensitivity is necessary when interpreting stopping times.
- The horizon changes apparent transition locations. The tested lower positive φ=.005 does not identify a mathematical threshold at zero.
- Reconnection requires querying non-neighbor opinions; h idealizes a search/recommendation capability.
- Opinion is one cardinal number; real issue alignment, identities, strategic behavior and attitudes toward groups are omitted.
- There is no repulsion, noise, population turnover, media or endogenous edge count. Adding these could change conclusions; none is silently implemented.
- Small groups are suppressed by the major-cluster KPI. Gap/cutoff sensitivity is reported rather than assumed harmless.
- End-state h differences were not detected, which is weaker than showing practical equivalence. A universal speed advantage also fails in an examined isolate-allowed cell.
- Synthetic scenario comparisons cannot justify platform policy or quantify real people's tolerance. Initial opinion convention and degree can matter.

For an IEOR interpretation, distinguish a finite-horizon service/design objective—maintain links for a specified time—from a claim of permanent protection. This is a simulation decision question; no real-world policy recommendation is estimated.

## 8. Eight-week plan: historical structure, superseded by the five-hour plan

| Stage | Intended milestone | Current handoff |
|---|---|---|
| Weeks1–2 |Concept, sources, minimum AnyLogic model|Concept/reference ready; AnyLogic build pending|
| Weeks3–4 |Verification, pilot, seeds and logging|Reference checks and export contract ready|
| Weeks5–6 |Controlled experiments and sensitivity|Reference grid and follow-up available|
| Weeks7–8 |Interpretation, figures, report, rehearsal|Interpretation revised; students must complete AnyLogic evidence and rehearse|

This is not a claim that eight weeks of work were actually performed. Use `FIVE_HOUR_PLAN.md` for the remaining session.

## 9. References

The full source notes, equations, figure locations and reading qualifications are in `LITERATURE_NOTES.md`. Core journal records:

1. Deffuant et al.(2000), *Mixing beliefs among interacting agents*. ACS3,87–98. [DOI](https://doi.org/10.1142/S0219525900000078).
2. Hegselmann & Krause(2002), *Opinion dynamics and bounded confidence: models, analysis and simulation*. JASSS5(3),2. [Article](https://www.jasss.org/5/3/2.html).
3. Kozma & Barrat(2008), *Consensus formation on adaptive networks*. PRE77,016102. [DOI](https://doi.org/10.1103/PhysRevE.77.016102).
4. Holme & Newman(2006), *Nonequilibrium phase transition in the coevolution of networks and opinions*. PRE74,056108. [DOI](https://doi.org/10.1103/PhysRevE.74.056108).
5. Vazquez et al.(2008), *Generic absorbing transition in coevolution dynamics*. PRL100,108702. [DOI](https://doi.org/10.1103/PhysRevLett.100.108702).
6. Sasahara et al.(2021), *Social influence and unfollowing accelerate the emergence of echo chambers*. JCSS4,381–402. [DOI](https://doi.org/10.1007/s42001-020-00084-7).
7. Kan, Feng & Porter(2023), *An adaptive bounded-confidence model of opinion dynamics on networks*. JCN11,cnac055. [DOI](https://doi.org/10.1093/comnet/cnac055).
8. Pansanella, Rossetti & Milli(2022), *Modeling algorithmic bias: simplicial complexes and evolving network topologies*. ANS7,57. [DOI](https://doi.org/10.1007/s41109-022-00495-7).
9. Flache et al.(2017), *Models of social influence: towards the next frontiers*. JASSS20(4),2. [DOI](https://doi.org/10.18564/jasss.3521).
10. Nardini et al.(2008), *Who's talking first? Consensus or lack thereof in coevolving opinion formation models*. PRL100,158701. [DOI](https://doi.org/10.1103/PhysRevLett.100.158701).
11. Gross & Blasius(2008), *Adaptive coevolutionary networks: a review*. JRSI5,259–271. [DOI](https://doi.org/10.1098/rsif.2007.1229).
12. Baumann et al.(2020), *Modeling echo chambers and polarization dynamics in social networks*. PRL124,048301. [DOI](https://doi.org/10.1103/PhysRevLett.124.048301).
13. Diakonova et al.(2015), *Noise in coevolving networks*. PRE92,032803. [DOI](https://doi.org/10.1103/PhysRevE.92.032803).
14. Bail et al.(2018), *Exposure to opposing views on social media can increase political polarization*. PNAS115,9216–9221. [DOI](https://doi.org/10.1073/pnas.1804840115).

Reviews/measurement and sociological sources are additionally listed with their actual reading status in the notes. Do not replace a partially read source with an invented complete citation.

## 10. Immediate implementation priorities

1. Open AnyLogic, create the two agents/population, paste the body and attach the two actions.
2. Pass the deterministic pair and six-node fixtures before stochastic scenarios.
3. Export a small batch, check distinct replication seeds, ingest CSV and compare against the matching reference rule/horizon.
4. Reproduce at least one low-φ long-horizon case and record the isolate switch.
5. Save the `.alp`, exported CSV, exact version and screenshots. Keep incomplete evidence labeled pending.

## 11. Spoken script for the selected product application

The timed13-minute presentation, including the live model, is [product_launch/SPEAKER_NOTES.md](product_launch/SPEAKER_NOTES.md). Use that script and PowerPoint for the course presentation.

“We simulate a hypothetical campus seller launching one reusable bottle to300 synthetic customers. We choose a price and a free-sample policy. Each person has their own budget, perceived value, awareness, experience and discussion contacts. People talk, close opinions move together, and an informed nonowner buys only when they can afford the bottle and think it is worth the price.

“Our opinion mechanism builds on Deffuant and adaptive-network work including Kozma and Barrat. Product seeding is also established prior work. Our contribution is a transparent decision comparison with explicit financial accounting and checks, rather than a new discovery of adaptive fragmentation.

“We compare policies within shared synthetic markets and keep pilot, exploratory follow-up and fresh-market confirmation distinct. On100 fresh markets, three samples rather than twelve improves modeled profit by Rs2,854.50 at the same price and degree targeting. The extra gain from degree over random targeting is small and uncertain. These contrasts have different purposes and should not be combined into an influencer-success claim.

“A surprising quality result exposes a limitation: a hard confidence cutoff can make moderate people ignore very positive owners. Removing the cutoff reverses that association, even without rewiring. This is a warning about the assumed mechanism, not advice to reduce real product quality.

“We ran the required AnyLogic product model and saved its screenshot and actual default export. It matches the matching Java reference. Large Monte Carlo results come from a separately labeled implementation. All inputs are synthetic, recommendations are conditional and no real-campus demand prediction is claimed.”

Sources for numerical lines: `product_launch/sim/analysis/confirmation_paired.csv`, `quality_paired.csv` and `actual_anylogic_exact_comparison.csv`.

### Historical opinion-mechanism script, for background questions only


“Our application is a hypothetical campus discussion platform choosing how many contacts to offer and whether to recommend similar or random new partners. Our question is whether people becoming more similar to their contacts can still leave a population divided into separate groups. We track opinions and paths between people separately.

We start with a published bounded-confidence mechanism, mainly Kozma and Barrat's adaptive model. Similar opinions move closer. Sufficient disagreement can cause a tie to be replaced, either randomly or with a similar person. All inputs are synthetic, and parameter values are scenarios rather than estimates of human behavior.

Our first runs suggested that denser networks required more rewiring to fragment. But many runs ended at the time cap. We extended those runs, and the apparently connected low-rewiring networks largely broke apart. That changed our conclusion: the earlier threshold mainly described how long we watched in those scenarios.

The model also makes an interesting distinction possible. Averaging always lowers overall opinion variance, yet separate opinion peaks and disconnected groups can develop. Agreement within contacts does not guarantee a connected population.

We did not find clear evidence for our hypothesis that choosing similar new contacts increases final fragmentation. We also found that the original rule forbidding new isolates can cause persistent searching. We therefore allow isolates in the recommended main model and retain the original as a sensitivity case. Capped time is not automatically a convergence time.

The original opinion-only port is separate from the selected product model. The product default has actual AnyLogic evidence; the background standalone reference and its benchmarks remain separately identified.”

After the students complete AnyLogic, replace only the final status statement with what they actually ran and the measured comparison. Use `VIVA_PREP.md` for questions, definitions and a shorter explanation.
