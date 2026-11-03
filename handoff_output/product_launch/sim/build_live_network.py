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
  double angle=local*2.399963229728653,radius=165*Math.sqrt((local+.5)/100.0);
  a.setXY(220+425*(i%3)+radius*Math.cos(angle),405+radius*Math.sin(angle));
 }
 launchExported=false;visualFrame=0;recentI=recentJ=rewireI=rewireK=-1;rewireLife=0;lastTieRewires=-1;lastCurveRows=-1;
 drawnTies.clear();tieStyles.clear();linksLayer.clear();historyLayer.clear();histogramLayer.clear();networkHistory.clear();
 if(animateNetwork)refreshLaunchLinks();refreshLaunchDisplay();
}
public java.awt.Color beliefColor(double belief){
 return new java.awt.Color(55,126,184); // One flat blue for the opinion histogram; no color scale.
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
    com.anylogic.engine.presentation.ShapeLine edge=line(a.getX(),a.getY(),z.getX()-a.getX(),z.getY()-a.getY(),new java.awt.Color(150,150,150,35),.6,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_DOTTED);
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
   e.getValue().setColor(code==2?new java.awt.Color(115,115,115,65):code==1?new java.awt.Color(145,145,145,45):new java.awt.Color(145,145,145,35));tieStyles.put(e.getKey(),code);
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
  double[] a=launch.history.get(k-1),z=launch.history.get(k);double x1=65+325*a[0]/60.0,x2=65+325*z[0]/60.0;
  historyLayer.add(line(x1,825-70*a[1]/300,x2-x1,-70*(z[1]-a[1])/300,new java.awt.Color(55,126,184),2.1,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
  historyLayer.add(line(x1,825-70*a[2]/300,x2-x1,-70*(z[2]-a[2])/300,new java.awt.Color(39,145,90),2.3,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
 }
}
public void refreshLaunchDisplay(){
 if(launch==null)return;
 double[] r=launch.snapshot(0),m=networkMetrics();refreshHistory(m);
 if(!animateNetwork)return;
 for(Consumer a:consumers){a.nodeMark.setFillColor(a.stateColor());a.ownerMark.setFillColor(a.ownerColor());a.focusMark.setVisible(a.customerId==recentI||a.customerId==recentJ||a.customerId==rewireK&&rewireLife>0);}
 synchronizeDisplayedTies();
 statusLabel.setText("Period "+launch.period+" / 60   |   price Rs "+(int)launch.config.price+"   |   "+launch.config.nSamples+" samples\nRecipients: "+new String[]{"Random recipients","Most contacts","Across social groups"}[launch.strategy]+"   |   contacts: "+(launch.config.h==0?"random":"similar"));
 kpiLabel.setText("Aware "+(int)r[1]+" / 300        Paid buyers "+(int)r[2]+"        Free samples "+(int)r[3]+"        Profit Rs "+(int)r[7]);
 financeLabel.setText("Revenue Rs "+(int)r[5]+"  -  all bottle costs Rs "+(int)r[6]+"  =  modeled profit");
 reachLabel.setText("Aware "+(int)r[1]+"     Paid "+(int)r[2]+"     |     periods 0–60");
 statsLabel.setText(String.format(java.util.Locale.US,"Compatible ties  %.1f%%   |   Replaced  %d\nLargest component  %.1f%%\nMean belief  %.3f   |   SD  %.3f",100*m[1]/1200,launch.rewires,100*r[10],r[13],Math.sqrt(r[14])));
 reasonsLabel.setText("Aware, not buying: "+(int)m[3]+"\nBudget too low: "+(int)m[4]+"   |   value too low: "+(int)m[5]+"\nReady at the next period end: "+(int)m[6]);
 histogramLayer.clear();double max=1;for(int j=0;j<10;j++)max=Math.max(max,m[7+j]);
 for(int j=0;j<10;j++)histogramLayer.add(new com.anylogic.engine.presentation.ShapeRectangle(true,480+28*j,825-70*m[7+j]/max,0,null,beliefColor((j+.5)/10.0),20,70*m[7+j]/max,0,com.anylogic.engine.presentation.LineStyle.LINE_STYLE_SOLID));
 histMaxLabel.setText((int)max+" people at top of scale");
 meetingLine.setVisible(recentI>=0&&recentJ>=0);
 if(recentI>=0&&recentJ>=0){
  positionHighlight(meetingLine,recentI,recentJ);
  interactionLabel.setText("Meeting "+recentI+" and "+recentJ+"   |   "+recentOutcome);
  beliefLabel.setText(String.format(java.util.Locale.US,"Their opinions:  %.4f -> %.4f      and      %.4f -> %.4f",recentBeforeI,recentAfterI,recentBeforeJ,recentAfterJ));
 }else{interactionLabel.setText("Sample recipients begin the launch. Watch awareness travel through contacts.");beliefLabel.setText("Customers are colored by awareness and ownership. Opinions appear here and in the distribution plot.");}
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
 if(state==null||!state.aware)return new java.awt.Color(176,176,176);
 if(state.freeSample)return new java.awt.Color(255,159,28);
 if(state.paidPeriod>=0)return new java.awt.Color(39,145,90);
 return new java.awt.Color(55,126,184);
}
public java.awt.Color ownerColor(){return java.awt.Color.WHITE;}
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

def text(parent,name,value,x,y,size=16,bold=False,color='25394a'):
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
    mainagent.find('SceneBackgroundColor').text=str(b.color('ffffff'))
    for ruler in root.iter('ScaleRuler'):
        ruler.find('PresentationFlag').text='false';ruler.find('ShowLabel').text='false'
    shape=mainagent.find('Presentation/Level/Presentation');eop=shape.find('EmbeddedObjectPresentation');shape.remove(eop);shape.clear()
    pshape=person.find('Presentation/Level/Presentation');pshape.clear();oval(pshape,'focusMark',0,0,9,'222222');oval(pshape,'ownerMark',0,0,7,'ffffff');oval(pshape,'nodeMark',0,0,6,'b0b0b0')
    b.rectangle(shape,'canvasBackground',0,0,1290,900,'ffffff')
    group(shape,'linksLayer');b.rectangle(shape,'meetingLine',0,0,0,2.5,'222222');b.rectangle(shape,'newContactLine',0,0,0,2,'377eb8');shape.append(eop)
    group(shape,'historyLayer');group(shape,'histogramLayer')
    text(shape,'titleLabel','Product launch simulation',24,20,25,True)
    text(shape,'statusLabel','',24,57,14);text(shape,'kpiLabel','',24,104,19,True);text(shape,'financeLabel','',24,133,13,color='667483')
    text(shape,'interactionLabel','',24,162,14,True);text(shape,'beliefLabel','',24,188,14)
    for g in range(3):text(shape,'group'+str(g),'Social group '+str(g+1),170+425*g,590,15,color='667483')
    for i,(color,label) in enumerate([('b0b0b0','Unaware'),('377eb8','Aware, not owner'),('ff9f1c','Free sample'),('27915a','Paid buyer')]):oval(shape,'ownerKey'+str(i),34+205*i,640,5,color);text(shape,'ownerCaption'+str(i),label,48+205*i,631,13)
    text(shape,'tieLegend','Solid: similar beliefs   ·   Dotted: different beliefs',850,631,12,color='667483')
    text(shape,'activityLegend','Black line: selected meeting   ·   Blue line: new contact',24,662,12,color='667483')
    b.rectangle(shape,'plotDivider',24,689,1240,1,'e0e5ea')
    text(shape,'reachTitle','Awareness and paid sales',40,704,16,True);text(shape,'reachLabel','',40,729,11,color='667483')
    b.rectangle(shape,'reachAxis',64,756,1,70,'c4ccd4');b.rectangle(shape,'reachFloor',64,825,327,1,'c4ccd4')
    text(shape,'reachTop','300',27,748,11,color='667483');text(shape,'reachZero','0',45,815,11,color='667483');text(shape,'reachPeriod0','0',65,834,11,color='667483');text(shape,'reachPeriod60','60 periods',333,834,11,color='667483')
    text(shape,'awareCurveKey','— Aware',105,847,11,color='377eb8');text(shape,'paidCurveKey','— Paid',225,847,11,color='27915a')
    text(shape,'opinionTitle','Belief distribution',460,704,16,True);text(shape,'histMaxLabel','',460,729,11,color='667483');text(shape,'lowBelief','0 · low appeal',480,835,11,color='667483');text(shape,'highBelief','1 · high appeal',680,835,11,color='667483')
    text(shape,'statsTitle','Network and purchase decisions',840,704,16,True);text(shape,'statsLabel','',840,733,13);text(shape,'reasonsLabel','',840,793,12,color='667483')
    text(shape,'caption','300 customers, 1,200 actual ties. Positions show known social groups. All inputs synthetic.',24,879,11,color='667483')
    frame=model.find('Frame');frame.find('Width').text='1290';frame.find('Height').text='900'
    mainagent.find('.//Variable[Name="outputDirectory"]/Properties/DefaultValue/Code').text='"product_network_output"'
    ET.indent(root,space='  ');out=ROOT/'CampusProductLaunch_LiveNetwork.alp';ET.ElementTree(root).write(out,encoding='utf-8',xml_declaration=True)
    ids=[e.text for e in root.iter('Id')];assert len(ids)==len(set(ids));assert hashlib.sha256(stable.read_bytes()).hexdigest()==before
    info=dict(model=out.name,approved_grid_model_unchanged=True,grid_sha256=before,live_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
        same_kernel_source=True,summary_schema_unchanged=True,actual_engine_status='Prior network default export verified; this simplified presentation requires a visual check. API/wiring checks are separate.',new_export='network_metrics with disjoint buying reasons and 10 opinion bins')
    (ROOT/'sim/live_network_build.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
