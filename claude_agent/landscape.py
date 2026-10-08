"""Bistability (metastability) detection on the exact bias-profiled landscape F(theta).

A first-order transition shows up as a range of p where F(theta) restricted to the
opposite-sign side theta in [-0.5, 0] has TWO local minima (one near mono, one sharing).
That bistable window shrinks to zero at a critical endpoint. We use it to locate the
endpoint c_e(sigma) on the negative-correlation side.
Usage: python landscape.py <sigma> <c> <p_lo> <p_hi> <n_p>
"""
import json, sys, time, os
import numpy as np
from fra2 import F

TH = -np.unique(np.concatenate([np.linspace(0, 0.5, 161), np.logspace(-4, -1, 31)]))


def landscape(p, c, sigma, eta=0.5):
    return np.array([F(t, p, c, sigma, eta)[0] for t in TH])


def local_minima(v, tol=1e-13):
    """Indices of strict local minima of v along the theta grid (endpoints included)."""
    idx = []
    n = len(v)
    for i in range(n):
        left = v[i - 1] if i > 0 else np.inf
        right = v[i + 1] if i < n - 1 else np.inf
        if v[i] < left - tol and v[i] < right - tol:
            idx.append(i)
    return idx


if __name__ == "__main__":
    sigma, c, plo, phi_, n = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
    os.makedirs("results/bistability", exist_ok=True)
    fn = f"results/bistability/s{sigma}_c{c}_p{plo}-{phi_}.json"
    rows = []
    t0 = time.time()
    order = np.argsort(TH)
    for p in np.linspace(plo, phi_, n):
        v = landscape(p, c, sigma)
        vs, ts = v[order], TH[order]
        mins = local_minima(vs)
        rows.append(dict(p=float(p), n_min=len(mins), minima_theta=[float(ts[i]) for i in mins],
                         minima_F=[float(vs[i]) for i in mins]))
        print(round(p, 5), len(mins), [round(ts[i], 4) for i in mins], [f"{vs[i]:.8f}" for i in mins], flush=True)
    json.dump(dict(sigma=sigma, c=c, theta_grid=TH.tolist(), rows=rows, secs=time.time() - t0), open(fn, "w"), indent=1)
    print("secs", round(time.time() - t0, 1))
