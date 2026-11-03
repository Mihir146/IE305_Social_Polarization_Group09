> **Background opinion/contact study.** The selected final application and its current evidence are in [product_launch/](product_launch/README.md). Product sales, experience and actual product-model engine runs are separate from the mechanism results below.

# Viva preparation

The answers describe the evidence at this handoff. Update implementation-status answers only from actual AnyLogic runs. Do not memorize a claim that a pending check has passed.

## One-page explanation for a smart non-expert

Imagine a campus platform where300 people discuss a proposed vehicle restriction, each holding a support score between0 and1. A link means that two people can interact. At first, opinions are spread across the range and links are placed randomly.

A randomly selected person talks to one randomly selected contact. If their opinions are sufficiently close, both move a little toward each other. For example,.20 and.30 become.23 and.27 when each moves30% of the distance. If they disagree too much, nothing happens to their opinions in that encounter. Instead, one may replace the contact with someone new. The replacement can favor similar opinions or be random.

There are two different outcomes to watch. **Opinion clustering** means people gather around a few distinct opinion values. **Network fragmentation** means the links split into disconnected pieces. People can disagree but remain linked. They can also occupy different network pieces while holding similar opinions. A single measure cannot describe both.

The basic mechanism is published work. Our project replicates it and examines contact choice, stopping time and measurement. The key follow-up came from runs that ended at the time limit. In one scenario, a network looked almost entirely connected after3000 sweeps. After30000 sweeps, the largest connected piece contained about58% of the population. Waiting longer changed our interpretation: apparent protection from fragmentation was largely a delay in those cases.

Another useful observation follows directly from averaging. Total opinion variance cannot increase under our update rule, even when the distribution develops separate peaks and the network breaks apart. A society can become more uniform within groups while losing communication between them. This model does not need opinions to become more spread out for the graph to divide.

One of our hypotheses failed. Favoring similar new contacts did not produce a clearly detected increase in final fragmentation in the tested comparisons. Speed differences also depend on the scenario. We additionally found that preventing new isolated people can leave a person searching forever when no compatible contact remains. A time limit is therefore not automatically a measured convergence time.

All input data are synthetic. Parameter values describe scenarios, not estimates of real people. Matching a published model checks implementation and behavior; it does not prove that a real population follows the mechanism. The required AnyLogic model must still be run and checked against its documented fixtures and the reference results.

## Twenty-five questions, easy to hard

1. **What is your research question?**  
   “We ask when opinion updates and changing social ties produce separate opinion groups, a disconnected network, or both. We also test whether the answer changes when we observe the simulation longer.”

2. **What does an agent represent?**  
   “One stylized campus participant with a scalar opinion. A graph edge is a topic-specific discussion connection, which can be replaced without ending an actual friendship. The number is an abstract opinion scale, not a measured personality or political score.”

3. **What do d,μ,φ and h control?**  
   “d is the maximum disagreement for compromise. μ controls how far each opinion moves. φ is the chance of trying to replace a disagreeing contact. h is the chance of selecting from similar non-neighbors when a replacement is attempted.”

4. **Show one opinion update.**  
   “With opinions.20 and.30,d=.20 andμ=.30, both are within confidence. The first becomes.23 and the second.27. We calculate both from the old opinions, preserving their sum.”

5. **Is your starting graph complete or guaranteed connected?**  
   “Neither. It is a uniform random simple graph with a fixed edge count. Some initial isolates or small components are possible. Our S≥.9 category means one large component, not exact connectivity.”

6. **Why choose uniform initial opinions?**  
   “It is a useful published-model benchmark and spreads opinions across the scale. It is a modeling assumption. We also tested an exactly Beta(2,2) centered distribution and a clipped bimodal mixture.”

7. **Why is the number of edges constant?**  
   “Every successful rewire deletes one edge and adds one. Self-edges and existing neighbors are excluded. Preventing isolates is a separate assumption; it is not needed to conserve edge count.”

8. **What is a sweep? Does everyone act once?**  
   “A sweep is N random activations with replacement. Some agents act repeatedly and some not at all. We use this integer clock to compare runs; it has no calibrated real-world duration.”

9. **How do you distinguish polarization from fragmentation?**  
   “We count separated major groups in opinion space and independently measure the largest connected graph component. Our echo-chamber label is an operational proxy requiring both kinds of division, not proof of hostility or misinformation.”

10. **Where do the rules come from?**  
    “The pair compromise is Deffuant's bounded-confidence rule. Kozma and Barrat provide the direct adaptive-network baseline. Homophilic reconnection also appears in Kan and co-authors, so that idea is not ours.”

11. **What is your contribution if the mechanism is already published?**  
    “An independent replication and controlled extension. Our most useful result is that a short observation horizon suggested a threshold that largely disappeared in longer runs. We also audited measurement cutoffs and the isolate restriction.”

12. **Which hypothesis failed?**  
    “H3 predicted more fragmentation with similar reconnection. Our paired intervals for the examined differences include zero. We report that as no clear support, not as proof that the two mechanisms are equivalent.”

13. **What changed about your threshold claim?**  
    “At d=.2 andφ=.005, degree8 and16 networks looked almost fully connected at3000 sweeps. At30000 sweeps their mean largest fractions were about.57. The earlier degree-dependent threshold described a finite observation horizon in these cases.”

14. **What is censoring, and why not discard capped runs?**  
    “We stop observing before the numerical freezing condition is met. Discarding those runs selects faster outcomes and can bias the result. We retain their snapshot KPIs, report their flags, and distinguish capped times from observed stopping times.”

15. **Can a capped run be something other than slow convergence?**  
    “Yes. Under isolate protection, a disagreeing two-node component can be blocked. An agent with no compatible person can also keep rewiring forever when its last tie is protected. We proved nonfreezing for all522 saved legacy states still flagged at30000. The recommended model allows isolates.”

16. **What did you verify directly?**  
    “Edge conservation, graph structure, reproducibility and hand-calculated metrics. Two separate triangles with opinions.2 and.8 give S=.5,K=2,cross fraction0,Q=.5 and variance.09. We also check conserved mean and the variance identity.”

17. **How close is the Kozma–Barrat comparison?**  
    “We use their scheduler, random reconnection,μ=.5,allow isolates and communication-path clusters. The consensus transition and its rewiring shift broadly match. Finite-N crossover and stopping/ensemble details prevent claiming an exact reproduction of every critical value.”

18. **Is HK's consensus threshold exactly.25?**  
    “No. It is a useful finite-population benchmark in their625-agent experiment. Our separate benchmark converges at that tolerance in all100 tested runs, but other formulations and sizes have different thresholds. We do not identify a universal constant.”

19. **Why not use Vazquez's mean-field formula to validate your φ?**  
    “It is a binary copying model with a different rewiring rule. Even there, mean field predicts2/3 at degree4 while simulations report about.38. We check a separate binary implementation; we do not transfer its number to our continuous model.”

20. **What do your95% intervals mean?**  
    “They quantify replication uncertainty under this synthetic model. New mean/difference intervals use a seeded bootstrap; proportions use Wilson intervals. They do not cover uncertainty about whether the model describes real people. Zero events in30 runs still allows a Wilson upper limit around11.4%.”

21. **Do common random numbers guarantee better comparisons?**  
    “No. Pairing can reduce the variance of a difference when covariance is positive. The A/B cells with fixed N,degree and initialization share their starting population. Changing degree or N consumes different initialization draws, so a reused seed label alone is not an identical population.”

22. **Are the opinion-cluster cutoffs arbitrary?**  
    “They are operational choices. We reclassified the same states using27 combinations. Gap and S-cutoff changes affected relatively few A labels, while changing the minimum group size from5% to1% changed112 of1440 labels. Small minorities matter.”

23. **How will you establish that AnyLogic agrees with the reference?**  
    “First run deterministic pair and graph fixtures. Then export genuinely distinct replications under matching parameters, horizon and isolate rule. Compare intervals for differences of means. Matching seed labels across Java and NumPy is not an exact-trajectory comparison.”

24. **How can you call it polarization if variance cannot rise?**  
    “Our term refers to separated opinion groups, not growing global spread. Symmetric averaging preserves mean and reduces variance by2μ(1−μ)(xi−xj)²/N. Rewiring leaves opinions unchanged. Separate peaks and broken communication can therefore coexist with lower variance.”

25. **What would be needed to claim this explains real polarization?**  
    “Evidence for the micro-rules, relevant parameter estimates and validation on independent real outcomes. Similar patterns can come from different mechanisms. Our model omits issue alignment, repulsion, noise and institutions. Bail's restricted field experiment also shows that attraction is not a universal response to opposing views.”

Answers17–22 refer to `VALIDATION_REPORT.md` and its raw/summary CSVs. Exact source rules and figure numbers are in `LITERATURE_NOTES.md`. If asked for an untested result: “We have not tested that; the evidence here does not establish it.”

## Glossary

| Term | Meaning in this project |
|---|---|
|Agent-based simulation|Individuals have states and interact through specified rules|
|Bounded confidence|Influence occurs only when opinion distance is inside a tolerance|
|Homophily|A tendency to connect or interact with similar others|
|Adaptive network|Node states affect links, and links affect later state changes|
|Compromise fraction μ|The fraction of the pair's opinion distance each moves|
|Scenario|One fixed combination of model inputs|
|Replication|One stochastic run with a specified independent replication seed|
|Monte Carlo experiment|Repeated stochastic runs used to estimate outcome distributions|
|Factorial grid|Examining combinations of factor levels, rather than changing one factor only|
|Sensitivity analysis|Checking how an outcome changes with an assumption, parameter or measurement rule|
|Common random numbers|Coupling scenario simulations through shared random inputs; not merely writing the same seed label|
|Paired comparison|Compare the same replication index across scenarios before averaging differences|
|Opinion cluster|Here a group separated by a gap in sorted opinions; KB instead uses compatible-edge paths|
|Major cluster|A gap group containing at least the chosen fraction of all agents|
|Consensus|Strictly, shared opinions. Our K=1 classification means only one major group|
|Polarization|In our operational usage, separated major opinion groups; not necessarily extreme positions|
|Connected component|A maximal group in which every pair is joined by some graph path|
|Giant component|A component occupying an appreciable fraction of the population; S is its measured fraction|
|Fragmentation|Here an operational network criterion S<.9; some papers use the word for many opinion groups|
|Cross-cluster edge fraction|The fraction of all edges joining different opinion-cluster labels|
|Modularity Q|Within-group edges compared with a degree-based random-network expectation, for a specified partition|
|Echo-chamber proxy|Opinion separation aligned with network separation; not a direct measure of message reinforcement|
|Absorbing state|No allowed update can change the system. Numerical freezing is an approximation|
|Metastable state|A configuration that persists a long time but can eventually change|
|Right censoring|Observation ends before the event of interest is observed|
|Restricted mean time|The average of min(event time,cap); not the uncensored event-time mean|
|Bootstrap interval|Uncertainty interval from resampling replications or replication pairs|
|Wilson interval|A binomial-proportion interval that remains useful with small counts or zero events|
|Verification|Checking that code implements its stated rules and calculations|
|Validation|Checking whether behavior matches appropriate external targets, within a stated scope|
|Calibration|Estimating inputs from evidence; not performed on real people here|
|Identifiability|Whether observations can distinguish particular parameters or mechanisms|

## Personal rehearsal checklist

Each student should explain the activation loop, compute the two-person example, identify the source baseline, interpret a capped run, explain why H3 failed, and point to the actual AnyLogic export. Swap presenter roles. A good answer states the conclusion, the evidence and its limit in two or three sentences.
