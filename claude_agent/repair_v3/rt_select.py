"""Step 1: bounded candidate screening (TRAIN + development-selection S only). Run once.
At most 12 candidate pairs in a fixed seeded order. Encoders fitted on TRAIN (sigma = 0). For each sigma
on the coarse selection grid, biases are fitted on TRAIN; Delta_S(sigma) = mean over S images of
(sharing - primary mono) per-image risk.
Classification: crossing = Delta_S(0) < 0 and first -/+ crossing in [0.05, 0.9];
control = Delta_S < 0 on the whole grid [0, 1]; else other.
Selected: first two crossing and first two control candidates in seed order. Identities are then frozen."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rt_core as R

OUT = os.path.join(R.HERE, "results", "selection.json")
ETA = [1.0, 0.5]
SIG_SEL = np.round(np.arange(0, 1.0001, 0.05), 4)


def previously_analysed():
    prev = set()
    base = os.path.join(R.ALGO, "claude_agent", "results")
    for f, keys in [("real_logits/pairs.json", None), ("real_triples_logits/triples.json", None)]:
        fp = os.path.join(base, f)
        if not os.path.exists(fp): continue
        d = json.load(open(fp)); items = d["pairs"] if isinstance(d, dict) else d
        for it in items:
            ids = [it[k] for k in ("i", "j", "k") if k in it]
            for a in ids:
                for b in ids:
                    if a < b: prev.add((a, b))
    return prev


if __name__ == "__main__":
    if os.path.exists(OUT): raise SystemExit("selection already exists (frozen); refusing to overwrite")
    t0 = time.time(); split = R.make_split()
    Ltr = np.maximum(np.load(R.LOGITS, mmap_mode="r")[R.TRAIN_ROWS].astype(float), 0)
    zf = (Ltr <= 0).mean(0)
    elig = [k for k in range(1000) if 0.2 <= zf[k] <= 0.8 and k not in (281, 207)]
    prev = previously_analysed()
    rng = np.random.default_rng(R.SPLIT_SEED + 1)
    cands = []
    while len(cands) < 12:
        a, b = sorted(rng.choice(elig, 2, replace=False).tolist())
        if (a, b) in prev or (a, b) in [tuple(c) for c in cands]: continue
        cands.append((a, b))
    PART = OUT.replace(".json", "_partial.json")       # resumable across the ~3-minute shell limit; same single run
    rows = json.load(open(PART)) if os.path.exists(PART) else []
    done = {tuple(r["pair"]) for r in rows}
    for (a, b) in cands:
        if (a, b) in done: continue
        if time.time() - t0 > 140: raise SystemExit("time budget for this call reached; rerun to continue (resumable)")
        Xtr = R.load_rows(R.TRAIN_ROWS, [a, b]); rms = np.sqrt((Xtr ** 2).mean(0)); Xtr = Xtr / rms
        XS = R.load_rows(split["S"], [a, b]) / rms
        enc = R.fit_sharing_encoder(Xtr, ETA); mono = R.fit_mono(Xtr, ETA)
        ws = np.array([np.cos(enc["theta"]), np.sin(enc["theta"])]); wm = np.zeros(2); wm[mono["retained"]] = 1.0
        d = []
        for s in SIG_SEL:
            bs, _ = R.fit_biases(ws, Xtr, s, ETA); bm, _ = R.fit_biases(wm, Xtr, s, ETA)
            d.append(float(np.mean(R.per_image_loss(ws, bs, XS, s, ETA) - R.per_image_loss(wm, bm, XS, s, ETA))))
        d = np.array(d); cr = R.first_crossing(SIG_SEL, d)
        if d[0] < 0 and np.isfinite(cr) and 0.05 <= cr <= 0.9: cls = "crossing"
        elif np.all(d < 0): cls = "control"
        else: cls = "other"
        rows.append(dict(pair=[a, b], train_rms=rms.tolist(), train_zero_frac=[float(zf[a]), float(zf[b])],
                         train_corr=float(np.corrcoef(Xtr.T)[0, 1]), encoder=enc, mono=mono,
                         delta_S=d.tolist(), crossing_S=cr if np.isfinite(cr) else None, cls=cls))
        json.dump(rows, open(PART, "w"), indent=1)
        print((a, b), cls, "theta %.4f" % enc["theta"], "mono r=%d" % mono["retained"], "Delta_S(0)=%.4f" % d[0],
              "cross", cr, flush=True)
    rows = sorted(rows, key=lambda r: [tuple(c) for c in cands].index(tuple(r["pair"])))
    sel = [r["pair"] for r in rows if r["cls"] == "crossing"][:2] + [r["pair"] for r in rows if r["cls"] == "control"][:2]
    out = dict(split_seed=R.SPLIT_SEED, split_sizes={k: len(v) for k, v in split.items()},
               split_rows={k: v.tolist() for k, v in split.items()}, excluded_rows=[512, 1024],
               eta=ETA, sigma_selection_grid=SIG_SEL.tolist(), candidates=rows,
               selected_crossing=[r["pair"] for r in rows if r["cls"] == "crossing"][:2],
               selected_control=[r["pair"] for r in rows if r["cls"] == "control"][:2],
               n_crossing_available=sum(r["cls"] == "crossing" for r in rows),
               n_control_available=sum(r["cls"] == "control" for r in rows), secs=time.time() - t0)
    json.dump(out, open(OUT, "w"), indent=1)
    print("SELECTED crossing", out["selected_crossing"], "control", out["selected_control"], round(out["secs"], 1), "s")
