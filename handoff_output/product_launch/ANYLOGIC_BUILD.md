# Build and test in AnyLogic8.9 PLE on Windows11

**Actual engine status: not yet compiled or run in AnyLogic.** The pure Java kernel is tested separately. This guide prepares the required engine execution and live animation; it does not claim that execution has happened.

## Fast path: one short engine check

Open **CampusProductLaunch.alp** in AnyLogic8.9PLE, accept the normal older-format conversion if offered, and run the default **Simulation** once to period60. No manual construction is needed for this generated project. The checks available here have passed: Java kernel fixtures,540 Java runs, wrapper compilation/export against stand-ins and XML structure. Actual engine import/compilation remains the one missing check.

With defaults **policyIndex=6,rep=1000**, the matching standalone Java run ends at **300 aware,148 paid buyers,12 samples,profit₹19200**. It should save one summary row and61 period rows. Report either those final values or the exact opening/compiler/runtime error. This is the only first test requested; further checks depend on what it shows.

The source file deliberately uses the observed8.8.2 project format for opening/upgrading in8.9. It was generated here, not saved by an installed AnyLogic editor. Preserve the saved/converted .alp after a successful run. The manual steps below are a fallback/reference.

## 1. Minimum build: two agent types, four parameters, one event

1. Create a new model, **CampusProductLaunch**, using seconds as the model time unit. Keep the root agent named **Main**.
2. Create an agent type named **Consumer**.
3. Open **Consumer → Advanced Java → Additional class code**. Paste the entire [Consumer body](anylogic/Consumer_additional_class_code.java.txt). Do not create separate Variable or Function elements with the same names.
4. Draw a small rectangle named **nodeMark**, size8×8 centered at(0,0), and make it public/visible on the upper agent. The controller updates its fill using `stateColor()`. Set its tooltip to `customerTooltip()` if the editor offers that property.
5. In Main, create an agent population named **consumers**, type **Consumer**, initial size **300**. Select a **User defined** network and enable its connection display. Do not use an automatic random-network generator: the model generates its own initial graph.
6. Create these four **Parameter** elements in Main, with exactly these names:

| Name | Type | Default |
|---|---|---|
|`policyIndex`|int|6|
|`rep`|int|1000|
|`animateNetwork`|boolean|true|
|`outputDirectory`|String|`"product_output"`|

7. Open **Main → Advanced Java → Additional class code**. Paste the entire [Main body](anylogic/Main_additional_class_code.java.txt). It embeds the kernel; no JAR, extra Java Class element or Python installation is needed inside AnyLogic.
8. Main **On startup** action: `initializeLaunch();`.
9. Create a cyclic timeout Event named **launchPeriod**. Set first occurrence to **.5 seconds**, recurrence **.5 seconds**, action `advanceLaunchPeriod();`.
10. In the Simulation experiment, use seconds and set its stop condition to **Never**, or a stop time greater than31 seconds. The model exports after period60 and calls `finishSimulation()` itself. An earlier experiment stop would prevent its final export.

Run once. At period0 there should be12 purple sample owners. Over time gray customers become informed, some turn green after paying, and the summary should reach period60. Inspect the console for the actual absolute CSV output path.

## 2. Animation and live display

The three clouds represent the three pre-campaign social groups. Customer positions depend only on ID/group; layout randomness does not consume model draws. Link colors/layout are not evidence of sales or fragmentation; the recorded metrics are.

| Color | Meaning |
|---|---|
|Gray|Unaware of the launch|
|Amber|Aware, without a free sample or paid purchase|
|Purple|Received a free sample; never counted as a paid sale|
|Green|Made one paid purchase|

Add a large public **Text** element named **statusLabel** in Main. The controller sets its text from `launchStatus()`. Put it above the agent clouds. Add a static legend using the four colors. Set a comfortable model window/presentation size, for example900×550, with the clouds around x150,400,650 and y230.

If time permits, add a Time Plot with automatic updates at.5-second intervals. Its values can reference the last history row:

```java
launch == null ? 0 : launch.history.get(launch.history.size()-1)[1] // aware
launch == null ? 0 : launch.history.get(launch.history.size()-1)[2] // paid buyers
```

The x-axis then shows **engine seconds**, with one model period per.5 seconds. Label this mapping. Use the CSV trajectory for plots whose x-axis must be the integer campaign period. The engine-time interval is not a real-day calibration.

The kernel's adjacency matrix is the graph used by the rules. With animateNetwork=true, the controller mirrors it into Consumer connections after every period. With animation off, it avoids those display updates; the mathematical graph still evolves. Each Consumer holds a reference to its own live kernel state, so its color/tooltip follows the actual customer state.

## 3. Policy index and reduced experiment

| Index | Sampling strategy | Price | h |
|---:|---|---:|---:|
|0,1|Random|400|0,1|
|2,3|Random|500|0,1|
|4,5|Random|600|0,1|
|6,7|Highest degree|400|0,1|
|8,9|Highest degree|500|0,1|
|10,11|Highest degree|600|0,1|
|12,13|Distributed across groups|400|0,1|
|14,15|Distributed across groups|500|0,1|
|16,17|Distributed across groups|600|0,1|

Every policy has12 samples and unit cost250. Thus comparisons at the same price hold sample spending fixed. Policy6 is the highest-pilot-mean candidate; policy2 is the default comparison policy. This is not a guaranteed optimum for actual customers.

If Parameter Variation is available in your PLE installation, choose **Freeform**,90 runs, with extra automatic replications **off**:

```java
policyIndex: index / 5
rep: 1000 + index % 5
animateNetwork: false
outputDirectory: "product_batch"
```

These are separate parameter-table expressions, not a Java block. Five runs/cell provide a small engine integration check, not the main precision claim. If time is tight, start with policies2 and6, ten replications each; then broaden only after checks pass. Manual Simulation runs with changed rep values are a fallback. Do not count an identical policy/rep rerun as a new independent observation.

Use virtual/maximum speed and animation off for batches. The PLE Custom experiment is not a fallback. Keep the actual exported run count in the report.

## 4. Exports and comparison

Each run writes separate files, avoiding parallel append conflicts:

```
product_output/summary/policy6_rep1000.csv
product_output/trajectories/policy6_rep1000.csv
```

Summary fields match `sim/results/main_runs.csv`. Trajectory fields match `main_trajectories.csv`. Replication seeds are four separate logged streams. Java and NumPy use different generators; equal seed labels do not mean identical markets or paths.

After collecting files, run the supplied ingestion/comparison commands from the product folder; see its README. Compare only the same price, sampling rule, h, horizon, group graph and behavioral assumptions. The standalone Java-kernel output is **not** an AnyLogic export.

## 5. Reference checks (not a request to run a long test suite)

- Population300, total initial graph edges1200, samples12, paid0, revenue0, cost3000, profit−3000 at period0.
- Free recipients remain separate from paid buyers; sample count stays12.
- At every paid purchase the buyer was aware, could afford the price, had sufficient pre-purchase value and had not already owned the product.
- The graph stays simple and undirected with1200 edges. Isolates are permitted.
- Repeat the same policy/rep: outputs match except wall-clock seconds. Change rep for a new market.
- Let the model reach period60. Confirm exactly one summary row and61 trajectory rows, including period0. Record output paths, version and actual values.
- Run a small batch and compare distributions with the matching reference. A single realization need not equal a reference mean.
- Save **CampusProductLaunch.alp**, all support files and screenshots. Reopen that saved model before presentation.

The Java class `ProductKernel.java` can be tested with `KernelCheck.java` independently of AnyLogic. Passing it strengthens the algorithm check; it does not verify the AnyLogic editor, population properties, animation, event wiring or export location.

## 6. Common build problems

| Symptom | Check / smallest likely correction |
|---|---|
|Duplicate variable/function|Remove editor elements duplicating fields/methods already pasted into Additional class code|
|Unknown Consumer/Main name|Keep the exact agent type/population names used in this guide|
|Unknown policyIndex/rep/etc.|Create the four Parameter elements in Main with the specified types|
|All circles stay gray|Use a dynamic fill expression, not a static fill; verify startup assigns Consumer.state|
|Model stops before export|Remove the experiment's early stop time and let period60 finish|
|Output files seem missing|Use the console's absolute path; the working directory can differ from the .alp folder|
|Repeated results across batch runs|Check that rep changes and that extra replication settings do not duplicate the same index|
|Compiler/API message|Save the exact error and surrounding code. Change the smallest affected line; do not alter the purchase rules to silence an unrelated editor error|

The earlier Agent API audit covers `connectTo`, `disconnectFromAll` and execution control; `setXY` is a documented Agent method. Exact engine integration remains pending until tested in your AnyLogic8.9PLE installation.
