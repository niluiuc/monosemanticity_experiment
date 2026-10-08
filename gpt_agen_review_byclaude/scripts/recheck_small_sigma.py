"""Small-sigma part of the recheck: polish each noisy bias by an independent Newton/bisection solve of the
exact bias-stationarity equation (Claude's own code), starting from rt_core's fitted bias.
Quotient (Delta(sigma)-Delta(0))/sigma^2 at sigma in {1e-5,3e-5,1e-4,3e-4} vs the calibration-aware B."""
import json, sys
import numpy as np
from scipy.special import ndtr
from scipy.optimize import brentq
ROOT = "/sessions/gracious-eloquent-goodall/mnt/algoverse"
sys.path.insert(0, ROOT + "/claude_agent/repair_v3")
import rt_core as R
SEL = json.load(open(ROOT + "/claude_agent/repair_v3/results/selection.json")); ETA = SEL["eta"]; P = R.make_split()["P"]
phi = lambda z: np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
def grad(o, t, s, b):
    mu = o + b; z = mu / s
    return np.mean(mu * ndtr(z) + s * phi(z) - t * ndtr(z))
def polish(o, t, s, b):
    if s == 0: return b
    lo, hi = b - max(10 * s, 1e-6), b + max(10 * s, 1e-6)
    if grad(o, t, s, lo) < 0 < grad(o, t, s, hi): return brentq(lambda x: grad(o, t, s, x), lo, hi, xtol=1e-16, rtol=1e-15)
    return b
prev = json.load(open(ROOT + "/gpt_agen_review_byclaude/results/recheck_calibration_boundary.json"))
out = {}
for pair in SEL["selected_crossing"] + SEL["selected_control"]:
    info = [c for c in SEL["candidates"] if c["pair"] == pair][0]; rms = np.array(info["train_rms"])
    C = R.load_rows(R.CAL_ROWS, pair) / rms; XP = R.load_rows(P, pair) / rms
    ws = np.array([np.cos(info["encoder"]["theta"]), np.sin(info["encoder"]["theta"])]); r = info["mono"]["retained"]; wm = np.zeros(2); wm[r] = 1
    def deployed(w, s):
        b, _ = R.fit_biases(w, C, s, ETA); oc = R.offsets(w, C)
        return np.array([polish(oc[i], C[:, i], abs(w[i]) * s, b[i]) for i in range(2)])
    d0 = float(np.mean(R.per_image_loss(ws, deployed(ws, 0), XP, 0, ETA) - R.per_image_loss(wm, deployed(wm, 0), XP, 0, ETA)))
    rows = []
    for s in [1e-5, 3e-5, 1e-4, 3e-4, 1e-3]:
        d = float(np.mean(R.per_image_loss(ws, deployed(ws, s), XP, s, ETA) - R.per_image_loss(wm, deployed(wm, s), XP, s, ETA)))
        rows.append((s, (d - d0) / s ** 2))
    k = f"{pair[0]}_{pair[1]}"; out[k] = dict(B_corrected=prev[k]["B_calibration_corrected"], quotients=rows)
    print(pair, "B_corr %.8f" % prev[k]["B_calibration_corrected"], [(s, round(q, 8)) for s, q in rows], flush=True)
json.dump(out, open(ROOT + "/gpt_agen_review_byclaude/results/recheck_small_sigma.json", "w"), indent=1)
