"""Compiled acceleration; numerical equivalence is checked in verify_native.py.

No downloaded packages required beyond NumPy; compiles native.cpp with g++.
The original model.py stays the readable reference. No fast-math is used.
"""
import ctypes as ct
from pathlib import Path
import subprocess
import numpy as np

ROOT = Path(__file__).resolve().parent
_lib = None

def library():
    global _lib
    if _lib is None:
        so = ROOT / 'native.so'
        if not so.exists() or so.stat().st_mtime < (ROOT/'native.cpp').stat().st_mtime:
            subprocess.run(['g++', '-std=c++17', '-O3', '-shared', '-fPIC',
                            '-ffp-contract=off', str(ROOT/'native.cpp'), '-o', str(so)], check=True)
        _lib = ct.CDLL(str(so))
        _lib.evolve.argtypes = [ct.c_int, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_int,
                               ct.c_double, ct.c_double, ct.c_double, ct.c_double,
                               ct.c_int, ct.c_int, ct.c_int, ct.c_int, ct.c_double, ct.c_void_p]
        _lib.evolve.restype = ct.c_int
    return _lib

def initial(n, k0, seed, init_mode=0):
    rng = np.random.RandomState(seed)
    adj = np.zeros((n,n), dtype=np.bool_)
    m = n*k0//2
    added = 0
    while added < m:
        a, b = rng.randint(n), rng.randint(n)
        if a != b and not adj[a,b]:
            adj[a,b] = adj[b,a] = True
            added += 1
    x = np.empty(n)
    for i in range(n):
        if init_mode == 0:
            x[i] = rng.random_sample()
        elif init_mode == 1:
            u,v,w = rng.random_sample(),rng.random_sample(),rng.random_sample()
            x[i] = max(min(u,v),min(max(u,v),w))
        else:
            c = .25 if rng.random_sample()<.5 else .75
            x[i] = min(1., max(0., c+.08*rng.randn()))
    return x,adj,rng.get_state()

def run(n,k0,d,mu,phi,h,seed,max_sweeps,init_mode,check_every,
        allow_isolates=False, scheduler='project', eps=1e-3):
    if not (n>1 and 0<=k0<n and 0<d<=1 and 0<mu<=.5 and
            0<=phi<=1 and 0<=h<=1 and max_sweeps>0 and check_every>0):
        raise ValueError('Invalid model parameters')
    if scheduler not in ('project','kb'):
        raise ValueError(scheduler)
    x,adj,state = initial(n,k0,seed,init_mode)
    info=np.zeros(2)
    code=library().evolve(n,x.ctypes.data,adj.ctypes.data,state[1].ctypes.data,state[2],
                         d,mu,phi,h,max_sweeps,check_every,allow_isolates,
                         scheduler=='kb',eps,info.ctypes.data)
    if code: raise RuntimeError(code)
    return x,adj,int(info[0]),bool(info[1]),n*k0//2,int(adj.sum()//2)
