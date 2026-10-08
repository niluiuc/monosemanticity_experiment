import json,hashlib,itertools,time,shutil,copy
from pathlib import Path
import numpy as np
import torch
from scipy.special import ndtr
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
H=Path(__file__).parent;ROOT=H.parents[1];O=H/'run_v1';O.mkdir(exist_ok=False)
def savejson(path,obj):path.write_text(json.dumps(obj,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
shutil.copyfile(__file__,O/'source_snapshot.py');shutil.copyfile(H/'PROTOCOL.md',O/'PROTOCOL.md')
# Stage existing data on D:, never download or write to its C: source.
cache=ROOT/'cache/visual_boundary_data';cache.mkdir(parents=True,exist_ok=True)
src=Path('C:/Users/indra/.cache/monosemanticity_vision_20261006/data/cifar-10-batches-py')
if not (cache/'cifar-10-batches-py').exists():shutil.copytree(src,cache/'cifar-10-batches-py')
from torchvision.datasets import CIFAR10
trainset=CIFAR10(str(cache),train=True,download=False);testset=CIFAR10(str(cache),train=False,download=False)
torch.set_num_threads(4);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
B=np.array(list(itertools.product([0.,1.],repeat=5)));cnt=B.sum(1);prob=.2**cnt*.8**(5-cnt)
a=2*np.pi*np.arange(5)/5;V=np.array([np.cos(a),np.sin(a)]);pent=V*np.sqrt(2/5)
mono=np.zeros((2,5));mono[0,0]=mono[1,1]=1
modelspec=[('sharing',pent,V,np.full(5,np.sqrt(2/5)/2)),('mono',mono,mono,np.array([.5,.5,0,0,0]))]
rng=np.random.default_rng(20261029);order=rng.permutation(len(trainset.data));ids=dict(train=order[:64],calibration=order[64:96],test=rng.permutation(len(testset.data))[:128])
np.savez_compressed(O/'split_ids.npz',**ids)
def render(data,ids,seed):
 rng=np.random.default_rng(seed);yy,xx=np.mgrid[:32,:32];out=[]
 centres=[(6,6),(16,6),(26,6),(9,23),(23,23)]
 for idx in ids:
  gray=data[int(idx)].astype(np.float32).mean(2)/255;base=np.repeat((.05+.20*gray)[None,:,:],3,axis=0)
  masks=[];intens=rng.uniform(.75,.95,5)
  for i,(cx,cy) in enumerate(centres):
   dx,dy=rng.integers(-1,2,2);x=xx-cx-dx;y=yy-cy-dy
   if i==0:mask=x*x+y*y<=9
   elif i==1:mask=(abs(x)<=1)&(abs(y)<=3)
   elif i==2:mask=((abs(x)<=1)&(abs(y)<=3))|((abs(y)<=1)&(abs(x)<=3))
   elif i==3:mask=(x*x+y*y<=12)&(x*x+y*y>=5)
   else:mask=(y>=-3)&(y<=3)&(abs(x)<=(y+3)/2)
   masks.append(mask)
  for b in B:
   image=base.copy()
   for i in np.flatnonzero(b):image[:,masks[i]]=intens[i]
   out.append(image)
 return np.stack(out).astype(np.float32)
def model():return torch.nn.Sequential(torch.nn.Conv2d(3,8,5,2,2),torch.nn.ReLU(),torch.nn.Conv2d(8,16,3,2,1),torch.nn.ReLU(),torch.nn.Flatten(),torch.nn.Linear(1024,32),torch.nn.ReLU(),torch.nn.Linear(32,2))
def infer(net,x):
 net.eval()
 with torch.inference_mode():return np.concatenate([net(torch.from_numpy(x[i:i+128])).numpy() for i in range(0,len(x),128)]).reshape(-1,32,2).astype(float)
X=render(trainset.data,ids['train'],20261033);C=render(trainset.data,ids['calibration'],20261034)
np.savez_compressed(O/'development_images.npz',train=X,calibration=C,states=B)
torch.manual_seed(20261030);initial=copy.deepcopy(model().state_dict());codes={};history={};complete=True
for name,W,dirs,t in modelspec:
 net=model();net.load_state_dict(initial);optim=torch.optim.Adam(net.parameters(),lr=.005)
 targets=np.tile(B@W.T,(len(ids['train']),1)).astype(np.float32);weights=np.tile(32*prob,len(ids['train'])).astype(np.float32)
 x=torch.from_numpy(X);y=torch.from_numpy(targets);weight=torch.from_numpy(weights);generator=torch.Generator().manual_seed(20261035);hist=[];start=time.monotonic();timed=False
 for ep in range(80):
  net.train();order=torch.randperm(len(x),generator=generator);total=0
  for i in range(0,len(x),128):
   if time.monotonic()-start>=300:timed=True;break
   batch=order[i:i+128];optim.zero_grad();loss=((net(x[batch])-y[batch])**2).sum(1);loss=(loss*weight[batch]).mean()
   if not torch.isfinite(loss):raise FloatingPointError('Nonfinite training loss')
   loss.backward();optim.step();total+=float(loss.detach())*len(batch)
  hist.append(dict(epoch=ep+1,loss=total/len(x),seconds=time.monotonic()-start,completed=not timed));savejson(O/f'{name}_history.json',hist)
  if timed:break
 torch.save(net.state_dict(),O/f'{name}_model.pt');codes[name]=infer(net,C);history[name]=hist
 np.savez_compressed(O/f'{name}_calibration.npz',codes=codes[name],states=B)
 complete&=not timed;print(name,'epochs',len(hist),'loss',hist[-1]['loss'],'timeout',timed,flush=True)
P=np.arange(2,33)*.025;S=np.arange(1,61)*.025
def perstate(code,dirs,t,s,name):
 scores=code@dirs
 if s==0:e=(scores>t)!=B[None,:,:]
 else:e=ndtr(-(2*B[None,:,:]-1)*(scores-t)/s)
 if name=='mono':e[:,:,2:]=B[None,:,2:]
 return e.sum(2)
def curves(code_dict):
 out=np.empty((len(S),len(P)));pr=P[None,:]**cnt[:,None]*(1-P[None,:])**(5-cnt[:,None])
 for i,s in enumerate(S):
  vals=[]
  for name,W,dirs,t in modelspec:vals.append(perstate(code_dict[name],dirs,t,s,name).mean(0))
  out[i]=(vals[0]-vals[1])@pr
 return out
ideal={name:(B@W.T)[None,:,:] for name,W,v,t in modelspec};ip=curves(ideal);cp=curves(codes)
def p2curve(cd,s):
 vals=[perstate(cd[name],v,t,s,name).mean(0)@prob for name,W,v,t in modelspec];return float(vals[0]-vals[1])
def roots(cd):
 grid=np.r_[0,S];g=[p2curve(cd,s) for s in grid];return [float(brentq(lambda s:p2curve(cd,s),l,h)) for l,h,gl,gh in zip(grid[:-1],grid[1:],g[:-1],g[1:]) if gl*gh<0]
prediction=dict(ideal_roots=roots(ideal),calibration_roots=roots(codes),calibration_clean_gap=p2curve(codes,0),training_complete=complete,calibration_code_rms={name:float(np.sqrt(np.mean(np.sum((codes[name]-(B@W.T)[None,:,:])**2,axis=2)))) for name,W,v,t in modelspec})
passed=complete and prediction['calibration_clean_gap']<0 and len(prediction['calibration_roots'])>0
prediction['prerequisites_passed']=passed
np.savez_compressed(O/'prediction.npz',ideal_gap=ip,calibration_gap=cp,p=P,sigma=S)
savejson(O/'prediction.json',prediction)
freeze={p.name:sha(p) for p in [H/'run.py',H/'PROTOCOL.md',O/'prediction.npz',O/'prediction.json',O/'sharing_model.pt',O/'mono_model.pt']};savejson(O/'frozen_prediction_hashes.json',dict(hashes=freeze,time_ns=time.time_ns()))
print('prediction',prediction,flush=True)
if not passed:
 savejson(O/'result.json',dict(status='prerequisite_failed',prediction=prediction,test_not_scored=True));raise SystemExit(0)
# Only after immutable prediction registration, construct and score TEST.
T=render(testset.data,ids['test'],20261036);np.savez_compressed(O/'test_images.npz',images=T,states=B)
tc={}
for name,W,v,t in modelspec:
 net=model();net.load_state_dict(torch.load(O/f'{name}_model.pt',weights_only=True));tc[name]=infer(net,T);np.savez_compressed(O/f'{name}_test_codes.npz',codes=tc[name],states=B)
noise=np.random.default_rng(20261031).normal(size=(128,32,16,2));np.savez_compressed(O/'test_noise.npz',noise=noise)
losses=np.empty((len(S),128,32));pr=P[None,:]**cnt[:,None]*(1-P[None,:])**(5-cnt[:,None])
for i,s in enumerate(S):
 errs=[]
 for name,W,v,t in modelspec:
  pred=(tc[name][:,:,None,:]+s*noise)@v>t
  if name=='mono':pred[:,:,:,2:]=False
  errs.append((pred!=B[None,:,None,:]).sum(3).mean(2))
 losses[i]=errs[0]-errs[1]
mc=losses.mean(1)@pr;clean=p2curve(tc,0);p2=losses@prob;mean=p2.mean(1)
brackets=[S[i:i+2].tolist() for i in range(len(S)-1) if mean[i]*mean[i+1]<0]
cross_mid=(sum(brackets[0])/2) if brackets else None
prediction_error=abs(cross_mid-prediction['calibration_roots'][0]) if cross_mid is not None else None
success=bool(clean<0 and brackets and prediction_error<=.05)
# Background-level bootstrap, conditional on one trained pair.
rng=np.random.default_rng(20261032);boot=[];cleanbg=np.array([p2curve({name:tc[name][j:j+1] for name,_,_,_ in modelspec},0) for j in range(128)])
for _ in range(256):
 take=rng.integers(0,128,128);g=p2[:,take].mean(1);bs=[(S[i]+S[i+1])/2 for i in range(len(S)-1) if g[i]*g[i+1]<0];boot.append((float(cleanbg[take].mean()),bs[0] if bs else np.nan))
boot=np.array(boot);np.savez_compressed(O/'test_results.npz',p=P,sigma=S,state_background_gaps=losses,simulation_gap=mc,test_exact_gap=curves(tc),clean_background_gap=cleanbg,bootstrap=boot)
result=dict(status='complete',clean_gap_p02=clean,observed_crossing_brackets_p02=brackets,calibration_prediction_error=prediction_error,ideal_prediction_error=abs(cross_mid-prediction['ideal_roots'][0]) if cross_mid is not None else None,quantitative_transfer_passed=success,clean_gap_interval=np.quantile(boot[:,0],[.025,.975]).tolist(),bootstrap_resolved_count=int(np.isfinite(boot[:,1]).sum()),bootstrap_crossing_interval=np.nanquantile(boot[:,1],[.025,.975]).tolist() if np.isfinite(boot[:,1]).any() else None,prediction=prediction,scope='Controlled semi-synthetic visual bottleneck; imposed code targets and code noise, not natural monosemanticity or pixel corruption.')
savejson(O/'result.json',result)
fig,ax=plt.subplots(figsize=(8,5.5),constrained_layout=True);im=ax.pcolormesh(P,S,mc,cmap='RdBu_r',vmin=-1,vmax=1,shading='auto');ax.contour(P,S,ip,levels=[0],colors='black',linewidths=2);ax.contour(P,S,cp,levels=[0],colors='green',linestyles='--',linewidths=2)
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([0],[0],color='black',label='Ideal formula'),Line2D([0],[0],color='green',linestyle='--',label='Calibration prediction')]);ax.set(xlabel='Evaluation concept frequency p',ylabel='Gaussian bottleneck-noise sigma',title='Held-out image CNN: sharing minus mono detection error');fig.colorbar(im,ax=ax,label='Simulated risk difference');fig.savefig(O/'visual_boundary_heatmap.png',dpi=180)
savejson(O/'sha256.json',{p.name:sha(p) for p in O.iterdir() if p.is_file() and p.name!='sha256.json'})
print(json.dumps(result,indent=2),flush=True)
