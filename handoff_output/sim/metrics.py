"""NumPy-only metrics, including Kozma--Barrat communication-path clusters."""
import numpy as np

def component_sizes(adj):
    n=len(adj); seen=np.zeros(n,dtype=bool); sizes=[]
    for s in range(n):
        if seen[s]: continue
        stack=[s]; seen[s]=True; size=0
        while stack:
            u=stack.pop();size+=1
            v=np.flatnonzero(adj[u] & ~seen)
            seen[v]=True;stack.extend(v.tolist())
        sizes.append(size)
    return np.array(sorted(sizes,reverse=True))

def opinion_labels(x,gap=.05):
    order=np.argsort(x); labels=np.empty(len(x),dtype=int)
    labels[order]=np.r_[0,np.cumsum(np.diff(x[order])>gap)]
    return labels

def measures(x,adj,d=.2,gap=.05,min_frac=.05,paths=False):
    n=len(x);sizes=component_sizes(adj);lab=opinion_labels(x,gap)
    cs=np.bincount(lab);u,v=np.nonzero(np.triu(adj,1));m=len(u)
    degree=adj.sum(axis=1);within=lab[u]==lab[v]
    internal=np.bincount(lab[u[within]],minlength=len(cs))
    dsum=np.bincount(lab,weights=degree,minlength=len(cs))
    result=dict(n_components=len(sizes),giant_frac=sizes[0]/n,
                isolated_frac=float(np.count_nonzero(sizes==1)/n),
                K=int(np.count_nonzero(cs>=min_frac*n)),
                cross_frac=float(1-within.mean()) if m else 0.,
                Q=float(np.sum(internal/m-(dsum/(2*m))**2)) if m else 0.,
                opinion_var=float(np.var(x)),opinion_range=float(np.ptp(x)))
    if paths:
        compatible=adj & (np.abs(x[:,None]-x[None,:])<d)
        ps=component_sizes(compatible)
        result.update(path_clusters=len(ps),path_largest=ps[0]/n,
                      path_second=ps[1]/n if len(ps)>1 else 0)
    return result

def stopping_diagnostics(x,adj,d,eps=1e-3):
    u,v=np.nonzero(np.triu(adj,1));dd=np.abs(x[u]-x[v]);deg=adj.sum(axis=1)
    bad=dd>=d
    eligible=((deg[v]>1)&(deg[u]<len(x)-1))|((deg[u]>1)&(deg[v]<len(x)-1))
    distances=np.abs(x[:,None]-x[None,:]);np.fill_diagonal(distances,np.inf)
    unmatched=np.all(distances>=d,axis=1)
    return dict(discordant_edges=int(bad.sum()),
                rewirable_discordant_edges=int(np.count_nonzero(bad&eligible)),
                blocked_discordant_edges=int(np.count_nonzero(bad&~eligible)),
                unsettled_compatible_edges=int(np.count_nonzero((dd<d)&(dd>eps))),
                unmatchable_agents=int(unmatched.sum()),
                discordant_with_unmatchable_endpoint=int(np.count_nonzero(bad&(unmatched[u]|unmatched[v]))))

def regime(K,S,cutoff=.9):
    if K==0: return 'No major opinion cluster'
    if S>=cutoff:
        return 'One major cluster, large component' if K==1 else 'Multiple major clusters, large component'
    return 'One major cluster, fragmented' if K==1 else 'Multiple major clusters, fragmented'

def wilson(k,n):
    if n==0:return float('nan'),float('nan')
    z=1.959963984540054;p=k/n;den=1+z*z/n
    c=(p+z*z/(2*n))/den
    h=z*np.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return max(0,c-h),min(1,c+h)
