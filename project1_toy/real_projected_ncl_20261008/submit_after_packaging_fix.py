import json,sys
from pathlib import Path
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'
for name in ('clean.sbatch','conditional.sbatch'):
    data=(base/name).read_bytes().replace(b'\r\n',b'\n'); (base/name).write_bytes(data)
    remote('cat > '+root+'/'+name,data)
clean=remote('cd '+root+' && sbatch --parsable clean.sbatch').stdout.decode().strip()
conditional=remote('cd '+root+' && sbatch --parsable --dependency=afterok:'+clean+' conditional.sbatch').stdout.decode().strip()
record=dict(clean_job=clean,conditional_job=conditional,scratch_root=root)
(base/'JOBS.json').write_text(json.dumps(record,indent=2)); print(json.dumps(record))
