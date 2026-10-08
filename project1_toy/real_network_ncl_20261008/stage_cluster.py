"""Transfer frozen protocol, implementation and original checkpoints; no job."""
from pathlib import Path
import json, tarfile, hashlib
from remote import remote

ROOT=Path(__file__).resolve().parent
CACHE=Path('C:/Users/indra/.cache/monosemanticity_ncl_20261008')
REMOTE='/scratch/idas3/ncl_native_20261008_v1'
files=['PROTOCOL.md','run_clean_gate.py','clean_gate.sbatch','cluster_bootstrap.sh']
with tarfile.open(CACHE/'cluster_payload.tar','w') as t:
    for name in files:t.add(ROOT/name,arcname=name)
    for p in sorted((CACHE/'checkpoints').glob('*.ckpt')):t.add(p,arcname='checkpoints/'+p.name)
print('Transfer started',flush=True)
r=remote('mkdir -p '+REMOTE+'/logs && tar xf - -C '+REMOTE,(CACHE/'cluster_payload.tar').read_bytes())
print(r.stdout.decode(),flush=True)
r=remote('cd '+REMOTE+' && sha256sum PROTOCOL.md run_clean_gate.py checkpoints/*.ckpt')
print(r.stdout.decode(),flush=True)
(ROOT/'cluster_upload_hashes.txt').write_bytes(r.stdout)
r=remote('cd '+REMOTE+' && nohup bash cluster_bootstrap.sh > logs/bootstrap.log 2>&1 < /dev/null &')
print('Bootstrap launched; no scientific job yet.',flush=True)
