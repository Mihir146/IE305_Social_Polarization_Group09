"""Validation against Kozma & Barrat (2008): ER graph, mean degree 10, mu=0.5, uniform opinions.
Published: static network, largest opinion cluster drops from ~N to ~N/2 near d1~0.256; fragmented phase below d2~1/(2k)=0.05.
KB's w (prob. of attempting rewiring) maps to our phi = w/(1-w)  (our phi=1 <-> w=0.5)."""
import sys; sys.path.insert(0, "/home/claude/sim")
import numpy as np
from model import run
N, K0, MU, REPS = 500, 10, 0.5, 8
run(N, K0, 0.3, MU, 0.0, 0.0, 1, 5, 0, 5)
def opinion_clusters(x, gap=0.02):
    s = np.sort(x); cuts = np.where(np.diff(s) > gap)[0]
    sizes = np.diff(np.concatenate(([-1], cuts, [len(s)-1])))
    return len(sizes), sizes.max()/len(s), int((sizes >= 0.05*len(s)).sum())
print("N=%d k=%d mu=%.1f reps=%d   (columns: all clusters | largest cluster frac | major clusters(>=5%%) | censored)" % (N, K0, MU, REPS))
for phi, label in [(0.0, "static (w=0)"), (1.0, "adaptive phi=1 (w=0.5), random reconnect h=0")]:
    print(label)
    for d in [0.03, 0.05, 0.08, 0.15, 0.2, 0.23, 0.25, 0.27, 0.30, 0.35]:
        rows = []; cn = 0
        for s in range(REPS):
            x, adj, sw, cens, e0, e1 = run(N, K0, d, MU, phi, 0.0, 900+s, 3000, 0, 10)
            assert e0 == e1; cn += cens
            rows.append(opinion_clusters(x))
        a = np.array(rows, float)
        print(f"  d={d:.2f}: clusters={a[:,0].mean():6.1f}  largest={a[:,1].mean():.2f}  major={a[:,2].mean():.1f}  censored={cn}/{REPS}")
