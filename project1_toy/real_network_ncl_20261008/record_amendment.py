"""Preserve original protocol/code, then install a documented pre-outcome amendment."""
import json
from pathlib import Path
from remote import remote
base=Path(__file__).parent; root='/scratch/idas3/ncl_native_20261008_v1'
guard="""import datetime,json,shutil,hashlib
from pathlib import Path
r=Path('/scratch/idas3/ncl_native_20261008_v1')
assert not (r/'clean_run_v1').exists(), 'Clean experiment has started: amendment forbidden'
b=r/'protocol_v1_before_amendment'; b.mkdir(exist_ok=False)
names=['PROTOCOL.md','run_prediction.py','run_test.py','run_conditional.py']
for n in names: shutil.copy2(r/n,b/n)
record=dict(amendment_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),scientific_images_scored=0,
original_sha256={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in names},
reason='Measure the fixed native corruption curve after clean prerequisites pass, even if the affine prediction fails. Failed prediction gates still reject the predictive claim. No scientific settings or grid expansion.')
(r/'PRE_OUTCOME_AMENDMENT.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
"""
result=remote('/sw/apps/anaconda3/2024.10/bin/python -',guard.encode()).stdout
(base/'PRE_OUTCOME_AMENDMENT.json').write_bytes(result)
(base/'PROTOCOL_v1_before_amendment.md').write_bytes(remote('cat '+root+'/protocol_v1_before_amendment/PROTOCOL.md').stdout)
for name in ('PROTOCOL.md','run_prediction.py','run_test.py','run_conditional.py'):
    remote('cat > '+root+'/'+name,(base/name).read_bytes())
print(result.decode())
