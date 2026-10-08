"""Retrospective pipeline check (NOT evidence): archived pair 281/207 with its original convention
(eta = (1, 2/3), absolute sigma = 0.730851028581592 * {0, .05, .1, .2, .4}, train RMS, mono both orientations,
calibration-fitted biases, archived test rows 512:4608). Compare with the archived calibrated differences
and report the sign of the theory coefficient B there."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rt_core as R

ETA = [1.0, 2 / 3]
SIG = 0.730851028581592 * np.array([0, .05, .1, .2, .4])
ARCH = [-.0710555300, -.0711548026, -.0713725079, -.0719331061, -.0732688755]
pair = [281, 207]
Xtr = R.load_rows(R.TRAIN_ROWS, pair); rms = np.sqrt((Xtr ** 2).mean(0)); Xtr = Xtr / rms
Xc = R.load_rows(R.CAL_ROWS, pair) / rms
Xt = R.load_rows(np.arange(512, 4608), pair) / rms
enc = R.fit_sharing_encoder(Xtr, ETA); mono = R.fit_mono(Xtr, ETA)
ws = np.array([np.cos(enc["theta"]), np.sin(enc["theta"])]); wm = np.zeros(2); wm[mono["retained"]] = 1
d = []
for s in SIG:
    bs, _ = R.fit_biases(ws, Xc, s, ETA); bm, _ = R.fit_biases(wm, Xc, s, ETA)
    d.append(float(np.mean(R.per_image_loss(ws, bs, Xt, s, ETA) - R.per_image_loss(wm, bm, Xt, s, ETA))))
bs0, _ = R.fit_biases(ws, Xc, 0.0, ETA)
B, f, pr = R.theory_B(ws, bs0, mono["retained"], Xt, ETA)
out = dict(encoder=enc, weights=ws.tolist(), archived_weights=[0.83541738, 0.54961605], mono=mono,
           sigma=SIG.tolist(), delta_reproduced=d, delta_archived=ARCH, max_abs_diff=float(np.max(np.abs(np.array(d) - ARCH))),
           theory_B=B, open_fracs=f, p_retained=pr,
           theory_reading="B<0 predicts the sharing advantage grows at small noise (no small-sigma crossing)" if B < 0 else "B>0")
json.dump(out, open(os.path.join(R.HERE, "results", "pipeline_check_281_207.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
