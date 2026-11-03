# Understand and defend the product-launch project

## One-page explanation for a smart non-expert

Imagine a seller introducing a reusable bottle to a campus. Giving free bottles to popular people may spread the news quickly. But free bottles cost money, and a person receiving one cannot also count as a paying customer. We ask which price and sampling policy gives the best modeled campaign profit.

We create 300 synthetic customers in three social groups and connect them with 1,200 discussion ties. Each customer has an initial belief about the offer, a rupee value scale and a separate affordability limit. These inputs are generated, not surveyed. For example, someone with value scale ₹800 and belief 0.6 values the offer at ₹480. They will not buy at ₹500 even if they can afford it.

Initially only free-sample recipients know the launch. They receive a personal experience signal. During a simulated period, people meet their contacts. Information sometimes spreads. When opinions are close enough, both people compromise; a large disagreement can cause a contact to be replaced. At the end of a period, an informed non-owner buys if they can afford the price and their perceived value reaches it. Every customer buys at most once. New owners then receive their own experience signal.

We run a 60-period campaign many times because a different population and sequence of meetings produces different outcomes. The same synthetic market is used across competing policies so that comparisons are fairer. We count paid purchases separately from free samples and compute profit as revenue minus the cost of every bottle supplied.

The original experiment compares three prices, three sample-targeting rules and two discussion-contact policies with 12 free samples. A later extension compares three samples. In the main synthetic markets, price ₹400 with three degree-targeted samples has the largest observed mean profit, ₹21,945. However, its improvement over random targeting is small and uncertain. Using fewer samples has a clearer financial benefit in this setting. The sample quantity is a decision under a budget ceiling; a budget does not have to be fully spent.

The most interesting warning is that very positive experiences can sell less under a strict opinion-distance cutoff: moderate customers ignore owners who seem too different. Removing the cutoff reverses this relationship. This is a result about the model's mechanism, not advice to make worse products.

Our project is a replication-informed simulation decision study. It combines established opinion and diffusion ideas with explicit price, affordability, experience and cost accounting. It does not invent bounded confidence, influencer seeding or homophilic rewiring. The data and recommendations are synthetic. We have checked software identities and several literature mechanisms, but only a successful run in the installed AnyLogic engine verifies the required demonstration.

## 25 questions, easy to hard

1. **What decision are you helping someone make?** Choose a price and a small free-sample campaign for one hypothetical product. We compare paid sales and modeled profit over a fixed horizon.

2. **What exactly is simulated?** Individual customers, their awareness, beliefs, one-time purchases and changing discussion contacts. Interactions produce the market-level results.

3. **Why choose a reusable bottle?** It makes the one-time purchase and rupee cost examples concrete. We have not collected evidence that these particular numerical assumptions fit an actual bottle market.

4. **Where did your data come from?** From specified synthetic distributions and repeated simulations. The input CSV is an example generated market; the output CSVs are simulation observations.

5. **What does one period mean?** Three hundred random interaction attempts followed by simultaneous purchase decisions. It is not calibrated to a calendar day.

6. **What is the difference between awareness and adoption?** Awareness means knowing the launch. A person can know the offer but reject its price. Paid adoption also excludes free samples.

7. **How does someone decide to buy?** They must be informed, not already own a bottle, afford the price and value it at least that much. With value scale ₹800 and belief 0.6, perceived value is ₹480.

8. **Why is there a budget limit and a value scale?** One represents ability to pay and the other perceived worth. Both are required. Their independence is a simplifying assumption.

9. **How do opinions change?** If two informed contacts differ by less than 0.2, each moves 30% toward the other's old opinion. Beliefs 0.4 and 0.5 become 0.43 and 0.47.

10. **What happens after a disagreement?** With probability 0.05 the focal customer replaces the contact. The replacement is uniformly random at h=0 or chosen from sufficiently similar non-neighbors at h=1, with random fallback if none qualify.

11. **Does a free sample count as a sale?** No. It creates an informed owner and incurs production cost but no revenue. That person cannot later become a paid buyer in this campaign.

12. **Show the profit calculation.** At price ₹400, 148 paid buyers and 12 samples, revenue is ₹59,200. Cost is 160 bottles times ₹250, or ₹40,000. Modeled profit is ₹19,200.

13. **Why use agent-based modeling?** Who talks to whom, heterogeneous affordability and feedback from purchases matter. A single aggregate demand equation would hide these local mechanisms.

14. **What are your three targeting rules?** Random recipients, highest-degree recipients and highest-degree recipients distributed equally across three known groups. Degree gives more contacts, not extra persuasive power.

15. **What is established in the literature?** Bounded-confidence averaging and adaptive opinion networks are established mechanisms. Product-diffusion studies already distinguish information and adoption and study promotional seeding. Our financial and buying rules are additional assumptions.

16. **What is your contribution?** A transparent synthetic decision comparison joining price, sampling, experience and adaptive discussion, plus a diagnostic showing how the confidence assumption can reverse the quality effect. We claim neither an invented mechanism nor proven research priority.

17. **Why repeat every policy?** Random populations and meetings vary. We compare average outcomes and intervals across independent markets, rather than presenting one lucky run.

18. **What are common random numbers?** Competing policies use the same initial market and aligned primitive random draws. We then compare outcomes within each market. Different resulting contacts can still produce different paths, and variance reduction is not guaranteed.

19. **What does a 95% interval mean here?** It describes Monte Carlo uncertainty in an estimated mean or paired difference under the specified model. It does not include uncertainty about whether our synthetic assumptions describe reality.

20. **Are all your CSV rows independent observations?** No. Policies and periods reuse a market. We resample whole markets. There are 100 independent main markets even though 36 policy variants produce 3,600 main evaluation rows.

21. **How did you verify the implementation?** We checked hand-calculated two-person updates, zero-information and zero-sharing cases, sample accounting and graph/ownership/purchase invariants. The accelerated implementation matches the readable reference in small seeded cases. AnyLogic execution is checked separately.

22. **Did you reproduce earlier papers exactly?** Some finite-size patterns, including the HK consensus example, were reproduced. Exact KB critical values and binary-model scaling were only partially reproduced. The product purchase rules have no empirical calibration, and we do not call those tests sales validation.

23. **Why can fewer free samples make more money?** They cost less and leave more possible paying customers. In the main degree/₹400 comparison, three rather than twelve saves ₹2,250 and raises paid sales by about four. Total ownership actually falls by about five because nine free owners disappear. We distinguish these measures.

24. **Does your quality result imply a business should reduce quality?** No. It exposes the hard confidence assumption. With tolerance 0.2, a belief of 0.5 ignores a signal near 0.95 but can interact with 0.6. On a fixed graph with all opinions compatible, increasing experience quality raises sales instead. This needs behavioral validation before business use.

25. **What could invalidate your final recommendation?** Different real demand, costs, sharing, confidence behavior, campaign duration, sample quantities or targeting expenses could change it. We compare a finite candidate set. Small targeting differences are uncertain; our recommendation is conditional, not a global optimum or forecast.

For question 21, describe only the AnyLogic evidence actually collected. Until the students' engine run succeeds, say: “The independent code and Java wiring are checked; actual AnyLogic execution is still pending.” Update that sentence after saving real evidence.

## Glossary

| Term | Meaning in plain language |
|---|---|
|Agent-based model|A simulation of individual decision-makers and their interactions|
|Bounded confidence|A person updates toward contacts only when their opinions are sufficiently close|
|Tolerance d|The maximum accepted opinion difference; here the comparison is strict, less than d|
|Compromise fraction μ|How far each person moves toward the other's old opinion|
|Homophily|A preference for similar contacts; our h controls replacement selection, not the initial group graph|
|Adaptive network|Contacts change in response to the states of the people connected|
|Degree|A person's number of current contacts|
|Giant-component fraction|The share of customers in the largest connected piece of the discussion graph|
|Fragmentation|The contact graph splitting into disconnected pieces; a disconnected graph is not automatically polarized attitudes|
|Polarization|A term requiring a specified attitude/cluster measure; the product report mainly uses sales and belief summaries rather than calling every disagreement polarization|
|Echo chamber|A setting with selective, reinforcing exposure; neither group membership nor high modularity alone proves this|
|Modularity|Within-group edge concentration relative to a degree-based reference graph; used in the background study, not the primary sales objective|
|Common random numbers|Shared primitive randomness for competing policies so paired comparisons are possible|
|Replication|A separately generated stochastic market and trajectory|
|Monte Carlo uncertainty|Sampling variation from using a finite number of simulated replications|
|Bootstrap interval|An interval computed by repeatedly resampling independent markets|
|Pointwise interval|Coverage intended for one specified estimate; it does not guarantee simultaneous coverage of every comparison|
|Censoring|An event, such as a sales target, is not observed before the observation period ends|
|Verification|Checking whether code implements the chosen rules correctly|
|Validation|Checking whether the rules are useful for the intended system; literature replication and empirical validation are different kinds of evidence|
|Contribution profit|Revenue less the modeled variable costs; omitted overhead must be stated|
|Sensitivity analysis|Changing assumptions to see whether conclusions depend on them|
|Ablation|Removing a mechanism to learn which part of the model produces an effect|
|Pilot / confirmation|A pilot helps choose a policy; a separate confirmation tests fixed comparisons without searching again|
|Synthetic data|Generated observations under explicit assumptions, rather than measurements of real people|
