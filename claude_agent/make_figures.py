"""All figures from saved results only (no new solves except the illustrative landscapes in fig4,
which are recomputed exactly and also saved to results/fig4_landscapes.json)."""
import json, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fra2 import pc_theory, K_C_theory, F

os.makedirs("figures", exist_ok=True)
ETA = 0.5; PC = pc_theory(ETA); K, C = K_C_theory(ETA)
BCAL = 0.1650382520217638  # D0 - v(p0) at eta=.5, project1_toy manuscript §5 (recomputed in README §3)
A3 = (BCAL / C) ** (1 / 3)
plt.rcParams.update({"font.size": 10, "figure.dpi": 140})

# ---- fig1 validation ---------------------------------------------------------
v = json.load(open("results/validate_clean.json"))
fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
for eta in sorted(set(r["eta"] for r in v)):
    rr = [r for r in v if r["eta"] == eta and r["eps"] > 0]
    e = [r["eps"] for r in rr]
    l = ax[0].plot(e, [r["k_over_eps"] for r in rr], "o-", label=f"eta={eta:.3g}")[0]
    ax[0].axhline(rr[0]["K_theory"], color=l.get_color(), ls=":")
    ax[1].plot(e, [r["gain_over_eps3"] for r in rr], "o-", color=l.get_color())
    ax[1].axhline(rr[0]["C_theory"], color=l.get_color(), ls=":")
ax[0].set(xscale="log", xlabel="eps = p_c - p", ylabel="k / eps", title="weak/strong ratio (dotted: K_eta)")
ax[1].set(xscale="log", xlabel="eps", ylabel="clean gain / eps^3", title="clean sharing gain (dotted: C_eta)")
ax[0].legend(fontsize=8)
fig.tight_layout(); fig.savefig("figures/fig1_validation_clean_theorem.png"); plt.close(fig)

# ---- fig2 correlation ---------------------------------------------------------
d = json.load(open("results/corr.json"))["rows"]
cs = sorted(set(r["c"] for r in d))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
cm = plt.cm.coolwarm
for i, c in enumerate(cs):
    rr = sorted([r for r in d if r["c"] == c and "error" not in r], key=lambda r: r["p"])
    ax[0].plot([r["p"] for r in rr], [r["t_star"] for r in rr], "o-", ms=3, color=cm(i / (len(cs) - 1)),
               lw=2.5 if c == 0 else 1.2, label=f"c={c:+g}")
ax[0].axvline(PC, color="k", ls=":", lw=0.8); ax[0].axhline(0, color="k", lw=0.5)
ax[0].set(xlabel="p (feature frequency)", ylabel="selected angle theta*  (0 = mono)",
          title="sigma=0: correlation c acts as a field")
ax[0].legend(fontsize=7, ncol=2)
s = json.load(open("results/corr_scaling.json"))["rows"]
neg = sorted([r for r in s if r["c"] < 0], key=lambda r: -r["c"])
pos = sorted([r for r in s if r["c"] > 0], key=lambda r: r["c"])
ax[1].loglog([-r["c"] for r in neg], [-r["t_star"] for r in neg], "o", label="c<0 (opposite-sign side)")
ax[1].loglog([r["c"] for r in pos], [r["t_star"] for r in pos], "s", label="c>0 (same-sign side)")
cc = np.logspace(-4, -1, 50)
q = 1 - PC; kap_plus = PC * q * (1 / (2 - PC) - ETA)
ax[1].loglog(cc, np.sqrt(2 * ETA * cc * PC * q * K ** 3 / (6 * C)), "k--", lw=0.8, label="pred. 0.734 |c|^(1/2)")
ax[1].loglog(cc, ETA * cc * PC * q / kap_plus, "k:", lw=0.8, label="pred. 4.24 c")
ax[1].set(xlabel="|c|", ylabel="|theta*| at p = p_c", title="response at the critical point")
ax[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig2_correlation_field.png"); plt.close(fig)

# ---- fig3 noise-trained ---------------------------------------------------------
d = json.load(open("results/noise.json"))["rows"]
cl = json.load(open("results/corr.json"))["rows"]
sig = sorted(set(r["sigma"] for r in d))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
rr = sorted([r for r in cl if r["c"] == 0.0], key=lambda r: r["p"])
ax[0].plot([r["p"] for r in rr], [r["t_star"] for r in rr], "k-", lw=2, label="sigma=0 (clean)")
for i, s_ in enumerate(sig):
    rr = sorted([r for r in d if r["sigma"] == s_], key=lambda r: r["p"])
    l = ax[0].plot([r["p"] for r in rr], [r["t_star"] for r in rr], "o-", ms=3, label=f"trained with sigma={s_}")[0]
    ax[0].axvline(PC - A3 * s_ ** (2 / 3), color=l.get_color(), ls=":", lw=0.9)
pp = np.linspace(0.15, PC, 100)
ax[0].plot(pp, -K * (PC - pp), color="gray", ls="--", lw=0.7, label="-K eps (clean asymptote)")
ax[0].set(xlabel="p", ylabel="theta*", title="training noise makes the transition first order\n(dotted: predicted p_c - (B_cal/C)^(1/3) sigma^(2/3))")
ax[0].legend(fontsize=7); ax[0].set_ylim(-0.5, 0.05)
# measured jump brackets vs prediction
meas = []
for s_ in sig:
    rr = sorted([r for r in d if r["sigma"] == s_], key=lambda r: r["p"])
    pmono = min(r["p"] for r in rr if abs(r["t_star"]) < 1e-6)      # first grid point selected mono
    last = max(r["p"] for r in rr if r["p"] < pmono)                  # last grid point selected sharing
    meas.append((s_, PC - last, PC - pmono))
ss = np.logspace(-3, -0.8, 50)
ax[1].loglog(ss, A3 * ss ** (2 / 3), "k--", label="prediction 0.832 sigma^(2/3) (no fit)")
for s_, a, b in meas:
    ax[1].plot([s_, s_], [b, a], "r-", lw=3)
ax[1].plot([], [], "r-", lw=3, label="measured bracket (p grid 0.005)")
ax[1].set(xlabel="training noise sigma", ylabel="shift eps*(sigma) = p_c - p*", title="shift of the storage transition")
ax[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig3_noise_trained_first_order.png"); plt.close(fig)
json.dump(dict(prediction_coeff=A3, measured_brackets=meas), open("results/fig3_shift_brackets.json", "w"), indent=1)

# ---- fig4 landscapes -----------------------------------------------------------
TH = -np.linspace(0, 0.3, 241)
land = {}
fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
for p in [0.36, 0.37, 0.38, 0.39]:
    vv = np.array([F(t, p, 0.0, 0.0, ETA)[0] for t in TH]); land[f"clean_p{p}"] = vv.tolist()
    ax[0].plot(TH, (vv - vv[0]) * 1e6, label=f"p={p}")
for p in [0.285, 0.295, 0.30, 0.305, 0.31]:
    vv = np.array([F(t, p, 0.0, 0.03, ETA)[0] for t in TH]); land[f"s0.03_p{p}"] = vv.tolist()
    ax[1].plot(TH, (vv - vv[0]) * 1e6, label=f"p={p}")
for a, ttl in zip(ax, ["clean training (sigma=0): single well, continuous", "trained with sigma=0.03: double well, first order"]):
    a.axhline(0, color="k", lw=0.5); a.set(xlabel="theta (opposite-sign side)", ylabel="[F(theta) - F(mono)] x 1e6", title=ttl)
    a.legend(fontsize=7)
ax[0].set_ylim(-8, 8); ax[1].set_ylim(-60, 60)
fig.tight_layout(); fig.savefig("figures/fig4_landscapes.png"); plt.close(fig)
json.dump(dict(theta=TH.tolist(), **land), open("results/fig4_landscapes.json", "w"))

# ---- fig5 phase diagram ---------------------------------------------------------
co = json.load(open("results/coexistence_clean.json"))
fig, ax = plt.subplots(figsize=(6.2, 4.2))
pp = np.linspace(0.30, PC, 100); ee = PC - pp
ax.plot(pp, 9 * C * ee ** 2 / (16 * ETA * pp * (1 - pp) * K), "k--", lw=0.8, label="sigma=0 first-order line, leading order")
ax.plot([r["p"] for r in co], [np.mean(r["c_star_bracket"]) for r in co], "ko", label="sigma=0 bisection (8 halvings)")
ax.plot([PC], [0], "k*", ms=12, label="sigma=0 critical point (existing theorem)")
# sigma=0.03: c=0 transition and negative-c endpoint bracket
ep = {}
for f in os.listdir("results/endpoint"):
    r = json.load(open("results/endpoint/" + f)); ep.setdefault(r["sigma"], []).append(r)
for s_, mk in [(0.003, "v"), (0.01, "^"), (0.03, "D")]:
    rs = sorted(ep[s_], key=lambda r: r["m"])
    yes = [r for r in rs if r["bistable_p"]]; no = [r for r in rs if not r["bistable_p"]]
    cin = min(r["c"] for r in yes); cout = max(r["c"] for r in no if r["c"] < cin) if any(r["c"] < cin for r in no) else None
    pin = [r for r in yes if r["c"] == cin][0]["bistable_p"][0]
    ax.plot([pin], [cin], mk, ms=8, label=f"sigma={s_}: last bistable c (endpoint in [{cout:.1e},{cin:.1e}])")
    ax.plot([PC - A3 * s_ ** (2 / 3)], [0], mk, ms=8, mfc="none", color=ax.lines[-1].get_color())
ax.axhline(0, color="gray", lw=0.5)
ax.set(xlabel="p", ylabel="feature correlation c", title="joint storage phase diagram (eta=0.5)\nopen markers: c=0 first-order point under training noise")
ax.legend(fontsize=6.5, loc="upper left")
fig.tight_layout(); fig.savefig("figures/fig5_phase_diagram.png"); plt.close(fig)

# ---- fig6 training dynamics --------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.2, 3.6))
for f, ls in [("results/hysteresis/s0.03_p0.28.json", "-"), ("results/hysteresis/s0.0_p0.28.json", ":")]:
    r = json.load(open(f))
    for init, col in [("mono_init", "C0"), ("sharing_init", "C3")]:
        for a in r[init]["adam"]:
            ax.plot(np.arange(1, len(a["traj"]) + 1) * 500, a["traj"], ls, color=col, lw=1.4)
ax.plot([], [], "C0-", label="init near mono, sigma=0.03"); ax.plot([], [], "C3-", label="init sharing, sigma=0.03")
ax.plot([], [], "k:", label="same, clean training (sigma=0)")
ax.set(xlabel="Adam step (batch 8192)", ylabel="theta", title="p=0.28: noise-trained models can stay stuck at mono")
ax.legend(fontsize=7)
fig.tight_layout(); fig.savefig("figures/fig6_training_metastability.png"); plt.close(fig)
print("figures done")
