"""Build editable PowerPoint with native Office charts and embedded workbooks.

No Office renderer is available here: package/relationship checks are separate
from visual inspection on the presentation computer. Scientific plots use the
PowerPoint chart engine; HTML uses Plotly with embedded data/table fallbacks.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
from zipfile import ZipFile,ZIP_DEFLATED
from io import BytesIO
import csv,json,posixpath
import numpy as np
ROOT=Path(__file__).resolve().parent.parent
AN=ROOT/'sim/analysis'
P='http://schemas.openxmlformats.org/presentationml/2006/main'
A='http://schemas.openxmlformats.org/drawingml/2006/main'
R='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
C='http://schemas.openxmlformats.org/drawingml/2006/chart'
REL='http://schemas.openxmlformats.org/package/2006/relationships'
CT='http://schemas.openxmlformats.org/package/2006/content-types'
EMU=914400
COLORS=['187D8D','E9A23B','586CA7','A85878']
BG='F5F7F8';INK='142E3D';MUTED='536C79';WHITE='FFFFFF'

def x(s):return escape(str(s))
def read(name):
    with (AN/name).open() as f:rows=list(csv.DictReader(f))
    for r in rows:
        for k,v in r.items():
            try:r[k]=float(v)
            except (ValueError,TypeError):pass
    return rows

def rels(items):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="'+REL+'">'+''.join(f'<Relationship Id="{id}" Type="{typ}" Target="{x(target)}"/>' for id,typ,target in items)+'</Relationships>'
def xml(s):return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'+s

def workbook(categories,series):
    ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main';rows=[['Category']+[s['name'] for s in series]]
    rows += [[cat]+[s['values'][i] for s in series] for i,cat in enumerate(categories)]
    cells=[]
    for ri,row in enumerate(rows,1):
        cc=[]
        for ci,value in enumerate(row):
            addr=chr(65+ci)+str(ri)
            cc.append(f'<c r="{addr}"><v>{value}</v></c>' if isinstance(value,(float,int)) else f'<c r="{addr}" t="inlineStr"><is><t>{x(value)}</t></is></c>')
        cells.append(f'<row r="{ri}">'+''.join(cc)+'</row>')
    buf=BytesIO()
    with ZipFile(buf,'w',ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',xml(f'<Types xmlns="{CT}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>'))
        z.writestr('_rels/.rels',rels([('rId1',R+'/officeDocument','xl/workbook.xml')]))
        z.writestr('xl/workbook.xml',xml(f'<workbook xmlns="{ns}" xmlns:r="{R}"><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>'))
        z.writestr('xl/_rels/workbook.xml.rels',rels([('rId1',R+'/worksheet','worksheets/sheet1.xml')]))
        z.writestr('xl/worksheets/sheet1.xml',xml(f'<worksheet xmlns="{ns}"><sheetData>'+''.join(cells)+'</sheetData></worksheet>'))
    return buf.getvalue()

def cache(vals,strings=False):
    tag='strCache' if strings else 'numCache'
    return f'<c:{tag}>'+('' if strings else '<c:formatCode>General</c:formatCode>')+f'<c:ptCount val="{len(vals)}"/>'+''.join(f'<c:pt idx="{i}"><c:v>{x(v)}</c:v></c:pt>' for i,v in enumerate(vals))+f'</c:{tag}>'
def literal(vals):return '<c:numLit><c:formatCode>General</c:formatCode><c:ptCount val="'+str(len(vals))+'"/>'+''.join(f'<c:pt idx="{i}"><c:v>{float(v)}</c:v></c:pt>' for i,v in enumerate(vals))+'</c:numLit>'
def rich(text,size=1200):return f'<a:bodyPr/><a:lstStyle/><a:p><a:pPr/><a:r><a:rPr lang="en-US" sz="{size}"><a:solidFill><a:srgbClr val="{INK}"/></a:solidFill><a:latin typeface="Aptos"/></a:rPr><a:t>{x(text)}</a:t></a:r><a:endParaRPr lang="en-US"/></a:p>'
def chart_xml(d):
    cats=d['categories'];parts=[]
    for i,s in enumerate(d['series']):
        col=chr(66+i);color=COLORS[i%len(COLORS)]
        q=f'<c:ser><c:idx val="{i}"/><c:order val="{i}"/><c:tx><c:strRef><c:f>Data!${col}$1</c:f>'+cache([s['name']],True)+'</c:strRef></c:tx>'
        q+=f'<c:spPr><a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:ln w="25400"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></c:spPr>'
        if d.get('kind')=='line':q+='<c:marker><c:symbol val="circle"/><c:size val="5"/></c:marker>'
        if 'lo' in s:
            q+='<c:errBars><c:errDir val="y"/><c:errBarType val="both"/><c:errValType val="cust"/><c:noEndCap val="0"/><c:plus>'+literal([hi-v for hi,v in zip(s['hi'],s['values'])])+'</c:plus><c:minus>'+literal([v-lo for lo,v in zip(s['lo'],s['values'])])+'</c:minus><c:spPr><a:ln w="12700"><a:solidFill><a:srgbClr val="354B59"/></a:solidFill></a:ln></c:spPr></c:errBars>'
        q+='<c:cat><c:strRef><c:f>Data!$A$2:$A$'+str(len(cats)+1)+'</c:f>'+cache(cats,True)+'</c:strRef></c:cat>'
        q+=f'<c:val><c:numRef><c:f>Data!${col}$2:${col}${len(cats)+1}</c:f>'+cache(s['values'])+'</c:numRef></c:val></c:ser>'
        parts.append(q)
    if d.get('kind')=='line':kind='<c:lineChart><c:grouping val="standard"/><c:varyColors val="0"/>'+''.join(parts)+'<c:marker val="1"/><c:smooth val="0"/><c:axId val="101"/><c:axId val="102"/></c:lineChart>'
    else:kind='<c:barChart><c:barDir val="col"/><c:grouping val="clustered"/><c:varyColors val="0"/>'+''.join(parts)+'<c:gapWidth val="90"/><c:overlap val="0"/><c:axId val="101"/><c:axId val="102"/></c:barChart>'
    axes='<c:catAx><c:axId val="101"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="b"/><c:majorTickMark val="none"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/><c:crossAx val="102"/><c:crosses val="autoZero"/><c:auto val="1"/><c:lblAlgn val="ctr"/><c:lblOffset val="100"/></c:catAx>'
    axes+='<c:valAx><c:axId val="102"/><c:scaling><c:orientation val="minMax"/></c:scaling><c:delete val="0"/><c:axPos val="l"/><c:majorGridlines><c:spPr><a:ln w="6350"><a:solidFill><a:srgbClr val="DEE6EA"/></a:solidFill></a:ln></c:spPr></c:majorGridlines><c:numFmt formatCode="'+x(d.get('format','#,##0'))+'" sourceLinked="0"/><c:majorTickMark val="none"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/><c:title><c:tx><c:rich>'+rich(d['ylabel'],1050)+'</c:rich></c:tx><c:overlay val="0"/></c:title><c:crossAx val="101"/><c:crosses val="autoZero"/><c:crossBetween val="between"/></c:valAx>'
    return xml(f'<c:chartSpace xmlns:c="{C}" xmlns:a="{A}" xmlns:r="{R}"><c:lang val="en-US"/><c:chart><c:autoTitleDeleted val="1"/><c:plotArea><c:layout/>'+kind+axes+'</c:plotArea><c:legend><c:legendPos val="b"/><c:layout/><c:overlay val="0"/></c:legend><c:plotVisOnly val="1"/><c:dispBlanksAs val="gap"/><c:showDLblsOverMax val="0"/></c:chart><c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln><a:noFill/></a:ln></c:spPr><c:txPr>'+rich('',1100)+'</c:txPr><c:externalData r:id="rId1"><c:autoUpdate val="0"/></c:externalData></c:chartSpace>')

class Slide:
    def __init__(self,title,tag='',note='',seconds=0,speaker='',backup=False):
        self.title=title;self.tag=tag;self.note=note;self.seconds=seconds;self.speaker=speaker;self.backup=backup;self.shapes=[];self.relationships=[];self.texts=[];self.chart_ids=[];self.id=1
        self.rect(0,0,13.333,7.5,BG)
        self.text(.45,.22,12,.25,tag.upper(),11,'187D8D',True)
        self.text(.45,.65,12.25,1.15,title,29 if len(title)>70 else 31,INK,True)
        self.rect(.45,1.80,1,.055,'E9A23B')
    def next(self):self.id+=1;return self.id
    def rect(self,xx,yy,w,h,fill):
        i=self.next();self.shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Panel {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(xx*EMU)}" y="{int(yy*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="{fill}"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr></p:sp>')
    def text(self,xx,yy,w,h,txt,size=21,color=INK,bold=False):
        i=self.next();self.texts.append(txt)
        paras=''.join('<a:p><a:pPr/><a:r><a:rPr lang="en-US" sz="'+str(int(size*100))+'" b="'+('1' if bold else '0')+'"><a:solidFill><a:srgbClr val="'+color+'"/></a:solidFill><a:latin typeface="Aptos"/></a:rPr><a:t>'+x(line)+'</a:t></a:r><a:endParaRPr lang="en-US"/></a:p>' for line in txt.split('\n'))
        self.shapes.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{int(xx*EMU)}" y="{int(yy*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="0" rIns="0" tIns="0" bIns="0" anchor="t"/><a:lstStyle/>'+paras+'</p:txBody></p:sp>')
    def chart(self,d,xx=5.1,yy=1.95,w=7.7,h=4.65):
        charts.append(d);cid=len(charts);rid='rId'+str(len(self.relationships)+2);self.relationships.append((rid,R+'/chart',f'../charts/chart{cid}.xml'));self.chart_ids.append(cid)
        i=self.next();self.shapes.append(f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{i}" name="{x(d["name"])}"/><p:cNvGraphicFramePr/><p:nvPr/></p:nvGraphicFramePr><p:xfrm><a:off x="{int(xx*EMU)}" y="{int(yy*EMU)}"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></p:xfrm><a:graphic><a:graphicData uri="{C}"><c:chart xmlns:c="{C}" xmlns:r="{R}" r:id="{rid}"/></a:graphicData></a:graphic></p:graphicFrame>')
    def body(self,blocks):
        y=1.95
        for heading,detail in blocks:
            self.text(.55,y,4.2,.5,heading,24,INK,True);self.text(.55,y+.57,4.2,1.0,detail,18,MUTED);y+=1.65
    def footer(self,n,source=''):
        self.text(.45,6.98,11.9,.23,source,9,MUTED)
        self.text(.45,7.25,11.7,.2,'IE305 · Group 9 · All customer inputs synthetic · '+('Backup' if self.backup else f'{self.speaker} · {self.seconds}s'),9,MUTED)
        self.text(12.35,7.2,.5,.2,str(n),10,MUTED)
    def xml(self):return xml(f'<p:sld xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'+''.join(self.shapes)+'</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')

charts=[];slides=[]
def slide(*args,**kw):s=Slide(*args,**kw);slides.append(s);return s

def series(rows,metric,name):return dict(name=name,values=[r[metric+'_mean'] for r in rows],lo=[r[metric+'_lo'] for r in rows],hi=[r[metric+'_hi'] for r in rows])
def main():
    policies=read('all_policy_summary.csv');confirm=read('confirmation_summary.csv');cp=read('confirmation_paired.csv');quality=read('quality_diagnostic_summary.csv');price_rows=sorted([r for r in policies if r['n_samples']==12 and r['strategy']=='degree' and r['h']==0],key=lambda r:r['price'])
    s=slide('Can a smaller giveaway\nmake a better product launch?','Price · Samples · Word of mouth',seconds=35,speaker='Mihir',note='We model a seller launching one reusable bottle in a synthetic campus market. The question is not just how many people hear about it: it is which tested price and sample policy earns more contribution profit. We will show the individual-agent mechanism, compare policies with uncertainty, and run the model live. All inputs are generated assumptions.')
    s.text(.55,2.12,11.8,.8,'An agent-based decision experiment\nfor a hypothetical campus bottle seller',26,MUTED)
    for i,(num,label) in enumerate([('300','individual customers'),('60','campaign periods'),('36','tested policy cells')]):
        s.rect(.55+i*4.1,3.8,3.8,1.45,WHITE);s.text(.8+i*4.1,4,3.2,.55,num,33,'187D8D',True);s.text(.8+i*4.1,4.7,3.2,.4,label,18,MUTED)
    s.text(.55,5.8,12,.8,'Mihir Jagdish Vasave · Vaibhav Mathur\nIE305 Simulation Lab · Group 9',20,INK)
    s.footer(1,'Scope: MODEL_SPEC.md; 36 cells include the exploratory three-sample extension.')

    s=slide('The seller chooses the launch. Customers decide to buy.','Scope and objectives',seconds=45,speaker='Mihir',note='Our seller chooses one of three prices and a sample policy. Random recipients, well-connected recipients and recipients distributed across groups are compared. Twelve samples were the initial fixed-spending design; three samples were a later budget-ceiling extension. We track awareness, paid sales and modeled profit separately. Inventory, repeat purchases, competitors and fixed overhead are outside this one-product campaign.')
    for i,(title,body) in enumerate([('CHOOSE','Price: Rs 400 / 500 / 600\nFree bottles: 3 or 12\nWho receives them?'),('SIMULATE','Customers talk to contacts\nOpinions and awareness change\nEligible individuals buy once'),('EVALUATE','Paid buyers, not free owners\nRevenue and all bottle costs\nProfit and uncertainty')]):
        s.rect(.55+4.1*i,2.05,3.8,3.5,WHITE);s.text(.8+4.1*i,2.35,3.3,.5,title,22,'187D8D',True);s.text(.8+4.1*i,3.1,3.3,2,body,21)
    s.text(.6,6.05,12,.6,'Discussion-contact policy is an additional scenario: random or similar-opinion replacements.',18,MUTED);s.footer(2,'Boundary: one product; one purchase/customer; no inventory shortage or fixed overhead. MODEL_SPEC.md')

    customers=list(csv.DictReader((ROOT/'data/customers_rep1000.csv').open()))
    key=next(k for k in customers[0] if 'prior' in k or k=='initial_belief')
    counts,edges=np.histogram([float(r[key]) for r in customers],bins=np.linspace(0,1,11))
    s=slide('Synthetic inputs are specified, not fitted to campus data.','Data and input analysis',seconds=60,speaker='Mihir',note='Each market has 300 generated customers in three groups and 1,200 contacts. Initial appeal follows Beta two two. A value scale between 500 and 1,000 rupees is separate from a budget between 400 and 1,000. Experiences are centered at 0.8 with clipped noise. This histogram is one generated market, not surveyed attitudes. We report actual generated moments and vary important assumptions rather than claiming empirical calibration.')
    s.body([('300 people, 1,200 ties','Three known groups; stronger initial preference for within-group contacts.'),('Different wants and budgets','Belief Beta(2,2)\nValue scale Rs 500–1,000\nAffordability Rs 400–1,000'),('Example market, rep 1000','Belief mean 0.490; SD 0.235.\nBudget mean Rs 710.93.')])
    s.chart(dict(name='Initial belief histogram',categories=[f'{edges[i]:.1f}–{edges[i+1]:.1f}' for i in range(10)],series=[dict(name='Customers',values=[int(v) for v in counts])],ylabel='Customer count'))
    s.footer(3,'data/customers_rep1000.csv; sim/analysis/input_statistics.csv. Histogram is one synthetic market.')

    s=slide('A conversation changes beliefs. A purchase needs value AND budget.','Agent rules',seconds=80,speaker='Mihir',note='A free recipient begins informed and receives an experience signal. An informed customer sometimes passes launch information to a contact. If their opinions differ by less than 0.2, both move 30 percent toward the other old opinion. A bigger disagreement can replace a discussion contact. After 300 attempts, informed nonowners buy if budget and perceived value both exceed price. An 800-rupee value scale times belief 0.6 is 480 rupees, so that person rejects a 500-rupee price. New owners receive their own experience. Samples never count as paid buyers.')
    for y,head,body in [(2,'1  INFORM','An aware contact shares launch news with probability 0.25.'),(3.12,'2  DISCUSS','Close beliefs compromise: 0.40 and 0.50 become 0.43 and 0.47.'),(4.24,'3  BUY ONCE','Aware + can afford + perceived value ≥ price. Purchases at period end.'),(5.36,'4  EXPERIENCE','New owners receive personal feedback. Beliefs and later conversations can change.')]:
        s.text(.6,y,2.5,.45,head,23,'187D8D',True);s.text(3.1,y,9.5,.9,body,23)
    s.footer(4,'Rules: MODEL_SPEC.md. d=0.2; mu=0.3; phi=0.05. Worked opinion example is illustrative.')

    s=slide('Established mechanisms; explicit new assumptions; checked code.','Literature and verification',seconds=60,speaker='Mihir',note='Bounded confidence comes from Deffuant and related work. Kozma and Barrat already study adaptive opinion-network fragmentation. Promotional seeding and awareness/adoption models also predate this project. Our course contribution is the transparent decision comparison and mechanism diagnostic, not inventing those ideas. We checked limiting cases, purchase eligibility and accounting, matched small reference/native cases and used a separate Java implementation. The first actual AnyLogic run matched its Java reference. The revised animation and actual default export have now also been confirmed.')
    for i,(head,body) in enumerate([('LITERATURE','Bounded confidence and adaptive ties\nPromotional seeding and diffusion\nNo claim to invent these mechanisms'),('OUR ASSUMPTIONS','Price/value/budget threshold\nExperience resets and cost accounting\nSynthetic graph and attributes'),('EVIDENCE','16 product checks passed\nFirst AnyLogic default matches Java\nRevised code: actual API compile passes')]):
        s.rect(.55+i*4.1,2,3.8,3.9,WHITE);s.text(.8+i*4.1,2.3,3.3,.5,head,21,'187D8D',True);s.text(.8+i*4.1,3.05,3.3,2.6,body,20)
    s.footer(5,'Deffuant et al. 2000; Kozma & Barrat 2008; Delre et al. 2007/2010; Kempe et al. 2003. See LITERATURE_NOTES.md and VALIDATION_REPORT.md.')

    s=slide('Compare policies on the same market; confirm on fresh markets.','Experimental design',seconds=60,speaker='Mihir',note='The initial design has 18 policies and a separate thirty-market pilot. One hundred main markets evaluate each policy using shared initial data and aligned random draws. The three-sample follow-up reuses those main markets, so it creates more policy evaluations, not more independent populations. We then freeze four comparisons and test 100 fresh markets. Bootstrap intervals resample whole markets. They quantify simulation variability under the model and are pointwise, not a guarantee that every comparison is simultaneously correct.')
    for i,(head,body) in enumerate([('PILOT','30 separate markets\n18 policies\nChoose a provisional policy'),('MAIN + FOLLOW-UP','100 main markets\n18 + 18 policies\n3,600 evaluations, paired'),('CONFIRMATION','100 fresh markets\n4 fixed comparisons\nNo search for a new winner')]):
        s.rect(.55+i*4.1,2,3.8,3.1,WHITE);s.text(.8+i*4.1,2.3,3.3,.65,head,21,'187D8D',True);s.text(.8+i*4.1,3.1,3.3,1.7,body,21)
    s.text(.65,5.65,12,1,'95% intervals: 10,000 bootstrap resamples of markets.\nCustomers, periods and reused policies are not independent replications.',23)
    s.footer(6,'sim/results/*manifest.json; sim/analysis/confirmation_paired.csv. Exploratory follow-up explicitly distinguished from initial design.')

    s=slide('Almost everyone hears. Far fewer buy at the high price.','Result 1 · Price',seconds=55,speaker='Vaibhav',note='Here twelve high-degree recipients and random replacement are held fixed. Mean paid sales drop from about 147 at 400 rupees to 85 at 500 and 32 at 600. Almost everyone still hears about the launch. Profit is highest at 400 within this comparison. That is why we separate awareness from conversion. This is simulated behavior under synthetic thresholds, not an estimated real-world demand curve.')
    s.body([('News is not conversion','At Rs 600, awareness is nearly 300; mean paid buyers are 32.21.'),('Margin alone is not enough','Profit means: Rs 19,100 / 18,213 / 8,274 at the three prices.'),('Hold other choices fixed','12 samples; degree targeting; random contact replacement.')])
    s.chart(dict(name='Awareness and paid sales by price',categories=['Rs 400','Rs 500','Rs 600'],series=[series(price_rows,'aware','Aware'),series(price_rows,'paid_buyers','Paid buyers')],ylabel='Customers'))
    s.footer(7,'sim/analysis/policy_summary.csv; 100 main markets/cell; error bars are pointwise 95% intervals for means.')

    ss=[next(r for r in confirm if r['policy']==k) for k in ('quantity_control','provisional')]
    s=slide('Nine fewer free bottles can increase profit while reducing total owners.','Result 2 · Sample quantity',seconds=65,speaker='Vaibhav',note='The same 400-rupee price and degree targeting are compared on fresh confirmation markets. Three samples earn about 21,711 rupees versus 18,857 for twelve. The paired gain is 2,854.50 rupees, with interval 2,698.50 to 3,006. The seller saves 2,250 rupees on samples and sells about four extra paid units. But total owners fall by about five because nine free owners disappear. We therefore recommend against interpreting more owners as automatically more profit. Only quantities three and twelve were tested.')
    s.body([('+ Rs 2,854.50','Fresh-market paired profit gain\n95% CI: Rs 2,698.50–3,006'),('Why it happens','Rs 2,250 less sample cost,\nplus margin on about 4 extra sales.'),('Different objectives differ','Paid sales rise; total owners fall.\nThree vs twelve is not a global quantity optimum.')])
    s.chart(dict(name='Confirmed sample quantity profit',categories=['12 free bottles','3 free bottles'],series=[series(ss,'profit','Profit')],ylabel='Modeled profit (Rs)'))
    s.footer(8,'sim/analysis/confirmation_summary.csv and confirmation_paired.csv; 100 fresh paired markets; price Rs 400, degree, h=0.')

    vv=[next(r for r in cp if r['provisional_minus']==k and r['metric']=='profit') for k in ('targeting_control','quantity_control')]
    s=slide('The sample saving is clear. The influencer premium is uncertain.','Result 3 · Targeting',seconds=50,speaker='Vaibhav',note='The targeting control holds price and sample quantity fixed. Degree targeting adds only 31.50 rupees over random selection on fresh markets, with an interval from minus 112.50 to plus 177. That is not evidence that the policies are equivalent, but it does not establish a large targeting premium. In strongly separated groups, distributed seeding helps early reach in a stress test, without a clear final-profit gain for the twelve-sample comparison. Contact recommendation effects are small and conditional; we retain their exceptions in the report.')
    s.body([('Degree over random','+ Rs 31.50\n95% CI: −112.50 to +177'),('Avoid expensive targeting','We have not established a large final-profit benefit from degree information.'),('Timing can still matter','Strong-group stress: distributed seeding helps early coverage, not clearly final profit.')])
    s.chart(dict(name='Confirmed profit contrasts',categories=['Degree vs random\n3 samples','3 vs 12 samples\ndegree'],series=[dict(name='Paired profit difference',values=[r['difference'] for r in vv],lo=[r['lo'] for r in vv],hi=[r['hi'] for r in vv])],ylabel='Profit difference (Rs)'))
    s.footer(9,'confirmation_paired.csv; stress_paired.csv. Pointwise intervals; lack of a clear difference is not equivalence.')

    s=slide('A surprise exposes a risky assumption: very positive opinions can be ignored.','Mechanism diagnostic',seconds=65,speaker='Vaibhav',note='When experiences become more positive, our narrow-confidence model can sell fewer bottles. We kept this awkward result. On a fixed graph, raising the experience mean from 0.6 to 0.95 reduces mean paid sales from about 169 to 131 with tolerance 0.2. With all opinions compatible, it raises sales from 175 to 281. A belief of 0.5 accepts 0.6 but ignores 0.95 under the narrow cutoff. This is a model-risk diagnostic, not advice to lower actual product quality. It tells us to validate the attention mechanism before using the model for business.')
    s.body([('At narrow confidence','Higher experience mean can reduce simulated sales.'),('Remove the gate','With all opinions compatible, the quality effect becomes positive.'),('Interpretation','Validate or soften the attention rule. Do not recommend worse products.')])
    qs=[]
    for d,label in ((.2,'Tolerance 0.2'),(1.,'All compatible')):
        sub=sorted([r for r in quality if r['d']==d and r['phi']==0],key=lambda r:r['quality']);qs.append(series(sub,'paid_buyers',label))
    s.chart(dict(name='Confidence quality diagnostic',categories=['0.60','0.80','0.95'],series=qs,ylabel='Paid buyers',kind='line'))
    s.footer(10,'quality_diagnostic_summary.csv; quality_paired.csv. Exploratory 100 paired markets/setting; fixed graph, Rs 400, 12 samples, degree.')

    s=slide('Live: follow one conversation, then check the campaign accounts.','AnyLogic demonstration',seconds=90,speaker='Vaibhav',note='Switch to the saved AnyLogic model. Show the three customer groups and ownership colors, then point to the individual blue opinion bars and the highlighted actual meeting. Explain one before/after opinion change and that purchases occur at the end of a period. Use around two-times speed and let the default finish. Check 300 aware, 148 paid, twelve samples, revenue 59,200, cost 40,000 and profit 19,200. The entire demonstration budget is ninety seconds including switching windows. If execution fails, use the saved real-engine screenshot and explicitly describe the failure.')
    for i,(head,body) in enumerate([('WATCH','Customer colors: awareness/ownership\nBlue mini-bars: current opinions\nSelected link: an actual meeting'),('EXPLAIN','Close opinions move together\nDistant opinions may change contacts\nBuying requires budget and value'),('CHECK','Default: 148 paid + 12 free\nRevenue Rs 59,200 − cost Rs 40,000\nProfit Rs 19,200')]):
        s.rect(.55+i*4.1,2,3.8,3.7,WHITE);s.text(.8+i*4.1,2.3,3.3,.5,head,22,'187D8D',True);s.text(.8+i*4.1,3.05,3.3,2.25,body,20)
    s.text(.6,6.1,12,.55,'Model: CampusProductLaunch.alp · default policyIndex=6, rep=1000 · switch back promptly.',19,MUTED);s.footer(11,'First actual engine run documented in anylogic/evidence/. Revised default screenshot and CSVs now confirmed; multi-policy batch remains separate.')

    s=slide('Start small. Revisit price with cost. Validate the behavior before deployment.','Conditional recommendation',seconds=70,speaker='Vaibhav',note='For this synthetic baseline and tested choices, start at 400 rupees with three free bottles. Degree targeting has the largest main mean, but its confirmatory gain over random targeting is uncertain and may not pay for collecting network data. Revisit price when unit cost changes; our cost scenarios shift the best observed price. The model demonstrates a mechanism and a decision process rather than predicting a real market. We would next calibrate sharing, willingness to pay and confidence behavior, and add actual operating and targeting costs. Our source, data, scripts and actual engine evidence are included. Research and implementation were AI-assisted; we are responsible for understanding and presenting the work.')
    for y,num,body in [(2.05,'01','Baseline candidate: Rs 400, three samples. Random targeting remains a practical alternative.'),(3.3,'02','Budget is a ceiling, not a spending target. Cost changes can change the preferred price.'),(4.55,'03','Synthetic assumptions drive outcomes. The quality reversal is a warning to validate behavior.')]:
        s.text(.6,y,.8,.6,num,30,'187D8D',True);s.text(1.6,y,10.9,1.05,body,25)
    s.text(.65,6.12,12,.5,'Best among tested candidates; no claim of a global optimum or actual-campus sales forecast.',19,MUTED);s.footer(12,'confirmation_paired.csv; all_cost_revaluation.csv; PROJECT_REPORT.md. AI-assisted research, code and drafting.')

    s=slide('Profit versus price under the original equal-sample design.','Backup · Full price comparison',backup=True)
    ser=[]
    for strategy in ('random','degree','distributed'):
        sub=sorted([r for r in policies if r['n_samples']==12 and r['strategy']==strategy and r['h']==0],key=lambda r:r['price']);ser.append(series(sub,'profit',strategy.title()))
    s.chart(dict(name='Profit by price and recipient strategy',categories=['Rs 400','Rs 500','Rs 600'],series=ser,ylabel='Profit (Rs)'),.6,1.95,12.2,4.8);s.footer(13,'all_policy_summary.csv. 12 samples, h=0; 100 markets; pointwise mean intervals.')

    s=slide('The preferred price depends on unit cost.','Backup · Cost revaluation',backup=True)
    cr=read('all_cost_revaluation.csv');ser=[]
    for price in (400.,500.,600.):
        sub=sorted([r for r in cr if r['n_samples']==3 and r['strategy']=='degree' and r['h']==0 and r['price']==price],key=lambda r:r['unit_cost']);ser.append(dict(name=f'Price Rs {price:.0f}',values=[r['profit_mean'] for r in sub]))
    s.chart(dict(name='Price and unit cost',categories=['Cost 150','Cost 250','Cost 350','Cost 450'],series=ser,ylabel='Profit (Rs)',kind='line'),.6,1.95,12.2,4.8);s.footer(14,'all_cost_revaluation.csv. 3 samples, degree, h=0; cost-only re-accounting holds customer behavior fixed.')

    s=slide('What we did not establish.','Backup · Limitations',backup=True)
    s.text(.65,2,12,4.9,'• No real demand calibration or empirical sales validation.\n• No global optimum: only three prices and two sample quantities.\n• No costly network-data collection, competition, inventory or fixed overhead.\n• Hard confidence, independent attributes and informed-nonbuyer sharing are assumptions.\n• Finite campaign outcomes are not equilibrium claims.\n• Pointwise intervals do not protect every comparison simultaneously.\n• Actual engine evidence must be kept separate from reference and Java runs.',23)
    s.footer(15,'OPEN_ISSUES.md; VALIDATION_REPORT.md; MODEL_SPEC.md.')

    s=slide('Sources and the boundary of our contribution.','Backup · Literature',backup=True)
    s.text(.65,1.95,12,4.95,'Deffuant et al. (2000), Mixing beliefs among interacting agents.\nKozma & Barrat (2008), PRE 77, 016102. doi:10.1103/PhysRevE.77.016102\nDelre et al. (2007), JBR 60, 826–835. doi:10.1016/j.jbusres.2007.02.002\nDelre et al. (2010), JPIM 27, 267–282. doi:10.1111/j.1540-5885.2010.00714.x\nKempe, Kleinberg & Tardos (2003), Maximizing the Spread of Influence.\n\nReplication-informed extension; seeding and homophilic rewiring are established.\nFull reading limits and claim checks are preserved in LITERATURE_NOTES.md.',20)
    s.footer(16,'Direct source links and remaining extraction limits are in the literature notes; no research-priority claim.')

    write_package();write_support()


def write_package():
    out=ROOT/'Campus_Product_Launch.pptx';entries={}
    entries['_rels/.rels']=rels([('rId1',R+'/officeDocument','ppt/presentation.xml'),('rId2','http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties','docProps/core.xml')])
    entries['docProps/core.xml']=xml('<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>Campus Product Launch</dc:title><dc:creator>Mihir Vasave; Vaibhav Mathur</dc:creator><dc:description>Synthetic IE305 decision study; AI-assisted research, implementation and drafting.</dc:description></cp:coreProperties>')
    entries['ppt/presentation.xml']=xml(f'<p:presentation xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>'+''.join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(len(slides)))+'</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
    entries['ppt/_rels/presentation.xml.rels']=rels([('rId1',R+'/slideMaster','slideMasters/slideMaster1.xml')]+[(f'rId{i+2}',R+'/slide',f'slides/slide{i+1}.xml') for i in range(len(slides))])
    emptytree='<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree>'
    entries['ppt/slideMasters/slideMaster1.xml']=xml(f'<p:sldMaster xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}"><p:cSld>'+emptytree+'</p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
    entries['ppt/slideMasters/_rels/slideMaster1.xml.rels']=rels([('rId1',R+'/slideLayout','../slideLayouts/slideLayout1.xml'),('rId2',R+'/theme','../theme/theme1.xml')])
    entries['ppt/slideLayouts/slideLayout1.xml']=xml(f'<p:sldLayout xmlns:p="{P}" xmlns:a="{A}" xmlns:r="{R}" type="blank" preserve="1"><p:cSld name="Blank">'+emptytree+'</p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
    entries['ppt/slideLayouts/_rels/slideLayout1.xml.rels']=rels([('rId1',R+'/slideMaster','../slideMasters/slideMaster1.xml')])
    theme_colors=''.join(f'<a:{name}><a:srgbClr val="{col}"/></a:{name}>' for name,col in [('dk1',INK),('lt1',WHITE),('dk2',MUTED),('lt2',BG),*[(f'accent{i+1}',v) for i,v in enumerate(COLORS+['A5B89B','8A9CAA'])],('hlink','187D8D'),('folHlink','586CA7')])
    fill='<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'
    entries['ppt/theme/theme1.xml']=xml(f'<a:theme xmlns:a="{A}" name="Campus"><a:themeElements><a:clrScheme name="Campus">'+theme_colors+'</a:clrScheme><a:fontScheme name="Campus"><a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Campus"><a:fillStyleLst>'+fill*3+'</a:fillStyleLst><a:lnStyleLst>'+''.join(f'<a:ln w="{w}">'+fill+'<a:prstDash val="solid"/></a:ln>' for w in (6350,12700,19050))+'</a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst>'+fill*3+'</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>')
    overrides=[('/ppt/presentation.xml','presentation.main'),('/ppt/slideMasters/slideMaster1.xml','slideMaster'),('/ppt/slideLayouts/slideLayout1.xml','slideLayout'),('/ppt/theme/theme1.xml','theme')]
    for i,s in enumerate(slides,1):
        entries[f'ppt/slides/slide{i}.xml']=s.xml();entries[f'ppt/slides/_rels/slide{i}.xml.rels']=rels([('rId1',R+'/slideLayout','../slideLayouts/slideLayout1.xml')]+s.relationships);overrides.append((f'/ppt/slides/slide{i}.xml','slide'))
    for i,d in enumerate(charts,1):
        entries[f'ppt/charts/chart{i}.xml']=chart_xml(d);entries[f'ppt/charts/_rels/chart{i}.xml.rels']=rels([('rId1',R+'/package',f'../embeddings/data{i}.xlsx')]);entries[f'ppt/embeddings/data{i}.xlsx']=workbook(d['categories'],d['series']);overrides.append((f'/ppt/charts/chart{i}.xml','chart'))
    types=[]
    for path,kind in overrides:
        if kind=='theme':ctype='application/vnd.openxmlformats-officedocument.theme+xml'
        elif kind=='chart':ctype='application/vnd.openxmlformats-officedocument.drawingml.chart+xml'
        else:ctype='application/vnd.openxmlformats-officedocument.presentationml.'+kind+'+xml'
        types.append(f'<Override PartName="{path}" ContentType="{ctype}"/>')
    entries['[Content_Types].xml']=xml(f'<Types xmlns="{CT}"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="xlsx" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'+''.join(types)+'</Types>')
    for name,value in entries.items():
        if name.endswith(('.xml','.rels')):ET.fromstring(value)
    with ZipFile(out,'w',ZIP_DEFLATED) as z:
        for name,value in entries.items():z.writestr(name,value)
    with ZipFile(out) as z:
        names=set(z.namelist())
        for name in names:
            if not name.endswith('.rels'):continue
            base='' if name=='_rels/.rels' else name.rsplit('/_rels/',1)[0]+'/'
            for rel in ET.fromstring(z.read(name)):
                target=posixpath.normpath(base+rel.attrib['Target'])
                assert target in names,(name,target)
        for i in range(1,len(charts)+1):
            with ZipFile(BytesIO(z.read(f'ppt/embeddings/data{i}.xlsx'))) as wb:
                for name in wb.namelist():ET.fromstring(wb.read(name))
    info=dict(slides=len(slides),main_slides=sum(not s.backup for s in slides),backup_slides=sum(s.backup for s in slides),
        native_editable_charts=len(charts),embedded_chart_workbooks=len(charts),planned_main_seconds=sum(s.seconds for s in slides),
        available_seconds=780,xml_and_relationships_checked=True,rendered_in_powerpoint_here=False,
        caution='Check rendering once in Windows PowerPoint; HTML/tables provide a fallback')
    (ROOT/'sim/deck_checks.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))

def write_support():
    notes=['# Presentation speaker notes and timing','', '12 main slides: 12 minutes 15 seconds including a 90-second live demo. Keep 45 seconds as a buffer. Slides 13–16 are Q&A backups. Mihir presents slides 1–6; Vaibhav slides 7–12. Rehearse aloud once.','']
    for i,s in enumerate(slides[:12],1):notes += [f'## {i}. {s.title.replace(chr(10)," ")} — {s.speaker}, {s.seconds} seconds','',s.note,'']
    notes+=['## Before entering the room','','Keep the saved `.alp`, final deck, real engine screenshot and CSVs on the laptop. Open AnyLogic before your turn. Start the live demo with the tested default; do not edit code on stage. If a visual revision remains untested, use the engine-tested version and say exactly what was run. Confirm Moodle upload separately.']
    (ROOT/'SPEAKER_NOTES.md').write_text('\n'.join(notes)+'\n')
    data=json.dumps(charts).replace('</','<\\/')
    tables=[]
    for i,d in enumerate(charts):
        head='<tr><th>Category</th>'+''.join('<th>'+x(s['name'])+'</th>' for s in d['series'])+'</tr>'
        body=''.join('<tr><td>'+x(cat)+'</td>'+''.join('<td>'+f'{s["values"][j]:,.2f}'+'</td>' for s in d['series'])+'</tr>' for j,cat in enumerate(d['categories']))
        tables.append(f'<section><h2>{x(d["name"])}</h2><p>{x(d["ylabel"])}. Error bars, where supplied, are pointwise 95% market intervals.</p><div id="chart{i}" class="plot"></div><details open><summary>Embedded data (available offline)</summary><table>{head}{body}</table></details></section>')
    html='''<!doctype html><html><head><meta charset="utf-8"><title>Campus launch results</title><style>body{font:17px system-ui;max-width:1150px;margin:35px auto;color:#142e3d;background:#f5f7f8}section{background:white;padding:24px;margin:24px 0}table{border-collapse:collapse;width:100%}td,th{text-align:left;border-bottom:1px solid #ddd;padding:7px}.plot{height:440px}summary{cursor:pointer}h1{font-size:38px}p{line-height:1.55}</style><script src="https://cdn.plot.ly/plotly-3.1.1.min.js"></script></head><body><h1>Campus product launch</h1><p>Synthetic customer data. Full analysis and sources: PROJECT_REPORT.md. The charts load Plotly from its CDN; all numerical tables remain available offline. The PowerPoint deck contains native charts and embedded data with no CDN requirement.</p>'''+''.join(tables)+'''<script>const charts='''+data+''';if(window.Plotly)charts.forEach((d,i)=>{const traces=d.series.map(s=>({name:s.name,x:d.categories,y:s.values,type:d.kind==='line'?'scatter':'bar',mode:'lines+markers',error_y:s.lo?{type:'data',symmetric:false,array:s.hi.map((v,j)=>v-s.values[j]),arrayminus:s.lo.map((v,j)=>s.values[j]-v)}:undefined}));Plotly.newPlot('chart'+i,traces,{barmode:'group',yaxis:{title:{text:d.ylabel}},margin:{t:20,b:85},legend:{orientation:'h'}},{responsive:true});});</script></body></html>'''
    (ROOT/'results_explorer.html').write_text(html)
    sections=[]
    for i,s in enumerate(slides,1):
        txt=''.join('<p>'+x(t).replace('\n','<br>')+'</p>' for t in s.texts[2:] if not t.startswith('IE305'))
        sections.append(f'<section><small>{i} / {len(slides)} · {x(s.tag)}</small><h1>{x(s.title).replace(chr(10),"<br>")}</h1>{txt}</section>')
    (ROOT/'presentation.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>Campus launch slides — text fallback</title><style>body{font:24px system-ui;color:#142e3d;background:#f5f7f8;margin:0}section{box-sizing:border-box;min-height:100vh;padding:4vh 6vw;border-bottom:3px solid #e9a23b}h1{font-size:42px;max-width:1100px}p{max-width:1100px;line-height:1.4}small{color:#187d8d}@media print{section{height:100vh;page-break-after:always;font-size:18px}}</style></head><body>'''+''.join(sections)+'''<script>document.addEventListener('keydown',e=>{const s=[...document.querySelectorAll('section')];let i=s.findIndex(x=>x.getBoundingClientRect().bottom>innerHeight/2);if(e.key==='ArrowRight'||e.key==='PageDown')s[Math.min(i+1,s.length-1)].scrollIntoView();if(e.key==='ArrowLeft'||e.key==='PageUp')s[Math.max(i-1,0)].scrollIntoView();});</script></body></html>''')
    (ROOT/'sim/analysis/presentation_chart_data.json').write_text(json.dumps(charts,indent=2)+'\n')

if __name__=='__main__':main()
