"""Dataset I/O only; no image extraction, model evaluation or test scoring."""
import hashlib
from pathlib import Path
import urllib.request

root = Path('/scratch/idas3/ncl_native_20261008_v1/data')
root.mkdir(exist_ok=True)
target = root / 'cifar-100-python.tar.gz'
partial = target.with_suffix('.partial')
expected = 'eb9058c3a382ffc7106e4002c42a8d85'
if not target.exists():
    urllib.request.urlretrieve('https://www.cs.toronto.edu/~kriz/cifar-100-python.tar.gz', partial)
    actual = hashlib.md5(partial.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f'Dataset MD5 mismatch: {actual}')
    partial.rename(target)
else:
    actual = hashlib.md5(target.read_bytes()).hexdigest()
    if actual != expected:
        raise RuntimeError(f'Existing dataset MD5 mismatch: {actual}')
print(f'Archive downloaded and MD5 verified: {target}', flush=True)
