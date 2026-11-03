"""Readable product-launch reference. All inputs are synthetic assumptions.

The native engine uses this initialization and is checked against this event loop.
"""
from dataclasses import dataclass,asdict,replace
import numpy as np

STRATEGIES=('random','degree','distributed')
DAY_COLUMNS=['period','aware','paid_buyers','free_samples','new_paid','revenue','total_cost',
             'profit','paid_adoption','min_group_adoption','giant_frac','cross_group_frac',
             'rewires','belief_mean','belief_variance','paid_group0','paid_group1','paid_group2',
             'aware_group0','aware_group1','aware_group2','degree_zero','total_edges']

@dataclass(frozen=True)
class Config:
    N:int=300
    k0:int=8
    groups:int=3
    within_weight:float=6.
    periods:int=60
    n_samples:int=12
    price:float=500.
    unit_cost:float=250.
    d:float=.2
    mu:float=.3
    phi:float=.05
    h:float=0.
    share_prob:float=.25
    quality:float=.8
    experience_sd:float=.1

def check_config(c):
    if not (c.N>=2 and 0<=c.k0<c.N and c.groups==3 and c.within_weight>=1 and
            c.periods>=1 and 0<=c.n_samples<=c.N and c.price>=0 and c.unit_cost>=0 and
            0<c.d<=1 and 0<=c.mu<=.5 and 0<=c.phi<=1 and 0<=c.h<=1 and
            0<=c.share_prob<=1 and 0<=c.quality<=1 and c.experience_sd>=0):
        raise ValueError('Invalid product configuration')

def market(c,rep):
    check_config(c)
    gr=np.arange(c.N,dtype=np.int32)%3
    rng=np.random.RandomState(1000000+rep)
    adj=np.zeros((c.N,c.N),dtype=np.uint8);m=c.N*c.k0//2;edges=0
    while edges<m:
        i,j=rng.randint(c.N),rng.randint(c.N)
        if i==j or adj[i,j]:continue
        if gr[i]!=gr[j] and rng.random_sample()>=1/c.within_weight:continue
        adj[i,j]=adj[j,i]=1;edges+=1
    rng=np.random.RandomState(2000000+rep)
    prior=np.empty(c.N);v=np.empty(c.N);budget=np.empty(c.N);experience=np.empty(c.N)
    for i in range(c.N):
        prior[i]=np.median(rng.random_sample(3))
        v[i]=500+500*rng.random_sample()
        budget[i]=400+600*rng.random_sample()
        experience[i]=np.clip(c.quality+c.experience_sd*rng.randn(),0,1)
    priority=np.random.RandomState(3000000+rep).permutation(c.N).astype(np.int32)
    return dict(group=gr,adj=adj,prior=prior,value_scale=v,budget=budget,
                experience=experience,priority=priority)

def select_samples(pop,count,strategy):
    if strategy not in STRATEGIES:raise ValueError(strategy)
    n=len(pop['prior']);mask=np.zeros(n,dtype=np.uint8)
    rank=np.empty(n,dtype=np.int32);rank[pop['priority']]=np.arange(n)
    degree=pop['adj'].sum(axis=1)
    if strategy=='random':chosen=pop['priority'][:count]
    elif strategy=='degree':chosen=sorted(range(n),key=lambda i:(-int(degree[i]),int(rank[i])))[:count]
    else:
        order=[sorted(np.flatnonzero(pop['group']==g).tolist(),key=lambda i:(-int(degree[i]),int(rank[i]))) for g in range(3)]
        chosen=[];g=0
        while len(chosen)<count:
            if order[g]:chosen.append(order[g].pop(0))
            g=(g+1)%3
    mask[chosen]=1
    return mask

def state(c,pop,samples,initial_aware=None):
    x=pop['prior'].copy();x[samples.astype(bool)]=pop['experience'][samples.astype(bool)]
    aware=samples.copy() if initial_aware is None else np.maximum(samples,initial_aware).astype(np.uint8)
    return dict(x=x,adj=pop['adj'].copy(),aware=aware,samples=samples.copy(),
                paid_period=np.full(c.N,-1,dtype=np.int32),
                aware_period=np.where(aware,0,-1).astype(np.int32),
                value_at_purchase=np.full(c.N,-1.,dtype=np.float64),rewires=0)

def interaction(c,pop,s,u,period):
    i=int(u[0]*c.N);neighbors=np.flatnonzero(s['adj'][i])
    if len(neighbors)==0:return
    j=int(neighbors[int(u[1]*len(neighbors))])
    if not s['aware'][i] and not s['aware'][j]:return
    if s['aware'][i]!=s['aware'][j]:
        if u[2]>=c.share_prob:return
        other=j if s['aware'][i] else i
        s['aware'][other]=1;s['aware_period'][other]=period
    xi,xj=s['x'][i],s['x'][j]
    if abs(xi-xj)<c.d:
        s['x'][i]=xi+c.mu*(xj-xi);s['x'][j]=xj+c.mu*(xi-xj)
    elif u[3]<c.phi:
        candidates=np.flatnonzero((s['adj'][i]==0)&(np.arange(c.N)!=i))
        if u[4]<c.h:
            close=candidates[np.abs(s['x'][candidates]-xi)<c.d]
            if len(close):candidates=close
        if len(candidates):
            k=int(candidates[int(u[5]*len(candidates))])
            s['adj'][i,j]=s['adj'][j,i]=0;s['adj'][i,k]=s['adj'][k,i]=1
            s['rewires']+=1

def purchase(c,pop,s,period):
    value=pop['value_scale']*s['x']
    new=np.flatnonzero((s['aware']>0)&(s['samples']==0)&(s['paid_period']<0)&
                       (pop['budget']>=c.price)&(value>=c.price))
    s['paid_period'][new]=period;s['value_at_purchase'][new]=value[new]
    s['x'][new]=pop['experience'][new]
    return len(new)

def record(c,pop,s,period,new_paid):
    paid=s['paid_period']>=0;gr=pop['group'];adj=s['adj'];n=c.N
    p=int(paid.sum());a=int(s['aware'].sum());f=int(s['samples'].sum())
    pg=np.bincount(gr,weights=paid,minlength=3);ag=np.bincount(gr,weights=s['aware'],minlength=3)
    eligible=np.bincount(gr,weights=1-s['samples'],minlength=3)
    rates=pg[eligible>0]/eligible[eligible>0]
    seen=np.zeros(n,dtype=bool);giant=0
    for i in range(n):
        if seen[i]:continue
        queue=[i];seen[i]=True;size=0
        while queue:
            j=queue.pop();size+=1
            fresh=np.flatnonzero((adj[j]>0)&~seen);seen[fresh]=True;queue.extend(fresh.tolist())
        giant=max(giant,size)
    ii,jj=np.nonzero(np.triu(adj,1));m=len(ii)
    return np.array([period,a,p,f,new_paid,c.price*p,c.unit_cost*(p+f),
        (c.price-c.unit_cost)*p-c.unit_cost*f,p/(n-f) if n>f else 0,
        rates.min() if len(rates) else 0,giant/n,
        np.mean(gr[ii]!=gr[jj]) if m else 0,s['rewires'],s['x'].mean(),s['x'].var(),
        *pg,*ag,np.count_nonzero(adj.sum(axis=1)==0),m],dtype=np.float64)

def run_reference(c,rep,strategy,pop=None,samples=None,initial_aware=None,attempts=None,event_seed=None):
    pop=market(c,rep) if pop is None else pop
    samples=select_samples(pop,c.n_samples,strategy) if samples is None else samples
    s=state(c,pop,samples,initial_aware)
    rng=np.random.RandomState(4000000+rep if event_seed is None else event_seed)
    rows=[record(c,pop,s,0,0)]
    for t in range(1,c.periods+1):
        for _ in range(c.N if attempts is None else attempts):interaction(c,pop,s,rng.random_sample(6),t)
        new=purchase(c,pop,s,t);rows.append(record(c,pop,s,t,new))
    return dict(pop=pop,state=s,daily=np.array(rows))
