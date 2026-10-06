"""Independent final-population loss/support/trace checks; no training."""
import argparse,hashlib,itertools,json,math
from pathlib import Path
import numpy as np
H=Path(__file__).resolve().parent;R=H/'clean_run_v1'
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=H/'independent_clean_review_v1')
O=parser.parse_args().output;O.mkdir(parents=True,exist_ok=False)
manifest=json.loads((R/'sha256_manifest.json').read_text())
for rel,digest in manifest.items():
    assert hashlib.sha256((R/rel).read_bytes()).hexdigest()==digest,rel
x=np.array(list(itertools.product([0.,1.],repeat=8)));P=np.prod(np.where(x==1,.2,.8),axis=1)
I=2.**(-np.arange(8)/4);checks=[]
for seed in range(5):
    data=np.load(R/f'seed_{seed}/final.npz');raw=json.loads((R/f'seed_{seed}/results.json').read_text())
    W=data['W'];beta=data['bias'];prediction=np.maximum(x@W.T@W+beta,0)
    loss=float(np.sum(P[:,None]*I*(prediction-x)**2))
    history=np.genfromtxt(R/f'seed_{seed}/history.csv',delimiter=',',names=True)
    assert len(history)==5001 and np.allclose(np.sum(W*W),4,atol=1e-12)
    assert abs(loss-raw['raw_clean_loss'])<1e-12
    change=abs(history['loss'][-100:].mean()-history['loss'][-200:-100].mean())
    assert abs(change-raw['diagnostics']['window_mean_loss_change'])<1e-12
    norms=np.linalg.norm(W,axis=0);Q=float(4/(3*math.sqrt(2*math.pi))*sum(I*.2/norms))
    checks.append(dict(seed=seed,independent_loss=loss,saved_loss=raw['raw_clean_loss'],
                       energy=float(np.sum(W*W)),loss_stability_pass=bool(change<=1e-5),
                       full_support=bool(np.all(norms>0)),minimum_column_norm=float(norms.min()),Q=Q))
(O/'results.json').write_text(json.dumps(dict(hash_checks=len(manifest),checks=checks,all_passed=True,
    scope='Independent recomputation of saved final losses/energy/stability/support constants; no stationarity or global geometry certificate.'),indent=2))
print('Verified',len(manifest),'hashes and all5 final losses; no stability passes.')
