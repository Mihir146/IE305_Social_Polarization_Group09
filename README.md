# IE305 — campus product launch through word of mouth

**Group 9 · Mihir Jagdish Vasave and Vaibhav Mathur**  
[Public repository](https://github.com/Mihir146/IE305_Social_Polarization_Group09)

We simulate a hypothetical seller launching a reusable bottle to 300 connected customers. Prices, free samples, conversations, individual budgets and experience shape paid purchases and modeled profit. All customer data and behavioral inputs are synthetic.

## Open the model

| File | Purpose / evidence |
|---|---|
|[CampusProductLaunch.alp](handoff_output/product_launch/CampusProductLaunch.alp)|Approved grid animation; actual default screenshot and CSV verified|
|[CampusProductLaunch_LiveNetwork.alp](handoff_output/product_launch/CampusProductLaunch_LiveNetwork.alp)|Separate live network with opinion colors, tie styles and history plots; actual API/wiring checks pass, current flat-color completed display and matching default export confirmed by student screenshot|
|[RUN_ANYLOGIC.md](RUN_ANYLOGIC.md)|Exact opening and running steps|
|[LIVE_NETWORK.md](handoff_output/product_launch/LIVE_NETWORK.md)|Visual meanings, extra data and immediate rollback|

Use AnyLogic **8.9 PLE**. The tested default is policyIndex6, rep1000: period60, 300 aware,148 paid buyers,12 samples and Rs19,200 profit. Free recipients are not paid buyers. The live-network variant uses the same behavioral kernel; opening the approved file is the rollback.

## Read and present

- [Project report](handoff_output/product_launch/PROJECT_REPORT.md): business question, inputs, model, experiments, results and limitations.
- [PowerPoint](handoff_output/product_launch/Campus_Product_Launch.pptx): 16 main slides plus4 backups; planned11m40s including the live model. Plain-language tables, parameter explanations and charts cover the rubric.
- [Short project explainer](handoff_output/product_launch/UNDERSTAND_THE_PROJECT.md): read this first to understand the model and every grading criterion.
- The previous deck and animation are preserved in `handoff_output/product_launch/revision_archive/`.
- [Speaker notes](handoff_output/product_launch/SPEAKER_NOTES.md) and [viva guide](handoff_output/product_launch/VIVA_PREP.md): explanations and25 questions.
- [Literature](handoff_output/product_launch/LITERATURE_NOTES.md), [validation](handoff_output/product_launch/VALIDATION_REPORT.md) and [open issues](handoff_output/product_launch/OPEN_ISSUES.md): precise evidence boundaries.
- [PROJECT_JOURNAL.md](PROJECT_JOURNAL.md): progress, issues, lessons and fixes.

The main synthetic finding is that three samples outperform twelve in contribution profit under the baseline assumptions; the gain persists on fresh confirmation markets. The extra degree-targeting advantage is small and uncertain. A quality/confidence diagnostic exposes an assumption that needs validation. None is presented as a real-campus sales forecast or a globally optimal policy.

[Submission ZIP](handoff_output/IE305_Group09_Submission.zip) contains both models, slides, reports, data and support code. See [SUBMISSION_GUIDE.md](handoff_output/product_launch/SUBMISSION_GUIDE.md) for the remaining presentation/upload steps.

## Data and reproducibility

The [product folder](handoff_output/product_launch/README.md) contains the exact model specification, synthetic inputs, raw policy outcomes, scripts, plots and actual engine evidence. Browser HTML files are optional chart/text-slide viewers. The required simulation is the `.alp`, and the submission deck is PowerPoint/PDF.

The original handoff is preserved in `handoff/`; the opinion-network literature and validation foundation is in `handoff_output/`. Its opinion-only results are separate from product-sales evidence.

## Git in this managed workspace

Commits use **Mihir <mihirv416@gmail.com>**. Git metadata is unified: the root `.git` points to `.git-storage`, and ordinary `git` and `project-git` share one history. The original metadata backup is ignored. From a normal terminal:

```sh
git add handoff_output PROJECT_JOURNAL.md RUN_ANYLOGIC.md README.md
git commit -m "Update project handoff"
git push
```

Git metadata and network access are now available to the project tool, and the completed package has been committed and pushed to the public remote under the configured user identity. A normal clone uses ordinary Git without any unification step. Installed third-party software and personal caches do not belong in the repository.

Research, implementation, analysis and drafting were AI-assisted. The students must understand the work, run their required model, follow course disclosure rules and submit/present it themselves.
