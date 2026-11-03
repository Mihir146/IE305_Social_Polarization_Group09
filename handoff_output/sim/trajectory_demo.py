"""One illustrative realization replayed to several horizons, not independent reps."""
from pathlib import Path
import numpy as np
from accelerated import run,initial
from metrics import measures
from analyze import save
ROOT=Path(__file__).resolve().parent
rows=[];states={}
for phi in [0.,.005]:
    for t in [0,10,30,100,300,1000,3000,6000,10000,30000]:
        if t==0:x,g,_=initial(300,8,1000);actual=0
        else:x,g,actual,_,_,_=run(300,8,.2,.3,phi,1.,1000,t,0,10,allow_isolates=True)
        rows.append(dict(seed=1000,N=300,k0=8,d=.2,mu=.3,phi=phi,h=1.,allow_isolates=1,requested_sweep=t,actual_sweep=actual,**measures(x,g,.2)))
        states[f'x_phi{phi}_t{t}']=x;states[f'adj_phi{phi}_t{t}']=g
save(ROOT/'trajectory_demo.csv',rows);np.savez_compressed(ROOT/'trajectory_states.npz',**states)
print('Saved one realization at ten horizons for each of two phi values')
