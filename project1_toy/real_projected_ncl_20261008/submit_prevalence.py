import datetime,json,sys
from pathlib import Path
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'
for name in ('prevalence_check.py','PREVALENCE_PROTOCOL.md'):
    remote('cat > '+root+'/'+name,(base/name).read_bytes())
batch='''#!/bin/bash
#SBATCH --job-name=ncl_prevalence
#SBATCH --partition=physics
#SBATCH --account=adshead
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:10:00
#SBATCH --output=/scratch/idas3/ncl_projected_20261008_v1/logs/prevalence_%j.log
set -euo pipefail
cd /scratch/idas3/ncl_projected_20261008_v1
runtime/bin/python -u prevalence_check.py --root "$PWD"
'''
remote('cat > '+root+'/prevalence.sbatch',batch.encode())
job=remote('cd '+root+' && sbatch --parsable prevalence.sbatch').stdout.decode().strip()
r=dict(job=job,submitted_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(base/'PREVALENCE_JOB.json').write_text(json.dumps(r,indent=2)); print(json.dumps(r))
