// Standalone Java kernel. The AnyLogic Main body embeds this as a static class.
// This class uses no AnyLogic APIs; engine integration is checked separately.
public class ProductKernel {
    public static class Config {
        public int N=300,k0=8,groups=3,periods=60,nSamples=12;
        public double withinWeight=6,price=500,unitCost=250,d=.2,mu=.3,phi=.05,h=0,
            shareProb=.25,quality=.8,experienceSD=.1;
        public void check() {
            if(N<2||k0<0||k0>=N||groups!=3||periods<1||nSamples<0||nSamples>N||withinWeight<1||price<0||unitCost<0||
               !(d>0&&d<=1&&mu>=0&&mu<=.5&&phi>=0&&phi<=1&&h>=0&&h<=1&&shareProb>=0&&shareProb<=1&&quality>=0&&quality<=1&&experienceSD>=0))
                throw new IllegalArgumentException("Invalid launch configuration");
        }
    }
    public static class Customer {
        public int group,awarePeriod=-1,paidPeriod=-1;
        public double initialBelief,belief,valueScale,budget,experience,valueAtPurchase=-1;
        public boolean aware=false,freeSample=false;
    }
    public static final String[] STRATEGIES={"random","degree","distributed"};
    public static final String DAY_HEADER="period,aware,paid_buyers,free_samples,new_paid,revenue,total_cost,profit,paid_adoption,min_group_adoption,giant_frac,cross_group_frac,rewires,belief_mean,belief_variance,paid_group0,paid_group1,paid_group2,aware_group0,aware_group1,aware_group2,degree_zero,total_edges";
    public static final String SUMMARY_HEADER="cohort,scenario,rep,graph_seed,trait_seed,selection_seed,event_seed,strategy,N,k0,groups,within_weight,periods,n_samples,price,unit_cost,d,mu,phi,h,share_prob,quality,experience_sd,aware,paid_buyers,free_samples,new_paid,revenue,total_cost,profit,paid_adoption,min_group_adoption,giant_frac,cross_group_frac,rewires,belief_mean,belief_variance,paid_group0,paid_group1,paid_group2,aware_group0,aware_group1,aware_group2,degree_zero,total_edges,t20,hit20,restricted_t20,secs";
    public final Config config;
    public final int rep,strategy;
    public final Customer[] customers;
    public final boolean[][] adj;
    public final int[] degree;
    public final java.util.ArrayList<double[]> history=new java.util.ArrayList<>();
    public int period=0,rewires=0;
    public final java.util.Random eventRng;
    private final long started=System.nanoTime();

    public ProductKernel(Config c,int replication,int seedingStrategy) {
        c.check();if(replication<0||replication>=1000000||seedingStrategy<0||seedingStrategy>2)
            throw new IllegalArgumentException("Invalid replication or strategy");
        config=c;rep=replication;strategy=seedingStrategy;
        int n=c.N;customers=new Customer[n];adj=new boolean[n][n];degree=new int[n];
        java.util.Random graphRng=new java.util.Random(1000000L+rep);
        int edges=0,target=n*c.k0/2;
        while(edges<target) {
            int i=graphRng.nextInt(n),j=graphRng.nextInt(n);
            if(i==j||adj[i][j])continue;
            if(i%3!=j%3&&graphRng.nextDouble()>=1/c.withinWeight)continue;
            adj[i][j]=adj[j][i]=true;degree[i]++;degree[j]++;edges++;
        }
        java.util.Random traitRng=new java.util.Random(2000000L+rep);
        for(int i=0;i<n;i++) {
            Customer a=new Customer();a.group=i%3;
            double u=traitRng.nextDouble(),v=traitRng.nextDouble(),w=traitRng.nextDouble();
            a.initialBelief=Math.max(Math.min(u,v),Math.min(Math.max(u,v),w));
            a.belief=a.initialBelief;a.valueScale=500+500*traitRng.nextDouble();
            a.budget=400+600*traitRng.nextDouble();
            a.experience=Math.max(0,Math.min(1,c.quality+c.experienceSD*traitRng.nextGaussian()));
            customers[i]=a;
        }
        int[] priority=new int[n],rank=new int[n];for(int i=0;i<n;i++)priority[i]=i;
        java.util.Random selectionRng=new java.util.Random(3000000L+rep);
        for(int i=n-1;i>0;i--){int j=selectionRng.nextInt(i+1),tmp=priority[i];priority[i]=priority[j];priority[j]=tmp;}
        for(int i=0;i<n;i++)rank[priority[i]]=i;
        Integer[] order=new Integer[n];for(int i=0;i<n;i++)order[i]=i;
        java.util.Arrays.sort(order,(a,b)->degree[a]!=degree[b]?Integer.compare(degree[b],degree[a]):Integer.compare(rank[a],rank[b]));
        if(strategy==0)for(int t=0;t<c.nSamples;t++)sample(priority[t]);
        else if(strategy==1)for(int t=0;t<c.nSamples;t++)sample(order[t]);
        else {
            int picked=0,g=0;
            while(picked<c.nSamples) {
                for(int i:order)if(customers[i].group==g&&!customers[i].freeSample){sample(i);picked++;break;}
                g=(g+1)%3;
            }
        }
        eventRng=new java.util.Random(4000000L+rep);
        history.add(snapshot(0));
    }

    private void sample(int i){Customer a=customers[i];a.freeSample=true;a.aware=true;a.awarePeriod=0;a.belief=a.experience;}

    public void interaction(double[] u) {
        int n=config.N,i=(int)(u[0]*n);if(degree[i]==0)return;
        int rank=(int)(u[1]*degree[i]),j=-1;
        for(int z=0;z<n;z++)if(adj[i][z]&&rank--==0){j=z;break;}
        if(j<0)throw new IllegalStateException("Neighbor rank mismatch");
        Customer a=customers[i],b=customers[j];
        if(!a.aware&&!b.aware)return;
        if(a.aware!=b.aware) {
            if(u[2]>=config.shareProb)return;
            Customer other=a.aware?b:a;other.aware=true;other.awarePeriod=period;
        }
        double xi=a.belief,xj=b.belief;
        if(Math.abs(xi-xj)<config.d){a.belief=xi+config.mu*(xj-xi);b.belief=xj+config.mu*(xi-xj);}
        else if(u[3]<config.phi) {
            int[] candidates=new int[n];int count=0;
            if(u[4]<config.h)for(int k=0;k<n;k++)if(k!=i&&!adj[i][k]&&Math.abs(customers[k].belief-xi)<config.d)candidates[count++]=k;
            if(count==0)for(int k=0;k<n;k++)if(k!=i&&!adj[i][k])candidates[count++]=k;
            if(count>0) {
                int k=candidates[(int)(u[5]*count)];
                adj[i][j]=adj[j][i]=false;adj[i][k]=adj[k][i]=true;
                degree[j]--;degree[k]++;rewires++;
            }
        }
    }

    public boolean stepPeriod() {
        if(period>=config.periods)return false;
        period++;
        for(int z=0;z<config.N;z++) {
            double[] u=new double[6];for(int q=0;q<6;q++)u[q]=eventRng.nextDouble();
            interaction(u);
        }
        int[] buyers=new int[config.N];int count=0;
        for(int i=0;i<config.N;i++) {
            Customer a=customers[i];double value=a.valueScale*a.belief;
            if(a.aware&&!a.freeSample&&a.paidPeriod<0&&a.budget>=config.price&&value>=config.price) {
                a.paidPeriod=period;a.valueAtPurchase=value;buyers[count++]=i;
            }
        }
        for(int z=0;z<count;z++)customers[buyers[z]].belief=customers[buyers[z]].experience;
        double[] row=snapshot(count);history.add(row);check(row);
        return period<config.periods;
    }

    public double[] snapshot(int newPaid) {
        int n=config.N,pa=0,aw=0,fr=0,edges=0,cross=0,isolates=0,giant=0;
        int[] pg=new int[3],ag=new int[3],eligible=new int[3];double mean=0,var=0;
        for(int i=0;i<n;i++) {
            Customer a=customers[i];boolean paid=a.paidPeriod>=0;
            pa+=paid?1:0;aw+=a.aware?1:0;fr+=a.freeSample?1:0;
            pg[a.group]+=paid?1:0;ag[a.group]+=a.aware?1:0;eligible[a.group]+=a.freeSample?0:1;
            mean+=a.belief;isolates+=degree[i]==0?1:0;
            for(int j=i+1;j<n;j++)if(adj[i][j]){edges++;cross+=a.group!=customers[j].group?1:0;}
        }
        mean/=n;for(Customer a:customers)var+=(a.belief-mean)*(a.belief-mean);var/=n;
        boolean[] seen=new boolean[n];int[] queue=new int[n];
        for(int root=0;root<n;root++)if(!seen[root]) {
            int front=0,end=0;queue[end++]=root;seen[root]=true;
            while(front<end){int u=queue[front++];for(int j=0;j<n;j++)if(adj[u][j]&&!seen[j]){seen[j]=true;queue[end++]=j;}}
            giant=Math.max(giant,end);
        }
        double minRate=1;boolean found=false;
        for(int g=0;g<3;g++)if(eligible[g]>0){found=true;minRate=Math.min(minRate,(double)pg[g]/eligible[g]);}
        return new double[]{period,aw,pa,fr,newPaid,config.price*pa,config.unitCost*(pa+fr),
            (config.price-config.unitCost)*pa-config.unitCost*fr,n>fr?(double)pa/(n-fr):0,
            found?minRate:0,(double)giant/n,edges>0?(double)cross/edges:0,rewires,mean,var,
            pg[0],pg[1],pg[2],ag[0],ag[1],ag[2],isolates,edges};
    }

    public void check(double[] row) {
        if(row[22]!=config.N*config.k0/2||row[3]!=config.nSamples||row[2]+row[3]>config.N||row[2]+row[3]>row[1])
            throw new IllegalStateException("Graph, sample or owner-count invariant failed");
        for(Customer a:customers) {
            if(!Double.isFinite(a.belief)||a.belief<0||a.belief>1)throw new IllegalStateException("Belief range failed");
            if(a.paidPeriod>=0&&(!a.aware||a.freeSample||a.budget<config.price||a.valueAtPurchase<config.price||a.awarePeriod>a.paidPeriod))
                throw new IllegalStateException("Purchase eligibility failed");
        }
    }

    public static String numbers(double[] row){java.util.ArrayList<String> a=new java.util.ArrayList<>();for(double v:row)a.add(Double.toString(v));return String.join(",",a);}
    public String summaryCsv(String cohort,String scenario) {
        Config c=config;java.util.ArrayList<String> a=new java.util.ArrayList<>();
        String[] meta={cohort,scenario,""+rep,""+(1000000L+rep),""+(2000000L+rep),""+(3000000L+rep),""+(4000000L+rep),STRATEGIES[strategy],
            ""+c.N,""+c.k0,""+c.groups,""+c.withinWeight,""+c.periods,""+c.nSamples,""+c.price,""+c.unitCost,""+c.d,""+c.mu,""+c.phi,""+c.h,""+c.shareProb,""+c.quality,""+c.experienceSD};
        java.util.Collections.addAll(a,meta);double[] last=history.get(history.size()-1);
        for(int i=1;i<last.length;i++)a.add(Double.toString(last[i]));
        int target=-1;double threshold=.2*(c.N-c.nSamples);
        for(double[] row:history)if(row[2]>=threshold){target=(int)row[0];break;}
        a.add(""+target);a.add(target>=0?"1":"0");a.add(""+(target>=0?target:c.periods));a.add(""+((System.nanoTime()-started)/1e9));
        return String.join(",",a);
    }
}
