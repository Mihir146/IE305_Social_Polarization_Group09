"""Independent OOXML validation with installed Apache POI/XmlBeans.

No proprietary PowerPoint execution is claimed. Optional previews use Java2D;
native chart rendering may be unsupported, so previews are layout diagnostics.
"""
from pathlib import Path
import tempfile,subprocess,os,json
ROOT=Path(__file__).resolve().parent.parent

def main():
    libs=Path('/opt/anylogic/plugins/com.anylogic.third_party_libraries_8.9.10.202609241721/lib')
    cp=os.pathsep.join(str(p) for p in libs.glob('*.jar'))
    if not cp:raise ValueError('Installed Apache POI dependencies unavailable')
    source=r'''
import java.io.*;import java.awt.*;import java.awt.image.*;import javax.imageio.ImageIO;
import java.util.*;import org.apache.poi.xslf.usermodel.*;import org.apache.xmlbeans.*;
public class DeckCheck {
 public static void main(String[] args)throws Exception {
  try(XMLSlideShow deck=new XMLSlideShow(new FileInputStream(args[0]))){
   ArrayList<XmlError> errors=new ArrayList<>();XmlOptions options=new XmlOptions().setErrorListener(errors);
   boolean valid=deck.getCTPresentation().validate(options);int n=0;
   for(XSLFSlide s:deck.getSlides()){
    valid=s.getXmlObject().validate(options)&&valid;n++;
    if(true){
     Dimension size=deck.getPageSize();BufferedImage out=new BufferedImage(size.width*2,size.height*2,BufferedImage.TYPE_INT_RGB);
     Graphics2D g=out.createGraphics();g.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON);g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,RenderingHints.VALUE_TEXT_ANTIALIAS_ON);g.setColor(Color.WHITE);g.fillRect(0,0,out.getWidth(),out.getHeight());g.scale(2,2);
     s.draw(g);g.dispose();ImageIO.write(out,"png",new File(args[1],"slide"+n+"_layout_preview.png"));
    }
   }
   int c=0;for(XSLFChart chart:deck.getCharts()){valid=chart.getCTChartSpace().validate(options)&&valid;c++;}
   System.out.println("slides="+n+" charts="+c+" schema_valid="+valid);
   for(XmlError err:errors)System.out.println(err.toString());
   if(!valid)throw new AssertionError("OOXML schema validation failed");
  }
 }
}
'''
    with tempfile.TemporaryDirectory(prefix='ie305_deck_poi_') as td:
        tmp=Path(td);(tmp/'DeckCheck.java').write_text(source)
        result=subprocess.run(['javac','-cp',cp,'-d',str(tmp),str(tmp/'DeckCheck.java')],capture_output=True,text=True)
        if result.returncode:print(result.stderr);raise SystemExit(result.returncode)
        previews=ROOT/'presentation_previews';previews.mkdir(exist_ok=True)
        result=subprocess.run(['java','-Djava.awt.headless=true','-cp',str(tmp)+os.pathsep+cp,'DeckCheck',str(ROOT/'Campus_Product_Launch.pptx'),str(previews)],capture_output=True,text=True)
        info=dict(independent_tool='Apache POI 5.4.1 / XmlBeans 5.3.0 from installed AnyLogic dependencies',
            schema_validation_passed=result.returncode==0,output=result.stdout,diagnostics=result.stderr,
            scope='OOXML schema/type parsing; Java2D previews can omit native charts; no PowerPoint rendering claimed')
        (ROOT/'sim/deck_poi_checks.json').write_text(json.dumps(info,indent=2)+'\n');print(json.dumps(info,indent=2))
        if result.returncode:raise SystemExit(result.returncode)
if __name__=='__main__':main()
