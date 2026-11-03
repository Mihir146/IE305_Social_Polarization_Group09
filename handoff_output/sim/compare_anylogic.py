"""Independent bootstrap differences, not overlap of two confidence intervals.

AnyLogic results are pending. This script does not fabricate a comparison.
"""
from pathlib import Path
from collections import defaultdict
import argparse,csv
import numpy as np
from analyze import load_csv,SCENARIO,save

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--anylogic',required=True,type=Path)
    ap.add_argument('--reference',type=Path,default=Path(__file__).resolve().parent/'results_primary.csv')
    ap.add_argument('--out',type=Path,default=Path('anylogic_comparison.csv'));a=ap.parse_args()
    java=load_csv(a.anylogic);ref=load_csv(a.reference);groups=defaultdict(list)
    for r in ref:groups[tuple(r[k] for k in SCENARIO)].append(r)
    jgroups=defaultdict(list)
    for r in java:jgroups[tuple(r[k] for k in SCENARIO)].append(r)
    out=[]
    for key,js in sorted(jgroups.items()):
        rs=groups.get(key)
        if not rs:raise ValueError('No matching reference scenario: '+str(key))
        # Never compare different horizons or isolate rules as implementation checks.
        for field,default in [('cap',3000),('allow_isolates',0)]:
            jvals={float(r.get(field,default)) for r in js};rvals={float(r.get(field,default)) for r in rs}
            if jvals!=rvals:raise ValueError('Mismatch in '+field)
        for metric in ['giant_frac','K','cross_frac','opinion_var']:
            x=np.array([r[metric] for r in js]);y=np.array([r[metric] for r in rs])
            rng=np.random.default_rng(20261103)
            dif=x[rng.integers(len(x),size=(10000,len(x)))].mean(axis=1)-y[rng.integers(len(y),size=(10000,len(y)))].mean(axis=1)
            lo,hi=np.quantile(dif,[.025,.975]);delta=x.mean()-y.mean()
            q=dict(zip(SCENARIO,key));q.update(metric=metric,n_anylogic=len(x),n_reference=len(y),
                anylogic_mean=x.mean(),reference_mean=y.mean(),difference=delta,lo=lo,hi=hi,
                includes_zero=int(lo<=0<=hi),S_equivalent_within_point05=int(lo>=-.05 and hi<=.05) if metric=='giant_frac' else '')
            out.append(q)
    save(a.out,out);print('Wrote',a.out,'; interpret low-power nonrejection separately from equivalence.')
if __name__=='__main__':main()
