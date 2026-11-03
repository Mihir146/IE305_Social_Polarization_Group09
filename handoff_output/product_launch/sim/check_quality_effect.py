"""Exploratory diagnostic prompted by the unexpected quality sensitivity.

Cross confidence and rewiring at a fixed price to distinguish their roles.
No product rule is changed to manufacture monotonic quality effects.
"""
from pathlib import Path
from itertools import product
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import numpy as np
from model import Config,market,select_samples
from engine import run,library
from run_experiments import summarize_run,save
from analyze import interval
ROOT=Path(__file__).resolve().parent

def work(rep):
    rows=[];contacts=[]
    for quality,d,phi in product((.6,.8,.95),(.2,1.),(0.,.05)):
        c=Config(price=400,h=0,quality=quality,d=d,phi=phi)
        pop=market(c,rep);samples=select_samples(pop,12,'degree')
        r=run(c,rep,'degree',pop=pop,samples=samples)
        scenario=f'q{quality}_d{d}_phi{phi}'
        summary,_,_=summarize_run(c,rep,'degree','quality_diagnostic',scenario,r);rows.append(summary)
        x=pop['prior'].copy();x[samples.astype(bool)]=pop['experience'][samples.astype(bool)]
        ii,jj=np.nonzero(np.triu(pop['adj'],1));mask=samples[ii]!=samples[jj]
        fraction=float(np.mean(np.abs(x[ii[mask]]-x[jj[mask]])<d)) if mask.any() else 0
        contacts.append(dict(rep=rep,quality=quality,d=d,phi=phi,
            sample_nonowner_edges=int(mask.sum()),initial_compatible_fraction=fraction))
    return rows,contacts

def main():
    library();rows=[];contacts=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for r,c in pool.map(work,range(4000,4100)):rows.extend(r);contacts.extend(c)
    save(ROOT/'results/quality_diagnostic_runs.csv',rows);save(ROOT/'results/quality_initial_contact_access.csv',contacts)
    summaries=[]
    for quality,d,phi in product((.6,.8,.95),(.2,1.),(0.,.05)):
        sub=[r for r in rows if (r['quality'],r['d'],r['phi'])==(quality,d,phi)]
        access=[r['initial_compatible_fraction'] for r in contacts if (r['quality'],r['d'],r['phi'])==(quality,d,phi)]
        q=dict(quality=quality,d=d,phi=phi,n=len(sub))
        for metric in ['profit','paid_buyers','aware']:
            mean,lo,hi=interval([r[metric] for r in sub]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
        mean,lo,hi=interval(access);q.update(initial_compatible_mean=mean,initial_compatible_lo=lo,initial_compatible_hi=hi)
        summaries.append(q)
    save(ROOT/'analysis/quality_diagnostic_summary.csv',summaries)
    print('Saved1200 exploratory confidence/rewiring/quality checks')

if __name__=='__main__':main()
