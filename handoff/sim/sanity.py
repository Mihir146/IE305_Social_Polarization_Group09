import time, sys
sys.path.insert(0, "/home/claude/sim")
import numpy as np
from model import run, kpis

N, K0, MU = 300, 8, 0.3

# compile
run(N, K0, 0.3, MU, 0.25, 1.0, 1, 5, 0, 5)
kpis(np.random.rand(N), np.zeros((N, N), dtype=np.bool_), N, 0.05, 0.05)

print("--- timing + one run ---")
t = time.time()
x, adj, sw, cens, e0, e1 = run(N, K0, 0.3, MU, 0.25, 1.0, 7, 5000, 0, 10)
print("sweeps", sw, "censored", cens, "edges", e0, e1, "secs", round(time.time() - t, 2))
print("kpis", kpis(x, adj, N, 0.05, 0.05))

print("--- phi=0 (static): major opinion clusters vs d, 10 reps ---")
for d in [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5]:
    Ks, cens_n, Ss = [], 0, []
    for s in range(10):
        x, adj, sw, cens, e0, e1 = run(N, K0, d, MU, 0.0, 1.0, 100 + s, 5000, 0, 10)
        assert e0 == e1
        r = kpis(x, adj, N, 0.05, 0.05)
        Ks.append(r[3]); Ss.append(r[1]); cens_n += cens
    print(f"d={d}: mean K={np.mean(Ks):.2f}  mean S={np.mean(Ss):.2f}  censored={cens_n}/10")

print("--- adaptive h=1, d=0.3: vary phi, 10 reps ---")
for phi in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
    rows = []
    cn = 0
    t = time.time()
    for s in range(10):
        x, adj, sw, cens, e0, e1 = run(N, K0, 0.3, MU, phi, 1.0, 200 + s, 5000, 0, 10)
        assert e0 == e1
        cn += cens
        rows.append(kpis(x, adj, N, 0.05, 0.05) + (sw,))
    a = np.array(rows)
    print(f"phi={phi}: K={a[:,3].mean():.2f} S={a[:,1].mean():.2f} comps={a[:,0].mean():.1f} cross={a[:,4].mean():.3f} Q={a[:,5].mean():.2f} sweeps={a[:,7].mean():.0f} cens={cn}/10  ({time.time()-t:.1f}s)")
