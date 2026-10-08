"""Training-dynamics follow-up to Result D / B2: how often does minibatch Adam started near mono
escape to the (globally better) sharing branch inside the metastable window?
Prediction from B2: the barrier is O(sigma^2) while the window stays O(1), so escape should be
MORE likely at smaller sigma and smaller batch (larger gradient noise).
Setting: eta=.5, c=0, p=0.29 (inside [p_sp=0.279, p*(sigma)) for sigma in {0.003,0.01,0.03}).
Usage: python sgd_escape.py <sigma> <batch> <seed-list>  -> results/escape/s<sigma>_b<batch>.json (appends)"""
import json, sys, os, time
import numpy as np
from train_hysteresis import adam, exact_loss
from fra2 import solve

s, batch = float(sys.argv[1]), int(sys.argv[2]); seeds = [int(x) for x in sys.argv[3].split(",")]
p = 0.29
os.makedirs("results/escape", exist_ok=True)
fn = f"results/escape/s{s}_b{batch}.json"
rec = json.load(open(fn)) if os.path.exists(fn) else dict(sigma=s, batch=batch, p=p, runs=[])
if "global" not in rec:
    g = solve(p, 0.0, s, 0.5); rec["global"] = dict(t_star=g["t_star"], F_star=g["F_star"], F_mono=g["F_mono"])
done = {r["seed"] for r in rec["runs"]}
for sd in seeds:
    if sd in done: continue
    t0 = time.time()
    a = adam(-0.01, p, 0.0, s, 1000 + sd, steps=6000, batch=batch)
    rec["runs"].append(dict(seed=sd, theta=a["theta"], escaped=bool(a["theta"] < -0.05), secs=time.time() - t0))
    json.dump(rec, open(fn, "w"), indent=1)
    print(s, batch, sd, round(a["theta"], 4), round(time.time() - t0, 1), flush=True)
