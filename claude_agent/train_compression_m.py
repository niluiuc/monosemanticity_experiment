"""Adam-trained check of the general-m shared-budget threshold p_c(eta=.5, m):
m=2: 0.4226, m=3: 0.4417, m=4: 0.4531. n = 2m, importances (1..1, .5..5), Frobenius budget m.
Usage: python train_compression_m.py <m> <p-list> <seeds>"""
import json, sys, os, time
import numpy as np


def train(n, m, eta, p, seed, steps=8000, batch=4096, lr=3e-3):
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(m, n)) * 0.5; W *= np.sqrt(m) / np.linalg.norm(W); b = np.zeros(n)
    mo = np.zeros(m * n + n); vo = np.zeros(m * n + n)
    for t in range(1, steps + 1):
        X = (rng.random((batch, n)) < p).astype(float)
        H = X @ W.T; U = H @ W + b; Y = np.maximum(U, 0)
        G = 2 * eta * (Y - X) * (U > 0) / batch
        gW = H.T @ G + (G @ W.T).T @ X
        gW = gW - W * (W * gW).sum() / (W * W).sum()
        g = np.concatenate([gW.ravel(), G.sum(0)])
        lr_t = lr * (0.1 if t > 0.75 * steps else 1)
        mo = 0.9 * mo + 0.1 * g; vo = 0.999 * vo + 0.001 * g * g
        st = lr_t * (mo / (1 - 0.9 ** t)) / (np.sqrt(vo / (1 - 0.999 ** t)) + 1e-12)
        W = W - st[:m * n].reshape(m, n); b = b - st[m * n:]; W *= np.sqrt(m) / np.linalg.norm(W)
    return W


if __name__ == "__main__":
    m = int(sys.argv[1]); n = 2 * m; ps = [float(x) for x in sys.argv[2].split(",")]; seeds = [int(x) for x in sys.argv[3].split(",")]
    eta = np.array([1.0] * m + [0.5] * m)
    fn = f"results/compression/trained_adam_m{m}.json"; rows = json.load(open(fn)) if os.path.exists(fn) else []
    for p in ps:
        for s in seeds:
            if any(r["p"] == p and r["seed"] == s for r in rows): continue
            t0 = time.time(); W = train(n, m, eta, p, s); nr = np.linalg.norm(W, axis=0)
            rows.append(dict(m=m, p=p, seed=s, col_norms=nr.tolist(), n_partners=int((nr[m:] > 0.01).sum()), max_partner=float(nr[m:].max())))
            json.dump(rows, open(fn, "w"), indent=1)
            print(m, p, s, "partners", rows[-1]["n_partners"], "max partner norm %.3f" % rows[-1]["max_partner"], round(time.time() - t0, 1), flush=True)
