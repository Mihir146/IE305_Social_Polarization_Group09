"""Build standard Plotly scientific figures with embedded data and offline tables.

The HTML loads Plotly from its official CDN. No observations are fetched online.
Use its camera button to export a chart in a browser. Rendering is a browser step.
"""
from pathlib import Path
import csv,html,json
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent

def read(name):
    with (ROOT/name).open() as f:
        rows=list(csv.DictReader(f))
    for r in rows:
        for k,v in r.items():
            try:r[k]=float(v)
            except (ValueError,TypeError):pass
    return rows

def main():
    names=['primary_horizon_summary.csv','primary_h3_paired.csv','kb_summary.csv',
           'hk_summary.csv','binary_summary.csv','primary_sensitivity_summary.csv',
           'trajectory_demo.csv','application_summary.csv','application_paired.csv',
           'primary_analysis/scenario_summary.csv']
    data={n:read(n) for n in names}
    panels=[
      ('primary','More contacts delay fragmentation in this scenario',
       'Primary model: isolates allowed; N=300,d=.2,μ=.3,h=1;30 runs/cell. Bars are pointwise95% bootstrap intervals. The x axis uses the tested φ categories, not a continuous fitted phase diagram.',
       'primary_horizon_summary.csv',['k0','phi','cap','n','S_mean','S_lo','S_hi','p_fragmented','censored']),
      ('policy','Contact policy: compare the path and the final state',
       'Six synthetic policies; φ=.005,d=.2,N=300,μ=.3;30 realizations/policy. Snapshots of a realization are repeated measures. Change the horizon to see how a policy comparison changes. “Cross links” use gap labels and do not measure hostility.',
       'application_summary.csv',['k0','h','cap','n','contacts','giant_frac_mean','cross_frac_mean','capped']),
      ('heatmap','Tolerance and rewiring: two outcomes, measured separately',
       'Primary A grid; N=300,k₀=8,μ=.3,h=1,30 runs/cell,cap30000,isolates allowed. K counts major gap groups. K=1 is not strict consensus.',
       'primary_analysis/scenario_summary.csv',['exp','d','phi','n','giant_frac_mean','K_mean','censored_fraction']),
      ('kb','Kozma–Barrat: a partial quantitative reproduction',
       'KB scheduler, μ=.5,h=0,isolates allowed,N=1000,k̄=10,100 runs/point. Path clusters are used. The dashed .256 line is a published approximate reference, not a fitted critical value. Eight w=.9 runs remain capped.',
       'kb_summary.csv',['family','N','k0','d','w','n_reps','largest_mean','censored']),
      ('hk','A separate HK benchmark reproduces the finite-N pattern',
       'Synchronous, self-inclusive complete-population averaging;625 agents,100 runs/tolerance. .25 is a finite-N benchmark, not a universal constant. Proportion bars are Wilson95% intervals.',
       'hk_summary.csv',['epsilon','n','p_consensus','p_lo','p_hi','mean_clusters']),
      ('binary','A separate binary benchmark approaches two large pieces',
       'Vazquez copying/rewire-to-same rules; simple4-regular graph,N=1000,100 runs/point. All700 runs absorb. The .38 line is the approximate published transition; our grid does not fit a critical exponent or precise critical point.',
       'binary_summary.csv',['p','n','S_mean','S_lo','S_hi','second_mean','censored']),
      ('h3','The original contact-selection hypothesis was not supported',
       'Primary B: h=1 minus h=0 final largest-component fraction;30 paired runs/cell. Every95% bootstrap interval includes zero. This does not demonstrate equivalence or cover untested scenarios.',
       'primary_h3_paired.csv',['d','phi','n','S_h1_minus_h0','lo','hi','time_h0','time_h1']),
      ('sensitivity','Minority size affects more classifications than the other cutoffs',
       'Reclassify the same1440 primary A states. Each bar changes only one choice from gap=.05,minimum=.05,S cutoff=.9. Counts are changed labels, not new simulation outcomes.',
       'primary_sensitivity_summary.csv',['gap','min_frac','S_cutoff','n','changed']),
      ('trajectory','One realization: opinions settle before the last bridges disappear',
       'Illustration only: seed1000,N=300,k₀=8,d=.2,μ=.3,h=1,φ=.005,isolates allowed. Requested horizons after numerical freezing reuse the frozen state. These ten points are not independent replications. At time0 a diffuse distribution can already have K=1.',
       'trajectory_demo.csv',['phi','requested_sweep','actual_sweep','giant_frac','cross_frac','opinion_var','K'])
    ]
    sections=[]
    for pid,title,caption,source,cols in panels:
        rows=data[source]
        if pid=='heatmap':rows=[r for r in rows if r['exp']=='A']
        if pid=='kb':rows=[r for r in rows if r['family']=='kb_d1']
        if pid=='trajectory':rows=[r for r in rows if r['phi']==.005]
        controls=''
        if pid=='policy':
            controls='<label>Observation horizon: <select id="policyCap">'+''.join(f'<option>{c}</option>' for c in [300,1000,3000,30000,300000])+'</select> sweeps</label>'
        table='<thead><tr>'+''.join('<th>'+html.escape(c)+'</th>' for c in cols)+'</tr></thead><tbody>'
        for r in rows:
            table+='<tr>'+''.join('<td>'+html.escape(f'{r[c]:.5g}' if isinstance(r[c],float) else str(r[c]))+'</td>' for c in cols)+'</tr>'
        table+='</tbody>'
        sections.append(f'<section id="{pid}"><h2>{html.escape(title)}</h2><p>{html.escape(caption)}</p>{controls}<div class="plot" id="plot_{pid}"></div><p class="source">Source: <a href="sim/{source}">{source}</a></p><details><summary>Numerical table (works offline)</summary><div class="table"><table>{table}</table></div></details></section>')
    script=r'''
const D=__DATA__;
const pal=['#125c8a','#c35b2c','#34835c','#855798'];
const config={responsive:true,displaylogo:false,toImageButtonOptions:{format:'png',width:1400,height:800,scale:2}};
const base={font:{family:'Arial, sans-serif',size:14,color:'#183044'},paper_bgcolor:'#fff',plot_bgcolor:'#fff',margin:{l:75,r:45,t:30,b:80},legend:{orientation:'h',y:1.16},hovermode:'closest'};
const err=(rows,m,l,u)=>({type:'data',symmetric:false,array:rows.map(r=>r[u]-r[m]),arrayminus:rows.map(r=>r[m]-r[l]),visible:true});
function plot(id,traces,layout){return Plotly.newPlot('plot_'+id,traces,{...base,...layout},config);}
function render(){
 let rows=D['primary_horizon_summary.csv'],tr=[];
 [4,8,16].forEach((k,j)=>[3000,30000].forEach(cap=>{let a=rows.filter(r=>r.k0===k&&r.cap===cap).sort((a,b)=>a.phi-b.phi);tr.push({x:a.map(r=>'φ='+r.phi),y:a.map(r=>r.S_mean),error_y:err(a,'S_mean','S_lo','S_hi'),mode:'lines+markers',name:'k₀='+k+', '+cap,marker:{color:pal[j]},line:{color:pal[j],dash:cap===3000?'dot':'solid'}});}));
 plot('primary',tr,{yaxis:{title:{text:'Largest component fraction S'},range:[0,1.06]},xaxis:{title:{text:'Tested rewiring probability φ'}}});
 function policy(){let cap=Number(document.getElementById('policyCap').value),a=D['application_summary.csv'].filter(r=>r.cap===cap),ts=[];[0,1].forEach((h,j)=>{let s=a.filter(r=>r.h===h);ts.push({x:s.map(r=>r.contacts),y:s.map(r=>r.giant_frac_mean),error_y:err(s,'giant_frac_mean','giant_frac_lo','giant_frac_hi'),mode:'lines+markers',name:h?'Similar contacts':'Random contacts',line:{color:pal[j]},customdata:s.map(r=>[r.cross_frac_mean,r.capped,r.n]),hovertemplate:'Contacts %{x}<br>S %{y:.4f}<br>Cross links %{customdata[0]:.4f}<br>Capped %{customdata[1]}/%{customdata[2]}<extra>%{fullData.name}</extra>'});});plot('policy',ts,{yaxis:{title:{text:'Largest component fraction S'},range:[0,1.06]},xaxis:{title:{text:'Total mutual-contact budget'},tickvals:[600,1200,2400]}});}
 document.getElementById('policyCap').addEventListener('change',policy);document.getElementById('policyCap').value='3000';policy();
 rows=D['primary_analysis/scenario_summary.csv'].filter(r=>r.exp==='A');let ds=[...new Set(rows.map(r=>r.d))].sort((a,b)=>a-b),ps=[...new Set(rows.map(r=>r.phi))].sort((a,b)=>a-b);
 plot('heatmap',[{type:'heatmap',x:ps.map(String),y:ds.map(String),z:ds.map(d=>ps.map(p=>rows.find(r=>r.d===d&&r.phi===p).giant_frac_mean)),colorscale:'Viridis',zmin:0,zmax:1,colorbar:{title:{text:'Mean S'}},hovertemplate:'d %{y}<br>φ %{x}<br>Mean S %{z:.4f}<extra></extra>'}],{xaxis:{title:{text:'Rewiring φ'},type:'category'},yaxis:{title:{text:'Tolerance d'},type:'category'}});
 rows=D['kb_summary.csv'].filter(r=>r.family==='kb_d1');tr=[];[0,.1,.5,.9].forEach((w,j)=>{let a=rows.filter(r=>r.w===w).sort((a,b)=>a.d-b.d);tr.push({x:a.map(r=>r.d),y:a.map(r=>r.largest_mean),error_y:err(a,'largest_mean','largest_lo','largest_hi'),mode:'lines+markers',name:'w='+w,line:{color:pal[j]}});});
 plot('kb',tr,{xaxis:{title:{text:'Confidence d'}},yaxis:{title:{text:'Largest path-cluster fraction'},range:[0,1.06]},shapes:[{type:'line',x0:.256,x1:.256,y0:0,y1:1,line:{color:'#777',dash:'dash'}}]});
 rows=D['hk_summary.csv'];plot('hk',[{x:rows.map(r=>r.epsilon),y:rows.map(r=>r.p_consensus),error_y:err(rows,'p_consensus','p_lo','p_hi'),mode:'lines+markers',name:'Consensus probability',line:{color:pal[0]}},{x:rows.map(r=>r.epsilon),y:rows.map(r=>r.mean_clusters),yaxis:'y2',mode:'lines+markers',name:'Mean cluster count',line:{color:pal[1],dash:'dot'}}],{xaxis:{title:{text:'Tolerance ε'}},yaxis:{title:{text:'Consensus probability'},range:[0,1.06]},yaxis2:{title:{text:'Mean opinion clusters'},overlaying:'y',side:'right'},margin:{...base.margin,r:85}});
 rows=D['binary_summary.csv'];plot('binary',[{x:rows.map(r=>r.p),y:rows.map(r=>r.S_mean),error_y:err(rows,'S_mean','S_lo','S_hi'),mode:'lines+markers',name:'Largest component',line:{color:pal[0]}},{x:rows.map(r=>r.p),y:rows.map(r=>r.second_mean),mode:'lines+markers',name:'Second component',line:{color:pal[1]}}],{xaxis:{title:{text:'Binary-model rewiring probability p'}},yaxis:{title:{text:'Population fraction'},range:[0,1.06]},shapes:[{type:'line',x0:.38,x1:.38,y0:0,y1:1,line:{color:'#777',dash:'dash'}},{type:'line',x0:.2,x1:.6,y0:.5,y1:.5,line:{color:'#aaa',dash:'dot'}}]});
 rows=D['primary_h3_paired.csv'];plot('h3',[{x:rows.map(r=>r.S_h1_minus_h0),y:rows.map(r=>'d='+r.d+', φ='+r.phi),error_x:err(rows,'S_h1_minus_h0','lo','hi'),mode:'markers',marker:{color:pal[0],size:9},name:'Paired difference'}],{xaxis:{title:{text:'S(similar) − S(random)'},zeroline:true,zerolinecolor:'#222',range:[-.13,.15]},yaxis:{automargin:true},showlegend:false,margin:{...base.margin,l:155}});
 rows=D['primary_sensitivity_summary.csv'].filter(r=>((r.gap!==.05)+(r.min_frac!==.05)+(r.S_cutoff!==.9))===1);plot('sensitivity',[{type:'bar',x:rows.map(r=>r.gap!==.05?'Gap '+r.gap:r.min_frac!==.05?'Minimum '+r.min_frac:'S cutoff '+r.S_cutoff),y:rows.map(r=>r.changed),marker:{color:pal[0]},name:'Changed labels'}],{yaxis:{title:{text:'A labels changed, out of1440'}},showlegend:false});
 rows=D['trajectory_demo.csv'].filter(r=>r.phi===.005);plot('trajectory',[{x:rows.map(r=>r.requested_sweep),y:rows.map(r=>r.giant_frac),mode:'lines+markers',name:'Largest component S',line:{color:pal[0]}},{x:rows.map(r=>r.requested_sweep),y:rows.map(r=>r.cross_frac),mode:'lines+markers',name:'Cross-group edge fraction',line:{color:pal[1]}},{x:rows.map(r=>r.requested_sweep),y:rows.map(r=>r.opinion_var),yaxis:'y2',mode:'lines+markers',name:'Opinion variance',line:{color:pal[2],dash:'dot'}}],{xaxis:{title:{text:'Requested sweep (0 shown at first category)'},type:'category'},yaxis:{title:{text:'Network fraction'},range:[0,1.06]},yaxis2:{title:{text:'Opinion variance'},overlaying:'y',side:'right',range:[0,.09]},margin:{...base.margin,r:90}});
 document.getElementById('loadStatus').textContent='Interactive figures loaded. Use the camera button to export PNGs; source tables remain below each chart.';
}
if(typeof Plotly==='undefined'){document.getElementById('loadStatus').textContent='Plotly could not load. Connect to the internet and reload for interactive charts, or expand the numerical tables below.';}else{render();}
'''.replace('__DATA__',json.dumps(data,separators=(',',':')))
    nav=''.join(f'<a href="#{pid}">{html.escape(title.split(":")[0])}</a>' for pid,title,*_ in panels)
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IE305 — evidence explorer</title><style>
body{margin:0;background:#eef3f6;color:#183044;font:17px/1.6 system-ui,sans-serif}main{max-width:1120px;margin:auto;padding:35px 22px}h1{font-size:2.3em;line-height:1.12;max-width:850px}h2{line-height:1.25;font-size:1.5em}section{background:white;border:1px solid #d4e0e7;border-radius:12px;padding:25px;margin:28px 0;scroll-margin-top:20px}.plot{height:500px}a{color:#125c8a}nav{display:flex;flex-wrap:wrap;gap:8px 22px}nav a{font-size:14px}.table{overflow:auto}table{border-collapse:collapse;font-size:13px;width:100%;font-variant-numeric:tabular-nums}th,td{text-align:left;border-bottom:1px solid #dce5eb;padding:8px;white-space:nowrap}th{background:#f3f7fa}.source{font-size:14px}summary{cursor:pointer}select{font:inherit;padding:4px}#loadStatus{background:#e5edf4;padding:12px;border-radius:8px}.eyebrow{font-size:14px;letter-spacing:.07em;text-transform:uppercase;color:#4f6475}@media print{body{background:white}section{break-inside:avoid}.plot{height:430px}nav{display:none}}
</style><main><p class="eyebrow">IE305 · Mihir Vasave and Vaibhav Mathur · 3 November 2026</p><h1>Local agreement can leave a community disconnected.</h1><p>Synthetic agent-based experiments on opinions, contact choice and observation time. The mechanism is a replication and extension of published work. <strong>AnyLogic execution remains pending.</strong></p><p id="loadStatus">Loading the plotting library…</p><p><a href="PROJECT_REPORT.md">Research report</a> · <a href="VALIDATION_REPORT.md">Validation evidence</a> · <a href="APPLICATION_DESIGN.md">Application and product proposal</a> · <a href="README.md">Start here</a></p><nav>'''+nav+'</nav>'+''.join(sections)+'</main><script src="https://cdn.plot.ly/plotly-4.1.1.min.js"></script><script>'+script+'</script></html>'
    (OUT/'results_explorer.html').write_text(page)
    (ROOT/'figure_script_for_syntax_check.js').write_text(script)
    print('Built',len(panels),'Plotly figures with embedded numerical tables')

if __name__=='__main__':main()
