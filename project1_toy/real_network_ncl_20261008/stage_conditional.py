import io,tarfile
from pathlib import Path
from remote import remote
base=Path(__file__).parent
names=['run_prediction.py','run_test.py','run_conditional.py','conditional.sbatch','RUN_STATUS.md']
stream=io.BytesIO()
with tarfile.open(fileobj=stream,mode='w') as tar:
    for name in names: tar.add(base/name,arcname=name)
remote('tar xf - -C /scratch/idas3/ncl_native_20261008_v1',stream.getvalue())
result=remote('cd /scratch/idas3/ncl_native_20261008_v1 && sbatch --parsable --dependency=afterok:11211651 conditional.sbatch')
print(result.stdout.decode(),end='')
