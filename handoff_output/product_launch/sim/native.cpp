// The opinion project's exact NumPy MT19937 implementation is reused unchanged.
#include "../../sim/native.cpp"

extern "C" int product_evolve(int n, uint8_t* adj, double* x,
    const int32_t* group, const double* value, const double* budget, const double* experience,
    const uint8_t* samples, uint8_t* aware, int32_t* paid_period, int32_t* aware_period,
    double* value_at_purchase, const uint32_t* rngstate, int rngpos,
    int periods, int attempts, double price, double cost, double d, double mu,
    double phi, double h, double share_prob, double* daily) {
    RandomState rng(rngstate,rngpos);
    std::vector<std::vector<int>> nbr(n);
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(adj[i*n+j]) nbr[i].push_back(j);
    int rewires=0;
    auto record=[&](int period,int newpaid){
        double* out=daily+period*23;
        int pa=0,aw=0,fr=0,pg[3]={0,0,0},ag[3]={0,0,0},eligible[3]={0,0,0};
        double mean=0,var=0;
        int edges=0,cross=0,isolates=0,giant=0;
        for(int i=0;i<n;i++){
            bool paid=paid_period[i]>=0;pa+=paid;aw+=aware[i];fr+=samples[i];
            pg[group[i]]+=paid;ag[group[i]]+=aware[i];eligible[group[i]]+=!samples[i];
            mean+=x[i];isolates+=nbr[i].empty();
            for(int j:nbr[i]) if(i<j){edges++;cross+=group[i]!=group[j];}
        }
        mean/=n;for(int i=0;i<n;i++) var+=(x[i]-mean)*(x[i]-mean);var/=n;
        std::vector<uint8_t> seen(n,0);std::vector<int> queue;
        for(int root=0;root<n;root++) if(!seen[root]){
            queue.clear();queue.push_back(root);seen[root]=1;
            for(size_t z=0;z<queue.size();z++) for(int j:nbr[queue[z]]) if(!seen[j]){seen[j]=1;queue.push_back(j);}
            giant=std::max(giant,(int)queue.size());
        }
        double minrate=1;bool found=false;
        for(int g=0;g<3;g++) if(eligible[g]){found=true;minrate=std::min(minrate,(double)pg[g]/eligible[g]);}
        double vals[23]={(double)period,(double)aw,(double)pa,(double)fr,(double)newpaid,
            price*pa,cost*(pa+fr),(price-cost)*pa-cost*fr,n>fr?(double)pa/(n-fr):0,
            found?minrate:0,(double)giant/n,edges?(double)cross/edges:0,(double)rewires,mean,var,
            (double)pg[0],(double)pg[1],(double)pg[2],(double)ag[0],(double)ag[1],(double)ag[2],
            (double)isolates,(double)edges};
        std::copy(vals,vals+23,out);
    };
    record(0,0);std::vector<int> candidates;
    for(int period=1;period<=periods;period++){
        for(int step=0;step<attempts;step++){
            // Always consume six draws, including skipped interactions.
            double u[6];for(int q=0;q<6;q++)u[q]=rng.uniform();
            int i=(int)(u[0]*n);if(nbr[i].empty())continue;
            int j=nbr[i][(int)(u[1]*nbr[i].size())];
            if(!aware[i]&&!aware[j])continue;
            if(aware[i]!=aware[j]){
                if(u[2]>=share_prob)continue;
                int k=aware[i]?j:i;aware[k]=1;aware_period[k]=period;
            }
            double xi=x[i],xj=x[j];
            if(std::abs(xi-xj)<d){x[i]=xi+mu*(xj-xi);x[j]=xj+mu*(xi-xj);}
            else if(u[3]<phi){
                candidates.clear();bool similar=u[4]<h;
                if(similar)for(int k=0;k<n;k++)if(k!=i&&!adj[i*n+k]&&std::abs(x[k]-xi)<d)candidates.push_back(k);
                if(candidates.empty())for(int k=0;k<n;k++)if(k!=i&&!adj[i*n+k])candidates.push_back(k);
                if(!candidates.empty()){
                    int k=candidates[(int)(u[5]*candidates.size())];
                    adj[i*n+j]=adj[j*n+i]=0;adj[i*n+k]=adj[k*n+i]=1;
                    auto remove=[&](int a,int b){auto&v=nbr[a];v.erase(std::lower_bound(v.begin(),v.end(),b));};
                    auto add=[&](int a,int b){auto&v=nbr[a];v.insert(std::lower_bound(v.begin(),v.end(),b),b);};
                    remove(i,j);remove(j,i);add(i,k);add(k,i);rewires++;
                }
            }
        }
        // Identify every purchase from the same end-of-period belief profile.
        std::vector<int> buyers;
        for(int i=0;i<n;i++)if(aware[i]&&!samples[i]&&paid_period[i]<0&&budget[i]>=price&&value[i]*x[i]>=price){
            buyers.push_back(i);paid_period[i]=period;value_at_purchase[i]=value[i]*x[i];
        }
        for(int i:buyers)x[i]=experience[i];
        record(period,(int)buyers.size());
    }
    return 0;
}
