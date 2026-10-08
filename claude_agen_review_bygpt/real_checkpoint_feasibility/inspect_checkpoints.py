"""Inspect public checkpoint provenance/architecture; do not evaluate images."""
from pathlib import Path
import hashlib, json
import requests
import torch

ROOT = Path(__file__).resolve().parent
CACHE = Path('C:/Users/indra/.cache/monosemanticity_ncl_20261008')
COMMIT = '880b3ceace102d1b04132ca371eb773faffdf54e'
FILES = {
    'CL': ('146YDJ8C0P4DCBYOiC-8qPrM6A0r2hcbE', 'cifar100-simclr-e200-3a7937mb-ep=199.ckpt'),
    'NCL': ('1b0k2rBs2EYvbq9q0shNY7LrtqRKzwtia', 'cifar100-simclr-e200-gelu_relu-jt2gegkm-ep=199.ckpt'),
}

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(1<<20), b''):
            h.update(data)
    return h.hexdigest()

def summarize(value, depth=0):
    if depth > 3:
        return str(type(value))
    if value is None or isinstance(value,(str,int,float,bool)):
        return value
    if isinstance(value,dict):
        return {str(k):summarize(v,depth+1) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [summarize(v,depth+1) for v in value[:30]]
    return str(type(value))

def main():
    source_dir = CACHE/'official_source'
    source_dir.mkdir(parents=True,exist_ok=True)
    sources = []
    for rel in ['main_eval.py','main_linear.py','solo/methods/simclr.py',
                'solo/methods/base.py','scripts/pretrain/cifar/ncl.yaml',
                'scripts/pretrain/cifar/simclr.yaml','scripts/linear/cifar/simclr.yaml']:
        url = f'https://raw.githubusercontent.com/PKU-ML/non_neg/{COMMIT}/{rel}'
        r = requests.get(url,timeout=30)
        r.raise_for_status()
        dest = source_dir/rel
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes(r.content)
        sources.append(dict(path=rel,url=url,sha256=sha(dest)))
    records = []
    for method,(drive_id,name) in FILES.items():
        path = CACHE/'checkpoints'/name
        rec = dict(method=method,drive_id=drive_id,name=name,bytes=path.stat().st_size,sha256=sha(path))
        try:
            checkpoint = torch.load(path,map_location='cpu',weights_only=True)
            state = checkpoint.get('state_dict',{})
            rec.update(load_mode='weights_only=True',keys=list(checkpoint),
                       epoch=checkpoint.get('epoch'),global_step=checkpoint.get('global_step'),
                       hyper_parameters=summarize(checkpoint.get('hyper_parameters',{})),
                       state_keys=list(state),
                       state_shapes={k:list(v.shape) for k,v in state.items() if isinstance(v,torch.Tensor)},
                       state_tensor_elements=sum(v.numel() for v in state.values() if isinstance(v,torch.Tensor)))
        except Exception as e:
            rec.update(load_mode='weights_only=True failed; unsafe loading not attempted',error=str(e))
        records.append(rec)
    report = dict(question='Are the two official CIFAR100 checkpoints present and loadable, and what evaluation architecture do they contain?',
                  connection_to_project1='Prerequisite for testing mono-versus-sharing classification robustness in the actual network; no compressor or corruption test here.',
                  stopping_rule='Inspect the two listed checkpoints and pinned source only. No image evaluation, replacement dataset, checkpoint search, or retraining.',
                  repository='https://github.com/PKU-ML/non_neg',commit=COMMIT,
                  checkpoints=records,sources=sources,images_evaluated=0)
    (ROOT/'checkpoint_inventory.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in {'sources','checkpoints'}}))
    print(json.dumps([{k:v for k,v in x.items() if k not in {'state_keys','state_shapes','hyper_parameters'}} for x in records],indent=2))

if __name__ == '__main__':
    main()
