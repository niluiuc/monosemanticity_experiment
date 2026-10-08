"""Task 3: differential test of fra2_v2.solve against an independent very dense search.
Sets: 'random' (40 pts, seed 2026: p~U[.15,.45], c~U[-.05,.05], sigma in {0,.003,.01,.03,.1}, eta=.5)
      'adv'    (adversarial: near-transition points, tiny sigma, tiny |c|, other eta).
Independent search: indep_eval.global_search (log grid rel 1e-3 on [1e-8, pi/2] both signs + 6001 linear
points, every discrete local min golden-refined).  Resumable; python diff_test.py <set> <worker> [budget]"""
import os, sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
import indep_eval as ie
import fra2_v2, fra2
ie.NB = 261
PC = (3 - np.sqrt(5)) / 2


def specs(name):
    if name == "random":
        rng = np.random.default_rng(2026)
        return [(float(rng.uniform(.15, .45)), float(rng.uniform(-.05, .05)),
                 float(rng.choice([0, .003, .01, .03, .1])), 0.5) for _ in range(40)]
    if name == "adv":
        out = []
        for s in [1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2]:
            pT = PC - 0.8316 * s ** (2 / 3) * 1.03          # ~ near the actual transition (+3% shift)
            for dp in [-2e-4, 0.0, 2e-4]:
                for c in [0.0, -1e-3, 1e-3]:
                    out.append((float(pT + dp), c, s, 0.5))
        for eta in [0.48, 0.52, 2 / 3]:
            pc = (1 + eta - np.sqrt(1 + 2 * eta - 3 * eta ** 2)) / (2 * eta)
            for s in [0.003]:
                out.append((float(pc - 0.018), 0.0, s, eta)); out.append((float(pc - 0.0175), 0.0, s, eta))
        return out
    raise SystemExit("unknown set")


if __name__ == "__main__":
    T0 = time.time()
    name, k = sys.argv[1], int(sys.argv[2]); budget = float(sys.argv[3]) if len(sys.argv) > 3 else 140
    out_dir = os.path.join(os.path.dirname(HERE), "numerics_results", "diff_" + name); os.makedirs(out_dir, exist_ok=True)
    S = specs(name); last = 0
    for i in range(k, len(S), 2):
        fn = os.path.join(out_dir, f"pt{i:03d}.json")
        if os.path.exists(fn): continue
        if time.time() - T0 + 1.3 * last > budget: print("budget stop"); break
        p, c, s, eta = S[i]; t1 = time.time()
        try:
            r2 = fra2_v2.solve(p, c, s, eta)
        except Exception as e:
            r2 = dict(error=str(e))
        tb, fb, F0, mins = ie.global_search(p, c, s, eta, rel=1e-3)
        # cross-check my best with fra2.F (the evaluator fra2_v2 reports)
        fb_fra2 = fra2.F(tb, p, c, s, eta)[0]
        out = dict(i=i, p=p, c=c, sigma=s, eta=eta, mine_t=tb, mine_F=fb, mine_F_via_fra2F=fb_fra2, mine_F0=F0,
                   n_local_minima_mine=len(mins), v2=r2,
                   v2_minus_mine=(r2["F_star"] - fb) if "F_star" in r2 else None,
                   v2_minus_fra2F_at_mine=(r2["F_star"] - fb_fra2) if "F_star" in r2 else None)
        last = time.time() - t1; out["secs"] = last
        json.dump(out, open(fn, "w"), indent=1)
        print(i, "p=%.6f c=%+.5f s=%.4g eta=%.3f  v2 t=%+.6f mine t=%+.6f  v2-mine=%+.2e  (%.1fs)" % (
            p, c, s, eta, r2.get("t_star", np.nan), tb, out["v2_minus_mine"] if out["v2_minus_mine"] is not None else np.nan, last), flush=True)
    else:
        print("ALL DONE", name, k)
