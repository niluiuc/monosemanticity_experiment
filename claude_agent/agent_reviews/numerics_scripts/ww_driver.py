"""Resumable driver for well_width.analyse (the sandbox kills processes after ~170 s).
python ww_driver.py <worker 0|1> [budget_s]  ; run two workers in parallel, repeat until 'ALL DONE'."""
import os, sys, json, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import well_width as ww

T0 = time.time()
k = int(sys.argv[1]); budget = float(sys.argv[2]) if len(sys.argv) > 2 else 135
NP = 21
out_dir = os.path.join(os.path.dirname(HERE), "numerics_results", "ww"); os.makedirs(out_dir, exist_ok=True)
tasks = []
SET = sys.argv[3] if len(sys.argv) > 3 else "main"
if SET == "main":
    for s in [0.001, 0.003, 0.01, 0.03]:
        for c in [0.0, -0.002, 0.002]:
            for i in range(NP):
                tasks.append((s, c, i))
else:      # adversarial: small |c| comparable to the noise-induced scales
    for s, cl in [(0.003, [-1e-3, -3e-4, -1e-4, 1e-4, 3e-4, 1e-3]), (0.001, [-1e-4, 1e-4])]:
        for c in cl:
            for i in range(0, NP, 2):
                tasks.append((s, c, i))
todo = [t for t in tasks if not os.path.exists(os.path.join(out_dir, f"ww_s{t[0]}_c{t[1]}_n{NP}_i{t[2]:03d}.json"))]
mine = todo[k::2]
last = 0
for s, c, i in mine:
    if time.time() - T0 + 1.3 * last > budget:
        print("budget stop; remaining", len(todo)); break
    p0 = ww.PC - 0.8316 * s ** (2 / 3); p = float((p0 + np.linspace(-0.01, 0.01, NP))[i])
    t1 = time.time(); r = ww.analyse(p, c, s, 2e-3); last = time.time() - t1; r["secs"] = last
    json.dump(dict(sigma=s, c=c, eta=0.5, rel=2e-3, rows=[r]),
              open(os.path.join(out_dir, f"ww_s{s}_c{c}_n{NP}_i{i:03d}.json"), "w"), indent=1)
    print(s, c, i, "%.1fs" % last, flush=True)
else:
    print("ALL DONE (worker %d)" % k)
