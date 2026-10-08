"""Training noise in the compression setting (n=4, m=2, shared budget, eta=.5): Adam with isotropic
Gaussian code noise h = W x + sigma Z. Prediction from S3/S4 (transferred qualitatively): noise moves
storage of the partner to sparser p (a downward shift of the threshold, ~ sigma^(2/3)) and makes it abrupt.
Usage: python train_compression_noise.py <sigma> <p-list> <seeds>"""
import json, sys, os, time
import numpy as np
ETA = np.array([1, 1, 0.5, 0.5])

def train(p, s, seed, steps=8000, batch=4096, lr=3e-3):
    rng = np.random.default_rng(seed)
    W = rng.normal(size=(2, 4)) * 0.5; W *= np.sqrt(2) / np.linalg.norm(W); b = np.zeros(4)
    mo = np.zeros(12); vo = np.zeros(12)
    for t in range(1, steps + 1):
        X = (rng.random((batch, 4)) < p).astype(float); Z = rng.standard_normal((batch, 2))
        H = X @ W.T + s * Z; U = H @ W + b; Y = np.maximum(U, 0)
        G = 2 * ETA * (Y - X) * (U > 0) / batch
        gW = H.T @ G + (G @ W.T).T @ X                  # noise enters h but does not depend on W
        gW = gW - W * (W * gW).sum() / (W * W).sum()
        g = np.concatenate([gW.ravel(), G.sum(0)])
        lr_t = lr * (0.1 if t > 0.75 * steps else 1)
        mo = 0.9 * mo + 0.1 * g; vo = 0.999 * vo + 0.001 * g * g
        st = lr_t * (mo / (1 - 0.9 ** t)) / (np.sqrt(vo / (1 - 0.999 ** t)) + 1e-12)
        W = W - st[:8].reshape(2, 4); b = b - st[8:]; W *= np.sqrt(2) / np.linalg.norm(W)
    return W

if __name__ == "__main__":
    s = float(sys.argv[1]); ps = [float(x) for x in sys.argv[2].split(",")]; seeds = [int(x) for x in sys.argv[3].split(",")]
    fn = "results/compression/trained_adam_noise.json"; rows = json.load(open(fn)) if os.path.exists(fn) else []
    for p in ps:
        for sd in seeds:
            if any(r["p"] == p and r["seed"] == sd and r["sigma"] == s for r in rows): continue
            W = train(p, s, sd); nr = np.linalg.norm(W, axis=0)
            rows.append(dict(sigma=s, p=p, seed=sd, col_norms=nr.tolist(), max_partner=float(nr[2:].max())))
            json.dump(rows, open(fn, "w"), indent=1); print(s, p, sd, "max partner %.3f" % nr[2:].max(), flush=True)
