"""Compile/run Main wiring against stand-ins; this is NOT an AnyLogic test."""
from pathlib import Path
import subprocess,tempfile,csv,json
ROOT=Path(__file__).resolve().parent.parent

def main():
    with tempfile.TemporaryDirectory(prefix='ie305_product_wiring_') as td:
        tmp=Path(td)
        body=(ROOT/'anylogic/Main_additional_class_code.java.txt').read_text()
        consumer=(ROOT/'anylogic/Consumer_additional_class_code.java.txt').read_text()
        prefix='''import java.util.*;
public class Main {
 public int policyIndex=6,rep=1000; public boolean animateNetwork=true;
 public String outputDirectory;
 public ArrayList<Consumer> consumers=new ArrayList<>();
 public Label statusLabel=new Label(); public boolean finished=false;
 public Label kpiLabel=new Label(),awarenessLabel=new Label(),salesLabel=new Label();
 public Label groupStatus0=new Label(),groupStatus1=new Label(),groupStatus2=new Label(),interactionLabel=new Label(),beliefLabel=new Label();
 public com.anylogic.engine.presentation.ShapeRectangle awarenessBar=new com.anylogic.engine.presentation.ShapeRectangle(),salesBar=new com.anylogic.engine.presentation.ShapeRectangle(),meetingLine=new com.anylogic.engine.presentation.ShapeRectangle(),newContactLine=new com.anylogic.engine.presentation.ShapeRectangle();
 public void finishSimulation(){finished=true;}
 public void traceln(String x){}
 public static class Label{public String value; public void setText(String s){value=s;}}
'''
        (tmp/'Main.java').write_text(prefix+body+'\n}\n')
        stub='''import java.util.*;
public class Consumer {
 public Mark nodeMark=new Mark(),headMark=new Mark(),beliefMark=new Mark(),focusMark=new Mark();
 public static class Mark extends com.anylogic.engine.presentation.ShapeRectangle {public java.awt.Color fill; public void setFillColor(java.awt.Color c){fill=c;}}
 private HashSet<Consumer> links=new HashSet<>();
 private double px,py;public void setXY(double x,double y){px=x;py=y;}public double getX(){return px;}public double getY(){return py;}
 public void disconnectFromAll(){for(Consumer b:new HashSet<>(links))b.links.remove(this);links.clear();}
 public boolean connectTo(Consumer b){if(b==this)throw new IllegalArgumentException();boolean fresh=links.add(b);b.links.add(this);return fresh;}
'''
        (tmp/'Consumer.java').write_text(stub+consumer+'\n}\n')
        (tmp/'WiringCheck.java').write_text('''public class WiringCheck {
 public static void main(String[] a)throws Exception{
  Main m=new Main();m.outputDirectory=a[0];for(int i=0;i<300;i++)m.consumers.add(new Consumer());
  m.initializeLaunch();if(m.launch.history.get(0)[3]!=12)throw new AssertionError("Samples");
  for(int t=0;t<1800;t++)m.advanceLaunchPeriod();
  if(!m.finished||!m.launchExported||m.launch.period!=60)throw new AssertionError("Completion");
  String last=m.statusLabel.value;m.advanceLaunchPeriod();if(!last.equals(m.statusLabel.value))throw new AssertionError("Duplicate advance");
  for(int i=0;i<300;i++)if(m.consumers.get(i).state!=m.launch.customers[i])throw new AssertionError("State wiring");
  if(m.awarenessBar.width!=730||Math.abs(m.salesBar.width-730*148.0/300)>1e-10)throw new AssertionError("Bars");
  Main batch=new Main();batch.policyIndex=36;batch.animateNetwork=false;batch.outputDirectory=a[1];
  for(int i=0;i<300;i++)batch.consumers.add(new Consumer());batch.initializeLaunch();
  for(int t=0;t<10800;t++)batch.advanceLaunchPeriod();
  if(!batch.finished||batch.launchCaseIndex!=180)throw new AssertionError("Batch completion");
 }
}''')
        shape=tmp/'com/anylogic/engine/presentation/ShapeRectangle.java';shape.parent.mkdir(parents=True)
        shape.write_text('package com.anylogic.engine.presentation;public class ShapeRectangle{public double width;public void setWidth(double v){width=v;}public void setVisible(boolean v){}public void setPos(double x,double y){}public void setRotation(double v){}}')
        subprocess.run(['javac','-d',str(tmp),str(shape),str(tmp/'Main.java'),str(tmp/'Consumer.java'),str(tmp/'WiringCheck.java')],check=True,capture_output=True,text=True)
        output=tmp/'output'
        batchout=tmp/'batch'
        subprocess.run(['java','-cp',str(tmp),'WiringCheck',str(output),str(batchout)],check=True,capture_output=True,text=True)
        with (output/'summary/policy6_rep1000.csv').open() as f:got=list(csv.DictReader(f))
        with (ROOT/'sim/results/java_kernel_runs.csv').open() as f:
            reference=next(r for r in csv.DictReader(f) if r['rep']=='1000' and r['strategy']=='degree' and float(r['price'])==400 and float(r['h'])==0)
        assert len(got)==1 and set(got[0])==set(reference)
        for k,v in got[0].items():
            if k in ('cohort','secs'):continue
            try:assert abs(float(v)-float(reference[k]))<1e-10,(k,v,reference[k])
            except ValueError:assert v==reference[k],(k,v,reference[k])
        with (output/'trajectories/policy6_rep1000.csv').open() as f:trajectory=list(csv.DictReader(f))
        assert len(trajectory)==61 and float(trajectory[0]['period'])==0 and float(trajectory[-1]['period'])==60
        reference_rows=list(csv.DictReader((ROOT/'sim/results/java_kernel_runs.csv').open()))
        targets={(r['scenario'],r['strategy'],float(r['price']),float(r['h']),int(r['rep'])):r for r in reference_rows}
        batchfiles=list((batchout/'summary').glob('*.csv'));assert len(batchfiles)==180
        for path in batchfiles:
            rr=list(csv.DictReader(path.open()));assert len(rr)==1;r=rr[0]
            target=targets[(r['scenario'],r['strategy'],float(r['price']),float(r['h']),int(r['rep']))]
            for key,value in r.items():
                if key in ('cohort','secs'):continue
                try:assert abs(float(value)-float(target[key]))<1e-10,(path,key)
                except ValueError:assert value==target[key],(path,key)
    result=dict(java_wrapper_compiles_with_standins=True,customer_state_references=True,
        one_summary_and_61_period_rows=True,exact_match_to_standalone_java_kernel=True,
        anylogic_engine_compiled=False,anylogic_engine_executed=False,
        expected_default_paid_buyers=float(reference['paid_buyers']),expected_default_profit=float(reference['profit']))
    result.update(batch_cases_exactly_match_java=180,bar_and_group_text_wiring=True,
        scope='Stand-in wiring, no AnyLogic engine execution; real first-run evidence is separate')
    (ROOT/'sim/wrapper_readiness.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
