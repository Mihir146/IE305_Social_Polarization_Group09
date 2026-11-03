# Application: contact recommendations for a campus discussion platform

**Historical contact-policy case study.** The students selected the product-launch application, now implemented in [product_launch/](product_launch/README.md). Its sales experiments and actual AnyLogic evidence are separate from the contact results below. All inputs and outcomes are synthetic.

## 1. A concrete setting and decision

A hypothetical university runs an online consultation about restricting private vehicles on campus. Students choose discussion contacts. The operator can change how many mutual discussion links are available and how new partners are recommended. It wants to preserve communication between students who disagree while understanding the trade-off with locally agreeable conversations.

An edge represents a **topic-specific discussion connection**. It does not mean that students end an actual friendship over this issue. The model does not simulate posts, ranked news feeds or directed follower relationships.

**Decision question:** At a stated consultation horizon, does a larger contact budget or a different partner-recommendation rule preserve a large connected community and cross-group communication? Does an apparent advantage persist when we observe longer?

This is a finite-horizon design comparison. The operator chooses contact budget and recommendation policy. Tolerance, susceptibility and disagreement-driven contact replacement describe uncertain user behavior; they are scenario assumptions, not quantities the operator can directly set.

## 2. What each input means

| Model quantity | Application meaning | Data status |
|---|---|---|
|300 agents|A synthetic cohort of platform participants|Chosen study size; not a measured campus sample|
|Opinion x in[0,1]|Support for the proposal;0 means fully oppose,1 fully support|A constructed continuous scale; uniform initial values are an assumption|
|Initial G(N,M) graph|Mutual opportunities for topic-specific discussion|Synthetic random graph; no surveyed friendships|
|Mean degree k₀=4,8,16|Initial contact capacity, corresponding to600,1200,2400 undirected links|Policy/resource scenarios, not money costs|
|d=.2|The largest opinion distance permitting compromise|Uncertain behavioral assumption|
|μ=.3|Each compatible participant moves30% toward the other's old opinion|Published mechanism; numerical value is assumed|
|φ=.005|A .5% chance of attempting replacement after a discordant encounter|Low-replacement scenario; not an estimated user rate|
|h=0 or1|Uniform versus compatible-opinion partner selection when a replacement occurs|Idealized recommendation-policy alternatives|
|One sweep|300 independent activation attempts|An interaction clock with no conversion to hours or days|
|Isolates allowed|A user may end up without a discussion contact|Primary model choice, recorded as an outcome|

At h=1, an empty compatible candidate set falls back to random non-neighbors. “Random” and “similar” are exact sampling rules; neither is a claim to reproduce a deployed commercial recommender.

## 3. Where the data come from

The input example consists of300 synthetic opinion rows in `data/synthetic_people_seed1000_k8.csv` and1200 unique undirected contacts in `data/synthetic_contacts_seed1000_k8.csv`. Both come from the same initialization used by the reference model. All other initial populations can be regenerated from the logged seeds and factors; there are no invented empirical records.

`sim/run_application.py` runs six policies: three contact budgets × two recommendation rules, with30 replication indices per policy. It records snapshots at300,1000,3000,30000 and300000 sweeps. These are **180 stochastic realizations and900 repeated-measure rows**, not900 independent realizations. The script replays each seed to the requested horizon; after numerical freezing the returned state is unchanged.

Within each degree, the h policies start from identical graphs and opinions. Across degrees, the original RNG convention does not preserve identical opinions. The degree comparison is therefore an ensemble comparison, not a controlled experiment holding every starting opinion fixed.

The study extends the original design after seeing horizon sensitivity. It is exploratory. It must not be advertised as a previously registered hypothesis test or pooled with overlapping D-grid seeds to inflate sample size.

## 4. What the output measures mean

- **S, largest component fraction:** how much of the cohort remains reachable within its largest discussion component. S≥.9 is an operational target, not complete connectivity.
- **Cross-group edge fraction:** the share of links between different sorted-opinion gap groups. It measures links, not how often users read messages or how hostile they feel.
- **Discordant edge fraction:** links whose endpoints differ by at least d. A low value means less modeled disagreement on links, not measured satisfaction.
- **Major opinion groups K:** groups with at least5% of agents under gap .05. Initial diffuse opinions can have K=1, so K alone does not establish consensus.
- **Isolated fraction and cap flag:** users without contacts, and whether the state is still active when observation ends.

We keep network reach and cross-group communication separate. A tiny number of bridges can keep S near1 while almost every contact stays within an opinion group. The model has no objective function valuing disagreement, inclusion or operational cost in monetary units; those preferences would have to be supplied before claiming an optimal platform policy.

<!-- APPLICATION RESULTS -->

| Mean degree / contact budget | Recommendation | S at3000 | S at30000 | S at300000 | Capped at30000→300000 |
|---|---|---:|---:|---:|---|
|4 / 600|Random|0.9602|0.5927|0.5927|0→0|
|4 / 600|Similar|0.8356|0.6031|0.6031|0→0|
|8 / 1200|Random|0.9994|0.5652|0.5652|0→0|
|8 / 1200|Similar|0.9986|0.5761|0.5761|0→0|
|16 / 2400|Random|1.0000|0.7254|0.5732|11→0|
|16 / 2400|Similar|1.0000|0.5677|0.5677|0→0|

Source: `sim/application_summary.csv`;30 realizations per policy. At the final cap, all180 realizations freeze numerically. All three final paired intervals for S(similar)−S(random) include zero; see `sim/application_paired.csv`. At degree16 the apparent30000-sweep difference is strongly affected by11 still-active random-policy runs.

At degree8 and3000 sweeps, mean cross-group edge fraction is.08994 with random recommendations and.01769 with similar recommendations, while mean S remains.99944 and.99856. Thus a nearly full giant component can conceal a large reduction in cross-group links. These are modeled links, not observed exposure or satisfaction.


## 5. What this application establishes

For these synthetic populations, adding links can preserve a large connected component over a finite observation window. It does not establish permanent protection. Likewise, similarity-based recommendations can remove cross-group links faster without producing a clearly distinguished final S in the paired comparisons after all tested realizations freeze numerically.

The duration matters to the decision. A platform running a short consultation may reasonably care about transient connectivity; a researcher claiming an enduring phase boundary needs longer observation and appropriate diagnostics. Our sweeps do not identify a real consultation's duration.

This is an application of established opinion/network mechanisms. Kozma–Barrat already study adaptive separation; Pansanella2022 and Zhao2026 study distinct timescales/pathways. Our contribution is the documented contact-budget/policy comparison and the audit that changes its interpretation. See `LITERATURE_NOTES.md` for full attribution and reading limits.

## 6. Product launch: the alternative discussed with the students

**Proposed question:** With a fixed free-sample budget, should a firm target highly connected people or distribute samples across social groups to generate more paid purchases?

A one-time purchase, such as a new reusable bottle, gives a manageable setting. Repeated subscriptions would also require renewal/churn decisions. A product model needs four distinct states: awareness, perceived value or willingness to pay, affordability and whether a paid purchase has already occurred. Receiving a free sample must be recorded separately from paying for a product.

The existing graph, bounded-confidence discussion and seed/replication machinery can be reused. The current simulator does **not** model awareness transmission, product experience, sample-induced beliefs, payment or profit. Adding those is a substantive model extension. Existing opinion outcomes cannot be relabeled purchase probabilities or sales.

A focused design would keep one product, fixed price, fixed quality assumptions and an equal sampling budget. Compare random, highest-degree and group-distributed seeding under h=0 versus h=1. Define the group-distribution rule from pre-campaign information; do not use final outcomes to select seeds. Report paid buyers, net revenue after samples, time to a sales target and adoption across groups.

A simple purchase decision could require awareness, no previous purchase, sufficient budget and perceived value above price. Then the probability of a purchase across synthetic realizations is an output. A logistic purchase rule is another assumption, but its coefficients would require sensitivity analysis. Repeating a positive purchase-probability coin forever would make nearly everyone buy eventually, so the purchase-opportunity process and finite campaign horizon must also be specified.

The experience mechanism is still a design choice: what does a sample tell its recipient, how noisy is that signal, and how does it enter an existing belief? Social averaging alone preserves the population mean and cannot represent advertising that raises average product valuation. If an external experience or marketing signal is introduced, the old variance invariant must be restricted to compromise events rather than asserted for the full product model.

Literature starting points are [Bass1969](https://doi.org/10.1287/mnsc.15.5.215), which concerns timing of initial purchases, and [Kempe, Kleinberg & Tardos2003](https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf), which concerns influence-maximizing seed selection. Only metadata/abstract and introductory material were checked for this domain discussion; these are **not a completed marketing literature review**. A new product implementation would require reading the relevant models fully, choosing the added rules, updating the AnyLogic port, and validating the new outcomes.

The product proposal was subsequently implemented. Use `product_launch/PROJECT_REPORT.md`, its raw sales CSVs and `CampusProductLaunch.alp` for the selected final application. The specification below records the earlier proposal; the authoritative implemented rules are in `product_launch/MODEL_SPEC.md`.
