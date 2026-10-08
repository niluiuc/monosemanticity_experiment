import io,json,sys,tarfile
from pathlib import Path
import numpy as np
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'; target=base/'outputs'
data=remote('tar cf - -C '+root+' probe_replication_v1 logs/probe_replication_11212673.log').stdout
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for m in archive.getmembers():
        if m.issym() or m.islnk() or not (target/m.name).resolve().is_relative_to(target.resolve()): raise RuntimeError('Unsafe archive')
    archive.extractall(target,filter='data')
out=target/'probe_replication_v1'; record=json.loads((out/'results.json').read_text())
seeds=record['seeds']; errors={}
for method in ('CL','NCL'):
    scores=[]
    for seed in seeds:
        a=np.load(out/str(seed)/method/'test_scores.npz'); labels=a['labels']; scores.append(a['errors'].mean(1))
        v=np.load(out/str(seed)/method/'validation.npz')
        assert np.array_equal(v['logits'].argmax(1)!=v['labels'],v['errors'])
        assert abs(float(v['errors'].mean())-record['validation_errors'][f'{seed}_{method}'])<1e-7
    errors[method]=np.stack(scores)
delta=errors['NCL']-errors['CL']; points=delta.mean(1)
ids=np.stack([np.flatnonzero(labels==c) for c in range(100)])
rng=np.random.default_rng(20261021); draws=[]
for _ in range(2000):
    selected=ids[np.arange(100)[:,None],rng.integers(0,100,(100,100))].reshape(-1)
    draws.append(delta[:,selected,:].mean(1))
draws=np.array(draws); bands=np.quantile(draws,[.025/4,1-.025/4],axis=0)
assert np.max(np.abs(points-record['delta_NCL_minus_CL']))<1e-12
assert np.max(np.abs(bands[0]-record['simultaneous_lower']))<1e-12
assert np.max(np.abs(bands[1]-record['simultaneous_upper']))<1e-12
assert np.max(np.abs(draws-np.load(out/'bootstrap.npz')['draws']))<1e-12
passed=bool(np.all(bands[0,:,0]>0) and np.all(bands[1,:,1]<0))
assert passed==record['probe_stability_gate_passed']
(out/'independent_verification.json').write_text(json.dumps(dict(passed=True,probe_stability_gate_passed=passed,
    checks=['validation argmax/errors','TEST differences','all 2000 paired bootstrap draws','simultaneous bands','stopping decision']),indent=2))
print(json.dumps(record,indent=2)); print('Independent replication-output verification passed.')
