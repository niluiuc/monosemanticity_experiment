"""Task 11: which features are stored, three features in one dimension, vs (p, c13).
Feature 2 independent (importance .5), feature 3 correlated with feature 1 at c13 (importance .45).
Usage: python packing_map.py <chunk> <nchunks> | merge <nchunks>  -> results/three_feature/packing_map.json"""
import json, sys, os, time
import numpy as np
from multiprocessing import Pool
import fra3

PS = np.round(np.arange(0.05, 0.401, 0.025), 4)
CS = [-0.1, -0.05, -0.02, 0.0, 0.01, 0.02, 0.05, 0.1, 0.2]
ETA = (1.0, 0.5, 0.45)
SPECS = [(float(p), float(c)) for c in CS for p in PS
         if min(p * p + c * p * (1 - p), (1 - p) ** 2 + c * p * (1 - p), p * (1 - p) * (1 - c)) > 0]


def run(spec):
    p, c = spec
    fra3.C13 = c
    t0 = time.time(); r = fra3.solve(p, ETA, 0.0); r["c13"] = c; r["secs"] = time.time() - t0
    return r


if __name__ == "__main__":
    os.makedirs("results/three_feature", exist_ok=True)
    if sys.argv[1] == "merge":
        n = int(sys.argv[2]); rows = []
        for i in range(n): rows += json.load(open(f"results/three_feature/packing_part{i}.json"))
        json.dump(rows, open("results/three_feature/packing_map.json", "w"), indent=1); print("merged", len(rows)); raise SystemExit
    i, n = int(sys.argv[1]), int(sys.argv[2])
    fn = f"results/three_feature/packing_part{i}.json"
    if os.path.exists(fn): raise SystemExit("exists")
    t0 = time.time()
    with Pool(2) as pool:
        out = pool.map(run, SPECS[i::n], chunksize=1)
    json.dump(out, open(fn, "w"), indent=1); print(i, len(out), round(time.time() - t0, 1), "s")
