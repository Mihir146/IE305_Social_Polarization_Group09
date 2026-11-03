"""Meaningful product invariants, exact limits and independent engine comparison."""
from pathlib import Path
from dataclasses import replace
import csv,json
import numpy as np
from model import Config,market,select_samples,run_reference,DAY_COLUMNS
from engine import run,verify_run
ROOT=Path(__file__).resolve().parent

def main():
    checks=[]
    def passed(name,detail):checks.append(dict(check=name,status='PASS',evidence=detail))
    for rep,strategy,h,price in [(0,'random',0,400),(1,'degree',1,500),(2,'distributed',0,600),(3,'random',1,500),(4,'distributed',1,0)]:
        c=Config(N=18,k0=4,n_samples=3,periods=8,h=h,price=price)
        a=run_reference(c,rep,strategy);b=run(c,rep,strategy)
        for k in ['x','adj','aware','samples','paid_period','aware_period','value_at_purchase']:
            assert np.array_equal(a['state'][k],b['state'][k]),(rep,k)
        assert np.allclose(a['daily'],b['daily'],atol=1e-12,rtol=1e-12)
        passed('native_reference_'+str(rep),'Exact customer states, graph, awareness, purchases and purchase values; daily metrics agree to1e-12')
    c=Config(N=30,k0=4,n_samples=0,periods=8,price=0)
    r=run(c,5,'random');assert r['daily'][-1,1]==r['daily'][-1,2]==0
    passed('no_launch_no_purchases','With no seeds and no awareness, even zero price produces no purchases')
    c=replace(c,n_samples=3,share_prob=0,price=500)
    r=run(c,5,'degree');assert r['daily'][-1,1]==3 and r['daily'][-1,2]==0 and r['daily'][-1,7]==-750
    passed('zero_sharing','Only3 sampled owners aware;0 paid buyers;profit−750')
    c=replace(c,share_prob=1,price=1001)
    r=run(c,5,'distributed');assert r['daily'][-1,2]==0
    passed('unattainable_price','Price exceeds every value scale, so no paid purchase is possible')
    c=replace(c,price=0);pop=market(c,5)
    r=run(c,5,'random',pop=pop,initial_aware=np.ones(c.N,dtype=np.uint8))
    assert r['daily'][1,2]==27 and r['daily'][-1,2]==27 and r['daily'][-1,3]==3
    assert r['daily'][-1,5]==0 and r['daily'][-1,6]==30*c.unit_cost
    passed('all_aware_zero_price','Exactly27 paid/free-price purchases plus3 samples; never30 paid sales; all30 production costs charged')
    c=Config(N=2,k0=1,n_samples=0,periods=1,price=1001,phi=0)
    pop=market(c,0);pop['prior']=np.array([.2,.3])
    r=run(c,0,'random',pop=pop,initial_aware=np.ones(2,dtype=np.uint8))
    assert np.allclose(r['state']['x'],[.242,.258],atol=1e-15)
    assert abs(r['state']['x'].mean()-.25)<1e-15
    assert abs(r['state']['x'].var()-.000064)<1e-15
    passed('two_compromises_hand_calculation','One2-agent period has2 activations: (.2,.3)→(.23,.27)→(.242,.258);mean.25,variance.000064')
    c=Config(N=3,k0=1,n_samples=0,periods=1,price=1001,phi=1,h=1)
    pop=market(c,0);pop['adj'][:]=0;pop['adj'][0,1]=pop['adj'][1,0]=1
    pop['prior']=np.array([.1,.9,.1])
    r=run(c,0,'random',pop=pop,initial_aware=np.ones(3,dtype=np.uint8),attempts=1,event_seed=5)
    assert r['state']['adj'][0,2] and not r['state']['adj'][0,1] and not r['state']['adj'][1].any()
    passed('rewire_before_cut','Forced one-activation fixture replaces(0,1)by(0,2);old neighbor excluded;one edge retained;isolate allowed')
    pop['prior']=np.array([.1,.9,.5])
    r=run(c,0,'random',pop=pop,initial_aware=np.ones(3,dtype=np.uint8),attempts=1,event_seed=5)
    assert r['state']['adj'][0,2]
    passed('empty_similar_set_fallback','No compatible candidate;uniform non-neighbor fallback reconnects to2')
    c=replace(c,k0=2);pop=market(c,0)
    r=run(c,0,'random',pop=pop,initial_aware=np.ones(3,dtype=np.uint8),attempts=1,event_seed=5)
    assert np.array_equal(r['state']['adj'],pop['adj'])
    passed('no_candidate_complete_graph','Complete graph has no eligible replacement;no edge lost')
    c=Config();p=market(c,0);mask=select_samples(p,12,'distributed')
    assert np.array_equal(np.bincount(p['group'],weights=mask),[4,4,4])
    passed('equal_budget_and_group_allocation','Distributed strategy gives exactly4 samples/group,12 total')
    p2=market(replace(c,within_weight=12,price=600,h=1),0)
    for k in ['prior','value_scale','budget','experience','priority']:assert np.array_equal(p[k],p2[k])
    passed('separate_initialization_streams','Changing graph clustering/price/h leaves customer attributes and selection priority identical at fixed rep')
    for strategy in ('random','degree','distributed'):
        for h in (0,1):
            r=run(replace(c,h=h),10,strategy)
            verify_run(replace(c,h=h),r)
    passed('full_market_invariants','Six300-person/60-period runs pass awareness-before-purchase,affordability,value,no double/sample sales,edge and accounting assertions')
    with (ROOT/'verification.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(checks[0]));w.writeheader();w.writerows(checks)
    (ROOT/'verification_summary.json').write_text(json.dumps(dict(checks=len(checks),passed=len(checks),anylogic_executed=False),indent=2)+'\n')
    print('PASS:',len(checks),'product checks; AnyLogic execution still pending')

if __name__=='__main__':main()
