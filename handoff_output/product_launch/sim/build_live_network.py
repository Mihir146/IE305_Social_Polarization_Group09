"""Separate live-network presentation; preserve the approved grid .alp exactly.

The kernel, random streams, purchase schedule and 49-column summary do not
change. Only presentation and an extra clearly defined metrics export are added.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import json,hashlib
import build_alp as b
ROOT=Path(__file__).resolve().parent.parent

WRAPPER=r'''
public ProductKernel launch;
public boolean launchExported=false,launchBatch=false;
public int launchCaseIndex=0,activePolicy=6,activeRep=1000,visualFrame=0,lastCurveRows=-1;
public int recentI=-1,recentJ=-1,rewireI=-1,rewireK=-1,rewireLife=0;
public double recentBeforeI,recentBeforeJ,recentAfterI,recentAfterJ;
public String recentOutcome="Campaign initialized";
public java.util.HashMap<Integer,com.anylogic.engine.presentation.ShapeLine> drawnTies=new java.util.HashMap<>();
public java.util.HashMap<Integer,Integer> tieStyles=new java.util.HashMap<>();
public int lastTieRewires=-1;
public java.util.ArrayList<String> networkHistory=new java.util.ArrayList<>();
public static final String NETWORK_HEADER="period,compatible_edges,discordant_edges,aware_nonowners,aware_cannot_afford,aware_low_value,ready_to_buy,belief_bin0,belief_bin1,belief_bin2,belief_bin3,belief_bin4,belief_bin5,belief_bin6,belief_bin7,belief_bin8,belief_bin9";

public void initializeLaunch(){
 if(policyIndex<0||policyIndex>36)throw new IllegalArgumentException("Choose policyIndex0..35 or36 for batch");
 launchBatch=policyIndex==36;launchCaseIndex=0;startLaunchCase(launchBatch?0:policyIndex,rep);
}
public void startLaunchCase(int policy,int replication){
 activePolicy=policy;activeRep=replication;int normal=policy%18;
 ProductKernel.Config c=new ProductKernel.Config();c.price=new double[]{400,500,600}[(normal/2)%3];c.h=normal%2;c.nSamples=policy>=18?3:12;
 launch=new ProductKernel(c,replication,normal/6);
 if(consumers.size()!=300)throw new IllegalStateException("Population must contain300 Consumer agents");
 for(int i=0;i<300;i++){
  Consumer a=consumers.get(i);a.customerId=i;a.state=launch.customers[i];int local=i/3;
  double angle=local*2.399963229728653,radius=127*Math.sqrt((local+.5)/100.0);
  a.setXY(170+280*(i%3)+radius*Math.cos(angle),405+radius*Math.sin(angle));
 }
 launchExported=false;visualFrame=0;recentI=recentJ=rewireI=rewireK=-1;rewireLife=0;lastTieRewires=-1;lastCurveRows=-1;
 drawnTies.clear();tieStyles.clear();linksLayer.clear();historyLayer.clear();histogramLayer.clear();networkHistory.clear();
 if(animateNetwork)refreshLaunchLinks();refreshLaunchDisplay();
}
public java.awt.Color beliefColor(double belief){
 double b=Math.max(0,Math.min(1,belief));return new java.awt.Color((int)(66+187*b),(int)(187-31*b),(int)(230-111*b));
}
public com.anylogic.engine.presentation.ShapeLine line(double x,double y,double dx,double dy,java.awt.Color color,double width,com.anylogic.engine.presentation.LineStyle style){
 return new com.anylogic.engine.presentation.ShapeLine(true,x,y,color,dx,dy,width,style);
}
public void refreshLaunchLinks(){
 for(Consumer a:consumers)a.disconnectFromAll();
 if(!animateNetwork)return;
 for(int i=0;i<300;i++)for(int j=i+1;j<300;j++)if(launch.adj[i][j])consumers.get(i).connectTo(consumers.get(j));
 synchronizeDisplayedTies();
}
public void synchronizeDisplayedTies(){
 if(!animateNetwork)return;
 if(launch.rewires!=lastTieRewires){
  java.util.Iterator<java.util.Map.Entry<Integer,com.anylogic.engine.presentation.ShapeLine>> it=drawnTies.entrySet().iterator();
  while(it.hasNext()){
   java.util.Map.Entry<Integer,com.anylogic.engine.presentation.ShapeLine> e=it.next();int i=e.getKey()/300,j=e.getKey()%300;
   if(!launch.adj[i][j]){linksLayer.remove(e.getValue());tieStyles.remove(e.getKey());it.remove();}
  }
  for(int i=0;i<300;i++)for(int j=i+1;j<300;j++)if(launch.adj[i][j]){
   int key=i*300+j;if(!drawnTies.containsKey(key)){
    Consumer a=consumers.get(i),z=consumers.get(j);
    com.anylogic.engine.presentation.ShapeLine edge=line(a.getX(),a.getY(),z.getX()-a.getX(),z.getY()-a.getY(),new java.awt.Color(132,151,179,30),.6,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_DOTTED);
    linksLayer.add(edge);drawnTies.put(key,edge);
   }
  }
  lastTieRewires=launch.rewires;
 }
 if(visualFrame%4==0||visualFrame==0)for(java.util.Map.Entry<Integer,com.anylogic.engine.presentation.ShapeLine> e:drawnTies.entrySet()){
  int i=e.getKey()/300,j=e.getKey()%300;ProductKernel.Customer a=launch.customers[i],z=launch.customers[j];
  boolean compatible=Math.abs(a.belief-z.belief)<launch.config.d;
  int code=compatible?(a.aware&&z.aware?2:1):0;
  if(tieStyles.getOrDefault(e.getKey(),-1)!=code){
   e.getValue().setLineStyle(compatible?com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID:com.anylogic.engine.presentation.LineStyle.LINE_STYLE_DOTTED);
   e.getValue().setColor(code==2?new java.awt.Color(74,194,202,65):code==1?new java.awt.Color(74,194,202,32):new java.awt.Color(158,168,191,28));tieStyles.put(e.getKey(),code);
  }
 }
}
public void positionHighlight(com.anylogic.engine.presentation.ShapeRectangle shape,int i,int j){
 Consumer a=consumers.get(i),z=consumers.get(j);double dx=z.getX()-a.getX(),dy=z.getY()-a.getY();
 shape.setPos(a.getX(),a.getY());shape.setWidth(Math.sqrt(dx*dx+dy*dy));shape.setRotation(Math.atan2(dy,dx));
}
public double[] networkMetrics(){
 int compatible=0,nonowners=0,budget=0,value=0,ready=0;int[] hist=new int[10];
 for(int i=0;i<300;i++){
  ProductKernel.Customer a=launch.customers[i];hist[Math.min(9,(int)(10*a.belief))]++;
  if(a.aware&&!a.freeSample&&a.paidPeriod<0){nonowners++;if(a.budget<launch.config.price)budget++;else if(a.valueScale*a.belief<launch.config.price)value++;else ready++;}
  for(int j=i+1;j<300;j++)if(launch.adj[i][j]&&Math.abs(a.belief-launch.customers[j].belief)<launch.config.d)compatible++;
 }
 if(budget+value+ready!=nonowners)throw new IllegalStateException("Decision-reason partition failed");
 double[] out=new double[17];out[0]=launch.period;out[1]=compatible;out[2]=1200-compatible;out[3]=nonowners;out[4]=budget;out[5]=value;out[6]=ready;
 int total=0;for(int j=0;j<10;j++){out[7+j]=hist[j];total+=hist[j];}if(total!=300)throw new IllegalStateException("Opinion histogram failed");return out;
}
public void refreshHistory(double[] metrics){
 if(launch.history.size()==lastCurveRows)return;
 lastCurveRows=launch.history.size();networkHistory.add(ProductKernel.numbers(metrics));
 if(!animateNetwork)return;
 historyLayer.clear();
 for(int k=1;k<launch.history.size();k++){
  double[] a=launch.history.get(k-1),z=launch.history.get(k);double x1=950+270*a[0]/60.0,x2=950+270*z[0]/60.0;
  historyLayer.add(line(x1,355-108*a[1]/300,x2-x1,-108*(z[1]-a[1])/300,new java.awt.Color(240,183,82),2.1,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
  historyLayer.add(line(x1,355-108*a[2]/300,x2-x1,-108*(z[2]-a[2])/300,new java.awt.Color(86,214,160),2.3,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
 }
}
public void refreshLaunchDisplay(){
 if(launch==null)return;
 double[] r=launch.snapshot(0),m=networkMetrics();refreshHistory(m);
 if(!animateNetwork)return;
 for(Consumer a:consumers){a.nodeMark.setFillColor(a.stateColor());a.ownerMark.setFillColor(a.ownerColor());a.focusMark.setVisible(a.customerId==recentI||a.customerId==recentJ||a.customerId==rewireK&&rewireLife>0);}
 synchronizeDisplayedTies();
 statusLabel.setText("Period "+launch.period+" / 60   |   price Rs "+(int)launch.config.price+"   |   "+launch.config.nSamples+" samples   |   "+new String[]{"Random recipients","Most contacts","Across social groups"}[launch.strategy]+"   |   contacts: "+(launch.config.h==0?"random":"similar"));
 kpiLabel.setText("AWARE "+(int)r[1]+" / 300        PAID "+(int)r[2]+"        FREE "+(int)r[3]+"        PROFIT Rs "+(int)r[7]);
 financeLabel.setText("Revenue Rs "+(int)r[5]+"  -  all bottle costs Rs "+(int)r[6]+"  =  modeled profit");
 reachLabel.setText("Aware "+(int)r[1]+"     Paid "+(int)r[2]+"     |     periods 0–60");
 statsLabel.setText(String.format(java.util.Locale.US,"Compatible ties  %.1f%%\nLargest connected group  %.1f%%\nContacts replaced  %d\nCross-social-group ties  %.1f%%\nMean belief  %.3f   |   SD  %.3f",100*m[1]/1200,100*r[10],launch.rewires,100*r[11],r[13],Math.sqrt(r[14])));
 reasonsLabel.setText("Aware nonowners: "+(int)m[3]+"\nBudget too low: "+(int)m[4]+"   |   value too low: "+(int)m[5]+"\nReady for period-end purchase: "+(int)m[6]);
 histogramLayer.clear();double max=1;for(int j=0;j<10;j++)max=Math.max(max,m[7+j]);
 for(int j=0;j<10;j++)histogramLayer.add(new com.anylogic.engine.presentation.ShapeRectangle(true,951+27*j,535-92*m[7+j]/max,0,null,beliefColor((j+.5)/10.0),20,92*m[7+j]/max,0,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
 histMaxLabel.setText((int)max+" people at top of scale");
 meetingLine.setVisible(recentI>=0&&recentJ>=0);
 if(recentI>=0&&recentJ>=0){
  positionHighlight(meetingLine,recentI,recentJ);
  interactionLabel.setText("RECENT MEETING  "+recentI+" and "+recentJ+"   |   "+recentOutcome);
  beliefLabel.setText(String.format(java.util.Locale.US,"Their opinions:  %.3f -> %.3f      and      %.3f -> %.3f",recentBeforeI,recentAfterI,recentBeforeJ,recentAfterJ));
 }else{interactionLabel.setText("Sample recipients begin the launch. Watch awareness travel through contacts.");beliefLabel.setText("Node fill: low appeal (blue) to high appeal (coral). Outer ring: ownership / awareness.");}
 newContactLine.setVisible(rewireLife>0&&rewireI>=0&&rewireK>=0);if(rewireLife>0)positionHighlight(newContactLine,rewireI,rewireK);
}
public void advanceLaunchPeriod(){
 if(launchExported)return;
 if(animateNetwork){
  for(int tick=0;tick<10;tick++){
   launch.stepActivation();
   if(launch.lastNew>=0){rewireI=launch.lastI;rewireK=launch.lastNew;rewireLife=18;}
   if(launch.activationInPeriod==0)break;
  }
 }else launch.stepPeriod();
 visualFrame++;if(rewireLife>0)rewireLife--;
 if(visualFrame%4==1||recentI<0){recentI=launch.lastI;recentJ=launch.lastJ;recentBeforeI=launch.beforeI;recentBeforeJ=launch.beforeJ;recentAfterI=launch.afterI;recentAfterJ=launch.afterJ;recentOutcome=launch.lastOutcome;}
 if(animateNetwork&&launch.activationInPeriod==0)refreshLaunchLinks();refreshLaunchDisplay();
 if(launch.period>=60&&launch.activationInPeriod==0){exportLaunch();if(launchBatch&&++launchCaseIndex<180)startLaunchCase(launchCaseIndex/5,rep+launchCaseIndex%5);else finishSimulation();}
}
public void exportLaunch(){
 if(launchExported)return;
 String id="policy"+activePolicy+"_rep"+activeRep,scenario=launch.config.nSamples==12?"baseline":"budget3";java.nio.file.Path base=java.nio.file.Paths.get(outputDirectory);
 try{
  java.nio.file.Files.createDirectories(base.resolve("summary"));java.nio.file.Files.createDirectories(base.resolve("trajectories"));java.nio.file.Files.createDirectories(base.resolve("network_metrics"));
  java.nio.file.Files.write(base.resolve("summary").resolve(id+".csv"),java.util.Arrays.asList(ProductKernel.SUMMARY_HEADER,launch.summaryCsv("anylogic",scenario)),java.nio.charset.StandardCharsets.UTF_8);
  java.util.ArrayList<String> rows=new java.util.ArrayList<>();rows.add("cohort,scenario,rep,strategy,price,h,"+ProductKernel.DAY_HEADER);
  for(double[] r:launch.history)rows.add("anylogic,"+scenario+","+activeRep+","+ProductKernel.STRATEGIES[launch.strategy]+","+launch.config.price+","+launch.config.h+","+ProductKernel.numbers(r));
  java.nio.file.Files.write(base.resolve("trajectories").resolve(id+".csv"),rows,java.nio.charset.StandardCharsets.UTF_8);
  java.util.ArrayList<String> net=new java.util.ArrayList<>();net.add(NETWORK_HEADER);net.addAll(networkHistory);java.nio.file.Files.write(base.resolve("network_metrics").resolve(id+".csv"),net,java.nio.charset.StandardCharsets.UTF_8);
  launchExported=true;traceln("Launch CSV saved: "+base.resolve("summary").resolve(id+".csv").toAbsolutePath());
 }catch(java.io.IOException e){throw new RuntimeException("CSV export failed",e);}
}
'''
CONSUMER=r'''
public int customerId;
public Main.ProductKernel.Customer state;
public java.awt.Color stateColor(){
 if(state==null||!state.aware)return new java.awt.Color(93,110,133);
 double b=Math.max(0,Math.min(1,state.belief));return new java.awt.Color((int)(66+187*b),(int)(187-31*b),(int)(230-111*b));
}
public java.awt.Color ownerColor(){
 if(state==null||!state.aware)return new java.awt.Color(125,142,165);
 if(state.freeSample)return new java.awt.Color(184,157,246);
 if(state.paidPeriod>=0)return new java.awt.Color(86,214,160);
 return new java.awt.Color(240,183,82);
}
public String customerTooltip(){
 if(state==null)return "Initializing";
 return "Customer "+customerId+" | group "+state.group+" | belief "+state.belief+" | perceived value Rs "+(int)(state.valueScale*state.belief)+" | budget Rs "+(int)state.budget+" | aware="+state.aware+" | free="+state.freeSample+" | paid period="+state.paidPeriod;
}
'''

def group(parent,name):
    e=b.el(parent,'Group');b.common(e,name,0,0,shape=True);b.el(e,'Rotation',0);contents=b.el(e,'Presentation');b.rectangle(contents,name+'Anchor',0,0,0,0,'0d1526');return e

def oval(parent,name,x,y,r,fill):
    e=b.el(parent,'Oval');b.common(e,name,x,y,shape=True)
    for tag,val in [('ZHeight',0),('LineWidth',0),('LineColor',b.color(fill)),('LineMaterial','null'),('LineStyle','SOLID'),('RadiusX',r),('RadiusY',r),('Rotation',0),('FillColor',b.color(fill)),('FillMaterial','null')]:b.el(e,tag,val)
    return e

def text(parent,name,value,x,y,size=16,bold=False,color='e4edf7'):
    e=b.text(parent,name,value,x,y,size,bold);e.find('Color').text=str(b.color(color));return e

def main():
    stable=ROOT/'CampusProductLaunch.alp';before=hashlib.sha256(stable.read_bytes()).hexdigest();root=ET.parse(stable).getroot();b.counter=max(int(e.text) for e in root.iter('Id'))
    model=root.find('Model');model.find('Name').text='CampusProductLaunch_LiveNetwork';model.find('JavaPackageName').text='campusproductlaunchnetwork'
    for e in root.iter('PackageName'):
        if e.text=='campusproductlaunch':e.text='campusproductlaunchnetwork'
    mainagent=root.find('.//ActiveObjectClass[Name="Main"]');person=root.find('.//ActiveObjectClass[Name="Consumer"]')
    kernel=(ROOT/'anylogic/ProductKernel.java').read_text().replace('public class ProductKernel {','public static class ProductKernel {',1)
    body=kernel+'\n'+WRAPPER;mainagent.find('AdditionalClassCode').text=body;person.find('AdditionalClassCode').text=CONSUMER
    folder=ROOT/'anylogic/live_network';folder.mkdir(exist_ok=True);(folder/'Main_additional_class_code.java.txt').write_text(body);(folder/'Consumer_additional_class_code.java.txt').write_text(CONSUMER)
    mainagent.find('SceneBackgroundColor').text=str(b.color('0d1526'))
    for ruler in root.iter('ScaleRuler'):
        ruler.find('PresentationFlag').text='false';ruler.find('ShowLabel').text='false'
    shape=mainagent.find('Presentation/Level/Presentation');eop=shape.find('EmbeddedObjectPresentation');shape.remove(eop);shape.clear()
    pshape=person.find('Presentation/Level/Presentation');pshape.clear();oval(pshape,'focusMark',0,0,9,'ffe3a1');oval(pshape,'ownerMark',0,0,6.5,'7d8ea5');oval(pshape,'nodeMark',0,0,4.4,'5d6e85')
    b.rectangle(shape,'canvasBackground',0,0,1290,900,'0d1526')
    b.rectangle(shape,'networkPanel',24,185,850,450,'121f32');b.rectangle(shape,'reachPanel',900,185,355,205,'17263b');b.rectangle(shape,'opinionPanel',900,405,355,175,'17263b');b.rectangle(shape,'statsPanel',900,595,355,205,'17263b');b.rectangle(shape,'meetingPanel',24,700,850,100,'17263b')
    group(shape,'linksLayer');b.rectangle(shape,'meetingLine',0,0,0,2.3,'ffe3a1');b.rectangle(shape,'newContactLine',0,0,0,3.0,'ff9a56');shape.append(eop)
    group(shape,'historyLayer');group(shape,'histogramLayer')
    text(shape,'titleLabel','THE LAUNCH NETWORK',24,20,29,True)
    text(shape,'introLabel','Watch launch news, opinions and purchases travel through a synthetic campus market.',24,57,16,color='9cafc5')
    text(shape,'statusLabel','',24,88,16);text(shape,'kpiLabel','',24,122,21,True);text(shape,'financeLabel','',24,154,14,color='9cafc5')
    text(shape,'networkTitle','300 individual customers · 1,200 actual discussion ties',42,203,17,True)
    for g in range(3):text(shape,'group'+str(g),'Social group '+str(g+1),106+280*g,580,16,True,color='9cafc5')
    text(shape,'reachTitle','REACH AND PAID SALES',920,204,17,True);text(shape,'reachLabel','',920,231,13,color='9cafc5')
    b.rectangle(shape,'reachAxis',949,246,1,110,'51647c');b.rectangle(shape,'reachFloor',949,355,275,1,'51647c')
    text(shape,'reachTop','300',917,247,11,color='9cafc5');text(shape,'reachZero','0',933,345,11,color='9cafc5');text(shape,'reachPeriod0','0',949,365,11,color='9cafc5');text(shape,'reachPeriod60','60 periods',1170,365,11,color='9cafc5')
    text(shape,'awareCurveKey','— Aware',990,372,12,color='f0b752');text(shape,'paidCurveKey','— Paid',1080,372,12,color='56d6a0')
    text(shape,'opinionTitle','CURRENT OPINIONS',920,421,17,True);text(shape,'histMaxLabel','',920,450,12,color='9cafc5');text(shape,'lowBelief','0 · low appeal',950,548,12,color='5ebee4');text(shape,'highBelief','1 · high appeal',1118,548,12,color='f39f7e')
    text(shape,'statsTitle','NETWORK AND DECISIONS',920,611,16,True);text(shape,'statsLabel','',920,639,14);text(shape,'reasonsLabel','',920,745,12,color='9cafc5')
    # Compact, explicit legends: link style is compatibility, not influence weight.
    text(shape,'tieLegend','Solid cyan: beliefs within tolerance   ·   Dotted gray: beliefs too far apart',34,647,14,color='9cafc5')
    text(shape,'activityLegend','Bright gold: a recent meeting   ·   Orange: a recently formed contact',34,671,14,color='9cafc5')
    text(shape,'interactionLabel','',42,718,14,True);text(shape,'beliefLabel','',42,748,14)
    text(shape,'meetingNote','One recent meeting is highlighted; all attempts affect the model. Purchases occur at period end.',42,778,12,color='9cafc5')
    for i,(color,label) in enumerate([('7d8ea5','Unaware'),('f0b752','Aware, not owner'),('b89df6','Free sample'),('56d6a0','Paid buyer')]):oval(shape,'ownerKey'+str(i),42+205*i,826,5,color);text(shape,'ownerCaption'+str(i),label,56+205*i,817,13,color='9cafc5')
    text(shape,'caption','Ring = awareness / ownership. Fill = current appeal. Positions show known groups, not opinion coordinates. All inputs synthetic.',24,855,12,color='9cafc5')
    frame=model.find('Frame');frame.find('Width').text='1290';frame.find('Height').text='900'
    mainagent.find('.//Variable[Name="outputDirectory"]/Properties/DefaultValue/Code').text='"product_network_output"'
    ET.indent(root,space='  ');out=ROOT/'CampusProductLaunch_LiveNetwork.alp';ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
    ids=[e.text for e in root.iter('Id')];assert len(ids)==len(set(ids));assert hashlib.sha256(stable.read_bytes()).hexdigest()==before
    info=dict(model=out.name,approved_grid_model_unchanged=True,grid_sha256=before,live_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        same_kernel_source=True,summary_schema_unchanged=True,actual_engine_status='Not yet run; API and wiring checks follow',new_export='network_metrics with disjoint buying reasons and 10 opinion bins')
    (ROOT/'sim/live_network_build.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
