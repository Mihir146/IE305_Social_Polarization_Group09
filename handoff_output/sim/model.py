"""Reference implementation of the adaptive bounded-confidence model (spec in blueprint section 3).

Used as (a) a verification oracle for the AnyLogic model and (b) a fast engine for the full experiment grid.
"""
import numpy as np
try:
    from numba import njit
except ImportError:
    # The readable reference remains executable without optional acceleration.
    def njit(*args, **kwargs):
        def identity(fn):
            return fn
        return identity


@njit(cache=True)
def _init_graph(n, k0, adj, deg):
    """Random graph with exactly n*k0/2 edges (Erdos-Renyi G(n,m))."""
    m = n * k0 // 2
    added = 0
    while added < m:
        a = np.random.randint(n)
        b = np.random.randint(n)
        if a != b and not adj[a, b]:
            adj[a, b] = True
            adj[b, a] = True
            deg[a] += 1
            deg[b] += 1
            added += 1


@njit(cache=True)
def _pick_partner(i, x, adj, n, d, h):
    """Choose a new contact for i. With prob h among similar non-neighbours, else uniform non-neighbour."""
    similar = np.random.random() < h
    cnt = 0
    if similar:
        for k in range(n):
            if k != i and not adj[i, k] and abs(x[k] - x[i]) < d:
                cnt += 1
    if cnt == 0:
        for k in range(n):
            if k != i and not adj[i, k]:
                cnt += 1
        similar = False
    if cnt == 0:
        return -1
    r = np.random.randint(cnt)
    for k in range(n):
        if k != i and not adj[i, k]:
            if (not similar) or abs(x[k] - x[i]) < d:
                if r == 0:
                    return k
                r -= 1
    return -1


@njit(cache=True)
def _frozen(x, adj, n, d, phi, eps):
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                dd = abs(x[i] - x[j])
                if dd < d:
                    if dd > eps:
                        return False
                elif phi > 0.0:
                    return False
    return True


@njit(cache=True)
def run(n, k0, d, mu, phi, h, seed, max_sweeps, init_mode, check_every,
        allow_isolates=False):
    """Returns (x, adj, sweeps, censored, edge_count_start, edge_count_end)."""
    np.random.seed(seed)
    adj = np.zeros((n, n), dtype=np.bool_)
    deg = np.zeros(n, dtype=np.int64)
    _init_graph(n, k0, adj, deg)
    x = np.empty(n)
    for i in range(n):
        if init_mode == 0:      # Uniform(0,1)
            x[i] = np.random.random()
        elif init_mode == 1:    # centred: Beta(2,2) via two uniforms (mean of 2 uniforms approximates; use exact Beta below)
            u = np.random.random()
            v = np.random.random()
            w = np.random.random()
            # median of three uniforms ~ Beta(2,2)
            x[i] = max(min(u, v), min(max(u, v), w))
        else:                   # bimodal: 50% around 0.25, 50% around 0.75, sd 0.08 (clipped)
            c = 0.25 if np.random.random() < 0.5 else 0.75
            x[i] = min(1.0, max(0.0, c + 0.08 * np.random.randn()))
    e0 = 0
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                e0 += 1
    eps = 1e-3
    total_steps = max_sweeps * n
    step = 0
    censored = True
    while step < total_steps:
        i = np.random.randint(n)
        # random neighbour via reservoir over adjacency row
        cnt = 0
        for k in range(n):
            if adj[i, k]:
                cnt += 1
        if cnt == 0:
            pass  # isolated agent: nothing to do (cuts that would create isolates are forbidden below)
        else:
            r = np.random.randint(cnt)
            j = -1
            for k in range(n):
                if adj[i, k]:
                    if r == 0:
                        j = k
                        break
                    r -= 1
            dd = abs(x[i] - x[j])
            if dd < d:
                xi = x[i]
                xj = x[j]
                x[i] = xi + mu * (xj - xi)
                x[j] = xj + mu * (xi - xj)
            elif np.random.random() < phi:
                # forbid cuts that would strand j (keeps edge count constant and creates no isolates)
                dj = 0
                for q in range(n):
                    if adj[j, q]:
                        dj += 1
                k = _pick_partner(i, x, adj, n, d, h) if (allow_isolates or dj > 1) else -1
                if k >= 0:
                    adj[i, j] = False
                    adj[j, i] = False
                    adj[i, k] = True
                    adj[k, i] = True
        step += 1
        if step % (check_every * n) == 0:
            if _frozen(x, adj, n, d, phi, eps):
                censored = False
                break
    e1 = 0
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                e1 += 1
    return x, adj, step // n, censored, e0, e1


@njit(cache=True)
def kpis(x, adj, n, gap, min_frac):
    """Network + opinion KPIs.

    Returns: n_components, giant_frac, isolated_frac, K (major opinion clusters),
             cross_edge_frac, modularity_Q, opinion_var
    """
    # connected components (iterative DFS)
    comp = -np.ones(n, dtype=np.int64)
    ncomp = 0
    sizes = np.zeros(n, dtype=np.int64)
    stack = np.empty(n, dtype=np.int64)
    for s in range(n):
        if comp[s] == -1:
            sp = 0
            stack[sp] = s
            sp += 1
            comp[s] = ncomp
            while sp > 0:
                sp -= 1
                u = stack[sp]
                sizes[ncomp] += 1
                for v in range(n):
                    if adj[u, v] and comp[v] == -1:
                        comp[v] = ncomp
                        stack[sp] = v
                        sp += 1
            ncomp += 1
    giant = 0
    iso = 0
    for c in range(ncomp):
        if sizes[c] > giant:
            giant = sizes[c]
        if sizes[c] == 1:
            iso += 1
    # opinion clusters by gaps in sorted opinions
    order = np.argsort(x)
    lab = np.zeros(n, dtype=np.int64)
    c = 0
    lab[order[0]] = 0
    for t in range(1, n):
        if x[order[t]] - x[order[t - 1]] > gap:
            c += 1
        lab[order[t]] = c
    nclu = c + 1
    csize = np.zeros(nclu, dtype=np.int64)
    for i in range(n):
        csize[lab[i]] += 1
    K = 0
    for q in range(nclu):
        if csize[q] >= min_frac * n:
            K += 1
    # edges, cross-cluster fraction, modularity of the opinion-cluster partition
    m = 0
    cross = 0
    deg = np.zeros(n, dtype=np.int64)
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i, j]:
                m += 1
                deg[i] += 1
                deg[j] += 1
                if lab[i] != lab[j]:
                    cross += 1
    cross_frac = cross / m if m > 0 else 0.0
    Q = 0.0
    if m > 0:
        inside = np.zeros(nclu)
        dsum = np.zeros(nclu)
        for i in range(n):
            dsum[lab[i]] += deg[i]
        for i in range(n):
            for j in range(i + 1, n):
                if adj[i, j] and lab[i] == lab[j]:
                    inside[lab[i]] += 1
        for q in range(nclu):
            Q += inside[q] / m - (dsum[q] / (2.0 * m)) ** 2
    mean = 0.0
    for i in range(n):
        mean += x[i]
    mean /= n
    var = 0.0
    for i in range(n):
        var += (x[i] - mean) ** 2
    var /= n
    return ncomp, giant / n, iso / n, K, cross_frac, Q, var
