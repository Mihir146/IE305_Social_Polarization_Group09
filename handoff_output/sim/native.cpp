// Optional acceleration of the supplied model, plus the published KB scheduler.
// RNG state is imported from NumPy RandomState after identical initialization.
#include <algorithm>
#include <cmath>
#include <cstdint>
#include <vector>

struct RandomState {
    uint32_t state[624]; int pos;
    RandomState(const uint32_t* s, int p):pos(p) {
        std::copy(s,s+624,state);
    }
    uint32_t next() {
        if (pos>=624) {
            for(int i=0;i<624;i++) {
                uint32_t y=(state[i]&0x80000000U)|(state[(i+1)%624]&0x7fffffffU);
                state[i]=state[(i+397)%624]^(y>>1)^((y&1U)?0x9908b0dfU:0);
            }
            pos=0;
        }
        uint32_t y=state[pos++];
        y^=y>>11; y^=(y<<7)&0x9d2c5680U; y^=(y<<15)&0xefc60000U; y^=y>>18;
        return y;
    }
    double uniform() {
        uint32_t a=next()>>5, b=next()>>6;
        return (a*67108864.0+b)/9007199254740992.0;
    }
    int integer(int n) {
        // NumPy legacy rk_interval, including its zero-draw n=1 case.
        uint32_t max=n-1, mask=max;
        if(!max) return 0;
        mask|=mask>>1; mask|=mask>>2; mask|=mask>>4;
        mask|=mask>>8; mask|=mask>>16;
        uint32_t v; do {v=next()&mask;} while(v>max);
        return (int)v;
    }
};

extern "C" int evolve(int n, double* x, uint8_t* adj,
                     const uint32_t* rngstate, int rngpos,
                     double d, double mu, double rate, double h,
                     int cap, int check, int isolates, int kb,
                     double eps, double* info) {
    RandomState rng(rngstate,rngpos);
    std::vector<std::vector<int>> nbr(n);
    for(int i=0;i<n;i++) for(int j=0;j<n;j++)
        if(adj[i*n+j]) nbr[i].push_back(j);
    auto frozen=[&]() {
        for(int i=0;i<n;i++) for(int j:nbr[i]) if(i<j) {
            double delta=std::abs(x[i]-x[j]);
            if(delta<d) {if(delta>eps) return false;}
            else if(rate>0) return false;
        }
        return true;
    };
    long long steps=(long long)cap*n, step=0;
    bool censored=true;
    std::vector<int> candidates;
    for(;step<steps;) {
        int i=rng.integer(n);
        if(!nbr[i].empty()) {
            int j=nbr[i][rng.integer((int)nbr[i].size())];
            double delta=std::abs(x[i]-x[j]);
            bool influence=false, rewire=false;
            if(kb) {
                bool attempt=rng.uniform()<=rate;
                influence=!attempt && delta<d;
                rewire=attempt && delta>d;
            } else {
                influence=delta<d;
                if(!influence) rewire=rng.uniform()<rate;
            }
            if(influence) {
                double xi=x[i],xj=x[j];
                x[i]=xi+mu*(xj-xi); x[j]=xj+mu*(xi-xj);
            } else if(rewire && (isolates || nbr[j].size()>1)) {
                bool similar=rng.uniform()<h;
                candidates.clear();
                if(similar) for(int k=0;k<n;k++)
                    if(k!=i && !adj[i*n+k] && std::abs(x[k]-x[i])<d)
                        candidates.push_back(k);
                if(candidates.empty()) for(int k=0;k<n;k++)
                    if(k!=i && !adj[i*n+k]) candidates.push_back(k);
                if(!candidates.empty()) {
                    int k=candidates[rng.integer((int)candidates.size())];
                    adj[i*n+j]=adj[j*n+i]=0;
                    adj[i*n+k]=adj[k*n+i]=1;
                    auto remove=[&](int a,int b){
                        auto& v=nbr[a]; v.erase(std::lower_bound(v.begin(),v.end(),b));
                    };
                    auto add=[&](int a,int b){
                        auto& v=nbr[a]; v.insert(std::lower_bound(v.begin(),v.end(),b),b);
                    };
                    remove(i,j); remove(j,i); add(i,k); add(k,i);
                }
            }
        }
        step++;
        if(step%((long long)check*n)==0 && frozen()) {
            censored=false; break;
        }
    }
    info[0]=(double)(step/n); info[1]=censored;
    return 0;
}

// Vazquez--Eguiluz--San Miguel: node update, binary copy or rewire-to-same.
extern "C" int binary_evolve(int n, int32_t* s, uint8_t* adj,
                            const uint32_t* rngstate, int rngpos,
                            double p, int cap, double* info) {
    RandomState rng(rngstate,rngpos);
    std::vector<std::vector<int>> nbr(n);
    int active=0;
    for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(adj[i*n+j]) {
        nbr[i].push_back(j); if(i<j && s[i]!=s[j]) active++;
    }
    long long step=0,limit=(long long)n*cap;
    while(active>0 && step<limit) {
        int i=rng.integer(n);
        if(!nbr[i].empty()) {
            int j=nbr[i][rng.integer((int)nbr[i].size())];
            if(s[i]!=s[j]) {
                if(rng.uniform()<p) {
                    std::vector<int> candidates;
                    for(int k=0;k<n;k++)
                        if(k!=i && !adj[i*n+k] && s[k]==s[i]) candidates.push_back(k);
                    if(!candidates.empty()) {
                        int k=candidates[rng.integer((int)candidates.size())];
                        adj[i*n+j]=adj[j*n+i]=0;adj[i*n+k]=adj[k*n+i]=1;
                        nbr[i].erase(std::lower_bound(nbr[i].begin(),nbr[i].end(),j));
                        nbr[j].erase(std::lower_bound(nbr[j].begin(),nbr[j].end(),i));
                        nbr[i].insert(std::lower_bound(nbr[i].begin(),nbr[i].end(),k),k);
                        nbr[k].insert(std::lower_bound(nbr[k].begin(),nbr[k].end(),i),i);
                        active--;
                    }
                } else {
                    for(int k:nbr[i]) active+=(s[i]==s[k]?1:-1);
                    s[i]=s[j];
                }
            }
        }
        step++;
    }
    info[0]=(double)step/n;info[1]=active>0;info[2]=active;
    return 0;
}
