"""Recommended model: allow isolates; preserve the supplied legacy grid separately.

Run after the isolate audit. Does not overwrite results.csv or its verification.
Writes a full long-horizon grid plus a matching short-horizon D comparison.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import csv,time
import numpy as np
from accelerated import run,library
from metrics import measures,regime
from analyze import SCHEMA,save
ROOT=Path(__file__).resolve().parent

def work(job):
    row,cap=job;t0=time.time();p={k:float(row[k]) for k in ['d','mu','phi','h']}
    n=int(row['N']);x,g,sw,cens,e0,e1=run(n,int(row['k0']),p['d'],p['mu'],p['phi'],p['h'],
        int(row['seed']),cap,int(row['init']),10,allow_isolates=True)
    assert e0==e1 and np.array_equal(g,g.T) and not np.diag(g).any()
    r={k:row[k] for k in SCHEMA};r.update(sweeps=sw,censored=int(cens),edges_start=e0,edges_end=e1,
        **measures(x,g,p['d']),secs=round(time.time()-t0,4),cap=cap,allow_isolates=1,
        stop_reason='cap' if cens else 'numerically_frozen')
    sens=[]
    if row['exp']=='A' and cap==30000:
        for gap,mf,cut in product([.02,.05,.08],[.01,.05,.1],[.8,.9,.95]):
            lab=np.r_[0,np.cumsum(np.diff(np.sort(x))>gap)]
            K=int(np.count_nonzero(np.bincount(lab)>=mf*n))
            sens.append(dict(exp='A',rep=row['rep'],seed=row['seed'],d=p['d'],phi=p['phi'],
                gap=gap,min_frac=mf,S_cutoff=cut,K=K,S=r['giant_frac'],regime=regime(K,r['giant_frac'],cut)))
    return r,sens

def main():
    library();t0=time.time()
    with (ROOT/'results.csv').open() as f:old=list(csv.DictReader(f))
    with ThreadPoolExecutor(max_workers=2) as pool:
        rows=[];sens=[]
        for i,(r,s) in enumerate(pool.map(work,[(r,30000) for r in old])):
            rows.append(r);sens.extend(s)
            if i%300==0:print('primary',i,round(time.time()-t0),'s',flush=True)
        save(ROOT/'results_primary.csv',rows);save(ROOT/'primary_kpi_sensitivity.csv',sens)
        short=[r for r in old if r['exp']=='D'];rows=[]
        for r,_ in pool.map(work,[(r,3000) for r in short]):rows.append(r)
        save(ROOT/'primary_short_D.csv',rows)
    print('done',round(time.time()-t0),'s',flush=True)
if __name__=='__main__':main()
