"""NumPy/stdlib analysis; no Pandas/SciPy required. All tables are traceable CSV.

New mean intervals are percentile bootstrap intervals (10000 resamples, seed20261103).
Binary proportions use Wilson intervals. Paired contrasts resample whole replicate pairs.
"""
from pathlib import Path
from collections import defaultdict
from itertools import product
import csv,json
import numpy as np
from metrics import wilson,regime

ROOT=Path(__file__).resolve().parent
KEYS=['exp','rep','N','k0','d','mu','phi','h','init']
def read(name):
    with (ROOT/name).open() as f:
        out=[]
        for row in csv.DictReader(f):
            r={}
            for k,v in row.items():
                try:r[k]=float(v)
                except (ValueError,TypeError):r[k]=v
            out.append(r)
        return out
def save(name,rows):
    with (ROOT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ci(x):
    x=np.asarray(x,dtype=float);n=len(x)
    rng=np.random.default_rng(20261103)
    b=np.mean(x[rng.integers(n,size=(10000,n))],axis=1)
    return float(x.mean()),float(np.quantile(b,.025)),float(np.quantile(b,.975))
def grouped(rows,keys):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in keys)].append(r)
    return sorted(groups.items())
def stats(rows,value):
    mean,lo,hi=ci([r[value] for r in rows]);return mean,lo,hi
def main():
    old=read('results.csv');long=read('long_cap.csv');kb=read('kb_validation.csv')
    look={tuple(r[k] for k in KEYS):r for r in long};extended=[]
    for r in old:
        q=dict(r);q.update(look.get(tuple(r[k] for k in KEYS),{}));q['cap']=30000
        q['regime']=regime(q['K'],q['giant_frac']);extended.append(q)
    # Uniform columns; absent diagnostics on originally frozen rows are zeros.
    columns=list(dict.fromkeys(k for r in extended for k in r))
    save('results_long_cap.csv',[{k:r.get(k,0) for k in columns} for r in extended])

    horizon=[]
    for k,p in product([4,8,16],[0,.005,.01,.02,.05,.1,.25]):
        for name,rows in [('3000',old),('30000',extended)]:
            s=[r for r in rows if r['exp']=='D' and r['k0']==k and r['phi']==p]
            mean,lo,hi=stats(s,'giant_frac');n=len(s);f=sum(r['giant_frac']<.9 for r in s)
            wl,wh=wilson(f,n)
            horizon.append(dict(k0=k,phi=p,cap=int(name),n=n,S_mean=mean,S_lo=lo,S_hi=hi,
                p_fragmented=f/n,p_lo=wl,p_hi=wh,censored=sum(r['censored'] for r in s)/n))
    save('horizon_summary.csv',horizon)

    kbs=[]
    for key,s in grouped(kb,['family','n','k0','d','phi']):
        m,lo,hi=stats(s,'path_largest');p90=sum(r['path_largest']>=.9 for r in s);wl,wh=wilson(p90,len(s))
        kbs.append(dict(zip(['family','N','k0','d','w'],key),n_reps=len(s),largest_mean=m,
            largest_lo=lo,largest_hi=hi,second_mean=float(np.mean([r['path_second'] for r in s])),
            clusters_mean=float(np.mean([r['path_clusters'] for r in s])),
            p_largest_ge_90=p90/len(s),p_lo=wl,p_hi=wh,censored=sum(r['censored'] for r in s)))
    save('kb_summary.csv',kbs)

    hks=[]
    for key,s in grouped(read('hk_validation.csv'),['epsilon']):
        f=sum(r['consensus'] for r in s);lo,hi=wilson(f,len(s));m,cl,ch=stats(s,'n_clusters')
        hks.append(dict(epsilon=key[0],n=len(s),p_consensus=f/len(s),p_lo=lo,p_hi=hi,
                         mean_clusters=m,clusters_lo=cl,clusters_hi=ch))
    save('hk_summary.csv',hks)

    bs=[]
    for key,s in grouped(read('binary_validation.csv'),['N','p']):
        m,lo,hi=stats(s,'giant_frac');bs.append(dict(N=key[0],p=key[1],n=len(s),S_mean=m,S_lo=lo,S_hi=hi,
            censored=sum(r['censored'] for r in s),second_mean=float(np.mean([r['second_frac'] for r in s]))))
    save('binary_summary.csv',bs)

    contrasts=[]
    for rules,rows in [('legacy_no_new_isolates',extended),('isolates_allowed',read('isolate_sensitivity.csv'))]:
        for d,p in product([.15,.25],[.05,.25,1.]):
            a={r['rep']:r for r in rows if r['exp']=='B' and r['d']==d and r['phi']==p and r['h']==0}
            b={r['rep']:r for r in rows if r['exp']=='B' and r['d']==d and r['phi']==p and r['h']==1}
            pairs=sorted(set(a)&set(b));m,lo,hi=ci([b[i]['giant_frac']-a[i]['giant_frac'] for i in pairs])
            contrasts.append(dict(rules=rules,d=d,phi=p,n=len(pairs),S_h1_minus_h0=m,lo=lo,hi=hi,
                restricted_mean_sweeps_h0=float(np.mean([a[i]['sweeps'] for i in pairs])),
                restricted_mean_sweeps_h1=float(np.mean([b[i]['sweeps'] for i in pairs])),
                censored_h0=float(np.mean([a[i]['censored'] for i in pairs])),
                censored_h1=float(np.mean([b[i]['censored'] for i in pairs]))))
    save('h3_paired.csv',contrasts)

    sens=read('kpi_sensitivity.csv');s=[r for r in sens if r['exp']=='A']
    base={(r['rep'],r['d'],r['phi']):r['regime'] for r in s if r['gap']==.05 and r['min_frac']==.05 and r['S_cutoff']==.9}
    sr=[]
    for key,ss in grouped(s,['gap','min_frac','S_cutoff']):
        changes=sum(r['regime']!=base[r['rep'],r['d'],r['phi']] for r in ss)
        sr.append(dict(gap=key[0],min_frac=key[1],S_cutoff=key[2],n=len(ss),changed=changes,change_fraction=changes/len(ss)))
    save('sensitivity_summary.csv',sr)

    active=[r for r in long if r['censored']]
    meta=dict(original_runs=len(old),original_censored=sum(int(r['censored']) for r in old),
        extended_censored=len(active),new_kb_runs=len(kb),new_hk_runs=len(read('hk_validation.csv')),
        new_binary_runs=len(read('binary_validation.csv')),
        isolate_sensitivity_runs=len(read('isolate_sensitivity.csv')),
        blocked_censored=sum(r['rewirable_discordant_edges']==0 and r['unsettled_compatible_edges']==0 for r in active),
        censored_all_discordant_edges_touch_unmatchable=sum(r['discordant_edges']==r['discordant_with_unmatchable_endpoint'] for r in active),
        isolate_sensitivity_censored=sum(r['censored'] for r in read('isolate_sensitivity.csv')),
        reproduced_output_rows=sum(r['matches_saved'] for r in read('replay_validation.csv')),
        bootstrap_seed=20261103,bootstrap_resamples=10000)
    (ROOT/'validation_summary.json').write_text(json.dumps(meta,indent=2)+'\n')
    print(json.dumps(meta,indent=2))

if __name__=='__main__':main()
