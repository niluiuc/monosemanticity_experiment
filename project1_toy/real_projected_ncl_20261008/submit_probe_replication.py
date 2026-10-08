import datetime,json,sys
from pathlib import Path
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'
for name in ('probe_replication.py','PROBE_REPLICATION_PROTOCOL.md'):
    remote('cat > '+root+'/'+name,(base/name).read_bytes())
batch='''#!/bin/bash
#SBATCH --job-name=ncl_probe_replication
#SBATCH --partition=physics
#SBATCH --account=adshead
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=00:45:00
#SBATCH --no-requeue
#SBATCH --output=/scratch/idas3/ncl_projected_20261008_v1/logs/probe_replication_%j.log
set -euo pipefail
export OMP_NUM_THREADS=8 MKL_NUM_THREADS=8
cd /scratch/idas3/ncl_projected_20261008_v1
runtime/bin/python -u probe_replication.py --root "$PWD"
'''
remote('cat > '+root+'/probe_replication.sbatch',batch.encode())
job=remote('cd '+root+' && sbatch --parsable probe_replication.sbatch').stdout.decode().strip()
record=dict(job=job,submitted_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(base/'PROBE_REPLICATION_JOB.json').write_text(json.dumps(record,indent=2)); print(json.dumps(record))
