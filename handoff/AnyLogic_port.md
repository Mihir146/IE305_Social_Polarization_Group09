# AnyLogic port: Java code for the reference model

**Status: written against the AnyLogic API docs, NOT compiled or run in AnyLogic** (AnyLogic is not available in the AI workspace). Expect small fixes. Test each function on a tiny population (N = 10) before scaling. Items marked `VERIFY` are API details to confirm in your AnyLogic version.

The Python reference (`sim/model.py`) is the oracle: your AnyLogic output must match its statistics (not its exact numbers, since random streams differ).

## 1. Project structure

- **Agent type `Person`**: variable `opinion` (double). No parameters needed.
- **Agent type `Main`** (holds the population):
  - Parameters: `N` (300), `k0` (8), `d` (0.2), `mu` (0.3), `phi` (0.25), `h` (1.0), `maxSweeps` (3000), `initMode` (0 uniform, 1 centred, 2 bimodal)
  - Population: replicated object `people` of type `Person`, initial number = `N`
  - Set the *Connection network type* of `Main` to **User defined**, so no links are created automatically
  - Variables: `int sweep`, `boolean censored`
  - Cyclic event `sweepEvent`, mode Cyclic, first occurrence at time 1, recurrence 1 time unit
- **Experiment**: Simulation experiment for building and debugging; then a custom or Parameters Variation experiment (see plan) for the runs.

## 2. Main > On startup

```java
sweep = 0;
censored = true;
// random graph with exactly N*k0/2 edges (same as Python reference)
int m = N * k0 / 2, added = 0;
while (added < m) {
    int a = uniform_discr(0, N - 1);   // VERIFY: inclusive bounds
    int b = uniform_discr(0, N - 1);
    if (a == b) continue;
    Person pa = people.get(a), pb = people.get(b);
    if (!pa.isConnectedTo(pb)) { pa.connectTo(pb); added++; }
}
// initial opinions
for (Person p : people) {
    if (initMode == 0) p.opinion = uniform();
    else if (initMode == 1) {            // centred: median of three uniforms ~ Beta(2,2)
        double u = uniform(), v = uniform(), w = uniform();
        p.opinion = Math.max(Math.min(u, v), Math.min(Math.max(u, v), w));
    } else {                             // bimodal around 0.25 / 0.75
        double c = randomTrue(0.5) ? 0.25 : 0.75;
        p.opinion = Math.min(1.0, Math.max(0.0, c + 0.08 * normal()));  // VERIFY normal() = N(0,1)
    }
}
```

## 3. Main functions

**`void step()`** (one activation):

```java
Person i = people.get(uniform_discr(0, N - 1));
int deg = i.getConnectionsNumber();
if (deg == 0) return;
Person j = (Person) i.getConnectedAgent(uniform_discr(0, deg - 1));
double dd = Math.abs(i.opinion - j.opinion);
if (dd < d) {
    double xi = i.opinion, xj = j.opinion;
    i.opinion = xi + mu * (xj - xi);
    j.opinion = xj + mu * (xi - xj);
} else if (randomTrue(phi)) {
    if (j.getConnectionsNumber() > 1) {          // forbid cuts that would isolate j
        Person k = pickPartner(i);
        if (k != null) { i.disconnectFrom(j); i.connectTo(k); }
    }
}
```

**`Person pickPartner(Person i)`**:

```java
boolean similar = randomTrue(h);
java.util.ArrayList<Person> cand = new java.util.ArrayList<>();
for (Person k : people) {
    if (k == i || i.isConnectedTo(k)) continue;
    if (!similar || Math.abs(k.opinion - i.opinion) < d) cand.add(k);
}
if (cand.isEmpty() && similar) {                 // fall back to any non-neighbour
    for (Person k : people) if (k != i && !i.isConnectedTo(k)) cand.add(k);
}
if (cand.isEmpty()) return null;
return cand.get(uniform_discr(0, cand.size() - 1));
```

**`boolean frozen()`**:

```java
double eps = 1e-3;
for (Person a : people)
    for (Person b : a.getConnections()) {
        if (a.hashCode() > b.hashCode()) continue;   // each edge once; VERIFY or use an index instead
        double dd = Math.abs(a.opinion - b.opinion);
        if (dd < d) { if (dd > eps) return false; }
        else if (phi > 0) return false;
    }
return true;
```

Tip: if `getConnections()` returns a typed list that complains about casting, write `for (Agent bAgent : a.getConnections())` and cast to `Person`.

## 4. Event `sweepEvent` action

```java
for (int s = 0; s < N; s++) step();   // one sweep = N random activations (random sequential updating)
sweep++;
if (sweep % 10 == 0 && frozen()) { censored = false; finishSimulation(); }
if (sweep >= maxSweeps) finishSimulation();
```

(This is the same update scheme as the Python reference. It replaces the Poisson-clock wording in the blueprint: N random activations per time unit is the standard discrete-time equivalent.)

## 5. KPI functions

**`double[] kpis()`** returns `{components, giantFrac, isolatedFrac, K, crossFrac, Q, opinionVar}`:

```java
int n = N;
java.util.HashMap<Person,Integer> idx = new java.util.HashMap<>();
for (int q = 0; q < n; q++) idx.put(people.get(q), q);

// components (BFS)
int[] comp = new int[n]; java.util.Arrays.fill(comp, -1);
java.util.ArrayList<Integer> sizes = new java.util.ArrayList<>();
for (int s = 0; s < n; s++) {
    if (comp[s] != -1) continue;
    int c = sizes.size(), cnt = 0;
    java.util.ArrayDeque<Integer> dq = new java.util.ArrayDeque<>();
    dq.add(s); comp[s] = c;
    while (!dq.isEmpty()) {
        int u = dq.poll(); cnt++;
        for (Person v : people.get(u).getConnections()) {
            int vi = idx.get(v);
            if (comp[vi] == -1) { comp[vi] = c; dq.add(vi); }
        }
    }
    sizes.add(cnt);
}
int giant = 0, iso = 0;
for (int sz : sizes) { giant = Math.max(giant, sz); if (sz == 1) iso++; }

// opinion clusters: sort, split at gaps > 0.05, keep clusters with >= 5% of agents
Integer[] ord = new Integer[n];
for (int q = 0; q < n; q++) ord[q] = q;
java.util.Arrays.sort(ord, (a, b) -> Double.compare(people.get(a).opinion, people.get(b).opinion));
int[] lab = new int[n]; int cl = 0; lab[ord[0]] = 0;
for (int t = 1; t < n; t++) {
    if (people.get(ord[t]).opinion - people.get(ord[t-1]).opinion > 0.05) cl++;
    lab[ord[t]] = cl;
}
int[] csz = new int[cl + 1];
for (int q = 0; q < n; q++) csz[lab[q]]++;
int K = 0; for (int sz : csz) if (sz >= 0.05 * n) K++;

// edges, cross-cluster fraction, modularity of the opinion-cluster partition
int m = 0, cross = 0; double[] inside = new double[cl + 1], dsum = new double[cl + 1];
for (int q = 0; q < n; q++) {
    Person a = people.get(q);
    dsum[lab[q]] += a.getConnectionsNumber();
    for (Person b : a.getConnections()) {
        int bi = idx.get(b);
        if (bi > q) { m++; if (lab[bi] != lab[q]) cross++; else inside[lab[q]]++; }
    }
}
double Q = 0;
if (m > 0) for (int c2 = 0; c2 <= cl; c2++) Q += inside[c2] / m - Math.pow(dsum[c2] / (2.0 * m), 2);
double mean = 0, var = 0;
for (Person p : people) mean += p.opinion; mean /= n;
for (Person p : people) var += (p.opinion - mean) * (p.opinion - mean); var /= n;
return new double[]{ sizes.size(), giant / (double) n, iso / (double) n, K, m > 0 ? cross / (double) m : 0, Q, var };
```

**`int edgeCount()`**: `int m = 0; for (Person p : people) m += p.getConnectionsNumber(); return m / 2;` (record at start and end; they must be equal.)

## 6. Logging each run

On simulation end (experiment "After simulation run" or in `onDestroy`), write one CSV row: `rep, seed, N, k0, d, mu, phi, h, initMode, sweeps, censored, edges_start, edges_end, kpis...` with the same column names as `sim/results.csv` so the Python analysis script can read AnyLogic output unchanged.

## 7. Seeds

Use a **fixed seed per replication** (Simulation experiment: *Randomness → Fixed seed*; for batch runs set the seed from the replication counter; `VERIFY` the exact API for setting seeds programmatically, e.g. `getEngine().setSeed(...)` or the experiment's `setRandomSeed`/`setCustomSeed` depending on version). Record the seed in the CSV.

## 8. Verification checklist (do these before any experiment)

1. N = 10, k0 = 2, print `edgeCount()` before and after 100 sweeps with φ = 1: must be equal.
2. KPI function on a hand-drawn 6-node graph with two components: components = 2, giantFrac = 0.5 (or whatever you drew).
3. φ = 0, 10 replications each at d = 0.1, 0.2, 0.3: mean K should be about 4, 2, 1 and S = 1 (Python reference: 3.8, 2.0, 1.0).
4. φ = 0.25, h = 1, d = 0.2, 10 replications: S about 0.6, K about 2, cross-cluster edge fraction about 0 (Python reference: S 0.59, K 2.0, cross 0.000).
