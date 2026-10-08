"""R2b — rerun every sweep that used fra2.solve, with the repaired search, and compare with the
archived results row by row. Same grids as sweep.py. Also re-solves the global optimum used in the
escape study (p = .29) and the S3 scaling-function comparison against the corrected eps_fix.
Run from claude_agent/:  python repair_v1/rerun_sweeps.py <noise|joint|corr|corr_scaling|escape|scaling>"""
import os, sys, json, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT)
from fra2_v2 import solve


def run(spec):
    import warnings; warnings.filterwarnings("ignore")
    p, c, s, eta = spec
    try:
        return solve(p, c, s, eta)
    except Exception as e:
        return dict(p=p, c=c, sigma=s, eta=eta, error=str(e))


def compare(name):
    old = json.load(open(os.path.join(ROOT, "results", f"{name}.json")))["rows"]
    old = [r for r in old if "error" not in r]
    specs = [(r["p"], r["c"], r["sigma"], r["eta"]) for r in old]
    with Pool(2) as pool:
        new = pool.map(run, specs, chunksize=4)
    rows, changed = [], 0
    for o, nw in zip(old, new):
        so = np.sign(round(o["t_star"], 9)); sn = np.sign(round(nw["t_star"], 9))
        dF = o["F_star"] - nw["F_star"]
        flag = bool(so != sn or abs(o["t_star"] - nw["t_star"]) > 1e-3)
        changed += flag
        rows.append(dict(p=o["p"], c=o["c"], sigma=o["sigma"], old_t=o["t_star"], new_t=nw["t_star"],
                         old_F=o["F_star"], new_F=nw["F_star"], old_minus_new_F=dF, changed=flag))
    out = dict(name=name, n=len(rows), n_changed=changed, max_F_improvement=max(r["old_minus_new_F"] for r in rows),
               rows=rows)
    json.dump(out, open(os.path.join(HERE, "results", f"{name}_v2_compare.json"), "w"), indent=1)
    print(name, "rows", len(rows), "changed", changed, "max F improvement %.3e" % out["max_F_improvement"])
    for r in rows:
        if r["changed"]:
            print("  CHANGED p=%.4f c=%+.4f s=%.4f  old t=%.5f  new t=%.5f  dF=%.2e" % (r["p"], r["c"], r["sigma"], r["old_t"], r["new_t"], r["old_minus_new_F"]))


if __name__ == "__main__":
    what = sys.argv[1]
    if what in ("noise", "joint", "corr", "corr_scaling"):
        compare(what)
    elif what == "escape":
        out = {}
        for s in [0.003, 0.01, 0.03]:
            old = json.load(open(os.path.join(ROOT, "results", "escape", f"s{s}_b8192.json")))["global"]
            nw = solve(0.29, 0.0, s, 0.5)
            out[str(s)] = dict(old=old, new=dict(t_star=nw["t_star"], F_star=nw["F_star"], F_mono=nw["F_mono"]))
            print(s, "old t*", round(old["t_star"], 5), "new t*", round(nw["t_star"], 5), "gain new %.3e" % (nw["F_mono"] - nw["F_star"]))
        json.dump(out, open(os.path.join(HERE, "results", "escape_global_v2.json"), "w"), indent=1)
    elif what == "scaling":
        old = json.load(open(os.path.join(ROOT, "results", "resultB", "S3_scaling_function2.json")))
        out = []
        for r in old:
            nf = json.load(open(os.path.join(HERE, "results", f"bisect_v2_eta0.5000_s{r['sigma']}.json")))
            fx = float(np.mean(nf["eps_fixed_bracket"])); tr = float(np.mean(nf["eps_trained_bracket"]))
            out.append(dict(sigma=r["sigma"], scaling_prediction=r["eps_scaling_with_amplitude"], eps_fixed_v2=fx, eps_trained_v2=tr,
                            rel_err_fixed=fx / r["eps_scaling_with_amplitude"] - 1, rel_err_trained=tr / r["eps_scaling_with_amplitude"] - 1))
            print(out[-1])
        json.dump(out, open(os.path.join(HERE, "results", "S3_scaling_vs_v2.json"), "w"), indent=1)
