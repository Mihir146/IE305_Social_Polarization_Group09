"""Compile agent bodies against an installed AnyLogic engine, without running it.

This is a real API type check, not editor XML import or engine execution.
"""
from pathlib import Path
import argparse,tempfile,subprocess,json,os
ROOT=Path(__file__).resolve().parent.parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--install',type=Path,default=Path('/opt/anylogic'));a=p.parse_args()
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
        (tmp/'Main.java').write_text(prefix+(ROOT/'anylogic/Main_additional_class_code.java.txt').read_text()+'\n}')
        consumer='''import com.anylogic.engine.*;import com.anylogic.engine.presentation.*;
public class Consumer extends Agent {
 public ShapeRectangle nodeMark,headMark,beliefMark,focusMark;
'''
        (tmp/'Consumer.java').write_text(consumer+(ROOT/'anylogic/Consumer_additional_class_code.java.txt').read_text()+'\n}')
        result=subprocess.run(['javac','-cp',cp,'-d',str(tmp),str(tmp/'Main.java'),str(tmp/'Consumer.java')],capture_output=True,text=True)
        info=dict(installation=str(a.install),engine_jars=len(jars),real_agent_and_shape_api_compile=result.returncode==0,
            compiler_output=result.stderr,scope='Actual installed API type check; no editor import, engine execution or rendering',
            first_engine_screenshot='anylogic/evidence/first_engine_run_windows.jpg')
        (ROOT/'sim/installed_api_check.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
        if result.returncode:raise SystemExit(result.returncode)
if __name__=='__main__':main()
