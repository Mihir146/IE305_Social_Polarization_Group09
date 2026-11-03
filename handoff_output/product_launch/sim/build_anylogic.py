"""Embed the pure Java kernel in Main, avoiding an external JAR dependency."""
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    kernel=(ROOT/'anylogic/ProductKernel.java').read_text().replace('public class ProductKernel {','public static class ProductKernel {',1)
    wrapper=r'''
public ProductKernel launch;
public boolean launchExported=false;
public boolean launchBatch=false;
public int launchCaseIndex=0,activePolicy=6,activeRep=1000;

public void initializeLaunch() {
    if(policyIndex<0||policyIndex>36)throw new IllegalArgumentException("policyIndex must be0..35;36 runs the batch");
    launchBatch=policyIndex==36;launchCaseIndex=0;
    startLaunchCase(launchBatch?0:policyIndex,rep);
}

public void startLaunchCase(int policy,int replication) {
    activePolicy=policy;activeRep=replication;
    int normalPolicy=policy%18;
    ProductKernel.Config c=new ProductKernel.Config();
    c.price=new double[]{400,500,600}[(normalPolicy/2)%3];
    c.h=normalPolicy%2;c.nSamples=policy>=18?3:12;
    launch=new ProductKernel(c,replication,normalPolicy/6);
    if(consumers.size()!=c.N)throw new IllegalStateException("Set consumers population size to300");
    for(int i=0;i<c.N;i++) {
        Consumer a=consumers.get(i);a.customerId=i;a.state=launch.customers[i];
        int local=i/3;
        a.setXY(66+320*(i%3)+18*(local%10),268+16*(local/10));
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
    if(animateNetwork)for(Consumer a:consumers){
        a.nodeMark.setFillColor(a.stateColor());a.headMark.setFillColor(a.stateColor());
        a.beliefMark.setWidth(12*a.state.belief);
        a.focusMark.setVisible(a.customerId==launch.lastI||a.customerId==launch.lastJ||a.customerId==launch.lastNew);
    }
    statusLabel.setText(launchStatus());
    double[] r=launch.snapshot(0);
    kpiLabel.setText("Aware "+(int)r[1]+" / 300     |     Paid buyers "+(int)r[2]+"     |     Free bottles "+(int)r[3]+
        "\nRevenue Rs "+(int)r[5]+"     Cost Rs "+(int)r[6]+"     Profit Rs "+(int)r[7]);
    awarenessBar.setWidth(730*r[1]/300.0);salesBar.setWidth(730*r[2]/300.0);
    awarenessLabel.setText("Heard about the launch: "+(int)r[1]+" / 300");
    salesLabel.setText("Paid for a bottle: "+(int)r[2]+" / 300");
    String[] labels=new String[3];
    for(int g=0;g<3;g++)labels[g]="Aware "+(int)r[18+g]+" / 100   |   Paid "+(int)r[15+g];
    groupStatus0.setText(labels[0]);groupStatus1.setText(labels[1]);groupStatus2.setText(labels[2]);
    meetingLine.setVisible(launch.lastI>=0&&launch.lastJ>=0);
    newContactLine.setVisible(launch.lastNew>=0);
    if(launch.lastI>=0&&launch.lastJ>=0){
        showMeetingLine(meetingLine,launch.lastI,launch.lastJ);
        interactionLabel.setText("Selected meeting: customer "+launch.lastI+" and customer "+launch.lastJ+"  |  "+launch.lastOutcome);
        beliefLabel.setText(String.format(java.util.Locale.US,"Opinions in this meeting:  customer %d  %.3f -> %.3f     |     customer %d  %.3f -> %.3f",launch.lastI,launch.beforeI,launch.afterI,launch.lastJ,launch.beforeJ,launch.afterJ));
    }else{
        interactionLabel.setText(launch.lastI<0?"Free-sample owners start the conversation":"Selected customer has no discussion contact");
        beliefLabel.setText("Each person's blue bar shows opinion: short = low expected appeal, long = high expected appeal.");
    }
    if(launch.lastNew>=0)showMeetingLine(newContactLine,launch.lastI,launch.lastNew);
}

public void showMeetingLine(com.anylogic.engine.presentation.ShapeRectangle line,int i,int j){
    Consumer a=consumers.get(i),b=consumers.get(j);
    double dx=b.getX()-a.getX(),dy=b.getY()-a.getY();
    line.setPos(a.getX(),a.getY());line.setWidth(Math.sqrt(dx*dx+dy*dy));line.setRotation(Math.atan2(dy,dx));
}

public String launchStatus() {
    if(launch==null)return "Launch initializing";
    String targeting=new String[]{"Random people","People with many contacts","People spread across groups"}[launch.strategy];
    return "Period "+launch.period+" / 60     |     Price Rs "+(int)launch.config.price+"     |     "+launch.config.nSamples+" free samples"+
        "\nSampling: "+targeting+"     |     New discussion contacts: "+(launch.config.h==0?"random":"similar opinions");
}

public void advanceLaunchPeriod() {
    if(launchExported)return;
    if(animateNetwork){for(int tick=0;tick<10;tick++){launch.stepActivation();if(launch.activationInPeriod==0)break;}}
    else launch.stepPeriod();
    if(animateNetwork&&launch.activationInPeriod==0)refreshLaunchLinks();
    refreshLaunchDisplay();
    if(launch.period>=launch.config.periods&&launch.activationInPeriod==0){
        exportLaunch();
        if(launchBatch&&++launchCaseIndex<180)startLaunchCase(launchCaseIndex/5,rep+launchCaseIndex%5);
        else finishSimulation();
    }
}

public void exportLaunch() {
    if(launchExported)return;
    String id="policy"+activePolicy+"_rep"+activeRep;
    String scenario=launch.config.nSamples==12?"baseline":"budget3";
    java.nio.file.Path base=java.nio.file.Paths.get(outputDirectory);
    try {
        java.nio.file.Files.createDirectories(base.resolve("summary"));
        java.nio.file.Files.createDirectories(base.resolve("trajectories"));
        java.nio.file.Path summary=base.resolve("summary").resolve(id+".csv");
        java.nio.file.Files.write(summary,java.util.Arrays.asList(ProductKernel.SUMMARY_HEADER,launch.summaryCsv("anylogic",scenario)),java.nio.charset.StandardCharsets.UTF_8);
        java.util.ArrayList<String> lines=new java.util.ArrayList<>();
        lines.add("cohort,scenario,rep,strategy,price,h,"+ProductKernel.DAY_HEADER);
        for(double[] r:launch.history)lines.add("anylogic,"+scenario+","+activeRep+","+ProductKernel.STRATEGIES[launch.strategy]+","+launch.config.price+","+launch.config.h+","+ProductKernel.numbers(r));
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
