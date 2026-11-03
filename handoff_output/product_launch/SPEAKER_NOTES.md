# Presentation speaker notes and timing

12 main slides: 12 minutes 15 seconds including a 90-second live demo. Keep 45 seconds as a buffer. Slides 13–16 are Q&A backups. Mihir presents slides 1–6; Vaibhav slides 7–12. Rehearse aloud once.

## 1. Can a smaller giveaway make a better product launch? — Mihir, 35 seconds

We model a seller launching one reusable bottle in a synthetic campus market. The question is not just how many people hear about it: it is which tested price and sample policy earns more contribution profit. We will show the individual-agent mechanism, compare policies with uncertainty, and run the model live. All inputs are generated assumptions.

## 2. The seller chooses the launch. Customers decide to buy. — Mihir, 45 seconds

Our seller chooses one of three prices and a sample policy. Random recipients, well-connected recipients and recipients distributed across groups are compared. Twelve samples were the initial fixed-spending design; three samples were a later budget-ceiling extension. We track awareness, paid sales and modeled profit separately. Inventory, repeat purchases, competitors and fixed overhead are outside this one-product campaign.

## 3. Synthetic inputs are specified, not fitted to campus data. — Mihir, 60 seconds

Each market has 300 generated customers in three groups and 1,200 contacts. Initial appeal follows Beta two two. A value scale between 500 and 1,000 rupees is separate from a budget between 400 and 1,000. Experiences are centered at 0.8 with clipped noise. This histogram is one generated market, not surveyed attitudes. We report actual generated moments and vary important assumptions rather than claiming empirical calibration.

## 4. A conversation changes beliefs. A purchase needs value AND budget. — Mihir, 80 seconds

A free recipient begins informed and receives an experience signal. An informed customer sometimes passes launch information to a contact. If their opinions differ by less than 0.2, both move 30 percent toward the other old opinion. A bigger disagreement can replace a discussion contact. After 300 attempts, informed nonowners buy if budget and perceived value both exceed price. An 800-rupee value scale times belief 0.6 is 480 rupees, so that person rejects a 500-rupee price. New owners receive their own experience. Samples never count as paid buyers.

## 5. Established mechanisms; explicit new assumptions; checked code. — Mihir, 60 seconds

Bounded confidence comes from Deffuant and related work. Kozma and Barrat already study adaptive opinion-network fragmentation. Promotional seeding and awareness/adoption models also predate this project. Our course contribution is the transparent decision comparison and mechanism diagnostic, not inventing those ideas. We checked limiting cases, purchase eligibility and accounting, matched small reference/native cases and used a separate Java implementation. The first actual AnyLogic run matched its Java reference. The revised animation and actual default export have now also been confirmed.

## 6. Compare policies on the same market; confirm on fresh markets. — Mihir, 60 seconds

The initial design has 18 policies and a separate thirty-market pilot. One hundred main markets evaluate each policy using shared initial data and aligned random draws. The three-sample follow-up reuses those main markets, so it creates more policy evaluations, not more independent populations. We then freeze four comparisons and test 100 fresh markets. Bootstrap intervals resample whole markets. They quantify simulation variability under the model and are pointwise, not a guarantee that every comparison is simultaneously correct.

## 7. Almost everyone hears. Far fewer buy at the high price. — Vaibhav, 55 seconds

Here twelve high-degree recipients and random replacement are held fixed. Mean paid sales drop from about 147 at 400 rupees to 85 at 500 and 32 at 600. Almost everyone still hears about the launch. Profit is highest at 400 within this comparison. That is why we separate awareness from conversion. This is simulated behavior under synthetic thresholds, not an estimated real-world demand curve.

## 8. Nine fewer free bottles can increase profit while reducing total owners. — Vaibhav, 65 seconds

The same 400-rupee price and degree targeting are compared on fresh confirmation markets. Three samples earn about 21,711 rupees versus 18,857 for twelve. The paired gain is 2,854.50 rupees, with interval 2,698.50 to 3,006. The seller saves 2,250 rupees on samples and sells about four extra paid units. But total owners fall by about five because nine free owners disappear. We therefore recommend against interpreting more owners as automatically more profit. Only quantities three and twelve were tested.

## 9. The sample saving is clear. The influencer premium is uncertain. — Vaibhav, 50 seconds

The targeting control holds price and sample quantity fixed. Degree targeting adds only 31.50 rupees over random selection on fresh markets, with an interval from minus 112.50 to plus 177. That is not evidence that the policies are equivalent, but it does not establish a large targeting premium. In strongly separated groups, distributed seeding helps early reach in a stress test, without a clear final-profit gain for the twelve-sample comparison. Contact recommendation effects are small and conditional; we retain their exceptions in the report.

## 10. A surprise exposes a risky assumption: very positive opinions can be ignored. — Vaibhav, 65 seconds

When experiences become more positive, our narrow-confidence model can sell fewer bottles. We kept this awkward result. On a fixed graph, raising the experience mean from 0.6 to 0.95 reduces mean paid sales from about 169 to 131 with tolerance 0.2. With all opinions compatible, it raises sales from 175 to 281. A belief of 0.5 accepts 0.6 but ignores 0.95 under the narrow cutoff. This is a model-risk diagnostic, not advice to lower actual product quality. It tells us to validate the attention mechanism before using the model for business.

## 11. Live: follow one conversation, then check the campaign accounts. — Vaibhav, 90 seconds

Switch to the saved engine-tested model. The approved grid shows opinion mini-bars and ownership colors; the separate live network shows belief as node fill and ownership as an outer ring. Follow the legend for the version actually tested. Point to a recent actual meeting and its before/after opinions. Explain that purchases occur at the end of a period. Use around two-times real-time speed and let the default finish. Check 300 aware, 148 paid, twelve samples, revenue 59,200, cost 40,000 and profit 19,200. The entire demonstration budget is ninety seconds including switching windows. If execution fails, use the saved real-engine screenshot and explicitly describe the failure.

## 12. Start small. Revisit price with cost. Validate the behavior before deployment. — Vaibhav, 70 seconds

For this synthetic baseline and tested choices, start at 400 rupees with three free bottles. Degree targeting has the largest main mean, but its confirmatory gain over random targeting is uncertain and may not pay for collecting network data. Revisit price when unit cost changes; our cost scenarios shift the best observed price. The model demonstrates a mechanism and a decision process rather than predicting a real market. We would next calibrate sharing, willingness to pay and confidence behavior, and add actual operating and targeting costs. Our source, data, scripts and actual engine evidence are included. Research and implementation were AI-assisted; we are responsible for understanding and presenting the work.

## Before entering the room

Keep the saved `.alp`, final deck, real engine screenshot and CSVs on the laptop. Open AnyLogic before your turn. Start the live demo with the tested default; do not edit code on stage. If a visual revision remains untested, use the engine-tested version and say exactly what was run. Confirm Moodle upload separately.
