// Standalone verification only. Running this is NOT an AnyLogic engine test.
public class KernelCheck {
    static void require(boolean ok,String message){if(!ok)throw new AssertionError(message);}
    public static void main(String[] args)throws Exception {
        ProductKernel.Config c=new ProductKernel.Config();c.N=2;c.k0=1;c.nSamples=0;c.periods=1;c.price=1001;c.phi=0;
        ProductKernel k=new ProductKernel(c,0,0);
        k.customers[0].belief=.2;k.customers[1].belief=.3;
        for(ProductKernel.Customer a:k.customers){a.aware=true;a.awarePeriod=0;}
        k.stepPeriod();require(Math.abs(k.customers[0].belief-.242)<1e-14&&Math.abs(k.customers[1].belief-.258)<1e-14,"Pair fixture");
        c=new ProductKernel.Config();c.N=30;c.k0=4;c.nSamples=3;c.periods=8;c.shareProb=0;
        k=new ProductKernel(c,2,1);while(k.period<c.periods)k.stepPeriod();
        double[] row=k.history.get(k.history.size()-1);require(row[1]==3&&row[2]==0&&row[7]==-750,"Zero sharing");
        c=new ProductKernel.Config();c.N=30;c.k0=4;c.nSamples=3;c.periods=2;c.price=0;
        k=new ProductKernel(c,2,0);for(ProductKernel.Customer a:k.customers){a.aware=true;a.awarePeriod=0;}
        while(k.period<c.periods)k.stepPeriod();row=k.history.get(k.history.size()-1);
        require(row[2]==27&&row[3]==3&&row[5]==0&&row[6]==7500,"Sample accounting");
        System.out.println("PASS: standalone Java pair, awareness and sample-accounting fixtures; NOT AnyLogic execution");
        if(args.length>0) {
            java.nio.file.Path output=java.nio.file.Paths.get(args[0]);
            try(java.io.BufferedWriter writer=java.nio.file.Files.newBufferedWriter(output,java.nio.charset.StandardCharsets.UTF_8)) {
                writer.write(ProductKernel.SUMMARY_HEADER);writer.newLine();
                for(int rep=1000;rep<1030;rep++)for(int strategy=0;strategy<3;strategy++)for(double price:new double[]{400,500,600})for(double h:new double[]{0,1}) {
                    c=new ProductKernel.Config();c.price=price;c.h=h;k=new ProductKernel(c,rep,strategy);
                    while(k.period<c.periods)k.stepPeriod();writer.write(k.summaryCsv("java_kernel","baseline"));writer.newLine();
                }
            }
            System.out.println("Wrote540 standalone Java kernel runs for distribution comparison");
        }
    }
}
