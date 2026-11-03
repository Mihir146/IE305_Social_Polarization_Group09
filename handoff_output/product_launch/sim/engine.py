"""Accelerated product engine, initialized by the readable model."""
from pathlib import Path
import ctypes as ct
import subprocess,time
import numpy as np
from model import Config,market,select_samples,state,DAY_COLUMNS,check_config

ROOT=Path(__file__).resolve().parent
_lib=None

def library():
    global _lib
    if _lib is None:
        so=ROOT/'product_native.so';src=ROOT/'native.cpp';shared=ROOT.parents[1]/'sim/native.cpp'
        if not so.exists() or so.stat().st_mtime<max(src.stat().st_mtime,shared.stat().st_mtime):
            subprocess.run(['g++','-std=c++17','-O3','-shared','-fPIC','-ffp-contract=off',str(src),'-o',str(so)],check=True)
        _lib=ct.CDLL(str(so));p=ct.c_void_p
        _lib.product_evolve.argtypes=[ct.c_int]+[p]*12+[ct.c_int,ct.c_int,ct.c_int]+[ct.c_double]*7+[p]
        _lib.product_evolve.restype=ct.c_int
    return _lib

def run(c,rep,strategy,pop=None,samples=None,initial_aware=None,attempts=None,event_seed=None):
    check_config(c);start=time.perf_counter()
    pop=market(c,rep) if pop is None else pop
    samples=select_samples(pop,c.n_samples,strategy) if samples is None else samples
    s=state(c,pop,samples,initial_aware);rng=np.random.RandomState(4000000+rep if event_seed is None else event_seed).get_state()
    daily=np.zeros((c.periods+1,len(DAY_COLUMNS)))
    arrays=[s['adj'],s['x'],pop['group'],pop['value_scale'],pop['budget'],pop['experience'],
            s['samples'],s['aware'],s['paid_period'],s['aware_period'],s['value_at_purchase'],rng[1]]
    code=library().product_evolve(c.N,*[a.ctypes.data for a in arrays],rng[2],c.periods,
        c.N if attempts is None else attempts,c.price,c.unit_cost,c.d,c.mu,c.phi,c.h,c.share_prob,daily.ctypes.data)
    if code:raise RuntimeError(code)
    s['rewires']=int(daily[-1,12]);result=dict(pop=pop,state=s,daily=daily,secs=time.perf_counter()-start)
    verify_run(c,result)
    return result

def verify_run(c,result):
    p=result['pop'];s=result['state'];a=result['daily'];paid=s['paid_period']>=0
    assert np.array_equal(s['adj'],s['adj'].T) and not np.diag(s['adj']).any()
    assert s['adj'].sum()==p['adj'].sum()
    assert np.isfinite(s['x']).all() and np.all((s['x']>=0)&(s['x']<=1))
    assert not np.any(paid&s['samples'].astype(bool))
    assert np.all(s['aware'][paid]) and np.all(p['budget'][paid]>=c.price)
    assert np.all(s['value_at_purchase'][paid]>=c.price)
    assert np.all(s['aware_period'][paid]<=s['paid_period'][paid])
    assert np.all(np.diff(a[:,1])>=0) and np.all(np.diff(a[:,2])>=0)
    assert np.all(a[:,2]+a[:,3]<=c.N) and np.all(a[:,2]<=a[:,1])
    assert np.allclose(a[:,5],c.price*a[:,2])
    assert np.allclose(a[:,6],c.unit_cost*(a[:,2]+a[:,3]))
    assert np.allclose(a[:,7],a[:,5]-a[:,6])
    assert np.all(a[:,22]==p['adj'].sum()//2)
    assert np.all(a[:,15:18].sum(axis=1)==a[:,2])
    assert np.all(a[:,18:21].sum(axis=1)==a[:,1])
