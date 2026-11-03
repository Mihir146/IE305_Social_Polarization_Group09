"""Check accelerated dynamics against the supplied Python implementation."""
import csv
import numpy as np
from accelerated import run as fast
from model import run as reference, kpis

checks=[]
for seed, init, phi, h, isolates in [(3,0,0,0,False),(4,0,.25,1,False),
    (5,1,1,.5,False),(6,2,.05,0,False),(7,0,.5,1,True)]:
    args=(20,4,.2,.3,phi,h,seed,30,init,10)
    a=reference(*args,allow_isolates=isolates)
    b=fast(*args,allow_isolates=isolates)
    assert np.array_equal(a[0],b[0]), (seed,'opinions',np.max(abs(a[0]-b[0])))
    assert np.array_equal(a[1],b[1]), (seed,'graph')
    assert a[2:]==b[2:], (seed,a[2:],b[2:])
    checks.append(dict(check='native_vs_reference',seed=seed,status='PASS'))

# Hand-calculated graph: two triangles, one opinion each, no cross edges.
x=np.array([.2,.2,.2,.8,.8,.8]); adj=np.zeros((6,6),dtype=np.bool_)
for group in [(0,1,2),(3,4,5)]:
    for i in group:
        for j in group:
            if i!=j: adj[i,j]=True
got=kpis(x,adj,6,.05,.05)
assert np.allclose(got,(2,.5,0,2,0,.5,.09)),got
checks.append(dict(check='hand_calculated_KPIs',seed='',status='PASS'))

# A structural property, independent of the implementation's event bookkeeping.
old=np.array([.2,.3]);mu=.3
new=np.array([old[0]+mu*(old[1]-old[0]),old[1]+mu*(old[0]-old[1])])
assert abs(new.mean()-old.mean())<1e-14
assert abs((new.var()-old.var())+2*mu*(1-mu)*(old[0]-old[1])**2/2)<1e-14
checks.append(dict(check='mean_and_variance_identity',seed='',status='PASS'))
with open(__file__.replace('verify_native.py','verification.csv'),'w') as f:
    w=csv.DictWriter(f,fieldnames=['check','seed','status']);w.writeheader();w.writerows(checks)
print('PASS: exact native/reference trajectories (five cases); hand-calculated KPIs')
