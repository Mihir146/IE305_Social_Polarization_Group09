# Run the model in AnyLogic 8.9 PLE on Windows 11

## Where the model is

Open **`handoff_output/product_launch/CampusProductLaunch.alp`**. It is the required AnyLogic model. HTML files are chart/presentation support files and do not run the simulation.

**First engine check succeeded:** the student supplied a Windows PLE screenshot showing period 60, 300 aware, 148 paid buyers, 12 samples, revenue ₹59,200, cost ₹40,000 and profit ₹19,200. This matches the standalone Java default. Evidence: `anylogic/evidence/first_engine_run_windows.jpg` and `engine_check.json`. The exact installed patch version and CSV contents are not visible in that screenshot.

**Current revision:** improves the animation and adds the three-sample policies and automatic batch. Java wiring checks pass, including unchanged default results and 180 batch cases exactly matching the Java reference. The revised animation is now confirmed by the student-supplied screenshot and actual default CSVs. The one default summary matches Java exactly except cohort/runtime, and 61 period rows were inspected. The automatic engine batch is still unobserved. Evidence: `revised_engine_run.png`, `revised_engine_check.json` and `actual_anylogic_exact_comparison.csv`.

## Open and run

1. Get the latest repository files and extract any ZIP first. In AnyLogic choose **File → Open**, select `CampusProductLaunch.alp`, and accept older-format conversion if offered.
2. Expand the project, right-click **Simulation → Run**. Press play if paused.
3. Keep **policyIndex=6**, **rep=1000** for the default illustration. It should still finish with **148 paid buyers and ₹19,200 profit**.
4. Use real-time speed 1× to watch conversations, or around 2× for a shorter demonstration. Use the toolbar's fit/zoom control if the entire presentation does not fit your screen.
5. Let period 60 complete. The console prints the absolute output path. Save the converted `.alp` and actual output files.

The editor's parameters are not intended as overlapping labels in the running presentation. To select another policy, stop the model and change the **Main parameter default** in the editor, or override it in the Simulation experiment's parameter properties. Restart for the changed setting. Changing a caption does not change a model input.

## What the animation means

There are three panels of 100 **Consumer agents**. The panel is the customer's known social group. Position within a panel is only a stable layout; it is not an opinion axis or a friendship edge.

- Gray: unaware of the launch. Amber: informed without ownership. Purple: free-sample owner. Green: paid owner.
- A blue mini-bar beneath each person shows their current belief, on a 0–1 scale. Longer means higher expected appeal.
- Yellow marks identify the participants in the highlighted meeting. A blue line connects the selected pair. An orange line marks a new contact when a disagreement causes replacement.
- The conversation panel gives the actual selected meeting and both before/after beliefs. It can also show a meeting where information was not shared or confidence was too low for averaging.
- The display advances **10 actual attempted interactions per visual tick**, highlighting the latest attempt. It does not pretend that the highlighted meetings are the entire contact graph or all interactions.
- Purchases happen simultaneously after all 300 attempts in a period. New owners then receive their own experience signal. Thus opinion changes can occur through conversations and through ownership experience.

The scheduler stores separate customer states and a contact graph. Every AnyLogic Consumer references its own live state. There is no aggregate sales-growth equation. Main schedules the agent interactions and collects results; central scheduling is compatible with agent-based modeling.

The event interval is .05 engine seconds. With animation on, one campaign period uses 30 ticks, or 1.5 engine seconds. A full campaign takes 90 engine seconds. These are display speeds, not real days. With animation off, each tick executes one entire campaign period for faster batch runs; the primitive random draw order and period-end purchase schedule stay the same.

## Policy choices

| Base index | Recipients | Price | Contact policy |
|---:|---|---:|---|
|0 / 1|Random people|₹400|Random / similar|
|2 / 3|Random people|₹500|Random / similar|
|4 / 5|Random people|₹600|Random / similar|
|6 / 7|Most contacts|₹400|Random / similar|
|8 / 9|Most contacts|₹500|Random / similar|
|10 / 11|Most contacts|₹600|Random / similar|
|12 / 13|Distributed across groups|₹400|Random / similar|
|14 / 15|Distributed across groups|₹500|Random / similar|
|16 / 17|Distributed across groups|₹600|Random / similar|

Indices **0–17 use 12 samples**. Add **18** to use **3 samples** with the same price, targeting and contact rule. For example **24 = ₹400, 3 samples, most contacts, random replacements**. This is the provisional finite-candidate recommendation. Index 6 remains the original default illustration so the first run has a stable numerical reference.

## One automatic engine batch after the visual run works

Set **policyIndex=36**, **rep=1000**, **animateNetwork=false**, and choose a fresh output directory such as `product_batch`. Select **virtual time / as fast as possible**, then run once. The model sequentially executes 36 policies × 5 markets = **180 campaigns** and writes separate files. No paid Parameter Variation feature is needed.

This is an integration batch, not the 100-market reference precision claim. No additional automatic replications should be added. Identical policy/rep reruns replace the same named export and are not new observations. A batch with another starting rep uses different markets; keep IDs below one million.

## CSV exports and comparison

Each campaign writes:

```
product_output/summary/policy6_rep1000.csv
product_output/trajectories/policy6_rep1000.csv
```

A normal campaign gives one summary row and 61 trajectory rows, including period 0. The summary schema matches the reference data. From this product folder, after collecting actual engine files:

```sh
python sim/ingest_anylogic.py PATH_TO_PRODUCT_OUTPUT
python sim/compare_implementations.py --candidate sim/results/anylogic_runs.csv --reference sim/results/java_kernel_runs.csv --exact-java --out sim/analysis/actual_anylogic_exact_comparison.csv
```

The supplied Java reference covers rep 1000–1029 and all 36 policies. A matching engine run should agree exactly except cohort label and wall-clock runtime. For other replication IDs, generate matching Java references or use a separately labeled distribution comparison. Java and NumPy/C++ same-numbered seeds are different generators, so they should not be forced into an exact trajectory comparison.

## Manual construction fallback

Use only if importing the `.alp` fails; preserve the exact error first. Create Main and Consumer, a Consumer population `consumers` of initial size 300, and the four parameters `policyIndex` int 6, `rep` int 1000, `animateNetwork` boolean true and `outputDirectory` String `"product_output"`. Paste the supplied additional-class bodies, set Main startup to `initializeLaunch();`, and add a cyclic timeout event at .05 seconds calling `advanceLaunchPeriod();`. Stop option must be **Never**; the model finishes itself.

The animation requires the named public shapes and labels serialized by `sim/build_alp.py`, including Consumer `nodeMark`, `headMark`, `beliefMark`, `focusMark`; Main status/group/interaction labels and progress/meeting rectangles. The build script lists their exact names and layout. The earlier minimalist manual instructions do not contain the revised animation, so importing the prepared file is the practical route.

## API evidence

The animation uses public documented rectangle methods `setWidth`, `setVisible`, `setPos`, `setRotation` and `setFillColor`; see [AnyLogic Rectangle documentation](https://www.anylogic.help/anylogic/presentation/rectangle.html). Consumer position and connection APIs use Agent methods. API documentation and stand-in checks support the revision, but the visual engine check remains necessary. No actual engine data are manufactured from the stand-in harness.
