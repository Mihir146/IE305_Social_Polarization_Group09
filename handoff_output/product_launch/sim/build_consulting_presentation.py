"""Build a plain-language, data-led 20-slide PDF and editable PowerPoint.

Run with requirements_presentation.txt. Numerical content comes from saved CSVs.
PDF text/fonts are embedded; all PowerPoint text/tables/diagrams remain editable.
"""
from pathlib import Path
import csv, json, textwrap, hashlib, shutil, re
from html import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

ROOT=Path(__file__).resolve().parent.parent
AN=ROOT/'sim/analysis';FIG=ROOT/'figures/presentation';FIG.mkdir(exist_ok=True)
W,H=960,540
INK='20252A';BLUE='245C89';GREY='646C73';LIGHT='F1F3F5';GREEN='278653';ORANGE='DC8B20'
FONT='/usr/share/fonts/TTF/Roboto-Regular.ttf';BOLD='/usr/share/fonts/TTF/Roboto-Bold.ttf'
pdfmetrics.registerFont(TTFont('Body',FONT));pdfmetrics.registerFont(TTFont('Bold',BOLD))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'axes.labelcolor':'#'+INK,'text.color':'#'+INK,'axes.edgecolor':'#AAB0B5','xtick.color':'#'+GREY,'ytick.color':'#'+GREY,'savefig.facecolor':'white'})

def read(name):
    rows=list(csv.DictReader((AN/name).open()))
    for r in rows:
        for k,v in r.items():
            try:r[k]=float(v)
            except (ValueError,TypeError):pass
    return rows
def pick(rows,**kw):return next(r for r in rows if all(r[k]==v for k,v in kw.items()))
def money(n):return f'Rs {n:,.0f}'
def readable(text):
    text=str(text).replace('→',' to ')
    text=re.sub(r'(?<=[A-Za-zμ])(?=\d)', ' ', str(text))
    text=re.sub(r'(?<=\d)(?=(?:samples|markets|periods|percent|times|attempts|seconds)\b)', ' ', text)
    text=re.sub(r'(?<=\d):(?=[A-Za-z])', ': ', text)
    return text
def interval(r,prefix='profit'):return f"{money(r[prefix+'_lo'])} to {money(r[prefix+'_hi'])}"
PROVENANCE=[]
def cite(*files):
    for f in files:
        if f not in PROVENANCE:PROVENANCE.append(f)
    return '; '.join(files)
def chart(name,draw):
    fig,ax=plt.subplots(figsize=(7.9,3.7),layout='constrained');draw(fig,ax)
    path=FIG/(name+'.png');fig.savefig(path,dpi=180);fig.savefig(FIG/(name+'.pdf'));plt.close(fig);return path
def err(ax,x,rows,metric,color):
    y=np.array([r[metric+'_mean'] for r in rows]);lo=np.array([r[metric+'_lo'] for r in rows]);hi=np.array([r[metric+'_hi'] for r in rows])
    ax.bar(x,y,color=color,width=.6);ax.errorbar(x,y,yerr=[y-lo,hi-y],fmt='none',ecolor='#20252A',capsize=4,lw=1)

class Deck:
    def __init__(self):
        self.ppt=Presentation();self.ppt.slide_width=Inches(13.333333);self.ppt.slide_height=Inches(7.5)
        self.pdf=canvas.Canvas(str(ROOT/'Campus_Product_Launch.pdf'),pagesize=(W,H));self.pdf.setTitle('A smaller giveaway, a better launch? — IE305 Group 9')
        self.items=[];self.bounds=[]
    def rect(self,x,y,w,h,fill=LIGHT,line=None):
        s=self.slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x/72),Inches(y/72),Inches(w/72),Inches(h/72))
        s.fill.solid();s.fill.fore_color.rgb=RGBColor.from_string(fill)
        if line:s.line.color.rgb=RGBColor.from_string(line)
        else:s.line.fill.background()
        self.pdf.setFillColor(HexColor('#'+fill));self.pdf.setStrokeColor(HexColor('#'+(line or fill)));self.pdf.rect(x,H-y-h,w,h,fill=1,stroke=bool(line))
    def text(self,x,y,w,text,size=16,bold=False,color=INK,h=None):
        text=readable(text)
        style=ParagraphStyle('s',fontName='Bold' if bold else 'Body',fontSize=size,leading=size*1.23,textColor=HexColor('#'+color))
        para=Paragraph(escape(str(text)).replace('\n','<br/>'),style);_,height=para.wrap(w,1000)
        height=max(height,h or 0)
        if y+height>492 and y<495:raise ValueError(('content below footer',self.n,text,y,height))
        para.drawOn(self.pdf,x,H-y-height+(height-para.height))
        shape=self.slide.shapes.add_textbox(Inches(x/72),Inches(y/72),Inches(w/72),Inches((height+5)/72))
        tf=shape.text_frame;tf.word_wrap=True;tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0
        for i,line in enumerate(str(text).split('\n')):
            p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.font.name='Roboto';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color);p.space_before=Pt(0);p.space_after=Pt(0);p.line_spacing=1.18
        self.bounds.append(dict(slide=self.n,x=x,y=y,w=w,h=height,text=str(text)))
        return height
    def image(self,path,x,y,w,h):
        self.pdf.drawImage(str(path),x,H-y-h,width=w,height=h,preserveAspectRatio=True,anchor='c',mask='auto')
        self.slide.shapes.add_picture(str(path),Inches(x/72),Inches(y/72),width=Inches(w/72),height=Inches(h/72))
    def table(self,headers,rows,widths,x=34,y=150,rowh=42,size=14):
        rowh=min(rowh,(435-y)/(len(rows)+1))
        for i,row in enumerate([headers]+rows):
            self.rect(x,y+i*rowh,sum(widths),rowh,BLUE if i==0 else ('F1F3F5' if i%2 else 'FFFFFF'))
            xx=x
            for j,cell in enumerate(row):
                cell=readable(cell);font=size
                while True:
                    style=ParagraphStyle('fit',fontName='Bold' if i==0 else 'Body',fontSize=font,leading=font*1.23)
                    para=Paragraph(escape(str(cell)).replace('\n','<br/>'),style)
                    _,height=para.wrap(widths[j]-18,1000)
                    if height<=rowh-14:break
                    font-=.5
                    if font<11:raise ValueError(('table cell too dense',self.n,cell))
                self.text(xx+9,y+i*rowh+7,widths[j]-18,cell,font,i==0,'FFFFFF' if i==0 else INK);xx+=widths[j]
    def panel(self,x,y,w,title,body,size=17):
        self.rect(x,y,w,250,LIGHT);self.text(x+15,y+15,w-30,title,18,True,BLUE);self.text(x+15,y+55,w-30,body,size)
    def start(self,title,section,seconds,note,source='',backup=False):
        if self.items:self.pdf.showPage()
        self.n=len(self.items)+1;self.slide=self.ppt.slides.add_slide(self.ppt.slide_layouts[6]);self.rect(0,0,W,H,'FFFFFF')
        self.text(34,18,890,section.upper(),10,True,BLUE)
        self.text(34,43,895,title,26,True)
        self.rect(34,116,892,1,'CAD0D5')
        self.text(34,499,890,source,8,color=GREY)
        self.text(34,520,850,'IE305 | Group 9 | Synthetic decision experiment'+(' | Q&A backup' if backup else ''),8,color=GREY)
        self.text(913,519,25,str(self.n),9,color=GREY)
        self.slide.notes_slide.notes_text_frame.text=note
        self.items.append(dict(number=self.n,title=title,section=section,seconds=seconds,note=note,source=source,backup=backup))
    def takeaway(self,text):
        self.rect(34,445,892,43,LIGHT);self.text(46,455,866,text,14,True,BLUE)
    def finish(self):
        from fontTools.ttLib import TTFont as InspectFont
        cmap=InspectFont(FONT).getBestCmap()
        assert all(ord(c) in cmap or c.isspace() for r in self.bounds for c in r['text'])
        overlaps=[]
        for i,a in enumerate(self.bounds):
            for b in self.bounds[i+1:]:
                if a['slide']!=b['slide']:continue
                overlap_x=min(a['x']+a['w'],b['x']+b['w'])-max(a['x'],b['x'])
                overlap_y=min(a['y']+a['h'],b['y']+b['h'])-max(a['y'],b['y'])
                if overlap_x>1 and overlap_y>1:overlaps.append((a['slide'],a['text'],b['text']))
        assert not overlaps,overlaps
        self.pdf.save();self.ppt.save(ROOT/'Campus_Product_Launch.pptx')
        assert len(self.items)==20 and sum(s['seconds'] for s in self.items)<=780
        info=dict(slides=20,main_slides=16,backup_slides=4,planned_main_seconds=sum(s['seconds'] for s in self.items),available_seconds=780,editable_text_tables_diagrams=True,pdf_fonts_embedded=True,text_glyph_coverage_checked=True,text_boxes_do_not_overlap=True,source_data=PROVENANCE,slides_detail=self.items)
        (ROOT/'sim/consulting_deck_checks.json').write_text(json.dumps(info,indent=2)+'\n')
        (ROOT/'sim/analysis/presentation_text_bounds.json').write_text(json.dumps(self.bounds,indent=2)+'\n')
        notes=['# Presentation: simple words and speaking plan','','16 main slides, 4 Q&A backups. '+str(info['planned_main_seconds'])+' seconds including the 90-second live model. Mihir: slides1–8; Vaibhav: slides9–16. The original pitch is saved in sources/. Professor feedback is attributed to the students’ account, not an invented written quotation.','']
        for s in self.items:notes += [f"## {s['number']}. {s['title']} — "+('backup' if s['backup'] else str(s['seconds'])+' seconds'),'',s['note'],'','Evidence: '+s['source'],'']
        notes+=['## Demo fallback','','Open the approved grid model if the simplified network display has a problem. It uses the same rules and default result. Do not debug code on stage. The PDF is the slide fallback. The 100-market scenario analysis is reference implementation output; actual AnyLogic evidence is one matched default market shown in two presentation variants, not a full engine batch.']
        (ROOT/'SPEAKER_NOTES.md').write_text('\n'.join(notes)+'\n')
        print(json.dumps({k:v for k,v in info.items() if k!='slides_detail'},indent=2))

def main():
    policies=read('all_policy_summary.csv');confirm=read('confirmation_summary.csv');cp=read('confirmation_paired.csv');quality=read('quality_diagnostic_summary.csv')
    d=Deck()
    d.start('Can a smaller giveaway make a better launch?','The decision',25,'Our original topic was social polarization. We retained the idea that conversations and contact choices affect opinions, but applied it to a seller launching a reusable bottle. We compare prices and free samples, then check whether the result holds in new simulated markets. Every customer input is synthetic.',cite('MODEL_SPEC.md','confirmation_paired.csv'))
    d.text(34,144,890,'From social polarization to a product-launch decision',21,True)
    d.text(34,188,890,'A hypothetical campus seller reaches 300 customers through word of mouth.\nThe aim: compare paid sales and contribution profit, not just publicity.',19)
    for x,num,label in [(34,'300','individual customers'),(337,'36','tested policy choices'),(640,'100','fresh confirmation markets')]:
        d.rect(x,280,286,108,LIGHT);d.text(x+15,295,255,num,32,True,BLUE);d.text(x+15,346,255,label,16)
    d.text(34,411,890,'Mihir Jagdish Vasave (24B4517)  |  Vaibhav Mathur (24B4534)',16)
    d.takeaway('Key result: fewer samples improved modeled profit; costly targeting was harder to justify.')

    d.start('We kept the mechanism and made the question useful','How the project evolved',35,'The original pitch asked whether a socially mixed population could split as people change contacts. The feedback, as we understood it, was to use a clear application, synthetic data and what-if comparisons. We therefore turned opinion into expected product appeal, added awareness and individual buying decisions, and kept adaptive discussion contacts. This is a change in application, not evidence that product buyers follow real political behavior.',cite('sources/project_pitch_social_polarization.pdf','Student-reported professor feedback','PROJECT_JOURNAL.md'))
    d.panel(34,150,286,'1  INITIAL PITCH','Question: can changing contacts split opinions?\n\nKeep: individual opinions, social contacts and disagreement.',17)
    d.panel(337,150,286,'2  FEEDBACK → DESIGN','Use a concrete application.\nSynthetic inputs are acceptable.\nCompare what-if scenarios.\n\nFeedback summarized from our account.',17)
    d.panel(640,150,286,'3  FINAL QUESTION','For a bottle launch, which price and free-sample plan earns more?\n\nAdd: awareness, budget, perceived value and costs.',17)
    d.takeaway('The application changed; the feedback between conversations and beliefs remained.')

    d.start('The seller chooses the offer; each customer decides to buy','Scope and objectives',35,'We model one product and one campaign. The seller chooses price, number of samples and who gets them. Contact replacement is an environment scenario, not necessarily a lever the seller controls. We exclude stock limits, delivery, competitors, returns and repeat purchases. Profit here means revenue minus the bottle cost of sales and samples.',cite('MODEL_SPEC.md'))
    d.table(['Seller decisions','Customer behavior','Measures'],[['Price: Rs400 / 500 / 600','Hear about launch; discuss appeal','Awareness: how many heard?'],['Free samples: 3 or 12','Buy once if value AND budget allow','Paid sales: samples excluded'],['Recipients: random / many contacts / across groups','Learn from owning the bottle','Profit after sold + free bottle costs']],[285,330,277],y=150,rowh=56,size=15)
    d.text(34,385,890,'Boundary: 300 customers, 3 groups, 1,200 contacts, 60 abstract periods.\nNo stock limits, repeat purchases, competition or fixed overhead.',16)
    d.takeaway('This is a decision experiment under stated assumptions, not a campus sales forecast.')

    d.start('Four simple AnyLogic parts create the agent-based model','Model overview and components',50,'Main is the organizer. It owns a population of 300 Consumer agents, each with its own changing state. A cyclic Event called launchPeriod schedules ten interaction attempts per visual tick. After 300 attempts, one period ends and eligible people buy. Java methods implement the rules and record CSVs. We use ordinary circles, lines, text and a histogram for presentation. We did not build a queueing process or move people through physical space; contacts are social ties.',cite('CampusProductLaunch_LiveNetwork.alp','anylogic/ProductKernel.java'))
    d.table(['Component in AnyLogic','What it does','What we can point to'],[['Main agent','Creates market; schedules and records','Setup, counters, CSV export'],['Consumer population (300)','Stores each person’s budget, belief and ownership','One circle = one person'],['Cyclic Event: launchPeriod','10 attempts/tick; 300 attempts/period','Calls advanceLaunchPeriod()'],['Java rules + basic shapes','Discussion, buying, experience; draw results','Methods, circles, lines, text']],[240,360,292],y=145,rowh=57,size=14)
    d.takeaway('Agent-based: total sales are the sum of individual decisions; no fitted sales-growth curve.')

    stats=read('input_statistics.csv')
    d.start('We generated customer differences instead of collecting surveys','Data and input analysis',45,'Synthetic means generated by explicit distributions, not arbitrary values typed per person. Most initial beliefs sit near the middle on a zero-to-one scale. Budget means ability to pay; the value scale converts belief into perceived rupee value. Experience is drawn before a campaign and revealed on ownership. This table is one saved example market, not a population estimate. Attributes are independent by assumption.',cite('data/customers_rep1000.csv','input_statistics.csv','initial_graph_statistics.csv'))
    rows=[]
    for key,label,rule,fmt in [('initial_belief','Initial appeal','Beta(2,2); range0–1','{:.3f}'),('value_scale','Value scale','Uniform Rs500–1,000','Rs{:.2f}'),('budget','Budget','Uniform Rs400–1,000','Rs{:.2f}'),('experience_signal','Owner experience','Normal(0.8,0.1), clipped0–1','{:.3f}'),('initial_degree','Contacts/person','Generated graph; average8','{:.2f}')]:
        r=pick(stats,input=key);rows.append([label,rule,fmt.format(r['mean']),fmt.format(r['sample_sd'])])
    d.table(['Input','Generation rule','Example mean','Example SD'],rows,[185,365,170,172],y=140,rowh=47,size=14)
    d.text(34,430,890,'Example market: 322 / 1,200 ties cross groups (26.8%). SD = spread across its 300 customers.',14)
    d.takeaway('Inputs are assumptions; repeated synthetic markets provide the output data.')

    d.start('Each behavior parameter answers a simple “how often / how much?”','Parameters we can explain',50,'These values are assumptions, not estimates from people. A one-in-four sharing chance means hearing the news is not automatic. Tolerance 0.2 is a gap on the zero-to-one appeal scale. A 30 percent adjustment uses both old beliefs; 0.4 and 0.5 become 0.43 and 0.47. Replacing a disagreeing contact is rare at five percent. New contacts are either random or close in belief. We examine sensitivity because the particular values matter.',cite('MODEL_SPEC.md','behavior_summary.csv'))
    d.table(['Parameter','Baseline','Meaning / example'],[['Sharing chance s','0.25','One aware person passes news in 1 in 4 eligible meetings'],['Tolerance d','0.20','Only belief gaps below0.20 allow opinion averaging'],['Opinion adjustment μ','0.30','Move30% toward the other’s old belief:0.40 →0.43'],['Replacement chance φ','0.05','A disagreeing meeting has a5% chance to replace its tie'],['New-contact rule h','0 or1','0:random; 1:similar beliefs, random fallback'],['Experience q; unit cost','0.8; Rs250','q is the normal draw’s pre-clipping mean; cost includes samples']],[225,125,542],y=140,rowh=47,size=13.5)
    d.takeaway('A period is 300 interaction attempts—not a day. We do not claim these inputs are calibrated.')

    d.start('One conversation can inform; a purchase still needs two checks','Individual rules: a worked example',55,'First samples become aware and receive experience. A random person meets a random contact; news may pass if only one is aware. If both know the launch, close beliefs move together; otherwise the contact may change. At period end an aware nonowner buys only if both conditions hold. For value scale800 and belief0.6, perceived value is480. At price400 with budget450, the customer buys; at500 they do not. Paid buyers then receive their own experience. All eligible customers buy simultaneously at the boundary.',cite('MODEL_SPEC.md','anylogic/ProductKernel.java'))
    steps=[('SAMPLE','Free recipients start aware and use their own experience.'),('MEET','Select a person and one current contact; news may pass.'),('DISCUSS','Close beliefs move together; disagreement may replace the tie.'),('BUY / LEARN','At period end, eligible nonowners buy once and learn from use.')]
    for i,(head,body) in enumerate(steps):
        y=144+i*56;d.text(34,y,170,head,16,True,BLUE);d.text(205,y,720,body,16)
    d.rect(34,380,892,53,LIGHT);d.text(46,391,866,'Example: Rs800 × belief0.60 = Rs480 perceived value; budgetRs450.\nPriceRs400 → buy.  PriceRs500 → do not buy.',15,True)
    d.takeaway('Buy only if aware, not already an owner, budget ≥ price AND perceived value ≥ price.')

    d.start('We compare like with like, then check fresh markets','Experiment design and confidence',45,'We first compared 18 policies with twelve samples. We later added three-sample alternatives on the same one hundred main markets, making36 choices and3,600 runs. These are not3,600 independent populations. We keep each market paired across policies: same customers and aligned random input draws. Then we fixed four policies and evaluated100 fresh markets. Intervals are based on10,000 resamples of whole markets. They describe run-to-run variability under our assumptions, not uncertainty about the real world.',cite('sim/results/*manifest.json','confirmation_paired.csv'))
    d.table(['Stage','Markets × choices','Purpose'],[['Pilot','30 separate markets ×18','Check setup and choose a provisional policy'],['Main + follow-up','100 markets ×36 =3,600 runs','Prices3 × recipients3 × contacts2 × samples2'],['Fresh confirmation','100 new markets ×4 =400 runs','Check fixed choices without searching again']],[210,300,382],y=150,rowh=53,size=15)
    d.text(34,372,892,'Fair comparison: the same generated market is reused across policy alternatives.\n95% interval: resample whole markets10,000 times; never treat customers as replications.',17)
    d.takeaway('The three-sample idea was exploratory. The separate fresh-market check strengthens its evidence.')

    d.start('Live demo: follow news, one meeting and one purchase','Animation — 90 seconds',90,'Open the simplified network model before this slide. Grey is unaware; blue is aware but not an owner; orange is free sample; green is a paid buyer. Point at the black meeting line and the before/after beliefs. Solid grey ties connect close beliefs; dotted ties connect more different ones. A blue highlight is a new contact. Positions are only social-group layout, not physical movement. Watch awareness rise before paid sales. Then accelerate to period60: the default policy6/rep1000 should show148 paid buyers andRs19,200 profit. This is one illustrative run, not the recommended three-sample policy or an average. If display fails, use the approved grid model.',cite('CampusProductLaunch_LiveNetwork.alp','anylogic/evidence/','LIVE_NETWORK.md'))
    d.image(ROOT/'anylogic/evidence/simplified_network_completed_user.png',34,136,485,303.3)
    d.text(550,143,370,'Actual completed default run',19,True,BLUE)
    d.text(550,181,370,'Grey: unaware\nBlue: aware, not owner\nOrange: free sample\nGreen: paid buyer',16)
    d.text(550,274,370,'Show one meeting and its belief change.\nThen watch awareness and paid sales.',16)
    d.text(550,346,370,'Policy6 / rep1000; price Rs400\n300 aware | 148 paid | 12 samples\nProfit Rs19,200\nOne run, not a policy average.',16,True)
    d.takeaway('Solid / dotted ties explain agreement; node color explains customer state. These are different facts.')

    price=sorted([r for r in policies if r['n_samples']==12 and r['strategy']=='degree' and r['h']==0],key=lambda r:r['price'])
    def price_draw(fig,ax):
        err(ax,range(3),price,'profit','#'+BLUE);ax.set_xticks(range(3),[money(r['price']) for r in price]);ax.set_ylabel('Mean profit (Rs)');ax.set_xlabel('Selling price');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    p=chart('price_profit',price_draw)
    d.start('A higher price lost buyers faster than it gained margin','Price comparison',40,'Hold twelve samples, well-connected recipients and random replacement fixed. At price400, mean paid buyers are147.33; at500,84.85; at600,32.21. Profit is highest at400 among these choices. Almost everyone hears in all cases, so awareness alone would miss the difference. The bars are main-market averages and error bars are95 percent intervals for mean profit, not the range of individual runs.',cite('all_policy_summary.csv'))
    d.image(p,320,145,605,283);d.table(['Price','Paid buyers','Mean profit'],[[money(r['price']),f"{r['paid_buyers_mean']:.2f}",money(r['profit_mean'])] for r in price],[89,94,103],x=34,y=160,rowh=52,size=13)
    d.takeaway('Near-total awareness is not launch success. Track paid sales and profit separately.')

    baseline=pick(policies,n_samples=12,strategy='degree',price=400,h=0);small=pick(policies,n_samples=3,strategy='degree',price=400,h=0)
    d.start('Nine fewer free bottles raised profit by about Rs2,846','Sample quantity: explain the money',40,'This is the main paired comparison at400 with the same targeting and contact rule. Reducing12 samples to3 saves9 times250, or2250. Paid sales also rise by3.97 on average, contributing595.50 at150 margin. Together the improvement is2845.50. Total ownership falls even though paid sales rise. We cannot say each removed sample turned into a sale: changing samples changes the whole diffusion path.',cite('budget_paired.csv','all_policy_summary.csv'))
    d.table(['Outcome: 100 main markets','12 samples','3 samples'],[['Paid buyers',f"{baseline['paid_buyers_mean']:.2f}",f"{small['paid_buyers_mean']:.2f}"],['Free bottles','12','3'],['Total owners (paid + free)',f"{baseline['paid_buyers_mean']+12:.2f}",f"{small['paid_buyers_mean']+3:.2f}"],['Mean profit',money(baseline['profit_mean']),money(small['profit_mean'])]],[440,226,226],y=145,rowh=43,size=15)
    d.text(34,370,890,'Profit gain = Rs2,250 saved on samples + Rs595.50 from extra paid margin.\nPaired95% interval: Rs2,673 to Rs3,013.50.',18,True)
    d.takeaway('More owners and more profit are different objectives. Free bottles cost money.')

    comparisons=[pick(cp,provisional_minus='quantity_control',metric='profit'),pick(cp,provisional_minus='targeting_control',metric='profit')]
    def confirm_draw(fig,ax):
        ys=[1,0]
        for y,r in zip(ys,comparisons):ax.errorbar(r['difference'],y,xerr=[[r['difference']-r['lo']],[r['hi']-r['difference']]],fmt='o',color='#'+BLUE,capsize=5,markersize=7)
        ax.axvline(0,color='#999999',lw=1);ax.set_yticks(ys,['3 vs12 samples','Many contacts vs random']);ax.set_xlabel('Paired mean profit gain (Rs); 95% interval');ax.set_ylim(-.6,1.6);ax.grid(axis='x',alpha=.15)
    p=chart('fresh_confirmation',confirm_draw)
    d.start('Fresh markets support fewer samples—not expensive targeting','Confirmation on 100 new markets',40,'We checked fixed choices on fresh markets. The provisional policy earns21711 mean profit. Three versus twelve samples gains2854.50, with an interval entirely above zero. Many-contact versus random recipients gains only31.50, with an interval from minus112.50 to177. That is uncertain; it does not prove exact equality. We therefore have a stronger case for fewer samples than for paying to identify popular people.',cite('confirmation_summary.csv','confirmation_paired.csv'))
    d.image(p,34,145,575,270)
    d.text(642,155,280,'Rs21,711',31,True,BLUE);d.text(642,202,280,'Mean profit: Rs400, 3 samples, many-contact recipients',17)
    d.text(642,286,280,'+Rs2,854.50\nFewer samples: clear gain\n\n+Rs31.50\nTargeting: uncertain gain',17)
    d.takeaway('Do not pay a substantial targeting fee on the basis of this small, uncertain advantage.')

    costs=read('all_cost_revaluation.csv');best=[max([r for r in costs if r['unit_cost']==c],key=lambda r:r['profit_mean']) for c in [150,250,350,450]]
    d.start('What-if analysis changes the price and the timing advice','Advanced output analysis',45,'If cost changes while buying rules stay fixed, we can recalculate profit on the same sales rather than rerun consumers. Across tested alternatives, the best observed price rises from400 to500 and600 as cost increases. This is finite-grid comparison, not continuous optimization. In a more separated graph, spreading samples across groups adds393 early profit versus targeting only the most connected, but its late difference includes zero. The best action depends on the goal and horizon.',cite('all_cost_revaluation.csv','stress_paired.csv','final_paired_contrasts.csv'))
    d.table(['Unit cost','Best tested price','Mean profit'],[[money(r['unit_cost']),money(r['price']),money(r['profit_mean'])] for r in best],[135,160,160],x=34,y=150,rowh=47,size=14)
    d.text(525,151,395,'When groups are more separated',18,True,BLUE)
    d.text(525,195,395,'Across-group vs many-contact seeding:\nPeriod7: +Rs393 [Rs203, Rs585]\nPeriod60: −Rs53 [−Rs155, Rs50]',17)
    d.text(525,303,395,'Similar-contact replacement atRs400, 3 samples: −Rs96 [−Rs179, −Rs15]. A small, exploratory effect; not a universal rule.',16)
    d.takeaway('Reprice when costs change. Use broad group coverage when early reach is the objective.')

    qrows=[[pick(quality,quality=q,d=t,phi=0) for q in [.6,.8,.95]] for t in [.2,1]]
    def quality_draw(fig,ax):
        for rows,label,color,mark in zip(qrows,['Narrow tolerance d=0.2','All beliefs compatible d=1.0'],['#'+BLUE,'#'+GREEN],['o','s']):
            x=np.arange(3);y=np.array([r['paid_buyers_mean'] for r in rows]);lo=np.array([r['paid_buyers_lo'] for r in rows]);hi=np.array([r['paid_buyers_hi'] for r in rows]);ax.errorbar(x,y,yerr=[y-lo,hi-y],label=label,color=color,marker=mark,capsize=3)
        ax.set_xticks(range(3),['0.60','0.80','0.95']);ax.set_xlabel('Experience parameter q (before clipping)');ax.set_ylabel('Mean paid buyers');ax.legend(frameon=False,fontsize=9);ax.grid(axis='y',alpha=.15)
    p=chart('quality_diagnostic',quality_draw)
    d.start('An awkward result exposed a weakness in our assumption','What we learned from a failed expectation',40,'We expected better owner experiences to help sales. Under narrow tolerance the opposite happened: on a fixed graph, increasing q from0.6 to0.95 reduced paid buyers from168.74 to130.58. With tolerance1, sales rose from174.76 to280.96. A moderate belief0.5 accepts0.6 but rejects0.95 at tolerance0.2. This points to the hard confidence gate, not a reason to sell worse bottles. We kept the result and ran a diagnostic instead of hiding it.',cite('quality_diagnostic_summary.csv','quality_paired.csv'))
    d.image(p,34,143,590,281);d.text(653,150,270,'Why can this happen?',18,True,BLUE)
    d.text(653,195,270,'Belief0.50 listens to0.60.\nIt ignores0.95 if d=0.20.\n\nVery positive owners can become too far from moderate nonowners to influence them.',17)
    d.takeaway('This is a model warning. Validate or soften the attention rule before real business use.')

    d.start('We improved the project by testing things that could go wrong','Issues, fixes and learning',35,'The initial novelty claim was too broad; the literature already contains adaptive opinion models and promotional seeding. We changed the claim to a transparent application and experiment. We also found that free ownership is not paid demand, short time snapshots can mislead, and a prettier network does not verify the code. The default actual AnyLogic run matches Java, but the full scenario analysis is reference output. AI assisted the research, code and drafting; we must explain and defend the rules ourselves.',cite('PROJECT_JOURNAL.md','VALIDATION_REPORT.md','../VALIDATION_REPORT.md'))
    d.table(['Issue','What we did','What we learned'],[['Existing mechanisms looked “novel”','Read primary literature; credit prior models','Contribution is application + comparison'],['Free owners confused with sales','Separate free / paid flags and costs','Reach, ownership and profit differ'],['Unexpected quality reversal','1,200 diagnostic runs; tolerance / rewiring checks','Test assumptions; keep awkward results'],['Animation and run evidence differ','Preserve tested fallback; compare actual CSVs','A display/API check is not engine validation']],[275,335,282],y=145,rowh=65,size=14)
    d.takeaway('Checks:16 product checks;1,080 standalone Java runs; actual matched default AnyLogic export.')

    d.start('Start small; buy network information only if it pays','Recommendation and limits',30,'Within our synthetic choices, start at400 with3 samples. Choose random recipients unless identifying well-connected people is cheap: its extra benefit is uncertain. Change the price advice if unit cost changes, and consider group coverage for early reach. This is conditional, not a global optimum or a forecast. Only two sample quantities and three prices were tried. We exclude operations and have no empirical calibration. Our strongest lesson is to separate hearing, buying and profit and to test whether assumptions drive the answer.',cite('confirmation_paired.csv','all_cost_revaluation.csv','OPEN_ISSUES.md'))
    d.panel(34,150,438,'ACTION UNDER OUR ASSUMPTIONS','1  Test priceRs400 and3 free samples.\n\n2  Use simple recipients unless contact information is cheap.\n\n3  Revisit price when unit cost changes.',19)
    d.panel(490,150,436,'BEFORE APPLYING IT OUTSIDE CLASS','Validate budgets, sharing and buying rules.\n\nTest the hard opinion cutoff.\n\nAdd targeting, inventory and operating costs.\n\nNo claim of real-campus demand.',18)
    d.takeaway('Better decisions came from clear metrics, fair comparisons and honest limits—not a complex animation.')

    d.start('Backup: exact parameters and policy codes','Q&A — model details',0,'Use this if asked how to reproduce the demo or change policy. policyIndex encodes recipient rule, price, contact rule and sample quantity. rep selects the synthetic market seed, not the number of runs. d,mu,phi and sharing are in ProductKernel.Config, not separate drag-and-drop blocks.',cite('MODEL_SPEC.md','anylogic/ProductKernel.java','CampusProductLaunch_LiveNetwork.alp'),True)
    d.table(['Setting','Definition / location'],[['policyIndex =6','Rs400;12 samples; many-contact recipients; random new contacts'],['policyIndex =24','Same as6, but3 samples; recommended-policy illustration'],['rep =1000','One reproducible Java market; not an average'],['Event recurrence =0.05','Animation scheduling time; not a market period/day'],['Model clock','10 attempts/visual tick;300 attempts/period;60 periods'],['Other defaults','N300; edges1200; d0.2; μ0.3; φ0.05; s0.25; q0.8']],[245,647],y=140,rowh=47,size=14)
    d.takeaway('The simulation is a central event scheduler acting on individual agents; no physical movement model.')

    d.start('Backup: statistical evidence and exact fresh-market comparisons','Q&A — uncertainty',0,'A replication is an independently generated market. The same market is paired across policies. We resample entire markets with replacement10,000 times. A95 percent interval does not include model-realism uncertainty; these are pointwise intervals. We did not establish equality when a targeting interval includes zero. Full scenario grids run in the reference implementation; actual AnyLogic execution evidence is narrower.',cite('confirmation_summary.csv','confirmation_paired.csv','sim/final_audit.json'),True)
    rows=[]
    for name,label in [('quantity_control','3 vs12 samples'),('targeting_control','Many contacts vs random'),('original_comparison','vs Rs500/12/random')]:
        r=pick(cp,provisional_minus=name,metric='profit');rows.append([label,f"{r['difference']:,.2f}",f"{r['lo']:,.2f} to {r['hi']:,.2f}"])
    d.table(['Provisional minus control','GainRs','95% paired intervalRs'],rows,[390,165,337],y=150,rowh=57,size=15)
    d.text(34,395,890,'100 independent fresh markets;4 fixed choices;400 evaluations.\nResampling unit = market. Confidence intervals do not validate real-world assumptions.',17)
    d.takeaway('Observed outcome variation ≠ uncertainty about whether people actually behave this way.')

    d.start('Backup: published mechanisms and our own assumptions','Q&A — literature and novelty',0,'The original pitch listed journal/year leads without precise papers. Those vague leads are not treated as verified citations. The final review uses identified primary sources. Our own exact purchase rule and synthetic rupee distributions are not validated by these authors. The contribution is a carefully documented course experiment and diagnostic, not priority for a new opinion or marketing mechanism.',cite('LITERATURE_NOTES.md','../LITERATURE_NOTES.md','sources/project_pitch_social_polarization.pdf'),True)
    d.table(['Primary source','What it supports','What it does NOT validate'],[['Deffuant et al.2000','Pairwise influence within a tolerance','Our purchase or budget rules'],['Kozma & Barrat2008','Adaptive contacts and opinion clusters','A new discovery of fragmentation'],['Delre et al.2007 /2010','Product diffusion, awareness and seeding','Our exact monetary/customer parameters'],['Kempe et al.2003','Influence maximization; compare heuristics','An optimality guarantee for our profit rule']],[245,335,312],y=150,rowh=64,size=14)
    d.takeaway('Read-status limits and claim corrections are explicit. Research, implementation and drafting were AI-assisted.')

    d.start('Backup: where every evaluation criterion is covered','Q&A — rubric and submission',0,'The required deliverables are the actual AnyLogic model, input/analysis support and slides. This map shows where the presentation addresses each criterion. Keep both models and the PDF offline; the approved grid is the fallback. No browser or internet is required for the talk.',cite('SUBMISSION_GUIDE.md','COURSE_REQUIREMENTS.md'),True)
    d.table(['Professor’s criterion','Slides / evidence'],[['Scope and objectives','2–3: application, boundary and decisions'],['Data and input analysis','5–6: distributions, actual generated summaries and parameters'],['Model building','4,6–7: AnyLogic components, scheduling and worked individual rule'],['Basic + advanced output analysis','8,10–14: metrics, intervals, alternatives, cost and mechanism checks'],['Animation','9:90-second live agent-network demonstration'],['Recommendation + communication','15–16: lessons, practical advice and limits; sources in footer']],[340,552],y=140,rowh=47,size=14)
    d.takeaway('Submit: .alp models + data/analysis support + slides. Keep the PDF and approved model as fallbacks.')
    d.finish()

if __name__=='__main__':main()
