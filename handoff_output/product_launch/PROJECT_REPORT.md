# Can a smaller giveaway make a better product launch?

**An agent-based simulation of price, free samples and word of mouth**  
IE305 Simulation Lab · Group 9 · Mihir Jagdish Vasave and Vaibhav Mathur

## 1. The business question

A hypothetical campus seller is introducing one reusable bottle. The seller can choose the price and whom to give free bottles to. News travels through customer contacts; hearing about the product does not guarantee a purchase. We ask which tested launch policy earns more modeled campaign profit and how much targeting and changing contacts matter.

This is a synthetic decision experiment. It is not a demand forecast for IIT Bombay or an empirical claim about actual consumers. The seller's controllable decisions are price, sample quantity and sample recipients. The discussion-contact policy is a platform/environment scenario; a seller may not control it directly.

**Main finding:** in the assumed market, reducing free samples from twelve to three improves profit more clearly than choosing highly connected recipients instead of random recipients. A separate fresh-market check supports the sample-quantity result. A second, deliberately awkward finding shows how a strict opinion-distance cutoff can reverse the expected effect of product experience. This helps identify a limitation of the model before recommending its use.

## 2. System boundary and assumptions

We simulate 300 customers in three pre-existing social groups. They have 1,200 undirected discussion contacts, giving mean initial degree eight. The graph is generated with a preference for within-group ties. There is one product, one launch and at most one paid purchase per customer. A campaign lasts 60 abstract periods, each containing 300 randomly scheduled interaction attempts.

There is no inventory shortage, delivery queue, competing brand, return, repeat purchase or fixed operating overhead. Modeled profit is revenue less the production cost of sold and sampled bottles. It is a contribution measure rather than a full business profit-and-loss account.

| Item | Baseline assumption | Why it is included |
|---|---|---|
|Initial belief|Beta(2,2), range 0–1|Heterogeneous initial expected appeal|
|Value scale|Uniform ₹500–₹1,000|Converts an opinion into perceived rupee value|
|Affordability limit|Uniform ₹400–₹1,000|Separates ability to pay from perceived worth|
|Experience signal|Normal mean 0.8, SD 0.1, clipped to [0,1]|Ownership can reveal new personal information|
|Within-group pair preference|Six times cross-group pair acceptance|A simple synthetic clustered social setting|
|Awareness transmission|Probability 0.25 in an aware/unaware meeting|News need not spread every time|
|Confidence tolerance d|0.2|Similar opinions can influence each other|
|Compromise μ|0.3|Each opinion moves 30% toward the other's old value|
|Discordant-tie rewiring φ|0.05|Disagreement can change discussion contacts|
|Contact selection h|0 or 1|Random versus similar-opinion replacement|
|Selling prices|₹400, ₹500, ₹600|A small, interpretable decision grid|
|Cost per supplied bottle|₹250|Accounts for samples as well as sales|
|Free samples|12 initially; 3 in a later follow-up|Compare targeting at equal spending, then whether to spend less|

The attributes are independent in the baseline. None of these distributions or monetary values was fitted to observed customers. Their purpose is to define an understandable scenario; sensitivity analysis examines some consequences of choosing them.

## 3. Input data analysis

Every replication generates its own customer table and network. Replication 1000 is included as a readable example: `data/customers_rep1000.csv` and `contacts_rep1000.csv`.

| Exemplar attribute | Mean | Sample SD | Observed minimum–maximum |
|---|---:|---:|---|
|Initial belief|0.490|0.235|0.023–0.968|
|Value scale|₹770.12|₹144.19|₹501.99–₹998.18|
|Affordability|₹710.93|₹178.23|₹403.20–₹998.04|
|Experience signal|0.803|0.094|0.555–1.000|
|Initial degree|8.000|2.846|1–16|

This particular generated graph has 322 cross-group edges, or 26.83% of 1,200, and no isolates initially. Other generated markets can contain isolates. These statistics describe one scenario realization, not measured campus demographics. Exact values and reproducible calculations are in `sim/analysis/input_statistics.csv` and `initial_graph_statistics.csv`; field definitions are in `data/DATA_DICTIONARY.md`.

## 4. Agent states and event logic

Each AnyLogic **Consumer** references a distinct customer state: ID, group, budget, value scale, current belief, awareness, ownership and experience. Main schedules local interactions and records outcomes. A centrally scheduled collection of individual agents is still agent-based: sales are obtained by checking individual decisions, rather than from an aggregate growth equation.

Initially, only sampled customers know the launch. They own a free bottle, incur cost and set their belief to their personal experience signal. Sample owners never become paid buyers in this campaign.

For every interaction attempt, a uniformly selected customer chooses one current neighbor. If neither is aware, there is no product discussion. If exactly one is aware, transmission occurs with probability 0.25. Any aware customer can share news, including a nonbuyer; this is an explicit assumption.

Once both are aware, sufficiently close beliefs compromise:

`b_i(new) = b_i(old) + μ × [b_j(old) − b_i(old)]`, and symmetrically for j.

For example, beliefs 0.4 and 0.5 with μ=0.3 become 0.43 and 0.47. Both use the old values. At a difference of 0.2 or greater, averaging does not occur. Instead, with probability 0.05, the focal customer replaces the discussion tie. At h=0 the new contact is a uniform non-neighbor. At h=1 it is a sufficiently similar non-neighbor, with random fallback when none is available. Self-links and duplicate links are excluded. A candidate is chosen before deletion, and isolates are permitted. Replacing one edge with one conserves the edge count.

After 300 attempts, all informed nonowners decide simultaneously. A person buys if:

`affordability ≥ price` **and** `value scale × current belief ≥ price`.

For example, value scale ₹800 and belief 0.6 give perceived value ₹480. At price ₹500 that customer does not buy, even with enough money. This threshold is our assumption, not a fitted purchase-probability equation. Across repeated markets, the fraction buying is a simulation output.

New buyers then receive their personal experience signal. Opinions can change again in later conversations. Awareness and ownership are irreversible during the campaign; beliefs and contacts are not. Experience resets mean that population mean belief need not be conserved. Only an individual symmetric averaging event conserves its pair mean.

## 5. Relationship to the literature

**Established mechanisms:** Deffuant et al. introduced the pairwise bounded-confidence rule used as our opinion foundation. Kozma and Barrat studied a closely related adaptive opinion network; their fragmentation result is a replication target, not our discovery. Published product-diffusion and promotional models by Delre and coauthors already distinguish information and adoption and study seeding. Kempe, Kleinberg and Tardos formalize influence maximization and show why degree heuristics are not generally optimal.

**Our assumptions:** explicit rupee affordability/value thresholds, personal experience resets, awareness from any informed person, the particular graph and input distributions, the cost accounting and the finite campaign horizon. These are not claimed to be jointly validated by those papers.

**Our contribution to this course project:** a replication-informed extension joining adaptive opinions to a concrete product-launch decision, with separate awareness, paid sales and sample accounting; paired comparisons and fresh-market confirmation; and an ablation exposing a counterintuitive implication of the confidence assumption. We do not claim first use of social influence, homophilic rewiring or distributed product seeding. Research priority for this exact combination has not been established by an exhaustive search.

The product-specific [literature notes](LITERATURE_NOTES.md) give direct sources and a claim-verification table. The parent [literature review](../LITERATURE_NOTES.md) gives the detailed opinion-model readings, read-status limits and quantitative targets.

## 6. Experiment design and uncertainty

Before the main experiments, the initial design fixed 12 samples, three prices, three recipient rules and two h values: 18 policy cells. Random sampling chooses twelve people. Degree targeting chooses twelve with the most initial contacts, with seeded tie-breaking. Distributed targeting chooses four highly connected people in each known group. All have the same ₹3,000 initial sample expense.

A 30-market-per-cell pilot was kept separate from 100 main markets per cell. The pilot selected price ₹400, degree targeting and h=0. On the separate main markets it outperformed the original ₹500/random/h=0 comparison by ₹874.50 mean profit, with paired 95% interval [₹260.95, ₹1,471.50]. This comparison changes price and targeting together; it cannot attribute the improvement to targeting alone. See `pilot_selected_evaluation.json`.

A subsequent stress test suggested examining fewer samples. The exploratory follow-up adds all eighteen corresponding three-sample policies on the same main markets. The combined dataset contains **3,600 policy evaluations on 100 independent markets**, not 3,600 independent populations. This extends the original equal-spending question to a budget-ceiling question: a seller is allowed to spend less than ₹3,000. For three samples, the distributed policy chooses one person per group.

Four comparisons were then fixed and evaluated on **100 fresh markets, IDs 5000–5099**: the provisional ₹400/3-sample/degree/h=0 policy, its random-targeting control, its 12-sample control and the original ₹500/12-sample/random comparison. This cohort is for confirmation, not another search for a best policy.

Four separated random streams initialize graph, traits, sample selection and interactions. Every activation consumes six uniforms even when it is skipped. Policies share the same market and aligned primitive draws, allowing paired comparisons. Graphs can later diverge; variance reduction is not assumed automatically.

Intervals use 10,000 market-level percentile bootstrap resamples and fixed seed 20261103. They are pointwise 95% Monte Carlo intervals. They do not account for uncertainty about the realism of the model or guarantee simultaneous coverage of many comparisons. Customers and period rows are not treated as independent replications.

## 7. Price: hearing about a product is not buying it

These are 100-market main means for **12 degree-targeted samples, h=0**:

| Price | Paid buyers | Modeled profit |
|---:|---:|---:|
|₹400|147.33|₹19,099.50|
|₹500|84.85|₹18,212.50|
|₹600|32.21|₹8,273.50|

Almost all customers become aware by period 60, yet far fewer pay at the high price. Awareness alone would therefore be a misleading launch-success measure. The pattern follows the synthetic value/budget thresholds and the resulting opinion feedback. It is not an estimated real demand curve. Source: `sim/analysis/policy_summary.csv`.

Among all 36 main policy means, ₹400/3 samples/degree/h=0 is largest: 151.30 paid buyers, 299.99 aware and ₹21,945 mean profit; pointwise mean-profit interval [₹21,580.50, ₹22,294.50]. This is a selected finite-candidate result. It does not prove that degree targeting or this price is globally optimal. Source: `all_policy_summary.csv`.

## 8. Sample quantity: profit and total ownership tell different stories

At price ₹400, degree targeting and h=0, switching from twelve to three samples changes main mean profit by **+₹2,845.50**, paired interval [₹2,673, ₹3,013.50]. Paid sales increase by 3.97, but sample owners decrease by nine. Total owners therefore decrease by about five, even while paid sales and profit rise. Paid-adoption denominators also change from 288 to 297; report the counts and definitions together. Source: `budget_paired.csv`.

The accounting decomposes the profit gain exactly: ₹2,250 less sample expenditure plus ₹150 margin on 3.97 additional paid sales, or ₹595.50. This does not establish that all nine removed recipients would otherwise buy; the sales difference includes changed diffusion and experience paths.

The fresh-market confirmation gives **₹21,711** mean profit for the provisional three-sample degree policy, interval [₹21,405, ₹22,017]. Against its twelve-sample version, the paired gain is **₹2,854.50**, interval [₹2,698.50, ₹3,006]. Against random targeting with three samples, the gain is only **₹31.50**, interval [−₹112.50, ₹177]. Against the original ₹500/12-sample/random comparison, the gain is ₹4,108.50, interval [₹3,581.50, ₹4,623.50]; that changes several decisions together. Sources: `confirmation_summary.csv` and `confirmation_paired.csv`.

## 9. Targeting and contact policy: retain the negative findings

At ₹400 with three samples in the main cohort, degree targeting exceeds random targeting by ₹114, interval [−₹66.04, ₹289.50]. Its fresh-market estimate is smaller and also uncertain. Acquiring expensive network information cannot be justified by a claimed large degree-targeting advantage from these results.

The contact-policy effect is not uniformly zero. With twelve samples, eight of nine profit h contrasts include zero; the ₹600/degree case has a positive exploratory interval. With three samples at ₹400, similar-contact replacement reduces mean profit for degree targeting by ₹96, pointwise interval [−₹178.50, −₹15]. These are small conditional differences with a multiple-comparison limitation, rather than evidence for one universal recommendation rule. Source: `paired_contrasts.csv`, `final_paired_contrasts.csv`.

A focused network stress test increases within-group preference from six to sixty, keeping other baseline inputs. With twelve samples at ₹400/h=0, group-distributed targeting improves **period-7** profit over degree targeting by ₹393, interval [₹202.50, ₹585]. At period 60 the difference is −₹52.50, interval [−₹154.50, ₹49.50]. Early reach and late profit can tell different stories. This conditional timing benefit is not a newly discovered principle; prior seeding literature already examines network coverage. Source: `stress_paired.csv`.

## 10. What-if analysis and the quality diagnostic

Cost does not enter a customer's decision rule, so changing cost can be evaluated by re-accounting the same simulated paid counts. This is valid only while price and customer behavior are unchanged. Across the tested cells, the largest observed mean shifts from price ₹400 at unit costs ₹150/₹250 to ₹500 at ₹350 and ₹600 at ₹450. Three samples are used in each of those selected cells. At cost ₹450 the best observed mean is still positive, ₹3,420; the earlier twelve-sample-only result would wrongly suggest abandoning every tested launch. Source: `all_cost_revaluation.csv`. These are selected pointwise comparisons, and sample spending is recalculated at the changed cost rather than held at ₹750.

Separate behavioral checks vary sharing, confidence and experience means. Price ₹400 remains the largest observed mean among the three prices for the checked degree/12-sample/h=0 scenarios. That limited sensitivity grid is not universal robustness. Slower sharing leaves mean awareness near 271 rather than 300 at period 60. Source: `behavior_summary.csv`.

**Unexpected result:** increasing experience quality from 0.6 to 0.95 can reduce purchases under d=0.2. Rather than hiding it or tuning it away, we ran 1,200 diagnostic simulations crossing three quality values, two confidence widths and rewiring on/off on 100 paired markets.

On the **fixed graph** (φ=0), mean paid buyers fall from 168.74 at q=0.6 to 130.58 at q=0.95 when d=0.2. The paired difference is −38.16 buyers, interval [−39.84, −36.49]. With d=1, where all actual opinion differences in these runs are compatible, paid buyers instead rise from 174.76 to 280.96: +106.20, interval [104.41, 108.02]. The reversal therefore does not require rewiring. Sources: `quality_diagnostic_summary.csv`, `quality_paired.csv`.

A moderate belief of 0.5 accepts 0.6 but rejects 0.95 at tolerance 0.2. Initial sample-to-nonowner compatible-edge fractions fall from about 0.510 to 0.186 over those quality settings. The hard confidence gate can block very positive experience from influencing moderate nonowners. These diagnostics support a mechanism explanation inside this model; they do not show that actual consumers prefer worse products. The result is a reason to validate or soften the attention rule before practical deployment.

## 11. Verification, validation and animation

The 16-check product suite covers readable/native agreement, hand calculations, no-information cases, unaffordable prices, sample accounting and graph/customer invariants. A separate Java kernel passes its fixtures and produces 1,080 reference runs. For the 36 policy cells, independent Java/C++ mean-difference intervals include zero in all 36 profit comparisons, all 36 paid-sales comparisons and 34 of 36 awareness comparisons. These are distribution diagnostics, not an equivalence proof; small awareness discrepancies remain visible in `java_kernel_all36_comparison.csv`.

The first actual AnyLogic run, documented by the student-supplied Windows PLE screenshot, reaches the exact default Java values: 300 aware, 148 paid, 12 sampled and ₹19,200 profit. That establishes successful execution for that version/configuration. It does not establish that every batch policy or later graphical revision has run. The revised bodies additionally compile against the actual installed AnyLogic 8.9.10 Agent/shape libraries; its 180-case batch wiring matches Java outside the engine. The managed workspace could not connect the editor to the desktop, so that launch attempt was not used as engine evidence. The students subsequently supplied the revised animation screenshot and actual default CSVs: all summary fields match matching Java except cohort/runtime, and the trajectory has 61 period rows. Multi-policy engine execution is still separate and unobserved.

The revised animation shows individual customer agents, ownership colors, opinion mini-bars and the highlighted latest actual conversation in each ten-attempt visual tick. Before/after opinions explain whether averaging happened. A rewired new contact is distinguished from the original meeting. Group grids are a stable layout, not opinion plots. Period-end bars show awareness versus paid sales. The UI does not imply that every highlighted pair is the complete network.

The original opinion-model validation remains available in the parent report: the finite-N HK pattern was reproduced, while exact KB/binary-voter critical-point replication is partial. Those benchmarks do not validate the new financial/purchase assumptions. There is no empirical sales validation.

## 12. Conditional recommendation and limits

For the baseline synthetic setting and the finite choices examined, begin with **price ₹400 and three samples**. Degree targeting has the largest main mean, but the confirmatory targeting advantage is small and uncertain; if identifying high-degree customers costs money, random selection is a reasonable simpler alternative to investigate. Use distributed seeding when early group coverage matters and test the relevant network setting. Do not spend the entire sample budget simply because it is available.

Revisit price if unit cost changes. Treat similar-contact recommendations as a secondary scenario, not a guaranteed sales lever. Before applying this outside a course demonstration, obtain evidence for price/value distributions, sharing, experience response and the confidence rule, then include operating and targeting costs.

Only sample counts three and twelve were tested, and the zero-sample model has no initial launch awareness. We have not optimized every quantity, price, graph or intervention time. All-aware nonbuyers sharing news makes late saturation easier than in an owner-only diffusion model. Independence, a hard confidence boundary, irreversible purchases and the fixed campaign horizon are consequential assumptions. The project shows what a specified mechanism can do; it does not establish what a real market will do.

## 13. Submission and reproducibility

Submit the actual `.alp`, supporting scripts/CSVs, the editable PowerPoint deck and any real engine exports. Use the thirteen-minute presentation plan, including its live demonstration; prepare for seven minutes of questions. Group 9 is scheduled on 4 November, 14:00–15:40 IST, LC002. The students must check Moodle submission access and save the final files on the presentation computer.

Research, implementation, experiments and drafting were AI-assisted. The students must understand the individual decision rules, run the required model, check their course's disclosure requirements and be able to defend the results. `VIVA_PREP.md`, `MODEL_SPEC.md`, `VALIDATION_REPORT.md` and the root journal support that preparation.

## Presentation variant added after the approved model

At the students' request, a separate live-network model adds ownership-colored nodes and explicit opinion values, solid/dotted actual ties, recent-interaction highlights, awareness/sales histories and customer-state diagnostics. It uses the same kernel and exports the same summaries plus a separate17-column network-metrics CSV. API/wiring checks pass; actual engine execution of this optional version is pending. The approved grid `.alp` remains the tested fallback. See LIVE_NETWORK.md.
