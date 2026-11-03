"""Run literature checks and all censored continuations; writes raw CSV evidence.

Usage: python sim/run_validation.py --part kb|hk|replay|long|all --workers 2
Each output records seeds and parameters. Replays retain the original stopping rule.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import argparse,csv,time,json
import numpy as np
from accelerated import run,initial,library
from metrics import measures,regime,stopping_diagnostics

ROOT=Path(__file__).resolve().parent
def save(name,rows):
    if not rows:return
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def simulate(p):
    a=dict(p);family=a.pop('family');rep=a.pop('rep')
    x,g,sw,cens,e0,e1=run(**a)
    assert e0==e1 and np.array_equal(g,g.T) and not np.diag(g).any()
    assert np.isfinite(x).all() and x.min()>=0 and x.max()<=1
    x0,_,_=initial(a['n'],a['k0'],a['seed'],a['init_mode'])
    assert abs(x.mean()-x0.mean())<1e-11
    r=dict(family=family,rep=rep,**a,sweeps=sw,censored=int(cens),edges_start=e0,edges_end=e1,
           **measures(x,g,a['d'],paths=True))
    r['initial_mean']=float(x0.mean());r['final_mean']=float(x.mean())
    return r

def kb_tasks():
    base=dict(n=1000,k0=10,d=.256,mu=.5,phi=0.,h=0.,max_sweeps=30000,
              init_mode=0,check_every=10,allow_isolates=True,scheduler='kb',eps=1e-5)
    jobs=[]
    for w,d in product([0.,.1,.5,.9],[.24,.25,.256,.26,.27,.28,.30,.32,.35]):
        for rep in range(100):
            jobs.append(dict(base,family='kb_d1',rep=rep,seed=20000+rep,phi=w,d=d))
    for n,k0,scale in product([500,1000,2000],[10,20,30],[.6,1.,1.4]):
        for rep in range(30):
            jobs.append(dict(base,family='kb_d2',rep=rep,seed=30000+rep,n=n,k0=k0,
                             d=scale/(2*k0)))
    return jobs

def hk():
    rows=[]
    for eps,rep in product([.01,.15,.20,.25,.30],range(100)):
        rng=np.random.RandomState(40000+rep);x=np.sort(rng.random_sample(625))
        for step in range(10000):
            lo=np.searchsorted(x,x-eps,side='left');hi=np.searchsorted(x,x+eps,side='right')
            cs=np.r_[0.,np.cumsum(x)];new=(cs[hi]-cs[lo])/(hi-lo)
            # With sorted x, updating all agents synchronously preserves order.
            delta=np.max(abs(new-x));x=new
            if delta<1e-10:break
        cuts=np.r_[0,np.flatnonzero(np.diff(x)>1e-6)+1,len(x)]
        sizes=np.diff(cuts)
        rows.append(dict(family='hk',N=625,epsilon=eps,seed=40000+rep,rep=rep,
                         synchronous=1,iterations=step+1,censored=int(step==9999),
                         n_clusters=len(sizes),largest=sizes.max()/625,
                         consensus=int(np.ptp(x)<1e-6)))
    save('hk_validation.csv',rows)

def original_rows():
    with (ROOT/'results.csv').open() as f:return list(csv.DictReader(f))

def replay_task(row):
    p={k:float(row[k]) for k in ['d','mu','phi','h']}
    p.update(n=int(row['N']),k0=int(row['k0']),seed=int(row['seed']),
             max_sweeps=3000,init_mode=int(row['init']),check_every=10)
    x,g,sw,cens,e0,e1=run(**p)
    m=measures(x,g,p['d'])
    # Saved Numba data are the second independent check of the native RNG path.
    matches=(sw==int(row['sweeps']) and cens==bool(int(row['censored'])) and
             all(abs(float(row[k])-m[k])<1e-10 for k in
                 ['n_components','giant_frac','isolated_frac','K','cross_frac','Q','opinion_var']))
    base=dict(exp=row['exp'],rep=int(row['rep']),seed=p['seed'],N=p['n'],k0=p['k0'],
              d=p['d'],mu=p['mu'],phi=p['phi'],h=p['h'],init=p['init_mode'],
              sweeps=sw,censored=int(cens),matches_saved=int(matches),**m)
    sensitivity=[]
    S=m['giant_frac']
    for gap,mf,cut in product([.02,.05,.08],[.01,.05,.1],[.8,.9,.95]):
        # Reuse the same final state; no stochastic reruns between metric choices.
        lab=np.r_[0,np.cumsum(np.diff(np.sort(x))>gap)]
        K=int(np.count_nonzero(np.bincount(lab)>=mf*len(x)))
        sensitivity.append(dict(exp=row['exp'],rep=int(row['rep']),seed=p['seed'],
                                k0=p['k0'],d=p['d'],phi=p['phi'],h=p['h'],
                                gap=gap,min_frac=mf,S_cutoff=cut,K=K,S=S,
                                regime=regime(K,S,cut)))
    return base,sensitivity

def long_task(row):
    p={k:float(row[k]) for k in ['d','mu','phi','h']}
    p.update(n=int(row['N']),k0=int(row['k0']),seed=int(row['seed']),max_sweeps=30000,
             init_mode=int(row['init']),check_every=10)
    x,g,sw,cens,e0,e1=run(**p)
    m=measures(x,g,p['d'],paths=True)
    state_dir=ROOT/'long_states';state_dir.mkdir(exist_ok=True)
    key='_'.join(str(row[k]) for k in ['exp','rep','N','k0','d','mu','phi','h','init'])
    np.savez_compressed(state_dir/(key+'.npz'),x=x,adj=g)
    return dict(exp=row['exp'],rep=int(row['rep']),seed=p['seed'],N=p['n'],k0=p['k0'],
                d=p['d'],mu=p['mu'],phi=p['phi'],h=p['h'],init=p['init_mode'],
                cap=30000,sweeps=sw,censored=int(cens),edges_start=e0,edges_end=e1,
                old_S=float(row['giant_frac']),old_K=int(row['K']),**m,
                **stopping_diagnostics(x,g,p['d']))

def isolate_task(row):
    p={k:float(row[k]) for k in ['d','mu','phi','h']}
    p.update(n=int(row['N']),k0=int(row['k0']),seed=int(row['seed']),max_sweeps=30000,
             init_mode=int(row['init']),check_every=10,allow_isolates=True)
    x,g,sw,cens,e0,e1=run(**p)
    assert e0==e1 and np.array_equal(g,g.T) and not np.diag(g).any()
    return dict(exp=row['exp'],rep=int(row['rep']),seed=p['seed'],N=p['n'],k0=p['k0'],
                d=p['d'],mu=p['mu'],phi=p['phi'],h=p['h'],init=p['init_mode'],
                cap=30000,allow_isolates=1,sweeps=sw,censored=int(cens),edges_start=e0,edges_end=e1,
                **measures(x,g,p['d'],paths=True),**stopping_diagnostics(x,g,p['d']))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--part',default='all',choices=['all','kb','hk','replay','long','isolates'])
    ap.add_argument('--workers',type=int,default=2);args=ap.parse_args();library();t0=time.time()
    # ctypes releases the GIL during the native dynamics. Each run owns its RNG.
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        if args.part in ('all','kb'):
            jobs=kb_tasks();out=[]
            for i,r in enumerate(pool.map(simulate,jobs,chunksize=4)):
                out.append(r)
                if i%200==0: print('KB',i,'/',len(jobs),round(time.time()-t0),'s',flush=True)
            save('kb_validation.csv',out)
        if args.part in ('all','hk'):hk();print('HK done',flush=True)
        if args.part in ('all','replay'):
            base=[];sens=[]
            for i,(r,s) in enumerate(pool.map(replay_task,original_rows(),chunksize=4)):
                base.append(r);sens.extend(s)
                if i%200==0:print('replay',i,round(time.time()-t0),'s',flush=True)
            save('replay_validation.csv',base);save('kpi_sensitivity.csv',sens)
        if args.part in ('all','long'):
            jobs=[r for r in original_rows() if int(r['censored'])]
            out=[]
            for i,r in enumerate(pool.map(long_task,jobs,chunksize=2)):
                out.append(r)
                if i%30==0:print('long',i,'/',len(jobs),round(time.time()-t0),'s',flush=True)
            save('long_cap.csv',out)
        if args.part in ('all','isolates'):
            jobs=[r for r in original_rows() if r['exp'] in ('B','D')]
            out=list(pool.map(isolate_task,jobs,chunksize=2));save('isolate_sensitivity.csv',out)
    print('done',round(time.time()-t0),'s',flush=True)

if __name__=='__main__':main()
