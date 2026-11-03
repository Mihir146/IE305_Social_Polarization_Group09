"""Embed the pure Java kernel in Main, avoiding an external JAR dependency."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    kernel=(ROOT/'anylogic/ProductKernel.java').read_text().replace('public class ProductKernel {','public static class ProductKernel {',1)
    wrapper=r'''
public ProductKernel launch;
public boolean launchExported=false;

public void initializeLaunch() {
    if(policyIndex<0||policyIndex>=18)throw new IllegalArgumentException("policyIndex must be0..17");
    ProductKernel.Config c=new ProductKernel.Config();
    c.price=new double[]{400,500,600}[(policyIndex/2)%3];
    c.h=policyIndex%2;
    launch=new ProductKernel(c,rep,policyIndex/6);
    if(consumers.size()!=c.N)throw new IllegalStateException("Set consumers population size to300");
    for(int i=0;i<c.N;i++) {
        Consumer a=consumers.get(i);a.customerId=i;a.state=launch.customers[i];
        double angle=2*Math.PI*(i/3)/100.0;
        double radius=30+8*Math.sqrt(i/3);
        a.setXY(150+250*(i%3)+radius*Math.cos(angle),230+radius*Math.sin(angle));
    }
    launchExported=false;
    refreshLaunchLinks();
    refreshLaunchDisplay();
}

public void refreshLaunchLinks() {
    for(Consumer a:consumers)a.disconnectFromAll();
    if(!animateNetwork)return;
    for(int i=0;i<launch.config.N;i++)for(int j=i+1;j<launch.config.N;j++)
        if(launch.adj[i][j])consumers.get(i).connectTo(consumers.get(j));
}

public void refreshLaunchDisplay() {
    if(launch==null)return;
    if(animateNetwork)for(Consumer a:consumers)a.nodeMark.setFillColor(a.stateColor());
    statusLabel.setText(launchStatus());
}

public String launchStatus() {
    if(launch==null)return "Launch initializing";
    double[] r=launch.history.get(launch.history.size()-1);
    return "Policy "+policyIndex+" | "+ProductKernel.STRATEGIES[launch.strategy]+" | price Rs "+launch.config.price+" | h="+launch.config.h+
        "\nPeriod "+launch.period+"/60 | aware "+(int)r[1]+" | paid buyers "+(int)r[2]+" | free samples "+(int)r[3]+
        "\nRevenue Rs "+(int)r[5]+" | total cost Rs "+(int)r[6]+" | profit Rs "+(int)r[7];
}

public void advanceLaunchPeriod() {
    if(launchExported)return;
    launch.stepPeriod();
    if(animateNetwork)refreshLaunchLinks();
    refreshLaunchDisplay();
    if(launch.period>=launch.config.periods){exportLaunch();finishSimulation();}
}

public void exportLaunch() {
    if(launchExported)return;
    String id="policy"+policyIndex+"_rep"+rep;
    java.nio.file.Path base=java.nio.file.Paths.get(outputDirectory);
    try {
        java.nio.file.Files.createDirectories(base.resolve("summary"));
        java.nio.file.Files.createDirectories(base.resolve("trajectories"));
        java.nio.file.Path summary=base.resolve("summary").resolve(id+".csv");
        java.nio.file.Files.write(summary,java.util.Arrays.asList(ProductKernel.SUMMARY_HEADER,launch.summaryCsv("anylogic","baseline")),java.nio.charset.StandardCharsets.UTF_8);
        java.util.ArrayList<String> lines=new java.util.ArrayList<>();
        lines.add("cohort,scenario,rep,strategy,price,h,"+ProductKernel.DAY_HEADER);
        for(double[] r:launch.history)lines.add("anylogic,baseline,"+rep+","+ProductKernel.STRATEGIES[launch.strategy]+","+launch.config.price+","+launch.config.h+","+ProductKernel.numbers(r));
        java.nio.file.Files.write(base.resolve("trajectories").resolve(id+".csv"),lines,java.nio.charset.StandardCharsets.UTF_8);
        launchExported=true;traceln("Launch CSV saved: "+summary.toAbsolutePath());
    }catch(java.io.IOException e){throw new RuntimeException("Launch CSV export failed",e);}
}
'''
    (ROOT/'anylogic/Main_additional_class_code.java.txt').write_text('// AnyLogic8.9PLE: paste the entire body into Main Additional class code.\n// Actual AnyLogic engine integration remains unexecuted here.\n'+kernel+'\n'+wrapper)
    consumer=r'''// Paste into Consumer Advanced Java > Additional class code.
public int customerId;
public Main.ProductKernel.Customer state;
public java.awt.Color stateColor() {
    if(state==null||!state.aware)return new java.awt.Color(140,155,170);
    if(state.freeSample)return new java.awt.Color(135,85,175);
    if(state.paidPeriod>=0)return new java.awt.Color(40,150,95);
    return new java.awt.Color(235,165,45);
}
public String customerTooltip() {
    if(state==null)return "Initializing";
    return "Customer "+customerId+" | group "+state.group+"\nBelief "+String.format(java.util.Locale.US,"%.2f",state.belief)+
        " | value Rs "+(int)(state.valueScale*state.belief)+" | budget Rs "+(int)state.budget+
        "\nAware="+state.aware+" | sample="+state.freeSample+" | paid period="+state.paidPeriod;
}
'''
    (ROOT/'anylogic/Consumer_additional_class_code.java.txt').write_text(consumer)
    print('Built self-contained Main and Consumer bodies for AnyLogic8.9PLE')

if __name__=='__main__':main()
