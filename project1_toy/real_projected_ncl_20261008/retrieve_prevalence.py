import io,json,sys,tarfile
from pathlib import Path
import numpy as np
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'; target=base/'outputs'
data=remote('tar cf - -C '+root+' prevalence_check_v1 logs/prevalence_11212722.log').stdout
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for m in archive.getmembers():
        if m.issym() or m.islnk() or not (target/m.name).resolve().is_relative_to(target.resolve()): raise RuntimeError('Unsafe archive')
    archive.extractall(target,filter='data')
out=target/'prevalence_check_v1'; d=json.loads((out/'results.json').read_text()); selections={}
def score(a,y):
    counts=np.zeros((100,a.shape[1]),dtype=np.int64)
    np.add.at(counts,y,a.astype(np.int64)); totals=counts.sum(0); keep=totals>0
    return float(np.mean(counts[:,keep].max(0)/totals[keep]))
for m in ('CL','NCL'):
    a=np.load(out/(m+'_selection.npz')); selections[m]=a['active']; y=a['labels']
    assert np.all(a['active'].sum(0)==d['k'])
    assert abs(score(a['active'],y)-d['methods'][m]['matched_purity'])<1e-12
    assert abs(score(a['original_active'],y)-d['methods'][m]['original_purity'])<1e-12
ids=np.stack([np.flatnonzero(y==c) for c in range(100)])
rng=np.random.default_rng(20261023); draws=[]
for _ in range(200):
    indices=ids[np.arange(100)[:,None],rng.integers(0,50,(100,50))].reshape(-1)
    draws.append(score(selections['NCL'][indices],y[indices])-score(selections['CL'][indices],y[indices]))
assert np.max(np.abs(np.array(draws)-np.load(out/'bootstrap.npz')['draws']))<1e-12
assert np.max(np.abs(np.quantile(draws,[.025,.975])-d['conditional_ci95']))<1e-12
(out/'independent_verification.json').write_text(json.dumps(dict(passed=True,
    checks=['equal per-coordinate activation count','majority-class purity via independent bincount','all bootstrap draws','conditional intervals'],
    limitations='Selection ranks are not regenerated here; full feature cache remains on cluster.'),indent=2))
print(json.dumps(d,indent=2)); print('Independent saved-selection verification passed.')
