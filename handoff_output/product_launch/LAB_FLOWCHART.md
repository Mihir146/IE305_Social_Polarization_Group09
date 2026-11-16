# Explicit decision-block model

**Open `CampusProductLaunch_LabFlowchart.alp`, then double-click Main.** Conversations are at the top; the buying/experience flow is below; the existing network animation is underneath. Eight native Variables and four parameters are at the right. The previous revision is preserved in `revision_archive/lab_flowchart_before_explicit_decisions/`; original tested grid/network files are unchanged.

## What changed?

| Item | First version | Current version |
|---|---:|---:|
|Real process-library blocks|11|33|
|SelectOutput decisions|4|17|
|Connected port links|14|49|
|Named Java functions|7|4|
|Customer eligibility loop|Java loop|Native flowchart loop|
|New-owner experience loop|Java loop|Separate native flowchart loop|

These components execute the decisions. The old interaction/step routines and the `shareLaunchNews`, `replaceContact`, `checkPurchases` helpers are absent. No separate Java routine determines purchases before merely displaying them in the chart.

## 1. Conversations and contacts

Source produces one **control token**, not a new customer. The permanent population remains300 Consumer agents. A Delay advances an encounter. Actual SelectOutput blocks check contact availability, whether either/both people are aware, sharing success, belief compatibility, whether to replace a tie, random/similar replacement, availability of similar candidates, and fallback to any permissible candidate.

The averaging branch contains the two belief assignments. The news action marks the newly aware person. The replacement action changes adjacency entries and degree counts. Neighbor/candidate scans still require short functions: ordinary palette blocks do not implement our adaptive-network search directly.

All17 SelectOutput blocks use **If condition is true**. Random decisions compare the original pre-drawn uniform against its parameter. They do not draw a new library probability, which would change the random sequence. Predicates, assignments and counters remain short expressions in Properties, as in lab models.

## 2. Buying and experience: two separate passes

`beginBuying` resets the cursor and clears the new-buyer list. For each customer, separate blocks check:

**buyerAware → notOwner → canAfford → worthPrice**

Any failed condition routes to the next customer. Passing all four records the purchase period/value and adds that person to the new-buyer list. A real flow loop continues until all300 customers have been inspected.

Only then does another loop reveal experiences for the new buyers. The saving block records period metrics and resets the attempt count. This preserves simultaneous buying: no new owner's experience can affect another customer's eligibility during the same round.

## What remains Java?

This is not a no-code model. The four remaining named Functions contain:

| Function | Nonblank lines | Purpose |
|---|---:|---|
|chooseContact|10|Find the neighbor at the selected rank|
|findSimilarContacts|6|List non-neighbors within tolerance|
|findAnyContacts|5|List all eligible non-neighbors|
|showProgress|10|Refresh the display at the original interval|

Roughly251 nonblank lines of inherited support remain for initialization, recipient ranking, metrics, accounting checks, drawing and CSV output. That support did not become native block logic. Moving it to an external file merely to lower the visible count would not reduce dependence, so it stays self-contained and disclosed.

The eight flow variables—draws, informed, a, z, customerIndex, experienceIndex, choices, newBuyers—are actual Variable elements, not hidden declarations. There are39 nonblank lines of short block actions in total. The main improvement is replacement of procedural branching and customer/experience loops with native routing, not disappearance of all expressions.

## Behavior preserved

Same initial graph, traits, recipients, seeds and Java generator; six primitive event draws per attempt, including skips; same neighbor/candidate order and strict tolerance; same belief/awareness/tie updates;300 attempts per period;60 periods; separate eligibility and experience passes; same exported schemas and `product_lab_output` folder.

Delay0.005 paces each attempt; other Delay stages are zero-time actions, not invented customer processing times. State-changing actions use **On at exit**, before SelectOutput evaluates its route. On exit can route from stale values: see the [official routing documentation](https://anylogic.help/library-reference-guides/process-modeling-library/selectoutput.html).

## Verification and honest limits

The actual serialized graph/conditions/actions match the original kernel in **80 checks**: all36 policies on two seeds plus eight edge cases. These include no samples, no sharing, unaffordable price, no contacts, broad tolerance, frequent rewiring with almost no similar opinions, a complete graph with no replacement candidate, and high experience/sharing/rewiring. All61×23 period metrics and final beliefs, awareness/purchase periods and every edge agree.

The bodies also compile against installed AnyLogic APIs. The harness traverses saved connectors; it does not merely call the original kernel. It is **not an actual PML scheduler/editor/rendering test**. A direct headless PML attempt could not initialize without a valid experiment context; no native-engine success is claimed. Earlier11-block output does not validate this expanded33-block file.

## One editor check

Close/reopen this exact file to load the33-block revision. Inspect Main and run defaults6/1000 once. Expected result: **300 aware,148 paid buyers,12 samples,Rs19,200 profit**. Preserve any exact import/compiler/runtime error. Policy36 automatic batch is not offered here.

The previous tested models and existing submission ZIP are preserved until the expanded model is confirmed. Source, Delay, SelectOutput and Sink were identified in your local A1/A2 lab handouts; copyrighted handouts are not redistributed. The file is still a hybrid agent-based network model with a process-flow scheduler, not customers arriving at a shop.
