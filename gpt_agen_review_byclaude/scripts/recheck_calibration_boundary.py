"""Independent recheck (Claude) of GPT's calibration-aware B (calibration_boundary_derivation.tex).
Uses Claude's own implementation (claude_agent/repair_v3/rt_core.py: exact Gaussian moments, exact
sigma=0 enumeration, noisy bias fits by grid + bounded refinement), NOT GPT's code. Rows: calibration
256:512 and the 896 P rows only (no E rows)."""
import json, os, sys
import numpy as np
from scipy.optimize import minimize_scalar
ROOT = "/sessions/gracious-eloquent-goodall/mnt/algoverse"
sys.path.insert(0, ROOT + "/claude_agent/repair_v3")
import rt_core as R
from scipy.special import ndtr
SEL = json.load(open(ROOT + "/claude_agent/repair_v3/results/selection.json"))
ETA = SEL["eta"]; P = R.make_split()["P"]
H = lambda z: (z * z + 1) * ndtr(z) + z * np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
sigmas = [1e-5, 3e-5, 1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1]
out = {}
for pair in SEL["selected_crossing"] + SEL["selected_control"]:
    info = [c for c in SEL["candidates"] if c["pair"] == pair][0]; rms = np.array(info["train_rms"])
    C = R.load_rows(R.CAL_ROWS, pair) / rms; XP = R.load_rows(P, pair) / rms
    ws = np.array([np.cos(info["encoder"]["theta"]), np.sin(info["encoder"]["theta"])])
    r = info["mono"]["retained"]; wm = np.zeros(2); wm[r] = 1
    bs0, _ = R.fit_biases(ws, C, 0.0, ETA); bm0, _ = R.fit_biases(wm, C, 0.0, ETA)
    o = R.offsets(ws, XP); f = [float(np.mean(o[i] + bs0[i] > 0)) for i in range(2)]
    pC = float(np.mean(C[:, r] > 0)); pP = float(np.mean(XP[:, r] > 0))
    zC = minimize_scalar(lambda z: pC * (1 + z * z) + (1 - pC) * H(z), bounds=(-8, 8), method="bounded", options={"xatol": 1e-13}).x
    zP = minimize_scalar(lambda z: pP * (1 + z * z) + (1 - pP) * H(z), bounds=(-8, 8), method="bounded", options={"xatol": 1e-13}).x
    shareB = sum(ETA[i] * ws[i] ** 2 * f[i] for i in range(2))
    B_corr = shareB - ETA[r] * (pP * (1 + zC ** 2) + (1 - pP) * H(zC))
    B_orig = shareB - ETA[r] * (pP * (1 + zP ** 2) + (1 - pP) * H(zP))
    d0 = float(np.mean(R.per_image_loss(ws, bs0, XP, 0, ETA) - R.per_image_loss(wm, bm0, XP, 0, ETA)))
    q = []
    for s in sigmas:
        bs, _ = R.fit_biases(ws, C, s, ETA); bm, _ = R.fit_biases(wm, C, s, ETA)
        d = float(np.mean(R.per_image_loss(ws, bs, XP, s, ETA) - R.per_image_loss(wm, bm, XP, s, ETA)))
        q.append(dict(sigma=s, quotient=(d - d0) / s ** 2, bias_mono_over_sigma=float(bm[r] / s)))
    # gate-distance scale: fraction of P sharing preactivations within distance d of a kink
    dist = np.min(np.abs(np.stack([o[i] + bs0[i] for i in range(2)])), 0)
    out[f"{pair[0]}_{pair[1]}"] = dict(B_original=B_orig, B_calibration_corrected=B_corr, z_cal=float(zC), p_cal=pC, p_pred=pP,
                                       delta0=d0, quotients=q, frac_P_within_1em3_of_gate=float(np.mean(dist < 1e-3)),
                                       frac_P_within_1em2_of_gate=float(np.mean(dist < 1e-2)), min_gate_distance=float(dist.min()))
    print(pair, "B_orig %.8f B_corr %.8f" % (B_orig, B_corr), [(x["sigma"], round(x["quotient"], 6)) for x in q], flush=True)
json.dump(out, open(ROOT + "/gpt_agen_review_byclaude/results/recheck_calibration_boundary.json", "w"), indent=1)
