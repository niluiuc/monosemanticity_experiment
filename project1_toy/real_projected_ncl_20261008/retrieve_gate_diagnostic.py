import io,json,sys,tarfile
from pathlib import Path
import numpy as np
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'
data=remote('tar cf - -C '+root+' gate_diagnostic_v1 logs/gate_diagnostic_11212585.log').stdout
target=base/'outputs'
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for m in archive.getmembers():
        if m.issym() or m.islnk() or not (target/m.name).resolve().is_relative_to(target.resolve()):
            raise RuntimeError('Unsafe archive')
    archive.extractall(target,filter='data')
out=target/'gate_diagnostic_v1'; reported=json.loads((out/'results.json').read_text()); checks=[]
for method in ('CL','NCL'):
    a=np.load(out/(method+'_logits.npz')); actual=a['actual_logits'].astype(float); clean=a['clean_logits'].astype(float)
    labels=a['labels'][:,None]; inc=actual-clean; inc-=inc.mean(-1,keepdims=True)
    actual_error=float(np.mean(actual.argmax(-1)!=labels))
    for key in ('full_affine_logits','backbone_affine_logits'):
        v=a[key].astype(float); r=actual-v; r-=r.mean(-1,keepdims=True)
        error=float(np.mean(v.argmax(-1)!=labels)); relative=float(np.sqrt(np.mean(r*r)/np.mean(inc*inc)))
        old=reported['methods'][method]['comparisons'][key]
        assert abs(error-old['error'])<1e-12
        assert abs(relative-old['relative_rms'])<1e-6
        assert (abs(error-actual_error)<=.02 and relative<=.25)==old['gate_passed']
        checks.append(dict(method=method,approximation=key,error=error,
            error_discrepancy=abs(error-actual_error),relative_rms=relative,gate_passed=old['gate_passed']))
(out/'independent_verification.json').write_text(json.dumps(dict(checks=checks,passed=True),indent=2))
print(json.dumps(reported,indent=2)); print('Independent saved-logit recomputation passed.')
