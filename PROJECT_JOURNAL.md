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
|Read the marketing sources supporting the added rules|In progress|Public Bass/Kempe/Delre sources located; reading status will be recorded honestly|
|Implement the purchase/awareness/experience model|Readable reference and accelerated engine written; first tiny run succeeds|`product_launch/sim/model.py`, `engine.py`, `native.cpp`; full verification next|
|Verify product rules and accounting|16 checks passed, including exact native/reference states and analytical limits|`product_launch/sim/verification.csv`; actual AnyLogic execution remains pending|
|Run pilot and independent main experiment|Pending|Planned18 cells:3 prices ×3 seeding rules ×2 recommendation rules|
|Run focused sensitivity checks|Pending|Inputs and policy contrasts will be logged|
|Prepare the product AnyLogic port and export contract|Pending|Actual compilation/runtime remains student-side|
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

### Next checkpoint

Implement both the readable product reference and accelerated engine, then run deterministic and limiting-case checks before interpreting any pilot outcome. Update the progress table with actual files and results.
