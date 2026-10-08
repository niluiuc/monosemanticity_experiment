"""Wait for the already-running dataset prefetch; do not download or score images."""
import hashlib,time
from pathlib import Path
archive=Path('/scratch/idas3/ncl_native_20261008_v1/data/cifar-100-python.tar.gz')
while not archive.exists(): time.sleep(20)
with archive.open('rb') as file:
    h=hashlib.md5()
    for block in iter(lambda:file.read(1<<20),b''): h.update(block)
if h.hexdigest()!='eb9058c3a382ffc7106e4002c42a8d85':
    raise RuntimeError('Prefetched archive checksum failed; no experiment started.')
print('Prefetched archive verified; starting unchanged clean experiment.',flush=True)
