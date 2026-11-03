"""Complete the3-sample what-if at all original prices/policies.

Motivated by the focused stress experiment. Uses the same100 main markets for
paired budget contrasts; these are not additional independent markets.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from dataclasses import replace
from model import Config,STRATEGIES,market
from engine import run,library
from run_experiments import summarize_run,save
from analyze import load_runs,interval
ROOT=Path(__file__).resolve().parent

def work(rep):
    pop=market(Config(),rep);rows=[];daily=[]
    for price,strategy,h in product((400.,500.,600.),STRATEGIES,(0.,1.)):
        c=Config(price=price,h=h,n_samples=3);r=run(c,rep,strategy,pop=pop)
        s,t,_=summarize_run(c,rep,strategy,'main','budget3',r);rows.append(s);daily.extend(t)
    return rows,daily

def main():
    library();rows=[];daily=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for s,t in pool.map(work,range(1000,1100)):rows.extend(s);daily.extend(t)
    save(ROOT/'results/budget3_runs.csv',rows);save(ROOT/'results/budget3_trajectories.csv',daily)
    combined=load_runs(ROOT/'results/main_runs.csv')+rows;save(ROOT/'results/main_extended_runs.csv',combined)
    out=[]
    for price,strategy,h in product((400.,500.,600.),STRATEGIES,(0.,1.)):
        a={int(r['rep']):r for r in rows if r['price']==price and r['strategy']==strategy and r['h']==h}
        b={int(r['rep']):r for r in combined if r['scenario']=='baseline' and r['price']==price and r['strategy']==strategy and r['h']==h}
        for metric in ['profit','paid_buyers','paid_adoption','aware']:
            mean,lo,hi=interval([a[i][metric]-b[i][metric] for i in sorted(a)])
            out.append(dict(price=price,strategy=strategy,h=h,metric=metric,n=len(a),three_minus_twelve=mean,lo=lo,hi=hi))
    save(ROOT/'analysis/budget_paired.csv',out)
    print('Saved1800 follow-up runs on the same100 main markets;36 candidate policies total')

if __name__=='__main__':main()
