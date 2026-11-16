"""Functional lab-palette scheduler for the existing individual-customer model.

Uses Source, Delay, SelectOutput, Sink and ordinary Function elements. The
Source produces one scheduler token, not additional customers. Palette routing
executes the actual discussion branches and period-end buying. The old files
are never overwritten. Initialization, diagnostics and CSV support are retained
and explicitly documented as custom code; this is not a no-code model.
"""
from pathlib import Path
import copy,xml.etree.ElementTree as ET,hashlib,json
import build_alp as b

ROOT=Path(__file__).resolve().parent.parent
PKG='campusproductlaunchlab'
LIB='com.anylogic.libraries.processmodeling'
EXAMPLES=Path('/opt/anylogic/plugins/com.anylogic.examples_8.9.10.202609241721')

FUNCTIONS={
'chooseMeeting':r'''
if (launch.activationInPeriod == 0) launch.period++;
for (int k = 0; k < 6; k++) draws[k] = launch.eventRng.nextDouble();
int i = (int)(draws[0] * 300);
launch.lastI = i; launch.lastJ = -1; launch.lastNew = -1;
launch.beforeI = launch.afterI = launch.customers[i].belief;
launch.lastOutcome = "No discussion contact";
if (launch.degree[i] == 0) return;
int rank = (int)(draws[1] * launch.degree[i]);
for (int j = 0; j < 300; j++) {
 if (launch.adj[i][j] && rank-- == 0) {
  launch.lastJ = j;
  launch.beforeJ = launch.afterJ = launch.customers[j].belief;
  break;
 }
}''',
'shareLaunchNews':r'''
canDiscuss = false;
if (launch.lastJ < 0) return;
ProductKernel.Customer a = launch.customers[launch.lastI];
ProductKernel.Customer z = launch.customers[launch.lastJ];
launch.lastOutcome = "Neither customer knows the launch";
if (!a.aware && !z.aware) return;
if (a.aware != z.aware) {
 launch.lastOutcome = "Launch news was not shared in this meeting";
 if (draws[2] >= launch.config.shareProb) return;
 ProductKernel.Customer other = a.aware ? z : a;
 other.aware = true; other.awarePeriod = launch.period;
}
canDiscuss = true;''',
'moveBeliefsCloser':r'''
double x = launch.beforeI, y = launch.beforeJ;
launch.customers[launch.lastI].belief = x + launch.config.mu * (y - x);
launch.customers[launch.lastJ].belief = y + launch.config.mu * (x - y);
launch.lastOutcome = "Opinions moved closer";''',
'replaceContact':r'''
launch.lastOutcome = "Opinions too far apart; contact kept";
if (draws[3] >= launch.config.phi) return;
int i = launch.lastI, j = launch.lastJ;
java.util.ArrayList<Integer> choices = new java.util.ArrayList<>();
for (int k = 0; k < 300; k++) {
 if (k != i && !launch.adj[i][k] && Math.abs(launch.customers[k].belief - launch.beforeI) < launch.config.d)
  choices.add(k);
}
if (draws[4] >= launch.config.h || choices.isEmpty()) {
 choices.clear();
 for (int k = 0; k < 300; k++) if (k != i && !launch.adj[i][k]) choices.add(k);
}
if (choices.isEmpty()) return;
int k = choices.get((int)(draws[5] * choices.size()));
launch.adj[i][j] = launch.adj[j][i] = false;
launch.adj[i][k] = launch.adj[k][i] = true;
launch.degree[j]--; launch.degree[k]++; launch.rewires++;
launch.lastNew = k;
launch.lastOutcome = "Disagreement: discussion contact replaced";''',
'countAttempt':r'''
launch.afterI = launch.customers[launch.lastI].belief;
if (launch.lastJ >= 0) launch.afterJ = launch.customers[launch.lastJ].belief;
launch.activationInPeriod++;
if (launch.lastNew >= 0) {
 rewireI = launch.lastI; rewireK = launch.lastNew; rewireLife = 18;
}''',
'checkPurchases':r'''
java.util.ArrayList<Integer> buyers = new java.util.ArrayList<>();
for (int i = 0; i < 300; i++) {
 ProductKernel.Customer a = launch.customers[i];
 double value = a.valueScale * a.belief;
 if (a.aware && !a.freeSample && a.paidPeriod < 0 && a.budget >= launch.config.price && value >= launch.config.price) {
  a.paidPeriod = launch.period; a.valueAtPurchase = value; buyers.add(i);
 }
}
for (int i : buyers) launch.customers[i].belief = launch.customers[i].experience;
launch.activationInPeriod = 0;
double[] row = launch.snapshot(buyers.size());
launch.history.add(row); launch.check(row);''',
'showProgress':r'''
if (launch.activationInPeriod % 10 != 0) return;
visualFrame++; if (rewireLife > 0) rewireLife--;
if (visualFrame % 4 == 1 || recentI < 0) {
 recentI = launch.lastI; recentJ = launch.lastJ;
 recentBeforeI = launch.beforeI; recentBeforeJ = launch.beforeJ;
 recentAfterI = launch.afterI; recentAfterJ = launch.afterJ;
 recentOutcome = launch.lastOutcome;
}
if (animateNetwork && launch.activationInPeriod == 0) refreshLaunchLinks();
refreshLaunchDisplay();''',
}

BLOCKS=[
('startCampaign','Source',60,1040,{'arrivalType':'self.MANUAL'}),
('nextMeeting','Delay',205,1040,{'delayTime':'0.005','onAtExit':'chooseMeeting(); shareLaunchNews();'}),
('bothAware','SelectOutput',380,1040,{'condition':'canDiscuss'}),
('closeEnough','SelectOutput',555,1040,{'condition':'Math.abs(launch.beforeI - launch.beforeJ) < launch.config.d'}),
('averageBeliefs','Delay',740,1000,{'delayTime':'0','onAtExit':'moveBeliefsCloser();'}),
('changeContact','Delay',740,1120,{'delayTime':'0','onAtExit':'replaceContact();'}),
('finishAttempt','Delay',925,1040,{'delayTime':'0','onAtExit':'countAttempt();'}),
('periodFinished','SelectOutput',1090,1040,{'condition':'launch.activationInPeriod == 300'}),
('buyAndExperience','Delay',1090,1170,{'delayTime':'0','onAtExit':'checkPurchases();'}),
('campaignFinished','SelectOutput',925,1290,{'condition':'launch.period >= 60 && launch.activationInPeriod == 0','onEnter':'showProgress();'}),
('finishCampaign','Sink',1090,1290,{'onEnter':'exportLaunch(); finishSimulation();'}),
]
EDGES=[('startCampaign','out','nextMeeting'),('nextMeeting','out','bothAware'),('bothAware','outT','closeEnough'),('bothAware','outF','finishAttempt'),('closeEnough','outT','averageBeliefs'),('closeEnough','outF','changeContact'),('averageBeliefs','out','finishAttempt'),('changeContact','out','finishAttempt'),('finishAttempt','out','periodFinished'),('periodFinished','outT','buyAndExperience'),('periodFinished','outF','campaignFinished'),('buyAndExperience','out','campaignFinished'),('campaignFinished','outT','finishCampaign'),('campaignFinished','outF','nextMeeting')]

def param(obj,name,value,unit=False):
    ps=obj.find('Parameters');p=next((e for e in ps if e.findtext('Name')==name),None)
    if p is None:p=b.el(ps,'Parameter');b.el(p,'Name',name)
    for e in list(p):
        if e.tag!='Name':p.remove(e)
    v=b.el(p,'Value',Class='CodeUnitValue' if unit else 'CodeValue');b.el(v,'Code',value)
    if unit:b.el(v,'Unit','SECOND',Class='TimeUnits')

def main():
    originals={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in ['CampusProductLaunch.alp','CampusProductLaunch_LiveNetwork.alp']}
    root=ET.parse(ROOT/'CampusProductLaunch_LiveNetwork.alp').getroot();b.counter=max(int(e.text) for e in root.iter('Id'))
    model=root.find('Model');old=model.findtext('JavaPackageName');model.find('Name').text='CampusProductLaunch_LabFlowchart';model.find('JavaPackageName').text=PKG
    for p in root.iter('PackageName'):
        if p.text==old:p.text=PKG
    a=root.find('.//ActiveObjectClass[Name="Main"]')
    # Keep initialization/statistics support, but remove the old behavioral loop:
    # actual branch execution now belongs to connected PML blocks.
    code=a.findtext('AdditionalClassCode');i=code.index('    public void interaction(double[] u)');j=code.index('    public double[] snapshot',i);code=code[:i]+code[j:]
    i=code.index('public void advanceLaunchPeriod()');j=code.index('public void exportLaunch()',i);code=code[:i]+code[j:]
    code+='\npublic double[] draws = new double[6];\npublic boolean canDiscuss = false;\n'
    code=code.replace('if(policyIndex<0||policyIndex>36)','if(policyIndex<0||policyIndex>35)').replace('Choose policyIndex0..35 or36 for batch','Choose one policyIndex0..35; this visual version runs one campaign')
    code=code.replace('launchBatch=policyIndex==36;launchCaseIndex=0;startLaunchCase(launchBatch?0:policyIndex,rep);','launchBatch=false;launchCaseIndex=0;startLaunchCase(policyIndex,rep);')
    a.find('AdditionalClassCode').text=code
    a.find('Events').clear();a.find('StartupCode').text='initializeLaunch();\nstartCampaign.inject(1);'
    a.find('.//Variable[Name="outputDirectory"]/Properties/DefaultValue/Code').text='"product_lab_output"'
    # First editor viewport must contain the actual PML blocks. The network
    # presentation is a translated group below, preserving local UI coordinates.
    shape=a.find('Presentation/Level/Presentation')
    old_shapes=list(shape);shape.clear()
    network=b.el(shape,'Group');b.common(network,'networkPresentation',0,650,shape=True);b.el(network,'Rotation',0)
    network_contents=b.el(network,'Presentation')
    for e in old_shapes:network_contents.append(e)
    functions=b.el(a,'Functions')
    for k,(name,body) in enumerate(FUNCTIONS.items()):
        f=b.el(functions,'Function',AccessType='public',StaticFunction='false');b.el(f,'ReturnModificator','VOID');b.el(f,'ReturnType','double');b.common(f,name,70+220*(k%4),500+65*(k//4),public=True,show=True);b.el(f,'Body',body.strip())
    sample=ET.parse(EXAMPLES/'basicmodels/Bank Office - Phase 3/Bank Office - Phase 3.alp').getroot().find('.//ActiveObjectClass[Name="Main"]')
    if model.find('RequiredLibraryReference[LibraryName="com.anylogic.libraries.processmodeling"]') is None:
        ref=b.el(model,'RequiredLibraryReference');b.el(ref,'LibraryName',LIB);b.el(ref,'VersionMajor',8);b.el(ref,'VersionMinor',0);b.el(ref,'VersionBuild',5)
    templates={o.findtext('ActiveObjectClass/ClassName'):o for o in sample.findall('EmbeddedObjects/EmbeddedObject') if o.findtext('ActiveObjectClass/ClassName') in ['Source','Delay','SelectOutput','Sink']}
    objects=a.find('EmbeddedObjects');names={}
    for name,kind,x,y,params in BLOCKS:
        y-=900
        o=copy.deepcopy(templates[kind]);o.find('Name').text=name;o.find('X').text=str(x);o.find('Y').text=str(y);o.find('ShowLabel').text='true';o.find('PresentationFlag').text='true';o.find('Label/X').text='-25';o.find('Label/Y').text='-25'
        for e in o.iter('Id'):e.text=b.ident()
        gs=o.find('GenericParameterSubstitute');v=gs.find('GenericParameterSubstituteValue')
        if v is not None:gs.remove(v)
        for p in o.find('Parameters'):
            for e in list(p):
                if e.tag!='Name':p.remove(e)
        if kind=='Delay':params=dict(params,capacity='1')
        if kind=='SelectOutput':params=dict(params,conditionIsProbabilistic='false',choiceIsVolatile='false')
        for key,value in params.items():param(o,key,value,key=='delayTime')
        # Explicit native icon presentation: embedded blocks otherwise exist
        # in the editor but have no shapes in the running Main presentation.
        presentation_id=b.ident();b.el(o,'PresentationId',presentation_id)
        icon=b.el(shape,'EmbeddedObjectPresentation');b.el(icon,'Id',presentation_id);b.el(icon,'Name',name+'_presentation');b.el(icon,'X',x);b.el(icon,'Y',y)
        lab=b.el(icon,'Label');b.el(lab,'X',0);b.el(lab,'Y',-25)
        for tag,v in [('PublicFlag','true'),('PresentationFlag','true'),('ShowLabel','true'),('DrawMode','SHAPE_DRAW_2D'),('EmbeddedIcon','true'),('Z',0),('Rotation',0),('ScaleType','AUTOMATICALLY_CALCULATED'),('GISScaleForRealEmbeddedObjectPresentationSize',1),('GISScaleForFixedEmbeddedObjectPresentationSize',1000)]:b.el(icon,tag,v)
        objects.append(o);names[name]=(kind,x,y)
    connectors=b.el(a,'Connectors')
    for k,(src,port,dst) in enumerate(EDGES):
        sk,sx,sy=names[src];dk,dx,dy=names[dst];c=b.el(connectors,'Connector');b.common(c,'flow'+str(k),sx,sy,public=False,show=False)
        for tag,package,cl,item in [('SourceEmbeddedObjectReference',PKG,'Main',src),('SourceConnectableItemReference',LIB,sk,port),('TargetEmbeddedObjectReference',PKG,'Main',dst),('TargetConnectableItemReference',LIB,dk,'in')]:
            ref=b.el(c,tag);b.el(ref,'PackageName',package);b.el(ref,'ClassName',cl);b.el(ref,'ItemName',item)
        points=b.el(c,'Points')
        if src=='campaignFinished' and port=='outF':coords=[(0,0),(-760,0),(-760,-250),(-720,-250)]
        elif src=='bothAware' and port=='outF':coords=[(0,0),(0,170),(545,170),(545,0)]
        else:coords=[(0,0),(dx-sx,dy-sy)]
        for x,y in coords:p=b.el(points,'Point');b.el(p,'X',x);b.el(p,'Y',y)
        # Draw the same connector route in the runtime presentation. These are
        # views of real connected PML ports, not additional behavioral logic.
        poly=b.el(shape,'Polyline');b.common(poly,'visibleFlow'+str(k),sx,sy,shape=True)
        for tag,v in [('LineWidth',1),('LineColor',b.color('909090')),('LineStyle','SOLID'),('LineMaterial','null'),('FillColor',-1),('FillMaterial','null'),('Closed','false'),('Rotation',0),('BeginArrowStyle',0),('EndArrowStyle',0),('BeginArrowSize',1),('EndArrowSize',1),('ZHeight',0)]:b.el(poly,tag,v)
        pp=b.el(poly,'Points')
        for x,y in coords:p=b.el(pp,'Point');b.el(p,'X',x);b.el(p,'Y',y);b.el(p,'Z',0)
    # Put runtime lines behind icons/text.
    for poly in list(shape.findall('Polyline')):shape.remove(poly);shape.insert(0,poly)
    b.text(shape,'flowHeading','Lab flowchart: Source, Delay, SelectOutput and Sink',24,25,23,True)
    b.text(shape,'flowHelp','Actual execution blocks. One control token schedules 300 customers; the social-network display is below.',24,65,14)
    b.text(shape,'flowLoopNote','False: repeat until 60 periods. Source creates a scheduler token, not another customer.',120,435,13)
    b.text(shape,'flowFunctionsNote','Rule functions (editable in the Main diagram). Network initialization and output still use custom support.',24,470,13)
    model.find('Frame/Height').text='1550'
    for kind in ['SimulationExperiment']:
        for ex in root.iter(kind):
            title=ex.find('PresentationProperties/Title')
            if title is not None:title.text='CampusProductLaunch_LabFlowchart : Simulation'
    out=ROOT/'CampusProductLaunch_LabFlowchart.alp';ET.indent(root,space='  ');ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
    ids=[e.text for e in root.iter('Id')];assert len(ids)==len(set(ids))
    for n,h in originals.items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    info=dict(model=out.name,blocks=len(BLOCKS),connectors=len(EDGES),functions=len(FUNCTIONS),palette_classes=['Source','Delay','SelectOutput','Sink'],original_hashes=originals,xml_and_ids_checked=True,engine_import_compile_run='Not yet verified',scope='Functional hybrid: PML controls behavior branches and clock; network setup/display/export remain custom Java. Not a no-code rewrite.')
    (ROOT/'sim/lab_flowchart_build.json').write_text(json.dumps(info,indent=2)+'\n')
    (ROOT/'anylogic/lab_flowchart_functions.json').write_text(json.dumps(FUNCTIONS,indent=2)+'\n')
    print(json.dumps(info,indent=2))

if __name__=='__main__':main()
