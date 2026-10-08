"""Describe saved training trajectories only; no new training or tuned settings."""
import json
from pathlib import Path
import numpy as np
here=Path(__file__).parent; out=here/'run_v1'
rows=[]
for seed in [0,1,2]:
 a=np.load(out/f'p0.20_seed{seed}/training.npz');h=a['history']; steps=a['checkpoint_steps'];w=a['checkpoint_W']
 last=h[-500:,1]
 row=dict(seed=seed,loss_last500_min=float(last.min()),loss_last500_max=float(last.max()),loss_last500_first100_mean=float(last[:100].mean()),loss_last500_last100_mean=float(last[-100:].mean()),last_checkpoint_encoder_change=float(np.linalg.norm(w[-1]-w[-2])),last_checkpoint_gram_change=float(np.linalg.norm(w[-1].T@w[-1]-w[-2].T@w[-2])),final_tangent_gradient=float(h[-1,3]))
 rows.append(row)
(out/'saved_trajectory_diagnostic.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
