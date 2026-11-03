# Product launch: model specification fixed before the main experiments

**Build started 3 November 2026,12:05 UTC. Four-hour delivery target:16:05 UTC.**

Application: a hypothetical campus social-commerce platform launches one reusable bottle. All customer attributes, prices, costs and behavior are synthetic assumptions. We study a decision under those assumptions, not a forecast for actual customers.

## Decision and experiment

Choose a launch price and recipients of a fixed free-sample budget. Compare random versus similarity-based replacement of product-discussion contacts as a platform policy/environment factor.

- Prices:₹400,₹500,₹600. Unit cost:₹250 for both paid units and samples.
- Exactly12 free samples, total sampling cost₹3000, in every policy.
- Seed rules: random12;12 highest-degree customers;4 highest-degree customers in each of three known social groups.
- Reconnection h=0 or1. This gives18 policy cells. No strategy is called mathematically optimal outside this finite candidate set.
- Campaign horizon:60 simulation periods. One period contains300 random interaction attempts, not a calibrated calendar day.
- Pilot30 replications/cell; separate main evaluation100 replications/cell. Do not pool pilot and main cohorts.

## Synthetic population

300 customers, three equal groups (e.g., campus residential communities). Initial graph:1200 distinct undirected edges. Uniformly propose unordered pairs and accept within-group pairs with probability1, between-group pairs with probability1/6, until the edge budget is filled. This is a weighted fixed-edge graph, not an ER graph or a guaranteed connected graph.

Each customer has:

| Attribute | Initialization / meaning |
|---|---|
|Group|Known pre-campaign membership; equal sizes|
|Initial belief b∈[0,1]|Median of three uniforms, exactly Beta(2,2); expected appeal/quality of the product category/offer|
|Value scale v|Uniform₹500–₹1000; perceived value is v×b|
|Affordability limit B|Uniform₹400–₹1000; a separate ability-to-pay constraint|
|Personal experience signal e|clip(Normal(q,.1),0,1), q=.8 in the main scenario; pre-drawn for every customer|
|Awareness|Initially false, except sample recipients. Awareness means receiving launch information, not merely knowing what a bottle is|
|Free sample / paid purchase|Separate flags; a sampled customer never generates a paid sale|

Signals, budgets, values and priors are independent in the baseline. This is an assumption to disclose, not empirical estimation. Highest degree confers more contact opportunities, not stronger persuasion. Group-distributed seeding uses pre-campaign groups and degree, not future outcomes.

## Initialization and random streams

For replication r, separate graph, attribute, selection and event streams use seeds1000000+r,2000000+r,3000000+r,4000000+r. All18 policies within a replication share the same market and event randomness. Tie-breaking for degree uses a seeded random priority. Sample recipients become aware and set belief to their own pre-drawn experience signal at period0.

Six uniform event draws are consumed on **every activation**, including skipped activations: focal customer, neighbor rank, awareness transmission, rewiring attempt, similar/random branch, partner rank. This keeps random-input alignment across policies. Their evolving neighbor lists can still differ, so shared randomness does not imply identical interactions or guarantee variance reduction.

## One interaction and one purchase opportunity

1. Choose a uniform customer i and a uniform current neighbor j. Skip an isolate.
2. If neither knows the launch, skip product discussion. If exactly one is aware, the other becomes aware with probability s=.25. If transmission fails, skip further product actions in this encounter.
3. Once both are aware, compare their beliefs. If |bi−bj|<d=.2, both move μ=.3 toward the other's old belief. Otherwise, with probability φ=.05, i attempts to replace j. With probability h choose uniformly among non-neighbors within d of i; otherwise choose among all non-neighbors. An empty similar set falls back to all non-neighbors. Exclude self and existing neighbors; choose before deleting. Isolates are allowed and edge count stays fixed.
4. After all N interaction attempts in a period, identify **all** aware non-owners with B≥price and v×b≥price. They buy simultaneously, once only. Record their pre-purchase perceived value and purchase period. Then each new buyer sets belief to the pre-drawn personal experience signal. Further discussions can change it.

Affordability and perceived value are both required. This threshold rule is a modeling assumption. The purchase probability across Monte Carlo markets is an output; we do not invent a fitted logistic coefficient. There is no recurring purchase coin that eventually forces every customer to buy.

Experiences introduce external information, so mean belief and variance need not be conserved across the entire launch. The old pairwise mean/variance identities still apply **within a compromise event**. Product purchases are irreversible during the campaign, while beliefs and discussion links can change.

## Accounting and outcomes

Paid buyers exclude free recipients. Revenue=price×paid buyers. Total modeled cost=unit cost×(paid buyers+12 samples). Profit=(price−unit cost)×paid buyers−12×unit cost. No fixed overhead, inventory limits, shipping, repeat purchases or competitor are modeled.

Primary outcomes: profit, paid sales, awareness and adoption over time. Secondary outcomes: minimum group paid-adoption rate, group sales, contact fragmentation and time to20% paid adoption among non-sampled customers. If the sales target is not reached by60 periods, record the target as unreached; do not call60 its true attainment time.

Use a fixed campaign horizon. Do not reuse the original opinion-only freezing predicate: awareness and new experience can remain active after pair opinions appear settled.

## Verification and interpretation

Check no purchase before awareness, no double purchase, no sample counted as sale, affordability/value at purchase, edge conservation, valid beliefs, exactly12 samples, and accounting identities. Test zero samples/awareness, zero sharing, unaffordable prices, zero-price all-aware cases and deterministic pair/rewiring fixtures. Quantitative literature checks remain separately identified; matching the original opinion model does not validate the added purchase rules.

The studied seeding idea has direct prior work in influence maximization and promotional diffusion. Our contribution is a transparent simulation decision comparison with price, affordability, experience and adaptive discussion. Results may be negative. No result is claimed before its CSV exists.

## Follow-ups and presentation variants (added after the original design)

The specification above records the original18-cell,12-sample design fixed before the main runs. A later exploratory extension adds three samples across the same18 combinations, creating36 candidate cells on the same100 main markets. Three-sample distributed targeting selects one person per known group. Accounting generalizes to `profit=(price−unit_cost)×paid−unit_cost×n_samples`. This is a budget-ceiling extension: sample spending may be below the original Rs3,000. It was not preregistered as part of the original design.

After inspecting that extension, four policies were fixed before a separate100-market confirmation (rep5000–5099): Rs400/3/degree/h0, Rs400/3/random/h0, Rs400/12/degree/h0 and Rs500/12/random/h0. This cohort is not searched for a new winner. Source: `sim/run_confirmation.py`, its manifest and paired CSV.

The quality diagnostic is also exploratory. It crosses q=.6,.8,.95 with d=.2 or1 and phi=0 or.05 at Rs400/12/degree/h0. It was motivated by an unexpected sensitivity result. The behavior was not tuned to remove the reversal.

The approved grid file and separate live-network file use the same customer kernel and primitive event draw order. Animated runs execute ten attempts per visual tick; unanimated batch runs execute a whole period per tick. Buying remains at each300-attempt period boundary. Display colors, spatial layout and plot updates consume no model randomness.

The live-network extension exports a separate61-row `network_metrics` CSV. A compatible edge has endpoint belief difference strictly below d, irrespective of whether both endpoints are informed; actual influence still requires awareness. Ten belief bins cover [0,.1),…,[.9,1]. Aware nonowners are partitioned first by insufficient budget, then insufficient perceived value among those who can afford, then eligible to buy. At completed period ends that last count is zero because eligible people have just bought. Mid-period it can be positive. The quantities are descriptive customer states, not fitted real-world probabilities.

The visible network draws all1,200 ties. In the simplified network presentation, black shows a selected recent actual meeting; blue briefly persists for a recently created tie. Neither highlighting nor line thickness adds a new influence weight. Node positions show known social groups and have no physical-distance or opinion-axis interpretation.

The parameter q is the mean of the underlying normal experience draw **before clipping**. Near the boundaries, the clipped experience distribution has a different actual mean and variance. Plots label q as an experience parameter rather than an observed customer average.

Similarity-based reconnection assumes access to every customer's current modeled belief, including the category/offer priors of currently unaware candidates. This is an ideal-information policy scenario. We do not model estimating those beliefs from ratings, observation errors or the cost of collecting network/preferences data. It is not presented as a deployable recommendation algorithm.
