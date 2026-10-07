"""Fixed continuous-activation pilot. No input download or feature extraction."""
from pathlib import Path
import argparse, hashlib, heapq, json, shutil, time
import numpy as np
from scipy.special import ndtr
from scipy.optimize import minimize_scalar

HOME=Path(__file__).resolve().parent
IMPORTANCE=np.array([1.,2./3.])
SLACK=1e-12
GAP=1e-7
EXPANSIONS=20000
TOTAL_SECONDS=300
SEED=20261006

def plain(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [plain(x) for x in v]
    return v

def write(path,v):path.write_text(json.dumps(plain(v),indent=2,allow_nan=False))

def manifest(out):
    write(out/'sha256_manifest.json',{p.relative_to(out).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()
                                    for p in out.rglob('*') if p.is_file() and p.name!='sha256_manifest.json'})

def clean_profile(offset,y,keep_candidates=False):
    """All empirical activation intervals, vertices and kink closures.

    Equal thresholds are grouped. An all-off plateau is retained explicitly.
    Positive weights multiplying a feature do not change its bias minimizer.
    """
    offset=np.asarray(offset,float);y=np.asarray(y,float)
    assert offset.shape==y.shape and offset.ndim==1 and len(y)>0
    assert np.all(np.isfinite(offset)) and np.all(np.isfinite(y)) and np.all(y>=0)
    n=len(y);order=np.argsort(-offset,kind='stable')
    thresholds=-offset[order];o=offset[order];target=y[order]
    unique,start,count=np.unique(thresholds,return_index=True,return_counts=True)
    initial=float(np.mean(y*y));candidates=[dict(beta=float(unique[0]-1),loss=initial,kind='all_off')]
    # Prefix active statistics permit exact quadratic evaluation on each interval.
    d=o-target;sumd=np.cumsum(d);sumd2=np.cumsum(d*d);sumy2=np.cumsum(target*target)
    totaly2=float(np.sum(y*y))
    for j,(lower,first,num) in enumerate(zip(unique,start,count)):
        active=int(first+num);idx=active-1
        upper=float(unique[j+1]) if j+1<len(unique) else None
        vertex=-sumd[idx]/active
        beta=max(float(lower),float(vertex))
        if upper is not None:beta=min(beta,upper)
        value=(sumd2[idx]+2*beta*sumd[idx]+active*beta*beta+totaly2-sumy2[idx])/n
        candidates.append(dict(beta=beta,loss=float(value),kind='interval_vertex',active=active,
                               lower=float(lower),upper=upper))
        # Every kink is present even when the interval vertex is interior.
        value=(sumd2[idx]+2*lower*sumd[idx]+active*lower*lower+totaly2-sumy2[idx])/n
        candidates.append(dict(beta=float(lower),loss=float(value),kind='kink',active=active))
    # Compare exact direct objectives rather than selecting on prefix cancellation.
    for item in candidates:
        item['loss']=float(np.mean((np.maximum(offset+item['beta'],0)-y)**2))
    best=min(candidates,key=lambda z:(z['loss'],z['beta']))
    result=dict(beta=best['beta'],loss=best['loss'])
    if keep_candidates:result['candidates']=candidates
    return result

def selected_loss(x,w,keep=False):
    h=x@w;profiles=[clean_profile(w[i]*h,x[:,i],keep) for i in range(2)]
    return dict(weights=w,loss=float(sum(IMPORTANCE[i]*profiles[i]['loss'] for i in range(2))),
                biases=np.array([v['beta'] for v in profiles]),profiles=profiles)

def clean_selection(x):
    histories=[]
    for size in [256,512]:
        angles=np.arange(size)*np.pi/size
        rows=[]
        for angle in angles:
            w=np.array([np.cos(angle),np.sin(angle)])
            item=selected_loss(x,w)
            rows.append(dict(angle=float(angle),loss=item['loss'],biases=item['biases']))
        best=min(rows,key=lambda v:v['loss']);half=np.pi/(2*size);trace=[]
        def objective(theta):
            angle=float(theta%np.pi);w=np.array([np.cos(angle),np.sin(angle)])
            value=selected_loss(x,w)['loss'];trace.append(dict(angle=angle,loss=value));return value
        refinement=minimize_scalar(objective,bounds=(best['angle']-half,best['angle']+half),
                                   method='bounded',options={'xatol':1e-10,'maxiter':100})
        angle=float(refinement.x%np.pi)
        # A failed or inferior local refinement cannot silently discard a grid incumbent.
        if not refinement.success or refinement.fun>best['loss']:angle=best['angle']
        result=selected_loss(x,np.array([np.cos(angle),np.sin(angle)]),True)
        histories.append(dict(size=size,grid=rows,refinement_trace=trace,
                              refinement_success=bool(refinement.success),result=result))
    orientations=[selected_loss(x,np.eye(2)[i],True) for i in range(2)]
    mono_index=int(np.argmin([v['loss'] for v in orientations]));mono=orientations[mono_index]
    sharing=histories[-1]['result']
    difference=abs(histories[0]['result']['loss']-sharing['loss'])
    gain=mono['loss']-sharing['loss']
    flags=dict(resolution_agreement=difference<=1e-6,
               both_refinements_successful=all(v['refinement_success'] for v in histories),
               resolved_clean_advantage=gain>1e-6,
               mixed_geometry=bool(np.all(np.square(sharing['weights'])>1e-8)))
    return dict(histories=histories,mono_orientations=orientations,mono_orientation=mono_index,
                mono=mono,sharing=sharing,clean_gain=gain,resolution_difference=difference,
                gates=flags,eligible=all(flags.values()))

def moments(mu,sd):
    mu=np.asarray(mu,float)
    if sd==0:
        m=np.maximum(mu,0);return m,m*m
    z=mu/sd;Phi=ndtr(z);phi=np.exp(-.5*z*z)/np.sqrt(2*np.pi)
    m1=mu*Phi+sd*phi;m2=(mu*mu+sd*sd)*Phi+mu*sd*phi
    # Cancellation can produce tiny negative tail moments in floating arithmetic.
    if np.min(m1)<-SLACK or np.min(m2)<-SLACK:raise FloatingPointError('negative Gaussian moment')
    return np.maximum(m1,0),np.maximum(m2,0)

def noisy_objective(beta,offset,y,sd):
    mu=offset+beta;m1,m2=moments(mu,sd)
    f=float(np.mean(m2-2*y*m1+y*y))
    if sd==0:g=2*float(np.mean((mu-y)*(mu>0)))
    else:
        z=mu/sd;phi=np.exp(-.5*z*z)/np.sqrt(2*np.pi)
        g=2*float(np.mean((mu-y)*ndtr(z)+sd*phi))
    return f,g

def calibrate(offset,y,sd,beta_zero,tolerance,deadline):
    offset=np.asarray(offset,float);y=np.asarray(y,float)
    if sd==0:
        profile=clean_profile(offset,y,True)
        return dict(beta=profile['beta'],lower=profile['loss'],upper=profile['loss'],gap=0.,
                    resolved=True,nodes=[],active_heap=[],expansions=0,stop='exact_clean_profile',profile=profile)
    lo=float(-np.max(offset)-12*sd-1);hi=float(np.max(y)-np.min(offset))
    best_beta=float(beta_zero);best=noisy_objective(best_beta,offset,y,sd)[0]
    # Bounded scalar minimization supplies an incumbent only, never global proof.
    incumbent=minimize_scalar(lambda b:noisy_objective(b,offset,y,sd)[0],
                             bounds=(lo,hi),method='bounded',options={'xatol':1e-10,'maxiter':100})
    if incumbent.success and incumbent.fun<best:best_beta=float(incumbent.x);best=float(incumbent.fun)
    upper=best+SLACK
    left_m1=moments(offset+lo,sd)[0]
    far_left=float(np.mean(y*y)-2*np.mean(y*left_m1)-SLACK)
    far_right=noisy_objective(hi,offset,y,sd)[0]-SLACK
    nodes=[];heap=[]
    def add(a,b,parent):
        nonlocal best,best_beta,upper
        mid=(a+b)/2;radius=(b-a)/2;f,g=noisy_objective(mid,offset,y,sd)
        left=offset+a;right=offset+b
        distance=np.where((left<=0)&(right>=0),0,np.minimum(abs(left),abs(right)))
        H=2*(1+float(np.mean(y*np.exp(-.5*(distance/sd)**2)/(sd*np.sqrt(2*np.pi)))))
        lower=max(0.,f-abs(g)*radius-H*radius*radius/2-SLACK)
        if f<best:best=f;best_beta=mid;upper=f+SLACK
        index=len(nodes);nodes.append(dict(id=index,parent=parent,lo=a,hi=b,mid=mid,
                                          f=f,g=g,H=H,lower=lower,upper_after=upper))
        if lower<upper:heapq.heappush(heap,(lower,index,a,b))
    add(lo,hi,None);expansions=0;stop=''
    while True:
        while heap and heap[0][0]>=upper:heapq.heappop(heap)
        lower=min(upper,far_left,far_right,heap[0][0] if heap else upper)
        gap=upper-lower
        if gap<=tolerance:stop='gap_resolved';break
        if expansions>=EXPANSIONS:stop='expansion_limit';break
        if time.monotonic()>=deadline:stop='shared_time_limit';break
        if not heap:stop='exterior_bound_unresolved';break
        _,idx,a,b=heapq.heappop(heap);mid=(a+b)/2;add(a,mid,idx);add(mid,b,idx);expansions+=1
    return dict(beta=best_beta,lower=float(lower),upper=float(upper),gap=float(gap),
                resolved=gap<=tolerance,nodes=nodes,active_heap=[list(v) for v in heap],
                expansions=expansions,stop=stop,left_endpoint=lo,right_endpoint=hi,
                exterior_lower_left=far_left,exterior_lower_right=far_right,
                incumbent_success=bool(incumbent.success),slack=SLACK,tolerance=tolerance)

def per_image_loss(x,w,b,sigma):
    h=x@w;columns=[]
    for i in range(2):
        m1,m2=moments(w[i]*h+b[i],sigma*abs(w[i]))
        columns.append(IMPORTANCE[i]*(m2-2*x[:,i]*m1+x[:,i]*x[:,i]))
    return np.sum(columns,axis=0)

def snapshot(out,features,review):
    folder=out/'source_snapshot';folder.mkdir()
    for source in [Path(__file__),HOME/'vision_transfer_protocol.md',review]:
        shutil.copy2(source,folder/source.name)
    write(out/'input_hashes.json',{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [features,review]})

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--features',type=Path,required=True)
    ap.add_argument('--review',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();assert args.features.is_file() and args.review.is_file()
    out=args.output;out.mkdir(parents=True,exist_ok=False);snapshot(out,args.features,args.review)
    raw=np.load(args.features,allow_pickle=False)
    arrays={key:np.asarray(raw[key],float) for key in ['train','calibration','test']}
    for key,n in [('train',256),('calibration',256),('test',512)]:
        assert arrays[key].shape==(n,512) and np.all(np.isfinite(arrays[key])) and np.all(arrays[key]>=0)
    metadata={key:raw[key].tolist() for key in raw.files if key not in arrays}
    write(out/'input_metadata.json',metadata)
    eligible_channels=np.flatnonzero((np.mean(arrays['train'],axis=0)>0)&(np.var(arrays['train'],axis=0)>0))
    if len(eligible_channels)<2:
        write(out/'stopping_decision.json',dict(stop='insufficient_nonconstant_channels'));manifest(out);return
    channels=eligible_channels[:2];rms=np.sqrt(np.mean(arrays['train'][:,channels]**2,axis=0))
    x={key:value[:,channels]/rms for key,value in arrays.items()}
    zero=np.mean(x['train']==0,axis=0);reference=float(np.sqrt(np.mean(np.var(x['train'],axis=0))))
    settings=dict(channels=channels,rms=rms,zero_fractions=zero,
                  coactivation=float(np.mean(np.all(x['train']>0,axis=1))),importance=IMPORTANCE,
                  sigma_reference=reference,multipliers=[0,.05,.1,.2,.4],seed=SEED,
                  grids=[256,512],loss_resolution_tolerance=1e-6,mixed_energy_threshold=1e-8,
                  calibration_gap=GAP,calibration_slack=SLACK,maximum_expansions=EXPANSIONS,
                  shared_calibration_seconds=TOTAL_SECONDS,bootstrap_replicates=2000)
    write(out/'settings.json',settings)
    np.savez_compressed(out/'normalized_targets.npz',**x)
    clean=clean_selection(x['train']);write(out/'clean_selection.json',clean)
    if not np.any(zero>0) or not clean['eligible']:
        write(out/'stopping_decision.json',dict(stop='mechanism_eligibility_failed',
              zero_support=bool(np.any(zero>0)),clean_gates=clean['gates']));manifest(out);return
    models={name:clean[name] for name in ['sharing','mono']}
    for name,item in models.items():
        h=x['calibration']@item['weights']
        baseline=[clean_profile(item['weights'][i]*h,x['calibration'][:,i],True) for i in range(2)]
        item['zero_calibration_biases']=np.array([v['beta'] for v in baseline])
        write(out/f'{name}_zero_calibration.json',baseline)
    deadline=time.monotonic()+TOTAL_SECONDS;rows=[];raw_losses={};bootstrap_arrays={}
    rng=np.random.default_rng(SEED);indices=rng.integers(0,512,size=(2000,512))
    np.save(out/'bootstrap_indices.npy',indices)
    for j,mult in enumerate(settings['multipliers']):
        sigma=mult*reference;losses={};profiles={}
        folder=out/f'noise_{j}';folder.mkdir()
        for name,item in models.items():
            w=item['weights'];b0=item['zero_calibration_biases'];h=x['calibration']@w
            ledgers=[calibrate(w[i]*h,x['calibration'][:,i],sigma*abs(w[i]),b0[i],
                               GAP/float(np.sum(IMPORTANCE)),deadline) for i in range(2)]
            for i,ledger in enumerate(ledgers):write(folder/f'{name}_feature_{i}.json',ledger)
            b=np.array([v['beta'] for v in ledgers]);profiles[name]=dict(
                calibrated_bias=b,frozen_bias=b0,resolved=all(v['resolved'] for v in ledgers),
                total_gap=float(sum(IMPORTANCE[i]*ledgers[i]['gap'] for i in range(2))))
            losses[name+'_frozen']=per_image_loss(x['test'],w,b0,sigma)
            losses[name+'_calibrated']=per_image_loss(x['test'],w,b,sigma)
            losses[name+'_training_bias_secondary']=per_image_loss(x['test'],w,item['biases'],sigma)
        comparisons=dict(delta_frozen=losses['sharing_frozen']-losses['mono_frozen'],
                         delta_calibrated=losses['sharing_calibrated']-losses['mono_calibrated'])
        comparisons['policy_contrast']=comparisons['delta_calibrated']-comparisons['delta_frozen']
        for name in models:comparisons[name+'_calibration_improvement']=losses[name+'_frozen']-losses[name+'_calibrated']
        summary={}
        for name,values in comparisons.items():
            boots=np.mean(values[indices],axis=1);bootstrap_arrays[f'noise_{j}_{name}']=boots
            summary[name]=dict(mean=float(np.mean(values)),interval95=np.quantile(boots,[.025,.975]))
        raw_losses.update({f'noise_{j}_{name}':values for name,values in {**losses,**comparisons}.items()})
        row=dict(multiplier=mult,sigma=sigma,profiles=profiles,
                 risks={name:float(np.mean(v)) for name,v in losses.items()},comparisons=summary)
        rows.append(row);write(out/'results.json',dict(cases=rows))
        print('sigma multiplier',mult,'delta frozen',summary['delta_frozen']['mean'],
              'delta calibrated',summary['delta_calibrated']['mean'],flush=True)
    np.savez_compressed(out/'per_image_losses.npz',**raw_losses)
    np.savez_compressed(out/'bootstrap_statistics.npz',**bootstrap_arrays)
    write(out/'stopping_decision.json',dict(stop='five_prescribed_levels_completed',
          calibration_all_resolved=all(p['resolved'] for r in rows for p in r['profiles'].values())))
    manifest(out)

if __name__=='__main__':main()
