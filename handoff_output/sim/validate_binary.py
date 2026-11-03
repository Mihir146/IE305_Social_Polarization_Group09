"""Independent binary benchmark. This is not an extension of the project model."""
from concurrent.futures import ThreadPoolExecutor
from itertools import product
from pathlib import Path
import ctypes as ct,csv,time
import numpy as np
from accelerated import library
from metrics import component_sizes

def regular_graph(n,k,rng):
    # Rejection of the configuration model conditioned on simplicity is uniform
    # over labeled simple k-regular graphs. Reject a whole pairing, not one edge.
    stubs=np.repeat(np.arange(n),k)
    for tries in range(10000):
        a=rng.permutation(stubs).reshape(-1,2)
        if np.any(a[:,0]==a[:,1]):continue
        a=np.sort(a,axis=1)
        if len(np.unique(a[:,0]*n+a[:,1]))!=len(a):continue
        adj=np.zeros((n,n),dtype=np.bool_)
        adj[a[:,0],a[:,1]]=True;adj[a[:,1],a[:,0]]=True
        return adj
    raise RuntimeError('Could not draw a simple regular graph')

def task(job):
    n,p,rep=job;rng=np.random.RandomState(50000+rep)
    g=regular_graph(n,4,rng)
    assert np.all(g.sum(axis=1)==4)
    s=rng.choice([-1,1],size=n).astype(np.int32);state=rng.get_state();info=np.zeros(3)
    initial_plus=float((s==1).mean())
    lib=library();lib.binary_evolve.argtypes=[ct.c_int,ct.c_void_p,ct.c_void_p,
        ct.c_void_p,ct.c_int,ct.c_double,ct.c_int,ct.c_void_p]
    lib.binary_evolve.restype=ct.c_int
    lib.binary_evolve(n,s.ctypes.data,g.ctypes.data,state[1].ctypes.data,state[2],p,30000,info.ctypes.data)
    sizes=component_sizes(g);active=int(np.count_nonzero(np.triu(g & (s[:,None]!=s[None,:]),1)))
    assert active==int(info[2]) and g.sum()==4*n
    assert np.array_equal(g,g.T) and not np.diag(g).any()
    return dict(N=n,k0=4,p=p,rep=rep,seed=50000+rep,cap=30000,sweeps=info[0],
                censored=int(info[1]),giant_frac=sizes[0]/n,
                second_frac=sizes[1]/n if len(sizes)>1 else 0.,n_components=len(sizes),
                active_edges=active,initial_plus=initial_plus,final_plus=float((s==1).mean()))

if __name__=='__main__':
    library();t0=time.time();jobs=list(product([1000],[.2,.3,.35,.38,.4,.45,.6],range(100)))
    out=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for i,r in enumerate(pool.map(task,jobs)):
            out.append(r)
            if i%100==0:print(i,round(time.time()-t0),'s',flush=True)
    with (Path(__file__).resolve().parent/'binary_validation.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    print('done',round(time.time()-t0),'s',flush=True)
