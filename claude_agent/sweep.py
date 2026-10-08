"""Run a grid of exact solves in parallel and save JSON. Usage: python sweep.py <name>"""
import json, sys, time, numpy as np
from multiprocessing import Pool
from fra2 import solve, pc_theory

ETA = 0.5
PC = pc_theory(ETA)


def specs(name):
    if name == "corr":          # Task 2: correlation as a field, clean training
        ps = np.round(np.arange(0.30, 0.4601, 0.005), 6)
        return [(p, c, 0.0, ETA) for c in [-0.05, -0.02, -0.005, 0.0, 0.005, 0.02, 0.05] for p in ps]
    if name == "corr_scaling":  # Task 2: weak weight at p = pc vs |c|
        cs = np.logspace(-4, -1, 13)
        return [(PC, s * c, 0.0, ETA) for s in (-1, 1) for c in cs]
    if name == "noise":         # Task 3: noise-trained selection, c = 0
        ps = np.round(np.arange(0.15, 0.4201, 0.005), 6)
        return [(p, 0.0, s, ETA) for s in [0.003, 0.01, 0.03, 0.1] for p in ps]
    if name == "joint":         # Task 4: correlation + training noise
        ps = np.round(np.arange(0.22, 0.4001, 0.005), 6)
        return [(p, c, 0.03, ETA) for c in [-0.05, -0.02, -0.005, 0.005, 0.02, 0.05] for p in ps]
    raise SystemExit(name)


def run(spec):
    p, c, s, eta = spec
    t0 = time.time()
    try:
        r = solve(p, c, s, eta)
    except ValueError as e:
        return dict(p=p, c=c, sigma=s, eta=eta, error=str(e))
    r["secs"] = time.time() - t0
    return r


if __name__ == "__main__":
    # python sweep.py <name> [chunk nchunks]   (the sandbox caps one call at ~3 min, so
    # large grids are run in chunks; `python sweep.py <name> merge <nchunks>` joins them)
    import os
    name = sys.argv[1]
    S = specs(name)
    if len(sys.argv) > 3 and sys.argv[2] == "merge":
        n = int(sys.argv[3]); rows = []
        for i in range(n):
            rows += json.load(open(f"results/{name}_part{i}.json"))["rows"]
        json.dump(dict(name=name, eta=ETA, pc_clean=PC, n=len(rows), rows=rows),
                  open(f"results/{name}.json", "w"), indent=1)
        print("merged", len(rows)); raise SystemExit
    i, n = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (0, 1)
    part = S[i::n]
    fn = f"results/{name}.json" if n == 1 else f"results/{name}_part{i}.json"
    if os.path.exists(fn):
        print("exists", fn); raise SystemExit
    t0 = time.time()
    with Pool(2) as pool:
        out = pool.map(run, part, chunksize=1)
    json.dump(dict(name=name, eta=ETA, pc_clean=PC, n=len(out), wall_secs=time.time() - t0, rows=out),
              open(fn, "w"), indent=1)
    print(name, i, len(out), "solves", round(time.time() - t0, 1), "s")
