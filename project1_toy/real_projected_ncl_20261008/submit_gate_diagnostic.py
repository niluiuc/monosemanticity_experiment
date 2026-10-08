import datetime, json, sys
from pathlib import Path
base=Path(__file__).parent
sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'
for name in ('gate_diagnostic.py','GATE_DIAGNOSTIC_PROTOCOL.md'):
    remote('cat > '+root+'/'+name,(base/name).read_bytes())
batch='''#!/bin/bash
#SBATCH --job-name=ncl_gate_diagnostic
#SBATCH --partition=primary
#SBATCH --account=adshead
#SBATCH --constraint=physics
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/idas3/ncl_projected_20261008_v1/logs/gate_diagnostic_%j.log
set -euo pipefail
cd /scratch/idas3/ncl_projected_20261008_v1
runtime/bin/python gate_diagnostic.py --root "$PWD"
'''
# Reuse the actual partition/account directives from the completed clean job.
prior=(base/'clean.sbatch').read_text()
lines=[line for line in prior.splitlines() if line.startswith('#SBATCH') and
       any(v in line for v in ('--partition','--account','--constraint'))]
batch_lines=[line for line in batch.splitlines() if not
    (line.startswith('#SBATCH') and any(v in line for v in ('--partition','--account','--constraint')))]
batch_lines[1:1]=lines
remote('cat > '+root+'/gate_diagnostic.sbatch', ('\n'.join(batch_lines)+'\n').encode())
job=remote('cd '+root+' && sbatch --parsable gate_diagnostic.sbatch').stdout.decode().strip()
record=dict(job=job,submitted_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),post_outcome=True)
(base/'GATE_DIAGNOSTIC_JOB.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record))
