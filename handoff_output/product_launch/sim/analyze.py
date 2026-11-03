"""Run-level uncertainty for product outcomes; customers are clustered by market."""
from pathlib import Path
from collections import defaultdict
from itertools import product,combinations
import csv,json,argparse
import numpy as np
from model import Config,STRATEGIES,check_config
from run_experiments import save
ROOT=Path(__file__).resolve().parent
SEED=20261103

def interval(values,alpha=.05):
    x=np.asarray(values,dtype=float);rng=np.random.default_rng(SEED)
    samples=x[rng.integers(len(x),size=(10000,len(x)))].mean(axis=1)
    lo,hi=np.quantile(samples,[alpha/2,1-alpha/2])
    return float(x.mean()),float(lo),float(hi)

def wilson(k,n):
    z=1.959963984540054;p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den;half=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0,center-half),min(1,center+half)

def read(path):
    with Path(path).open() as f:rows=list(csv.DictReader(f))
    for r in rows:
        for k,v in r.items():
            try:r[k]=float(v)
            except (ValueError,TypeError):pass
    return rows

def load_runs(path):
    rows=read(path);seen=set();cfgfields=Config.__dataclass_fields__
    integers={'N','k0','groups','periods','n_samples'}
    for r in rows:
        check_config(Config(**{k:int(r[k]) if k in integers else r[k] for k in cfgfields}))
        assert all(np.isfinite(v) for v in r.values() if isinstance(v,float))
        key=(r['cohort'],r['scenario'],r['strategy'],r['price'],r['h'],r['rep'])
        if key in seen:raise ValueError('Duplicate market/policy row')
        seen.add(key)
        for field,base in [('graph_seed',1000000),('trait_seed',2000000),('selection_seed',3000000),('event_seed',4000000)]:
            if r[field]!=base+r['rep']:raise ValueError('Unexpected seed mapping')
        if r['free_samples']!=r['n_samples'] or not 0<=r['paid_buyers']<=r['N']-r['n_samples']:raise ValueError('Invalid owner counts')
        if not r['paid_buyers']+r['n_samples']<=r['aware']<=r['N']:raise ValueError('Invalid awareness')
        if abs(r['revenue']-r['price']*r['paid_buyers'])>1e-8:raise ValueError('Revenue identity failed')
        if abs(r['total_cost']-r['unit_cost']*(r['paid_buyers']+r['free_samples']))>1e-8:raise ValueError('Cost identity failed')
        if abs(r['profit']-(r['revenue']-r['total_cost']))>1e-8:raise ValueError('Profit identity failed')
        if r['total_edges']!=r['N']*r['k0']//2:raise ValueError('Edge count mismatch')
    return rows

def policy_key(r):return r['price'],r['strategy'],r['h']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=ROOT/'results/main_runs.csv')
    ap.add_argument('--outdir',type=Path,default=ROOT/'analysis');args=ap.parse_args()
    rows=load_runs(args.input);out=args.outdir;out.mkdir(exist_ok=True,parents=True)
    groups=defaultdict(list)
    for r in rows:groups[(r['scenario'],*policy_key(r))].append(r)
    summaries=[]
    for key,sub in sorted(groups.items()):
        q=dict(scenario=key[0],price=key[1],strategy=key[2],h=key[3],n=len(sub))
        for metric in ['profit','paid_buyers','paid_adoption','aware','min_group_adoption','giant_frac','rewires','restricted_t20']:
            mean,lo,hi=interval([r[metric] for r in sub]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
        hits=sum(r['hit20'] for r in sub);lo,hi=wilson(hits,len(sub))
        q.update(p_hit20=hits/len(sub),p_hit20_lo=lo,p_hit20_hi=hi)
        summaries.append(q)
    save(out/'policy_summary.csv',summaries)
    # These baseline contrasts are paired within a market, not customer-level t-tests.
    contrasts=[]
    baseline=[r for r in rows if r['scenario']=='baseline']
    if baseline:
        bypolicy={k:{int(r['rep']):r for r in baseline if policy_key(r)==k} for k in {policy_key(r) for r in baseline}}
        specs=[]
        for price,h in product((400.,500.,600.),(0.,1.)):
            for lhs,rhs in combinations(STRATEGIES,2):specs.append(('seeding',(price,lhs,h),(price,rhs,h)))
        for price,strategy in product((400.,500.,600.),STRATEGIES):specs.append(('recommendation',(price,strategy,1.),(price,strategy,0.)))
        for kind,lhs,rhs in specs:
            if lhs not in bypolicy or rhs not in bypolicy:continue
            a,b=bypolicy[lhs],bypolicy[rhs];common=sorted(set(a)&set(b))
            for metric in ['profit','paid_buyers','min_group_adoption']:
                mean,lo,hi=interval([a[i][metric]-b[i][metric] for i in common])
                contrasts.append(dict(kind=kind,lhs=str(lhs),rhs=str(rhs),metric=metric,n=len(common),difference=mean,lo=lo,hi=hi))
        save(out/'paired_contrasts.csv',contrasts)
        # Rule is selected using pilot data only; report its held-out comparison.
        pilotpath=ROOT/'results/pilot_runs.csv'
        if pilotpath.exists():
            pilot=load_runs(pilotpath);pg=defaultdict(list)
            for r in pilot:pg[policy_key(r)].append(r['profit'])
            chosen=max(sorted(pg),key=lambda k:np.mean(pg[k]));base=(500.,'random',0.)
            common=sorted(set(bypolicy[chosen])&set(bypolicy[base]))
            mean,lo,hi=interval([bypolicy[chosen][i]['profit']-bypolicy[base][i]['profit'] for i in common])
            selected=dict(selection_rule='Highest pilot mean profit; lexicographic tie-break',
                pilot_selected=dict(price=chosen[0],strategy=chosen[1],h=chosen[2]),
                baseline=dict(price=base[0],strategy=base[1],h=base[2]),
                main_n=len(common),main_profit_difference=mean,lo=lo,hi=hi,
                pilot_replications=sorted({int(r['rep']) for r in pilot}),
                main_replications=common)
            (out/'pilot_selected_evaluation.json').write_text(json.dumps(selected,indent=2)+'\n')
        # Cost does not affect customer dynamics, so revalue the same paid counts.
        costs=[]
        for key,sub in sorted(bypolicy.items()):
            for cost in (150.,250.,350.,450.):
                q=dict(price=key[0],strategy=key[1],h=key[2],unit_cost=cost,n=len(sub),n_samples=12)
                mean,lo,hi=interval([(key[0]-cost)*r['paid_buyers']-cost*r['free_samples'] for r in sub.values()])
                q.update(profit_mean=mean,profit_lo=lo,profit_hi=hi);costs.append(q)
        save(out/'cost_revaluation.csv',costs)
    # Period means bootstrap over markets: the same realization's periods are not pooled.
    name=args.input.name.replace('_runs.csv','_trajectories.csv');tpath=args.input.parent/name
    if tpath.exists():
        tg=defaultdict(list)
        for r in read(tpath):tg[(r['scenario'],r['price'],r['strategy'],r['h'],r['period'])].append(r)
        ts=[]
        for key,sub in sorted(tg.items()):
            q=dict(scenario=key[0],price=key[1],strategy=key[2],h=key[3],period=key[4],n=len(sub))
            for metric in ['aware','paid_buyers','profit','min_group_adoption']:
                mean,lo,hi=interval([r[metric] for r in sub]);q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
            ts.append(q)
        save(out/'trajectory_summary.csv',ts)
    # Conditional conversion: bootstrap markets, retaining customers within their market.
    spath=args.input.parent/args.input.name.replace('_runs.csv','_segments.csv')
    if spath.exists():
        sg=defaultdict(list)
        for r in read(spath):sg[(r['scenario'],r['price'],r['strategy'],r['h'],r['prior_band'],r['affordable'])].append(r)
        ss=[]
        for key,sub in sorted(sg.items()):
            numerator=np.array([r['paid'] for r in sub]);denominator=np.array([r['eligible'] for r in sub]);rng=np.random.default_rng(SEED)
            idx=rng.integers(len(sub),size=(10000,len(sub)));den=denominator[idx].sum(axis=1);num=numerator[idx].sum(axis=1)
            valid=den>0;ratios=num[valid]/den[valid]
            total=denominator.sum();mean=numerator.sum()/total if total else None
            lo,hi=np.quantile(ratios,[.025,.975]) if len(ratios) else (None,None)
            ss.append(dict(scenario=key[0],price=key[1],strategy=key[2],h=key[3],prior_band=key[4],affordable=key[5],
                markets=len(sub),customers=int(total),paid=int(numerator.sum()),conversion=mean,lo=lo,hi=hi))
        save(out/'conditional_conversion.csv',ss)
    info=dict(input=str(args.input),runs=len(rows),markets=len({r['rep'] for r in rows}),
        policy_cells=len(summaries),bootstrap_seed=SEED,bootstrap_resamples=10000,
        intervals='Pointwise95%; market resampling; no global multiple-comparison guarantee',anylogic_executed=False)
    (out/'summary.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info,indent=2))
    for r in sorted(summaries,key=lambda r:r['profit_mean'],reverse=True)[:4]:
        print(r['price'],r['strategy'],r['h'],'profit',round(r['profit_mean'],2),'CI',round(r['profit_lo'],2),round(r['profit_hi'],2))

if __name__=='__main__':main()
