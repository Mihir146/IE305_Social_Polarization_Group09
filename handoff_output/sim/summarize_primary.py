"""Summaries of the recommended model; preserve legacy analysis separately."""
from itertools import product
from collections import defaultdict
import json,numpy as np
from summarize_validation import ROOT,read,save,ci,grouped
from metrics import wilson

def main():
    long=read('results_primary.csv');short=read('primary_short_D.csv');out=[];brackets=[]
    for k in [4,8,16]:
        for cap,rs in [(3000,short),(30000,long)]:
            ps=sorted({r['phi'] for r in rs if r['exp']=='D' and r['k0']==k});curve=[]
            for p in ps:
                s=[r for r in rs if r['exp']=='D' and r['k0']==k and r['phi']==p]
                m,lo,hi=ci([r['giant_frac'] for r in s]);f=sum(r['giant_frac']<.9 for r in s);wl,wh=wilson(f,len(s));pf=f/len(s)
                out.append(dict(k0=k,phi=p,cap=cap,n=len(s),S_mean=m,S_lo=lo,S_hi=hi,p_fragmented=pf,p_lo=wl,p_hi=wh,censored=sum(r['censored'] for r in s)))
                curve.append(pf)
            j=next((i for i,x in enumerate(curve) if x>=.5),None)
            brackets.append(dict(k0=k,cap=cap,lower=ps[j-1] if j and j>0 else 0,upper=ps[j] if j is not None else 'unreached',definition='first grid crossing P(S<.9)>=.5'))
    save('primary_horizon_summary.csv',out);save('primary_threshold_brackets.csv',brackets)
    out=[]
    for d,p in product([.15,.25],[.05,.25,1.]):
        a={r['rep']:r for r in long if r['exp']=='B' and r['d']==d and r['phi']==p and r['h']==0}
        b={r['rep']:r for r in long if r['exp']=='B' and r['d']==d and r['phi']==p and r['h']==1};pairs=sorted(a)
        m,lo,hi=ci([b[i]['giant_frac']-a[i]['giant_frac'] for i in pairs]);tm,tl,th=ci([b[i]['sweeps']-a[i]['sweeps'] for i in pairs])
        out.append(dict(d=d,phi=p,n=len(pairs),S_h1_minus_h0=m,lo=lo,hi=hi,time_h0=np.mean([a[i]['sweeps'] for i in pairs]),time_h1=np.mean([b[i]['sweeps'] for i in pairs]),time_difference=tm,time_lo=tl,time_hi=th))
    save('primary_h3_paired.csv',out)
    s=read('primary_kpi_sensitivity.csv');base={(r['rep'],r['d'],r['phi']):r['regime'] for r in s if r['gap']==.05 and r['min_frac']==.05 and r['S_cutoff']==.9};out=[]
    for key,ss in grouped(s,['gap','min_frac','S_cutoff']):
        changed=sum(r['regime']!=base[r['rep'],r['d'],r['phi']] for r in ss)
        out.append(dict(gap=key[0],min_frac=key[1],S_cutoff=key[2],n=len(ss),changed=changed,change_fraction=changed/len(ss)))
    save('primary_sensitivity_summary.csv',out)
    meta=dict(runs=len(long),censored=sum(r['censored'] for r in long),short_D_runs=len(short),isolate_rule='allowed',cap=30000,
              edge_conservation=all(r['edges_start']==r['edges_end'] for r in long))
    (ROOT/'primary_summary.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
if __name__=='__main__':main()
