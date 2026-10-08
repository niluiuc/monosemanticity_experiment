"""Step 2: deployed models + forecasts on P (no E access). See PROTOCOL_FROZEN.md.
   python rt_predict.py calib <a> <b>     (calibration bias fits for one selected pair; resumable)
   python rt_predict.py forecast          (P losses, joint bootstrap, gates, theory forecast)"""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rt_core as R

RES = os.path.join(R.HERE, "results")
SEL = json.load(open(os.path.join(RES, "selection.json")))
ETA = SEL["eta"]
SIG = np.round(np.arange(0, 1.0001, 0.01), 4)
Z = 2.394                       # two-sided 98.33% (Bonferroni over 3 pairs)
Q = (0.05 / 3 / 2, 1 - 0.05 / 3 / 2)


def pair_info(pair):
    return [c for c in SEL["candidates"] if c["pair"] == pair][0]


def models(info):
    ws = np.array([np.cos(info["encoder"]["theta"]), np.sin(info["encoder"]["theta"])])
    r = info["mono"]["retained"]; wm = np.zeros(2); wm[r] = 1.0; wm2 = np.zeros(2); wm2[1 - r] = 1.0
    return {"share": ws, "mono": wm, "mono_secondary": wm2}


def calib(pair):
    fn = os.path.join(RES, f"calib_{pair[0]}_{pair[1]}.json")
    if os.path.exists(fn): print("exists", fn); return
    info = pair_info(pair); rms = np.array(info["train_rms"])
    Xc = R.load_rows(R.CAL_ROWS, pair) / rms
    out = {}
    for name, w in models(info).items():
        out[name] = dict(w=w.tolist(), biases=[R.fit_biases(w, Xc, s, ETA)[0].tolist() for s in SIG])
    json.dump(dict(pair=pair, sigma=SIG.tolist(), models=out), open(fn, "w"), indent=1); print("calibrated", pair)


def curves(pair, X):
    c = json.load(open(os.path.join(RES, f"calib_{pair[0]}_{pair[1]}.json")))
    L = {}
    for name, m in c["models"].items():
        w = np.array(m["w"])
        L[name] = np.stack([R.per_image_loss(w, np.array(m["biases"][k]), X, s, ETA) for k, s in enumerate(SIG)], 1)
        b0 = np.array(m["biases"][0])
        L[name + "_frozen"] = np.stack([R.per_image_loss(w, b0, X, s, ETA) for s in SIG], 1)
    return L, c


def forecast():
    fn = os.path.join(RES, "predictions.json")
    if os.path.exists(fn): raise SystemExit("predictions exist (frozen)")
    split = R.make_split(); P = split["P"]; nP = len(P)
    pairs = SEL["selected_crossing"] + SEL["selected_control"]
    rng = np.random.default_rng(20261010); boots = [rng.integers(0, nP, nP) for _ in range(2000)]
    out = dict(sigma=SIG.tolist(), z=Z, n_boot=2000, pairs={})
    for pair in pairs:
        info = pair_info(pair); rms = np.array(info["train_rms"]); XP = R.load_rows(P, pair) / rms
        L, c = curves(pair, XP)
        dper = L["share"] - L["mono"]                     # per-image difference (nP x nSig)
        d = dper.mean(0)
        bd = np.array([dper[ix].mean(0) for ix in boots])
        band = np.quantile(bd, Q, axis=0)
        cr = R.first_crossing(SIG, d); bcr = np.array([R.first_crossing(SIG, x) for x in bd])
        # theory forecast
        ws = np.array(c["models"]["share"]["w"]); bs0 = np.array(c["models"]["share"]["biases"][0]); r = info["mono"]["retained"]
        def th(ix):
            X = XP[ix]; B, f, pr = R.theory_B(ws, bs0, r, X, ETA); G = -dper[ix, 0].mean()
            return (np.sqrt(G / B) if (B > 0 and G > 0) else np.nan), B, G, f, pr
        sth, B, G, f, pr = th(np.arange(nP))
        bth = np.array([th(ix)[0] for ix in boots[:500]])        # 500 resamples suffice for the theory interval
        o = R.offsets(ws, XP)
        def appl(s_):
            if not np.isfinite(s_): return None
            near_share = float(np.mean(np.any(np.stack([np.abs(o[i] + bs0[i]) < 2 * s_ for i in range(2)]), 0)))
            near_mono = float(np.mean((XP[:, r] > 0) & (XP[:, r] < 2 * s_)))
            return dict(frac_near_sharing_gate=near_share, frac_retained_in_0_2sigma=near_mono)
        rec = dict(cls=info["cls"], delta_P=d.tolist(), band_lo=band[0].tolist(), band_hi=band[1].tolist(),
                   delta_P_frozen=(L["share_frozen"] - L["mono_frozen"]).mean(0).tolist(),
                   delta_P_mono_secondary=(L["share"] - L["mono_secondary"]).mean(0).tolist())
        if info["cls"] == "crossing":
            ok = np.isfinite(bcr) & (bcr >= 0.05) & (bcr <= 0.9)
            v_emp = float(np.var(np.log(bcr[ok]))) if ok.sum() > 1 else np.nan
            h_emp = float(Z * np.sqrt(v_emp * (1 + nP / 1792))) if np.isfinite(v_emp) else np.nan
            okt = np.isfinite(bth)
            v_th = float(np.var(np.log(bth[okt]))) if okt.sum() > 1 else np.nan
            h_th = float(Z * np.sqrt(v_th * (1 + nP / 1792))) if np.isfinite(v_th) else np.nan
            ap = appl(sth)
            gate_emp = dict(a_clean_resolved=bool(band[1][0] < 0), b_frac_root_in_range=float(ok.mean()), c_h=h_emp)
            gate_emp["passes"] = bool(gate_emp["a_clean_resolved"] and gate_emp["b_frac_root_in_range"] >= 0.95 and np.isfinite(h_emp) and h_emp <= 0.20)
            gate_th = dict(frac_B_pos=float(np.mean(okt)), c_h=h_th, applicability=ap)
            inside = ap is not None and ap["frac_near_sharing_gate"] <= 0.2 and ap["frac_retained_in_0_2sigma"] <= 0.2
            gate_th["passes"] = bool(gate_th["frac_B_pos"] >= 0.95 and np.isfinite(h_th) and h_th <= 0.20 and inside)
            gate_th["label"] = "evaluable" if gate_th["passes"] else ("outside asymptotic domain" if (ap is not None and not inside) else "imprecise/unavailable")
            rec.update(sigma_star_emp=cr if np.isfinite(cr) else None, var_log_emp=v_emp, gate_emp=gate_emp,
                       sigma_star_th=float(sth) if np.isfinite(sth) else None, theory_B=float(B), theory_G=float(G),
                       open_fracs=f, p_retained=pr, var_log_th=v_th, gate_th=gate_th,
                       emp_root_quantiles=np.quantile(np.where(np.isfinite(bcr), bcr, 9.9), [Q[0], 0.5, Q[1]]).tolist())
        else:
            rec.update(control_band_below_zero_on_P=bool(np.all(band[1] < 0)),
                       theory_B=float(B), theory_G=float(G), sigma_star_th=float(sth) if np.isfinite(sth) else None)
        out["pairs"][f"{pair[0]}_{pair[1]}"] = rec
        print(pair, info["cls"], json.dumps({k: v for k, v in rec.items() if not isinstance(v, list)}), flush=True)
    out["any_crossing_forecast_informative"] = any(v.get("gate_emp", {}).get("passes", False) or v.get("gate_th", {}).get("passes", False)
                                                   for v in out["pairs"].values())
    json.dump(out, open(fn, "w"), indent=1)
    print("ANY INFORMATIVE CROSSING FORECAST:", out["any_crossing_forecast_informative"])


if __name__ == "__main__":
    if sys.argv[1] == "calib": calib([int(sys.argv[2]), int(sys.argv[3])])
    else: forecast()
