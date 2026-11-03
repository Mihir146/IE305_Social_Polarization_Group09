> **Background opinion/contact study.** The selected final application and its current evidence are in [product_launch/](product_launch/README.md). Product sales, experience and actual product-model engine runs are separate from the mechanism results below.

# Validation report

**IE305 — 3 November 2026.** All numerical results below are synthetic simulation results. Literature replication tests check specified mechanisms; they do not validate a real population. The required AnyLogic execution remains pending.

## 1. What passed and what did not

| Check | Status | Evidence and practical limit |
|---|---|---|
| Reproduce the supplied reference outputs | **PASS** | All 2790 saved output rows/KPIs reproduced; `sim/replay_validation.csv`. This compares saved outcomes, not independently archived full trajectories |
| Accelerated versus readable reference engine | **PASS** | Five small, seeded trajectory comparisons, covering initialization modes and isolate rules; `sim/verification.csv` and `verify_native.py` |
| Structural identities and hand-calculated KPIs | **PASS** | Edge conservation, simple undirected graph, conserved mean, decreasing variance, two-triangle metrics; same verification file |
| KB static d₁≈.256 at degree10 | **PARTIAL** | N=1000,100 runs/point; transition in the expected neighborhood, but no precise critical-point reproduction; §3 |
| KB d₂≈1/(2k̄) | **PARTIAL** | Communication-path clusters, three sizes and three degrees support the inverse-degree scale; no finite-size critical-point fit; §3 |
| KB d₁ shifts with rewiring w | **PASS for direction; PARTIAL for critical values** | Largest-opinion-cluster crossover moves to higher d with larger w; eight w=.9 runs remain capped |
| HK complete-population benchmark | **PASS for the published finite-N pattern** | N=625;100 runs each at five tolerances; all runs reach consensus at .25/.30. This is not a universal threshold estimate |
| Vazquez binary model | **PARTIAL** | Separate degree4 implementation reproduces a crossover near the published .38 region and two large pieces above it; no critical scaling fit |
| Extend every originally capped run | **PASS** | All707 extended from3000 to30000 sweeps; snapshot connectivity changes sharply at low φ |
| Diagnose persistent legacy flags | **PASS for the saved states** | All522 still-flagged states have a structural nonfreezing certificate; `sim/stall_audit.csv` |
| Recommended isolate-allowed primary grid | **PASS for numerical freezing within cap** | All2790 primary runs satisfy the numerical predicate before30000; exact mathematical absorption is not asserted |
| Measurement robustness | **PASS as a sensitivity audit** | 27 cutoff combinations on the same1440 A states; minority-size cutoff matters more than the other individual changes |
| AnyLogic compilation, runtime and output comparison | **PENDING** | API audit and paste-ready code exist. A local Java syntax check used stand-in API classes; it is not an AnyLogic test |

## 2. Model variants and reproducibility

The **legacy** process protects a dropped neighbor's last tie and caps runs at3000 sweeps. `results.csv` is the unchanged supplied output. `results_long_cap.csv` replaces only the originally capped rows with their30000-sweep follow-up. It retains the same isolate protection.

The **recommended primary** process allows isolates. `results_primary.csv` repeats the full matched2790-run grid with cap30000. `primary_short_D.csv` supplies matching3000-sweep snapshots for the630 D runs. Changing the isolate rule is a documented model revision, not a retroactive claim that the original results used this rule. Both variants conserve the number of edges.

Initialization, factors and replication seeds are in every raw CSV. Project replications use seed1000+rep; dedicated KB, HK and binary checks use separate seed ranges recorded in their drivers. At fixed N,degree and initialization, policy comparisons start from the same population. Across different N or degrees, graph generation consumes a different number of random draws, so equal seed labels do not imply identical starting opinions.

The acceleration engine imports NumPy's MT19937 state after the original initialization and preserves the reference draw/update order. It uses no fast-math optimization. The readable Python model remains the specification. Native acceleration requires NumPy and a C++17 compiler; the reference can instead use numba when installed. Analysis tables require NumPy; Matplotlib is optional for PNG export.

New intervals use10000 percentile-bootstrap resamples, fixed seed20261103, for means and paired differences. Proportions use95% Wilson intervals. These are pointwise Monte Carlo intervals, with no multiple-comparison correction. A zero count in30 trials still has an upper Wilson bound about.114. Reused initial seeds across different experiments must not be pooled as independent replications.

## 3. Quantitative literature checks

### Kozma & Barrat

Published targets and figure locations are in `LITERATURE_NOTES.md` §1.1. We implement their separate scheduler, μ=.5, random reconnection h=0, isolates allowed, numerical tolerance10⁻⁵ and communication-path clusters. A path cluster is a connected component after deleting discordant edges. Sorted-opinion gaps cannot substitute for this at tiny d.

The project scheduler uses φ only after disagreement. The relative-rate mapping is φ=w/(1−w), with clocks related by t_project=(1−w)t_KB. A project probability φ≤1 covers only w≤.5. The dedicated scheduler is therefore necessary for w=.9.

**d₁ and rewiring:**3600 runs: N=1000,k̄=10; w=0,.1,.5,.9; d=.24,.25,.256,.26,.27,.28,.30,.32,.35;100 replications each, cap30000. At w=0,d=.256 the mean largest path-cluster fraction is.7134,95% interval[.6693,.7579]. The probability that this fraction is at least.9 is.40. It becomes.47 at d=.26 and.78 at .27. Our first grid crossing of50% is therefore(.26,.27], using **our own operational crossing definition**, not the authors' critical-point definition.

The same50% crossing lies in(.26,.27] for w=.1, (.27,.28] for w=.5, and(.30,.32] for w=.9. This reproduces the direction of the rewiring shift. It does not reproduce precise published d₁(w) values. Eight of900 w=.9 runs are capped; their KPIs are snapshots and their final state is uncertain. Random-graph ensemble, finite N and numerical stopping differences remain material. We do not report d₁=.256 as an exactly reproduced constant.

**d₂:**810 runs: N=500,1000,2000; k̄=10,20,30; d=.6,1,1.4 times1/(2k̄);30 replications each. For k̄=10 below the heuristic threshold, mean largest path-cluster fraction falls .0333→.0259→.0213 as N grows. Above it, fractions are .2019,.2150,.2126. This is consistent with subextensive versus extensive clusters around the predicted scale. Other degrees show the same qualitative separation. A fitted limiting threshold or exponent is **not established** by three points and three sizes.

Source files: `kb_validation.csv` and `kb_summary.csv`; driver `run_validation.py --part kb`. The4410 KB runs are separate from the project grid.

### Hegselmann–Krause

Separate synchronous, self-inclusive averaging over the complete population; N=625, independent uniform initial opinions,100 replications/tolerance, numerical tolerance10⁻¹⁰, cap10000 iterations. No rewiring or Deffuant pair updates enter this benchmark.

| ε | Mean final opinion clusters | Consensus observations |
|---|---:|---:|
|.01|37.92|0/100|
|.15|2.66|0/100|
|.20|1.97|3/100|
|.25|1.00|100/100|
|.30|1.00|100/100|

All500 runs stabilize numerically. HK Fig.2 reports38-cluster, two-camp and consensus examples at .01,.15,.25; its .15 example is **two camps**, not an ensemble expectation of exactly2. Their original vector is unavailable. We reproduce the finite-N pattern and explicitly retain the different ensemble mean2.66. Other sizes and density formulations need not have the same consensus boundary. Files: `hk_validation.csv`, `hk_summary.csv`; driver `run_validation.py --part hk`.

### Vazquez, Eguíluz & San Miguel

Separate binary ±1 copying model on a uniform simple random4-regular graph. Discordance causes rewire-to-same with probability p, otherwise focal-node copying. N=1000; p=.2,.3,.35,.38,.4,.45,.6;100 replications/point. All700 runs absorb within30000 sweeps.

| p | Mean largest component fraction |
|---|---:|
|.20|.99583|
|.30|.98565|
|.35|.81091|
|.38|.59902|
|.40|.56726|
|.45|.54813|
|.60|.52819|

The crossover and approach to roughly N/2 agree with the published pattern. At p=.60 the mean second component is.47103. The coarse grid and single N do not estimate p_c precisely or test critical exponents. The paper itself explains why mean field gives2/3 rather than the simulated≈.38. Neither number validates our continuous-model φ. Files: `binary_validation.csv`, `binary_summary.csv`; driver `validate_binary.py`.

## 4. The horizon correction changes the main conclusion

For the recommended primary process, d=.2,μ=.3,φ=.005,h=1,N=300;30 replications per row:

| Initial mean degree | Mean S at3000 | Mean S at30000 (95% interval) | Fragmented observations,3000→30000 |
|---|---:|---|---|
|4|.8356|.6031[.5667,.6439]|11/30→29/30|
|8|.9986|.5761[.5484,.6102]|0/30→29/30|
|16|1.0000|.5677[.5481,.5899]|0/30→30/30|

S is the largest topological component fraction; our operational fragmentation cutoff is S<.9. These are matched paths observed at different caps, not independent short/long populations. All degree8/16 short runs at φ=.005 are capped; none of their matching long runs is capped.

Define an empirical φ₅₀ as the first tested φ at which the observed fragmentation proportion is at least.5. Its bracket shifts:

| Degree |3000-sweep bracket|30000-sweep bracket|
|---|---|---|
|4|(.005,.01]|(0,.005]|
|8|(.01,.02]|(0,.005]|
|16|(.02,.05]|(0,.005]|

These are grid brackets without threshold-confidence intervals. They do not prove a mathematical phase boundary at zero, monotonicity everywhere, or a universal degree effect. They contradict the earlier interpretation of a positive **long-run** threshold in these scenarios. Files: `primary_horizon_summary.csv`, `primary_threshold_brackets.csv`.

## 5. Isolate protection was a substantive assumption

Of707 originally capped legacy runs,522 still fail the old predicate after30000 sweeps. The saved-state audit proves why each cannot subsequently pass under that rule:

- 520 have a nonisolated agent with no compatible agent anywhere. All other opinions lie outside its confidence interval. Convex averaging on either side cannot create a compatible partner, and opposite sides cannot compromise across a gap≥2d. Its last discordant tie is protected forever.
- The remaining2 have blocked discordant dimers; every other component has opinion range<d, so no new discordant rewiring can free the blocked endpoints. Their convex hulls remain separated.

The snapshot diagnostic counts39 immediately blocked cases and520 unmatched-agent cases, with overlap37; these are **not additive categories**. The proof classification above is disjoint. `stall_audit_summary.json` records522 proved and0 unresolved for these saved states. It does not assert a theorem covering every possible initial state.

The separate1170 B/D isolate-allowed check has0 capped runs. The full recommended2790-run primary grid also has0 capped runs at30000. Thus the recommended main model allows isolates and measures their fraction. The legacy model remains available as sensitivity evidence.

## 6. Negative result and measurement sensitivity

**H3 remains unsupported in its original B comparisons.** All six paired95% intervals for h=1 minus h=0 final S include zero. For example d=.15,φ=.25 gives ΔS=.00056,[−.02556,.02456]. This is not equivalence. Here mean stopping time changes385.67→148.33 sweeps, but at d=.15,φ=1 the corresponding means115.67→147.00 do not support a universal speed advantage. Files: `primary_h3_paired.csv`.

Reclassify the same1440 primary A states using gaps .02,.05,.08; minimum sizes .01,.05,.10; and S cutoffs .8,.9,.95. Relative to(.05,.05,.9), individual changes produce:

| Changed choice | Number of A labels changed |
|---|---:|
|Gap .02 or .08|5 each|
|Minimum fraction .01|112|
|Minimum fraction .10|12|
|S cutoff .8|3|
|S cutoff .95|6|

The results are fairly stable to these gap/cutoff choices, but the minority convention matters. Across all27 combinations the largest count is122/1440. These are label changes, not altered trajectories. K=1 means one **major gap cluster**, not universal agreement; an initially diffuse distribution can also have K=1. S≥.9 means a large component, not literal connectivity. Q evaluates the opinion partition and is not proof of hostility. Files: `primary_kpi_sensitivity.csv`, `primary_sensitivity_summary.csv`.

## 7. Application and implementation limits

`APPLICATION_DESIGN.md` maps the tested process to a hypothetical discussion platform. Its contact-policy study reuses the same mechanism and records repeated snapshots explicitly. It is an application of a synthetic mechanism, with no empirically calibrated clock or human parameters. The product-launch idea remains a proposed extension: no paid-purchase, revenue or profit result is claimed from opinion data.

AnyLogic documentation has been checked and CSV ingestion/analysis code is supplied. Actual API compatibility, runtime behavior, stochastic agreement, animation and installed-edition experiment support remain unverified until the students run it. Record actual version, fixture outcomes, exported seeds and `.alp` before claiming completion of the course implementation.

## 8. Reproduce the evidence

Run from this folder, with Python3, NumPy and g++ available:

```sh
python sim/verify_native.py
python sim/sanity.py
python sim/run_validation.py --part replay --workers 2
python sim/run_validation.py --part kb --workers 2
python sim/run_validation.py --part hk --workers 2
python sim/validate_binary.py
python sim/run_validation.py --part long --workers 2
python sim/run_validation.py --part isolates --workers 2
python sim/summarize_validation.py
python sim/stall_audit.py
python sim/run_primary.py
python sim/summarize_primary.py
python sim/run_application.py
python sim/trajectory_demo.py
python sim/analyze.py --tables-only --outdir sim/primary_analysis
python sim/build_figures.py
```

The KB check took much longer than the original small grid in this workspace; full regeneration is not a two-minute promise. Retain the supplied raw CSVs if only inspecting results. Rebuild presentation artifacts after regenerating their source tables.
