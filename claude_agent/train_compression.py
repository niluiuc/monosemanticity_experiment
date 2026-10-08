"""Do actually TRAINED networks (minibatch Adam on sampled data, n=4, m=2, Frobenius budget 2,
clean) find the shared-budget phases predicted by Proposition C?
Prediction (eta=.5): mono for p > 0.4226, a single partner (symmetry broken) below it (p ~ 0.3-0.4).
Usage: python train_compression.py <p-list> <seeds>"""
import json, sys, os, time
import numpy as np
ETA = np.array([1, 1, 0.5, 0.5])


def train(p, seed, steps=8000, batch=4096, lr=3e-3):
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(2, 4)) * 0.5; W *= np.sqrt(2) / np.linalg.norm(W); b = np.zeros(4)
    m = np.zeros(12); v = np.zeros(12)
    for t in range(1, steps + 1):
        X = (rng.random((batch, 4)) < p).astype(float)
        H = X @ W.T; U = H @ W + b; Y = np.maximum(U, 0)
        G = 2 * ETA * (Y - X) * (U > 0) / batch                   # dL/dU
        gW = H.T @ G + (G @ W.T).T @ X                            # direct + through H
        gb = G.sum(0)
        gW = gW - W * (W * gW).sum() / (W * W).sum()              # tangent to the Frobenius sphere
        g = np.concatenate([gW.ravel(), gb])
        lr_t = lr * (0.1 if t > 0.75 * steps else 1)
        m = 0.9 * m + 0.1 * g; v = 0.999 * v + 0.001 * g * g
        step = lr_t * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-12)
        W = W - step[:8].reshape(2, 4); b = b - step[8:]
        W *= np.sqrt(2) / np.linalg.norm(W)
    return W


if __name__ == "__main__":
    ps = [float(x) for x in sys.argv[1].split(",")]; seeds = [int(x) for x in sys.argv[2].split(",")]
    os.makedirs("results/compression", exist_ok=True); fn = "results/compression/trained_adam_v2.json"
    rows = json.load(open(fn)) if os.path.exists(fn) else []
    for p in ps:
        for s in seeds:
            if any(r["p"] == p and r["seed"] == s for r in rows): continue
            t0 = time.time(); W = train(p, s)
            norms = np.linalg.norm(W, axis=0)
            rows.append(dict(p=p, seed=s, W=W.tolist(), col_norms=norms.tolist(),
                             n_partners=int((norms[2:] > 0.01).sum()), secs=time.time() - t0))
            json.dump(rows, open(fn, "w"), indent=1)
            print(p, s, np.round(norms, 3), "partners:", rows[-1]["n_partners"], round(time.time() - t0, 1), flush=True)
