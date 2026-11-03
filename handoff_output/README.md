# IE305 reviewed handoff

**Mihir Vasave and Vaibhav Mathur · 3 November 2026**

The tested application is **contact recommendations for a hypothetical campus discussion platform**. Synthetic agents discuss one policy and may replace disagreeing contacts. The most useful result is that adding contacts or changing recommendations can change how quickly communication separates, so a short observation window can suggest a misleading long-run threshold.

**Selected final application: [product launch](product_launch/README.md).** The supplied product `.alp` has a successful actual default run, screenshot and inspected CSV export. Product sales results, report and PowerPoint are in that folder. The material below preserves the original opinion/contact mechanism study; its opinion-only Java port remains a separate unexecuted port.

## Read in this order

| File | Use |
|---|---|
|[PROJECT_REPORT.md](PROJECT_REPORT.md)|Readable application, model, data, experiments, findings and limits|
|[presentation.html](presentation.html)|Offline presentation with tables and speaker prompts; keyboard arrows navigate|
|[results_explorer.html](results_explorer.html)|Nine standard Plotly scientific figures, embedded data, CSV links and offline numerical tables|
|[APPLICATION_DESIGN.md](APPLICATION_DESIGN.md)|Historical contact study and pointer to the implemented product application|
|[AnyLogic_port.md](AnyLogic_port.md)|Build instructions, Java bodies, API audit, CSV export and test checklist|
|[VALIDATION_REPORT.md](VALIDATION_REPORT.md)|Pass/partial/pending checks, quantitative benchmarks, revised conclusions and commands|
|[LITERATURE_NOTES.md](LITERATURE_NOTES.md)|Actual reading status, exact published rules/targets, limitations and57 original claim passages|
|[VIVA_PREP.md](VIVA_PREP.md)|One-page explanation,25 questions and glossary|
|[FIVE_HOUR_PLAN.md](FIVE_HOUR_PLAN.md)|Prioritized work split for the two students|
|[OPEN_ISSUES.md](OPEN_ISSUES.md)|Remaining uncertainties ranked by assessment impact|

## Important changes from the supplied package

- The recommended main model **allows isolates** and uses a30,000-sweep cap. All2,790 primary runs freeze numerically within this cap. Original results remain separately preserved.
- Every originally capped legacy run was extended. All522 still flagged at30,000 have a diagnosed structural reason to remain nonfreezing under isolate protection.
- The apparent positive rewiring threshold moves substantially when we observe longer. The original long-run interpretation is withdrawn.
- H3 remains unsupported: the examined paired intervals include zero. This does not establish equivalence. A universal speed advantage is also unsupported.
- Literature equations, mechanisms and citations were corrected; numerical/source gaps remain labeled. Read status is not silently upgraded to “fully verified.”
- The application has180 realizations and900 repeated snapshots across six policies. The extra horizon rows do not increase the independent replication count.

## Data to use

| Path | Meaning |
|---|---|
|`sim/results_primary.csv`|Recommended full grid:2790 rows, isolates allowed, cap30000|
|`sim/primary_short_D.csv`|Matching short-horizon primary D comparison:630 rows, cap3000|
|`sim/primary_analysis/`|Primary scenario summaries and intervals|
|`sim/application_snapshots.csv`|Six contact policies;180 realizations, five repeated horizons|
|`sim/application_by_horizon/`|One180-row file per horizon, ready for ordinary CSV analysis|
|`sim/application_summary.csv`, `application_paired.csv`|Application means, intervals and within-degree paired contrasts|
|`data/`|An actual generated300-person/1200-edge input example, not empirical data|
|`sim/kb_validation.csv`, `hk_validation.csv`, `binary_validation.csv`|Separate published-model benchmark runs|
|`sim/results.csv`, `results_long_cap.csv`|Legacy protected-isolate outputs, retained for audit|
|`sim/legacy_figures/`|Original plots/summary; historical evidence, not the revised primary figures|

Repeated scenarios/seeds across files must not be pooled as new independent observations. Metadata identifies model rule and observation cap. `sim/analyze.py` rejects mixtures and duplicate replication/seed rows.

## Run only what you need

From this folder, using Python3 and NumPy:

```sh
python sim/analyze.py --tables-only --outdir sim/primary_analysis
python sim/build_figures.py
```

The interactive figures use the official Plotly CDN and need internet access to render charts. Data are embedded, not fetched remotely. Expand the numerical tables to read the results offline; the presentation's tables also work offline. The camera button exports PNGs in a compatible browser. Rendering/export in the students' actual browser still needs checking. If Matplotlib is installed, omitting `--tables-only` also generates PNGs from the analyzer.

To rerun the primary/application experiments, NumPy plus a C++17 compiler (`g++`) is sufficient for the supplied accelerator:

```sh
python sim/verify_native.py
python sim/sanity.py
python sim/run_primary.py
python sim/summarize_primary.py
python sim/run_application.py
python sim/build_figures.py
```

The shared library is built locally from `native.cpp`. A Linux binary is not a portable requirement; no fast-math flags are used. The readable model optionally uses numba. Full literature regeneration is substantially longer than the old two-minute reference grid; see the exact commands in `VALIDATION_REPORT.md`.

## Students' remaining implementation work

1. Open AnyLogic and follow the two-agent/two-action build in `AnyLogic_port.md`.
2. Run the deterministic pair, triangle and bridge checks; record actual results and version.
3. Run a reduced stochastic batch with distinct replication indices. Save its CSVs and analyze against the matching rule/horizon reference.
4. Save the `.alp`, screenshots and comparison evidence. Replace pending statements only with what actually ran.
5. Rehearse using the viva questions. Both students should explain the mechanism, censoring and failed hypothesis.

No AnyLogic CSV, `.alp` or screenshot is fabricated. API documentation and a stand-in Java syntax check do not replace engine execution.

## Provenance and unresolved reading

The original supplied folder is preserved as `../handoff/`; the claim inventory records original line locations and SHA256 hashes. `sources/READING_LOG.md` records what was actually accessed. A readable original Deffuant PDF and an OCR/text-enabled DiMaggio1996 PDF would resolve the largest remaining extraction gaps; Bail's supporting information is not fully read. See `OPEN_ISSUES.md` for the full register.

AI assistance covered literature review, programming, experiments and drafting. The students should understand and verify the material they present and record their actual implementation work.
