# Live network animation — separate, reversible model

## Which file to open

- **New animation:** `CampusProductLaunch_LiveNetwork.alp`.
- **Approved fallback:** `CampusProductLaunch.alp`.

The fallback is preserved byte-for-byte. Open it to roll back; no Git operation or data deletion is necessary. Its verified SHA-256 is `2762e98ce1b432139fcf5b896f8deb3f6b2a87718a9990b5f32bb1bf2b840759`.

The live-network version uses the same Java customer kernel, random streams, policy mapping and period-end purchases. It does not change the financial experiment to make a prettier animation.

## What to watch

Every node is one of 300 Consumer agents. The three clouds are the known initial social groups. Positions are a display layout, not an opinion axis or a physical map.

| Visual | Meaning |
|---|---|
|Node fill gray / amber / purple / green|Unaware / informed nonowner / free recipient / paid owner|
|Blue participant halo|Customer involved in the highlighted recent meeting|
|Thin solid cyan discussion tie|Endpoint beliefs differ by less than the confidence tolerance|
|Thin dotted gray discussion tie|Endpoint beliefs are too far apart to average|
|Bright blue line and participant halos|A recent actual meeting, with before/after opinions below|
|Orange line|A recently formed contact after actual rewiring; it briefly persists for visibility|
|Gold and green history curves|All aware customers and paid buyers over completed campaign periods|
|Current-opinion histogram|All 300 current beliefs, including unaware customers; bin counts are exported|
|Decision panel|Aware nonowners split into insufficient budget, insufficient perceived value, or ready for the next period-end purchase|

The current design uses a white background and a larger network, with compact plots below. Individual opinions appear in the highlighted conversation and the distribution plot. All 1,200 discussion ties are drawn. Line style shows compatibility, not an empirical measure of friendship strength. A compatible edge does not guarantee both endpoints know the launch or that they are the pair currently meeting.

The animation advances ten attempted interactions per visual tick. It highlights one recent meeting periodically so the caption can be read. All attempts still affect the simulation. The last orange edge can remain visible briefly even after another meeting happens; it is labeled recent, not current. Pause the model to inspect a conversation.

## Checks completed before requesting an engine run

- Actual AnyLogic 8.9.10 Agent/ShapeGroup/ShapeLine/ShapeOval APIs compile with no errors.
- The animated default and 180 batch cases match the old standalone Java reference in every summary field except cohort/runtime.
- There are 300 distinct customer state references and 1,200 displayed actual edges at the default start and end.
- Every campaign emits 61 extra metric rows. Histogram bins sum to 300; compatible plus discordant edges sum to 1,200; buying-reason categories partition the aware nonowners.
- The approved fallback file remains unchanged.

These checks use API compilation and stand-in wiring. **The live-network editor import, engine animation and performance still need the first actual run.** They are not inferred from the successful fallback run.

## One first engine check

Open the new `.alp` in AnyLogic, keep `policyIndex=6`, `rep=1000`, and run Simulation. Let the animation progress and finish. Expected final totals remain **300 aware, 148 paid buyers, 12 samples and Rs19,200 profit**. Check that the network, history curves and histogram are visible; preserve the exact error if not.

Output defaults to `product_network_output`. Existing summary and trajectory schemas are unchanged. A new `network_metrics/policy6_rep1000.csv` provides period, compatible/discordant edges, aware nonowners, disjoint buying reasons and ten belief-bin counts. The existing ingestion/comparison script can collect its `summary/` folder normally.

The automatic batch remains policyIndex36, animateNetwork=false and virtual time. It is optional after the first live-network run succeeds; do not run unnecessary duplicate tests.
