from pathlib import Path
from remote import remote
root=Path(__file__).resolve().parent
r=remote('cat > /scratch/idas3/ncl_native_20261008_v1/cluster_bootstrap.sh',(root/'cluster_bootstrap.sh').read_bytes())
r=remote('nohup bash /scratch/idas3/ncl_native_20261008_v1/cluster_bootstrap.sh > /scratch/idas3/ncl_native_20261008_v1/logs/bootstrap.log 2>&1 < /dev/null &')
print('Isolated runtime setup started with a lock to prevent duplicate installation.')
