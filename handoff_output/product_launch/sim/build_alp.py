"""Serialize an editable AnyLogic project in the observed8.8.2 XML format.

Designed for opening/upgrading in8.9PLE. Well-formed XML and Java code checks do
not replace opening/compiling in the actual engine. No engine execution claimed.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import json
ROOT=Path(__file__).resolve().parent.parent
PKG='campusproductlaunch'
counter=1793700000000

def ident():
    global counter
    counter+=1;return str(counter)

def el(parent,tag,text=None,**attrs):
    a=ET.SubElement(parent,tag,attrs)
    if text is not None:a.text=str(text)
    return a

def cv(parent,tag,code,unit=None):
    a=el(parent,tag,Class='CodeUnitValue' if unit else 'CodeValue');el(a,'Code',code)
    if unit:el(a,'Unit','SECOND',Class='TimeUnits')
    return a

def common(parent,name,x=0,y=0,public=True,show=False,shape=False):
    id=ident();el(parent,'Id',id);el(parent,'Name',name);el(parent,'X',x);el(parent,'Y',y)
    lab=el(parent,'Label');el(lab,'X',10);el(lab,'Y',0)
    el(parent,'PublicFlag',str(public).lower());el(parent,'PresentationFlag','true');el(parent,'ShowLabel',str(show).lower())
    if shape:el(parent,'DrawMode','SHAPE_DRAW_2D');el(parent,'EmbeddedIcon','false');el(parent,'Z',0)
    return id

def color(code):
    n=int('ff'+code,16);return n-(1<<32)

def text(parent,name,label,x,y,size=16,bold=False):
    t=el(parent,'Text');common(t,name,x,y,shape=True)
    el(t,'Rotation',0);el(t,'Color',color('17364b'));el(t,'Text',label)
    font=el(t,'Font');el(font,'Name','SansSerif');el(font,'Size',size);el(font,'Style',1 if bold else 0)
    el(t,'Alignment','LEFT');return t

def rectangle(parent,name,x,y,w,h,fill):
    t=el(parent,'Rectangle');common(t,name,x,y,shape=True)
    for tag,value in [('ZHeight',0),('LineWidth',0),('LineColor',color(fill)),('LineMaterial','null'),('LineStyle','SOLID'),
                      ('Width',w),('Height',h),('Rotation',0),('FillColor',color(fill)),('FillMaterial','null')]:el(t,tag,value)
    return t

def agent(parent,name,code):
    a=el(parent,'ActiveObjectClass');id=ident();el(a,'Id',id);el(a,'Name',name)
    el(a,'AdditionalClassCode',code);el(a,'Generic','false')
    gp=el(a,'GenericParameter');gpid=ident();el(gp,'Id',gpid);el(gp,'Name',gpid)
    cv(gp,'GenericParameterValue','T extends Agent');el(gp,'GenericParameterLabel','Generic parameter:')
    for tag,value in [('FlowChartsUsage','ENTITY'),('SamplesToKeep',100),('LimitNumberOfArrayElements','false'),
                      ('ElementsLimitValue',100),('MakeDefaultViewArea','true'),('SceneBackgroundColor',-1),('SceneSkybox','null')]:el(a,tag,value)
    props=el(a,'AgentProperties');el(props,'EnvironmentDefinesInitialLocation','true');el(props,'RotateAnimationTowardsMovement','false');el(props,'RotateAnimationVertically','false')
    speed=el(props,'VelocityCode',Class='CodeUnitValue');el(speed,'Code',0);el(speed,'Unit','MPS',Class='SpeedUnits')
    for tag in ['PhysicalLength','PhysicalWidth','PhysicalHeight']:
        t=el(props,tag,Class='CodeUnitValue');el(t,'Code',1);el(t,'Unit','METER',Class='LengthUnits')
    env=el(a,'EnvironmentProperties');el(env,'EnableSteps','false');cv(env,'StepDurationCode',1,unit=True)
    for tag,value in [('SpaceType','CONTINUOUS'),('WidthCode',1000),('HeightCode',650),('ZHeightCode',0),('ColumnsCountCode',100),('RowsCountCode',100),
                      ('NeigborhoodType','MOORE'),('LayoutType','USER_DEF'),('LayoutTypeApplyOnStartup','true'),('NetworkType','USER_DEF'),('NetworkTypeApplyOnStartup','true'),
                      ('ConnectionsPerAgentCode',2),('ConnectionsRangeCode',50),('NeighborLinkFractionCode',.95),('MCode',10)]:el(env,tag,value)
    ds=el(a,'DatasetsCreationProperties');el(ds,'AutoCreate','false');el(ds,'OccurrenceAtTime','true');el(ds,'OccurrenceDate',1793664000000)
    cv(ds,'OccurrenceTime',0,unit=True);cv(ds,'RecurrenceCode',.5,unit=True)
    scale=el(a,'ScaleRuler');common(scale,'scale',0,-150,public=False)
    for tag,value in [('Length',100),('Rotation',0),('ScaleType','BASED_ON_LENGTH'),('ModelLength',100),('LengthUnits','METER'),('Scale',1),('InheritedFromParentAgentType','true')]:el(scale,tag,value)
    levelid=ident();linkid=ident();el(a,'CurrentLevel',levelid);el(a,'ConnectionsId',linkid)
    links=el(a,'AgentLinks');link=el(links,'AgentLink');el(link,'Id',linkid);el(link,'Name','connections');el(link,'X',50);el(link,'Y',-50)
    lab=el(link,'Label');el(lab,'X',15);el(lab,'Y',0)
    for tag,value in [('PublicFlag','false'),('PresentationFlag','true'),('ShowLabel','false'),('HandleReceiveInConnections','false'),('AgentLinkType','COLLECTION_OF_LINKS'),
                      ('AgentLinkBidirectional','true'),('MessageType','Object'),('LineStyle','SOLID'),('LineWidth',.5),('LineColor',int('448899aa',16)),
                      ('LineZOrder','UNDER_AGENTS'),('LineArrow','NONE'),('LineArrowPosition','END')]:el(link,tag,value)
    presentation=el(a,'Presentation');level=el(presentation,'Level');el(level,'Id',levelid);el(level,'Name','level');el(level,'X',0);el(level,'Y',0)
    lab=el(level,'Label');el(lab,'X',10);el(lab,'Y',0)
    for tag,value in [('PublicFlag','true'),('PresentationFlag','true'),('ShowLabel','false'),('DrawMode','SHAPE_DRAW_2D'),('Z',0),('LevelVisibility','DIM_NON_CURRENT')]:el(level,tag,value)
    shapes=el(level,'Presentation')
    return a,id,gpid,shapes

def timeprops(parent):
    t=el(parent,'ModelTimeProperties')
    for tag,value in [('StopOption','Never'),('InitialDate',1793664000000),('InitialTime',0),('FinalDate',1793750400000),('FinalTime',31)]:el(t,tag,value)

def main():
    root=ET.Element('AnyLogicWorkspace',WorkspaceVersion='1.9',AnyLogicVersion='8.8.4.202307181718',AlpVersion='8.8.2')
    model=el(root,'Model');el(model,'Id',ident());el(model,'Name','CampusProductLaunch');el(model,'EngineVersion',6);el(model,'JavaPackageName',PKG);el(model,'ModelTimeUnit','Second')
    classes=el(model,'ActiveObjectClasses')
    body=(ROOT/'anylogic/Main_additional_class_code.java.txt').read_text();consumer=(ROOT/'anylogic/Consumer_additional_class_code.java.txt').read_text()
    mainagent,mainid,_,mainshapes=agent(classes,'Main',body)
    person,personid,personGP,personshapes=agent(classes,'Consumer',consumer)
    rectangle(personshapes,'focusMark',-8,-8,16,16,'fde68a')
    rectangle(personshapes,'headMark',-2,-6,4,4,'8c9baa')
    rectangle(personshapes,'nodeMark',-4,-1,8,6,'8c9baa')
    rectangle(personshapes,'beliefTrack',-6,7,12,2,'d2dce5')
    rectangle(personshapes,'beliefMark',-6,7,6,2,'2463a0')
    el(mainagent,'StartupCode','initializeLaunch();')
    variables=el(mainagent,'Variables')
    for i,(name,type,value) in enumerate([('policyIndex','int','6'),('rep','int','1000'),('animateNetwork','boolean','true'),('outputDirectory','String','"product_output"')]):
        p=el(variables,'Variable',Class='Parameter');common(p,name,30,80+i*35,public=False,show=True)
        p.find('PresentationFlag').text='false';p.find('ShowLabel').text='false'
        prop=el(p,'Properties',SaveInSnapshot='true',ModificatorType='STATIC');el(prop,'Type',type);el(prop,'UnitType','NONE');el(prop,'SdArray','false');cv(prop,'DefaultValue',value)
        editor=el(prop,'ParameterEditor');el(editor,'Id',ident());el(editor,'EditorContolType','TEXT_BOX');el(editor,'MinSliderValue',0);el(editor,'MaxSliderValue',100);el(editor,'DelimeterType','NO_DELIMETER')
    objects=el(mainagent,'EmbeddedObjects');pop=el(objects,'EmbeddedObject');common(pop,'consumers',280,80,public=False,show=True)
    pop.find('ShowLabel').text='false';pop.find('PresentationFlag').text='false'
    presentationid=ident();el(pop,'PresentationId',presentationid)
    ref=el(pop,'ActiveObjectClass');el(ref,'PackageName',PKG);el(ref,'ClassName','Consumer')
    gps=el(pop,'GenericParameterSubstitute');ref=el(gps,'GenericParameterSubstituteReference');el(ref,'PackageName',PKG);el(ref,'ClassName','Consumer');el(ref,'ItemName',personGP)
    el(pop,'Parameters');el(pop,'ReplicationFlag','true');cv(pop,'Replication',300);el(pop,'CollectionType','ARRAY_LIST_BASED');el(pop,'InEnvironment','true');el(pop,'InitialLocationType','AT_ANIMATION_POSITION')
    for tag in ['XCode','YCode','ZCode','ColumnCode','RowCode','LatitudeCode','LongitudeCode']:cv(pop,tag,0)
    cv(pop,'LocationNameCode','""');el(pop,'InitializationType','SPECIFIED_NUMBER');q=el(pop,'InitializationDatabaseTableQuery');el(q,'TableReference');el(pop,'InitializationDatabaseType','ONE_AGENT_PER_DATABASE_RECORD');el(pop,'QuantityColumn')
    events=el(mainagent,'Events');event=el(events,'Event');common(event,'launchPeriod',280,140,public=False,show=True)
    event.find('PresentationFlag').text='false';event.find('ShowLabel').text='false'
    props=el(event,'Properties',TriggerType='timeout',Mode='cyclic');cv(props,'Timeout',.05,unit=True)
    rate=el(props,'Rate',Class='CodeUnitValue');el(rate,'Code',20);el(rate,'Unit','PER_SECOND',Class='RateUnits')
    el(props,'OccurrenceAtTime','true');el(props,'OccurrenceDate',1793664000000);cv(props,'OccurrenceTime',.05,unit=True);cv(props,'RecurrenceCode',.05,unit=True);el(props,'Condition','true');el(event,'Action','advanceLaunchPeriod();')
    eop=el(mainshapes,'EmbeddedObjectPresentation');el(eop,'Id',presentationid);el(eop,'Name','consumers_presentation');el(eop,'X',0);el(eop,'Y',0)
    lab=el(eop,'Label');el(lab,'X',10);el(lab,'Y',0)
    for tag,value in [('PublicFlag','true'),('PresentationFlag','true'),('ShowLabel','false'),('DrawMode','SHAPE_DRAW_2D'),('AsObject','true'),('EmbeddedIcon','false'),('Z',0),('Rotation',0),('DrawingMode','AGENT_CURRENT_POSITION'),('ScaleType','AUTOMATICALLY_CALCULATED'),('GISScaleForRealEmbeddedObjectPresentationSize',1),('GISScaleForFixedEmbeddedObjectPresentationSize',1000)]:el(eop,tag,value)
    text(mainshapes,'titleLabel','Can a smaller giveaway make a better product launch?',32,22,24,True)
    text(mainshapes,'introLabel','A synthetic campus market: news spreads, customers decide, the seller earns or loses.',32,60,16)
    text(mainshapes,'statusLabel','Initializing launch...',32,98,16)
    text(mainshapes,'kpiLabel','',32,154,18,True)
    for g in range(3):
        rectangle(mainshapes,'groupPanel'+str(g),32+320*g,225,290,230,'f0f4f7')
        text(mainshapes,'groupLabel'+str(g),'Social group '+str(g+1)+'  ·  100 customers',48+320*g,240,16,True)
        text(mainshapes,'groupStatus'+str(g),'',48+320*g,430,14)
    for i,(name,fill,label) in enumerate([('unaware','8c9baa','Unaware'),('aware','eba52d','Aware, not owner'),('sample','8755af','Free sample'),('paid','28965f','Paid buyer')]):
        rectangle(mainshapes,'legendMark'+str(i),40+i*235,477,13,13,fill);text(mainshapes,'legendLabel'+str(i),label,60+i*235,473,14)
    rectangle(mainshapes,'meetingLine',0,0,0,2,'2878c0');rectangle(mainshapes,'newContactLine',0,0,0,3,'e5922f')
    rectangle(mainshapes,'interactionPanel',32,515,930,95,'eff6fd')
    text(mainshapes,'interactionLabel','',48,532,14,True);text(mainshapes,'beliefLabel','',48,561,14)
    text(mainshapes,'interactionKey','Blue link = selected actual meeting. Orange = a new contact after rewiring. Only the latest of each 10 attempts is highlighted.',48,589,12)
    text(mainshapes,'awarenessLabel','Heard about the launch',32,632,15)
    rectangle(mainshapes,'awarenessTrack',195,657,730,12,'e5eaee');rectangle(mainshapes,'awarenessBar',195,657,0,12,'eba52d')
    text(mainshapes,'salesLabel','Paid for a bottle',32,684,15)
    rectangle(mainshapes,'salesTrack',195,709,730,12,'e5eaee');rectangle(mainshapes,'salesBar',195,709,0,12,'28965f')
    text(mainshapes,'clockLabel','Each person is an agent. Blue mini-bars show individual opinions. Yellow highlights mark the selected participants.',32,744,13)
    text(mainshapes,'dataLabel','Synthetic inputs; 60 periods are not calendar days. Ten interaction attempts per visual tick; purchases at period end.',32,767,13)
    mainshapes.remove(eop);mainshapes.append(eop)  # customer marks above panel backgrounds
    for tag,value in [('DifferentialEquationsMethod','EULER'),('MixedEquationsMethod','RK45_NEWTON'),('AlgebraicEquationsMethod','MODIFIED_NEWTON'),('AbsoluteAccuracy','1.0E-5'),('FixedTimeStep',.001),('RelativeAccuracy','1.0E-5'),('TimeAccuracy','1.0E-5')]:el(model,tag,value)
    frame=el(model,'Frame');el(frame,'Id',ident());el(frame,'Width',1000);el(frame,'Height',810)
    db=el(model,'Database');el(db,'Id',ident());el(db,'Logging','false');el(db,'AutoExport','false');el(db,'ImportSettings');el(db,'ExportSettings')
    run=el(model,'RunConfiguration',ActiveObjectClassId=mainid);el(run,'Id',ident());el(run,'Name','RunConfiguration');timeprops(run)
    anim=el(run,'AnimationProperties')
    for tag,value in [('StopNever','true'),('ExecutionMode','realTimeScaled'),('RealTimeScale',1),('EnableZoomAndPanning','true'),('EnableDeveloperPanel','true'),('ShowDeveloperPanelOnStart','false')]:el(anim,tag,value)
    el(run,'Inputs');el(run,'Outputs')
    experiments=el(model,'Experiments');experiment=el(experiments,'SimulationExperiment',ActiveObjectClassId=mainid);el(experiment,'Id',ident());el(experiment,'Name','Simulation')
    el(experiment,'CommandLineArguments','');el(experiment,'MaximumMemory',512);el(experiment,'RandomNumberGenerationType','fixedSeed');el(experiment,'CustomGeneratorCode','new Random()');el(experiment,'SeedValue',1);el(experiment,'SelectionModeForSimultaneousEvents','LIFO');el(experiment,'VmArgs','');el(experiment,'LoadRootFromSnapshot','false');el(experiment,'Parameters')
    pp=el(experiment,'PresentationProperties')
    for tag,value in [('EnableZoomAndPanning','true'),('ExecutionMode','realTimeScaled'),('Title','CampusProductLaunch : Simulation'),('EnableDeveloperPanel','true'),('ShowDeveloperPanelOnStart','false'),('RealTimeScale',1)]:el(pp,tag,value)
    timeprops(experiment);el(experiment,'BypassInitialScreen','true')
    ET.indent(root,space='  ');path=ROOT/'CampusProductLaunch.alp';ET.ElementTree(root).write(path,encoding='UTF-8',xml_declaration=True)
    parsed=ET.parse(path).getroot();assert parsed.find('.//ActiveObjectClass[Name="Main"]/AdditionalClassCode').text==body
    ids=[a.text for a in parsed.iter('Id')];assert len(ids)==len(set(ids))
    assert parsed.find('.//EmbeddedObject/Replication/Code').text=='300'
    assert parsed.find('.//Event/Action').text=='advanceLaunchPeriod();'
    info=dict(xml_well_formed=True,unique_ids=len(ids),agent_types=2,consumer_count=300,parameters=4,
              source_format='8.8.2; intended upgrade/open in8.9PLE',anylogic_compiled=False,anylogic_executed=False)
    (ROOT/'sim/alp_structure_checks.json').write_text(json.dumps(info,indent=2)+'\n')
    print(path,'written; XML structure checked; AnyLogic compilation remains pending')

if __name__=='__main__':main()
