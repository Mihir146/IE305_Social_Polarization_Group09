# Literature Notes: what the papers actually say and what we learned

**Written 3 Nov 2026. Read this before presenting; it changes the framing in earlier files.**

## 0. What was and was not read

- **First session (21 Oct):** I only ran searches and used abstracts/snippets. No paper was read in full. The earlier blueprint's literature table was built on that, and a few claims in it were wrong or overstated (corrections in §3).
- **Now:** I read the full text of the seven papers below, through a fetch tool that returns a summary of each page's text.

| Paper | Read | Limits of the reading |
|---|---|---|
| Kozma & Barrat 2008 | Full text (PDF) | Some equations and numbers garbled in extraction (marked below) |
| Holme & Newman 2006 | Full text | Good |
| Vazquez, Eguíluz, San Miguel 2008 | Full text except the last ~5,000 characters | Good |
| Sasahara et al. 2021 | Full text | Good |
| Baumann et al. 2020 | Full text | Good |
| Deffuant et al. 2000 | Full text | **Equations and parameter values garbled**; critical numbers not recoverable |
| Hegselmann & Krause 2002 | Full text | Several equations garbled |
| Flache et al. 2017 | Two reads covering most of the page | Parts of the recommendations section only partly visible |
| Nardini et al. 2008, Gross & Blasius 2008, Diakonova et al. 2015, Bail et al. 2018 | **Abstracts only** | Cite them only for what the abstract says |

Anything below marked *(garbled)* should be checked on the publisher page before it goes in the report.

---

## 1. Paper by paper

### Kozma & Barrat (2008), Phys. Rev. E 77, 016102. **Our closest relative.**
- **Their model:** N agents (500 to 20,000), opinion in [0,1] uniform at start, Erdős–Rényi network with mean degree k̄ (mostly 10). Pick a random node and a random neighbour. If opinions differ by ≤ d, both move toward each other by μ (they use μ = ½). With probability w the pair is instead tested for rewiring, which happens **only if they disagree (> d)**: the link i–j is replaced by i–k with **k a uniformly random non-neighbour, chosen without looking at its opinion**. A run stops when no link joins different opinions.
- **Static case (w = 0), k̄ = 10:** consensus gives way to a polarized state with two macroscopic clusters at d ≈ 0.256 (largest cluster drops from ~N to ~N/2, sharper with larger N, read by the authors as first-order). Fragmentation (no large cluster) below d ≈ 1/(2k̄) ≈ 0.05, a heuristic percolation argument.
- **Adaptive case:** the consensus-to-polarization threshold shifts to **larger d** as w grows ("the more easily agents can change their connections, the larger tolerance values are necessary to achieve consensus"). The total cluster count is much smaller than in the static case; the fragmented phase disappears. In the polarized phase **each opinion cluster becomes its own connected component** (the network breaks into as many pieces as clusters).
- **Timescales:** three stages: early (loners merge, network still connected), intermediate (clusters form and can split), late (links between differing clusters are cut). No direct speed comparison with the static case; at low w the late stage dominates and gets slow.
- **Variant:** agents beyond d still interact with a decaying probability; static always reaches consensus; the adaptive case still shows a consensus-to-polarization transition, shifted to larger d. Conclusion: transitions are "more robust" on adaptive networks.
- **Limits they state:** mostly Erdős–Rényi, μ = ½, random-target rewiring only, scaling arguments are heuristic, several results "not shown", no numeric critical w.

### Holme & Newman (2006), Phys. Rev. E 74, 056108
- **Model:** **discrete** opinions (G of them, γ = N/G holders each). Pick a vertex; with probability φ move one of its edges to a random vertex **with the same opinion** (rewire-to-similar); otherwise copy a random neighbour's opinion.
- **Results:** for k̄ = 4, γ = 10, **φ_c = 0.458 ± 0.008**; near φ_c the community sizes follow a power law with exponent ≈ 3.5; a giant community of like-minded agents forms at the transition. At φ → 1 communities are the initial opinion holders; at φ → 0 they are the initial graph components. Convergence time: ~log N at φ = 1, ~N at φ = 0, scaling ~N^0.61 at criticality.
- **Limits:** numerical only, large-G regime only, multi-edges allowed, **initial conditions not systematically tested**.

### Vazquez, Eguíluz & San Miguel (2008), Phys. Rev. Lett. 100, 108702
- **Model:** **binary** states, degree-regular random graph (μ = 4 in the simulations). Pick a node and a neighbour; if states differ, with probability p the node **rewires to a random node in its own state**, otherwise copies the neighbour.
- **Mean field:** p_c = (μ − 2)/(μ − 1), which is 2/3 for μ = 4. **Simulations give p_c ≈ 0.38**, so the mean-field value is substantially too high (the authors blame correlations). Time scale diverges near p_c, τ ~ |p_c − p|⁻¹.
- **Structure:** below p_c the network stays one connected component (active phase); above p_c it ends in **two large components of opposite state, giant component ≈ N/2**.
- **Limits:** mean-field closure, only μ = 4 simulated in the part I read.

### Sasahara et al. (2021), J. Comput. Soc. Sci. 4
- **Model:** opinions in [−1, 1], N = 100, 400 directed edges, bounded confidence ε = 0.4, μ = 0.5, users see the 10 latest messages from friends, repost with probability p = 0.5, **unfollow a discordant poster with probability q = 0.5** and follow someone new (random, repost-based or recommendation-based).
- **Results:** influence alone or rewiring alone gives polarization only "after a very long time"; **when both rates are above 0.1, echo chambers appear in a fraction of the time** (they say about an order of magnitude). The three new-link rules give **comparable stable states** (similar cluster counts and diversity); **recommendation-based (similarity-based) rewiring converges more than twice as fast**, and repost/recommendation produce more closed triads and hubs.
- **Twitter comparison is weak evidence:** the simulation is stopped when its segregation matches the data (so that match is built in), the closed-triad match is "consistent" with no numbers, and the empirical fit needs different parameters (ε = 0.65, μ = 0.015, N = 18,470).
- **Limits:** idealised, one-dimensional opinions, some undefined behaviour (no concordant message on the screen), the "inevitability" claim depends on parameter regime.

### Baumann et al. (2020, arXiv 1906.12325)
- **Model:** continuous opinions with *conviction* (sign = stance, magnitude = strength), dynamics ẋ = −x + K Σ A(t) tanh(α x_j), heterogeneous activity, homophily exponent β, reciprocity r; temporal network ~100× faster than opinions.
- **Results:** three regimes (neutral consensus, one-sided radicalization, polarization). Consensus is destabilised by social-influence strength K and topic controversialness α; mean-field α_c ≈ 1/((1+r)K m ⟨a⟩). **Polarization is metastable** and decays to one-sided radicalization for moderate β. Echo chambers are identified visually, no scalar index. Twitter comparison is qualitative with hand-picked parameters.
- **Relevance:** it needs reinforcing ingredients (saturating odd influence, reciprocity) to reach extreme opinions. It does not test bounded confidence directly.

### Deffuant et al. (2000) *(equations garbled in the text I could read)*
- Uniform initial opinions on [0,1]; μ between 0 and 0.5; only pairs within threshold d interact. High d gives consensus; low d gives several clusters; d "controls the number of peaks". **μ and N "only influence convergence time and the width" of final opinion peaks.** Square lattice (29×29): consensus except isolated "extremist" agents; other networks conjectured, not simulated.
- **Not recoverable:** the exact consensus threshold and any "clusters ≈ 1/(2d)" formula. I earlier suggested that formula from memory; **do not cite it** unless you verify it in the paper.

### Hegselmann & Krause (2002)
- Opinions in [0,1], 625 agents, each agent moves to the mean of all agents within ε; simultaneous updating. Fragmentation → polarization → consensus as ε rises: about **two camps at ε ≈ 0.15 and consensus at ε ≈ 0.25** (approximate, read from simulations; no exact critical value). Random serial updating gives extreme opinions "a slightly better chance to survive"; main effects do not depend critically on simultaneous updating. Networks left as future work.

### Flache et al. (2017), JASSS 20(4)
- Three model classes: assimilative influence, similarity-biased influence (bounded confidence, homophily), repulsive influence. **Bounded confidence cannot produce opinions beyond the initial range** ("a population cannot become more extreme than its initial extremists"). Even "subtle and seemingly innocent changes in the assumptions" can change predictions. **More initial opinion variance raises the chance of bi-polarization; outcomes depend on the exact initial distribution.** Updating scheme: pairwise vs simultaneous mainly changes details. They ask modellers to justify ingredients, test whether results hinge on assumptions, and compare models within a class. Key parameters (confidence thresholds) are largely unmeasured empirically. Their own illustrative runs use uniform initial opinions, N = 100; uniform is one case, not a neutral default.

---

## 2. Check of our simulator against Kozma & Barrat

Ran our reference model on their setup (ER graph, k̄ = 10, μ = 0.5, uniform opinions, N = 500 vs their 1,000, 8 replications per point; KB's w maps to our φ = w/(1 − w), so our φ = 1 is w = 0.5; h = 0 to match their random reconnection). Largest opinion cluster as a fraction of agents (clusters defined by gaps > 0.02 in sorted opinions, not their path definition):

| d | static | adaptive (w = 0.5) |
|---|---|---|
| 0.15 | 0.42 | 0.44 |
| 0.20 | 0.57 | 0.59 |
| 0.25 | 0.68 | 0.56 |
| 0.27 | 0.80 | 0.67 |
| 0.30 | 0.98 | 0.94 |

Total number of opinion clusters (static → adaptive): 10.4 → 3.6 at d = 0.15, 6.8 → 2.5 at d = 0.20, 16.0 → 6.6 at d = 0.08.

**What this supports:**
- Static consensus-to-polarization transition around d ≈ 0.25 to 0.30. KB report 0.256; ours is smoother (smaller N, different cluster definition, 8 replications). **Broadly consistent, not an exact match.**
- Adaptation shifts the transition to larger d (at d = 0.25 and 0.27 the adaptive largest cluster is clearly smaller). **Matches KB.**
- Adaptation reduces the total cluster count a lot. **Matches KB.** (Our major-cluster count K barely changes because it ignores clusters under 5% of agents, and the reduction comes from small "debris" clusters. This is why F2 does not contradict KB.)

**What this does not support:**
- KB's d₂ ≈ 1/(2k̄) ≈ 0.05 fragmentation point: **not checked**. At d = 0.03 our gap-based cluster measure is meaningless because opinions barely move and sit evenly across [0,1]. A path-based cluster definition would be needed.
- Our no-isolate rule differs from KB (they allow isolated agents). This is a deliberate difference; say so.
- Many adaptive runs hit the time cap (up to 6 of 8 at tiny d), so these are snapshots.

---

## 3. Corrections to what I told you earlier

| Earlier claim | What the papers say |
|---|---|
| Holme & Newman note the transition "depends on the initial state" (blueprint §2 and §7) | That statement came from a review's summary. The paper itself does **not** test initial conditions. Removed. |
| Test our model against Vazquez's p_c = (μ−2)/(μ−1), e.g. 0.86 for mean degree 8 (earlier chat) | That mean-field value is too high: the paper itself gets 2/3 theoretical vs ≈ 0.38 simulated at μ = 4. Compare qualitatively (threshold rises with mean degree), never to the formula's number. Also, their model is binary with rewire-to-same and copying; ours is continuous with no copying. |
| Sasahara: "even minimal influence and unfriending produce echo chambers"; Twitter data is a "validation target" | Each mechanism alone is very slow; **both above 0.1 together** are fast. The Twitter match is partly built in (stopping rule). Use it as qualitative context only. |
| Deffuant: clusters ≈ 1/(2d) (earlier chat, from memory) | Could not be verified in the text I could read. Do not cite. |
| Kozma & Barrat as one of several related works | It is **nearly our model** (h = 0 version). This changes the novelty claim (see §4). |

I have patched the blueprint and the 5-hour plan for these.

---

## 4. What we actually learned, and what it means for the project

1. **Our core result is a replication, not a discovery.** Kozma & Barrat already show that adaptive rewiring turns each opinion cluster into its own component, shifts the consensus threshold to larger d, and reduces cluster counts. Our F1 and the d-shift reproduce that. **Say so.** The honest headline is: *"We reproduced the Kozma–Barrat results with an independent implementation and extended them."*
2. **What is plausibly ours (check before claiming):**
   - the explicit **h parameter** (similar vs random reconnection) inside a bounded-confidence model. KB only studied random reconnection; Sasahara compares link rules but in a message-sharing model. Our finding that h changes speed, not the end state, agrees with Sasahara's result that link rules give comparable stable states with faster convergence for similarity-based rules.
   - the **regime classification** (consensus / polarized-connected / echo chambers) with probabilities and confidence intervals, plus cross-cluster edge fraction and modularity as KPIs;
   - the **mean-degree dependence** of the rewiring threshold in this bounded-confidence setting (qualitatively consistent with Vazquez's mean-field dependence on mean degree, not yet compared with anything quantitative in KB).
   I could not find these in the seven papers, but I did not do a systematic literature search for them, so phrase it as "to our knowledge" and as an extension.
3. **The "slow near the transition" result has a published explanation.** Vazquez et al. attribute their transition to a competition of time scales with a diverging relaxation time; KB identify three time scales. Our censoring spike at small φ is probably this effect, but our runs are capped, so threshold locations are approximate.
4. **Starting distribution matters** (Flache et al.: more initial variance raises the chance of polarization). Our centred-start result (F6) fits this.
5. **Our model cannot make extremists** (Flache; Baumann). State it as a limitation, not a bug.
6. **Update scheme and N are secondary** (Deffuant: μ and N affect convergence time and peak width; Flache/HK: update scheme mostly affects details). This matches our sensitivity results F7.
7. **Everything validated so far is qualitative or approximate.** The one quantitative anchor (KB's d ≈ 0.256) agrees only roughly. Say "broadly consistent".

## 5. What to say if the professor asks "what did you learn from the literature?"

"The closest published model is Kozma and Barrat's adaptive Deffuant model. They show that when agents can drop ties after disagreement, each opinion cluster ends up as its own disconnected component, and the tolerance needed for consensus goes up. We re-implemented that, checked it against their results, and extended it with a parameter for how new contacts are chosen. Sasahara and co-authors found that influence and unfollowing together are much faster at producing echo chambers than either alone, and that the rule for choosing new contacts changes speed more than the end state, which matches what we saw. Vazquez and co-authors explain the connected-to-fragmented switch as a race between two time scales, and note that their mean-field formula for the switch overestimates it, so we compare only qualitatively. Flache and co-authors warn that results depend on assumptions like the starting opinion distribution, which is why we test other distributions."
