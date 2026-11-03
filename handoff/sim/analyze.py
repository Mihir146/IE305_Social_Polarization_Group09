import sys
sys.path.insert(0, "/home/claude/sim")
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("/home/claude/sim/results.csv")
assert (df.edges_start == df.edges_end).all(), "edge conservation violated"
print("runs:", len(df), "| edge conservation OK | censored share:", round(df.censored.mean(), 3))

df["connected"] = df.giant_frac >= 0.9
df["multi"] = df.K >= 2
def regime(r):
    if r.connected and not r.multi: return "Consensus"
    if r.connected and r.multi: return "Polarized, connected"
    if (not r.connected) and not r.multi: return "Fragmented, one opinion"
    return "Polarized + fragmented (echo chambers)"
df["regime"] = df.apply(regime, axis=1)
df.to_csv("/home/claude/sim/results_with_regimes.csv", index=False)

def ci(x):
    x = np.asarray(x, float); n = len(x)
    m = x.mean(); h = stats.t.ppf(0.975, n-1) * x.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    return m, h
def wilson(k, n, z=1.96):
    p = k/n; den = 1+z*z/n
    c = (p + z*z/(2*n))/den; hw = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return c-hw, c+hw

plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
C = dict(blue="#2a6f97", red="#c1121f", grey="#6c757d", green="#2d6a4f", orange="#e07a1f")

# ---- Fig 1: Exp A heatmaps (d x phi), h=1 ----
A = df[df.exp == "A"]
ds = sorted(A.d.unique()); ps = sorted(A.phi.unique())
def grid(col, fn):
    return np.array([[fn(A[(A.d == d) & (A.phi == p)][col]) for p in ps] for d in ds])
fig, ax = plt.subplots(1, 3, figsize=(15, 4.2))
for a, (title, M, cmap, vmin, vmax) in zip(ax, [
    ("Opinion clusters K (mean)", grid("K", np.mean), "viridis", 1, 5),
    ("Giant-component fraction S (mean)", grid("giant_frac", np.mean), "viridis", 0, 1),
    ("Share of runs hitting time cap", grid("censored", np.mean), "magma", 0, 1)]):
    im = a.imshow(M, origin="lower", aspect="auto", cmap=cmap, vmin=vmin, vmax=vmax)
    a.set_xticks(range(len(ps))); a.set_xticklabels(ps, rotation=45); a.set_yticks(range(len(ds))); a.set_yticklabels(ds)
    a.set_xlabel("rewiring probability φ"); a.set_ylabel("tolerance d"); a.set_title(title)
    for i in range(len(ds)):
        for j in range(len(ps)):
            a.text(j, i, f"{M[i,j]:.2f}" if vmax <= 1 else f"{M[i,j]:.1f}", ha="center", va="center", color="w", fontsize=7)
    plt.colorbar(im, ax=a, fraction=0.046)
fig.suptitle("Experiment A (h=1, N=300, k0=8, 30 reps/cell): opinion clustering is set by d; network fragmentation appears once φ>0", y=1.02)
fig.tight_layout(); fig.savefig("/home/claude/sim/fig1_expA_heatmaps.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ---- Fig 2: regime probabilities vs phi at d=0.2 and d=0.15 ----
order = ["Consensus", "Polarized, connected", "Fragmented, one opinion", "Polarized + fragmented (echo chambers)"]
cols = [C["green"], C["orange"], C["grey"], C["red"]]
fig, ax = plt.subplots(1, 3, figsize=(15, 3.8), sharey=True)
for a, d in zip(ax, [0.1, 0.2, 0.3]):
    sub = A[A.d == d]
    bottom = np.zeros(len(ps))
    for rg, c in zip(order, cols):
        v = np.array([(sub[sub.phi == p].apply(regime, axis=1) == rg).mean() for p in ps])
        a.bar(range(len(ps)), v, bottom=bottom, color=c, label=rg); bottom += v
    a.set_xticks(range(len(ps))); a.set_xticklabels(ps, rotation=45); a.set_xlabel("rewiring probability φ"); a.set_title(f"tolerance d = {d}")
ax[0].set_ylabel("share of 30 replications"); ax[2].legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
fig.tight_layout(); fig.savefig("/home/claude/sim/fig2_regimes.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ---- Fig 3: Exp D: critical rewiring depends on mean degree ----
D = df[df.exp == "D"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4))
for k0, c in zip([4, 8, 16], [C["blue"], C["orange"], C["red"]]):
    sub = D[D.k0 == k0]; ps2 = sorted(sub.phi.unique())
    m = [ci(sub[sub.phi == p].giant_frac) for p in ps2]
    ax[0].errorbar(range(len(ps2)), [x[0] for x in m], yerr=[x[1] for x in m], marker="o", color=c, capsize=3, label=f"k0={k0}")
    ax[1].plot(range(len(ps2)), [sub[sub.phi == p].censored.mean() for p in ps2], marker="s", color=c, label=f"k0={k0}")
for a in ax:
    a.set_xticks(range(len(ps2))); a.set_xticklabels(ps2, rotation=45); a.set_xlabel("rewiring probability φ")
ax[0].set_ylabel("giant-component fraction S (mean, 95% CI)"); ax[0].set_title("Network fragmentation vs φ, by mean degree (d=0.2)"); ax[0].legend()
ax[1].set_ylabel("share of runs hitting time cap"); ax[1].set_title("Slowing down near the transition")
fig.tight_layout(); fig.savefig("/home/claude/sim/fig3_expD_meandegree.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ---- Fig 4: Exp B selection h ----
B = df[df.exp == "B"]
fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for a, d in zip(ax, [0.15, 0.25]):
    sub = B[B.d == d]
    for h, c in zip([0.0, 0.5, 1.0], [C["grey"], C["orange"], C["blue"]]):
        m = [ci(sub[(sub.h == h) & (sub.phi == p)].giant_frac) for p in [0.05, 0.25, 1.0]]
        a.errorbar([0, 1, 2], [x[0] for x in m], yerr=[x[1] for x in m], marker="o", capsize=3, color=c, label=f"h={h}")
    a.set_xticks([0, 1, 2]); a.set_xticklabels([0.05, 0.25, 1.0]); a.set_xlabel("φ"); a.set_title(f"d={d}")
ax[0].set_ylabel("giant-component fraction S"); ax[0].legend(title="selection of new tie")
fig.tight_layout(); fig.savefig("/home/claude/sim/fig4_expB_selection.png", dpi=160, bbox_inches="tight"); plt.close(fig)

# ---- numbers for the write-up ----
out = []
out.append("## Exp A: P(network fragmented, S<0.9) with Wilson 95% CI (rows d, cols phi)")
for d in ds:
    row = []
    for p in ps:
        s = A[(A.d == d) & (A.phi == p)]; k = int((~s.connected).sum()); lo, hi = wilson(k, len(s))
        row.append(f"{k/len(s):.2f}[{lo:.2f},{hi:.2f}]")
    out.append(f"d={d}: " + "  ".join(row))
out.append("\n## Exp A: mean cross-cluster edge fraction (phi=0 vs phi>0) by d")
for d in ds:
    out.append(f"d={d}: phi0={A[(A.d==d)&(A.phi==0)].cross_frac.mean():.3f}  phi>0={A[(A.d==d)&(A.phi>0)].cross_frac.mean():.3f}  Q(phi>0)={A[(A.d==d)&(A.phi>0)].Q.mean():.2f}")
out.append("\n## Exp B: giant_frac mean (h x phi) per d")
for d in [0.15, 0.25]:
    for h in [0.0, 0.5, 1.0]:
        out.append(f"d={d} h={h}: " + "  ".join(f"phi={p}: S={B[(B.d==d)&(B.h==h)&(B.phi==p)].giant_frac.mean():.2f} cens={B[(B.d==d)&(B.h==h)&(B.phi==p)].censored.mean():.2f} sweeps={B[(B.d==d)&(B.h==h)&(B.phi==p)].sweeps.mean():.0f}" for p in [0.05, 0.25, 1.0]))
out.append("\n## Exp C sensitivity (d=0.2, phi=0.25, h=1): baseline row from Exp A d=0.2 phi=0.25")
base = A[(A.d == 0.2) & (A.phi == 0.25)]
out.append(f"baseline: S={base.giant_frac.mean():.2f} K={base.K.mean():.2f} cens={base.censored.mean():.2f}")
Cc = df[df.exp == "C"]
for key in ["N", "mu", "init"]:
    for v in sorted(Cc[key].unique()):
        s = Cc[(Cc[key] == v) & ((Cc.N == 300) | (key == "N"))]
        if key != "N": s = s[s.N == 300]
        if key == "mu": s = s[s.init == 0]
        if key == "init": s = s[s.mu == 0.3]
        if key == "N": s = s[(s.mu == 0.3) & (s.init == 0)]
        if len(s) and ((key == "N" and (s.N == v).all()) or key != "N"):
            s = s[s[key] == v]
            out.append(f"{key}={v}: S={s.giant_frac.mean():.2f} K={s.K.mean():.2f} cens={s.censored.mean():.2f} n={len(s)}")
out.append("\n## Exp D: S by k0 x phi (d=0.2)")
for k0 in [4, 8, 16]:
    out.append(f"k0={k0}: " + "  ".join(f"phi={p}: S={D[(D.k0==k0)&(D.phi==p)].giant_frac.mean():.2f}/cens={D[(D.k0==k0)&(D.phi==p)].censored.mean():.2f}" for p in sorted(D.phi.unique())))
out.append("\n## Regime counts overall\n" + df.regime.value_counts().to_string())
open("/home/claude/sim/summary.txt", "w").write("\n".join(out))
print("\n".join(out))
