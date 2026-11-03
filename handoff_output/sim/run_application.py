"""Campus deliberation: six contact-design policies, paired within degree.

All inputs are synthetic. Each policy has 30 independent replication indices.
Five snapshots of the SAME realization are repeated measures, not 150 replicates.
Uses the unchanged primary model and its original seed convention.
"""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import time
import numpy as np
from accelerated import initial, run, library
from analyze import save
from metrics import measures, wilson
from summarize_validation import ci

ROOT=Path(__file__).resolve().parent
HORIZONS=(300,1000,3000,30000,300000)

def work(job):
    k,h,rep=job
    rows=[]
    for cap in HORIZONS:
        started=time.perf_counter()
        x,g,sw,cens,e0,e1=run(300,k,.2,.3,.005,h,1000+rep,cap,0,10,allow_isolates=True)
        ii,jj=np.where(np.triu(g,1))
        rows.append(dict(exp='APPLICATION',rep=rep,seed=1000+rep,N=300,k0=k,
            d=.2,mu=.3,phi=.005,h=h,init=0,sweeps=sw,censored=int(cens),
            edges_start=e0,edges_end=e1,**measures(x,g,.2),secs=round(time.perf_counter()-started,6),
            cap=cap,allow_isolates=1,
            discordant_fraction=float(np.mean(np.abs(x[ii]-x[jj])>=.2)),
            stop_reason='cap' if cens else 'numerically_frozen'))
        assert e0==e1
    return rows

def main():
    library();t=time.time()
    jobs=list(product((4,8,16),(0.,1.),range(30)))
    rows=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,res in enumerate(pool.map(work,jobs)):
            rows.extend(res)
            if i%30==0:print('application',i,'/',len(jobs),round(time.time()-t),'s',flush=True)
    save(ROOT/'application_snapshots.csv',rows)
    summaries=[]
    for k,h,cap in product((4,8,16),(0.,1.),HORIZONS):
        sub=[r for r in rows if (r['k0'],r['h'],r['cap'])==(k,h,cap)]
        q=dict(k0=k,h=h,cap=cap,n=len(sub),contacts=300*k//2,
               capped=sum(r['censored'] for r in sub))
        for key in ('giant_frac','K','cross_frac','opinion_var','isolated_frac','discordant_fraction'):
            m,lo,hi=ci([r[key] for r in sub]);q.update({key+'_mean':m,key+'_lo':lo,key+'_hi':hi})
        nfrag=sum(r['giant_frac']<.9 for r in sub);lo,hi=wilson(nfrag,len(sub))
        q.update(p_fragmented=nfrag/len(sub),p_lo=lo,p_hi=hi)
        summaries.append(q)
    save(ROOT/'application_summary.csv',summaries)
    contrasts=[]
    for k,cap in product((4,8,16),HORIZONS):
        by_h=[{r['rep']:r for r in rows if r['k0']==k and r['cap']==cap and r['h']==h} for h in (0,1)]
        q=dict(k0=k,cap=cap,n=30)
        for key in ('giant_frac','cross_frac','discordant_fraction'):
            m,lo,hi=ci([by_h[1][i][key]-by_h[0][i][key] for i in range(30)])
            q.update({key+'_h1_minus_h0':m,key+'_lo':lo,key+'_hi':hi})
        contrasts.append(q)
    save(ROOT/'application_paired.csv',contrasts)
    data=ROOT.parent/'data';data.mkdir(exist_ok=True)
    x,g,_=initial(300,8,1000,0)
    save(data/'synthetic_people_seed1000_k8.csv',[dict(person_id=i,initial_support=float(v)) for i,v in enumerate(x)])
    ii,jj=np.where(np.triu(g,1))
    save(data/'synthetic_contacts_seed1000_k8.csv',[dict(person_i=int(i),person_j=int(j)) for i,j in zip(ii,jj)])
    from split_snapshots import main as split
    split()
    print('Saved',len(rows),'snapshots from',len(jobs),'realizations;',round(time.time()-t),'s',flush=True)

if __name__=='__main__':main()
