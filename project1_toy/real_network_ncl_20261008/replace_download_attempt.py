from pathlib import Path
from remote import remote
base=Path(__file__).parent; root='/scratch/idas3/ncl_native_20261008_v1'
remote('scancel 11212068')
# Preserve the provenance-only attempt and incomplete archive. Refuse if any features/results exist.
code="""from pathlib import Path
r=Path('/scratch/idas3/ncl_native_20261008_v1').resolve()
o=r/'clean_run_v1'
assert all(p.name=='provenance.json' for p in o.iterdir()), 'Scientific files present; do not replace this run'
assert (r/'data/cifar-100-python.tar.gz').stat().st_size<169001437, 'Archive may be complete; inspect first'
o.rename(r/'clean_download_only_attempt_11212068')
(r/'data/cifar-100-python.tar.gz').rename(r/'clean_download_only_attempt_11212068/incomplete_archive.gz')
print('Preserved download-only attempt; no features or results existed')
"""
remote('/sw/apps/anaconda3/2024.10/bin/python -',code.encode())
for name in ('wait_for_archive.py','clean_gate_prefetched.sbatch'):
    remote('cat > '+root+'/'+name,(base/name).read_bytes())
job=remote('cd '+root+' && sbatch --parsable clean_gate_prefetched.sbatch').stdout.decode().strip()
remote('scontrol update JobId=11211781 Dependency=afterok:'+job)
print('Replacement clean job:',job)
