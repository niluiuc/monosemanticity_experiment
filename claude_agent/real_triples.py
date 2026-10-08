"""Real triples test (see real_triples_protocol.md).
   python real_triples.py select | run <chunk> <n> | merge <n> | analyse"""
import json, sys, os, time
import numpy as np
from scipy.optimize import minimize
from multiprocessing import Pool
import real_pairs as R

OUT = "results/real_triples" if os.environ.get("REAL_DATASET", "layer4") == "layer4" else "results/real_triples_logits"; os.makedirs(OUT, exist_ok=True)
ETA = np.array([1.0, 0.5, 0.45]); SIG = 0.005
BINS = [(-0.20, -0.05), (-0.05, -0.01), (-0.01, 0.01), (0.01, 0.05), (0.05, 0.15), (0.15, 0.60)]
A = np.concatenate([[0.0], np.logspace(-3, np.log10(np.pi / 2), 39)])
B = np.linspace(-np.pi, np.pi, 49)[:-1]


def dirs(a, b):
    return np.stack([np.cos(a), np.sin(a) * np.cos(b), np.sin(a) * np.sin(b)], -1)


def profiled_loss(W, Xs):
    """W: (D,3) unit directions; Xs: (n,3). Exact Gaussian-smoothed loss, biases profiled (grid+Newton)."""
    h = Xs @ W.T                                     # (n, D)
    tot = np.zeros(W.shape[0])
    for i in range(3):
        wi = W[:, i][:, None]
        m = wi * h.T                                 # (D, n)
        s = np.maximum(np.abs(wi) * SIG, 1e-12)
        x = Xs[:, i][None, :]
        best = np.full(W.shape[0], np.inf); bb = np.zeros(W.shape[0])
        for b in np.linspace(-1.5, 1.5, 31):
            L = R.out_loss_and_derivs(m + b, s, x)[0].mean(1); u = L < best; best[u] = L[u]; bb[u] = b
        for _ in range(10):
            L, d1, d2 = R.out_loss_and_derivs(m + bb[:, None], s, x); g, hh = d1.mean(1), d2.mean(1)
            cand = bb + np.clip(np.where(hh > 1e-8, -g / np.maximum(hh, 1e-8), -0.05 * np.sign(g)), -0.1, 0.1)
            Lc = R.out_loss_and_derivs(m + cand[:, None], s, x)[0].mean(1); bb = np.where(Lc <= L.mean(1), cand, bb)
        tot += ETA[i] * R.out_loss_and_derivs(m + bb[:, None], s, x)[0].mean(1)
    return tot


def solve(Xs):
    aa, bbb = np.meshgrid(A, B, indexing="ij")
    W = dirs(aa.ravel(), bbb.ravel())
    Fv = profiled_loss(W, Xs)
    order = np.argsort(Fv)[:3]
    best = (Fv[order[0]], W[order[0]])
    for k in order:
        a0, b0 = aa.ravel()[k], bbb.ravel()[k]
        r = minimize(lambda z: profiled_loss(dirs(np.array([z[0]]), np.array([z[1]])), Xs)[0], [a0, b0],
                     method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-12, maxiter=300))
        if r.fun < best[0]:
            best = (r.fun, dirs(np.array([r.x[0]]), np.array([r.x[1]]))[0])
    return float(best[0]), best[1].tolist()


def work(t):
    X, zf, el = R.load(); Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
    Xs = Xn[:, [t["i"], t["j"], t["k"]]]
    t0 = time.time(); F, w = solve(Xs)
    return dict(**t, F=F, w=w, secs=time.time() - t0)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "select":
        X, zf, el = R.load(); Xn = X / np.sqrt((X ** 2).mean(0, keepdims=True) + 1e-30)
        C = np.corrcoef(Xn[:, el].T); rng = np.random.default_rng(20261008); n = len(el)
        triples = []
        for lo, hi in BINS:
            got = 0; tries = 0
            while got < 20 and tries < 200000:
                tries += 1
                a_, b_, c_ = rng.choice(n, 3, replace=False)
                if abs(C[a_, b_]) < 0.02 and abs(C[b_, c_]) < 0.05 and lo <= C[a_, c_] < hi:
                    triples.append(dict(i=int(el[a_]), j=int(el[b_]), k=int(el[c_]), c13=float(C[a_, c_]),
                                        c12=float(C[a_, b_]), c23=float(C[b_, c_]), bin=[lo, hi],
                                        pbar=float(1 - zf[[el[a_], el[b_], el[c_]]].mean())))
                    got += 1
            print((lo, hi), got, tries)
        json.dump(triples, open(OUT + "/triples.json", "w"), indent=1)
    elif mode == "run":
        ch, n = int(sys.argv[2]), int(sys.argv[3]); fn = f"{OUT}/part{ch}.json"
        if os.path.exists(fn): raise SystemExit("exists")
        T = json.load(open(OUT + "/triples.json"))[ch::n]; t0 = time.time()
        with Pool(2) as pool: out = pool.map(work, T, chunksize=1)
        json.dump(out, open(fn, "w"), indent=1); print(ch, len(out), round(time.time() - t0, 1))
    elif mode == "merge":
        n = int(sys.argv[2]); rows = []
        for ch in range(n): rows += json.load(open(f"{OUT}/part{ch}.json"))
        json.dump(rows, open(OUT + "/solutions.json", "w"), indent=1); print("merged", len(rows))
    elif mode == "analyse":
        S = json.load(open(OUT + "/solutions.json")); res = {}
        def stored(w, j): return abs(w[j]) / max(abs(x) for x in w) > 0.05
        for lo, hi in BINS:
            rr = [s for s in S if s["bin"] == [lo, hi]]
            res[f"[{lo},{hi})"] = dict(n=len(rr), store2=sum(stored(s["w"], 1) for s in rr), store3=sum(stored(s["w"], 2) for s in rr),
                                       sign3_matches_c13=sum(1 for s in rr if stored(s["w"], 2) and np.sign(s["w"][0] * s["w"][2]) == np.sign(s["c13"])),
                                       dominant_is_1=sum(1 for s in rr if np.argmax(np.abs(s["w"])) == 0))
        strong = [s for s in S if abs(s["c13"]) >= 0.05]
        st3 = [s for s in strong if stored(s["w"], 2)]
        res["T1_sign_rule_|c13|>=0.05"] = [sum(1 for s in st3 if np.sign(s["w"][0] * s["w"][2]) == np.sign(s["c13"])), len(st3)]
        z = [s for s in S if s["bin"] == [-0.01, 0.01]]
        strongbins = [s for s in S if s["bin"] in ([-0.20, -0.05], [0.15, 0.60])]
        res["T2_store2_strong_vs_zero"] = [[sum(stored(s["w"], 1) for s in strongbins), len(strongbins)], [sum(stored(s["w"], 1) for s in z), len(z)]]
        res["T3_store3_strong_vs_zero"] = [[sum(stored(s["w"], 2) for s in strong), len(strong)], [sum(stored(s["w"], 2) for s in z), len(z)]]
        json.dump(res, open(OUT + "/analysis.json", "w"), indent=1)
        for k_, v in res.items(): print(k_, v)
