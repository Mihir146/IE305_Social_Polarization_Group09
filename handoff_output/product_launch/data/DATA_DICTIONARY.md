# Synthetic inputs and simulation outputs

No field is measured from actual campus residents. The synthetic population is a scenario, not an estimate of IIT Bombay customers. Rupee values provide a concrete decision scale; periods are abstract campaign periods.

## Input fields

| Field | Distribution or construction | Purpose |
|---|---|---|
|Customer ID|0–299|Stable identity|
|Group|ID modulo 3|Three pre-campaign groups of 100|
|Initial belief|Median of three independent Uniform(0,1) draws, equivalent to Beta(2,2)|Initial expected appeal, range 0–1|
|Value scale|Uniform ₹500–₹1,000|Multiplied by current belief to obtain perceived rupee value|
|Affordability limit|Uniform ₹400–₹1,000|Independent hard purchasing-budget constraint|
|Experience signal|Normal(mean q, SD 0.1), clipped to [0,1]|Pre-drawn personal assessment revealed on ownership|
|Initial contact edge|Weighted pair sampling until 1,200 simple undirected edges|Within-group acceptance 1; cross-group acceptance 1/6|
|Sample recipient|Policy-selected before the campaign|Becomes aware and owns a free product at period 0|

The exemplar replication 1000 is saved in this folder. `sim/analysis/input_statistics.csv` gives its actual sample moments, and `initial_graph_statistics.csv` gives graph statistics. Those moments summarize one generated market; they are not fitted population parameters. The generator, not this one CSV, produces new independent markets.

## Run-summary fields

`sim/results/main_runs.csv` and `budget3_runs.csv` use the same 49-column schema as the AnyLogic summary exports.

| Fields | Meaning |
|---|---|
|cohort, scenario|Which experiment and assumption set generated the row|
|rep|Independent market replication ID within a generator; repeated across policies intentionally|
|graph_seed, trait_seed, selection_seed, event_seed|Four logged random-stream seeds|
|strategy|random, degree or distributed|
|N, k0, groups, within_weight|Population, initial mean degree, known groups and initial within-group preference|
|periods, n_samples, price, unit_cost|Campaign horizon, giveaway count, selling price and cost per unit|
|d, mu, phi, h|Confidence tolerance, compromise fraction, discordant-tie replacement chance, similar-contact branch probability|
|share_prob, quality, experience_sd|Awareness-transmission chance, experience mean and untruncated SD|
|aware|Customers informed by the end, including all owners|
|paid_buyers, free_samples, new_paid|Paid owners, sampled owners and paid purchases during the final period|
|revenue, total_cost, profit|Price × paid; cost × all supplied units; revenue minus cost|
|paid_adoption|Paid buyers / (N − free samples), rather than owners / N|
|min_group_adoption|Minimum over groups of paid buyers / non-sampled customers in that group|
|giant_frac|Largest connected component of the current discussion graph / N|
|cross_group_frac|Edges joining different known initial groups / total edges; not opinion polarization|
|rewires|Cumulative successful edge replacements|
|belief_mean, belief_variance|Population mean and population variance at the end|
|paid_group0/1/2, aware_group0/1/2|Group counts; sum to their population totals|
|degree_zero, total_edges|Isolate count and edge count; edges must remain 1,200|
|t20, hit20|First period paid adoption reaches 0.2; t20 = −1 when unreached, hit20 = 0|
|restricted_t20|t20 if reached, otherwise 60; a capped descriptive measure, not an imputed true event time|
|secs|Wall-clock runtime; not a campaign outcome and not expected to reproduce exactly|

## Repeated observations and uncertainty

Trajectory CSVs contain period 0 through period 60, one row per policy, market and period. The same market appears in multiple policies and periods. Bootstrap intervals resample whole markets; the period rows and 300 customers are not independent replications.

The ledger records realized purchase decisions and pre-purchase eligibility. Conditional-conversion tables condition on initial-belief band and affordability. They describe this model's simulated conditional rates, not a fitted causal effect in actual consumers.

The default AnyLogic run writes one summary file and 61 period rows. The console supplies the absolute output path. Re-running the same policy and replication intentionally replaces the same named export; it does not create additional independent evidence.
