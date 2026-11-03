"""Traceable final tables; no new model rules or simulation runs."""
from pathlib import Path
from collections import defaultdict
from itertools import product
import json
from analyze import read, load_runs, interval
from run_experiments import save
ROOT=Path(__file__).resolve().parent

def main():
    out=ROOT/'analysis'
    summary=read(out/'policy_summary.csv')+read(ROOT/'budget3_analysis/policy_summary.csv')
    for r in summary:r['n_samples']=12 if r['scenario']=='baseline' else 3
    save(out/'all_policy_summary.csv',summary)
    rows=load_runs(ROOT/'results/main_extended_runs.csv');groups=defaultdict(dict)
    for r in rows:groups[(r['n_samples'],r['price'],r['strategy'],r['h'])][int(r['rep'])]=r
    contrasts=[]
    specs=[('price400_minus500',(s,400.,t,h),(s,500.,t,h)) for s,t,h in product((3.,12.),('random','degree','distributed'),(0.,1.))]
    specs += [('degree_minus_random',(s,p,'degree',h),(s,p,'random',h)) for s,p,h in product((3.,12.),(400.,500.,600.),(0.,1.))]
    specs += [('similar_minus_random_contacts',(s,p,t,1.),(s,p,t,0.)) for s,p,t in product((3.,12.),(400.,500.,600.),('random','degree','distributed'))]
    for kind,lhs,rhs in specs:
        a,b=groups[lhs],groups[rhs];reps=sorted(set(a)&set(b))
        for metric in ('profit','paid_buyers','aware'):
            mean,lo,hi=interval([a[i][metric]-b[i][metric] for i in reps])
            contrasts.append(dict(kind=kind,n_samples=lhs[0],price=lhs[1],strategy=lhs[2],h=lhs[3],metric=metric,n=len(reps),difference=mean,lo=lo,hi=hi))
    save(out/'final_paired_contrasts.csv',contrasts)
    costs=[]
    for (s,p,t,h),sub in sorted(groups.items()):
        for c in (150.,250.,350.,450.):
            mean,lo,hi=interval([(p-c)*r['paid_buyers']-c*s for r in sub.values()])
            costs.append(dict(n_samples=s,price=p,strategy=t,h=h,unit_cost=c,n=len(sub),sample_spend=c*s,profit_mean=mean,lo=lo,hi=hi))
    save(out/'all_cost_revaluation.csv',costs)
    qrows=load_runs(ROOT/'results/quality_diagnostic_runs.csv');qgroups=defaultdict(dict)
    for r in qrows:qgroups[(r['quality'],r['d'],r['phi'])][int(r['rep'])]=r
    qc=[]
    for d,phi in product((.2,1.),(0.,.05)):
        a,b=qgroups[(.95,d,phi)],qgroups[(.6,d,phi)];reps=sorted(a)
        for metric in ('paid_buyers','profit'):
            mean,lo,hi=interval([a[i][metric]-b[i][metric] for i in reps])
            qc.append(dict(contrast='quality095_minus060',d=d,phi=phi,metric=metric,n=len(reps),difference=mean,lo=lo,hi=hi))
    for metric in ('paid_buyers','profit'):
        reps=sorted(qgroups[(.95,1.,0.)])
        x=[(qgroups[(.95,1.,0.)][i][metric]-qgroups[(.6,1.,0.)][i][metric])-(qgroups[(.95,.2,0.)][i][metric]-qgroups[(.6,.2,0.)][i][metric]) for i in reps]
        mean,lo,hi=interval(x);qc.append(dict(contrast='quality_effect_d1_minus_d02_static_graph',d='difference',phi=0,metric=metric,n=len(reps),difference=mean,lo=lo,hi=hi))
    save(out/'quality_paired.csv',qc)
    best=max(summary,key=lambda r:r['profit_mean'])
    evidence=dict(main_policy_evaluations=len(rows),independent_main_markets=100,policy_cells=36,
        fixed_budget_design='18 cells, 12 samples, fixed before main analysis',
        followup_design='18 cells, 3 samples, exploratory follow-up on same 100 markets',
        largest_observed_mean=best,interval_scope='Pointwise 95% market bootstrap; exploratory selection is not an independent confirmation',
        simulation_counts=dict(pilot=540,main_fixed12=1800,budget3_followup=1800,stress=2400,behavior=2100,quality_diagnostic=1200,standalone_java=1080),
        anylogic_engine_status='Awaiting student opening/compilation/run evidence; no engine result inferred from Java')
    (out/'final_evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
    print(json.dumps(evidence,indent=2))
    for r in costs:
        if r['n_samples']==3 and r['strategy']=='degree' and r['h']==0:print(r)
    for r in qc:print(r)
if __name__=='__main__':main()
