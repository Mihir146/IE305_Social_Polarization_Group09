"""Compile agent bodies against an installed AnyLogic engine, without running it.

This is a real API type check, not editor XML import or engine execution.
"""
from pathlib import Path
import argparse,tempfile,subprocess,json,os,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parent.parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--install',type=Path,default=Path('/opt/anylogic'));p.add_argument('--model',type=Path);a=p.parse_args()
    jars=list((a.install/'plugins').glob('com.anylogic.engine*/**/*.jar'))
    if not jars:raise ValueError('No installed AnyLogic engine jars found')
    cp=os.pathsep.join(map(str,jars))
    with tempfile.TemporaryDirectory(prefix='ie305_real_anylogic_api_') as td:
        tmp=Path(td)
        prefix='''import java.util.*;
import com.anylogic.engine.*;
import com.anylogic.engine.presentation.*;
import static com.anylogic.engine.Utilities.*;
public class Main extends Agent {
 public int policyIndex=6,rep=1000;public boolean animateNetwork=true;
 public String outputDirectory="product_output";
 public ArrayList<Consumer> consumers=new ArrayList<>();
 public ShapeText statusLabel,kpiLabel,awarenessLabel,salesLabel,groupStatus0,groupStatus1,groupStatus2,interactionLabel,beliefLabel;
 public ShapeRectangle awarenessBar,salesBar,meetingLine,newContactLine;
'''
        if a.model:
            tree=ET.parse(a.model).getroot();agents={e.findtext('Name'):e for e in tree.findall('.//ActiveObjectClass')};types={'Group':'ShapeGroup','Rectangle':'ShapeRectangle','Text':'ShapeText','Oval':'ShapeOval'}
            def fields(agent):return '\n'.join(' public '+types[e.tag]+' '+e.findtext('Name')+';' for e in agent.find('Presentation').iter() if e.tag in types and e.find('Name') is not None)
            prefix=prefix[:prefix.index(' public ShapeText')]+fields(agents['Main'])+'\n'
            mainbody=agents['Main'].findtext('AdditionalClassCode')
        else:mainbody=(ROOT/'anylogic/Main_additional_class_code.java.txt').read_text()
        (tmp/'Main.java').write_text(prefix+mainbody+'\n}')
        consumer='''import com.anylogic.engine.*;import com.anylogic.engine.presentation.*;
public class Consumer extends Agent {
 public ShapeRectangle nodeMark,headMark,beliefMark,focusMark;
'''
        if a.model:consumer='import com.anylogic.engine.*;import com.anylogic.engine.presentation.*;public class Consumer extends Agent {\n'+fields(agents['Consumer'])+'\n';consumerbody=agents['Consumer'].findtext('AdditionalClassCode')
        else:consumerbody=(ROOT/'anylogic/Consumer_additional_class_code.java.txt').read_text()
        (tmp/'Consumer.java').write_text(consumer+consumerbody+'\n}')
        result=subprocess.run(['javac','-cp',cp,'-d',str(tmp),str(tmp/'Main.java'),str(tmp/'Consumer.java')],capture_output=True,text=True)
        info=dict(installation=str(a.install),engine_jars=len(jars),real_agent_and_shape_api_compile=result.returncode==0,
            compiler_output=result.stderr,scope='Actual installed API type check; no editor import, engine execution or rendering',
            first_engine_screenshot='anylogic/evidence/first_engine_run_windows.jpg')
        name='live_network_api_check.json' if a.model else 'installed_api_check.json'
        (ROOT/'sim'/name).write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
        if result.returncode:raise SystemExit(result.returncode)
if __name__=='__main__':main()
