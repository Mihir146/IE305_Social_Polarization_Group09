"""Create a compact, offline presentation from verified CSV summaries."""
from pathlib import Path
import csv,html
ROOT=Path(__file__).resolve().parent
OUT=ROOT.parent

def read(name):
    with (ROOT/name).open() as f:return list(csv.DictReader(f))

def table(headers,rows):
    return '<table><thead><tr>'+''.join('<th>'+html.escape(v)+'</th>' for v in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table>'

def main():
    horizon=read('primary_horizon_summary.csv');app=read('application_summary.csv');paired=read('application_paired.csv')
    hs=[]
    for k in (4,8,16):
        a={int(r['cap']):r for r in horizon if int(r['k0'])==k and float(r['phi'])==.005}
        hs.append([str(k),f'{float(a[3000]["S_mean"]):.4f}',f'{float(a[30000]["S_mean"]):.4f}',f'{round(30*float(a[3000]["p_fragmented"]))}/30 → {round(30*float(a[30000]["p_fragmented"]))}/30'])
    aps=[]
    for h in (0,1):
        r=next(r for r in app if int(r['k0'])==8 and float(r['h'])==h and int(r['cap'])==3000)
        aps.append(['Random' if h==0 else 'Similar',f'{100*float(r["giant_frac_mean"]):.2f}%',f'{100*float(r["cross_frac_mean"]):.2f}%'])
    ps=[]
    for r in paired:
        if int(r['cap'])==300000:
            ps.append([r['k0'],f'{float(r["giant_frac_h1_minus_h0"]):+.4f}',f'[{float(r["giant_frac_lo"]):+.4f}, {float(r["giant_frac_hi"]):+.4f}]'])
    graph='''<svg viewBox="0 0 620 270" role="img" aria-label="Two three-person opinion groups joined by a single bridge"><g stroke="#8295a5" stroke-width="4"><path d="M80 75 L190 75 L135 195 Z" fill="none"/><path d="M430 75 L540 75 L485 195 Z" fill="none"/></g><path d="M135 195 L430 75" stroke="#9857a4" stroke-width="5"/><g fill="#125c8a"><circle cx="80" cy="75" r="24"/><circle cx="190" cy="75" r="24"/><circle cx="135" cy="195" r="24"/></g><g fill="#c35b2c"><circle cx="430" cy="75" r="24"/><circle cx="540" cy="75" r="24"/><circle cx="485" cy="195" r="24"/></g><g fill="white" text-anchor="middle" dominant-baseline="middle" font-size="15"><text x="80" y="75">.2</text><text x="190" y="75">.2</text><text x="135" y="195">.2</text><text x="430" y="75">.8</text><text x="540" y="75">.8</text><text x="485" y="195">.8</text></g><text x="245" y="230" fill="#9857a4" font-size="18">One bridge keeps S = 1</text></svg>'''
    slides=[
    ('Can more contacts prevent echo chambers—or only delay them?',
     '<p class="lead">Designing contact recommendations for a synthetic campus discussion platform.</p><p>Mihir Vasave · Vaibhav Mathur<br>IE305 Simulation Lab</p><div class="note">Reference evidence complete. Actual AnyLogic execution remains pending.</div>',
     'Open with the operator’s decision: more conversation capacity, random introductions, or similar-opinion partners. The question is about maintaining communication over a stated duration.', 'PROJECT_REPORT.md'),
    ('A concrete decision, with synthetic input data',
     '<p>300 participants discuss one campus policy. Opinion0 means full opposition;1 means full support.</p><div class="cards"><div><b>Capacity</b><br>600 / 1,200 / 2,400 mutual discussion links</div><div><b>Recommendation</b><br>Random or similar new partners</div><div><b>Behavior</b><br>Compromise when close; possibly replace a contact when far apart</div></div><p class="equation">.20 and .30 → .23 and .27 at μ=.30</p><p>Published mechanism; scenario parameters are assumptions.</p>',
     'Edges are topic-specific discussion connections, not friendships ending over a policy. No survey data or calibrated real-time clock is claimed. Explain one activation before introducing results.', 'APPLICATION_DESIGN.md; data/README.md'),
    ('Opinion groups and graph pieces are different',
     '<div class="two"><div>'+graph+'</div><div><p><b>K = 2:</b> two major opinion groups.</p><p><b>S = 1:</b> everyone belongs to one connected component.</p><p><b>Cross links = 1/7:</b> only one link joins the groups.</p></div></div><p>A large connected component can survive on very few bridges.</p>',
     'This is a hand-calculated six-agent fixture. Removing the bridge gives S=.5 while the opinions stay the same. Q alone does not prove antagonism or misinformation.', 'AnyLogic_port.md §6; sim/verify_native.py'),
    ('Six policies; repeated snapshots of the same paths',
     '<p class="lead">3 contact budgets × 2 recommendation rules × 30 replications.</p><p>Observe at300,1,000,3,000,30,000 and300,000 sweeps.</p><div class="cards"><div><b>180</b><br>stochastic realizations</div><div><b>900</b><br>repeated-measure rows</div><div><b>95% intervals</b><br>seeded bootstrap; Wilson for proportions</div></div><p>Fixed: N=300,d=.2,μ=.3,φ=.005; isolates allowed.</p>',
     'Do not call900 snapshots independent runs. The follow-up is exploratory. Pair h policies within degree. Across degrees, the original initialization convention does not keep every opinion fixed.', 'sim/application_snapshots.csv; sim/run_application.py'),
    ('More contacts looked protective—until we waited',
     table(['Initial degree','Mean S:3,000','Mean S:30,000','Fragmented runs'],hs)+'<p>Here h=1,φ=.005;30 matched runs per row. Fragmentation means S&lt;.9.</p><p class="lead">The apparent positive rewiring threshold was strongly horizon-dependent.</p>',
     'For degree8, none of the30 short snapshots met our fragmentation cutoff;29 did at the longer horizon. This does not prove a universal zero threshold. The full intervals are in the source table.', 'sim/primary_horizon_summary.csv; sim/primary_threshold_brackets.csv'),
    ('Connectivity alone misses the loss of cross-group links',
     table(['Recommendation','Mean S','Mean cross-group link fraction'],aps)+'<p>Degree8,3,000 sweeps;30 runs per policy. Both giant components are almost the entire population.</p><p class="lead">Similar partners remove cross-group links faster in this scenario.</p>',
     'These are modeled edge fractions, not actual exposure frequencies or measured satisfaction. Distinguish graph reachability from how many links bridge different opinions.', 'sim/application_summary.csv'),
    ('Our preferred final-state hypothesis was not supported',
     table(['Initial degree','Final S(similar)−S(random)','Paired95% interval'],ps)+'<p>After the300,000-sweep check, all180 realizations freeze numerically. Every interval above includes zero.</p><p>The original six B-cell comparisons also did not support H3. <b>No clear difference is not proof of equivalence.</b></p>',
     'At degree16,11 random-policy runs were still active at30,000; extending them removed the apparent large final-state advantage. Speed effects are conditional, not universally favorable to similar recommendations.', 'sim/application_paired.csv; sim/primary_h3_paired.csv'),
    ('Verification separates what passed from what remains uncertain',
     table(['Check','Evidence'],[['Reference replay','All2,790 saved legacy rows reproduced'],['Identities / hand fixtures','Edge count, mean, variance and graph metrics checked'],['HK benchmark','Finite-N consensus pattern reproduced'],['KB / binary benchmarks','Broad quantitative agreement; exact critical values only partial'],['AnyLogic','API audit and Java bodies ready; actual compile/run pending']])+'<p>Source gaps, censoring and failed hypotheses remain visible.</p>',
     'Name Kozma–Barrat as the direct baseline. Do not claim a new social mechanism or exact critical-point validation. A stand-in Java syntax check is not an AnyLogic implementation test.', 'VALIDATION_REPORT.md; LITERATURE_NOTES.md'),
    ('A useful design conclusion includes its observation horizon',
     '<p class="lead">More contact capacity can buy time. It does not establish durable integration in these scenarios.</p><p>Assess both the largest component and cross-group links at the consultation horizon.</p><p>Global opinion variance falls under symmetric averaging, even while the graph separates.</p><div class="note">Synthetic mechanism study: no calibrated human parameters, real-time prediction or welfare optimum.</div>',
     'The mechanism and broad temporal distinction are prior work. Our contribution is replication plus controlled output analysis that changes a conclusion. The product-launch alternative needs a separate purchasing model.', 'PROJECT_REPORT.md §§6–8'),
    ('Before presenting: complete the actual AnyLogic evidence',
     '<ol><li>Compile the model and pass pair/triangle/bridge fixtures.</li><li>Export distinct replications under matching rules and horizons.</li><li>Compare distributions, save the .alp and record the version.</li><li>Insert actual screenshots and replace pending status statements.</li></ol><p>Source review, code, experiments and drafting used AI assistance. Both students should understand and verify the presented work.</p><p><a href="AnyLogic_port.md">Build instructions</a> · <a href="VIVA_PREP.md">Viva preparation</a> · <a href="results_explorer.html">Interactive figures</a></p>',
     'This slide records the current handoff. Replace it with actual implementation evidence once completed. Do not state that matching seed labels across Java and NumPy produce identical trajectories.', 'AnyLogic_port.md; OPEN_ISSUES.md')]
    body=[]
    for i,(title,content,notes,source) in enumerate(slides,1):
        body.append(f'<section class="slide" id="s{i}"><div class="eyebrow">IE305 · Contact recommendations · {i}/{len(slides)}</div><h1>{title}</h1>{content}<footer>Evidence: {html.escape(source)}</footer><details><summary>Speaker prompt</summary><p>{notes}</p></details></section>')
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>IE305 — contact design</title><style>
*{box-sizing:border-box}body{margin:0;background:#e8eff4;color:#17364b;font:22px/1.5 system-ui,sans-serif}.slide{display:none;max-width:1200px;min-height:92vh;margin:auto;padding:45px 65px 30px;background:white}.slide.active{display:block}h1{font-size:44px;line-height:1.15;margin:22px 0 30px;max-width:1050px}.eyebrow,footer{font-size:13px;color:#607789}.eyebrow{text-transform:uppercase;letter-spacing:.08em}.lead{font-size:28px;line-height:1.4}.note{background:#e9f1f6;border-left:5px solid #125c8a;padding:18px;margin-top:25px}.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.cards>div{background:#edf3f7;border-radius:8px;padding:20px;font-size:19px}.cards b{font-size:26px}.equation{font-size:34px;color:#125c8a}.two{display:grid;grid-template-columns:1.3fr 1fr;gap:25px;align-items:center}svg{width:100%}table{border-collapse:collapse;width:100%;font-size:21px;font-variant-numeric:tabular-nums}th,td{text-align:left;padding:15px 12px;border-bottom:1px solid #d5e0e8}th{background:#edf3f7}footer{margin-top:28px;overflow-wrap:anywhere}details{font-size:15px;color:#4d6576;margin-top:15px}a{color:#125c8a}nav{position:sticky;bottom:0;padding:8px;text-align:center;background:#17364b;color:white;font-size:14px}button{font:inherit;padding:7px 18px;border:0;border-radius:5px;margin:0 12px;cursor:pointer}li{margin:12px 0}@media(max-width:750px){.slide{padding:25px;font-size:18px}h1{font-size:34px}.cards,.two{grid-template-columns:1fr}table{font-size:16px}}@media print{body{background:white}.slide{display:block;break-after:page;min-height:0;height:95vh;padding:20px 35px;font-size:18px}h1{font-size:34px}nav,details{display:none}table{font-size:18px}}
</style>'''+''.join(body)+'''<nav><button id="prev">← Previous</button><span id="counter"></span><button id="next">Next →</button> Arrow keys navigate · Print saves all slides</nav><script>
const slides=[...document.querySelectorAll('.slide')];let current=0;
function show(i){current=Math.max(0,Math.min(slides.length-1,i));slides.forEach((s,j)=>s.classList.toggle('active',j===current));document.getElementById('counter').textContent=(current+1)+' / '+slides.length;}
document.getElementById('prev').onclick=()=>show(current-1);document.getElementById('next').onclick=()=>show(current+1);
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight'||e.key==='PageDown')show(current+1);if(e.key==='ArrowLeft'||e.key==='PageUp')show(current-1);if(e.key==='Home')show(0);if(e.key==='End')show(slides.length-1);});show(0);
</script></html>'''
    (OUT/'presentation.html').write_text(page)
    print('Built',len(slides),'offline slides from source tables')
if __name__=='__main__':main()
