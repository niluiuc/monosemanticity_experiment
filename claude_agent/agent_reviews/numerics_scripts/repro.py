"""Task 4: reproduce repair_v1 results.
  bis <eta> <sigma>  : rerun the archived bisection with fra2_v2 (same code path as rerun_B_bisections.py,
                       nothing written there) AND an independent bisection with indep_eval
                       (sharing min found on a log grid |t| in [1e-4, 0.6], rel 3e-3, golden-refined).
  rows <name> <k1,k2,...> : re-solve archived sweep rows with fra2_v2 and with the independent dense search.
Writes ../numerics_results/repro_*.json"""
import os, sys, json, time, warnings
import numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); CA = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE); sys.path.insert(0, CA); sys.path.insert(0, os.path.join(CA, "repair_v1"))
os.chdir(CA)
import indep_eval as ie
ie.NB = 261
import fra2_v2
from fra2 import pc_theory
OUT = os.path.join(os.path.dirname(HERE), "numerics_results")


def indep_best_sharing(p, c, s, eta, rel=3e-3):
    g = np.geomspace(1e-4, 0.6, int(np.log(6000) / np.log1p(rel)) + 1)
    ts = np.concatenate([-g[::-1], g])
    v = ie.Fvec(ts, p, c, s, eta)
    j = int(np.argmin(v))
    t, f = ie.golden_t(lambda x: ie.F1(x, p, c, s, eta), ts[max(j - 1, 0)], ts[min(j + 1, len(ts) - 1)], it=70)
    return (t, f) if f < v[j] else (ts[j], v[j])


def bisect(fun, lo, hi, n=30):
    assert (not fun(lo)) and fun(hi)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if fun(mid): hi = mid
        else: lo = mid
    return [lo, hi]


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "bis":
        eta, s = float(sys.argv[2]), float(sys.argv[3])
        arch = json.load(open(os.path.join(CA, "repair_v1", "results", f"bisect_v2_eta{eta:.4f}_s{s}.json")))
        pred = arch["eps_pred"]; pc = pc_theory(eta)
        import rerun_B_bisections as rb
        t0 = time.time()
        bt = rb.bisect(rb.trained_shares, s, eta, pred)
        bf = rb.bisect(rb.fixed_shares, s, eta, pred)
        t1 = time.time()
        # independent: trained = min over t of noisy F beats F(0); fixed = clean optimum angle evaluated under noise
        def tr(eps):
            p = pc - eps; F0 = ie.F1(0.0, p, 0.0, s, eta)
            return indep_best_sharing(p, 0.0, s, eta)[1] < F0 - 1e-16
        def fx(eps):
            p = pc - eps; tc, fc = indep_best_sharing(p, 0.0, 0.0, eta)
            if fc >= ie.F1(0.0, p, 0.0, 0.0, eta): return False
            return ie.F1(tc, p, 0.0, s, eta) < ie.F1(0.0, p, 0.0, s, eta) - 1e-16
        it = bisect(tr, 0.3 * pred, 2.0 * pred, 30)
        jf = bisect(fx, 0.3 * pred, 2.0 * pred, 30)
        out = dict(eta=eta, sigma=s, archived_trained=arch["eps_trained_bracket"], archived_fixed=arch["eps_fixed_bracket"],
                   rerun_v2_trained=bt, rerun_v2_fixed=bf, indep_trained=it, indep_fixed=jf,
                   v2_identical=bool(bt == arch["eps_trained_bracket"] and bf == arch["eps_fixed_bracket"]),
                   indep_minus_arch_trained_rel=float(np.mean(it) / np.mean(arch["eps_trained_bracket"]) - 1),
                   indep_minus_arch_fixed_rel=float(np.mean(jf) / np.mean(arch["eps_fixed_bracket"]) - 1),
                   secs_v2=t1 - t0, secs_indep=time.time() - t1)
        json.dump(out, open(os.path.join(OUT, f"repro_bisect_eta{eta:.4f}_s{s}.json"), "w"), indent=1)
        print(json.dumps(out, indent=1))
    elif mode == "rows":
        name = sys.argv[2]; ks = [int(x) for x in sys.argv[3].split(",")]
        d = json.load(open(os.path.join(CA, "repair_v1", "results", f"{name}_v2_compare.json")))
        res = []
        for k in ks:
            r = d["rows"][k]; eta = 0.5
            n2 = fra2_v2.solve(r["p"], r["c"], r["sigma"], eta)
            tb, fb, F0, _ = ie.global_search(r["p"], r["c"], r["sigma"], eta, rel=2e-3)
            res.append(dict(name=name, k=k, p=r["p"], c=r["c"], sigma=r["sigma"], arch_new_t=r["new_t"], arch_new_F=r["new_F"],
                            rerun_t=n2["t_star"], rerun_F=n2["F_star"], indep_t=tb, indep_F=fb,
                            rerun_minus_arch=n2["F_star"] - r["new_F"], arch_minus_indep=r["new_F"] - fb))
            print("%s[%d] p=%.4f c=%+.4f s=%.3f  arch t=%+.6f  rerun t=%+.6f  indep t=%+.6f  rerun-arch=%+.1e arch-indep=%+.1e" % (
                name, k, r["p"], r["c"], r["sigma"], r["new_t"], n2["t_star"], tb, n2["F_star"] - r["new_F"], r["new_F"] - fb), flush=True)
        json.dump(res, open(os.path.join(OUT, f"repro_rows_{name}_{sys.argv[3].replace(',', '_')}.json"), "w"), indent=1)
