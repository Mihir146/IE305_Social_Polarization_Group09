"""Independent-distribution comparison or exact matching to the same Java kernel."""
from pathlib import Path
from collections import defaultdict
import argparse
import numpy as np
from analyze import load_runs,interval
from run_experiments import save
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True)
    ap.add_argument('--reference',type=Path,default=ROOT/'results/main_runs.csv')
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--exact-java',action='store_true');a=ap.parse_args()
    candidate=load_runs(a.candidate);reference=load_runs(a.reference)
    factors=list(ConfigFields())
    ref=defaultdict(list)
    for r in reference:ref[tuple(r[k] for k in factors)].append(r)
    groups=defaultdict(list)
    for r in candidate:groups[tuple(r[k] for k in factors)].append(r)
    out=[]
    if a.exact_java:
        match={tuple(r[k] for k in factors+['rep']):r for r in reference}
        for r in candidate:
            target=match.get(tuple(r[k] for k in factors+['rep']))
            if target is None:raise ValueError('Missing matching Java-kernel realization')
            errors=[]
            for k,v in r.items():
                if k in ('cohort','secs'):continue
                if isinstance(v,float):
                    if abs(v-target[k])>1e-10:errors.append(k)
                elif v!=target[k]:errors.append(k)
            out.append(dict(policy=str(tuple(r[k] for k in ['price','strategy','h'])),rep=r['rep'],exact_match=int(not errors),different_fields=';'.join(errors)))
    else:
        for key,sub in sorted(groups.items()):
            other=ref.get(key)
            if not other:raise ValueError('No matching reference policy/configuration')
            for metric in ['paid_buyers','profit','aware']:
                x=np.array([r[metric] for r in sub]);y=np.array([r[metric] for r in other]);rng=np.random.default_rng(20261103)
                dif=x[rng.integers(len(x),size=(10000,len(x)))].mean(axis=1)-y[rng.integers(len(y),size=(10000,len(y)))].mean(axis=1)
                lo,hi=np.quantile(dif,[.025,.975])
                out.append(dict(price=sub[0]['price'],strategy=sub[0]['strategy'],h=sub[0]['h'],metric=metric,
                    n_candidate=len(x),n_reference=len(y),candidate_mean=x.mean(),reference_mean=y.mean(),
                    difference=x.mean()-y.mean(),lo=lo,hi=hi,includes_zero=int(lo<=0<=hi),
                    scope='Distribution diagnostic; not empirical validation or automatic equivalence'))
    save(a.out,out);print('Wrote',len(out),'comparisons to',a.out)

def ConfigFields():
    from model import Config
    return ['scenario','strategy',*Config.__dataclass_fields__]

if __name__=='__main__':main()
