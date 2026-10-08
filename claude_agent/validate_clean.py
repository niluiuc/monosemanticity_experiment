"""Task 1: reproduce the existing clean theorem (c=0, sigma=0) with the new solver."""
import json, time, numpy as np
from fra2 import solve, pc_theory, K_C_theory
rows=[]
for eta in [0.48, 0.5, 0.52, 2/3]:
    pc=pc_theory(eta); K,C=K_C_theory(eta)
    for eps in [0.02,0.01,0.005,0.0025,-0.005]:
        t0=time.time(); r=solve(pc-eps,0.0,0.0,eta)
        k=abs(np.tan(r['t_star'])); gain=r['F_mono']-r['F_star']
        rows.append(dict(eta=eta,pc=pc,eps=eps,t_star=r['t_star'],k=k,k_over_eps=k/eps if eps>0 else None,
                         K_theory=K,gain=gain,gain_over_eps3=gain/eps**3 if eps>0 else None,C_theory=C,secs=time.time()-t0))
        print({a:(round(b,6) if isinstance(b,float) else b) for a,b in rows[-1].items()})
json.dump(rows,open('results/validate_clean.json','w'),indent=1)
