"""Audit structural nonfreezing using saved long-cap states, without rerunning.

An agent with no other opinion within d can never gain a compatible opinion:
same-side averages stay outside its confidence interval, while opposite sides
are at least 2d apart and cannot compromise. Isolate protection keeps a last
discordant tie. Such a run cannot meet the original freezing predicate.
"""
from pathlib import Path
import csv,json
import numpy as np
ROOT=Path(__file__).resolve().parent

def components(g):
    seen=np.zeros(len(g),bool);out=[]
    for i in range(len(g)):
        if seen[i]:continue
        seen[i]=True;stack=[i];members=[]
        while stack:
            u=stack.pop();members.append(u)
            v=np.flatnonzero(g[u]&~seen);seen[v]=True;stack.extend(v.tolist())
        out.append(np.array(members))
    return out

def main():
    rows=list(csv.DictReader((ROOT/'long_cap.csv').open()));out=[]
    for r in rows:
        if int(r['censored'])==0:continue
        parts=[r['exp']]+[str(int(r[k])) for k in ['rep','N','k0']]+[str(float(r[k])) for k in ['d','mu','phi','h']]+[str(int(r['init']))]
        path=ROOT/'long_states'/('_'.join(parts)+'.npz')
        with np.load(path) as state:x=state['x'];g=state['adj']
        d=float(r['d']);distance=np.abs(x[:,None]-x[None,:]);np.fill_diagonal(distance,np.inf)
        unmatched=np.all(distance>=d,axis=1);deg=g.sum(axis=1)
        unmatched_with_tie=int(np.count_nonzero(unmatched&(deg>0)))
        blocked=0;safe=True
        for group in components(g):
            if len(group)==2 and g[group[0],group[1]] and abs(x[group[0]]-x[group[1]])>=d:
                blocked+=1
            elif np.ptp(x[group])>=d:
                safe=False
        trapped=bool(blocked and safe and int(r['rewirable_discordant_edges'])==0)
        reason='unmatchable_agent_keeps_a_tie' if unmatched_with_tie else ('blocked_dimer_and_invariant_component_ranges' if trapped else 'unresolved')
        out.append(dict(exp=r['exp'],rep=r['rep'],N=r['N'],k0=r['k0'],d=r['d'],phi=r['phi'],h=r['h'],
                        unmatched_with_ties=unmatched_with_tie,blocked_dimers=blocked,
                        other_component_ranges_below_d=int(safe),proved_nonfreezing=int(unmatched_with_tie>0 or trapped),reason=reason,state_file=str(path.relative_to(ROOT))))
    with (ROOT/'stall_audit.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
    summary=dict(audited=len(out),proved_nonfreezing=sum(r['proved_nonfreezing'] for r in out),
                 unmatched_with_ties=sum(r['unmatched_with_ties']>0 for r in out),
                 remaining_blocked_proofs=sum(r['reason']=='blocked_dimer_and_invariant_component_ranges' for r in out),
                 unresolved=sum(r['reason']=='unresolved' for r in out))
    (ROOT/'stall_audit_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
