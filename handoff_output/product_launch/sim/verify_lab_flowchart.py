"""Check lab flow actions against original kernel, and installed API types.

Traversal follows the serialized connector graph and executes block actions
and conditions. This is not an AnyLogic editor/import or PML runtime test.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import tempfile,subprocess,json,os,csv

ROOT=Path(__file__).resolve().parent.parent
TYPES={'Group':'ShapeGroup','Rectangle':'ShapeRectangle','Text':'ShapeText','Oval':'ShapeOval'}

def fields(agent):
    return '\n'.join('public com.anylogic.engine.presentation.'+TYPES[e.tag]+' '+e.findtext('Name')+';' for e in agent.find('Presentation').iter() if e.tag in TYPES and e.find('Name') is not None)

def main():
    root=ET.parse(ROOT/'CampusProductLaunch_LabFlowchart.alp').getroot();a=root.find('.//ActiveObjectClass[Name="Main"]');person=root.find('.//ActiveObjectClass[Name="Consumer"]')
    blocks={e.findtext('Name'):e for e in a.findall('EmbeddedObjects/EmbeddedObject') if e.findtext('ActiveObjectClass/PackageName')=='com.anylogic.libraries.processmodeling'}
    edges={}
    for c in a.findall('Connectors/Connector'):
        edges[(c.findtext('SourceEmbeddedObjectReference/ItemName'),c.findtext('SourceConnectableItemReference/ItemName'))]=c.findtext('TargetEmbeddedObjectReference/ItemName')
    def value(o,n,default=''):return o.findtext('Parameters/Parameter[Name="'+n+'"]/Value/Code',default)
    cases=[]
    for name,o in blocks.items():
        kind=o.findtext('ActiveObjectClass/ClassName');p='case "'+name+'": {'
        if kind=='Source':p+='node="'+edges[name,'out']+'"; break;'
        elif kind=='Sink':p+='return;'
        elif kind=='Delay':p+=value(o,'onAtExit')+value(o,'onExit')+'node="'+edges[name,'out']+'"; break;'
        elif kind=='SelectOutput':p+=value(o,'onEnter')+'node=('+value(o,'condition')+')?"'+edges[name,'outT']+'":"'+edges[name,'outF']+'"; break;'
        cases.append(p+'}')
    functions='\n'.join('public void '+f.findtext('Name')+'(){\n'+f.findtext('Body')+'\n}' for f in a.findall('Functions/Function'))
    jars=list(Path('/opt/anylogic/plugins').glob('com.anylogic.engine*/**/*.jar'))+[Path('/opt/anylogic/plugins/com.anylogic.process_modeling_library_8.9.10.202609241721/lib/ProcessModelingLibrary.jar')]
    jars+=list(Path('/opt/anylogic/plugins').glob('com.anylogic.third_party_libraries*/lib/*.jar'))
    cp=os.pathsep.join(map(str,jars))
    with tempfile.TemporaryDirectory(prefix='ie305_lab_flow_') as td:
        tmp=Path(td)
        prefix='import java.util.*;import com.anylogic.engine.*;import com.anylogic.engine.presentation.*;public class Main extends Agent { public int policyIndex=6,rep=1000;public boolean animateNetwork=true;public String outputDirectory="product_lab_output";public ArrayList<Consumer> consumers=new ArrayList<>(); public com.anylogic.libraries.processmodeling.Source<Agent> startCampaign;'
        # Traverse actual block properties, with rendering overridden only for
        # pure kernel equality checks. Actual API methods still compile below.
        body=a.findtext('AdditionalClassCode')
        start=body.index('public void refreshLaunchDisplay()');end=body.index('public void exportLaunch()',start)
        # Preserve display implementation for the API compile; do not run it.
        runner='public void executeFlow(){String node="startCampaign";int visits=0;while(visits++<300000){switch(node){'+''.join(cases)+'default:throw new AssertionError(node);}}throw new AssertionError("Flow did not finish");}'
        src=prefix+fields(a)+body+functions+runner+'}'
        (tmp/'Main.java').write_text(src)
        (tmp/'Consumer.java').write_text('import com.anylogic.engine.*;import com.anylogic.engine.presentation.*;public class Consumer extends Agent {'+fields(person)+person.findtext('AdditionalClassCode')+'}')
        original=(ROOT/'anylogic/ProductKernel.java').read_text().replace('ProductKernel','OriginalKernel')
        (tmp/'OriginalKernel.java').write_text(original)
        # no UI updates in the branch harness; the exact same source was API-compiled.
        runner_src=r'''
public class FlowCheck {
 static class QuietMain extends Main {public void showProgress(){}}
 public static void main(String[] args){
  int cases=0;
  for(int policy=0;policy<36;policy++)for(int rep=1000;rep<1002;rep++){
   int normal=policy%18;Main m=new QuietMain();Main.ProductKernel.Config c=new Main.ProductKernel.Config();
   c.price=new double[]{400,500,600}[(normal/2)%3];c.h=normal%2;c.nSamples=policy>=18?3:12;
   m.launch=new Main.ProductKernel(c,rep,normal/6);
   OriginalKernel.Config z=new OriginalKernel.Config();z.price=c.price;z.h=c.h;z.nSamples=c.nSamples;
   OriginalKernel reference=new OriginalKernel(z,rep,normal/6);while(reference.period<60)reference.stepPeriod();
   m.executeFlow();
   if(m.launch.period!=60||m.launch.history.size()!=61)throw new AssertionError("Completion");
   for(int t=0;t<61;t++)for(int k=0;k<23;k++)if(Math.abs(m.launch.history.get(t)[k]-reference.history.get(t)[k])>1e-12)
    throw new AssertionError("Trajectory mismatch policy="+policy+" rep="+rep+" t="+t+" field="+k);
   for(int i=0;i<300;i++){
    if(m.launch.customers[i].belief!=reference.customers[i].belief||m.launch.customers[i].paidPeriod!=reference.customers[i].paidPeriod||m.launch.customers[i].awarePeriod!=reference.customers[i].awarePeriod)throw new AssertionError("Person mismatch");
    for(int j=0;j<300;j++)if(m.launch.adj[i][j]!=reference.adj[i][j])throw new AssertionError("Network mismatch");
   }
   cases++;
  }
  System.out.println("Exact original-kernel match: "+cases+" policy/seed cases, all61x23 trajectory fields, final beliefs/ties/purchase/awareness periods.");
 }
}'''
        (tmp/'FlowCheck.java').write_text(runner_src)
        r=subprocess.run(['javac','-cp',cp,'-d',str(tmp),*map(str,tmp.glob('*.java'))],capture_output=True,text=True)
        if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
        r=subprocess.run(['java','-Djava.awt.headless=true','-cp',str(tmp)+os.pathsep+cp,'FlowCheck'],capture_output=True,text=True)
        if r.returncode:print(r.stdout,r.stderr);raise SystemExit(r.returncode)
        info=dict(installed_api_compile=True,serialized_connector_graph_executed_in_harness=True,matching_cases=72,all_period_metrics_and_final_states_match=True,output=r.stdout,scope='Agent/shape/Source APIs compiled against installed libraries. Block graph/actions traversed by harness, not by PML engine. Actual AnyLogic editor import/compile/runtime still needs verification.')
        (ROOT/'sim/lab_flowchart_checks.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))

if __name__=='__main__':main()
