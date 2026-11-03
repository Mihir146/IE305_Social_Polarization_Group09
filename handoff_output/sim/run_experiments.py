from pathlib import Path
ROOT = Path(__file__).resolve().parent
"""Run all experiments (A: tolerance x rewiring, B: selection h, C: sensitivity, D: mean degree). Writes results.csv"""
import sys, itertools, time, csv
sys.path.insert(0, str(Path(__file__).resolve().parent))
from concurrent.futures import ThreadPoolExecutor
import importlib.util
import numpy as np

REPS = 30
CAP = 3000
BASE = dict(N=300, k0=8, d=0.2, mu=0.3, phi=0.25, h=1.0, init=0)

def tasks():
    T = []
    # A: d x phi (h=1)
    for d in [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]:
        for phi in [0, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]:
            for r in range(REPS):
                T.append(("A", dict(BASE, d=d, phi=phi), r))
    # B: selection h x phi at two d values
    for d in [0.15, 0.25]:
        for h in [0.0, 0.5, 1.0]:
            for phi in [0.05, 0.25, 1.0]:
                for r in range(REPS):
                    T.append(("B", dict(BASE, d=d, h=h, phi=phi), r))
    # C: one-at-a-time sensitivity around baseline (d=0.2, phi=0.25, h=1)
    for key, vals in [("N", [100, 600]), ("mu", [0.1, 0.5]), ("init", [1, 2])]:
        for v in vals:
            for r in range(REPS):
                T.append(("C", dict(BASE, **{key: v}), r))
    # D: mean degree x low phi at d=0.2
    for k0 in [4, 8, 16]:
        for phi in [0, 0.005, 0.01, 0.02, 0.05, 0.1, 0.25]:
            for r in range(REPS):
                T.append(("D", dict(BASE, k0=k0, phi=phi), r))
    return T

def work(t):
    if importlib.util.find_spec('numba') is not None:
        from model import run, kpis
    else:
        from accelerated import run
        from metrics import measures
    exp, p, r = t
    seed = 1000 + r          # same rep index -> same initial population across scenarios (common random numbers)
    t0 = time.time()
    x, adj, sw, cens, e0, e1 = run(p["N"], p["k0"], p["d"], p["mu"], p["phi"], p["h"], seed, CAP, p["init"], 10)
    if importlib.util.find_spec('numba') is not None:
        nc, S, iso, K, cross, Q, var = kpis(x, adj, p["N"], 0.05, 0.05)
    else:
        m = measures(x, adj, p['d'])
        nc,S,iso,K,cross,Q,var = [m[k] for k in ['n_components','giant_frac','isolated_frac','K','cross_frac','Q','opinion_var']]
    return dict(exp=exp, rep=r, seed=seed, **p, sweeps=sw, censored=int(cens), edges_start=e0, edges_end=e1,
                n_components=nc, giant_frac=S, isolated_frac=iso, K=K, cross_frac=cross, Q=Q, opinion_var=var,
                secs=round(time.time() - t0, 3))

if __name__ == "__main__":
    T = tasks()
    print(len(T), "runs", flush=True)
    t0 = time.time()
    if importlib.util.find_spec('numba') is None:
        from accelerated import library
        library()
    with ThreadPoolExecutor(max_workers=2) as pool, open(str(ROOT / "results.csv"), "w", newline="") as f:
        w = None
        for i, row in enumerate(pool.map(work, T)):
            if w is None:
                w = csv.DictWriter(f, fieldnames=list(row.keys())); w.writeheader()
            w.writerow(row)
            if i % 200 == 0:
                print(i, round(time.time() - t0), "s", flush=True)
    print("done", round(time.time() - t0), "s", flush=True)
