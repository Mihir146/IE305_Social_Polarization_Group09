# Final presentation handoff plan — selected product application

The original five-hour mechanism plan is retained below as historical background. The selected four-hour product build began at12:05 UTC on3 November. The model, synthetic experiments, report, viva and editable deck now exist; the approved revised default has actual AnyLogic evidence.

1. Save/pull the exact approved `product_launch/CampusProductLaunch.alp` and actual engine exports. Avoid feature changes before presentation.
2. Open `product_launch/Campus_Product_Launch.pptx` once on the presenting computer and check its native charts/layout. The12 main slides budget735 seconds, including90 seconds for the live model; four extra slides are Q&A backups.
3. If feasible, collect the already prepared automatic180-campaign engine batch with policyIndex36, animateNetwork=false and virtual time. This adds actual policy evidence; do not relabel reference runs or duplicate reruns as engine replications.
4. Read the one-page explanation and25 answers in `product_launch/VIVA_PREP.md`. Both students must explain one conversation, one buying decision, sample accounting and one uncertain result.
5. Rehearse: Mihir slides1–6; Vaibhav slides7–12 including the live model. Bring the local screenshot/CSV fallback and identify it honestly if the live run fails.
6. Submit the actual model, supporting data/analysis and slides through Moodle; check the announced deadline/access. Group9 presents4 November14:00–15:40 IST in LC002 and must attend the whole slot.

The main recommendation is conditional: Rs400 and three samples among the tested baseline choices, with no established large premium for degree targeting. Keep the quality-cutoff warning, synthetic-data status and pointwise-interval limits visible.

---

# Five-hour execution plan — revised 3 November 2026

**Mihir Vasave and Vaibhav Mathur, IE305 Simulation Lab.** The research/reference analysis is prepared. The highest-priority remaining work is to execute and verify the required AnyLogic model.

## 0. Start here

Read `VALIDATION_REPORT.md`, then the model loop and invariants in `polarization_project_blueprint.md` §3. Use the **updated** documents in this folder. The original supplied figures and summary describe3000-sweep measurements; their old threshold captions must not drive the presentation.

The selected final application is now implemented in `product_launch/`. The contact-policy study below is background. Use the product report, PowerPoint and timed speaker notes for the final presentation.

The interesting story is now: **“A network that looks protected may simply not have fragmented yet.”** Pair that with the mathematical observation that opinion variance falls while the graph can break apart. These make a clear, defensible presentation. They are course-project contributions in replication and analysis; the mechanism itself is published work.

The original opinion-only port remains separate. The selected product default has an actual successful AnyLogic screenshot and inspected export matching Java; the large reference grid must still not be called AnyLogic output.

## 1. Findings the evidence supports

| ID | Finding | Evidence and qualification |
|---|---|---|
| F1 | Opinion groups and graph components are distinct | Replicates KB. Multiple opinion peaks can coexist with a large connected component; adaptive separation aligns groups and components in suitable states. K=1 and S≥.9 are operational proxies, not literal universal agreement/connectivity |
| F2 | Tolerance is a strong determinant of opinion-group counts | Primary A grid. “Rewiring never changes opinion counts” is too strong; the major/minor distinction and near-consensus cells matter |
| F3 | The apparent rewiring threshold is strongly horizon-dependent at d=.2 | At φ=.005,k0=8: mean S changes .999→.576 from3000 to30000 sweeps; k0=16:1.000→.568. The earlier long-run H4 interpretation is not supported |
| F4 | H3 was not supported | All six h=1 minus h=0 paired S intervals include zero in the examined B cells. This is not an equivalence test. Contact-selection speed effects depend on the cell and isolate rule |
| F5 | High tolerance weakens fragmentation in the tested grid | Primary A,d=.4: no fragmented observations in each30-run cell. A zero observed proportion is not a known zero probability |
| F6 | Initial opinion distribution matters | In the legacy3000-sweep grid the centered Beta(2,2) sensitivity has mean S≈.95,K≈1.17 versus baseline S≈.59,K≈2. These are synthetic scenario results, not a Flache theorem about our model |
| F7 | The isolate assumption changes the meaning of convergence | Of707 originally capped rows,522 still fail the criterion at30000;39 are blocked at the numerical tolerance, and520 have every remaining discordant edge touching a currently unmatched agent. These counts overlap. All1170 isolate-allowed B/D checks and all2790 primary grid runs freeze numerically within cap |

Sources: `sim/primary_horizon_summary.csv`, `primary_h3_paired.csv`, `validation_summary.json`, `isolate_sensitivity.csv`, `results.csv`, and the detailed report. Every literature attribution has a source location in `LITERATURE_NOTES.md`.

A useful speech line: “Our preferred contact-selection hypothesis failed, and longer runs changed another conclusion. Those checks tell us which claims the model can actually support.”

## 2. Timeline and division of work

Mihir owns the AnyLogic model. Vaibhav owns exported-data checks and the report. Both should be able to explain every equation and result.

| Time from start | Mihir | Vaibhav | Required output |
|---|---|---|---|
|0:00–0:25|Read the model loop and run through the .20/.30 compromise example together|Explain K,S,censoring and the revised F3/F4 together|Both can explain one activation and why a cap matters|
|0:25–1:10|Create Main/Person/people; paste Java bodies; attach startup and sweep actions|Check parameter names, CSV schema and private replication seed; read API audit|Tiny model compiles in actual AnyLogic|
|1:10–1:45|Execute pair/triangle/bridge fixtures with Vaibhav; repair exact reported errors|Record expected/actual values, version and pass/fail; check one CSV|Deterministic V&V evidence|
|1:45–2:30|Run reduced A batch in virtual/fastest time with animation off|Merge CSV; run analysis and implementation comparison; inspect seeds and interval widths|Actual AnyLogic CSV and comparison table|
|2:30–3:15|Run the small D horizon check; add B only if time permits|Check cap/rule separation; incorporate actual AnyLogic evidence into the report|One direct implementation check of the main finding|
|3:15–4:00|Save `.alp` and two comparable screenshots|Finalize report/slides using source tables and revised findings|Reviewable presentation package|
|4:00–4:40|Viva rehearsal; swap questioner/presenter roles|Use `VIVA_PREP.md`, especially the hard questions|Both can defend limitations without reading paragraphs|
|4:40–5:00|Open the saved model again and check the intended demonstration|Check citations, counts, captions and remaining pending statements|Final model/data/report/slides package|

At the90-minute mark, prioritize a correctly running tiny model and deterministic metrics. Reduce optional runs and slide polish if necessary. At the three-hour mark, a verified smaller AnyLogic experiment is preferable to claiming an unexecuted large batch. Report the actual run count.

**Do not let simulated seconds become wall-clock waiting.** Parameter Variation runs fast by design; for manual Simulation runs use virtual time/maximum speed. The .1-second event interval is only the engine-time representation of a sweep.

## 3. Minimal AnyLogic experiments

`AnyLogic_port.md` gives exact freeform expressions.

- **A:** d=.1,.2,.3 × φ=0,.05,.25;10 replications;h=1,N=300,k0=8,μ=.3,cap30000:90 runs.
- **D:** k0=8,16 × cap3000,30000;φ=.005,d=.2;five replications:20 runs.
- **Optional B:** d=.15,φ=.25,h=0,1;10 replications:20 runs. Use matching reference B cells.

**Use allowIsolates=true and cap30000 for the recommended main model**, comparing against `results_primary.csv`. D also has a matching cap3000 reference. The original protected-isolate data remain a separate legacy sensitivity; do not mix them with primary outputs. The exported cap and rule fields must identify the variant.

If Parameter Variation is unavailable in the installed edition, perform a smaller number of manual Simulation runs. Custom experiments are not a PLE fallback. Never repeat a fixed rep value and count the resulting duplicate as a new independent replication.

Cut scope in this order: optional B; additional screenshots; number of replications; overlay-figure polish. Preserve the actual AnyLogic execution, deterministic checks, saved CSV and rehearsal. Do not add noise, repulsion, real-data collection or new network topologies in this session.

## 4. Report and slide structure

The supplied blueprint, validation report, literature notes and viva preparation contain the substantive material. A compact report can follow:

1. Question and separate definitions of opinion groups/network fragmentation.
2. Direct prior work and modest replication/extension claim.
3. Exact homogeneous model, synthetic inputs, timing, isolate switch and stopping rule.
4. Verification identities and published-model checks, with discrepancies.
5. Original experiment design and the reason for the follow-up horizon audit.
6. F3 horizon table/figure, F4 negative result, isolate/KPI sensitivity.
7. Actual AnyLogic implementation evidence and comparison, once executed.
8. Limitations, finite-horizon design interpretation, references and provenance.

An eight-slide presentation can use these messages:

| Slide | Message | Visual/evidence |
|---|---|---|
|1|Can local agreement leave society disconnected?|Research question and one opinion/network sketch|
|2|Published mechanisms give us a testable model|One activation loop; name KB and Deffuant|
|3|We measure groups and paths separately|Triangle/bridge fixture with K,S,cross edges|
|4|The reference reproduces established patterns|Short V&V table, including partial/pending checks|
|5|Our apparent threshold moved when we waited|3000/30000-sweep comparison with intervals|
|6|Our contact-selection hypothesis was not supported|Paired h contrast and its interval; explain non-equivalence|
|7|Assumptions can keep a run active indefinitely|Isolate-rule diagnosis and controlled comparison|
|8|A reliable conclusion includes its observation horizon|Main finding, limits, actual AnyLogic evidence|

The variance identity can be explained on slide3 or in backup: averaging lowers total variance, so emerging separated peaks must not be described as increasing spread. Avoid presenting a high Q as proof of antagonism.

## 5. Evidence that matters for assessment

- A runnable saved AnyLogic model with clear state, stochastic events and outputs.
- An exact conceptual model that matches code; synthetic assumptions identified.
- Deterministic verification plus behavioral/quantitative literature checks.
- Appropriate replication, seed handling, intervals and censoring analysis.
- A controlled follow-up that corrects an earlier interpretation.
- A clearly reported failed hypothesis and important model limitations.
- Figures whose captions identify horizon, rule variant and sample size.
- Students who can explain the mechanism, checks and uncertainty aloud.

These support a strong submission; a grade depends on the actual course rubric and completed work.

## 6. Useful debugging prompts

**Compile error:** “AnyLogic[version] reports[exact error]. Here are the surrounding lines and the Main parameter/population names. Give the smallest fix consistent with this model.”

**Comparison issue:** “For this matching rule/horizon, AnyLogic gives[this mean and sample size] and the reference gives[these]. Compute the interval for their difference and distinguish low power from equivalence.”

**Rehearsal:** “Ask one question from VIVA_PREP at a time. After my answer, identify the missing reasoning before proceeding.”

**Report update:** “Replace only the pending AnyLogic section using these actual exported files and checks. Preserve the negative results and unresolved discrepancies.”

## 7. Files to use

| File | Purpose |
|---|---|
|`AnyLogic_port.md` and `anylogic/`|Build instructions, Java bodies, API audit and fixtures|
|`VALIDATION_REPORT.md`|What passed, partially matched and remains pending|
|`LITERATURE_NOTES.md`|Actual readings, exact mechanisms, targets, corrections and claim inventory|
|`sim/`|Original outputs, new raw checks, summaries and analysis scripts|
|`results_explorer.html`|Interactive validation/horizon charts; source tables remain readable offline|
|`VIVA_PREP.md`|One-page explanation,25 questions and glossary|
|`OPEN_ISSUES.md`|Remaining work ranked by importance|

The original supplied package is preserved outside this output folder. Old narrative claims must be checked against these revised documents before presentation.
