"""18 launch policies; separate pilot/main cohorts and traceable outputs."""
from pathlib import Path
from dataclasses import asdict,replace
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import csv,json,time,argparse
import numpy as np
from model import Config,STRATEGIES,DAY_COLUMNS,market,select_samples
from engine import run,library

ROOT=Path(__file__).resolve().parent

def save(path,rows):
    if not rows:return
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def metadata(c,rep,strategy,cohort,scenario):
    return dict(cohort=cohort,scenario=scenario,rep=rep,graph_seed=1000000+rep,
        trait_seed=2000000+rep,selection_seed=3000000+rep,event_seed=4000000+rep,
        strategy=strategy,**asdict(c))

def summarize_run(c,rep,strategy,cohort,scenario,r):
    meta=metadata(c,rep,strategy,cohort,scenario)
    last=dict(zip(DAY_COLUMNS,r['daily'][-1]));last.pop('period')
    threshold=.2*(c.N-int(r['state']['samples'].sum()))
    hits=np.flatnonzero(r['daily'][:,2]>=threshold) if threshold>0 else np.array([0])
    t20=int(hits[0]) if len(hits) else -1
    summary=dict(meta,**last,t20=t20,hit20=int(t20>=0),restricted_t20=t20 if t20>=0 else c.periods,secs=round(r['secs'],6))
    daily=[]
    for row in r['daily']:
        daily.append(dict(cohort=cohort,scenario=scenario,rep=rep,strategy=strategy,price=c.price,h=c.h,
                          **dict(zip(DAY_COLUMNS,row))))
    segments=[];p=r['pop'];s=r['state'];bands=np.minimum((p['prior']*3).astype(int),2)
    for band,affordable in product(range(3),(0,1)):
        mask=(bands==band)&((p['budget']>=c.price)==bool(affordable))&(s['samples']==0)
        segments.append(dict(cohort=cohort,scenario=scenario,rep=rep,strategy=strategy,price=c.price,h=c.h,
            prior_band=band,affordable=affordable,eligible=int(mask.sum()),
            paid=int(np.count_nonzero(mask&(s['paid_period']>=0))),aware=int(np.count_nonzero(mask&s['aware'].astype(bool)))))
    return summary,daily,segments

def work(job):
    rep,cohort=job;pop=market(Config(),rep)
    summaries=[];daily=[];segments=[];examples=[]
    for strategy in STRATEGIES:
        samples=select_samples(pop,12,strategy)
        for price,h in product((400.,500.,600.),(0.,1.)):
            c=Config(price=price,h=h);r=run(c,rep,strategy,pop=pop,samples=samples)
            a,b,d=summarize_run(c,rep,strategy,cohort,'baseline',r)
            summaries.append(a);daily.extend(b);segments.extend(d)
            if rep in (0,1000):
                s=r['state']
                for i in range(c.N):
                    examples.append(dict(cohort=cohort,rep=rep,strategy=strategy,price=price,h=h,
                        customer=i,group=int(pop['group'][i]),initial_belief=pop['prior'][i],
                        value_scale=pop['value_scale'][i],budget=pop['budget'][i],experience=pop['experience'][i],
                        free_sample=int(s['samples'][i]),aware_period=int(s['aware_period'][i]),
                        paid_period=int(s['paid_period'][i]),value_at_purchase=s['value_at_purchase'][i],
                        final_belief=s['x'][i]))
    return summaries,daily,segments,examples

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cohort',choices=['pilot','main'],required=True)
    ap.add_argument('--workers',type=int,default=2);a=ap.parse_args();library();start=time.perf_counter()
    indices=range(30) if a.cohort=='pilot' else range(1000,1100)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    summaries=[];trajectories=[];segments=[];examples=[]
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for i,(s,t,g,e) in enumerate(pool.map(work,[(r,a.cohort) for r in indices])):
            summaries.extend(s);trajectories.extend(t);segments.extend(g);examples.extend(e)
            if i%10==0:print(a.cohort,i+1,'markets,',len(summaries),'runs,',round(time.perf_counter()-start),'s',flush=True)
    save(out/f'{a.cohort}_runs.csv',summaries);save(out/f'{a.cohort}_trajectories.csv',trajectories)
    save(out/f'{a.cohort}_segments.csv',segments);save(out/f'{a.cohort}_example_ledger.csv',examples)
    info=dict(cohort=a.cohort,markets=len(indices),policies=18,runs=len(summaries),
        repeated_period_rows=len(trajectories),elapsed_seconds=round(time.perf_counter()-start,3),
        fixed_campaign_periods=60,anylogic_executed=False)
    (out/f'{a.cohort}_manifest.json').write_text(json.dumps(info,indent=2)+'\n')
    if a.cohort=='main':
        pop=market(Config(),1000);data=ROOT.parent/'data'
        save(data/'customers_rep1000.csv',[dict(customer=i,group=int(pop['group'][i]),
            initial_belief=pop['prior'][i],value_scale=pop['value_scale'][i],budget=pop['budget'][i],
            experience_signal=pop['experience'][i]) for i in range(300)])
        ii,jj=np.nonzero(np.triu(pop['adj'],1))
        save(data/'contacts_rep1000.csv',[dict(customer_i=int(i),customer_j=int(j)) for i,j in zip(ii,jj)])
    print(json.dumps(info,indent=2),flush=True)

if __name__=='__main__':main()
