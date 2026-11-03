# Verification and validation: product-launch application

**Scope:** synthetic mechanism and decision study. The numerical experiments here were executed with a readable Python specification, an accelerated C++ implementation and a separate Java kernel. The revised AnyLogic default has been run by the students and its actual export inspected. The multi-policy engine batch is still pending. Successful software checks do not establish empirical accuracy.

## Evidence table

| Check | Status | Evidence and limit |
|---|---|---|
|Readable reference versus accelerated implementation|PASS|Five small seeded cases match final states exactly and period metrics to 10⁻¹²; `sim/verification.csv`|
|Limiting cases and hand calculation|PASS|Zero awareness gives zero sales even at zero price; zero sharing leaves only sample owners; unaffordable prices give no sales; all-aware zero price separates paid owners and samples; exact two-person averaging and forced rewiring fixtures|
|Run invariants|PASS in executed designs|Simple undirected graph, fixed edges, bounded beliefs, no purchase before awareness, no repeated purchase, no sample counted as sale, affordability/value at purchase, monotone awareness/ownership and accounting asserted by the accelerator wrapper|
|Full product verification suite|PASS, 16/16|`sim/verification_summary.json`; this is a count of the implemented checks, not a measure of empirical validity|
|Separate Java implementation|PASS for its fixtures|Pair averaging, zero sharing and sample accounting; `anylogic/KernelCheck.java`|
|Java versus accelerated distribution check|DIAGNOSTIC|30 Java markets per cell versus 100 NumPy/C++ markets per cell, all 36 policies. `java_kernel_all36_comparison.csv` records independent-bootstrap differences. Inclusion of zero is not proof of equivalence; these generators do not produce identical markets|
|Main/Consumer wiring and export outside AnyLogic|PASS for stand-ins|`sim/verify_wrapper.py` compiles the actual additional-class bodies with simple stand-ins and checks state references, completion and exact Java summary fields. Stand-ins cannot verify AnyLogic API behavior or XML import|
|Generated `.alp` structure|PASS for XML checks|Two agent types, population 300, four parameters, event action, unique IDs and embedded source consistency checked by `build_alp.py`; no claim of engine compatibility from XML alone|
|AnyLogic 8.9 PLE import/compile/run/animation/export|PENDING|One default engine run requested. Expected matching Java realization: 300 aware, 148 paid, 12 samples, ₹19,200 profit. Record actual version, outcomes and output files after execution|
|Awareness/paid-sales distinction|PASS|Separate flags, free-sample expenditure and no sample revenue. Run-level identities rechecked by analysis ingestion|
|Random-stream alignment|PASS by construction/checks|Four separate stream families; six event draws per attempted activation including skipped encounters. Policies share primitive draws; realized interactions can differ|
|Pilot/main separation|PASS|Pilot IDs 0–29, main IDs 1000–1099. Follow-up three-sample variants reuse main IDs deliberately; they do not add independent markets|
|Confirmation of exploratory extension|SEE CSV|Four fixed policies on IDs 5000–5099, separate from selection markets; `confirmation_manifest.json`, `confirmation_summary.csv`, `confirmation_paired.csv`|
|Sensitivity and awkward results|REPORTED|Network separation, sample count, sharing, tolerance, experience and cost are examined. Counterintuitive quality effects remain in raw data and the report|
|Literature mechanism checks|PARTIAL / PASS by check|See the parent `../VALIDATION_REPORT.md`: HK finite-N pattern reproduced; KB and binary-voter critical values only partially reproduced. Those tests concern the original mechanisms, not the new purchase rule|
|Empirical validation|NOT DONE|No real behavioral data, demand calibration or out-of-sample real sales. All recommendations are conditional on the synthetic assumptions|

## Independent implementations and what they establish

The readable Python model specifies the rules. The accelerator receives the same initialized market and random state, so it can be checked for exact small-case agreement. The Java kernel follows the same rules but uses `java.util.Random`. It is embedded in Main to make the AnyLogic project self-contained. Comparing Java and C++ distributions can reveal discrepancies; a small nonsignificant difference cannot prove that none exists.

The stand-in Main test checks our Java wiring logic and export identities. It does not execute AnyLogic's event scheduler, agent population, graphical objects or serialization loader. Actual engine testing is a separate necessary step. No file produced by the stand-in harness is presented as an AnyLogic observation.

## Time, censoring and financial identities

The campaign intentionally ends after 60 periods. This is a planning horizon, not a claim of equilibrium. Target attainment is recorded with an event flag and `t20=-1` when unreached. Reporting a capped descriptive time of 60 does not convert an unobserved event into an observed one.

For the default Java realization: price ₹400, 148 paid buyers, 12 samples and cost ₹250 per unit imply revenue ₹59,200, total cost ₹40,000 and profit ₹19,200. Samples are an expense and an ownership state, never paid sales. This hand calculation can be checked on the live display.

The original opinion process conserved mean opinion during all its dynamics. The application introduces experience resets, so the whole-campaign mean is not conserved. Only a symmetric compromise event conserves the pair mean. Reusing the original global invariant or its freezing predicate would be an error.

## Statistical interpretation

Each policy cell has repeated independent markets. Policies evaluated on the same market are paired. Intervals use 10,000 bootstrap resamples with seed 20261103; whole markets, not customer rows or period rows, are resampled. The intervals are pointwise 95% Monte Carlo intervals under the assumed model. They do not include uncertainty about whether the assumptions represent reality. Many comparisons were examined, so isolated positive intervals are exploratory unless separately confirmed.

The original 12-sample pilot selected price ₹400, degree targeting and h=0 before main evaluation. The three-sample extension was motivated by the later stress results. It is explicitly labeled exploratory; the fresh confirmation design checks four fixed contrasts without searching its results for another winner.

## Evidence still needed from the students

The revised screenshot and actual default CSV files are saved. Preserve the AnyLogic-converted `.alp` as well. Record the installed version and the successful run configuration. If the default result differs from its matching Java realization, resolve the discrepancy before showing a claimed match. If engine execution remains unavailable, say so clearly in the presentation and use precomputed reference data only as reference data.

## Separate live-network presentation checks

`CampusProductLaunch_LiveNetwork.alp` preserves the original customer kernel and summaries. It compiles against actual installed AnyLogic8.9.10 APIs. A separate stand-in wiring test matches the animated default and180 batch summaries to the existing Java references. It checks1,200 displayed actual ties,300 state references and61 extra metric rows per campaign, with exact histogram/tie/reason partitions. Actual engine execution of that optional variant is still pending; the approved grid model is preserved byte-for-byte.

The primary16-slide PowerPoint is independently parsed and schema-validated with Apache POI5.4.1/XmlBeans5.3.0, and its Java2D previews were inspected. Its scientific plots are rendered by JFreeChart/JFreeSVG from the exact supplied bootstrap endpoints. A separate native-chart deck is provided; its complete schema validation was unavailable because the installed lite schema omits a chart type. No Windows PowerPoint execution is claimed here.
