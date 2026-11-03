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
 public void finishSimulation(){finished=true;}
 public void traceln(String x){}
 public static class Label{public String value; public void setText(String s){value=s;}}
'''
        (tmp/'Main.java').write_text(prefix+body+'\n}\n')
        stub='''import java.util.*;
public class Consumer {
 public Mark nodeMark=new Mark();
 public static class Mark {public java.awt.Color fill; public void setFillColor(java.awt.Color c){fill=c;}}
 private HashSet<Consumer> links=new HashSet<>();
 public void setXY(double x,double y){}
 public void disconnectFromAll(){for(Consumer b:new HashSet<>(links))b.links.remove(this);links.clear();}
 public boolean connectTo(Consumer b){if(b==this)throw new IllegalArgumentException();boolean fresh=links.add(b);b.links.add(this);return fresh;}
'''
        (tmp/'Consumer.java').write_text(stub+consumer+'\n}\n')
        (tmp/'WiringCheck.java').write_text('''public class WiringCheck {
 public static void main(String[] a)throws Exception{
  Main m=new Main();m.outputDirectory=a[0];for(int i=0;i<300;i++)m.consumers.add(new Consumer());
  m.initializeLaunch();if(m.launch.history.get(0)[3]!=12)throw new AssertionError("Samples");
  for(int t=0;t<60;t++)m.advanceLaunchPeriod();
  if(!m.finished||!m.launchExported||m.launch.period!=60)throw new AssertionError("Completion");
  String last=m.statusLabel.value;m.advanceLaunchPeriod();if(!last.equals(m.statusLabel.value))throw new AssertionError("Duplicate advance");
  for(int i=0;i<300;i++)if(m.consumers.get(i).state!=m.launch.customers[i])throw new AssertionError("State wiring");
 }
}''')
        subprocess.run(['javac','-d',str(tmp),str(tmp/'Main.java'),str(tmp/'Consumer.java'),str(tmp/'WiringCheck.java')],check=True,capture_output=True,text=True)
        output=tmp/'output'
        subprocess.run(['java','-cp',str(tmp),'WiringCheck',str(output)],check=True,capture_output=True,text=True)
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
    result=dict(java_wrapper_compiles_with_standins=True,customer_state_references=True,
        one_summary_and_61_period_rows=True,exact_match_to_standalone_java_kernel=True,
        anylogic_engine_compiled=False,anylogic_engine_executed=False,
        expected_default_paid_buyers=float(reference['paid_buyers']),expected_default_profit=float(reference['profit']))
    (ROOT/'sim/wrapper_readiness.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
