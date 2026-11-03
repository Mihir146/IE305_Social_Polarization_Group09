# Campus product launch through word of mouth

**IE305 Simulation Lab · Group 9 · Mihir Jagdish Vasave and Vaibhav Mathur**

A hypothetical campus seller launches a reusable bottle to 300 connected customers. We compare launch prices, free-sample recipients, sample quantities and discussion-contact policies. The business outcome is campaign profit, while awareness and paid purchases are tracked separately. All input data are synthetic assumptions.

## Start here

- Open [CampusProductLaunch.alp](CampusProductLaunch.alp) in **AnyLogic 8.9 PLE on Windows 11**. Follow [ANYLOGIC_BUILD.md](ANYLOGIC_BUILD.md). The first default run should match the independently tested Java realization: period 60, 300 aware, 148 paid, 12 free samples, ₹19,200 profit.
- Read [UNDERSTAND_THE_PROJECT.md](UNDERSTAND_THE_PROJECT.md) first: a short explanation of every grading criterion, parameter and key result. Use [PROJECT_REPORT.md](PROJECT_REPORT.md) and [VIVA_PREP.md](VIVA_PREP.md) for details.
- Use `Campus_Product_Launch.pdf` or the matching editable `Campus_Product_Launch.pptx`:20 slides (16 main,4 Q&A), planned11m40s including the demo. Text/tables are editable in PowerPoint. The previous native-chart deck remains archival; it is not the current talk. HTML files are optional older viewers.
- Check [VALIDATION_REPORT.md](VALIDATION_REPORT.md) and [OPEN_ISSUES.md](OPEN_ISSUES.md) before making claims about engine validation or real-world accuracy.
- The living progress/issue/learning record is [PROJECT_JOURNAL.md](../../PROJECT_JOURNAL.md).

**Engine status:** the revised model has run successfully in AnyLogic. The student-supplied screenshot and actual default export match the Java reference exactly, except cohort and runtime. One summary row and 61 period rows were inspected. The automatic multi-policy engine batch remains unobserved. Evidence is in `anylogic/evidence/` and `sim/analysis/actual_anylogic_exact_comparison.csv`.

The optional [live-network variant](LIVE_NETWORK.md) is a separate `.alp`. The approved grid file remains unchanged. Check its own evidence status before using it for the live demo.

## What the model does

Customers can be unaware, aware without owning, free-sample owners or paid owners. An aware contact can inform a neighbor. Similar opinions average; sufficiently different opinions can trigger replacement of a discussion tie. An informed non-owner buys only if both affordability and perceived value exceed the price. A new owner receives a personal experience signal. Each person buys at most once.

The original opinion-only project is preserved one level above this folder and in `../../handoff/`. Its opinion results are background validation evidence; they are not product-sales data.

## Data and experimental design

The original design fixed 12 samples, three prices, three seeding rules and two contact policies: **18 cells × 100 main markets = 1,800 runs**, preceded by a separate 30-market pilot. A later exploratory follow-up adds three-sample versions: **36 cells × the same 100 main markets = 3,600 policy evaluations**. This is still 100 independent markets, not 3,600 independent populations.

A further 400 evaluations compare four fixed policies on 100 fresh confirmation markets. Focused checks add 2,400 network/sample-stress runs, 2,100 behavioral sensitivity runs and 1,200 quality/confidence diagnostic runs. The separate Java implementation has 1,080 reference runs. Do not pool these designs or generators into one sample size.

`sim/results/` contains raw rows. `sim/analysis/` contains bootstrap summaries and paired contrasts. `data/` contains the reproducible 300-customer exemplar and initial contacts. The data dictionary explains fields and synthetic distributions. Fixed seeds and the exact model rules are in [MODEL_SPEC.md](MODEL_SPEC.md).

## Reproduce outside AnyLogic

AnyLogic itself needs no Python or external JAR for the supplied self-contained model. For the independent accelerated experiments, use Python with NumPy and a C++17 compiler (`g++`):

```sh
cd handoff_output/product_launch
python3 sim/verify.py
python3 sim/run_experiments.py --cohort pilot --workers 2
python3 sim/run_experiments.py --cohort main --workers 2
python3 sim/analyze.py
python3 sim/run_sensitivity.py
python3 sim/analyze_sensitivity.py
python3 sim/run_budget_followup.py
python3 sim/analyze.py --input sim/results/budget3_runs.csv --outdir sim/budget3_analysis
python3 sim/check_quality_effect.py
python3 sim/finalize_analysis.py
```

Read each script's `--help` before changing options. Sensitivity scripts may offer cohort arguments; preserve the supplied replication ranges. These commands are for a machine with the stated dependencies; the Windows AnyLogic demo does not need a C++ compiler. Precomputed CSVs are included.

To compile the independent Java implementation, from this folder:

```sh
javac -d java_build anylogic/ProductKernel.java anylogic/KernelCheck.java
java -cp java_build KernelCheck sim/results/java_kernel_runs.csv
```

`KernelCheck` contains the authoritative output-path behavior; inspect it before rerunning. Java and NumPy use different random generators. Their same-numbered seeds do not identify the same markets. Compare their distributions; compare an AnyLogic export exactly only with its matching Java-kernel run.

## Interpretation

The largest observed mean is a finite simulated policy comparison. It is not a global optimum, a calibrated business forecast or proof that the chosen targeting rule is best. In the baseline, price and sample spending matter more than small final targeting differences. A hard confidence cutoff also produces a counterintuitive quality result; the report keeps it visible as a model-risk diagnostic.

Research, code, analysis and drafting were AI-assisted. The students are responsible for understanding, running and presenting the model and for following their course's disclosure rules.

## Rebuild the current presentation

Install `sim/requirements_presentation.txt` in a temporary Python environment, then run `python sim/build_consulting_presentation.py`. It produces matching PDF and PowerPoint, charts from saved CSVs, speaker notes and a provenance/timing manifest. `sim/verify_deck_with_poi.py` independently validates/previews the PowerPoint with installed Apache POI. Rendered PDF pages were also inspected. The older `build_deck.py`/`portable_deck.py` workflow reproduces the previous archived deck, not the current version. Third-party libraries are not redistributed.
