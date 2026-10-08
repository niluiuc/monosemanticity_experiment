"""Does actual training see the noise-induced metastability?  Two experiments:
 (1) gradient flow on the EXACT population loss (L-BFGS-B from a given init; local, no search);
 (2) minibatch Adam on sampled data with sampled code noise (what a practitioner would run).
Each from a near-mono init (theta0=-0.01) and a sharing init (theta0=-0.25).
Params: v in R^2 (w = v/|v|, energy one), b in R^2.  eta=0.5, c=0.
Usage: python train_hysteresis.py <sigma> <p1,p2,...>"""
import json, sys, os, time
import numpy as np
from scipy.optimize import minimize
from fra2 import output_loss, states

ETA = 0.5


def exact_loss(params, p, c, s):
    t, b1, b2 = params
    return float(output_loss(np.cos(t), b1, t, 0, p, c, s) + ETA * output_loss(np.sin(t), b2, t, 1, p, c, s))


def flow(theta0, p, c, s):
    x0 = np.array([theta0, 0.0, p * 0.5])
    r = minimize(exact_loss, x0, args=(p, c, s), method="L-BFGS-B",
                 options=dict(ftol=1e-15, gtol=1e-11, maxiter=20000))
    return dict(theta=float(r.x[0]), b=r.x[1:].tolist(), loss=float(r.fun), success=bool(r.success))


def adam(theta0, p, c, s, seed, steps=6000, batch=8192, lr=3e-3):
    rng = np.random.default_rng(seed)
    X, pr = states(p, c)
    v = np.array([np.cos(theta0), np.sin(theta0)]); b = np.array([0.0, p * 0.5])
    m = np.zeros(4); u = np.zeros(4); b1_, b2_ = 0.9, 0.999
    traj = []
    for k in range(1, steps + 1):
        x = X[rng.choice(4, size=batch, p=pr)]
        nv = np.linalg.norm(v); w = v / nv
        h = x @ w + s * rng.standard_normal(batch)
        uu = w[None, :] * h[:, None] + b[None, :]
        y = np.maximum(uu, 0)
        g = 2 * np.array([1.0, ETA])[None, :] * (y - x) * (uu > 0)          # dL/du_i
        gb = g.mean(0)
        gw = (g * h[:, None]).mean(0)                                        # direct: u_i = w_i h + b_i
        gw = gw + ((g @ w)[:, None] * x).mean(0)                             # through h = w.x (noise does not depend on w)
        gv = (gw - w * (w @ gw)) / nv                                        # project: |w|=1
        grad = np.concatenate([gv, gb])
        lr_k = lr * (0.1 if k > 0.7 * steps else 1.0)
        m = b1_ * m + (1 - b1_) * grad; u = b2_ * u + (1 - b2_) * grad ** 2
        step = lr_k * (m / (1 - b1_ ** k)) / (np.sqrt(u / (1 - b2_ ** k)) + 1e-12)
        v = v - step[:2]; b = b - step[2:]
        if k % 500 == 0:
            ww = v / np.linalg.norm(v)
            traj.append(float(np.arctan(ww[1] / ww[0])))
    ww = v / np.linalg.norm(v); th = float(np.arctan(ww[1] / ww[0]))
    return dict(theta=th, b=b.tolist(), exact_loss_at_end=exact_loss([th, b[0], b[1]], p, c, s), traj=traj)


if __name__ == "__main__":
    s = float(sys.argv[1]); ps = [float(x) for x in sys.argv[2].split(",")]
    os.makedirs("results/hysteresis", exist_ok=True)
    for p in ps:
        fn = f"results/hysteresis/s{s}_p{p}.json"
        if os.path.exists(fn):
            continue
        t0 = time.time(); rec = dict(sigma=s, p=p, c=0.0)
        for name, th0 in [("mono_init", -0.01), ("sharing_init", -0.25)]:
            rec[name] = dict(flow=flow(th0, p, 0.0, s), adam=[adam(th0, p, 0.0, s, seed) for seed in (0, 1)])
            print(s, p, name, "flow theta", round(rec[name]["flow"]["theta"], 4),
                  "adam theta", [round(a["theta"], 4) for a in rec[name]["adam"]], flush=True)
        rec["secs"] = time.time() - t0
        json.dump(rec, open(fn, "w"), indent=1)
