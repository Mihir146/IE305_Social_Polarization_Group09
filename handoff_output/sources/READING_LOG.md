# Reading and retrieval log — 3 November 2026

This records this session, not the previous assistant's claimed reading. The web tool returned literal, line-numbered HTML/PDF extraction, not a generated page summary. Equations sometimes survive in arXiv HTML even when PDF fonts fail. Figure captions were read; initial raster-plot screenshot calls returned no image payload. Later local rendered-page checks are recorded below; they do not imply that every plot was digitized. No graph coordinates have been invented or digitized. Initial shell downloads failed DNS resolution; later direct downloads succeeded after the workspace permission change, as recorded below. HAL returned an access-denied challenge; PMC returned reCAPTCHA. Those restrictions were not bypassed. Open arXiv and author-deposited copies were used instead.

## Priority sources

| Paper | Actual material read in this session | Limits / remaining action |
|---|---|---|
| Kozma–Barrat 2008 | arXiv 0707.4416v1 HTML §§I–VII, equations 1–7 and captions 1–14; published PDF pp. 1–5 checked for model, threshold and figure labels | Journal PDF's Greek glyphs garbled; arXiv HTML recovers equations. Journal correctly says d₂; arXiv sentence mistakenly says d₁ for the percolation estimate. Plot-only critical w and debris exponents not transcribed. |
| Deffuant et al. 2000 | Edinburgh PDF all prose §§1–5, captions and vector-opinion section; author-uploaded ResearchGate OCR for equations and captions | Later rendered teaching-draft pages recovered the density and peak-count expressions and vector examples. Body says N=1000, Fig.1 caption N=2000. Journal typesetting not independently compared; draft inconsistencies retained. |
| Vazquez et al. 2008 | arXiv 0710.4910v2 HTML entire main text, equations 1–6, captions 1–4, notes | Only degree 4 numerical results appear in this paper. No rewire-to-random variant found. Other degrees enter mean field, not a simulated sweep. |
| Holme–Newman 2006 | arXiv physics/0603023v3 HTML §§I–V and captions 1–5 | Fig. 4 contains other k and gamma curves; exact plotted coordinates not recovered. No analytic phi_c(k,gamma) formula. |
| Sasahara et al. 2021 | arXiv 1905.03919v3 main text, Methods A–F, appendix; authors' agent.py and stopping-code excerpt in echo_chamber_dynamics.py | Empty concordant screen resolved from author code: no opinion update; post own opinion. Triad normalization in HTML appears inconsistent; do not copy as validated. Code checked by reading, not executed. |
| Hegselmann–Krause 2002 | JASSS 33-page PDF main narrative, numerical experiments, appendix theorems and references; central BC equation cross-checked with Lorenz's clear HTML | Several matrix/Greek expressions remain garbled, so not every appendix formula is verified. Main BC average and self-inclusion recovered. Random serial claim is §4.3 p.29. |
| Baumann et al. 2020 | arXiv 1906.12325v2 main text and supplementary §§I–VIII | Journal citation verified in arXiv metadata: PRL 124,048301, DOI 10.1103/PhysRevLett.124.048301. Supplement prose/caption disagree r=.65 vs .5 in lifetime figure. |
| Flache et al. 2017 | JASSS HTML main theoretical review and Frontiers, concluding discussion | Explicit extra-variance result concerns repulsive-influence models. It is not a theorem about our attractive model. No systematic numerical validation benchmark. |
| Nardini et al. 2008 | arXiv 0711.1261v1 full main text, direct/reverse VM and naming-game equations and captions | Published journal formatting not compared. Node-neighbour order can change logarithmic to exponential convergence: strong counterexample to blanket updating-insensitivity claims. |
| Gross–Blasius 2008 | arXiv 0709.1858v2 review §§I–VII and Box/caption material | Some application-model details need original cited studies for exact reproduction. Not a single specified model or universal threshold. |
| Diakonova et al. 2015 | arXiv 1411.5181 main text, homogeneous/targeted noise, six-map approximation, appendix A–C text/tables | Appendices A–C checked; notation/figure-reference errors remain; no claim of reproducing their noisy simulations. Mean-field approximation knowingly allows unavailable partners/multiedges. |
| Bail et al. 2018 | EPFL copy of published main article pp.9216–9221, including Fig.3 effects and stated limitations | Attached PDF also has 56 pages of SI; SI not fully read. Do not claim its robustness checks independently verified. Main article is empirical, not an opinion-dynamics model. |

## Additional sources and leads

| Work | Reading so far | Why it matters |
|---|---|---|
| Kan, Feng & Porter 2023, J. Complex Networks 11(1), cnac055 | arXiv 2112.05856v3 §§1–5, eqs1–4, captions1–7; journal indexed full-text excerpts | Direct prior homophilic adaptive DW model. Uses a 5% major-cluster definition. Our h is not the invention of homophilic rewiring. Finite-size study also changes expected degree 10→50: confound. |
| Lorenz 2007 survey, arXiv 0707.1762v2 | Definitions1–4, §§1–5, diagrams and extensions | HK vs DW communication, finite-size effects, minor clusters, nonuniform starts, mu-dependent minor clusters, density discretization and stopping artifacts. HK .19/.22 density thresholds differ from finite N625 .25 example. |
| Newman 2006, arXiv physics/0602124 | Main article and benchmark table | Q evaluates partition against a degree-based null model. We evaluate a fixed opinion partition; we do not maximize Q or discover communities. |
| DiMaggio, Evans & Bryson 1996 | Full published pp.690–755, appendix/reference text from public university copy; selected damaged pages checked as images | No plot digitization or present-day trend inference; short-series/measurement limitations recorded. |
| Baldassarri & Gelman 2008 | Published author PDF main article pp.408–446 | Distinguishes issue partisanship from issue alignment; NES1972–2004. Full main text read; correlation and centering-year errors noted in the literature notes. |
| Balsamo et al., Inside the Echo Chamber, arXiv1906.09076v2 | Full arXiv main text; supplement not independently read | Direct precedent separating interaction dynamics and opinion polarization. |
| Pansanella, Rossetti & Milli 2022, ANS7:57 | Full main HTML; image-only algorithms/supplement not fully inspected | Adaptive algorithmic bias; slower graph dynamics need not change final opinion state. |
| Zhao, Sasahara & Chen 2026, arXiv2601.16457v2 | Full main and supplement HTML, all501 extracted lines | Temporal-path precedent; stopping-cap and uniform-homophily formula inconsistencies retained. |
| Guerra et al. 2013, DOI10.1609/icwsm.v7i1.14421 | Full10-page main PDF text, boundary score and tables2–3 | Empty-boundary and separation-versus-antagonism qualifications; no plot digitization. |
| Interian et al. 2023, DOI10.1111/itor.13224 | Partial main text through §3.6, lines0–612 | Remaining review unread. Follow primary Newman for modularity, not the questionable printed normalization. |

## Source URLs

- https://arxiv.org/html/0707.4416
- https://www.cpt.univ-mrs.fr/~barrat/PhysRevE_77_016102.pdf
- https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/dbba/2023/deffuantmixingbeliefsamonginteractingagents.pdf
- https://www.researchgate.net/publication/235737446_Mixing_beliefs_among_interacting_agents (author-uploaded text; upload date is not publication date)
- https://arxiv.org/html/0710.4910
- https://arxiv.org/html/physics/0603023
- https://arxiv.org/html/1905.03919
- https://github.com/soramame0518/echo_chamber_model/blob/master/agent.py
- https://raw.githubusercontent.com/soramame0518/echo_chamber_model/master/echo_chamber_dynamics.py
- https://jasss.soc.surrey.ac.uk/5/3/2/2.pdf
- https://arxiv.org/html/1906.12325
- https://www.jasss.org/20/4/2.html
- https://arxiv.org/html/0711.1261v1
- https://arxiv.org/html/0709.1858
- https://arxiv.org/html/1411.5181
- https://dlab.epfl.ch/teaching/spring2019/cs718/papers/bail2018exposure.pdf
- https://arxiv.org/html/2112.05856
- https://academic.oup.com/comnet/article/11/1/cnac055/7031227
- https://arxiv.org/html/0707.1762v2
- https://arxiv.org/html/physics/0602124
- https://cpi.stanford.edu/_media/pdf/Reference%20Media/DiMaggio_1996_Public_Opinion.pdf
- https://sites.stat.columbia.edu/gelman/surveys.course/BaldassarriGelman2008.pdf
- https://arxiv.org/html/1906.09076
- https://link.springer.com/article/10.1007/s41109-022-00495-7
- https://arxiv.org/html/2601.16457

## Important deductions to carry into the project

Our own algebra: symmetric pair averaging conserves mean, and changes population variance by -2*mu*(1-mu)*(xi-xj)^2/N. Rewiring leaves opinions fixed. Thus variance cannot increase in this model. Multimodality and disconnection can increase while variance falls. This is an elementary invariant, not a new research theorem.

Mapping: project phi=w/(1-w), w=phi/(1+phi), only w<=.5 is reachable with a project probability phi<=1. KB's w=.9 must use KB's separate update scheduler. Times in sweeps also differ by factor 1-w. Isolate protection is unnecessary for conserving edge count; replacing one edge by one already conserves it. Protection creates blocked discordant dyads, potentially causing permanent censoring under the old frozen() predicate. Diagnose these separately from slow dynamics.

Observed so far: accelerated engine reproduced all 2790 saved runs/KPIs exactly; 707 were originally censored. At 30000 sweeps 522 of those remain flagged; D, k=8/16, phi=.005 changes from S≈1 to S≈.57. All522 remaining saved states have nonfreezing proofs:520 unmatched-agent cases and2 remaining blocked cases. The full isolate-allowed primary2790-run grid has0 capped runs at30000. See stall_audit.csv and results_primary.csv. HK N625 100 reps: epsilon=.01 mean37.92 clusters; .15 mean2.66; .20 Pcons=.03; .25/.30 Pcons=1. All source results remain in raw CSV.

## Product-launch sources added during the four-hour build

- Delre et al.2007: literal author PDF main text, tables, captions and Appendix A read,954 extracted lines. Parameter/timing inconsistencies are preserved in product notes.
- Delre et al.2010: author PDF1354 lines. Main model/experiments/conclusions read across overlapping extracts, but visible coverage of lines695–745 remains incomplete; repeat requests timed out. Eq.3 typography partly garbled. Status remains partial.
- Kempe, Kleinberg & Tardos2003: author PDF1101 lines, complete main text, proofs, experiments, extensions and references read through overlapping extracts. High-degree heuristic is distinguished from marginal-gain greedy selection; their guarantee is not applied to our profit objective.
- Bass1969: publisher metadata/abstract confirmed, including the publisher's unusual title wording; located14-page scan returned zero text. Abstract-level only. No Bass fit or replication.
- Actual AnyLogic8.9.10 public Agent/shape APIs became locally available; revised source compiled against them. GUI launch from the managed workspace could not connect to the desktop. Student-supplied actual revised run screenshot and exports subsequently checked separately.

## Direct PDF follow-up after network access became available

- Delre2010 author PDF downloaded directly (340,517 bytes); complete main text/references extracted locally with pdftotext. The previously missing social-influence/uncertainty discussion is now read. Rendered p.271 inspected: Eq.3 is q_g^gamma/(q_g^gamma+p_i^gamma), gamma50. Direction affects adoption utility but not information exchange in their directional variant (p.279).
- Deffuant teaching/author PDF downloaded directly (1,142,884 bytes); full text read and draft pp.3–5 and9 inspected as images. Printed density expression and p_max heuristic recovered; journal typography not separately checked. Vector m13/d3/d2 examples and inconsistent radius/diameter statement recorded rather than silently corrected.
- Bass scan and a public university-hosted DiMaggio PDF are now downloaded to temporary reading storage. They are not yet upgraded to full-read status; OCR/read progress is recorded separately. Copyrighted source PDFs are not added to the public repository.

- Bass1969 follow-up: all13 article pages plus scan cover read via Tesseract OCR (29,076 extracted characters). Rendered journal pp.217–218 and225 inspected, recovering central hazard, cumulative-adoption and peak equations and the historical color-TV forecast. Some regression table cells/discrete-bias typography remain OCR-uncertain and are not copied as verified. No Bass model is added to the project.

- DiMaggio1996: a public University at Buffalo copy downloaded successfully after the Stanford TLS failure. Read journal pp.690–755, including appendix tables and references; visually checked Figure1 and damaged body paragraphs on pp.734/737. Rotated plots are not digitized and uncertain OCR coefficients are not copied. Historical survey period and heuristic significance conventions are explicit in the notes.

## Final direct-page follow-up

HK published PDF pp.30–33 were inspected as images: FJ matrix solution, time-varying contraction lemma/Theorem4, confidence-chain Theorem5, cluster-stabilization Theorem6, and reference pages. Earlier garbled extraction is not treated as a proof. Some earlier appendix typography remains unchecked. Source PDFs/OCR stay in temporary storage; the public repository contains source links, hashes and reading scopes, not redistributed articles.
