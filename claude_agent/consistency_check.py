"""Recompute headline numbers quoted in README/STATEMENTS/addendum from saved result files."""
import json, numpy as np
chk = {}
a = json.load(open("results/real/analysis.json")); b = json.load(open("results/real_logits/analysis.json"))
chk["pairs_sign_layer4"] = (a["P1_opposite_sign_rate_corr_lt_-0.05"], a["P1_same_sign_rate_corr_gt_0.15"])
chk["pairs_sign_logits"] = (b["P1_opposite_sign_rate_corr_lt_-0.05"], b["P1_same_sign_rate_corr_gt_0.15"])
chk["bistable_layer4_low_high"] = (a["P2_bistable_rate_low_absCorr_tercile"], a["P2_bistable_rate_high_absCorr_tercile"])
chk["bistable_logits_low_high"] = (b["P2_bistable_rate_low_absCorr_tercile"], b["P2_bistable_rate_high_absCorr_tercile"])
chk["coexist_posthoc"] = json.load(open("results/real_branch_coexistence_posthoc.json"))
for k in chk["coexist_posthoc"]:
    cc = chk["coexist_posthoc"][k]["corr_of_coexisting"]; chk["coexist_posthoc"][k] = dict(pos=sum(c > 0 for c in cc), neg=sum(c < 0 for c in cc), zero=sum(c == 0 for c in cc))
t = json.load(open("results/real_triples/analysis.json")); chk["triples"] = {k: v for k, v in t.items() if k.startswith("T")}
v = json.load(open("results/verify.json")); chk["mc_max_z"] = max(abs(r["z"]) for r in v["monte_carlo"])
A = json.load(open("results/analytic_A.json")); chk["analytic_A"] = {k: A[k] for k in ["B_independent", "B_from_K_C", "critical_response_coeff_c<0", "same_sign_response_coeff", "c_star_coeff_eps2", "max_abs_diff"]}
g = json.load(open("results/gate_lemma.json")); chk["gate_lemma_all_positive"] = g["all_positive"]
for f in ["transition_bisection", "bisection_eta0.3", "bisection_eta0.7_same_sign"]:
    r = json.load(open(f"results/compression/{f}.json")); chk[f] = (r["bracket"], r.get("prediction", r.get("prediction_shared")))
chk["bicritical"] = json.load(open("results/bicritical_identity.json"))["verified"]
print(json.dumps(chk, indent=1, default=str))
json.dump(chk, open("results/consistency_check.json", "w"), indent=1, default=str)
