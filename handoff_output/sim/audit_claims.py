"""Inventory paper-citing passages in the original supplied handoff, not edited files."""
from pathlib import Path
import csv,re,hashlib,json
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parents[1]/'handoff'
PAT=re.compile(r'Deffuant|Hegselmann|Krause|Kozma|Barrat|Holme|Newman|Vazquez|Sasahara|Baumann|Flache|Bail|Nardini|Diakonova|Gross|Blasius')
BP={
63:'Discrete-opinion model; clarify the direction and their local-consensus definition; no initial-state sensitivity test.',
64:'Finite systems absorb below the transition too; other-degree dependence is mean-field, not a simulated sweep or our threshold.',
65:'Closest replication, with different clocks/isolate protection; previous gap-based check was preliminary.',
67:'Separate joint influence/segregation from reconnection-strategy sufficiency; speed is model/regime-specific.',
68:'Journal metadata now verified: PRL124,048301(2020).',
70:'Republican effect significant; Democratic effect not significant; restricted sample and intervention.',
81:'Homophilic bounded confidence and separating opinions from topology already have direct precedents.',
101:'Baseline d in the tested code is .2; no universal fragmentation-to-consensus critical d is inferred.',
141:'Synthetic study is defensible; empirical microdata can in principle inform parameters, but none were estimated here.',
148:'Separate literature-model replication from empirical validation; new quantitative benchmarks are available.',
151:'Empirical data can inform parameters as well as test patterns; none were fitted here. Sasahara uses an empirical stopping target, not independent validation.',
233:'Network unchanged at phi=0; trend is qualitative, with finite-size/minor-cluster qualifications.',
247:'Flache variance passage is about repulsive-influence models, not a prediction for our attractive model.',
249:'Averaging cannot expand the initial range; it can move individual moderates toward an existing extreme.',
256:'Homogeneous and targeted noise have distinct effects; no noisy extension was implemented.',
285:'DOI10.1103/PhysRevE.77.016102 now directly verified.',
287:'Completed bibliographic record: ACS3(1-4),87-98(2000),DOI10.1142/S0219525900000078.',
289:'Completed pages381-402; distinguish 2020 online/preprint from 2021 journal volume.',
290:'Verified journal record rather than memory: PRL124,048301(2020).',
294:'Completed journal record: PNAS115(37),9216-9221.',
318:'Replace obsolete status; reference grid exists, actual reading is logged, AnyLogic execution remains pending.',
324:'Do not generalize binary/categorical transitions to our model; empirical segregation was a stopping target in Sasahara.',
326:'Retain empirical caveat; specify the significant partisan group and limit generalization.',
331:'No small-world/scale-free project runs were done; synthetic mixed opinions do not ensure a connected initial graph.',
352:'Rewiring is substantially inherited from KB; h is a parameterization, not the invention of this mechanism.'}
FP={
31:'Replication credit confirmed, but snapshots and initial small components qualify fully connected/any-rewiring language.',
33:'Long-cap check invalidates the claimed positive long-run threshold and its degree shift at d=.2.',
34:'H3 is not supported, not an equivalence result; isolate-controlled runs show speed advantage is not universal.',
39:'Rewrite headline around observation-time sensitivity and qualified h comparison, with direct prior credit.',
100:'Bibliographic gaps partly resolved; central extraction and SI gaps remain explicitly marked.',
104:'AnyLogic comparison remains a task, not a completed validation result.',
129:'Credit Kan and other homophilic BC precedents; isolate protection is separate from edge conservation.',
138:'Long-cap/KPI checks now done; noise type must be specified; exact binary critical-point scaling still incomplete.'}
locators=[('Kozma','KB §§II–VI, Figs.3–14'),('Barrat','KB/Nardini model sections'),
 ('Deffuant','DW §§2–4, Figs.1–9'),('Hegselmann','HK §2, §4 and Appendix'),('Krause','HK §2, §4 and Appendix'),
 ('Holme','HN §§II–IV, Figs.2–5'),('Vazquez','Vazquez Eqs.1–6, Figs.2–4'),
 ('Sasahara','Sasahara Model, Results, Methods C–F; author agent.py'),
 ('Baumann','Baumann Eqs.1–3, supplement I–VIII; arXiv journal metadata'),
 ('Flache','Flache Table1, similarity/repulsive sections, Frontiers'),
 ('Bail','Bail main article Fig.3 and limitations'),('Nardini','Nardini Figs.1–4 and Eqs.1–3'),
 ('Diakonova','Diakonova §§II–V and Appendix A'),('Gross','Gross §§I,VI–VII'),('Newman','HN §§II–IV / Newman Eq.1–2')]
rows=[];manifest=[]
for p in sorted(SOURCE.rglob('*')):
 if not p.is_file() or p.suffix not in ('.md','.txt','.py'):continue
 if p.name in ('00_AGENT_PROMPT.md','LITERATURE_NOTES.md'):continue
 rel=str(p.relative_to(SOURCE));content=p.read_text();manifest.append(dict(file=rel,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
 for lineno,line in enumerate(content.splitlines(),1):
  if not PAT.search(line):continue
  # This heading itself makes no research claim.
  if line.lstrip().startswith('#') and not line.lstrip().startswith('###'):continue
  reason='Underlying mechanism or bibliographic claim confirmed; scope remains restricted to the cited model.';status='confirmed'
  if p.name=='polarization_project_blueprint.md' and lineno in BP:status='corrected';reason=BP[lineno]
  if p.name=='FIVE_HOUR_PLAN.md' and lineno in FP:status='corrected';reason=FP[lineno]
  if p.name=='validate_kb.py' and lineno==1:status='corrected';reason='The supplied script is a preliminary N500/eight-rep gap-cluster check; replaced as quantitative evidence by run_validation.py.'
  if p.name=='01_MANIFEST.md':
   status='corrected';reason='Supplied snapshot; replication credit holds, but threshold, blanket h-speed and readiness claims need the new report.'
  if line.strip().startswith(('-', '>')) and ('[ ]' in line or line.strip().startswith('>')):
   status='unverifiable';reason='Instruction or future check, not a completed literature-validation result.'
  source='; '.join(dict.fromkeys(v for k,v in locators if k in line))
  rows.append(dict(id=f'C{len(rows)+1:03}',file=rel,line=lineno,original_claim=line.strip(),status=status,reason=reason,source_locator=source))
# Mapping equation lies on the following non-citing line of the same source docstring.
p=SOURCE/'sim/validate_kb.py';line=p.read_text().splitlines()[2]
rows.append(dict(id=f'C{len(rows)+1:03}',file='sim/validate_kb.py',line=3,original_claim=line,status='corrected',
 reason='phi=w/(1-w) is admissible only for w<=.5 when phi is a probability; compare clocks too.',source_locator='KB §II; update-kernel algebra in blueprint'))
with (ROOT/'claim_inventory.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(ROOT/'input_hashes.json').write_text(json.dumps(manifest,indent=2)+'\n')
lines=['\n| ID | Original location and claim (abbreviated) | Status | Verification / correction |', '|---|---|---|---|']
for r in rows:
 claim=r['original_claim'].replace('|',' / ').replace('`','').replace('**','')
 if len(claim)>130:claim=claim[:127]+'…'
 lines.append(f"| {r['id']} | `{r['file']}:{r['line']}` — {claim} | **{r['status']}** | {r['reason']} |")
notes=ROOT.parent/'LITERATURE_NOTES.md';text=notes.read_text();marker='\n<!-- GENERATED CLAIM TABLE -->'
text=text.split(marker)[0];notes.write_text(text+marker+'\n'+'\n'.join(lines)+'\n')
print(len(rows),'paper-citing passages inventoried')
