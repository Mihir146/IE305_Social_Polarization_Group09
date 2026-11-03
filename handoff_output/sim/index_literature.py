"""Index the benchmark rows from the notes; source numbers remain distinct from runs."""
from pathlib import Path
import re,csv
ROOT=Path(__file__).resolve().parent
notes=(ROOT.parent/'LITERATURE_NOTES.md').read_text().split('## 7. Claim verification')[0]
urls={
 'KB':'https://www.cpt.univ-mrs.fr/~barrat/PhysRevE_77_016102.pdf',
 'DW':'https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/dbba/2023/deffuantmixingbeliefsamonginteractingagents.pdf',
 'V':'https://arxiv.org/html/0710.4910','HN':'https://arxiv.org/html/physics/0603023',
 'S':'https://arxiv.org/html/1905.03919','HK':'https://jasss.soc.surrey.ac.uk/5/3/2/2.pdf',
 'B':'https://arxiv.org/html/1906.12325','N':'https://arxiv.org/html/0711.1261v1',
 'D':'https://arxiv.org/html/1411.5181','BA':'https://dlab.epfl.ch/teaching/spring2019/cs718/papers/bail2018exposure.pdf'}
rows=[]
for line in notes.splitlines():
 if re.match(r'^\| [A-Z]+[0-9]+ \|',line):
  cells=[c.strip() for c in line.strip('|').split('|')];id,where=cells[:2];value=' | '.join(cells[2:])
  prefix=re.match('[A-Z]+',id).group()
  rows.append(dict(id=id,source_url=urls[prefix],locator=where,published_setup_or_result=value,
                   status='contains_unverified_plot_values' if '[UNVERIFIED]' in value else 'confirmed'))
extra=[
 ('KFP1','https://arxiv.org/html/2112.05856','§4','N1000,p.01,M1,K5,alpha.1,50 runs; major>=5%; shifted C .26 -> up to .34'),
 ('KFP2','https://arxiv.org/html/2112.05856','Fig.2 and §4.5','pseudo-consensus subcluster difference .0003; N5000,p.01,M5,K25 changes mean degree to50'),
 ('L1','https://arxiv.org/html/0707.1762v2','Figs.1-2','1001 bins,mass threshold1e-9; density HK thresholds about .19/.22, max reported convergence21431'),
 ('L2','https://arxiv.org/html/0707.1762v2','§3','approximate integer-part 1/(2epsilon) major-cluster heuristic; not an exact finite-N theorem'),
 ('NE1','https://arxiv.org/html/physics/0602124','Table1','karate optimized Q .419; not a fixed-partition validation target'),
 ('BS1','https://arxiv.org/html/1906.09076','§III and §V','43 weekly windows,285670 users,2066042 mentions; coherence exp(-beta*distance),beta1; randomized ensemble100'),
 ('P1','https://link.springer.com/article/10.1007/s41109-022-00495-7','Experimental settings','N250,30 runs,mu.5; epsilon .2,.3,.4; gamma0,.4,.8,1.2,1.6; pr0,.1,...,.5; cap1e5'),
 ('BG1','https://sites.stat.columbia.edu/gelman/surveys.course/BaldassarriGelman2008.pdf','Tables1,3','47 issues,NES1972-2004; correlation slopes .05/.04 per decade(SE.01); issue-pair slope .02/decade'),
 ('GB1','https://arxiv.org/html/0709.1858','§III and Fig.3','Boolean-network K=2+12.4*N^(-.47); oscillator exponent -.48; not opinion-model validation targets')]
for id,url,where,value in extra:
 rows.append(dict(id=id,source_url=url,locator=where,published_setup_or_result=value,status='confirmed'))
with (ROOT/'literature_targets.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(len(rows),'source benchmarks indexed')
