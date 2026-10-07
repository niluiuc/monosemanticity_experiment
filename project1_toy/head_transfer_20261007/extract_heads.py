"""One fixed class-mapped forward pass; no score selection or reconstruction fit."""
from pathlib import Path
import hashlib, json, os, shutil, time

HERE=Path(__file__).resolve().parent
ASSEMBLY=HERE.parent/'paper_assembly_20261006'
CACHE=Path('C:/Users/indra/.cache/monosemanticity_vision_20261006')
EXPECTED_CHECKPOINT='f37072fd47e89c5e827621c5baffa7500819f7896bbacec160b1a16c560e07ec'

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def write(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')

def main():
    start=time.monotonic();out=HERE/'extraction_run_v1'
    out.mkdir(parents=True,exist_ok=False)
    snapshot=out/'source_snapshot';snapshot.mkdir()
    for source in [Path(__file__),ASSEMBLY/'head_transfer_protocol.md',ASSEMBLY/'head_transfer_design_review.md']:
        assert source.is_file();shutil.copy2(source,snapshot/source.name)
    os.environ['TORCH_HOME']=str(CACHE/'weights')
    import numpy as np
    import torch,torchvision
    from torchvision.datasets import CIFAR10
    from torchvision.models import ResNet18_Weights,resnet18
    torch.set_num_threads(4);torch.set_num_interop_threads(1)
    weights=ResNet18_Weights.IMAGENET1K_V1;categories=weights.meta['categories']
    assert [categories[281],categories[207]]==['tabby','golden retriever']
    checkpoint=CACHE/'weights/hub/checkpoints/resnet18-f37072fd.pth'
    assert checkpoint.is_file() and sha(checkpoint)==EXPECTED_CHECKPOINT
    transform=weights.transforms();dataset=CIFAR10(root=str(CACHE/'data'),train=True,download=False)
    model=resnet18(weights=weights,progress=False).eval()
    for p in model.parameters():p.requires_grad_(False)
    indices=np.random.default_rng(20261007).permutation(len(dataset))[:4608]
    np.save(out/'image_indices.npy',indices)
    write(out/'categories.json',categories)
    metadata=dict(status='started',checkpoint_sha256=sha(checkpoint),checkpoint_url=weights.url,
        dataset_archive_sha256=sha(CACHE/'data'/CIFAR10.filename),
        ids=[281,207],names=['tabby','golden retriever'],seed=20261007,
        feature_definition='rectify fixed class logits at zero; not concept absence',
        split_sizes=[256,256,4096],transform=repr(transform),
        torch=torch.__version__,torchvision=torchvision.__version__,numpy=np.__version__,
        batch_size=32,threads=4,max_seconds=1200)
    write(out/'provenance.json',metadata)
    logits=[];labels=[]
    try:
        with torch.inference_mode():
            for begin in range(0,len(indices),32):
                if time.monotonic()-start>=1200:raise TimeoutError('Fixed extraction budget exhausted')
                samples=[dataset[int(i)] for i in indices[begin:begin+32]]
                batch=torch.stack([transform(im) for im,_ in samples])
                values=model(batch).cpu().numpy()
                assert values.shape==(len(samples),1000) and np.isfinite(values).all()
                logits.append(values.copy());labels.extend(int(y) for _,y in samples)
                if begin%256==0:print('Extracted',begin+len(samples),'of',len(indices),'elapsed',round(time.monotonic()-start,1),flush=True)
        raw=np.concatenate(logits);targets=np.maximum(raw[:,[281,207]],0).astype(np.float64)
        np.savez_compressed(out/'targets.npz',train=targets[:256],calibration=targets[256:512],test=targets[512:],
            train_indices=indices[:256],calibration_indices=indices[256:512],test_indices=indices[512:],
            train_labels=np.asarray(labels[:256]),calibration_labels=np.asarray(labels[256:512]),test_labels=np.asarray(labels[512:]))
        metadata['status']='complete'
    except Exception as e:
        metadata.update(status='failed',error_type=type(e).__name__,error=str(e));raise
    finally:
        if logits:
            np.save(out/'raw_logits.npy',np.concatenate(logits));np.save(out/'labels.npy',np.asarray(labels,dtype=np.int64))
        metadata.update(elapsed_seconds=time.monotonic()-start,images_completed=len(labels))
        write(out/'provenance.json',metadata)
        write(out/'sha256_manifest.json',{p.relative_to(out).as_posix():sha(p) for p in out.rglob('*') if p.is_file() and p.name!='sha256_manifest.json'})

if __name__=='__main__':main()
