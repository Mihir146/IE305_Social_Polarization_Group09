# Can more contacts prevent echo chambers—or only delay them?

**Contact recommendations for a synthetic campus discussion platform**  
Mihir Vasave and Vaibhav Mathur · IE305 Simulation Lab · 3 November 2026

**Implementation status:** Reference experiments and analysis are complete. The AnyLogic port is prepared but has not been compiled or run in AnyLogic. Add actual model/export evidence before submitting this as an implemented AnyLogic project.

## Abstract

We study a hypothetical discussion platform whose users can replace disagreeing contacts. The platform varies contact capacity and whether new partners are chosen randomly or by opinion similarity. A continuous bounded-confidence model separates opinion grouping from graph fragmentation. The main finding is sensitive to observation time: in a 300-agent scenario, a degree-8 network's mean largest component falls from .9986 at 3,000 sweeps to .5761 at 30,000. A further policy study shows that a nearly full giant component can coexist with very few cross-group links. Final contact-selection differences are not clearly detected in the tested paired comparisons. These are synthetic mechanism experiments, not estimates of a real campus population.

## 1. Application and research question

Imagine a university consultation on restricting private vehicles on campus. Students use a platform that recommends topic-specific discussion partners. An operator can offer more contact capacity or change partner selection. It wants to maintain communication between different views without assuming that every disagreement is harmful.

Our question is: **How do contact capacity, partner recommendations and observation horizon affect opinion groups and network connectivity?** An edge is a mutual discussion connection; it is not an actual friendship or a ranked-feed impression. We do not estimate a monetary optimum, measured satisfaction or a real-world campaign duration.

`APPLICATION_DESIGN.md` gives the complete domain mapping and synthetic input/output schema. The alternative product-launch application remains a proposal. This report contains no simulated sales or purchase probabilities.

## 2. Established foundation and our assumptions

**Established literature:** Deffuant et al. introduce the pairwise bounded-confidence compromise rule. Kozma and Barrat study the direct adaptive-network baseline. Similarity-based reconnection also appears in Kan, Feng and Porter. Pansanella et al. distinguish opinion stabilization from later network separation. The mechanisms and the broad timing distinction are prior work.

**Our assumptions:** homogeneous tolerance and susceptibility, one continuous opinion, a simple undirected graph with fixed edge count, a hard confidence cutoff and a mixture of random/similar reconnection. Initial opinions, graph size and parameter values are synthetic scenarios. No human parameter has been estimated.

**Our contribution:** replication and a controlled extension through contact-policy experiments, horizon checks, stopping diagnostics and measurement sensitivity. To our knowledge, we did not locate this exact combination of controls in the reviewed sources; this is not an exhaustive novelty claim. Source equations, figure locations and reading limits are in `LITERATURE_NOTES.md`.

## 3. Model

Agent i has opinion xᵢ in [0,1]. A value of 0 means full opposition to the illustrative proposal and 1 full support. The initial graph is G(N,M), with M=floor(Nk₀/2) distinct undirected links. Initial opinions are independent Uniform(0,1). The main grid also checks centered and bimodal starts.

Each activation chooses a uniform agent and one uniform neighbor. An isolate has no interaction. If |xᵢ−xⱼ|<d, both move toward the other's **old** opinion:

`xᵢ′ = xᵢ + μ(xⱼ−xᵢ)`; `xⱼ′ = xⱼ + μ(xᵢ−xⱼ)`.

For example, .20 and .30 become .23 and .27 at μ=.30. Otherwise, a φ coin permits a replacement attempt. With probability h the new partner is uniform among compatible non-neighbors; otherwise it is uniform among all non-neighbors. An empty compatible set falls back to all non-neighbors. Choose the candidate before cutting, exclude self-links and duplicates, then replace one edge by one.

The recommended main process allows isolates. The earlier version protected the dropped neighbor's last link. Both conserve edge count, but protection can prevent numerical freezing; we retain that variant as a sensitivity case.

A sweep consists of N activation attempts with replacement. Check every 10 sweeps: compatible edges must differ by at most 10⁻³, and with φ>0 no discordant edge may remain. This is a numerical stopping rule, not exact mathematical absorption. A capped run supplies a snapshot and a censoring flag. Sweeps have no calibrated conversion to days.

Symmetric compromise preserves mean opinion and changes population variance by

`ΔVar = −2μ(1−μ)(xᵢ−xⱼ)²/N ≤ 0`.

Rewiring leaves opinions unchanged. Thus separate opinion peaks and disconnected groups can emerge while total variance falls. “More polarized” cannot mean increasing global variance in this particular model.

## 4. Data and experimental design

The matched primary grid contains 2,790 runs, 30 replications per cell, cap 30,000 and isolates allowed. It varies tolerance, rewiring, contact selection and selected initialization/size/susceptibility factors. The original protected-isolate grid remains unchanged for comparison. All 707 originally capped runs were extended under their original rules.

The focused application uses N=300, d=.2, μ=.3 and φ=.005. Three initial degrees (4,8,16) correspond to contact budgets of 600,1,200 and 2,400 links. Two recommendation rules (h=0,1) give six policies, each with 30 replication indices. Five observation horizons yield 900 rows from **180 realizations**. Snapshots of the same realization are not independent replications.

Within a degree, h comparisons share initial graphs and opinions. Changing degree consumes different initialization draws, so cross-degree comparisons do not hold every initial opinion fixed. New uncertainty intervals use a seeded 10,000-resample percentile bootstrap for means/paired differences, and Wilson intervals for proportions. They quantify simulation sampling uncertainty, not uncertainty about real human behavior. They are pointwise, without multiplicity adjustment.

## 5. Measures

Opinion groups are formed by sorting opinions and splitting at gaps greater than .05. K counts groups containing at least 5% of agents. S is the largest topological connected component divided by N. We classify S<.9 as fragmented. Cross-group edge fraction and fixed-partition modularity describe alignment between opinions and links.

These conventions have limits: K=1 does not prove universal agreement; S≥.9 does not imply exact connectivity; modularity does not establish antagonism. A diffuse initial opinion distribution can already have K=1. We therefore report multiple measures and sensitivity to their cutoffs.

## 6. Results

### 6.1 The apparent threshold depends on how long we observe

For h=1 at φ=.005, mean S changes as follows; each row has 30 matched replications:

| Initial degree | S at 3,000 sweeps | S at 30,000 sweeps | Fragmented observations, short→long |
|---|---:|---:|---|
|4|.8356|.6031|11/30→29/30|
|8|.9986|.5761|0/30→29/30|
|16|1.0000|.5677|0/30→30/30|

Source: `sim/primary_horizon_summary.csv`; intervals are in the CSV and interactive figure. The first tested crossing of a 50% observed fragmentation proportion moves from (.01,.02] to (0,.005] at degree 8, and from (.02,.05] to (0,.005] at degree 16. These are grid brackets, not fitted critical values or proof of a mathematical transition at zero.

More contacts preserve connectivity longer in these scenarios. They do not establish permanent protection. This revises the earlier interpretation of a positive long-run rewiring threshold.

### 6.2 A giant component can conceal weak cross-group communication

At degree 8 and 3,000 sweeps, random versus similar recommendations yield mean S=.99944 versus .99856. Yet mean cross-group edge fractions are .08994 versus .01769. A few remaining bridges keep most users mutually reachable while most links already stay within groups.

At degree 16 and 30,000 sweeps, random recommendations appear to retain a much larger component, but 11/30 runs remain active. Extending to 300,000 removes those flags. The final paired difference S(similar)−S(random) is −.00556, with interval [−.01489,.00444]. The other two degree-specific final intervals also include zero. This is no clear detected difference, not statistical equivalence. Sources: `application_summary.csv`, `application_paired.csv`.

### 6.3 The original preferred hypothesis failed

H3 predicted that similar reconnection produces more final fragmentation. All six original B-cell paired intervals include zero. Speed effects vary by scenario: at d=.15,φ=.25 mean numerical stopping time changes from 385.67 to 148.33 sweeps for random→similar reconnection, while at φ=1 the means are 115.67 and 147.00. A universal speed advantage is unsupported. Source: `primary_h3_paired.csv`.

### 6.4 Stopping and KPI choices matter

Of 707 originally capped protected-isolate runs, 522 remain flagged at 30,000. Saved-state proofs identify an unmatched nonisolated agent in 520 cases and blocked structures in the remaining 2. These cannot pass the old freezing rule. The recommended isolate-allowed full grid has no capped runs at 30,000.

Reclassifying 1,440 primary A states across 27 cutoff combinations changes relatively few labels for individual gap or S-cutoff changes. Lowering the minimum major-group fraction from 5% to 1% changes 112 labels. Small minorities therefore affect interpretation. These audits change neither trajectories nor raw opinion states.

## 7. Verification and validation

The acceleration engine reproduces all 2,790 saved legacy output rows and matches the readable reference on five small seeded trajectories. Hand calculations and structural identities provide additional verification.

Dedicated published-model checks comprise 4,410 KB runs, 500 synchronous HK runs and 700 binary voter runs. HK reproduces the finite-N consensus pattern at ε=.25. KB reproduces the broad crossover and its shift with w, but the exact d₁ and d₂ critical values are only partially matched. The binary model reproduces the crossover region and approach to two large components, without a precise critical-point fit. Eight high-w KB runs remain capped. Full pass/partial/pending judgments are in `VALIDATION_REPORT.md`.

AnyLogic remains the required implementation. Its API audit, code bodies, export contract and deterministic checklist are supplied. **No actual AnyLogic compile, run or cross-implementation agreement is claimed.** Add version, actual fixture outcomes, independent CSVs, comparison intervals and saved `.alp` here after execution.

## 8. Interpretation and limits

For a hypothetical operator, the design implication is to evaluate both connectivity and cross-group links over a specified interaction horizon. Reducing disagreeing links can coexist with loss of communication. A short consultation and a long-run segregation study ask different questions.

The model omits repulsion, media, noise, heterogeneous tolerance, user turnover, multi-issue attitudes and a changing edge budget. It has no empirical calibration. Different mechanisms can create similar macroscopic patterns. The result demonstrates what these assumptions can produce; it does not predict a real campus or establish a policy that optimizes welfare.

## References and provenance

The complete verified records and claim audit are in `LITERATURE_NOTES.md`. Principal sources are [Deffuant et al.2000](https://doi.org/10.1142/S0219525900000078), [Kozma & Barrat2008](https://doi.org/10.1103/PhysRevE.77.016102), [Kan et al.2023](https://doi.org/10.1093/comnet/cnac055), [Pansanella et al.2022](https://doi.org/10.1007/s41109-022-00495-7) and [Newman2006](https://doi.org/10.1073/pnas.0601602103).

AI assistance was used for source review, coding, experiments and drafting. The students should understand and verify the submitted work, record their actual AnyLogic contribution and follow their course's disclosure requirements. This statement does not claim that pending work has already happened.
