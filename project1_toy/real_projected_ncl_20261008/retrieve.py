import io,sys,tarfile
from pathlib import Path
base=Path(__file__).parent; sys.path.insert(0,str(base.parent/'real_network_ncl_20261008'))
from remote import remote
root='/scratch/idas3/ncl_projected_20261008_v1'; target=base/'outputs'; target.mkdir(exist_ok=True)
command='tar cf - -C '+root+' --exclude=clean_train_features.npz clean_run_v1 prediction_run_v1 test_run_v1 logs REGISTRATION.json'
data=remote(command).stdout
(base/'retrieved_outputs.tar').write_bytes(data)
with tarfile.open(fileobj=io.BytesIO(data)) as archive:
    for m in archive.getmembers():
        if m.issym() or m.islnk() or not (target/m.name).resolve().is_relative_to(target.resolve()):
            raise RuntimeError('Unsafe archive member')
    archive.extractall(target,filter='data')
print('Retrieved complete scientific outputs; full feature caches remain on scratch.')
