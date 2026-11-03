"""Analyze a reference/AnyLogic CSV. NumPy only for tables; Matplotlib for PNGs.

Example: python sim/analyze.py --input anylogic.csv --outdir sim/anylogic_analysis
Mean intervals: seeded percentile bootstrap. Proportions: Wilson95%.
"""
from pathlib import Path
from collections import defaultdict
import argparse,csv,json
import numpy as np
from metrics import regime,wilson
from summarize_validation import ci

ROOT=Path(__file__).resolve().parent
SCHEMA='exp,rep,seed,N,k0,d,mu,phi,h,init,sweeps,censored,edges_start,edges_end,n_components,giant_frac,isolated_frac,K,cross_frac,Q,opinion_var,secs'.split(',')
SCENARIO=['exp','N','k0','d','mu','phi','h','init']
LABELS=['One major cluster, large component','Multiple major clusters, large component',
        'One major cluster, fragmented','Multiple major clusters, fragmented','No major opinion cluster']
COLORS=['#26845b','#e5a331','#75818a','#bd3e47','#665a93']

def load_csv(path):
    with Path(path).open() as f:
        reader=csv.DictReader(f)
        missing=set(SCHEMA)-set(reader.fieldnames or [])
        if missing:raise ValueError('Missing CSV columns: '+', '.join(sorted(missing)))
        rows=[]
        for line,row in enumerate(reader,2):
            r=dict(row)
            for k in SCHEMA[1:]:r[k]=float(row[k])
            if not all(np.isfinite(r[k]) for k in SCHEMA[1:]):raise ValueError(f'Nonfinite value at line {line}')
            for k in ['rep','seed','N','k0','init','sweeps','censored','edges_start','edges_end','n_components','K']:
                if r[k]!=int(r[k]):raise ValueError(f'{k} must be an integer at line {line}')
            if r['N']<2 or not 0<=r['k0']<r['N']:raise ValueError('Invalid population size or degree')
            if r['rep']<0 or r['seed']<0 or r['init'] not in (0,1,2):raise ValueError('Invalid replication, seed or initialization')
            if not (0<r['d']<=1 and 0<r['mu']<=.5 and 0<=r['phi']<=1 and 0<=r['h']<=1):raise ValueError('Invalid model parameters')
            if r['edges_start']!=r['edges_end']:raise ValueError(f'Edge count changed at line {line}')
            if r['edges_start']!=int(r['N']*r['k0']//2):raise ValueError('Edge count does not match G(N,M) initialization')
            if r['censored'] not in (0,1):raise ValueError('censored must be 0 or 1')
            if not all(0<=r[k]<=1 for k in ['giant_frac','cross_frac','isolated_frac']):raise ValueError('Fraction outside [0,1]')
            if not (1<=r['n_components']<=r['N'] and 0<=r['K']<=r['N']):raise ValueError('Invalid component/cluster count')
            if r['sweeps']<1 or r['secs']<0 or not 0<=r['opinion_var']<=.25+1e-12:raise ValueError('Invalid time or variance')
            for k in ['cap','allow_isolates']:
                if k in r:
                    r[k]=float(r[k])
                    if not np.isfinite(r[k]) or r[k]!=int(r[k]):raise ValueError('Invalid '+k)
            if 'cap' in r and (r['cap']<r['sweeps'] or r['cap']<1):raise ValueError('Invalid observation cap')
            if 'allow_isolates' in r and r['allow_isolates'] not in (0,1):raise ValueError('Invalid isolate rule')
            rows.append(r)
    if not rows:raise ValueError('CSV has no runs')
    for k in ['cap','allow_isolates']:
        if k in rows[0] and len({r[k] for r in rows})>1:
            raise ValueError(f'Analyze one {k} value at a time; split the CSV first')
    seen=set();seeds=set()
    for r in rows:
        key=tuple(r[k] for k in SCENARIO+['rep'])
        if key in seen:raise ValueError('Duplicate scenario/rep row; do not count reruns as new replications')
        seen.add(key)
        seedkey=tuple(r[k] for k in SCENARIO+['seed'])
        if seedkey in seeds:raise ValueError('A scenario repeats a seed across replication indices')
        seeds.add(seedkey)
    return rows

def save(path,rows):
    with Path(path).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def summarize(rows,cutoff):
    groups=defaultdict(list)
    for r in rows:groups[tuple(r[k] for k in SCENARIO)].append(r)
    out=[]
    for key,s in sorted(groups.items()):
        q=dict(zip(SCENARIO,key));n=len(s);k=sum(r['giant_frac']<cutoff for r in s);lo,hi=wilson(k,n)
        q.update(n=n,p_fragmented=k/n,p_fragmented_lo=lo,p_fragmented_hi=hi,
                 censored_fraction=float(np.mean([r['censored'] for r in s])))
        for metric in ['giant_frac','K','cross_frac','Q','opinion_var','sweeps']:
            mean,lo,hi=ci([r[metric] for r in s])
            q.update({metric+'_mean':mean,metric+'_lo':lo,metric+'_hi':hi})
        out.append(q)
    return out

def make_plots(rows,out):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
    except ImportError:
        print('Tables written. Matplotlib is unavailable; interactive validation charts are in results_explorer.html.')
        return
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    A=[r for r in rows if r['exp']=='A']
    if A:
        for k in ['N','k0','mu','h','init']:
            if len({r[k] for r in A})>1:raise ValueError('Split A runs by '+k+' before plotting')
        ds=sorted({r['d'] for r in A});ps=sorted({r['phi'] for r in A})
        fig,axs=plt.subplots(1,3,figsize=(14,4))
        for ax,metric,title in zip(axs,['K','giant_frac','censored'],['Major opinion clusters K','Largest component S','Fraction capped']):
            z=np.full((len(ds),len(ps)),np.nan)
            for i,d in enumerate(ds):
                for j,p in enumerate(ps):
                    ss=[r[metric] for r in A if r['d']==d and r['phi']==p]
                    if ss:z[i,j]=np.mean(ss)
            im=ax.imshow(z,origin='lower',aspect='auto');ax.set_title(title)
            ax.set_xticks(range(len(ps)),labels=ps,rotation=45);ax.set_yticks(range(len(ds)),labels=ds)
            ax.set_xlabel('Rewiring probability φ');ax.set_ylabel('Tolerance d');fig.colorbar(im,ax=ax)
        fig.suptitle('Fixed-horizon measurements; capped runs are snapshots')
        fig.tight_layout();fig.savefig(out/'fig1_expA_heatmaps.png',dpi=180);plt.close(fig)
        fig,axs=plt.subplots(1,len(ds),figsize=(max(6,3*len(ds)),4),squeeze=False,sharey=True)
        for ax,d in zip(axs[0],ds):
            bottom=np.zeros(len(ps))
            for label,color in zip(LABELS,COLORS):
                v=[]
                for p in ps:
                    ss=[r for r in A if r['d']==d and r['phi']==p]
                    v.append(np.mean([r['regime']==label for r in ss]) if ss else 0)
                ax.bar(range(len(ps)),v,bottom=bottom,label=label,color=color);bottom+=v
            ax.set_title('d='+str(d));ax.set_xticks(range(len(ps)),labels=ps,rotation=45)
        axs[0][0].set_ylabel('Replication fraction');axs[0][-1].legend(fontsize=7)
        fig.tight_layout();fig.savefig(out/'fig2_regimes.png',dpi=180);plt.close(fig)
    for exp,factor,filename in [('B','h','fig4_expB_selection.png'),('D','k0','fig3_expD_meandegree.png')]:
        sub=[r for r in rows if r['exp']==exp]
        if not sub:continue
        ds=sorted({r['d'] for r in sub})
        fig,axs=plt.subplots(1,len(ds),figsize=(6*len(ds),4),squeeze=False)
        for ax,d in zip(axs[0],ds):
            for v in sorted({r[factor] for r in sub}):
                ps=sorted({r['phi'] for r in sub if r['d']==d and r[factor]==v});ms=[]
                for p in ps:ms.append(ci([r['giant_frac'] for r in sub if r['d']==d and r[factor]==v and r['phi']==p]))
                means=np.array([m[0] for m in ms]);lo=means-np.array([m[1] for m in ms]);hi=np.array([m[2] for m in ms])-means
                ax.errorbar(range(len(ps)),means,yerr=[lo,hi],marker='o',capsize=3,label=f'{factor}={v:g}')
                ax.set_xticks(range(len(ps)),labels=ps,rotation=45)
            ax.set_ylim(0,1.05);ax.set_xlabel('Rewiring probability φ');ax.set_ylabel('Largest component S');ax.legend();ax.set_title(f'{exp}, d={d:g}; horizon-specific')
        fig.tight_layout();fig.savefig(out/filename,dpi=180);plt.close(fig)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=ROOT/'results_primary.csv')
    ap.add_argument('--outdir',type=Path,default=ROOT/'analysis')
    ap.add_argument('--S-cutoff',type=float,default=.9);ap.add_argument('--tables-only',action='store_true');args=ap.parse_args()
    rows=load_csv(args.input);args.outdir.mkdir(parents=True,exist_ok=True)
    for r in rows:r['regime']=regime(r['K'],r['giant_frac'],args.S_cutoff)
    summary=summarize(rows,args.S_cutoff)
    save(args.outdir/'results_with_regimes.csv',rows);save(args.outdir/'scenario_summary.csv',summary)
    info=dict(input=str(args.input.resolve()),runs=len(rows),scenarios=len(summary),
              censored=sum(r['censored'] for r in rows),S_cutoff=args.S_cutoff,
              mean_CI='percentile bootstrap95%',proportion_CI='Wilson95%',bootstrap_seed=20261103)
    (args.outdir/'summary.json').write_text(json.dumps(info,indent=2)+'\n')
    (args.outdir/'summary.txt').write_text(json.dumps(info,indent=2)+'\nSee scenario_summary.csv for intervals.\n')
    if not args.tables_only:make_plots(rows,args.outdir)
    print(json.dumps(info,indent=2))
if __name__=='__main__':main()
