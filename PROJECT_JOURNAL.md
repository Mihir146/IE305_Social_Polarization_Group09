# IE305 product-launch project — progress, understanding and lessons

**Team:** Mihir Vasave and Vaibhav Mathur  
**Current direction:** launching one reusable bottle in a synthetic campus market  
**Four-hour build started:**3 November2026,12:05 UTC /17:35 IST  
**Delivery target:**16:05 UTC /21:35 IST  
**Status:** specification written; implementation and new sales experiments in progress. Actual AnyLogic execution is still required on the students' computer.

This is the main living record. A checkbox means evidence exists, not merely that the task is planned. New findings and failed checks belong here as well as successful results.

## 1. What are we trying to decide?

A hypothetical campus platform launches a new reusable bottle. It can choose a price and distribute12 free samples. We compare:

1. Random recipients.
2. Customers with the most discussion contacts.
3. Recipients spread across three social groups, selecting the most connected within each group.

We also compare random versus similar-opinion contact recommendations. The business question is **which of these launch policies produces the most modeled profit, and how reliably?** We will also check whether the policy with the most buyers is the one with the most profit.

Everything is synthetic. We are not collecting student data or predicting actual campus sales. The model lets us compare decisions under explicit assumptions.

## 2. How the model works, without jargon

There are300 customers in three groups. They have1200 mutual discussion links altogether. Each has an initial belief about the product's appeal, a maximum value scale and an affordability limit. All of these are generated from stated distributions.

Free-sample recipients know about the launch and receive a simulated product experience. Conversations can spread awareness. When two informed customers have sufficiently similar beliefs, they move a little toward one another. If they disagree strongly, a discussion connection may be replaced. The platform may recommend someone similar or a random new contact.

At the end of a simulation period, an informed customer buys if they can afford the price and their perceived value is at least the price. A customer buys at most once. A free sample is not a paid sale. Buying supplies a personal experience signal that can change later discussions.

One period contains300 random interaction attempts. It is not a measured calendar day. We observe a60-period campaign.

The illustrative price choices are₹400,₹500 and₹600. Unit cost is₹250. Twelve samples cost₹3000. These are fictional scenario inputs. Profit is:

`(price − unit cost) × paid buyers − sample count × unit cost`.

Example for understanding only: at price₹500,100 paid buyers and12 samples would give₹22000 modeled profit. This is arithmetic, **not an experiment result**.

The exact rules are in [MODEL_SPEC.md](handoff_output/product_launch/MODEL_SPEC.md).

## 3. Progress and evidence

| Work item | Current state | Evidence |
|---|---|---|
|Read the original assignment and supplied model|Done|Original files preserved in `handoff/`|
|Review the opinion/network literature|Substantial full-text review completed; extraction gaps remain explicit|`handoff_output/LITERATURE_NOTES.md` and `sources/READING_LOG.md`|
|Verify the supplied opinion results|Done|All2790 saved rows reproduced; `sim/replay_validation.csv`|
|Check longer horizons and isolate rule|Done for the opinion foundation|`VALIDATION_REPORT.md`, `sim/stall_audit.csv`, `sim/results_primary.csv`|
|Build a concrete contact-recommendation case study|Done in the reference|180 realizations,900 repeated snapshots; `sim/application_summary.csv`|
|Select product launch as the final domain|Done; user selected it|Conversation decision,3 November2026|
|Write exact product rules before examining sales results|Done|`product_launch/MODEL_SPEC.md`|
|Read the marketing sources supporting the added rules|In progress|Delre2007 model section confirms separate awareness/adoption and prior group-targeting work; full-source notes being completed|
|Implement the purchase/awareness/experience model|Readable reference and accelerated engine written; first tiny run succeeds|`product_launch/sim/model.py`, `engine.py`, `native.cpp`; full verification next|
|Verify product rules and accounting|16 checks passed, including exact native/reference states and analytical limits|`product_launch/sim/verification.csv`; actual AnyLogic execution remains pending|
|Run pilot and independent main experiment|Done:540 pilot and1800 main runs; disjoint replication cohorts|`product_launch/sim/results/`;100 main markets per policy|
|Run focused sensitivity checks|Done:2400 targeting-stress and2100 behavioral-sensitivity runs; analysis available|`analysis/stress_summary.csv`, `behavior_summary.csv`, `stress_paired.csv`|
|Prepare the product AnyLogic port and export contract|Generated .alp and paste-ready source ready for one engine check|`CampusProductLaunch.alp`, `ANYLOGIC_BUILD.md`; wrapper/Java checks pass; actual engine pending|
|Finish product report, presentation and viva notes|Pending|Will use new sales CSVs, not relabeled opinion outcomes|

## 4. Issues, lessons and fixes

| Issue or question | What we learned | Fix / current status | Evidence |
|---|---|---|---|
|The original model had no concrete application|A mechanism demonstration needs a decision-maker, controllable choices and useful outputs|First mapped it to contact recommendations; user then selected product launch|Application discussion and product specification|
|Can we call the opinion score a purchase probability?|Liking, awareness, affordability and purchase are different things|Add explicit awareness, perceived value, affordability and one-time ownership. New sales experiments are required|MODEL_SPEC.md|
|Can free samples be counted as sales?|That would inflate conversion and revenue|Use separate sample and paid flags; charge sample cost but record no sample revenue|Accounting rule; verification pending|
|Can we toss a purchase coin every period forever?|Any positive recurring probability can force eventual purchase and create artificial success|Use a transparent eligibility/value threshold and a finite campaign horizon|MODEL_SPEC.md|
|Does the old opinion stopping rule still work?|Awareness and experience can change even after opinions appear settled|Run a fixed60-period campaign; report unreached sales targets separately|Product timing specification|
|Does the old conserved-mean result still hold?|Pair compromise preserves the mean, but product experiences introduce external information|Restrict the invariant to compromise events; do not claim global mean/variance conservation for the product model|MODEL_SPEC.md; original verification identity|
|Original short runs suggested a degree-dependent long-run threshold|A connected snapshot can be a long delay before separation|Extend horizons and report the cap. Withdraw the unsupported long-run interpretation|Primary horizon summary|
|Some original runs never passed the freezing condition|Protecting a person's last disagreeing tie can make freezing impossible|Proved nonfreezing for all522 remaining saved legacy states; allow isolates in the recommended opinion process|stall_audit.csv; VALIDATION_REPORT.md|
|Our preferred similar-contact hypothesis did not clearly change final fragmentation|A failed hypothesis is useful evidence; absence of significance is not equivalence|Keep the negative result visible and qualify speed effects|primary_h3_paired.csv|
|Are900 contact snapshots900 independent runs?|Multiple horizons reuse the same stochastic realization|State180 realizations/900 repeated rows; split by horizon before ordinary analysis|application_by_horizon/|
|Does reusing a seed always give the same population across policies?|Different graph-generation paths can consume different draws|The product model uses separate graph, attribute, selection and event streams, with a fixed event-draw schedule|Product seed specification; implementation verification pending|
|Was AnyLogic already verified?|API documentation and a stand-in Java syntax check are not actual engine execution|Keep compile/run/export evidence pending until obtained from AnyLogic|AnyLogic_port.md; product port pending|
|Some papers have unreadable equations/scanned pages|A source being located does not mean its complete content was read|Try accessible copies, retain explicit read-status limits, request readable PDFs for unresolved material|LITERATURE_NOTES.md; OPEN_ISSUES.md|

|Git tracking in the managed workspace|The root `.git` directory is read-only, so ordinary initialization failed|Use supported alternate metadata in `.git-storage`, accessed with `./project-git`; this tracks the same working directory|Git initialization succeeded; first commit being prepared|
|Publishing to GitHub|The tool environment cannot connect to `api.github.com`; the login check alone cannot distinguish a bad token from network failure|Prepare `publish_github.sh` for a normal terminal; public upload remains pending until a successful URL is verified|`gh api user` connection error; publishing script|

|Pilot/main stream separation|Offsetting replication IDs by1000 would reuse a different stream family when seed bases are only1000 apart|Changed product stream bases to1,2,3 and4 million before the main experiments; pilot/main replication IDs stay disjoint|model.py and engine.py; verification rerun after the change|

|AnyLogic integration confidence|A tested Java algorithm is still not proof of engine wiring|Ran540 standalone Java cases and compiled/executed the Main wrapper against stand-ins; wrapper export exactly matches the Java reference. Generated a structurally checked .alp. Request only one actual engine run first|`java_kernel_comparison.csv`, `wrapper_readiness.json`, `alp_structure_checks.json`|
|Sales versus awareness|Nearly all customers know the launch by the end, yet many do not buy at higher prices|Keep the funnel explicit: awareness is not conversion. At price600, average paid sales are around32, not300|`analysis/policy_summary.csv`|
|Targeting effects are smaller than price effects in the baseline|We must not credit a price-plus-targeting improvement entirely to targeting|Compare seed rules at fixed price and show paired intervals; pilot-selected policy comparison remains separate|`analysis/paired_contrasts.csv`, `pilot_selected_evaluation.json`|
|Recommendation effect is not universally zero|Eight of nine final-profit h contrasts include zero; one high-price contrast has a positive pointwise interval|Report the exception and the multiple-comparison limitation instead of claiming no effect everywhere|paired_contrasts.csv|

|Unexpected quality sensitivity|At the hard confidence cutoff, higher experience quality produced fewer purchases in the first sensitivity runs|Do not hide or fix the result by tuning parameters. Launch an exploratory quality×confidence×rewiring diagnostic at fixed price400, plus initial sample-contact compatibility measurements. Interpretation pending its results|`sim/check_quality_effect.py`; original behavioral summaries retained|

## 5. Decisions made and their reasons

- Keep one product and one-time purchases to avoid adding subscription churn or replacement demand.
- Keep the same sample budget across launch policies, so a targeting comparison does not secretly spend more.
- Use three known social groups for the diversified strategy. Do not choose recipients using final simulation outcomes.
- Give highly connected people more opportunities to inform others, without assuming they have magically stronger persuasive power.
- Keep all price/cost/distribution values labeled synthetic and check sensitivity.
- Separate pilot and main replication cohorts. Do not pool overlapping seeds to claim extra independent data.
- Preserve the old opinion project as the validated mechanism foundation. Its existing numbers are not sales results.

## 6. How to understand and present the eventual results

For each policy we will show paid buyers, awareness, profit and uncertainty across independent synthetic markets. We will explain why the best observed policy wins in this model, how stable the comparison is, and which assumptions could change it. A model-based optimum among18 tested choices is not a guarantee for a real business.

Before presenting, both students should be able to explain one interaction, one purchase decision, the profit calculation, one verification check and one failed or uncertain hypothesis. The required AnyLogic `.alp`, actual CSVs and screenshots must be saved separately from the prepared Java text.

## 7. Chronological build log

| Time | Change / learning |
|---|---|
|Before product pivot|Read and corrected literature, reproduced opinion outputs, extended capped runs, diagnosed the isolate trap and completed a synthetic contact-policy case study|
|3 November,12:05 UTC /17:35 IST|Started the requested four-hour product build after the user selected the domain|
|Specification stage|Fixed the application,18-cell design, awareness/purchase distinction, synthetic attribute distributions, sample accounting, separate random streams and60-period horizon before sales experiments|
|Journal created|Added this living file at the user's request; subsequent implementation failures, fixes, checks and findings will be appended here|

|Implementation checkpoint|Readable product reference and C++ accelerator written; first30-customer/3-period run completed with accounting and structural assertions passing|
|Version-control checkpoint|Created a Git repository using alternate metadata because the managed `.git` path is read-only. Commits use the configured user identity; GitHub publication needs network access outside this sandbox|

|Main-results checkpoint|All18 policies evaluated on100 separate main markets. Pilot-selected price400/high-degree/h0 improves mean profit by₹874.50 over price500/random/h0, with paired95% interval[₹260.95,₹1471.50]. This changes both price and targeting; it does not isolate the targeting benefit|
|AnyLogic-readiness checkpoint|Generated CampusProductLaunch.alp;16 product checks and540 standalone Java cases complete. Main wiring/export check against stand-ins matches the Java reference exactly. One actual8.9PLE run is now needed; expected default148 paid buyers and₹19200 profit|

### Next checkpoint

Await the single AnyLogic engine check while finishing the marketing literature notes,13-minute slides, report, sensitivity interpretation and viva preparation. Keep actual engine status pending until students report/record it.

## Verified animation and confirmation checkpoint

- The first real AnyLogic run matched the default Java realization: 300 aware, 148 paid, 12 samples, Rs 19,200 profit. Its spiral layout and overlapping editor labels were confusing.
- We replaced that layout with three customer grids, person-shaped Consumer agents, opinion mini-bars and actual highlighted conversations. Animation now advances ten real interaction attempts per visual tick, preserving primitive draw order and period-end purchases.
- The students ran the revised model successfully. Their screenshot and actual default exports are saved: one summary and 61 period rows. Every summary field except cohort and wall-clock runtime matches the Java reference. This establishes one tested engine realization, not all reference-grid runs.
- The current animation is approved by the user. Further animation ideas were discussed only; no additional redesign is being implemented at this checkpoint.
- Real installed AnyLogic 8.9.10 libraries are now available locally. The revised code compiles against their actual Agent/shape APIs. Launching the editor from this managed workspace failed because desktop/socket access is restricted; the students supplied the successful runtime evidence instead.
- Three versus twelve samples improved profit on the main markets. To avoid selecting and confirming on the same data, four fixed comparisons were evaluated on 100 fresh markets (rep 5000–5099). The sample reduction gains Rs 2,854.50, paired 95% CI [2,698.50,3,006]; degree over random gains only Rs 31.50, CI [-112.50,177].
- The unexpected quality reversal persists without rewiring and reverses when all beliefs can influence each other. We keep it as a warning about the hard confidence assumption, not advice to lower quality.
- Prepared the report, viva, editable 16-slide PowerPoint (12 main + 4 backups), speaker notes and traceable chart data. Planned main duration is 735 seconds, leaving 45 seconds within the required 13 minutes. Windows PowerPoint rendering still needs a local look.
- Cache-cleanup request: found 8.4 GB yay cache and 4.4 GB pacman cache, but these paths are mounted read-only to tools. No successful deletion is claimed. Safe normal-terminal commands were supplied.

## Live-network branch, after the approved grid version

The user approved the grid animation, then requested a cleaner live-network alternative with explicit rollback. The alternative is a separate `CampusProductLaunch_LiveNetwork.alp`; the approved `CampusProductLaunch.alp` remains byte-identical. A local Git branch `approved_grid_animation_337a0f1` also preserves the checkpoint.

The new view draws all1,200 actual discussion ties, with solid/dotted compatibility styles, recent-meeting and new-contact highlights, opinion-colored customer nodes and separate ownership rings. It adds awareness/sales history, an opinion histogram and disjoint reasons why informed nonowners are not buying. These are computed from individual states and exported in61 period rows; no new behavioral assumption or random draw was added.

Checks: compilation against actual installed AnyLogic8.9.10 APIs passes; animated default plus180 batch summaries match the prior Java reference except cohort/runtime. Histogram sums, tie counts and buying-reason partitions pass. Actual live-network editor import/render/performance remains pending the first student engine run. Opening the approved grid file is the immediate rollback.

Presentation improvement: generated seven standard JFreeChart plots as PNG and SVG with exact asymmetric bootstrap endpoints. The primary PowerPoint uses those rendered figures for portable display. A separate deck retains native editable Office charts/workbooks. Apache POI/XmlBeans independently parses and schema-validates the primary16-slide deck; Windows PowerPoint rendering is still a separate compatibility check. Java2D previews were inspected and an overlapping heading was shortened.

## Git-history repair

The normal `.git` branch and the tool's writable `.git-storage` branch diverged when both were committed independently. The files were substantially the same, but Git correctly rejected a non-fast-forward push. We fetched the local ordinary history and merged it without conflicts, preserving both parent histories and the user's commit `bb8f9da`.

Prepared `unify-git.sh` for the normal terminal. It merges any remaining ordinary/remote commits, backs up the original metadata to ignored `.git-root-backup/`, and replaces `.git` with Git's supported pointer to `.git-storage`. Ordinary `git` and `project-git` then share one branch/index. It does not reset working files or force-push. A normal-terminal step is required because the managed permission profile makes the original root `.git` read-only to tools.

## Live-network visual simplification

The user rejected the dark dashboard style as cluttered. We changed the separate network variant to a white background, a larger full-width graph, plain labels and compact plots underneath. Customer colors now use the familiar four awareness/ownership states; opinions appear in the selected meeting and histogram instead of requiring a second color/ring legend. The highlighted meeting is blue and a new tie is orange. Data definitions, buying rules and financial outcomes are unchanged. The approved grid fallback remains byte-identical.

The Git unification has been applied: `.git` now points to `.git-storage`, so ordinary Git and tool checkpoints share the same history.

## Final package checkpoint

The saved-data audit passed for10,240 reference policy evaluations,1,080 standalone Java evaluations and the supplied actual engine exports. The engine exports describe the same replication1000 across grid/network variants and are not independent extra markets. The approved grid SHA-256 remains unchanged.

Both presentation copies, a16-page PDF, seven PNG/SVG figures, the report, literature/validation notes, viva and speaker notes are prepared. The primary deck passes independent OOXML schema validation and its previews were inspected. The submission ZIP includes project files and archived mechanism evidence, with a per-file SHA-256 manifest and archive CRC check. Moodle upload, current white-animation visual review, presentation-computer compatibility and rehearsal remain student actions. A multi-policy AnyLogic batch is recommended additional engine evidence; the larger reference grid stays separately labeled.

Git metadata is unified for normal-terminal use. The managed tool now sees that shared metadata as read-only, so final file commits/pushes are performed by the user; no successful tool-side push is claimed.

## Final literature and packaging follow-up — 3 November

Direct public PDF access became available after the workspace permissions changed. We completed the previously missing Delre2010 segment and Eq.3, read Bass1969 through full local OCR, read DiMaggio1996 main text/appendices/references with damaged paragraphs checked as images, and recovered Deffuant draft equations/captions through rendered pages. HK appendix pp.30–33 were also inspected. The lesson is that an extraction failure is not evidence that an equation is absent: image checks can resolve fonts, while draft contradictions and uncertain table cells still need explicit limits. Source URLs, hashes and coverage are recorded; copyrighted articles are not redistributed.

The product behavior and both animations are unchanged in this follow-up. We clarified that degree-targeted recipients are peers in a modest-degree synthetic network, and that similarity-based reconnection assumes knowledge of candidates’ beliefs. Final audit and archive regeneration follow the note corrections. Git access is restored and the completed package can be committed and pushed under the configured user identity. Students still review the white layout/slides on the presenting machine, rehearse, and handle Moodle submission.

## 4 November — simplify and explain for the presentation

The students requested a simpler flat-color network, a data-led presentation with the initial pitch/feedback/application story, and a short guide to every grading criterion. We retrieved and read the original three-page pitch from Downloads and saved it in the product sources folder. Feedback is explicitly attributed to the students’ account; no quotation or undocumented professor instruction was invented.

We preserved the previous model/deck/notes in `revision_archive/before_presentation_simplification/`. The approved grid remains byte-identical. The separate network now uses grey/blue/orange/green customer states, grey solid/dotted ties, black meeting highlights, blue new contacts and a single-blue opinion histogram. Its customer kernel, seeds, scheduling and CSV schemas did not change. Installed API compilation and animated/default plus180 stand-in batch comparisons passed; the latest display still needs one student visual check.

The new20-slide presentation has16 main slides and4 Q&A backups, with a700-second plan including90 seconds for the demo. It explains actual AnyLogic components, all behavior parameters, synthetic-input summaries, individual rules and worked examples, paired/fresh-market experiments, recommendations, negative findings and limitations. The short explainer is about2,000 words; report/viva remain optional references. PDF and PowerPoint are generated from the same content and saved CSVs. Rendering checks caught table/text crowding, so table row heights and fitted text were corrected before publication.
