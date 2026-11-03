# AnyLogic port and minimal verification plan

**Actual AnyLogic status: NOT compiled or run.** Documentation signatures were checked. A plain Java compiler was used with small stand-ins for the documented agent methods to catch syntax/type errors; that is **not** compilation against the AnyLogic engine and is not a runtime test. The students must save and execute the actual `.alp` model.

This version removes the need to create many Function elements. Paste one Java body into Main, then attach two actions. The Python implementation is a comparison reference, not proof that every implementation must be correct.

## 1. Build the model

1. Create an AnyLogic model with agent types `Main` and `Person`.
2. In **Person → Advanced Java → Additional class code**, paste [Person body](anylogic/Person_additional_class_code.java.txt). Do not also create Variable elements with the same names.
3. In Main create a population **people**, agent type Person, initial number **N**. Set the network to **User defined**. Startup also clears connections before explicitly generating the graph.
4. Create the Main Parameters below. These are editor Parameter elements; the supplied Java body expects their names exactly.
5. In **Main → Advanced Java → Additional class code**, paste [Main body](anylogic/Main_additional_class_code.java.txt). Do not add duplicate Variable/Function elements for names already declared there.
6. Main **On startup** action: `initializeModel();`.
7. Add a cyclic timeout Event named `sweepEvent`. First occurrence `.1` seconds; recurrence `.1` seconds. Action: `advanceSweep();`.
8. Set the Simulation experiment's model time to seconds and its stop setting to **Never**, or beyond `.1*maxSweeps+1`. An earlier experiment stop would prevent the code's final CSV export.

| Parameter | Type | Default expression |
|---|---|---|
| N |int|300|
| k0 |int|8|
| d |double|0.2|
| mu |double|0.3|
| phi |double|0.25|
| h |double|1.0|
| maxSweeps |int|30000|
| initMode |int|0|
| rep |int|0|
| exp |String|`"A"` (or B,C,D,APPLICATION)|
| allowIsolates |boolean|true|
| csvDirectory |String|`"anylogic_csv"`|

The number `.1` is an arbitrary engine-time interval: the substantive clock is the integer sweep count. One event executes N random activations. Even30000 sweeps then occupies3000 simulated seconds. This stays below the current documented PLE simulation-time limit of five simulated hours; no real behavioral time is being calibrated. See the [edition limitations](https://anylogic.help/anylogic/ui/editions.html).

For a first visible run, set N=10,k0=2. A small circle in Person can use a dynamic fill such as `new java.awt.Color((float)opinion, 0.2f, (float)(1.0-opinion))`. Enable the population's connection display. Fixed positions and identical layout settings make comparison screenshots easier to interpret. Layout is not evidence of fragmentation: use component metrics.

For longer batches, disable animation. Do not change rules while collecting results. The code's own RNG makes layout/display randomness independent of the model's draws.

## 2. What the body implements

The body matches the homogeneous Python project model: G(N,M), initial opinions after graph generation, uniform focal agent/neighbor, simultaneous old-value compromise, candidate selection before deletion, compatible-candidate fallback, optional isolate protection, gap/major-cluster KPIs and the original numerical-freezing predicate.

**Recommended setting: allowIsolates=true**, matching the primary reference and removing the proved nonfreezing trap. `false` reproduces the supplied legacy rule and is retained for sensitivity. Write these variants to their separate output folders. Neither setting changes edge-count conservation.

The original hash-code comparison has been replaced by a stable `Person.idx`. Generic connection iteration is explicit: `a.<Person>getConnections()`. The connection list is inspected but never directly modified. Dynamic links change through `disconnectFrom` and `connectTo`.

The run seed is computed **inside initialization** as `1000L+rep`; it is the exact value logged. Changing only AnyLogic's default fixed-seed option does not change this private RNG. For distinct replications, change rep. Repeating a parameter/rep combination intentionally reproduces that Java run and overwrites that combination's per-run file; it is not a new independent observation.

Java and NumPy use different generators and neighbor ordering. Identical seed labels across languages do not imply identical trajectories. Compare deterministic fixtures and replication distributions.

## 3. API audit: the former VERIFY items

| Former item | Resolution | Evidence / remaining limit |
|---|---|---|
| `uniform_discr` endpoints |Source-confirmed inclusive; port uses `Random.nextInt(bound)` instead|[Official assignment example](https://anylogic.help/advanced/code/assignment.html)|
| `normal()` standard normal |Source-confirmed mean0,SD1; port uses `nextGaussian()`|[Official normal documentation](https://anylogic.help/online/advanced/functions/normal.html). Note two-argument AnyLogic order is sigma,mean|
| `connectTo` direction/counting |Source-confirmed bidirectional; returns false for existing connection; self-connection errors|[Agent API](https://anylogic.help/api/com/anylogic/engine/Agent.html), connectTo. Do **not** connect both directions separately|
| `getConnectedAgent(index)` |Source-confirmed return type Agent; explicit Person cast supplied|Same Agent API|
| `getConnections()` typing |Source-confirmed generic `List<T>`; explicit type argument supplied|Same Agent API. Collection must not be modified directly|
| Hash-code edge uniqueness |Replaced by stable population index|Java hash codes are not guaranteed unique or meaningful graph identifiers|
| `getEngine().setSeed` / guessed seed APIs |Removed|Private documented Java RNG avoids version-dependent engine seeding calls|
| Finish/export hook |Export happens before finish, guarded once|[Execution-control documentation](https://anylogic.help/anylogic/running/controlling-model-execution.html): finish completes current event and preserves model; `onDestroy` is not a reliable finish hook|
| Custom experiment fallback in PLE |Corrected|[Experiment documentation](https://anylogic.help/anylogic/experiments/about-experiments.html): Custom requires Researcher/Professional. Use Simulation/manual runs if needed|
| Installed edition/version, property labels |**Runtime confirmation still required**|This environment has no AnyLogic installation; documentation checks cannot resolve the students' exact editor/build|
| Java engine integration |**Unverified**|Stand-in syntax compilation is not AnyLogic compilation; no `.alp` execution claimed|

## 4. CSV contract

The code writes one header plus one row per run to a parameter-specific file under:

```
anylogic_csv/no_new_isolates/cap3000/
anylogic_csv/no_new_isolates/cap30000/
anylogic_csv/isolates_allowed/cap30000/
```

The console prints the actual absolute output path. This avoids parallel experiments appending to one shared CSV. Header:

```csv
exp,rep,seed,N,k0,d,mu,phi,h,init,sweeps,censored,edges_start,edges_end,n_components,giant_frac,isolated_frac,K,cross_frac,Q,opinion_var,secs,cap,allow_isolates,stop_reason
```

`init` is the CSV name; the editor parameter is initMode. `censored` is0/1, not a Java boolean string. `secs` is wall time and must not be interpreted as model time. `sweeps` is the model clock. Metadata prevents pooling different caps or isolate rules. Header-only [schema file](sim/anylogic_schema.csv) contains no fabricated AnyLogic observations.

Example commands from `handoff_output/`:

```sh
python sim/ingest_anylogic.py anylogic_csv/isolates_allowed/cap30000 --out sim/anylogic_primary.csv
python sim/analyze.py --input sim/anylogic_primary.csv --outdir sim/anylogic_analysis
python sim/compare_anylogic.py --anylogic sim/anylogic_primary.csv --reference sim/results_primary.csv --out sim/anylogic_comparison.csv
```

For primary short D compare with `sim/primary_short_D.csv`. For the protected-isolate legacy cap3000/cap30000 compare with `sim/results.csv` / `sim/results_long_cap.csv`. Do not compare a different model rule/horizon and call the difference an implementation error. The ingestion tool checks headers, duplicate scenario/rep rows, edge conservation and cap/rule mixing.

The comparison uses bootstrap intervals for the **difference of means**, with independent resampling between languages. Inclusion of zero is a consistency diagnostic with limited power; it does not prove equivalence. The additional S-equivalence column requires the entire interval within±.05. Do not modify that margin after seeing results.

## 5. Reduced batch setup

If Parameter Variation is available, choose **Freeform**,90 runs, and leave the extra “Use replications” option **off**. The freeform run index already encodes replication. Use these root-parameter expressions:

```java
// Experiment A: 9 scenarios, 10 replications each
rep:       index % 10
exp:       "A"
d:         new double[]{0.1,0.2,0.3}[(index / 10) / 3]
phi:       new double[]{0.0,0.05,0.25}[(index / 10) % 3]
N:         300
k0:        8
mu:        0.3
h:         1.0
initMode:  0
maxSweeps: 30000
allowIsolates: true
```

These lines describe parameter-table entries, not one block to paste into Java. The official freeform interface provides `index`: [Parameter Variation](https://anylogic.help/anylogic/experiments/parameter-variation.html).

Optional20-run B batch: rep=`index%10`, exp=`"B"`, d=.15,phi=.25,h=`new double[]{0.0,1.0}[index/10]`; other parameters as above. This has matching reference B cells.

For the main horizon finding,20 runs cover two degrees, two caps and five replications: rep=`index%5`, exp=`"D"`,k0=`new int[]{8,8,16,16}[index/5]`,maxSweeps=`new int[]{3000,30000,3000,30000}[index/5]`,d=.2,phi=.005,h=1. Separate the caps when ingesting. Five replications give a small implementation check, not a precise threshold estimate.

For an optional application batch,30 runs give six policies × five replications: rep=`index%5`, exp=`"APPLICATION"`, k0=`new int[]{4,4,8,8,16,16}[index/5]`, h=`new double[]{0,1,0,1,0,1}[index/5]`,d=.2,phi=.005,mu=.3,N=300,initMode=0,allowIsolates=true. Set maxSweeps to the desired horizon and compare with `sim/application_by_horizon/cap<HORIZON>.csv`. Each horizon has a separate file. For maxSweeps=300000, set the event first occurrence and recurrence to **.01 seconds**, so the engine horizon remains3000 seconds within the documented PLE time limit; the integer sweep clock and model rules are unchanged. Ordinary A/B/D batches can retain .1 seconds.

If the installed edition lacks the chosen batch interface, set parameters and rep manually in the Simulation experiment, resetting the model for each run. Keep the exported run count honest. Do not use an unavailable Custom experiment as the fallback.

## 6. Minimal tests before scaling

Record these as pending/pass/fail with actual output. Toy outputs must stay in a separate `toy_only` CSV directory.

1. **Population/graph:** N=10,k0=2 gives10 edges, no self-links/duplicates, symmetric connections. After100 sweeps, edge count remains10.
2. **Pair update:** N=2,k0=1,d=.2,mu=.3,phi=0. Override initial opinions to .2,.3 after initializeModel; call modelStep once. Expected .23,.27, with unchanged mean. Both old values must be used.
3. **Two triangles:** N=6,k0=2. Replace the graph after initialization by triangles(0,1,2) and(3,4,5); opinions .2 for the first three,.8 for the others. Set edgesAtStart=modelEdges(). `modelKPIs()` should return **[2,.5,0,2,0,.5,.09]**. This is a hand calculation, not a stochastic expectation.
4. **Bridge fixture:** Add edge(2,3) to those triangles. Expected C=1,S=1,K=2,cross fraction=1/7,Q=5/14. This demonstrates multiple opinion groups in a connected graph. With phi=0,d=.2 those disagreeing cross-group opinions do not compromise.
5. **Stopping/export:** A compatible equal-opinion toy graph freezes numerically; exactly one row is saved. A deliberately tiny cap is flagged. Confirm the experiment's own stop time did not preempt export.
6. **Reproducibility:** Reset and repeat the same scenario/rep. All model outputs match, excluding wall-time secs. A different rep logs a different seed.
7. **Rule switch:** A degree-one dropped neighbor can lose its last link only when allowIsolates=true. Edge count stays constant under both settings.
8. **Stochastic check:** Run the reduced scenarios. Use the comparison script and inspect interval width and systematic discrepancies, rather than requiring an individual run to equal a reference mean.
9. **Horizon check:** At d=.2,phi=.005, compare3000/30000-sweep snapshots. Do not relabel capped times as observed convergence.
10. **Save evidence:** actual `.alp`, AnyLogic version, CSV, comparison table, and at least two screenshots with identical layout conventions.

The stopping predicate preserves the original numerical criterion. Under legacy isolate protection it can remain false permanently. The recommended isolate-allowed model removes that restriction; both variants and their results are named explicitly.
