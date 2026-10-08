"""Frozen-checkpoint native classifier clean gates. No TEST dataset is loaded."""
import argparse, datetime, hashlib, json, math, os, time
from pathlib import Path
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from torchvision.datasets import CIFAR100
from torchvision.models import resnet18
from torchvision.transforms import Compose, ToTensor, Normalize

SEED=20261008
MEAN=(.4914,.4822,.4465); STD=(.247,.243,.261)
NAMES={'CL':'cifar100-simclr-e200-3a7937mb-ep=199.ckpt',
       'NCL':'cifar100-simclr-e200-gelu_relu-jt2gegkm-ep=199.ckpt'}

def digest(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def save(p,d):
    Path(p).write_text(json.dumps(d,indent=2),encoding='utf-8')

def make_backbone(path,device):
    ck=torch.load(path,map_location='cpu',weights_only=True)
    model=resnet18(weights=None)
    model.conv1=nn.Conv2d(3,64,3,stride=1,padding=2,bias=False)
    model.maxpool=nn.Identity(); model.fc=nn.Identity()
    state={k.removeprefix('backbone.'):v for k,v in ck['state_dict'].items() if k.startswith('backbone.')}
    model.load_state_dict(state,strict=True)
    for p in model.parameters():p.requires_grad_(False)
    return model.eval().to(device)

@torch.inference_mode()
def extract(model,dataset,device):
    loader=DataLoader(dataset,batch_size=256,shuffle=False,num_workers=4,pin_memory=True)
    features=[]; labels=[]
    for step,(x,y) in enumerate(loader):
        features.append(model(x.to(device,non_blocking=True)).cpu())
        labels.append(y)
        if step%40==0:print('extract',step,len(loader),flush=True)
    return torch.cat(features),torch.cat(labels)

def fit_probe(features,labels,device,out):
    torch.manual_seed(SEED)
    mean=features.mean(0); std=features.std(0,unbiased=False).clamp_min(1e-6)
    x=((features-mean)/std).to(device); y=labels.to(device)
    head=nn.Linear(512,100).to(device)
    opt=torch.optim.AdamW(head.parameters(),lr=.01,weight_decay=1e-4)
    sched=torch.optim.lr_scheduler.CosineAnnealingLR(opt,T_max=50)
    hist=[]
    for epoch in range(50):
        order=torch.randperm(len(y),device=device); total=0.; correct=0
        for idx in order.split(1024):
            opt.zero_grad(set_to_none=True); logits=head(x[idx]); loss=nn.functional.cross_entropy(logits,y[idx]); loss.backward(); opt.step()
            total+=float(loss.detach())*len(idx); correct+=int((logits.detach().argmax(1)==y[idx]).sum())
        sched.step(); hist.append(dict(epoch=epoch,fit_loss=total/len(y),fit_accuracy=correct/len(y)))
        if epoch%10==0:print('probe',hist[-1],flush=True)
    head.eval(); torch.save(dict(state_dict=head.cpu().state_dict(),mean=mean,std=std),out/'probe.pt')
    save(out/'probe_history.json',hist)
    return head.to(device),mean.to(device),std.to(device)

@torch.inference_mode()
def consistency(features,y):
    f=nn.functional.normalize(features,dim=1)
    active=f.abs()>1e-5
    counts=torch.zeros(100,512,device=f.device)
    counts.index_add_(0,y,active.float())
    denom=counts.sum(0); keep=denom>0
    score=(counts[:,keep].max(0).values/denom[keep]).mean()
    return score, int(keep.sum())

def main():
    a=argparse.ArgumentParser(); a.add_argument('--root',type=Path,required=True); args=a.parse_args()
    root=args.root; out=root/'clean_run_v1'; out.mkdir(exist_ok=False)
    t0=time.time(); device='cuda' if torch.cuda.is_available() else 'cpu'
    torch.set_num_threads(8); torch.manual_seed(SEED); np.random.seed(SEED)
    torch.backends.cuda.matmul.allow_tf32=False; torch.backends.cudnn.allow_tf32=False
    save(out/'provenance.json',dict(start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seed=SEED,device=device,
        gpu=torch.cuda.get_device_name(0) if device=='cuda' else None,torch=torch.__version__,script_sha256=digest(__file__),
        protocol_sha256=digest(root/'PROTOCOL.md'),checkpoint_sha256={m:digest(root/'checkpoints'/n) for m,n in NAMES.items()},images_evaluated='TRAIN only; no TEST'))
    ds=CIFAR100(str(root/'data'),train=True,download=True,transform=Compose([ToTensor(),Normalize(MEAN,STD)]))
    targets=np.array(ds.targets); rng=np.random.default_rng(SEED); fit=[]; val=[]
    for c in range(100):
        ids=rng.permutation(np.flatnonzero(targets==c)); fit.extend(ids[:450]); val.extend(ids[450:])
    fit=np.array(fit); val=np.array(val); np.savez(out/'split_indices.npz',fit=fit,validation=val)
    records={}; acts=[]; errors=[]; yval=torch.tensor(targets[val],device=device)
    for method,name in NAMES.items():
        sub=out/method; sub.mkdir(); model=make_backbone(root/'checkpoints'/name,device)
        f,y=extract(model,ds,device); np.savez(sub/'clean_train_features.npz',features=f.numpy(),labels=y.numpy())
        head,mean,std=fit_probe(f[fit],y[fit],device,sub)
        fv=f[val].to(device)
        with torch.inference_mode():
            logits=head((fv-mean)/std); err=(logits.argmax(1)!=yval)
            sc,nd=consistency(fv,yval)
        np.savez(sub/'validation_predictions.npz',logits=logits.cpu().numpy(),errors=err.cpu().numpy(),labels=yval.cpu().numpy())
        records[method]=dict(validation_error=float(err.float().mean()),semantic_consistency=float(sc),active_dimensions=nd,
            raw_sparsity_below_point01=float((fv.abs()<.01).float().mean()))
        acts.append(fv); errors.append(err.float()); print(method,records[method],flush=True)
        del model,head,f; torch.cuda.empty_cache() if device=='cuda' else None
    generator=torch.Generator(device=device).manual_seed(SEED+1)
    error_boot=[]; sc_boot=[]; base=torch.arange(5000,device=device).view(100,50)
    for b in range(2000):
        choice=torch.randint(0,50,(100,50),generator=generator,device=device)
        idx=base.gather(1,choice).reshape(-1)
        error_boot.append(float((errors[1][idx]-errors[0][idx]).mean()))
        if b<200:
            sc_boot.append(float(consistency(acts[1][idx],yval[idx])[0]-consistency(acts[0][idx],yval[idx])[0]))
    error_ci=np.quantile(error_boot,[.025,.975]).tolist(); sc_ci=np.quantile(sc_boot,[.025,.975]).tolist()
    passed=error_ci[0]>0 and sc_ci[0]>0
    result=dict(models=records,delta_error=records['NCL']['validation_error']-records['CL']['validation_error'],
        delta_consistency=records['NCL']['semantic_consistency']-records['CL']['semantic_consistency'],
        error_difference_ci95=error_ci,consistency_difference_ci95=sc_ci,
        clean_gates_passed=bool(passed),decision='PASS to conditional prediction stage' if passed else 'STOP fixed checkpoint pair: clean prerequisites failed',
        elapsed_seconds=time.time()-t0,test_images_evaluated=0,
        limitations='One checkpoint and one probe per condition; intervals are conditional paired image bootstraps, not training-seed or causal uncertainty.')
    np.savez(out/'bootstrap_draws.npz',error_difference=np.array(error_boot),consistency_difference=np.array(sc_boot))
    save(out/'results.json',result); print(json.dumps(result,indent=2),flush=True)
    save(out/'completed.json',dict(end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),success=True))

if __name__=='__main__': main()
