"""Check the separate live-network wiring with stand-ins, never fake engine data."""
from pathlib import Path
import xml.etree.ElementTree as ET
import subprocess,tempfile,json,csv,hashlib
ROOT=Path(__file__).resolve().parent.parent
TYPES={'Group':'ShapeGroup','Rectangle':'ShapeRectangle','Text':'ShapeText','Oval':'ShapeOval'}

def shapes(agent):return [(TYPES[e.tag],e.findtext('Name')) for e in agent.find('Presentation').iter() if e.tag in TYPES and e.find('Name') is not None]
def fields(agent):return '\n'.join(f' public com.anylogic.engine.presentation.{t} {n}=new com.anylogic.engine.presentation.{t}();' for t,n in shapes(agent))

def main():
    tree=ET.parse(ROOT/'CampusProductLaunch_LiveNetwork.alp').getroot();agents={e.findtext('Name'):e for e in tree.findall('.//ActiveObjectClass')}
    baseline_hash=hashlib.sha256((ROOT/'CampusProductLaunch.alp').read_bytes()).hexdigest()
    with tempfile.TemporaryDirectory(prefix='ie305_live_network_wiring_') as td:
        tmp=Path(td);pkg=tmp/'com/anylogic/engine/presentation';pkg.mkdir(parents=True)
        source={
          'Shape':'public class Shape{public boolean visible;public void setVisible(boolean x){visible=x;}}',
          'LineStyle':'public enum LineStyle{LINE_STYLE_SOLID,LINE_STYLE_DOTTED,LINE_STYLE_DASHED}',
          'ShapeRectangle':'public class ShapeRectangle extends Shape{public double width;public ShapeRectangle(){}public ShapeRectangle(boolean p,double x,double y,double r,java.awt.Paint l,java.awt.Paint f,double w,double h,double lw,LineStyle s){width=w;}public void setWidth(double x){width=x;}public void setFillColor(java.awt.Color c){}public void setPos(double x,double y){}public void setRotation(double x){}}',
          'ShapeOval':'public class ShapeOval extends ShapeRectangle{}',
          'ShapeText':'public class ShapeText extends Shape{public String value;public void setText(Object o){value=o.toString();}}',
          'ShapeLine':'public class ShapeLine extends Shape{public ShapeLine(boolean p,double x,double y,java.awt.Paint c,double dx,double dy,double w,LineStyle s){}public void setLineStyle(LineStyle s){}public void setColor(java.awt.Color c){}}',
          'ShapeGroup':'public class ShapeGroup extends Shape{public java.util.ArrayList<Shape> children=new java.util.ArrayList<>();public void clear(){children.clear();}public void add(Shape s){children.add(s);}public boolean remove(Shape s){return children.remove(s);}}'
        }
        for name,body in source.items():(pkg/(name+'.java')).write_text('package com.anylogic.engine.presentation;'+body)
        prefix='''import java.util.*;public class Main {
 public int policyIndex=6,rep=1000;public boolean animateNetwork=true,finished=false;
 public String outputDirectory;
 public ArrayList<Consumer> consumers=new ArrayList<>();
 public void finishSimulation(){finished=true;}public void traceln(String s){}
'''
        (tmp/'Main.java').write_text(prefix+fields(agents['Main'])+'\n'+agents['Main'].findtext('AdditionalClassCode')+'\n}')
        consumer='''public class Consumer{
 private double px,py;public void setXY(double x,double y){px=x;py=y;}public double getX(){return px;}public double getY(){return py;}
 public void disconnectFromAll(){}public boolean connectTo(Consumer a){return true;}
'''
        (tmp/'Consumer.java').write_text(consumer+fields(agents['Consumer'])+'\n'+agents['Consumer'].findtext('AdditionalClassCode')+'\n}')
        (tmp/'LiveCheck.java').write_text('''public class LiveCheck{
 public static void main(String[] a){
  Main m=new Main();m.outputDirectory=a[0];for(int i=0;i<300;i++)m.consumers.add(new Consumer());m.initializeLaunch();
  if(m.drawnTies.size()!=1200)throw new AssertionError("All actual ties drawn");
  for(int z=0;z<1800;z++)m.advanceLaunchPeriod();
  if(!m.finished||m.launch.period!=60||m.networkHistory.size()!=61)throw new AssertionError("Completion/logging");
  for(int i=0;i<300;i++)if(m.consumers.get(i).state!=m.launch.customers[i])throw new AssertionError("Agent state");
  if(m.drawnTies.size()!=1200)throw new AssertionError("Conserved displayed edge count");
  Main b=new Main();b.policyIndex=36;b.animateNetwork=false;b.outputDirectory=a[1];for(int i=0;i<300;i++)b.consumers.add(new Consumer());b.initializeLaunch();
  for(int z=0;z<10800;z++)b.advanceLaunchPeriod();if(!b.finished||b.launchCaseIndex!=180)throw new AssertionError("Batch");
 }
}''')
        files=list(pkg.glob('*.java'))+[tmp/'Main.java',tmp/'Consumer.java',tmp/'LiveCheck.java']
        r=subprocess.run(['javac','-d',str(tmp),*map(str,files)],capture_output=True,text=True)
        if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
        output,batch=tmp/'output',tmp/'batch';r=subprocess.run(['java','-cp',str(tmp),'LiveCheck',str(output),str(batch)],capture_output=True,text=True)
        if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
        references=list(csv.DictReader((ROOT/'sim/results/java_kernel_runs.csv').open()))
        targets={(r['scenario'],r['strategy'],float(r['price']),float(r['h']),int(r['rep'])):r for r in references}
        for path in [*output.glob('summary/*.csv'),*batch.glob('summary/*.csv')]:
            rows=list(csv.DictReader(path.open()));assert len(rows)==1;row=rows[0];target=targets[(row['scenario'],row['strategy'],float(row['price']),float(row['h']),int(row['rep']))]
            for key,value in row.items():
                if key in ('cohort','secs'):continue
                try:assert abs(float(value)-float(target[key]))<1e-10,(path,key)
                except ValueError:assert value==target[key],(path,key)
        for path in [*output.glob('network_metrics/*.csv'),*batch.glob('network_metrics/*.csv')]:
            rows=list(csv.DictReader(path.open()));assert len(rows)==61
            for i,r in enumerate(rows):
                assert float(r['period'])==i
                assert float(r['compatible_edges'])+float(r['discordant_edges'])==1200
                assert sum(float(r[f'belief_bin{j}']) for j in range(10))==300
                assert sum(float(r[k]) for k in ('aware_cannot_afford','aware_low_value','ready_to_buy'))==float(r['aware_nonowners'])
                assert float(r['ready_to_buy'])==0
        assert len(list(batch.glob('summary/*.csv')))==180
    assert hashlib.sha256((ROOT/'CampusProductLaunch.alp').read_bytes()).hexdigest()==baseline_hash
    info=dict(wiring_compiles_with_standins=True,animated_default_matches_java=True,batch_matches_java=180,
        displayed_actual_ties=1200,customer_state_references=300,network_metric_rows_per_campaign=61,
        extra_metric_partitions_checked=True,approved_grid_model_unchanged=True,
        scope='Stand-in wiring only. Installed API compile is separate. Earlier network default engine export is verified; current simplified display still needs a visual check.')
    (ROOT/'sim/live_network_wiring_checks.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
if __name__=='__main__':main()
