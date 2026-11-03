# Handoff package manifest (3 Nov 2026)

| File or folder | What it is | Status |
|---|---|---|
| `00_AGENT_PROMPT.md` | The instruction to give the next agent | Read first |
| `02_original_brief.txt` | The students' original assignment text (IE 305 project planning and research) | Original, unchanged |
| `polarization_project_blueprint.md` | Research question, hypotheses, model spec, data plan, AnyLogic architecture, experiments, 8-week plan, references, spoken script (§11) | Patched after testing; literature rows patched after reading papers |
| `FIVE_HOUR_PLAN.md` | 5-hour execution plan, findings F1 to F7, prompts, report outline, viva questions | Patched for novelty and literature corrections |
| `LITERATURE_NOTES.md` | What each paper says, read status, corrections to earlier claims, validation against Kozma & Barrat | First thorough pass; to be upgraded |
| `AnyLogic_port.md` | Java code and setup for AnyLogic plus verification checklist | **Not compiled or run**; contains `VERIFY` items |
| `sim/model.py` | Reference model (numba): graph init, dynamics, KPIs | Tested: edge count conserved in 2,790 runs |
| `sim/run_experiments.py` | Experiment grid A to D (2,790 runs, 30 reps) | Run; about 2 min on 2 cores |
| `sim/analyze.py` | Statistics, regime classification, figures | Run |
| `sim/validate_kb.py` | Check against Kozma & Barrat setup (N = 500, 8 reps) | Run; broadly consistent, not exact |
| `sim/sanity.py` | First sanity checks | Run |
| `sim/results.csv`, `sim/results_with_regimes.csv` | Raw and classified results | Generated |
| `sim/summary.txt` | Key numbers with confidence intervals | Generated |
| `sim/fig1_expA_heatmaps.png` to `fig4_expB_selection.png` | Figures: tolerance × rewiring, regimes, mean degree, selection | Generated |

## Snapshot of key results (30 replications per scenario, N = 300, time cap 3,000 sweeps; 25% of runs censored)

- No rewiring: polarized but connected. With rewiring: opinion clusters become separate components (replicates Kozma & Barrat).
- Network threshold in φ rises with mean degree; slowing near it. Qualitative agreement with Vazquez et al.
- Similar vs random reconnection (h) changes speed, not the end state. H3 not supported. Agrees with Sasahara et al.
- High tolerance (d ≥ 0.3): consensus. Centred starting opinions weaken the effect.

## Known open items

Deffuant parameters and thresholds; Kozma & Barrat garbled equations; four abstract-only papers; Baumann journal version; AnyLogic code untested; AnyLogic licence (experiment types) unknown; KPI threshold sensitivity not run; longer-cap reruns not run.
