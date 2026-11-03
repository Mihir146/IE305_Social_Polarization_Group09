"""Summarize focused robustness and generated input statistics."""
from pathlib import Path
from collections import defaultdict
from itertools import product
import numpy as np
from analyze import read,load_runs,interval
from run_experiments import save
ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'analysis';out.mkdir(exist_ok=True)
    for name in ['stress','behavior']:
        rows=load_runs(ROOT/f'results/{name}_runs.csv');g=defaultdict(list)
        for r in rows:g[(r['scenario'],r['price'],r['strategy'],r['h'])].append(r)
        summary=[]
        for key,sub in sorted(g.items()):
            q=dict(scenario=key[0],price=key[1],strategy=key[2],h=key[3],n=len(sub),n_samples=sub[0]['n_samples'],within_weight=sub[0]['within_weight'],d=sub[0]['d'],share_prob=sub[0]['share_prob'],quality=sub[0]['quality'])
            for metric in ['profit','paid_buyers','aware','min_group_adoption']:
                mean,lo,hi=interval([r[metric] for r in sub]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
            summary.append(q)
        save(out/f'{name}_summary.csv',summary)
    stress=read(ROOT/'results/stress_trajectories.csv');g=defaultdict(list)
    for r in stress:
        if r['period'] in (7,60):g[(r['scenario'],r['strategy'],r['h'],r['period'])].append(r)
    summary=[];contrasts=[]
    for key,sub in sorted(g.items()):
        q=dict(scenario=key[0],strategy=key[1],h=key[2],period=key[3],n=len(sub))
        for metric in ['aware','paid_buyers','profit','min_group_adoption']:
            mean,lo,hi=interval([r[metric] for r in sub]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
        summary.append(q)
    save(out/'stress_horizons.csv',summary)
    for scenario,h,period in product(sorted({r['scenario'] for r in stress}),(0.,1.),(7.,60.)):
        a={int(r['rep']):r for r in g[(scenario,'distributed',h,period)]}
        b={int(r['rep']):r for r in g[(scenario,'degree',h,period)]}
        for metric in ['aware','paid_buyers','profit','min_group_adoption']:
            mean,lo,hi=interval([a[i][metric]-b[i][metric] for i in sorted(a)])
            contrasts.append(dict(scenario=scenario,h=h,period=period,metric=metric,n=len(a),distributed_minus_degree=mean,lo=lo,hi=hi))
    save(out/'stress_paired.csv',contrasts)
    inputs=read(ROOT.parent/'data/customers_rep1000.csv');statistics=[]
    for field in ['initial_belief','value_scale','budget','experience_signal']:
        x=np.array([r[field] for r in inputs]);statistics.append(dict(input=field,n=len(x),mean=x.mean(),sample_sd=x.std(ddof=1),minimum=x.min(),maximum=x.max()))
    contacts=read(ROOT.parent/'data/contacts_rep1000.csv');degree=np.zeros(len(inputs),dtype=int);cross=0
    for r in contacts:
        i,j=int(r['customer_i']),int(r['customer_j']);degree[i]+=1;degree[j]+=1;cross+=inputs[i]['group']!=inputs[j]['group']
    statistics.append(dict(input='initial_degree',n=len(degree),mean=degree.mean(),sample_sd=degree.std(ddof=1),minimum=degree.min(),maximum=degree.max()))
    save(out/'input_statistics.csv',statistics)
    save(out/'initial_graph_statistics.csv',[dict(rep=1000,N=len(inputs),edges=len(contacts),mean_degree=degree.mean(),cross_group_edges=cross,cross_group_fraction=cross/len(contacts),isolates=int(np.count_nonzero(degree==0)))])
    print('Wrote sensitivity, paired horizons and actual synthetic-input statistics')

if __name__=='__main__':main()
