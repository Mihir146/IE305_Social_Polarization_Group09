"""Fresh-market check after the exploratory three-sample extension.

Fixed before this confirmation executes: four policies, 100 new markets
(5000..5099), baseline assumptions, h=0. Compare the provisional 400/3/degree
recommendation with (a) equal-price random targeting, (b) its 12-sample version,
and (c) the original 500/12/random comparison. Do not search this cohort.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict
import json
from model import Config,market
from engine import run,library
from run_experiments import summarize_run,save
from analyze import interval
ROOT=Path(__file__).resolve().parent
POLICIES=[('provisional',400,3,'degree'),('targeting_control',400,3,'random'),
          ('quantity_control',400,12,'degree'),('original_comparison',500,12,'random')]

def work(rep):
    pop=market(Config(),rep);out=[]
    for name,price,samples,strategy in POLICIES:
        c=Config(price=price,n_samples=samples,h=0)
        result=run(c,rep,strategy,pop=pop)
        row,_,_=summarize_run(c,rep,strategy,'confirmation',name,result)
        out.append(row)
    return out

def main():
    library();rows=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for batch in pool.map(work,range(5000,5100)):rows.extend(batch)
    save(ROOT/'results/confirmation_runs.csv',rows)
    groups=defaultdict(dict)
    for r in rows:groups[r['scenario']][r['rep']]=r
    summary=[];contrasts=[]
    for name,price,samples,strategy in POLICIES:
        sub=groups[name];q=dict(policy=name,price=price,n_samples=samples,strategy=strategy,h=0,n=len(sub))
        for metric in ('profit','paid_buyers','aware'):
            mean,lo,hi=interval([r[metric] for r in sub.values()]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
        summary.append(q)
        if name=='provisional':continue
        for metric in ('profit','paid_buyers','aware'):
            mean,lo,hi=interval([groups['provisional'][i][metric]-sub[i][metric] for i in sorted(sub)])
            contrasts.append(dict(provisional_minus=name,metric=metric,n=len(sub),difference=mean,lo=lo,hi=hi))
    save(ROOT/'analysis/confirmation_summary.csv',summary)
    save(ROOT/'analysis/confirmation_paired.csv',contrasts)
    (ROOT/'results/confirmation_manifest.json').write_text(json.dumps(dict(
        purpose='Fresh-market confirmation of four fixed comparisons after exploratory follow-up',
        policies=POLICIES,rep_start=5000,rep_end=5099,independent_markets=100,runs=400,
        selection_on_this_cohort=False,anylogic_executed=False),indent=2)+'\n')
    print(json.dumps(summary,indent=2));print(json.dumps(contrasts,indent=2))
if __name__=='__main__':main()
