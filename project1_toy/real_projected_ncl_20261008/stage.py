import io,json,sys,tarfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/'real_network_ncl_20261008'))
from remote import remote
base=Path(__file__).parent; root='/scratch/idas3/ncl_projected_20261008_v1'
code="""import datetime,json
from pathlib import Path
r=Path('/scratch/idas3/ncl_projected_20261008_v1'); r.mkdir(exist_ok=False)
p=Path('/scratch/idas3/ncl_native_20261008_v1')
assert not (p/'test_run_v1').exists() and not (p/'prediction_run_v1').exists()
for n in ['data','checkpoints','runtime']: (r/n).symlink_to(p/n,target_is_directory=True)
(r/'logs').mkdir()
record=dict(protocol_registration_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
projected_features_computed=0,test_images_scored=0,prior_backbone_result='Both prerequisites failed; retained',
source_justification='Anchor linear forward explicitly uses projector and NCL ReLU; predecessor main_eval scores z.')
(r/'REGISTRATION.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))
"""
registration=remote('/sw/apps/anaconda3/2024.10/bin/python -',code.encode()).stdout
(base/'REGISTRATION.json').write_bytes(registration)
stream=io.BytesIO()
with tarfile.open(fileobj=stream,mode='w') as archive:
    for path in base.iterdir():
        if path.is_file(): archive.add(path,arcname=path.name)
remote('tar xf - -C '+root,stream.getvalue())
clean=remote('cd '+root+' && sbatch --parsable clean.sbatch').stdout.decode().strip()
conditional=remote('cd '+root+' && sbatch --parsable --dependency=afterok:'+clean+' conditional.sbatch').stdout.decode().strip()
record=dict(clean_job=clean,conditional_job=conditional,scratch_root=root)
(base/'JOBS.json').write_text(json.dumps(record,indent=2)); print(json.dumps(record))
