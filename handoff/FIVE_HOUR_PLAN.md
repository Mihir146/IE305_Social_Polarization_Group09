# 5-Hour Plan: IE 305 Simulation Lab (Mihir and Vaibhav)

**Project:** When Social Choice Creates Social Polarization (adaptive bounded-confidence model, AnyLogic)
**Date written:** 3 Nov 2026

---

## 0. Read this first

1. **Course rules.** Check what your course allows for AI help and disclose it in the report. This plan assumes AI assistance is permitted. The plan below makes sure you *understand* everything you present, which is what protects you in a viva.
2. **AnyLogic is mandatory, and the AI cannot run it.** So the work is split like this:
   - **Already done (by the AI, tonight):** a fast Python reference model, all experiments (2,790 runs), figures and statistics. This is your *oracle* and your source of results.
   - **Your job in AnyLogic:** build the model from `AnyLogic_port.md`, verify it against the Python oracle, and run a reduced set of experiments inside AnyLogic.
   - **In the report, say exactly this:** "The model was implemented in AnyLogic and independently in Python; the two implementations were cross-verified; the full experimental grid was run on the Python implementation for speed." Cross-implementation verification is a genuine strength, not a weakness, as long as you state it honestly.
3. **The AnyLogic Java code has not been compiled.** Budget time for small fixes.

---

## 1. What we already have (results you can present)

All numbers are from the Python reference: N = 300, 30 replications per scenario, time cap 3,000 sweeps. Files are in `sim_package.zip` (`results.csv`, 4 figures, `summary.txt`).

**Spec changes the testing forced (mention these, they show real V&V):**
- The blueprint said isolated agents reconnect *and* edge count is constant. These contradict each other (the test caught it: edges grew). Fix: a cut that would leave the other agent with zero links is forbidden. Edge count is now exactly conserved in all 2,790 runs, and no isolates are created.
- Time is in sweeps (N random activations per sweep) instead of a Poisson clock. Equivalent, simpler.

**Findings (each tied to a hypothesis):**

| # | Finding | Evidence | Hypothesis |
|---|---|---|---|
| F1 | **Opinion polarization and network fragmentation are different things, and rewiring converts one into the other.** Without rewiring (φ = 0) the network stays fully connected even with 2 to 4 opinion clusters, and 30 to 66% of links cross clusters ("polarized but connected"). With any rewiring, cross-cluster links drop to ~0 and the clusters become separate components (modularity 0.5 to 0.7 at d ≤ 0.2). **This reproduces Kozma & Barrat (2008), who already show each opinion cluster becoming its own component. Present it as a replication, not a discovery.** | Fig 1, Fig 2, summary.txt | H2 supported |
| F2 | **The number of opinion clusters is set by tolerance d, not by rewiring.** K barely changes with φ (e.g. 2.0 at d = 0.2 for every φ). Rewiring changes the *network*, not the opinion count. | Fig 1 left | Refines H1/H2 |
| F3 | **There is a transition in φ, and it moves with mean degree.** At d = 0.2 the network fragments at φ ≈ 0.005 to 0.01 for k0 = 4, ≈ 0.01 to 0.02 for k0 = 8, ≈ 0.02 to 0.05 for k0 = 16. Close to it, runs slow down sharply (up to 100% hit the time cap). Qualitatively consistent with Vazquez et al. (2008), whose mean-field critical rate depends on mean degree (but note their formula overestimates the simulated value, 2/3 vs ≈ 0.38 at mean degree 4, so compare only the direction). | Fig 3 | H4 supported (exploratory) |
| F4 | **Choosing *similar* contacts (h = 1) vs random contacts (h = 0) does not change how fragmented the network ends up.** It changes *speed*: h = 0 runs take longer and hit the cap more often (e.g. d = 0.15, φ = 0.25: 40% capped at h = 0 vs 0% at h = 1). Cutting disagreeing ties is what matters. **Agrees with Sasahara et al. (2021): different link rules give comparable stable states, with similarity-based rules converging over twice as fast.** | Fig 4, summary.txt | **H3 not supported** (report this honestly) |
| F5 | **High tolerance removes the effect.** At d ≥ 0.3 almost all runs end in consensus, connected, regardless of φ (fragmented in only 3 to 7% of runs at d = 0.3, 0% at d = 0.4). | Fig 1, Fig 2 | H5 supported |
| F6 | **The starting distribution matters.** With a centred start (Beta(2,2)-like) at d = 0.2, φ = 0.25: S = 0.95, K = 1.17, versus S = 0.59, K = 2.0 for uniform. So "echo chambers emerge" depends on the population starting out spread across the whole range. | Exp C | Key limitation |
| F7 | Population size (100 vs 600) and susceptibility (μ = 0.1 vs 0.5) change the results only slightly (S between 0.57 and 0.69). | Exp C | Robustness |

**Headline story for the presentation:** *We re-implemented the adaptive bounded-confidence model of Kozma and Barrat, checked it against their results, and extended it. Polarized is not the same as fragmented: tie-cutting turns a polarized-but-connected society into disconnected echo chambers once rewiring passes a threshold that rises with how connected people are. The choice of whom to reconnect to affects how fast this happens, not whether it happens (consistent with Sasahara et al.).* See `LITERATURE_NOTES.md` for what each paper says and what is and is not novel.

**Honest caveats to state yourselves (do not wait to be asked):**
- 25% of all runs hit the time cap. For those, the KPIs are a snapshot at 3,000 sweeps, not a final state. Near φ = 0.005 to 0.01 the "still connected" result for k0 = 8 and 16 may simply mean "not yet fragmented", because those runs are slowing down. Say "threshold location is approximate".
- One batch of seeds, 30 replications per scenario. Confidence intervals are in `summary.txt` for fragmentation probability.
- Everything is synthetic and stylized. No claim about real populations or platforms.
- We did not compare quantitatively with Vazquez's mean-field critical value (it is for binary opinions); only qualitative agreement is claimed.
- Not yet checked: sensitivity to the cluster-gap threshold (0.05) and the S ≥ 0.9 cutoff. Optional extra (30 minutes) if time remains.

---

## 2. Timeline (5 hours, two people)

**Mihir: model owner (AnyLogic build). Vaibhav: analysis owner (KPIs, verification, report).** Both attend the understanding block and the rehearsal. The AI is the third teammate for debugging and explanations.

| Time | Mihir | Vaibhav | Output |
|---|---|---|---|
| **0:00 to 0:30** | **Understanding block (both).** Read `FIVE_HOUR_PLAN.md` §1 and `summary.txt`. Run the Python model once (`python3 sim/sanity.py`). Use Prompt U1 and U2 below until each of you can explain the model loop in 60 seconds without notes | | Both can explain F1 to F6 |
| **0:30 to 1:30** | Build in AnyLogic: `Person`, `Main`, startup, `step()`, `pickPartner()`, sweep event (`AnyLogic_port.md` §1 to 4). Get a 10-agent version running and animated | Add KPI function (§5) and edge-count function; test KPI on a hand-drawn 6-node graph; set up the CSV logging with the same column names as `results.csv` | A running AnyLogic model |
| **1:30 to 2:15** | Scale to N = 300. Fix compile and API issues (Prompt B1). Turn animation off for runs | Run the verification checklist (§8). Compare against Python numbers. Write the V&V table with pass/fail | V&V table |
| **2:15 to 3:15** | Run the **reduced AnyLogic grid** (see below) and export CSV | Load AnyLogic CSV in Python; compare with `results.csv` on the same scenarios (mean ± CI). Make one overlay figure "AnyLogic vs reference" | Cross-verification figure |
| **3:15 to 4:00** | Take 3 screenshots of the AnyLogic network (φ = 0 vs φ = 0.25, d = 0.2; colour agents by opinion) for the slides | Write the report with Prompt R1 using the structure in §4 | Report draft |
| **4:00 to 4:40** | **Viva drill (both).** Prompt V1: AI quizzes you; swap roles | Same | Both can answer the §6 questions |
| **4:40 to 5:00** | Slides finalised, files packaged | Report proofread, citations checked against `blueprint` §9 | Done |

**Reduced AnyLogic grid (target ≈ 100 runs):** d ∈ {0.1, 0.2, 0.3} × φ ∈ {0, 0.05, 0.25} × 10 replications = 90 runs, h = 1, N = 300, k0 = 8. Plus 10 runs of h = 0, d = 0.2, φ = 0.25.

**If your AnyLogic edition has no batch or parameter-variation experiment:** run scenarios manually from the Simulation experiment (set parameters on the experiment window, run headless, log the CSV row at the end), 5 replications for the nine scenarios above (45 runs, ~20 min). State the reduced replication count honestly. The full-grid findings still come from the reference implementation.

**Fallbacks if you fall behind (cut in this order):** (1) overlay figure → table of means instead; (2) AnyLogic replications 10 → 5; (3) network screenshots → one screenshot; (4) never cut: AnyLogic model running, V&V checks, the viva drill.

---

## 3. Prompts to use (copy, paste, fill the brackets)

**U1: understanding the model** (attach `sim/model.py` and `summary.txt`)
> I'm a 3rd-year IEOR student presenting this simulation to my professor. Explain this model to me as if I must defend it in a viva. Walk through one activation step by step with a concrete numerical example (N = 5 agents, d = 0.2, μ = 0.3). Then explain, in plain words, what φ, h, d and k0 each control, and what would change if I doubled each. Do not use jargon without defining it. End by asking me 3 questions to check I understood.

**U2: understanding the results**
> Here are my results (attach `summary.txt` and the 4 figures). For each finding F1 to F6, explain (a) what the figure shows, (b) why the mechanism produces it, in plain words, (c) one way a sceptical professor could attack it, and (d) my best honest reply. Flag anything that might be a simulation artefact (for example, time-cap censoring).

**B1: AnyLogic debugging** (use every time something fails)
> AnyLogic [version] gives this error: [paste exact error text and the 10 lines of code around it]. Context: agent type Person has `opinion`; Main has a replicated population `people`; network is user-defined; I call `i.connectTo(k)`, `i.disconnectFrom(j)`, `getConnections()`. Give the minimal fix and explain why it failed. Do not rewrite unrelated code.

**B2: verification help**
> My AnyLogic model gives [numbers] for [scenario]; the reference implementation gives [numbers] (mean and CI over [n] reps). Are these statistically consistent? Show the calculation (two-sample t or comparison of CIs) and tell me what to check if not.

**R1: report writing** (give it the structure in §4, the results, and the instruction below)
> Write section [X] of the report in a clear, plain academic style, in first person plural, past tense for what we did. Use only the facts and numbers I give you; do not invent citations, numbers or results. If a claim needs a citation, use only these references: [paste blueprint §9 list]. Mark anything you are unsure of with [CHECK]. Keep it under [N] words.

**V1: viva drill**
> Act as my IE 305 professor. Ask me one question at a time about my project, starting easy and getting harder: model assumptions, parameter choices, verification, validation, output analysis, limitations, and why results might be wrong. After each answer, tell me what a strong answer would have included, then ask the next question. Do 15 questions. Be critical.

**S1: slides**
> Turn this report into a 10-slide outline: one message per slide as the title, at most 3 bullets, and name which figure goes on each slide. Do not add facts that are not in the report.

---

## 4. Report structure (about 8 to 10 pages)

1. **Problem and research question** (½ page): polarization vs fragmentation; hypotheses H1 to H5.
2. **Literature** (1 page): bounded confidence (Deffuant; Hegselmann-Krause); coevolving networks (Holme-Newman; Vazquez et al.; Kozma-Barrat); echo chambers (Sasahara et al.); caveats (Flache et al.; Bail et al.). Cite from `blueprint` §9; check Deffuant (journal details) and Baumann (journal version) before citing.
3. **Model** (2 pages): agents, network, update rule (pseudocode from blueprint §3.3), parameter table, stopping rule, the isolate-rule fix. Distinguish established vs our adaptation.
4. **Data and distribution choice** (½ page): synthetic; Uniform(0,1) is the literature convention; alternatives tested; parameters swept, not calibrated.
5. **Implementation** (1 page): AnyLogic architecture, Python reference, why two implementations.
6. **Verification and validation** (1 page): edge conservation (2,790 runs), φ = 0 reproduces bounded-confidence behaviour, KPI unit tests, AnyLogic vs reference overlay, qualitative match with Kozma-Barrat and Vazquez.
7. **Experiments and results** (2 pages): Exp A to D, Figs 1 to 4, regime table with confidence intervals.
8. **Discussion and limitations** (1 page): F4 (H3 not supported), F6 (start distribution), censoring, stylization; decision-oriented reading (rewiring rate and tolerance as levers).
9. **References.**

---

## 5. What makes this "full grade": checklist against typical simulation-lab rubrics

- [ ] Clear problem statement, objectives, hypotheses
- [ ] Conceptual model and assumptions listed
- [ ] Input modelling: distributions justified (literature convention + sensitivity)
- [ ] Verification (debugging, unit tests, conservation check) and validation (behavioural match with published findings)
- [ ] Terminating vs steady-state handled (stopping rule, censoring reported)
- [ ] Replications, seeds, common random numbers, confidence intervals
- [ ] Experimental design (factorial grid, one-at-a-time sensitivity)
- [ ] Output analysis and decision-oriented insights
- [ ] Honest limitations
- [ ] AnyLogic model demonstrably running (screenshots, live demo)

---

## 6. Viva: questions you must be able to answer (short answers)

1. **What is the model?** Agents with opinions on a network; each step a random agent talks to a random neighbour; close opinions move together; far opinions may cause the agent to cut the tie and link to someone new.
2. **Where do the rules come from?** Update rule from Deffuant bounded confidence; rewiring idea from Holme-Newman and Kozma-Barrat; our adaptation is the separate "choose similar" parameter h and the no-isolate rule.
3. **Why uniform opinions?** Literature convention, allows comparison with published results, represents a mixed population; we tested centred and bimodal. With a centred start the effect weakens (F6).
4. **Where do parameter values come from?** Swept, not calibrated. No claim they match real people.
5. **How do you know the code is right?** Edge count constant in every run; φ = 0 matches known bounded-confidence behaviour; KPI code unit-tested; AnyLogic and Python agree statistically.
6. **Why two implementations?** AnyLogic is mandatory but slow for a 2,790-run grid; Python gave speed and an independent check. We report which results came from which.
7. **What's the main result?** Rewiring converts polarized-but-connected into echo chambers; the threshold φ rises with mean degree; where people reconnect affects speed, not the end state.
8. **Which hypothesis failed?** H3. Selection of similar contacts did not change the end state. We report it as such.
9. **What are the weaknesses?** Time-capped runs (25%), single seed batch, stylized model, no extremism or repulsion, depends on starting distribution.
10. **Is this real-world evidence?** No. It shows what the mechanism can do.
11. **What would you do with more time?** Longer caps near the threshold; test thresholds; add opinion noise (Diakonova et al. show noise changes the transition); compare quantitatively with Vazquez et al.
12. **Anything you don't know:** "We haven't tested that; it's in our future work." Never guess a number.

---

## 7. Files you have

| File | What it is |
|---|---|
| `FIVE_HOUR_PLAN.md` | This plan |
| `AnyLogic_port.md` | Untested Java code and setup for AnyLogic, plus verification checklist |
| `sim_package.zip` | `model.py` (reference model), `run_experiments.py`, `analyze.py`, `results.csv`, 4 figures, `summary.txt`. Needs `pip install numba numpy pandas matplotlib scipy`; full rerun takes about 2 minutes |
| `polarization_project_blueprint.md` | Earlier blueprint and script, patched to match the tested model |
