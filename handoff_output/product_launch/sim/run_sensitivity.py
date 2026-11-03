"""Focused stress design plus one-factor behavioral uncertainty checks."""
from pathlib import Path
from dataclasses import replace
from itertools import product
from concurrent.futures import ThreadPoolExecutor
import time,json
from model import Config,STRATEGIES,market,select_samples
from engine import run,library
from run_experiments import summarize_run,save
ROOT=Path(__file__).resolve().parent

def stress(rep):
    summaries=[];daily=[]
    for weight,count in product((6.,60.),(3,12)):
        base=Config(price=400,within_weight=weight,n_samples=count)
        pop=market(base,rep);scenario=f'samples{count}_within{int(weight)}'
        for strategy,h in product(STRATEGIES,(0.,1.)):
            c=replace(base,h=h);r=run(c,rep,strategy,pop=pop)
            s,t,_=summarize_run(c,rep,strategy,'stress',scenario,r)
            summaries.append(s);daily.extend(t)
    return summaries,daily

BEHAVIOR=[('base',{}),('quality_low',{'quality':.6}),('quality_high',{'quality':.95}),
          ('confidence_low',{'d':.1}),('confidence_high',{'d':.4}),
          ('sharing_low',{'share_prob':.05}),('sharing_high',{'share_prob':.5})]

def behavior(rep):
    summaries=[];daily=[]
    for scenario,changes in BEHAVIOR:
        base=replace(Config(h=0),**changes);pop=market(base,rep)
        for price in (400.,500.,600.):
            c=replace(base,price=price);r=run(c,rep,'degree',pop=pop)
            s,t,_=summarize_run(c,rep,'degree','behavior',scenario,r)
            summaries.append(s);daily.extend(t)
    return summaries,daily

def main():
    library();start=time.perf_counter();out=ROOT/'results';out.mkdir(exist_ok=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        for name,fn,indices in [('stress',stress,range(2000,2100)),('behavior',behavior,range(3000,3100))]:
            rows=[];daily=[]
            for i,(s,t) in enumerate(pool.map(fn,indices)):
                rows.extend(s);daily.extend(t)
                if i%20==0:print(name,i+1,'markets',round(time.perf_counter()-start),'s',flush=True)
            save(out/f'{name}_runs.csv',rows);save(out/f'{name}_trajectories.csv',daily)
            (out/f'{name}_manifest.json').write_text(json.dumps(dict(markets=len(indices),runs=len(rows),
                period_rows=len(daily),rep_start=min(indices),rep_end=max(indices),anylogic_executed=False),indent=2)+'\n')
    print('Completed sensitivity in',round(time.perf_counter()-start),'s',flush=True)

if __name__=='__main__':main()
