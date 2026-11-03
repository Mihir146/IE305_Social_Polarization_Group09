"""Small structural checks of the recommended isolate-allowed model."""
import numpy as np
try:
    from numba import njit
    from model import run
except ImportError:
    from accelerated import run
for phi in [0.,.25,1.]:
    x,g,sw,cens,e0,e1=run(20,4,.2,.3,phi,1.,1000,200,0,10,allow_isolates=True)
    assert e0==e1==40
    assert np.array_equal(g,g.T) and not np.diag(g).any()
    assert np.isfinite(x).all() and x.min()>=0 and x.max()<=1
    print('phi',phi,'edges',e1,'sweeps',sw,'capped',cens)
print('PASS: structural sanity; not a validation of AnyLogic or real populations')
