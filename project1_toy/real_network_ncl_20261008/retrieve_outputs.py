"""Retrieve scientific outputs, keeping bulky reproducible feature caches on scratch."""
import io,tarfile
from pathlib import Path
from remote import remote
base=Path(__file__).parent; target=base/'outputs'; target.mkdir(exist_ok=True)
command=('tar cf - -C /scratch/idas3/ncl_native_20261008_v1 '
         '--exclude=clean_train_features.npz clean_run_v1 logs/clean-11212169.out '
         'PRE_OUTCOME_AMENDMENT.json protocol_v1_before_amendment')
data=remote(command).stdout
(base/'retrieved_outputs.tar').write_bytes(data)
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for member in archive.getmembers():
        destination=(target/member.name).resolve()
        if not destination.is_relative_to(target.resolve()) or member.issym() or member.islnk():
            raise RuntimeError('Unsafe archive member')
    archive.extractall(target,filter='data')
print('Retrieved outputs; full training feature caches remain on scratch:',target)
