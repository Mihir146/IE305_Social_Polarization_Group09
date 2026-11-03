"""Render scientific plots with JFreeChart/JFreeSVG, both standard Java tools.

Uses copies already bundled in the installed AnyLogic examples; does not modify
AnyLogic or redistribute its libraries. Set --examples for another installation.
"""
from pathlib import Path
import argparse,json,subprocess,tempfile,os
ROOT=Path(__file__).resolve().parent.parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--examples',type=Path,default=Path('/opt/anylogic/plugins/com.anylogic.examples_8.9.10.202609241721/basicmodels/Custom Sankey Chart'));a=ap.parse_args()
    jars=list(a.examples.glob('jfree*.jar'))
    if len(jars)<2:raise ValueError('Specify the folder containing JFreeChart and JFreeSVG jars')
    cp=os.pathsep.join(map(str,jars));charts=json.loads((ROOT/'sim/analysis/presentation_chart_data.json').read_text());out=ROOT/'figures';out.mkdir(exist_ok=True)
    source=r'''
import java.awt.*;import java.awt.geom.*;import java.io.*;import java.nio.file.*;import java.util.*;
import org.jfree.chart.*;import org.jfree.chart.axis.*;import org.jfree.chart.plot.*;import org.jfree.chart.renderer.category.*;import org.jfree.chart.renderer.xy.*;import org.jfree.chart.title.*;import org.jfree.chart.ui.*;import org.jfree.chart.entity.*;
import org.jfree.data.category.*;import org.jfree.data.xy.*;import org.jfree.graphics2d.svg.*;
public class Figures {
 static Color[] colors={new Color(24,125,141),new Color(233,162,59),new Color(88,108,167)};
 static class AsymmetricBars extends BarRenderer {
  double[][] low,high;
  AsymmetricBars(double[][] lo,double[][] hi){low=lo;high=hi;setShadowVisible(false);setBarPainter(new StandardBarPainter());setMaximumBarWidth(.15);}
  public void drawItem(Graphics2D g,CategoryItemRendererState state,Rectangle2D area,CategoryPlot plot,CategoryAxis domain,ValueAxis range,CategoryDataset data,int row,int col,int pass){
   super.drawItem(g,state,area,plot,domain,range,data,row,col,pass);
   if(Double.isNaN(low[row][col]))return;
   double xx=calculateBarW0(plot,plot.getOrientation(),area,domain,state,row,col)+state.getBarWidth()/2;
   double ylo=range.valueToJava2D(low[row][col],area,plot.getRangeAxisEdge()),yhi=range.valueToJava2D(high[row][col],area,plot.getRangeAxisEdge());
   g.setColor(new Color(53,75,89));g.setStroke(new BasicStroke(1.6f));g.draw(new Line2D.Double(xx,ylo,xx,yhi));g.draw(new Line2D.Double(xx-5,ylo,xx+5,ylo));g.draw(new Line2D.Double(xx-5,yhi,xx+5,yhi));
  }
 }
 public static void main(String[] args)throws Exception{
  java.util.Locale.setDefault(java.util.Locale.US);
  java.util.List<String> lines=Files.readAllLines(Path.of(args[0]));String[] meta=lines.get(0).split("\\t",-1),cats=lines.get(1).split("\\t",-1);
  int ns=lines.size()-2,n=cats.length;String[] names=new String[ns];double[][] values=new double[ns][n],lo=new double[ns][n],hi=new double[ns][n];
  for(int r=0;r<ns;r++){String[] f=lines.get(r+2).split("\\t",-1);names[r]=f[0];for(int j=0;j<n;j++){values[r][j]=Double.parseDouble(f[1+3*j]);lo[r][j]=Double.parseDouble(f[2+3*j]);hi[r][j]=Double.parseDouble(f[3+3*j]);}}
  JFreeChart chart;
  if(meta[0].equals("line")){
   YIntervalSeriesCollection data=new YIntervalSeriesCollection();
   for(int r=0;r<ns;r++){YIntervalSeries ss=new YIntervalSeries(names[r]);for(int j=0;j<n;j++)ss.add(j,values[r][j],Double.isNaN(lo[r][j])?values[r][j]:lo[r][j],Double.isNaN(hi[r][j])?values[r][j]:hi[r][j]);data.addSeries(ss);}
   chart=ChartFactory.createXYLineChart(meta[1],meta.length>3?meta[3]:null,meta[2],data,PlotOrientation.VERTICAL,true,false,false);
   XYPlot plot=chart.getXYPlot();SymbolAxis axis=new SymbolAxis(meta.length>3?meta[3]:null,cats);axis.setGridBandsVisible(false);axis.setTickLabelFont(new Font("SansSerif",Font.PLAIN,17));axis.setLabelFont(new Font("SansSerif",Font.PLAIN,20));plot.setDomainAxis(axis);
   XYErrorRenderer rr=new XYErrorRenderer();rr.setDrawXError(false);rr.setDrawYError(true);rr.setDefaultLinesVisible(true);rr.setDefaultShapesVisible(true);rr.setCapLength(7);rr.setErrorPaint(new Color(53,75,89));rr.setErrorStroke(new BasicStroke(1.5f));
   for(int r=0;r<ns;r++){rr.setSeriesPaint(r,colors[r%colors.length]);rr.setSeriesStroke(r,new BasicStroke(3));}plot.setRenderer(rr);
   plot.setBackgroundPaint(Color.WHITE);plot.setRangeGridlinePaint(new Color(221,230,235));plot.setDomainGridlinesVisible(false);plot.setOutlineVisible(false);plot.getRangeAxis().setLabelFont(new Font("SansSerif",Font.PLAIN,20));plot.getRangeAxis().setTickLabelFont(new Font("SansSerif",Font.PLAIN,16));
  }else{
   DefaultCategoryDataset data=new DefaultCategoryDataset();for(int r=0;r<ns;r++)for(int j=0;j<n;j++)data.addValue(values[r][j],names[r],cats[j]);
   chart=ChartFactory.createBarChart(meta[1],meta.length>3?meta[3]:null,meta[2],data,PlotOrientation.VERTICAL,true,false,false);CategoryPlot plot=chart.getCategoryPlot();AsymmetricBars rr=new AsymmetricBars(lo,hi);for(int r=0;r<ns;r++)rr.setSeriesPaint(r,colors[r%colors.length]);plot.setRenderer(rr);plot.getDomainAxis().setLabelFont(new Font("SansSerif",Font.PLAIN,20));
   plot.setBackgroundPaint(Color.WHITE);plot.setRangeGridlinePaint(new Color(221,230,235));plot.setOutlineVisible(false);plot.getDomainAxis().setTickLabelFont(new Font("SansSerif",Font.PLAIN,cats.length>6?13:17));plot.getRangeAxis().setTickLabelFont(new Font("SansSerif",Font.PLAIN,16));plot.getRangeAxis().setLabelFont(new Font("SansSerif",Font.PLAIN,20));
  }
  double ymin=0,ymax=0;for(int r=0;r<ns;r++)for(int j=0;j<n;j++){ymin=Math.min(ymin,Double.isNaN(lo[r][j])?values[r][j]:lo[r][j]);ymax=Math.max(ymax,Double.isNaN(hi[r][j])?values[r][j]:hi[r][j]);}
  double span=Math.max(1,ymax-ymin);ValueAxis ya=meta[0].equals("line")?chart.getXYPlot().getRangeAxis():chart.getCategoryPlot().getRangeAxis();ya.setRange(ymin<0?ymin-.05*span:0,ymax+.08*span);
  if(ya instanceof NumberAxis){double raw=span/6,base=Math.pow(10,Math.floor(Math.log10(raw))),step=10*base;for(double m:new double[]{1,2,2.5,5,10})if(m*base>=raw){step=m*base;break;}((NumberAxis)ya).setTickUnit(new NumberTickUnit(step));((NumberAxis)ya).setNumberFormatOverride(new java.text.DecimalFormat("#,##0.##"));}
  chart.setBackgroundPaint(Color.WHITE);chart.getTitle().setFont(new Font("SansSerif",Font.BOLD,23));chart.getLegend().setItemFont(new Font("SansSerif",Font.PLAIN,17));chart.setPadding(new RectangleInsets(15,20,15,25));
  if(ns==1)chart.removeLegend();
  TextTitle note=new TextTitle(meta[1].contains("histogram")?"One synthetic market, N=300":"Synthetic simulations; pointwise 95% intervals where shown",new Font("SansSerif",Font.PLAIN,14));note.setPosition(RectangleEdge.BOTTOM);chart.addSubtitle(note);
  ChartUtils.saveChartAsPNG(new File(args[1]+".png"),chart,1400,840);
  SVGGraphics2D svg=new SVGGraphics2D(1400,840);chart.draw(svg,new Rectangle2D.Double(0,0,1400,840));Files.writeString(Path.of(args[1]+".svg"),svg.getSVGElement());
 }
}
'''
    with tempfile.TemporaryDirectory(prefix='ie305_jfree_figures_') as td:
        tmp=Path(td);(tmp/'Figures.java').write_text(source)
        r=subprocess.run(['javac','-cp',cp,'-d',str(tmp),str(tmp/'Figures.java')],capture_output=True,text=True)
        if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
        manifest=[]
        for i,d in enumerate(charts,1):
            clean=lambda s:str(s).replace('\n',' ').replace('\t',' ')
            labels={'Initial belief histogram':'Initial expected appeal (0–1)','Confidence quality diagnostic':'Mean personal experience q','Awareness and paid sales by price':'Launch price (Rs)','Confirmed sample quantity profit':'Free-sample policy','Confirmed profit contrasts':'Fixed paired comparison','Profit by price and recipient strategy':'Launch price (Rs)','Price and unit cost':'Unit cost (Rs)'}
            lines=['\t'.join([d.get('kind','bar'),clean(d['name']),clean(d['ylabel']),labels.get(d['name'],'')]),'\t'.join(map(clean,d['categories']))]
            for ss in d['series']:
                values=[]
                for j,v in enumerate(ss['values']):values.extend([str(v),str(ss['lo'][j]) if 'lo' in ss else 'NaN',str(ss['hi'][j]) if 'hi' in ss else 'NaN'])
                lines.append('\t'.join([clean(ss['name']),*values]))
            path=out/f'chart{i}_data.tsv';path.write_text('\n'.join(lines)+'\n')
            r=subprocess.run(['java','-Djava.awt.headless=true','-cp',str(tmp)+os.pathsep+cp,'Figures',str(path),str(out/f'chart{i}')],capture_output=True,text=True)
            if r.returncode:print(r.stderr);raise SystemExit(r.returncode)
            manifest.append(dict(chart=i,title=d['name'],tool='JFreeChart1.5.3 / JFreeSVG3.4.3',data=path.name,png=f'chart{i}.png',svg=f'chart{i}.svg'))
        (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Rendered',len(manifest),'PNG and SVG charts with exact supplied interval endpoints')
if __name__=='__main__':main()
