"""Independent final losses/gradients and every saved Armijo decision."""
from pathlib import Path
import argparse,hashlib,itertools,json,csv
import numpy as np
H=Path(__file__).resolve().parent;R=H/'repair_run_v1'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=H/'independent_repair_review_v1')
O=parser.parse_args().output;O.mkdir(parents=True,exist_ok=False)
manifest=json.loads((R/'sha256_manifest.json').read_text())
for rel,digest in manifest.items():assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==digest,rel
X=np.array(list(itertools.product([0.,1.],repeat=8)));P=np.prod(np.where(X==1,.2,.8),axis=1)
I=2.**(-np.arange(8)/4);rows=[];trials_count=0
for seed in range(5):
    final=np.load(R/f'seed_{seed}/final.npz');W=final['W'];b=final['bias'];Hid=X@W.T;Z=Hid@W+b
    residual=np.maximum(Z,0)-X;loss=float(np.sum(P[:,None]*I*residual**2))
    D=2*P[:,None]*I*residual*(Z>0);g=Hid.T@D+(D@W.T).T@X;gb=D.sum(axis=0)
    tangent=g-(np.sum(g*W)/4)*W;joint=float(np.hypot(np.linalg.norm(tangent),np.linalg.norm(gb)))
    saved=json.loads((R/f'seed_{seed}/results.json').read_text())
    assert abs(loss-saved['final_clean_loss'])<1e-12 and abs(joint-saved['joint_gradient_norm'])<1e-12
    history=np.genfromtxt(R/f'seed_{seed}/history.csv',delimiter=',',names=True)
    trials=np.genfromtxt(R/f'seed_{seed}/backtracking_trials.csv',delimiter=',',names=True)
    assert len(history)==2001 and len(trials)==2000
    with (R/f'seed_{seed}/backtracking_trials.csv').open(newline='') as fh:
        accepted=[row['accepted']=='True' for row in csv.DictReader(fh)]
    assert all(accepted) and np.all(trials['proposal_loss']<=trials['armijo_target'])
    assert np.all(np.diff(history['loss'])<=1e-12) and joint>1e-5
    trials_count+=len(trials)
    rows.append(dict(seed=seed,recomputed_final_loss=loss,recomputed_joint_gradient=joint,
                     gradient_threshold_pass=False,accepted_trials=len(trials),monotone_loss=True))
(O/'results.json').write_text(json.dumps(dict(all_passed=True,hash_checks=len(manifest),armijo_trials_checked=trials_count,cases=rows,
    scope='Saved-trajectory and final-gradient audit only; not convergence/global optimum certification.'),indent=2))
print('Verified',len(manifest),'hashes,10000 Armijo decisions and all5 final losses/gradients; none passes gradient threshold.')
