"""Prepare the official CIFAR10 cache within a fresh reproduction package."""
import argparse,os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--download',action='store_true');a=p.parse_args()
root=a.root.resolve();cache=root/'cache/visual_boundary_data';cache.mkdir(parents=True,exist_ok=True)
for name,relative in [('TORCH_HOME','cache/torch'),('HF_HOME','cache/huggingface'),('MPLCONFIGDIR','cache/matplotlib'),('TEMP','tmp'),('TMP','tmp')]:
 target=root/relative;target.mkdir(parents=True,exist_ok=True);os.environ[name]=str(target)
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from torchvision.datasets import CIFAR10
for training in [True,False]:
 d=CIFAR10(str(cache),train=training,download=a.download)
 print('train' if training else 'test',len(d),'cache',cache)
