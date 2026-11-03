# Literature behind the product-launch application

**Reading honesty:** this supplement adds marketing sources to the detailed parent review. “Full main text” means literal HTML/PDF text and captions read, not independent visual digitization of every plot. Garbled equations and incomplete sections remain marked. The source papers are linked rather than redistributed. **L** = literature; **A** = our assumption; **R** = our own simulation result.

## 1. Read-status table

| Source | What was actually read | Remaining limit |
|---|---|---|
|Deffuant et al. 2000|Full teaching/author draft; central printed mathematics now checked from rendered PDF pages|Journal typesetting not compared separately; draft inconsistencies recorded in parent notes|
|Kozma & Barrat 2008|Full arXiv main text; journal PDF notation cross-check|Plot-only coordinates not digitized|
|Delre, Jager, Bijmolt & Janssen 2007|Full author PDF, main text and Appendix A, including tables/captions|Several body/appendix parameter and timing inconsistencies; not silently repaired|
|Delre, Jager, Bijmolt & Janssen 2010|Full author PDF main text/captions/references, with missing section recovered by direct PDF extraction; Eq.3 inspected visually|Plots not digitized; Eq.3 now resolved exactly|
|Kempe, Kleinberg & Tardos 2003|Full 10-page author PDF main text, proofs, experiments, extensions and references, literal extraction lines 0–1101 across overlapping reads|No plot digitization or reproduction of their greedy algorithm. Some long mathematical typography is difficult; no claim to verify every proof algebra symbol|
|Bass 1969|Complete 13-page main article/references via local Tesseract OCR of the 14-page public scan; central equations and selected tables inspected as images|OCR has errors in some table cells and discrete-bias algebra; those values are not silently transcribed. No model fit/replication attempted|
|Other opinion/network sources|See the parent table for all twelve priority papers and additional readings|A survey citation does not imply reading all of its cited papers|

Local OCR and rendered-page inspection now resolve the main Bass reading gap. Direct PDF access after the workspace permission change resolved the missing Delre2010 segment and Eq.3. No paywall or access challenge was bypassed.

## 2. The foundations we actually use

**L — bounded-confidence compromise.** Deffuant, Neau, Amblard & Weisbuch, *Mixing beliefs among interacting agents*, **Advances in Complex Systems 3**, 87–98 (2000), is the source of the simultaneous pairwise opinion update. We use a strict confidence condition and μ=0.3. Their model does not provide our rupee valuation, awareness, experience or purchase rule. [Author-hosted teaching copy](https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/dbba/2023/deffuantmixingbeliefsamonginteractingagents.pdf).

**L — adaptive contacts.** Kozma & Barrat, *Consensus formation on adaptive networks*, **PRE 77, 016102** (2008), DOI [10.1103/PhysRevE.77.016102](https://doi.org/10.1103/PhysRevE.77.016102), studies closely related continuous opinions and changing ties. The random-reconnection baseline is direct prior work. Its scheduler differs; our original-model comparison uses the documented relative-rate mapping, not an assertion of identical clocks. It contains neither product prices nor customer experience resets. [Full arXiv text](https://arxiv.org/html/0707.4416).

**A — application boundary.** These papers justify studying a stylized opinion mechanism. They do not empirically establish that a moderate bottle customer ignores a very positive owner at exactly distance 0.2. The product extension's hard confidence gate must be treated as a consequential assumption.

## 3. Direct product-diffusion work

### Delre et al. (2007)

*Targeting and timing promotional activities: An agent-based model for the takeoff of new products*, **Journal of Business Research 60(8), 826–835**, DOI [10.1016/j.jbusres.2007.02.002](https://doi.org/10.1016/j.jbusres.2007.02.002). [Full author PDF](https://www.rug.nl/staff/w.jager/delre_jager_bijmolt_janssen_jbr_2007.pdf).

**L — model and relevant targets.** Distinguishes unaware, aware nonadopters and adopters; adopters inform neighbors. Adoption combines individual and social threshold components on a small-world network. The reported main setup includes N=3,000, twenty runs and 500 steps. Figure 5 compares promotional arrangements of 120 initial recipients: forty groups of three performs best in that setting. Figure 4's reported random-seeding takeoff scale is setting-dependent, not our universal sample requirement.

**Limit and relevance.** Distributed/cohesive seeding and campaign timing are established prior art. Our platform also allows aware nonbuyers to inform contacts and uses price/value/budget accounting. The paper does not validate those additions. Appendix/body β conventions and a Figure 7 campaign-rate caption differ; one timing table is difficult to reconcile. We preserve these discrepancies rather than use those rows as exact numerical benchmarks.

### Delre et al. (2010)

*Will It Spread or Not? The Effects of Social Influences and Network Topology on Innovation Diffusion*, **Journal of Product Innovation Management 27, 267–282**, DOI [10.1111/j.1540-5885.2010.00714.x](https://doi.org/10.1111/j.1540-5885.2010.00714.x). [Author PDF](https://www.rug.nl/staff/w.jager/delre_jager_bijmolt_janssen_jpim_2010.pdf).

**L — verified parts.** Informed agents evaluate utility combining individual preferences and the fraction of adopting neighbors; adoption requires a utility threshold. Initial free adoption is 0.5%. Only adopters propagate information. Static lattice/scale-free network variants examine social susceptibility and hub constraints. Figure 3 uses N=900 and thirty runs; the main factorial study uses N=100,000, 900 steps and at least thirty runs per condition. Their h is a hub/network parameter, not our reconnection h.

**Relevance and limits.** The authors distinguish hubs' information reach from stronger persuasion. This supports testing degree as an opportunity advantage, not assigning popular customers a magical persuasion coefficient. Our model adds explicit money, adaptive opinions/contacts and personal experience. These do not follow as validated consequences. No full-model reproduction was attempted. Eq.3 is now recovered exactly from rendered p.271: `y_ig = q_g^γ / (q_g^γ + p_i^γ)`, with γ=50. At q_g=p_i>0 this individual-utility component is1/2; it is not our rupee purchase threshold. The directional-link variant changes social utility, while its information exchange remains unaffected by that direction process (p.279). No quantitative adoption target from this source was used to tune our sales results.

## 4. Seeding is a known optimization problem

Kempe, Kleinberg & Tardos (2003), *Maximizing the Spread of Influence through a Social Network*, **KDD '03**. [Full author PDF](https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf).

**L — exact scope.** Independent Cascade gives a newly active node one probabilistic attempt per inactive neighbor; Linear Threshold uses random uniform thresholds and incoming weights summing to at most one. The objective is expected activated population for a fixed seed-set size. Submodularity supports a greedy approximation guarantee in those models. Their test graph has 10,748 researchers; Figure 4 shows random targeting can surpass degree/centrality heuristics at larger seed counts in the 10% cascade setting.

**A/R — implication for us.** Our high-degree rule is a heuristic, not their marginal-gain greedy algorithm. Their guarantee is not proved for our price, profit, experience and adaptive-tie feedback. Their results support comparing structural heuristics instead of assuming one is best. We do not reproduce their influence benchmark or infer an identical ranking for bottle sales. Profit can fall when free recipients increase, so a theorem about monotone activation spread cannot simply be relabeled a profit theorem.

### Bass (1969): a distinct aggregate diffusion model

*A New Product Growth for Model Consumer Durables* (verified publisher title), **Management Science15(5),215–227**, DOI [10.1287/mnsc.15.5.215](https://doi.org/10.1287/mnsc.15.5.215). [Public scan](https://pdodds.w3.uvm.edu/files/papers/others/1969/bass1969a.pdf). Complete main text was read through local OCR; central mathematics was checked against rendered pp.217–218.

**L — model.** Conditional purchase hazard is `p+qF(t)`. Thus cumulative first purchases Y=mF obey `Y'=(p+qY/m)(m−Y)`, with Y(0)=0. This is an aggregate continuous-time model, without an explicit contact network. For q>p, p.218 gives `t*=ln(q/p)/(p+q)` and peak sales `m(p+q)²/(4q)`. These are possible analytical checks for a Bass implementation, which we have not implemented. Table5 forecasts a1968 color-TV peak of6.7 million units; it is a historical forecast, not our result.

**Limits/relevance.** The article concerns initial purchases of new generic product classes, distinguishes them from new brands/models, excludes replacement sales in its fitted intervals, and warns that sparse early data yield unstable parameters. It also distinguishes ex-post fitting from forecasting. Our bottle campaign is an individual-agent scenario, not an estimated Bass forecast. No Bass coefficients, fit or approximation guarantee are claimed. OCR-damaged table cells and discrete-bias algebra remain untranscribed rather than guessed.

## 5. Application claim-verification table

| Claim used in report/slides/viva | Status | Boundary / source |
|---|---|---|
|Similar opinions can be modeled with simultaneous pairwise compromise|**confirmed**|Deffuant pair rule; its use for product appeal is A|
|Adaptive continuous-opinion networks predate our project|**confirmed**|Kozma–Barrat full model; replication credited|
|Opinion fragmentation and graph disconnection require separate definitions|**confirmed**|Parent literature review; not every disconnected network is polarized attitudes|
|Product-diffusion models distinguish information and adoption|**confirmed**|Delre 2007 and verified 2010 model sections|
|Promotional recipient arrangement and timing have prior work|**confirmed**|Delre 2007; distributed seeding is not our invention|
|A highly connected person need not have extra persuasive power|**confirmed**|Delre 2010 examines reach versus influence; not a universal empirical assertion|
|Highest-degree targeting is globally optimal|**corrected**|Kempe distinguishes degree heuristics from greedy influence maximization; our comparisons do not establish this|
|Our profit optimizer inherits a 63% approximation guarantee|**corrected**|No submodularity or corresponding guarantee proved for this model|
|The three-sample policy is best among every possible policy|**corrected**|Only a finite tested set; exploratory selection and fresh fixed comparisons identified|
|A strict 0.2 confidence cutoff is calibrated customer behavior|**unverifiable**|No product behavioral data; A rather than L|
|All informed people, including nonbuyers, share launch news|**confirmed**|Our specification/code; Delre owner-only information propagation|
|Price/value/budget and experience rules are jointly validated by prior papers|**corrected**|New application assumptions; mechanism verification is not empirical sales validation|
|The quality reversal is established marketing fact|**corrected**|R from our diagnostic CSVs; a model-risk finding|
|The Java reference grid was executed in AnyLogic|**corrected**|Separate implementations. Actual engine export count is recorded independently|
|Our model was fitted to Bass diffusion|**corrected**|Full main text is now read; still no Bass fitting or benchmark implemented|
|Every equation in every source was read cleanly|**corrected**|Read table and parent review explicitly preserve extraction gaps|

## 6. What to say about novelty

“This is a replication-informed extension for a concrete launch decision. Seeding, bounded confidence and adaptive contacts are established ideas. We add transparent financial and ownership accounting, paired policy comparisons and a diagnostic showing how a confidence assumption can reverse a quality effect. We do not establish research priority for this combination.”

The original hypothesis that similar versus random reconnection would clearly change the final opinion state failed in the background study and remains visible in the parent report. The application also keeps small or uncertain targeting effects and nonuniform contact-policy effects. A failed expectation is reported rather than removed to make a stronger sales story.
