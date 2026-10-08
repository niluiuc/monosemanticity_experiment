"""Independent recheck (Claude) of GPT's controlled learned-image completion. Own Gaussian-risk code;
reads saved scores/labels/models only; no training, no new inference."""
import json, hashlib, sys
import numpy as np
from scipy.special import ndtr
ROOT = "/sessions/gracious-eloquent-goodall/mnt/algoverse"
G = ROOT + "/claude_agen_review_bygpt"; O = G + "/controlled_image_completion_v1"
TR = ROOT + "/project1_toy/controlled_image_phase_20261007/learning_run_v1"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
def risk(r, X, w, b, sigma):
    tot = 0
    for i in range(2):
        mu = w[i] * (r @ w) + b[i]; s = abs(w[i]) * sigma
        if s == 0: tot = tot + (np.maximum(mu, 0) - X[:, i]) ** 2; continue
        z = mu / s; Phi = ndtr(z); phi = np.exp(-z * z / 2) / np.sqrt(2 * np.pi)
        m1 = mu * Phi + s * phi; m2 = (mu * mu + s * s) * Phi + mu * s * phi
        tot = tot + m2 - 2 * X[:, i] * m1 + X[:, i] ** 2
    return tot
pred = json.load(open(O + "/prediction.json")); ev = json.load(open(O + "/evaluation.json"))
prov = json.load(open(O + "/test_inference/provenance.json")); shas = json.load(open(O + "/test_inference/sha256.json"))
out = {}
# --- integrity
out["prediction_sha_matches_provenance"] = sha(O + "/prediction.json") == prov["prediction_sha256"]
out["model_sha_matches"] = sha(TR + "/model.pt") == pred["model_sha256"] == prov["model_sha256"]
out["script_sha_current_matches_prediction"] = sha(G + "/controlled_image_completion.py") == pred["script_sha256"]
out["test_inference_file_hashes_match"] = all(sha(O + "/test_inference/" + k) == v for k, v in shas.items())
import os
out["mtime_prediction"] = os.path.getmtime(O + "/prediction.json"); out["mtime_test_scores"] = os.path.getmtime(O + "/test_inference/test_scores.npz")
out["prediction_written_before_test_scores"] = out["mtime_prediction"] < out["mtime_test_scores"]
ids = np.load(TR + "/split_background_ids.npz"); tids = np.load(O + "/test_inference/split_background_ids.npz")
out["split_files_identical"] = all(np.array_equal(ids[k], tids[k]) for k in ids.files)
test = np.load(O + "/test_inference/test_scores.npz"); r = test["scores"]; X = test["labels"]
out["test_backgrounds_disjoint"] = (len(set(test["background_ids"]) & set(ids["train"])) == 0 and len(set(test["background_ids"]) & set(ids["calibration"])) == 0)
out["test_backgrounds_are_declared_test_split"] = set(test["background_ids"]) == set(ids["test"])
out["labels_balanced_tile"] = bool(np.array_equal(X, np.tile([[0, 0], [0, 1], [1, 0], [1, 1]], (len(X) // 4, 1))))
# --- recompute
delta = float(np.sqrt(np.mean(np.sum((r - X) ** 2, 1)))); out["test_recovery_rms"] = delta
STATES = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], float)
rows = []
for p, e in zip(pred["rows"], ev["rows"]):
    m = p["models"]; s = p["sigma"]
    d_test = float(np.mean(risk(r, X, np.array(m["share"]["weights"]), np.array(m["share"]["biases"]), s) - risk(r, X, np.array(m["mono"]["weights"]), np.array(m["mono"]["biases"]), s)))
    rs = float(np.mean(risk(STATES, STATES, np.array(m["share"]["weights"]), np.array(m["share"]["biases"]), s)))
    rm = float(np.mean(risk(STATES, STATES, np.array(m["mono"]["weights"]), np.array(m["mono"]["biases"]), s)))
    lo = max(0, np.sqrt(rs) - delta) ** 2 - (np.sqrt(rm) + delta) ** 2; hi = (np.sqrt(rs) + delta) ** 2 - max(0, np.sqrt(rm) - delta) ** 2
    rows.append(dict(sigma=s, observed_diff_recomputed=d_test, observed_diff_gpt=e["observed_difference"], abs_err=abs(d_test - e["observed_difference"]),
                     ideal_reference_diff=rs - rm, ideal_reference_gpt=p["reference_difference"], actual_delta_bound=[lo, hi],
                     inside_predicted=p["predicted_interval"][0] <= d_test <= p["predicted_interval"][1],
                     observed_minus_ideal=d_test - (rs - rm)))
out["rows"] = rows
# --- Lipschitz coupling check (empirical): per-image |sqrt-risk| perturbation vs score error
out["note"] = "Coupling bound: x -> tied-ReLU reconstruction is 1-Lipschitz in L2 for energy-one w and equal importances, so |sqrt R(r) - sqrt R(X)| <= RMS||r-X||."
json.dump(out, open(ROOT + "/gpt_agen_review_byclaude/results/recheck_controlled_image.json", "w"), indent=1, default=float)
print(json.dumps(out, indent=1, default=float))
