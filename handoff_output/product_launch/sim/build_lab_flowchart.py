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
'chooseContact':r'''
int i = launch.lastI, rank = (int)(draws[1] * launch.degree[i]);
for (int j = 0; j < 300; j++) {
 if (launch.adj[i][j] && rank-- == 0) {
  launch.lastJ = j;
  z = launch.customers[j];
  launch.beforeJ = launch.afterJ = launch.customers[j].belief;
  break;
 }
}

launch.lastOutcome = "Neither customer knows the launch";''',
'findSimilarContacts':r'''
choices.clear();
int i = launch.lastI;
for (int k = 0; k < 300; k++) {
 if (k != i && !launch.adj[i][k] && Math.abs(launch.customers[k].belief - launch.beforeI) < launch.config.d)
  choices.add(k);
}''',
'findAnyContacts':r'''
choices.clear();
int i = launch.lastI;
for (int k = 0; k < 300; k++) {
 if (k != i && !launch.adj[i][k]) choices.add(k);
}''',
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

FLOW_VARIABLES=[
('draws','double[]','new double[6]'),
('informed','boolean','false'),
('a','ProductKernel.Customer','null'),
('z','ProductKernel.Customer','null'),
('customerIndex','int','0'),
('experienceIndex','int','0'),
('choices','java.util.ArrayList<Integer>','new java.util.ArrayList<Integer>()'),
('newBuyers','java.util.ArrayList<ProductKernel.Customer>','new java.util.ArrayList<ProductKernel.Customer>()'),
]


BLOCKS=[
('startCampaign','Source',60,140,{'arrivalType':'self.MANUAL'}),
('nextMeeting','Delay',205,140,{'delayTime':'0.005','onAtExit':r'''
if (launch.activationInPeriod == 0) launch.period++;
for (int k = 0; k < 6; k++) draws[k] = launch.eventRng.nextDouble();
launch.lastI = (int)(draws[0] * 300);
launch.lastJ = launch.lastNew = -1; informed = false;
a = launch.customers[launch.lastI]; z = null;
launch.beforeI = launch.afterI = a.belief;
launch.lastOutcome = "No discussion contact";'''.strip()}),
('hasContact','SelectOutput',380,140,{'condition':'launch.degree[launch.lastI] > 0'}),
('chooseNeighbor','Delay',555,140,{'delayTime':'0','onAtExit':'chooseContact();'}),
('eitherAware','SelectOutput',740,140,{'condition':'a.aware || z.aware'}),
('bothAware','SelectOutput',925,140,{'condition':'a.aware && z.aware'}),
('sharingWorks','SelectOutput',1120,140,{'condition':'draws[2] < launch.config.shareProb','onExitFalse':'launch.lastOutcome = "Launch news was not shared in this meeting";'}),
('receiveNews','Delay',1120,260,{'delayTime':'0','onAtExit':'ProductKernel.Customer other = a.aware ? z : a;\nother.aware = true; other.awarePeriod = launch.period; informed = true;'}),
('closeEnough','SelectOutput',925,260,{'condition':'Math.abs(launch.beforeI - launch.beforeJ) < launch.config.d'}),
('averageBeliefs','Delay',740,260,{'delayTime':'0','onAtExit':'a.belief = launch.beforeI + launch.config.mu * (launch.beforeJ - launch.beforeI);\nz.belief = launch.beforeJ + launch.config.mu * (launch.beforeI - launch.beforeJ);\nlaunch.lastOutcome = informed ? "News shared and opinions moved closer" : "Opinions moved closer";'}),
('replaceThisTie','SelectOutput',925,380,{'condition':'draws[3] < launch.config.phi','onEnter':'launch.lastOutcome = informed ? "Launch news shared; opinions too far apart" : "Opinions too far apart; contact kept";'}),
('preferSimilar','SelectOutput',1120,380,{'condition':'draws[4] < launch.config.h'}),
('scanSimilar','Delay',1120,500,{'delayTime':'0','onAtExit':'findSimilarContacts();'}),
('similarExists','SelectOutput',925,500,{'condition':'!choices.isEmpty()'}),
('scanAnyone','Delay',1120,620,{'delayTime':'0','onAtExit':'findAnyContacts();'}),
('anyoneExists','SelectOutput',925,620,{'condition':'!choices.isEmpty()'}),
('changeContact','Delay',740,500,{'delayTime':'0','onAtExit':r'''
int i = launch.lastI, j = launch.lastJ;
int k = choices.get((int)(draws[5] * choices.size()));
launch.adj[i][j] = launch.adj[j][i] = false;
launch.adj[i][k] = launch.adj[k][i] = true;
launch.degree[j]--; launch.degree[k]++; launch.rewires++;
launch.lastNew = k; rewireI = i; rewireK = k; rewireLife = 18;
launch.lastOutcome = "Disagreement: discussion contact replaced";'''.strip()}),
('finishAttempt','Delay',205,500,{'delayTime':'0','onAtExit':'launch.afterI = a.belief;\nif (launch.lastJ >= 0) launch.afterJ = z.belief;\nlaunch.activationInPeriod++;'}),
('periodFinished','SelectOutput',380,500,{'condition':'launch.activationInPeriod == 300'}),
('showCampaign','Delay',380,740,{'delayTime':'0','onAtExit':'showProgress();'}),
('campaignFinished','SelectOutput',205,740,{'condition':'launch.period >= 60 && launch.activationInPeriod == 0'}),
('finishCampaign','Sink',60,740,{'onEnter':'exportLaunch(); finishSimulation();'}),
('beginBuying','Delay',60,940,{'delayTime':'0','onAtExit':'customerIndex = 0; experienceIndex = 0; newBuyers.clear();'}),
('moreCustomers','SelectOutput',240,940,{'condition':'customerIndex < 300'}),
('buyerAware','SelectOutput',430,940,{'condition':'launch.customers[customerIndex].aware'}),
('notOwner','SelectOutput',620,940,{'condition':'!launch.customers[customerIndex].freeSample && launch.customers[customerIndex].paidPeriod < 0'}),
('canAfford','SelectOutput',810,940,{'condition':'launch.customers[customerIndex].budget >= launch.config.price'}),
('worthPrice','SelectOutput',1000,940,{'condition':'launch.customers[customerIndex].valueScale * launch.customers[customerIndex].belief >= launch.config.price'}),
('recordBuyer','Delay',1190,940,{'delayTime':'0','onAtExit':'ProductKernel.Customer buyer = launch.customers[customerIndex];\nbuyer.paidPeriod = launch.period; buyer.valueAtPurchase = buyer.valueScale * buyer.belief;\nnewBuyers.add(buyer);'}),
('nextCustomer','Delay',620,1060,{'delayTime':'0','onAtExit':'customerIndex++;'}),
('moreExperiences','SelectOutput',240,1180,{'condition':'experienceIndex < newBuyers.size()'}),
('revealExperience','Delay',430,1180,{'delayTime':'0','onAtExit':'newBuyers.get(experienceIndex).belief = newBuyers.get(experienceIndex).experience;\nexperienceIndex++;'}),
('savePeriod','Delay',620,1180,{'delayTime':'0','onAtExit':'launch.activationInPeriod = 0;\ndouble[] row = launch.snapshot(newBuyers.size());\nlaunch.history.add(row); launch.check(row);'}),
]
EDGES=[('startCampaign','out','nextMeeting'),('nextMeeting','out','hasContact'),('hasContact','outT','chooseNeighbor'),('hasContact','outF','finishAttempt'),('chooseNeighbor','out','eitherAware'),('eitherAware','outT','bothAware'),('eitherAware','outF','finishAttempt'),('bothAware','outT','closeEnough'),('bothAware','outF','sharingWorks'),('sharingWorks','outT','receiveNews'),('sharingWorks','outF','finishAttempt'),('receiveNews','out','closeEnough'),('closeEnough','outT','averageBeliefs'),('closeEnough','outF','replaceThisTie'),('averageBeliefs','out','finishAttempt'),('replaceThisTie','outT','preferSimilar'),('replaceThisTie','outF','finishAttempt'),('preferSimilar','outT','scanSimilar'),('preferSimilar','outF','scanAnyone'),('scanSimilar','out','similarExists'),('similarExists','outT','changeContact'),('similarExists','outF','scanAnyone'),('scanAnyone','out','anyoneExists'),('anyoneExists','outT','changeContact'),('anyoneExists','outF','finishAttempt'),('changeContact','out','finishAttempt'),('finishAttempt','out','periodFinished'),('periodFinished','outT','beginBuying'),('periodFinished','outF','showCampaign'),('showCampaign','out','campaignFinished'),('campaignFinished','outT','finishCampaign'),('campaignFinished','outF','nextMeeting'),('beginBuying','out','moreCustomers'),('moreCustomers','outT','buyerAware'),('moreCustomers','outF','moreExperiences'),('buyerAware','outT','notOwner'),('buyerAware','outF','nextCustomer'),('notOwner','outT','canAfford'),('notOwner','outF','nextCustomer'),('canAfford','outT','worthPrice'),('canAfford','outF','nextCustomer'),('worthPrice','outT','recordBuyer'),('worthPrice','outF','nextCustomer'),('recordBuyer','out','nextCustomer'),('nextCustomer','out','moreCustomers'),('moreExperiences','outT','revealExperience'),('moreExperiences','outF','savePeriod'),('revealExperience','out','moreExperiences'),('savePeriod','out','showCampaign')]

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
    code=code.replace('if(policyIndex<0||policyIndex>36)','if(policyIndex<0||policyIndex>35)').replace('Choose policyIndex0..35 or36 for batch','Choose one policyIndex0..35; this visual version runs one campaign')
    code=code.replace('launchBatch=policyIndex==36;launchCaseIndex=0;startLaunchCase(launchBatch?0:policyIndex,rep);','launchBatch=false;launchCaseIndex=0;startLaunchCase(policyIndex,rep);')
    a.find('AdditionalClassCode').text=code
    a.find('Events').clear();a.find('StartupCode').text='initializeLaunch();\nstartCampaign.inject(1);'
    a.find('.//Variable[Name="outputDirectory"]/Properties/DefaultValue/Code').text='"product_lab_output"'
    variables=a.find('Variables')
    for k,(name,typ,initial) in enumerate(FLOW_VARIABLES):
        v=b.el(variables,'Variable',Class='PlainVariable');b.common(v,name,1460,140+70*k,public=True,show=True)
        prop=b.el(v,'Properties',SaveInSnapshot='true',Constant='false',AccessType='public',StaticVariable='false');b.el(prop,'Type',typ);b.cv(prop,'InitialValue',initial)
    for k,p in enumerate(variables.findall('Variable[@Class="Parameter"]')):
        p.find('PresentationFlag').text='true';p.find('ShowLabel').text='true';p.find('X').text='1460';p.find('Y').text=str(790+70*k)
    # First editor viewport must contain the actual PML blocks. The network
    # presentation is a translated group below, preserving local UI coordinates.
    shape=a.find('Presentation/Level/Presentation')
    old_shapes=list(shape);shape.clear()
    network=b.el(shape,'Group');b.common(network,'networkPresentation',0,1450,shape=True);b.el(network,'Rotation',0)
    network_contents=b.el(network,'Presentation')
    for e in old_shapes:network_contents.append(e)
    functions=b.el(a,'Functions')
    for k,(name,body) in enumerate(FUNCTIONS.items()):
        f=b.el(functions,'Function',AccessType='public',StaticFunction='false');b.el(f,'ReturnModificator','VOID');b.el(f,'ReturnType','double');b.common(f,name,100+300*(k%4),1340,public=True,show=True);b.el(f,'Body',body.strip())
    sample=ET.parse(EXAMPLES/'basicmodels/Bank Office - Phase 3/Bank Office - Phase 3.alp').getroot().find('.//ActiveObjectClass[Name="Main"]')
    if model.find('RequiredLibraryReference[LibraryName="com.anylogic.libraries.processmodeling"]') is None:
        ref=b.el(model,'RequiredLibraryReference');b.el(ref,'LibraryName',LIB);b.el(ref,'VersionMajor',8);b.el(ref,'VersionMinor',0);b.el(ref,'VersionBuild',5)
    templates={o.findtext('ActiveObjectClass/ClassName'):o for o in sample.findall('EmbeddedObjects/EmbeddedObject') if o.findtext('ActiveObjectClass/ClassName') in ['Source','Delay','SelectOutput','Sink']}
    objects=a.find('EmbeddedObjects');names={}
    for name,kind,x,y,params in BLOCKS:
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
        if kind=='SelectOutput':
            b.text(shape,name+'TrueLabel','Yes',x+40,y-15,10)
            b.text(shape,name+'FalseLabel','No',x+40,y+15,10)
        objects.append(o);names[name]=(kind,x,y)
    connectors=b.el(a,'Connectors')
    for k,(src,port,dst) in enumerate(EDGES):
        sk,sx,sy=names[src];dk,dx,dy=names[dst];c=b.el(connectors,'Connector');b.common(c,'flow'+str(k),sx,sy,public=False,show=False)
        for tag,package,cl,item in [('SourceEmbeddedObjectReference',PKG,'Main',src),('SourceConnectableItemReference',LIB,sk,port),('TargetEmbeddedObjectReference',PKG,'Main',dst),('TargetConnectableItemReference',LIB,dk,'in')]:
            ref=b.el(c,tag);b.el(ref,'PackageName',package);b.el(ref,'ClassName',cl);b.el(ref,'ItemName',item)
        points=b.el(c,'Points')
        if src=='campaignFinished' and port=='outF':coords=[(0,0),(-175,0),(-175,-520),(0,-520),(0,-600)]
        elif dst=='finishAttempt' and src not in ['averageBeliefs','changeContact']:
            route_y=810+12*['hasContact','eitherAware','sharingWorks','replaceThisTie','anyoneExists'].index(src)
            coords=[(0,0),(60,0),(60,route_y-sy),(dx-sx,route_y-sy),(dx-sx,dy-sy)]
        elif src=='preferSimilar' and port=='outF':coords=[(0,0),(110,0),(110,240),(0,240)]
        elif src=='similarExists' and port=='outF':coords=[(0,0),(85,0),(85,120),(195,120)]
        elif src=='moreExperiences' and port=='outF':coords=[(0,0),(0,40),(380,40),(380,0)]
        elif dst=='nextCustomer':coords=[(0,0),(0,dy-sy),(dx-sx,dy-sy)]
        elif src=='nextCustomer':coords=[(0,0),(-380,0),(-380,-120)]
        elif src=='periodFinished' and port=='outT':coords=[(0,0),(-300,0),(-300,440),(-320,440)]
        elif src=='savePeriod':coords=[(0,0),(80,0),(80,-440),(-240,-440)]
        else:coords=[(0,0),(dx-sx,0),(dx-sx,dy-sy)]
        for x,y in coords:p=b.el(points,'Point');b.el(p,'X',x);b.el(p,'Y',y)
        # Draw the same connector route in the runtime presentation. These are
        # views of real connected PML ports, not additional behavioral logic.
        poly=b.el(shape,'Polyline');b.common(poly,'visibleFlow'+str(k),sx,sy,shape=True)
        for tag,v in [('LineWidth',1),('LineColor',b.color('909090')),('LineStyle','SOLID'),('LineMaterial','null'),('FillColor',-1),('FillMaterial','null'),('Closed','false'),('Rotation',0),('BeginArrowStyle',0),('EndArrowStyle',0),('BeginArrowSize',1),('EndArrowSize',1),('ZHeight',0)]:b.el(poly,tag,v)
        pp=b.el(poly,'Points')
        for x,y in coords:p=b.el(pp,'Point');b.el(p,'X',x);b.el(p,'Y',y);b.el(p,'Z',0)
    # Put runtime lines behind icons/text.
    for poly in list(shape.findall('Polyline')):shape.remove(poly);shape.insert(0,poly)
    b.text(shape,'flowHeading','1. Conversations and adaptive contacts - real process-library decisions',24,25,21,True)
    b.text(shape,'flowHelp','SelectOutput diamonds contain the actual yes/no tests. Actions contain short assignments. One token schedules 300 customers.',24,65,13)
    b.text(shape,'purchaseHeading','2. Buying round: inspect every customer BEFORE revealing any new experience',24,890,19,True)
    b.text(shape,'flowLoopNote','No customer is eligible? Skip to next customer. Once everyone is checked, update only the new owners.',24,1245,13)
    b.text(shape,'flowFunctionsNote','Remaining helpers: neighbor/candidate scans and display refresh. Initialization, metrics and CSV support still use Java.',24,1295,13)
    b.text(shape,'networkHeading','3. Existing agent network and results (same customer rules and random streams)',24,1410,19,True)
    model.find('Frame/Width').text='1400';model.find('Frame/Height').text='2350'
    for kind in ['SimulationExperiment']:
        for ex in root.iter(kind):
            title=ex.find('PresentationProperties/Title')
            if title is not None:title.text='CampusProductLaunch_LabFlowchart : Simulation'
    out=ROOT/'CampusProductLaunch_LabFlowchart.alp';ET.indent(root,space='  ');ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
    ids=[e.text for e in root.iter('Id')];assert len(ids)==len(set(ids))
    for n,h in originals.items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    info=dict(model=out.name,blocks=len(BLOCKS),decision_blocks=sum(t=='SelectOutput' for _,t,*_ in BLOCKS),connectors=len(EDGES),functions=len(FUNCTIONS),native_flow_variables=len(FLOW_VARIABLES),palette_classes=['Source','Delay','SelectOutput','Sink'],original_hashes=originals,xml_and_ids_checked=True,engine_import_compile_run='Expanded decision version not yet verified in actual editor/runtime',scope='PML explicitly controls awareness/sharing/confidence/rewiring/candidate fallback and individual purchase/experience passes. Only small assignments, neighbor scans and setup/metrics/display/export support remain Java.',two_pass_buying=True,primitive_random_draws_per_attempt=6)
    (ROOT/'sim/lab_flowchart_build.json').write_text(json.dumps(info,indent=2)+'\n')
    (ROOT/'anylogic/lab_flowchart_functions.json').write_text(json.dumps(FUNCTIONS,indent=2)+'\n')
    block_map=[dict(block=n,type=t,condition=p.get('condition'),action=p.get('onAtExit') or p.get('onEnter'),x=x,y=y) for n,t,x,y,p in BLOCKS]
    (ROOT/'anylogic/lab_flowchart_block_map.json').write_text(json.dumps(block_map,indent=2)+'\n')
    print(json.dumps(info,indent=2))

if __name__=='__main__':main()
